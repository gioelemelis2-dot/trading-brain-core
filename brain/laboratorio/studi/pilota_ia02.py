"""Pilota del collaudo del test IA-02 nel disegno del DGS (DGS-06 §2c), 17/11/2026, eseguito su delega del titolare.

SOLO numeri inventati. È SVILUPPO DEL METODO, non certificazione: serve a scegliere metodo, margine e costi prima di
una validazione indipendente su repliche nuove. Nessuno screening o veto di H-002: si valuta l'intervallo isolato.

Disegno (proposte del DGS, applicate alla lettera salvo dove indicato):
- D = 1.000 sedute; quote a = b = 0,025; σ marginale = 1,25 R; soglia c = +0,15 R.
- 12 celle: 1–4 gaussiano iid (μ 0,10; 0,15; 0,20; 0,30); 5–8 AR(1) ρ = 0,25 (stesse μ); 9–10 conteggi casuali
  K_d ∈ {0, 1, 3} (prob. 0,25; 0,5; 0,25) con componente giornaliera AR(1) e innovazioni individuali (μ 0,15; 0,20);
  11–12 perdite rare iid q = 0,01 (μ 0,15; 0,20).
- Coppie giornaliere (S_d, K_d); stimatore μ̂ = ΣS/ΣK.
- HAC: e_d = S_d − μ̂K_d, Bartlett con L = ⌊4(D/100)^(2/9)⌋ = 6, SE = √(V/(D·K̄²)), limiti μ̂ ± z(0,975)·SE.
- Bootstrap: circolare a blocchi ℓ = 10, D/ℓ = 100 blocchi, B = 3.999, intervallo BASIC
  [2μ̂ − Q(0,975), 2μ̂ − Q(0,025)], quantile di rango ⌈p·B⌉ senza interpolazione; un ricampionamento con ΣK = 0 fa
  fallire la replica (errore, non promozione).
- M = 3.000 repliche per cella; stessi dati per i due metodi (confronti appaiati).
DIFFERENZA DICHIARATA: il progetto usa solo la libreria standard, quindi niente PCG64/SeedSequence di NumPy. Ogni
flusso è un random.Random con seme = SHA-256 della tupla (master, fase, cella, replica, componente); componenti:
0 dati iid/AR o componente comune Z, 1 conteggi K, 2 innovazioni individuali, 3 bootstrap. Master 2026111706.

Uso:
  benchmark (fase 0, 30 repliche per cella):  python3 -s -B -m brain.laboratorio.studi.pilota_ia02 --fase 0 --repliche 30
  pilota    (fase 1, 3.000 repliche):         python3 -s -B -m brain.laboratorio.studi.pilota_ia02 --fase 1 --repliche 3000
"""
import argparse
import hashlib
import json
import math
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from statistics import NormalDist

from .collaudo_ia02 import clopper_pearson

MASTER = 2026111706
D = 1000
SIGMA = 1.25
SOGLIA = 0.15
A = 0.025
Z = NormalDist().inv_cdf(1 - A)
RHO = 0.25
Q_RARE = 0.01
BLOCCO = 10
CELLE = {1: ("iid", 0.10), 2: ("iid", 0.15), 3: ("iid", 0.20), 4: ("iid", 0.30),
         5: ("ar1", 0.10), 6: ("ar1", 0.15), 7: ("ar1", 0.20), 8: ("ar1", 0.30),
         9: ("conteggi", 0.15), 10: ("conteggi", 0.20), 11: ("rare", 0.15), 12: ("rare", 0.20)}


def flusso(fase: int, cella: int, replica: int, componente: int, master: int = MASTER) -> random.Random:
    chiave = f"{master}:{fase}:{cella}:{replica}:{componente}".encode()
    return random.Random(int.from_bytes(hashlib.sha256(chiave).digest(), "big"))


def _ar1(n: int, rnd: random.Random) -> list:
    z = [rnd.gauss(0.0, 1.0)]                                          # inizio stazionario
    s = math.sqrt(1 - RHO * RHO)
    for _ in range(n - 1):
        z.append(RHO * z[-1] + s * rnd.gauss(0.0, 1.0))
    return z


