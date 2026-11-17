"""Rendiconto del protocollo DGS-07 per il collaudo del metodo IA-02 (adottato dal titolare «così com'è», D-25).

Legge il file dei limiti grezzi prodotto da `pilota_ia02 --limiti` e applica il protocollo SENZA scelte: conteggi
E, P, B, I per metodo, margine Δ e cella; controlli con Clopper–Pearson unilaterale superiore; classifica della
fase 1; verdetto della fase 2 con inventario dei semi e diagnostica dei 216 confronti fra flussi (§2b).
Solo dati inventati. Impegno: `laboratorio/studi/IMPEGNO-PROTOCOLLO-IA02.md`.

Uso:
  fase 1:  python3 -s -B -m brain.laboratorio.studi.protocollo_ia02 --limiti limiti_fase1.json --fase 1
  fase 2:  python3 -s -B -m brain.laboratorio.studi.protocollo_ia02 --limiti limiti_fase2.json --fase 2 \\
               --candidato bootstrap:0.01
"""
import argparse
import hashlib
import json
import math
import sys

from . import pilota_ia02 as P
from .collaudo_ia02 import _cdf_binomiale, clopper_pearson

SOGLIA = 0.15
TASSO = 0.025
MARGINI = (0.0, 0.01, 0.025, 0.05)
CELLE_CONFINE = (2, 6, 9, 11)
CELLE_SOTTO = (1, 5)
CELLE_POTENZA = (3, 7, 10, 12)
DELTA = {1: 0.05, 2: 0.001}                    # limite unilaterale 95% in fase 1, 99,9% in fase 2
M_FASE2 = 12000
BANDA = (4796, 5204)
N_BIT = 10000


def ucp(k: int, M: int, delta: float) -> float:
    """Limite superiore unilaterale di Clopper–Pearson: il p con P[Bin(M, p) ≤ k] = δ (BetaQuantile(1−δ; k+1, M−k))."""
    if k >= M:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if _cdf_binomiale(k, M, mid) > delta:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def k_massimo(M: int, delta: float) -> int:
    """Il k più grande con U_CP(k, M; δ) ≤ 0,025, cioè P[Bin(M; 0,025) ≤ k] ≤ δ; −1 se nemmeno k = 0 basta."""
    k = -1
    while k + 1 < M and _cdf_binomiale(k + 1, M, TASSO) <= delta:
        k += 1
    return k


def prob_passare(p: float, M: int, k: int) -> float:
    return _cdf_binomiale(k, M, p)


def _soglie(margine: float) -> tuple:
    return round(SOGLIA + margine, 10), round(SOGLIA - margine, 10)


def _intervallo_ammesso(iv) -> bool:
    if iv is None:
        return True
    if not isinstance(iv, list) or len(iv) != 2 or not all(isinstance(x, (int, float)) for x in iv):
        return False
    return P.intervallo_valido(float(iv[0]), float(iv[1])) is not None


def conta(limiti: list, margine: float) -> dict:
    alto, basso = _soglie(margine)
    c = {"E": 0, "P": 0, "B": 0, "I": 0}
    for iv in limiti:
        if iv is None:
            c["E"] += 1
        elif iv[0] > alto:
            c["P"] += 1
        elif iv[1] < basso:
            c["B"] += 1
        else:
            c["I"] += 1
    return c


def valuta(dati: dict, fase: int) -> dict:
    """{(metodo, margine): {completa, celle, controlli, potenze, ammissibile}} per i metodi presenti nel file."""
    M = dati["repliche"]
    delta = DELTA[fase]
    kmax = k_massimo(M, delta)
    celle = dati.get("celle", {})
    metodi = [m for m in P.METODI if any(m in v for v in celle.values())]
    esito = {}
    for metodo in metodi:
        completa = all(str(c) in celle and isinstance(celle[str(c)].get(metodo), list)
                       and len(celle[str(c)][metodo]) == M
                       and all(_intervallo_ammesso(iv) for iv in celle[str(c)][metodo]) for c in P.CELLE)
        for margine in MARGINI:
            per_cella, controlli, potenze = {}, [], {}
            if completa:
                for c in P.CELLE:
                    n = conta(celle[str(c)][metodo], margine)
                    per_cella[c] = dict(M=M, **n, kp=n["P"] + n["E"], km=n["B"] + n["E"])
                for c in CELLE_SOTTO + CELLE_CONFINE:
                    k = per_cella[c]["kp"]
                    controlli.append(("falsa promozione", c, k, ucp(k, M, delta), k <= kmax))
                for c in CELLE_CONFINE:
                    k = per_cella[c]["km"]
                    controlli.append(("falsa bocciatura", c, k, ucp(k, M, delta), k <= kmax))
                potenze = {c: per_cella[c]["P"] for c in CELLE_POTENZA}
            ammissibile = completa and all(x[4] for x in controlli) and all(v >= 1 for v in potenze.values())
            esito[(metodo, margine)] = {"completa": completa, "celle": per_cella, "controlli": controlli,
                                        "potenze": potenze, "ammissibile": ammissibile, "kmax": kmax}
    return esito


