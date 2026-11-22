"""Controlli decisionali e statistici aperti (DGS-15 punto 5), 22/11/2026. Solo dati inventati, nessuna rete.

1. D-47: screening con potenza stimata esattamente 50% (passa) e appena sotto (non passa).
2. #123: lo stesso requisito «fallito» come descrittivo (non cambia l'esito) e come vincolante per promuovere (lo cambia).
3. #124: medie del modulo contro il riferimento in frazioni, all'uguaglianza e a ±1 ulp dalla soglia.
4. Potenza replica per replica alla media vera +0,25 R: repliche avviate M, segnali favorevoli F, promozioni P,
   scarto (F−P)/M, promozioni senza segnale favorevole nella stessa replica (devono essere 0), intervalli esatti
   (Clopper-Pearson al 95%) con invalide e inconclusive nel denominatore.
5. D-44: limiti superiori esatti unilaterali al 99,9% per 107, 2 e 3 eventi avversi su 12.000.
Uso (dalla radice): python3 -s -B brain/laboratorio/ricevute/2026-11-22-percorso-127/controlli_aperti.py [M]
"""
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from brain.laboratorio.studi import pilota_ia02 as P                    # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V               # noqa: E402

CTX = {"registro": "registro_prove.json", "n_prove": 1, "impronta": "ab" * 32}
M = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
out = {"python": sys.version.split()[0]}


def costanti(media, n, delta=0.1):
    s = [media + delta] * (n // 2) + [media - delta] * (n - n // 2)
    random.Random(7).shuffle(s)
    return [(x, 1) for x in s]


# 1. D-47
out["D-47"] = {"potenza 0.50": V.screening(costanti(0.6, 780), 9, 0.50)["ammessa"],
               "potenza 0.4999999999999999": V.screening(costanti(0.6, 780), 9, 0.4999999999999999)["ammessa"]}

# 2. #123
su = costanti(0.6, 1000)
desc = V.verdetto(su, 5, [{"id": "costi", "veto": False, "descrittivo": True, "esito": "fallito"}], contesto=CTX)
vinc = V.verdetto(su, 5, [{"id": "costi", "veto": False, "esito": "fallito"}], contesto=CTX)
out["#123"] = {"descrittivo fallito": [desc["esito"], desc["segnale"]],
               "vincolante per promuovere fallito": [vinc["esito"], vinc["segnale"]],
               "riga nel rapporto (descrittivo)": [r for r in V.rapporto(desc).splitlines() if "costi" in r]}


# 3. #124: uguaglianza e ±1 ulp, media dello screening e media di blocco
def esatta(valori, k):
    return Fraction(sum(Fraction(x) for x in valori), k)


casi = {}
for nome, valori, soglia in (("screening 125×0,3+125×0,2 contro 0,25", [0.3] * 125 + [0.2] * 125, 0.25),
                             ("blocco 250×0,3 contro 0,3", [0.3] * 250, 0.3),
                             ("blocco 125×(−0,3)+125×(−0,2) contro −0,25", [-0.3] * 125 + [-0.2] * 125, -0.25)):
    for lato, f in (("uguale", lambda x: x), ("+1 ulp", lambda x: math.nextafter(x, math.inf)),
                    ("−1 ulp", lambda x: math.nextafter(x, -math.inf))):
        vv = [f(x) for x in valori]
        cp = [(x, 1) for x in vv]
        if nome.startswith("screening"):
            with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
                media = V.screening(cp, 9, 0.9)["media"]
            dec_mod, dec_es = media > soglia, esatta(vv, len(vv)) > Fraction(soglia)
        else:
            media = V.veto_blocchi(cp, soglia, 1)["medie"][0]
            dec_mod, dec_es = media < soglia, esatta(vv, len(vv)) < Fraction(soglia)
        casi[f"{nome} · {lato}"] = {"media del modulo": repr(media), "decisione del modulo": dec_mod,
                                    "decisione esatta": dec_es, "coincide": dec_mod == dec_es}
out["#124"] = casi


# 4. Potenza replica per replica
def clopper(k, n, a=0.05):
    def cdf(p, kk):                                                    # P(X ≤ kk), somma in logaritmi
        if p <= 0:
            return 1.0
        if p >= 1:
            return 0.0 if kk < n else 1.0
        lp, lq = math.log(p), math.log1p(-p)
        return math.fsum(math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
                         for i in range(kk + 1))

    def cerca(f, obiettivo):
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) > obiettivo:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    basso = 0.0 if k == 0 else cerca(lambda p: cdf(p, k - 1), 1 - a / 2)     # P(X ≥ k) = a/2
    alto = 1.0 if k == n else cerca(lambda p: cdf(p, k), a / 2)
    return [basso, alto]