def genera(cella: int, fase: int, replica: int) -> list:
    """D coppie (S_d, K_d) della replica. Non si ricentra la media realizzata."""
    tipo, mu = CELLE[cella]
    r0 = flusso(fase, cella, replica, 0)
    if tipo == "iid":
        return [(mu + SIGMA * r0.gauss(0.0, 1.0), 1) for _ in range(D)]
    if tipo == "ar1":
        return [(mu + SIGMA * z, 1) for z in _ar1(D, r0)]
    if tipo == "rare":
        scala = SIGMA / math.sqrt(Q_RARE * (1 - Q_RARE))
        return [(mu + scala * (Q_RARE - (1 if r0.random() < Q_RARE else 0)), 1) for _ in range(D)]
    rk, ri = flusso(fase, cella, replica, 1), flusso(fase, cella, replica, 2)
    zc = _ar1(D, r0)
    coppie = []
    for d in range(D):
        u = rk.random()
        k = 0 if u < 0.25 else (1 if u < 0.75 else 3)
        s = sum(mu + SIGMA * (math.sqrt(0.5) * zc[d] + math.sqrt(0.5) * ri.gauss(0.0, 1.0)) for _ in range(k))
        coppie.append((float(s), k))
    return coppie


def impronta_modulo() -> str:
    """SHA-256 di questo file: identifica la versione che ha prodotto un file di limiti (DGS-07 §2a.1)."""
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def intervallo_valido(lo: float, hi: float):
    """Contratto di DGS-06 §2c: limiti non finiti, invertiti o di ampiezza nulla sono errori (non stimabilità)."""
    if not (math.isfinite(lo) and math.isfinite(hi)) or not lo < hi:
        return None
    return lo, hi


def ritardi_predefiniti(d: int) -> int:
    return math.floor(4 * (d / 100) ** (2 / 9))


def intervallo_hac(coppie: list, ritardi: int = None):
    """(L, U) con HAC di Bartlett sul rapporto ΣS/ΣK; None se non stimabile (denominatore o varianza nulli)."""
    n = len(coppie)
    sk = sum(k for _, k in coppie)
    if sk == 0:
        return None
    mu = sum(s for s, _ in coppie) / sk
    e = [s - mu * k for s, k in coppie]
    L = ritardi_predefiniti(n) if ritardi is None else ritardi
    v = sum(x * x for x in e) / n
    for h in range(1, L + 1):
        v += 2 * (1 - h / (L + 1)) * sum(e[d] * e[d - h] for d in range(h, n)) / n
    kbar = sk / n
    if not v > 0 or not math.isfinite(v):
        return None
    se = math.sqrt(v / (n * kbar * kbar))
    return intervallo_valido(mu - Z * se, mu + Z * se)


def medie_bootstrap(coppie: list, rnd: random.Random, ricampionamenti: int, blocco: int = BLOCCO):
    """Medie μ* = ΣS*/ΣK* del bootstrap circolare a blocchi; None se un ricampionamento ha ΣK* = 0."""
    n = len(coppie)
    estese = coppie + coppie[:blocco - 1]                               # circolare
    cs, ck = [0.0], [0]
    for s, k in estese:
        cs.append(cs[-1] + s)
        ck.append(ck[-1] + k)
    blocchi = n // blocco
    medie = []
    for _ in range(ricampionamenti):
        ts = tk = 0
        for _ in range(blocchi):
            i = rnd.randrange(n)
            ts += cs[i + blocco] - cs[i]
            tk += ck[i + blocco] - ck[i]
        if tk == 0:
            return None
        medie.append(ts / tk)
    return medie


def intervallo_bootstrap(coppie: list, rnd: random.Random, ricampionamenti: int = 3999, blocco: int = BLOCCO):
    sk = sum(k for _, k in coppie)
    if sk == 0:
        return None
    medie = medie_bootstrap(coppie, rnd, ricampionamenti, blocco)
    if medie is None:
        return None
    mu = sum(s for s, _ in coppie) / sk
    o = sorted(medie)
    q = lambda p: o[math.ceil(p * ricampionamenti) - 1]              # noqa: E731
    return intervallo_valido(2 * mu - q(1 - A), 2 * mu - q(A))


METODI = ("hac", "bootstrap")