def seleziona(valutazione: dict):
    """Classifica di DGS-07 §2a.5: max min(P), poi max somma, poi Δ più piccolo, poi HAC; None = STOP."""
    ammessi = [(k, v) for k, v in valutazione.items() if v["ammissibile"]]
    if not ammessi:
        return None
    ordine = sorted(ammessi, key=lambda kv: (-min(kv[1]["potenze"].values()), -sum(kv[1]["potenze"].values()),
                                             kv[0][1], P.METODI.index(kv[0][0])))
    return ordine[0][0]


def verdetto_fase2(valutazione: dict, candidato: tuple, diagnostica_ok: bool) -> tuple:
    cause = []
    v = valutazione.get(candidato)
    if v is None:
        return "NON CONFERMATO", [f"candidato {candidato} assente dal file"]
    if not v["completa"]:
        cause.append("corsa incompleta o non valida")
    else:
        M = next(iter(v["celle"].values()))["M"]
        if M != M_FASE2:
            cause.append(f"repliche registrate {M} invece di {M_FASE2} (12.000)")
        for nome, c, k, u, passa in v["controlli"]:
            if not passa:
                cause.append(f"{nome} nella cella {c}: k = {k} > {v['kmax']} (U_CP = {u:.10f})")
        for c, p in v["potenze"].items():
            if p < 1:
                cause.append(f"nessuna promozione nella cella di potenza {c}")
    if not diagnostica_ok:
        cause.append("controllo dei flussi non superato (inventario dei semi o 216 confronti)")
    return ("CONFERMATO NEL DOMINIO DEL PILOTA" if not cause else "NON CONFERMATO"), cause


def p_bilaterale(x: int, n: int = N_BIT) -> float:
    basso = _cdf_binomiale(x, n, 0.5)
    alto = 1.0 if x <= 0 else 1 - _cdf_binomiale(x - 1, n, 0.5)
    return min(1.0, 2 * min(basso, alto))


def banda(n: int, soglia: float) -> tuple:
    """Il più piccolo e il più grande X che NON segnalano (p > soglia)."""
    lo = next(x for x in range(n + 1) if p_bilaterale(x, n) > soglia)
    hi = next(x for x in range(n, -1, -1) if p_bilaterale(x, n) > soglia)
    return lo, hi


def _bit(fase: int, cella: int, replica: int, componente: int) -> list:
    r = P.flusso(fase, cella, replica, componente)                  # copia appena inizializzata
    return [1 if r.random() >= 0.5 else 0 for _ in range(N_BIT + 2)]


def diagnostica_flussi() -> list:
    """I 216 confronti di DGS-07 §2b (gruppi A, B, C; ritardi −1, 0, +1; t = 1…10.000)."""
    coppie = []
    for c in P.CELLE:
        coppie.append(("A", c, (1, 1, 0), (2, 1, 0)))
        for f in (1, 2):
            coppie.append(("B", c, (f, 1, 0), (f, 2, 0)))
        for g in (1, 2, 3):
            coppie.append(("C", c, (1, 1, 0), (1, 1, g)))
    out = []
    for gruppo, c, primo, secondo in coppie:
        a = _bit(primo[0], c, primo[1], primo[2])
        b = _bit(secondo[0], c, secondo[1], secondo[2])
        for h in (-1, 0, 1):
            x = sum(1 for t in range(1, N_BIT + 1) if a[t] == b[t + h])
            out.append({"gruppo": gruppo, "cella": c, "primo": primo, "secondo": secondo, "h": h, "X": x,
                        "segnala": not BANDA[0] <= x <= BANDA[1]})
    return out