def scenario(sigma, seme):
    r = random.Random(seme)
    conti = {"M": M, "F": 0, "P": 0, "promosse senza segnale favorevole": 0, "invalide": 0, "inconclusive": 0,
             "fermate fra le favorevoli": {"veto": 0, "minimi": 0, "requisito": 0}}
    for i in range(M):
        cp = [(r.gauss(0.25, sigma), 1) for _ in range(1000)]
        veto = V.veto_blocchi(cp, -0.25, 50)
        v = V.verdetto(cp, i + 1, [veto], contesto=CTX)
        f, p = v["segnale"] == "favorevole", v["esito"] == "promossa"
        conti["F"] += f
        conti["P"] += p
        conti["promosse senza segnale favorevole"] += p and not f
        conti["invalide"] += v["segnale"] == "invalido"
        conti["inconclusive"] += v["segnale"] == "inconclusivo"
        if f and not p:
            conti["fermate fra le favorevoli"]["veto" if veto["esito"] == "fallito" else
                                               "minimi" if V.minimi_mancanti(cp) else "requisito"] += 1
    conti.update({"F/M": conti["F"] / M, "P/M": conti["P"] / M, "(F−P)/M": (conti["F"] - conti["P"]) / M,
                  "IC95 F/M": [round(x, 5) for x in clopper(conti["F"], M)], "IC95 P/M": [round(x, 5) for x in clopper(conti["P"], M)],
                  "IC95 (F−P)/M": [round(x, 5) for x in clopper(conti["F"] - conti["P"], M)]})
    return conti


out["potenza"] = {"media +0,25 R, σ 1,25 R, un trade per seduta, 1.000 sedute": scenario(1.25, 101),
                  "media +0,25 R, σ 0,80 R, un trade per seduta, 1.000 sedute": scenario(0.80, 202)}


# 6. Veti: prova LOGICA deterministica (DGS-16 Q6). Quattro blocchi da 250 sedute, un trade per seduta, rumore
#    gaussiano σ = 0,30 R con seme fisso; blocco debole a media −0,35 R, gli altri a +0,70 R, così il segnale del metro
#    è favorevole e il solo veto può fermare la promozione. Veto a −0,25 R, minimo 50 trade per blocco. Il risultato
#    atteso del veto è calcolato qui sotto in modo indipendente dal modulo (frazioni esatte sui valori generati).
FORTE = 0.70


def blocco(media, seme, n=250, trade=None):
    trade = n if trade is None else trade
    r = random.Random(seme)
    return [(media + r.gauss(0, 0.30), 1) for _ in range(trade)] + [(0.0, 0)] * (n - trade)


def atteso_veto(coppie, soglia, minimo, ampiezza=250):
    esito = "superato"
    sottile = False
    for i in range(0, len(coppie), ampiezza):
        b = coppie[i:i + ampiezza]
        k = sum(x for _, x in b)
        if k < minimo:
            sottile = True
        elif Fraction(sum(Fraction(s) for s, _ in b), k) < Fraction(soglia):
            esito = "fallito"
    return esito if esito == "fallito" else ("non valutabile" if sottile else "superato")


veti = {}
casi = [(f"debole in posizione {pos + 1}", [blocco(-0.35 if j == pos else FORTE, 10 * pos + j) for j in range(4)])
        for pos in range(4)]
media_omogenea = (-0.35 + 3 * FORTE) / 4                                   # stessa media complessiva (+0,4375 R)
casi.append(("controllo omogeneo (stessa media)", [blocco(media_omogenea, 40 + j) for j in range(4)]))
for k in (49, 50, 51):
    casi.append((f"debole con {k} trade (minimo 50)", [blocco(-0.35, 50 + k, trade=k)] +
                 [blocco(FORTE, 60 + j) for j in range(3)]))
for nome, blocchi in casi:
    cp = [x for b in blocchi for x in b]
    veto = V.veto_blocchi(cp, -0.25, 50)
    v = V.verdetto(cp, 7, [veto], contesto=CTX)
    atteso = atteso_veto(cp, -0.25, 50)
    veti[nome] = {"segnale del metro": v["segnale"], "veto": veto["esito"], "veto atteso": atteso,
                  "coincide": veto["esito"] == atteso, "esito": v["esito"], "causa": v["causa"],
                  "medie dei blocchi": [None if m is None else round(m, 6) for m in veto["medie"]]}
out["veti (prova logica)"] = veti


# 5. D-44
def limite_alto(k, n=12000, a=0.001):
    return clopper(k, n, 2 * a)[1]


out["D-44"] = {f"{k} su 12.000": f"{limite_alto(k):.4%}" for k in (107, 2, 3)}
print(json.dumps(out, ensure_ascii=False, indent=1))