def esegui_cella(cella: int, fase: int, repliche: int, ricampionamenti: int = 3999, metodi: tuple = METODI) -> dict:
    mu = CELLE[cella][1]
    out = {"cella": cella, "tipo": CELLE[cella][0], "mu": mu, "repliche": repliche, "secondi": {},
           "limiti": {m: [] for m in metodi}}
    conta = {m: {"promosse": 0, "bocciate": 0, "attraversamenti": 0, "errori": 0, "coperture": 0, "ampiezze": [],
                 "stime": []} for m in metodi}
    tempi = {m: 0.0 for m in metodi}
    for r in range(1, repliche + 1):
        coppie = genera(cella, fase, r)
        for metodo in metodi:
            t0 = time.perf_counter()
            iv = intervallo_hac(coppie) if metodo == "hac" else \
                intervallo_bootstrap(coppie, flusso(fase, cella, r, 3), ricampionamenti)
            tempi[metodo] += time.perf_counter() - t0
            out["limiti"][metodo].append(None if iv is None else [iv[0], iv[1]])
            c = conta[metodo]
            if iv is None:
                c["errori"] += 1
                continue
            lo, hi = iv
            c["promosse" if lo > SOGLIA else ("bocciate" if hi < SOGLIA else "attraversamenti")] += 1
            c["coperture"] += lo <= mu <= hi
            c["ampiezze"].append(hi - lo)
            c["stime"].append((lo + hi) / 2 if metodo == "hac" else None)
    for metodo, c in conta.items():
        a = sorted(c.pop("ampiezze"))
        stime = [x for x in c.pop("stime") if x is not None]
        c["ampiezza_mediana"] = a[len(a) // 2] if a else None
        c["distorsione"] = (sum(stime) / len(stime) - mu) if stime else None
        out[metodo] = c
        out["secondi"][metodo] = tempi[metodo]
    return out


def _riga(r: dict, metodo: str) -> str:
    c, M = r[metodo], r["repliche"]
    lo, hi = clopper_pearson(c["promosse"], M)
    lob, hib = clopper_pearson(c["bocciate"], M)
    peggio = (c["promosse"] + c["errori"]) / M
    return (f"| {r['cella']} | {r['tipo']} | {r['mu']:+.2f} | {metodo} | {c['promosse']}/{M} ({c['promosse'] / M:.2%}; "
            f"{lo:.2%}–{hi:.2%}) | {c['bocciate']}/{M} ({lob:.2%}–{hib:.2%}) | {c['attraversamenti']} | "
            f"{c['errori']} (con errori {peggio:.2%}) | {c['coperture'] / M:.1%} | "
            f"{(c['ampiezza_mediana'] or 0):.3f} | {r['secondi'][metodo] / M * 1000:.1f} ms |")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--fase", type=int, default=1)
    p.add_argument("--repliche", type=int, default=3000)
    p.add_argument("--ricampionamenti", type=int, default=3999)
    p.add_argument("--celle", default=",".join(map(str, CELLE)))
    p.add_argument("--processi", type=int, default=4)
    p.add_argument("--metodi", default=",".join(METODI))
    p.add_argument("--limiti", help="file JSON dove salvare i limiti grezzi per replica (DGS-07 §2a.1)")
    x = p.parse_args(argv)
    celle = [int(c) for c in x.celle.split(",")]
    metodi = tuple(m for m in METODI if m in x.metodi.split(","))
    if x.fase != 1 or x.repliche < 3000:
        print(f"ATTENZIONE: fase {x.fase}, {x.repliche} repliche: questo NON è il pilota impegnato (fase 1, 3.000 "
              f"repliche per cella).\n")
    t0 = time.time()
    if x.processi > 1:
        with ProcessPoolExecutor(max_workers=x.processi) as ex:
            ris = list(ex.map(esegui_cella, celle, [x.fase] * len(celle), [x.repliche] * len(celle),
                              [x.ricampionamenti] * len(celle), [metodi] * len(celle)))
    else:
        ris = [esegui_cella(c, x.fase, x.repliche, x.ricampionamenti, metodi) for c in celle]
    if x.limiti:
        with open(x.limiti, "w", encoding="utf-8") as f:
            json.dump({"versione": impronta_modulo(), "fase": x.fase, "repliche": x.repliche,
                       "ricampionamenti": x.ricampionamenti, "master": MASTER,
                       "celle": {str(r["cella"]): r["limiti"] for r in sorted(ris, key=lambda r: r["cella"])}},
                      f, sort_keys=True)
    print(f"Pilota IA-02 (DGS-06 §2c): D = {D}, a = b = {A}, soglia +{SOGLIA}, master {MASTER}, fase {x.fase}, "
          f"B = {x.ricampionamenti}. Intervalli: Clopper–Pearson bilaterali DESCRITTIVI al 95%.\n")
    print("| cella | generatore | μ vera | metodo | L > 0,15 (intervallo) | U < 0,15 (intervallo) | attraversano | "
          "errori | copertura di μ | ampiezza mediana | tempo/replica |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in ris:
        for metodo in metodi:
            print(_riga(r, metodo))
    print(f"\nLettura: sotto e al confine (μ ≤ 0,15) «L > 0,15» è falsa promozione; sopra è potenza. Al confine «U < 0,15» "
          f"è falsa bocciatura. Nessuna certificazione. Tempo totale {time.time() - t0:.0f} s.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