def inventario_semi(fasi: dict) -> dict:
    """Tutte le chiavi (fase, cella, replica, componente) delle fasi date: i semi devono essere tutti distinti."""
    semi = set()
    n = 0
    for fase, M in fasi.items():
        for c in P.CELLE:
            for r in range(1, M + 1):
                for g in range(4):
                    semi.add(hashlib.sha256(f"{P.MASTER}:{fase}:{c}:{r}:{g}".encode()).digest())
                    n += 1
    return {"chiavi": n, "semi_distinti": len(semi)}


def _fmt(x: float) -> str:
    return f"{x:g}".replace(".", ",")


def tabella(valutazione: dict, fase: int) -> str:
    righe = [f"| metodo | Δ | cella | M | E | P | B | I | k⁺ | k⁻ | potenza P/M (CP 95% bilaterale, descrittivo) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for (metodo, margine), v in valutazione.items():
        if not v["completa"]:
            righe.append(f"| {metodo} | {_fmt(margine)} | — | corsa INCOMPLETA o non valida: non valutabile |"
                         " | | | | | | |")
            continue
        for c, n in v["celle"].items():
            lo, hi = clopper_pearson(n["P"], n["M"])
            righe.append(f"| {metodo} | {_fmt(margine)} | {c} | {n['M']} | {n['E']} | {n['P']} | {n['B']} | {n['I']}"
                         f" | {n['kp']} | {n['km']} | {n['P'] / n['M']:.4f} ({lo:.4f}–{hi:.4f}) |")
    righe += ["", "| metodo | Δ | controllo | cella | k | U_CP | esito |", "|---|---|---|---|---|---|---|"]
    for (metodo, margine), v in valutazione.items():
        for nome, c, k, u, passa in v["controlli"]:
            righe.append(f"| {metodo} | {_fmt(margine)} | {nome} | {c} | {k} | {u:.10f} | "
                         f"{'passa' if passa else 'NON passa'} |")
    return "\n".join(righe)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--limiti", required=True)
    a.add_argument("--fase", type=int, required=True, choices=(1, 2))
    a.add_argument("--candidato", help="metodo:margine, solo in fase 2 (es. hac:0.01)")
    x = a.parse_args(argv)
    with open(x.limiti, encoding="utf-8") as f:
        dati = json.load(f)
    if dati.get("fase") != x.fase:
        print(f"ERRORE: il file è della fase {dati.get('fase')}, non della fase {x.fase}", file=sys.stderr)
        return 2
    v = valuta(dati, x.fase)
    kmax = k_massimo(dati["repliche"], DELTA[x.fase])
    print(f"Protocollo DGS-07, fase {x.fase}: M = {dati['repliche']}, δ = {DELTA[x.fase]}, controllo passa se "
          f"k ≤ {kmax} (U_CP ≤ 0,025). Versione del pilota: {dati.get('versione')}.\n")
    print(tabella(v, x.fase))
    print()
    if x.fase == 1:
        sel = [(k[0], _fmt(k[1]), min(e["potenze"].values()), sum(e["potenze"].values()))
               for k, e in v.items() if e["ammissibile"]]
        print("Ammissibili (metodo, Δ, min P, somma P): " + ("; ".join(map(str, sel)) if sel else "nessuno"))
        s = seleziona(v)
        print(f"Candidato scelto: {s[0]}, margine {_fmt(s[1])} R" if s else
              "STOP: nessun candidato ammissibile, nessuna fase 2 (DGS-07 §2a.5)")
        return 0
    if not x.candidato:
        print("ERRORE: in fase 2 serve --candidato metodo:margine", file=sys.stderr)
        return 2
    metodo, margine = x.candidato.split(":")
    inv = inventario_semi({1: 3000, 2: M_FASE2})
    conf = diagnostica_flussi()
    segnalati = [c for c in conf if c["segnala"]]
    ok = inv["chiavi"] == inv["semi_distinti"] and not segnalati
    print(f"Inventario dei semi (fasi 1 e 2): {inv['chiavi']} chiavi, {inv['semi_distinti']} semi distinti.")
    print(f"Diagnostica dei flussi: 216 confronti, banda {BANDA[0]}…{BANDA[1]}, segnalati {len(segnalati)}"
          + (": " + "; ".join(f"{c['gruppo']} cella {c['cella']} {c['primo']}~{c['secondo']} h={c['h']} X={c['X']}"
                              for c in segnalati) if segnalati else "") + ".")
    esito, cause = verdetto_fase2(v, (metodo, float(margine)), ok)
    print(f"Esito: {esito}" + ("" if not cause else " — cause: " + "; ".join(cause)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
