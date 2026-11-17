"""Pilota del collaudo del test IA-02 sul limite inferiore (17/11/2026; risposta 7 al DGS, §4).

Domanda: un metodo che promuove quando «limite inferiore della media di R > +0,15 R» mantiene il tasso di falsa
promozione dichiarato (quota a) quando i trade sono dipendenti? Si confrontano tre metodi su serie INVENTATE:
- «ingenuo»: errore standard s/√n (assume trade indipendenti): riferimento negativo;
- «hac»: Newey–West con nucleo di Bartlett e ritardi fissati PRIMA (regola L = ⌊4·(n/100)^(2/9)⌋);
- «bootstrap»: bootstrap a blocchi mobili della media, limite = quantile a delle medie ricampionate
  (blocco ⌈n^(1/3)⌉ fissato prima).
Celle del pilota: rumore gaussiano indipendente e AR(1) con rho 0,25; media vera al confine (+0,15) e sopra
(+0,30); n = 1.000 trade; a = 2,5%; repliche impegnate prima (3.000) con semi fissi. Per ogni cella e metodo:
promozioni k su M, tasso, intervallo esatto di Clopper–Pearson al 95%.

Il pilota NON certifica nulla (è sviluppo del metodo, da dichiarare): serve a scegliere metodo e margine prima di
scrivere la matrice completa (K celle, M repliche) e la regola U ≤ a proposta dal DGS. Si esegue solo con il via del
titolare. Riferimenti analitici del DGS (addendum §2) riprodotti da `fattore_ar1` e `falsa_promozione_ingenua`.

Uso (pilota vero, SOLO con il via del titolare; qualche minuto: il bootstrap costa circa 13 ms a replica):
  python3 -s -B -m brain.laboratorio.studi.collaudo_ia02 --repliche 3000 --bootstrap 499 --n 1000
"""
import argparse
import math
import random
import sys
from statistics import NormalDist

SOGLIA = 0.15
SIGMA = 1.25
_N = NormalDist()
METODI = ("ingenuo", "hac", "bootstrap")
CELLE = ((0.15, 0.0), (0.15, 0.25), (0.30, 0.0), (0.30, 0.25))      # (media vera, rho)


def Z(a: float) -> float:
    return _N.inv_cdf(1 - a)


def fattore_ar1(n: int, rho: float) -> float:
    """Var(media) = sigma² · F / n per un AR(1) stazionario: F = 1 + 2 Σ_{k=1}^{n-1} (1 − k/n) rho^k."""
    return 1 + 2 * sum((1 - k / n) * rho ** k for k in range(1, n))


def falsa_promozione_ingenua(n: int, rho: float, a: float) -> float:
    """Tasso esatto di falsa promozione al confine del test che usa sigma/√n con dati AR(1) (riferimento del DGS)."""
    return 1 - _N.cdf(Z(a) / math.sqrt(fattore_ar1(n, rho)))


def serie_ar1(n: int, mu: float, sigma: float, rho: float, rnd: random.Random) -> list:
    """Serie gaussiana AR(1) STAZIONARIA (primo valore già dalla distribuzione marginale): media mu, varianza sigma²."""
    e = rnd.gauss(0.0, sigma)
    out = [mu + e]
    scala = sigma * math.sqrt(1 - rho * rho)
    for _ in range(n - 1):
        e = rho * e + rnd.gauss(0.0, scala)
        out.append(mu + e)
    return out


def limite_ingenuo(x: list, a: float) -> float:
    n = len(x)
    m = sum(x) / n
    s = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1))
    return m - Z(a) * s / math.sqrt(n)


def ritardi_newey_west(n: int) -> int:
    return math.floor(4 * (n / 100) ** (2 / 9))


def limite_hac(x: list, a: float, ritardi: int = None) -> float:
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    L = ritardi_newey_west(n) if ritardi is None else ritardi
    var = sum(v * v for v in d) / n
    for l in range(1, L + 1):
        var += 2 * (1 - l / (L + 1)) * sum(d[i] * d[i + l] for i in range(n - l)) / n
    return m - Z(a) * math.sqrt(max(var, 0.0) / n)


def blocco_predefinito(n: int) -> int:
    return math.ceil(n ** (1 / 3))


def limite_bootstrap(x: list, a: float, ricampionamenti: int, rnd: random.Random, blocco: int = None) -> float:
    """Bootstrap a blocchi mobili: le somme dei blocchi si leggono dai prefissi cumulati (veloce in Python puro)."""
    n = len(x)
    b = blocco or blocco_predefinito(n)
    cum = [0.0]
    for v in x:
        cum.append(cum[-1] + v)
    blocchi = math.ceil(n / b)
    ultimo = n - b
    medie = []
    for _ in range(ricampionamenti):
        tot = 0.0
        for _ in range(blocchi):
            i = rnd.randint(0, ultimo)
            tot += cum[i + b] - cum[i]
        medie.append(tot / (blocchi * b))
    medie.sort()
    return medie[max(0, math.ceil(a * ricampionamenti) - 1)]


def _cdf_binomiale(k: int, M: int, p: float) -> float:
    if p <= 0:
        return 1.0
    if p >= 1:
        return 0.0 if k < M else 1.0
    lp, lq = math.log(p), math.log(1 - p)
    return sum(math.exp(math.lgamma(M + 1) - math.lgamma(i + 1) - math.lgamma(M - i + 1) + i * lp + (M - i) * lq)
               for i in range(k + 1))


def clopper_pearson(k: int, M: int, livello: float = 0.95) -> tuple:
    """Intervallo esatto bilaterale per la frequenza k/M (bisezione sulla funzione di ripartizione binomiale)."""
    d = (1 - livello) / 2

    def cerca(f):                                            # f crescente in p, cerca f(p) = 0
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    basso = 0.0 if k == 0 else cerca(lambda p: (1 - _cdf_binomiale(k - 1, M, p)) - d)
    alto = 1.0 if k == M else cerca(lambda p: d - _cdf_binomiale(k, M, p))
    return basso, alto


def cella(n: int, mu: float, rho: float, metodo: str, repliche: int, seme: int, ricampionamenti: int = 499,
          a: float = 0.025) -> dict:
    """Promozioni (limite inferiore > SOGLIA) su `repliche` serie indipendenti. Ogni replica resta nel denominatore."""
    if metodo not in METODI:
        raise ValueError(f"metodo {metodo!r} non in {METODI}")
    rnd = random.Random(seme)
    promosse = 0
    for _ in range(repliche):
        x = serie_ar1(n, mu, SIGMA, rho, rnd)
        if metodo == "ingenuo":
            lim = limite_ingenuo(x, a)
        elif metodo == "hac":
            lim = limite_hac(x, a)
        else:
            lim = limite_bootstrap(x, a, ricampionamenti, rnd)
        promosse += lim > SOGLIA
    return {"n": n, "mu": mu, "rho": rho, "metodo": metodo, "repliche": repliche, "promosse": promosse}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--repliche", type=int, default=3000)
    p.add_argument("--bootstrap", type=int, default=499)
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--seme", type=int, default=20261117)
    x = p.parse_args(argv)
    if x.repliche < 1000:
        print(f"ATTENZIONE: {x.repliche} repliche: questa NON è il pilota impegnato (3.000), solo una prova del "
              f"funzionamento.\n")
    print(f"Riferimento analitico (DGS): test ingenuo al confine, n = {x.n}, a = 2,5%: rho 0 → "
          f"{falsa_promozione_ingenua(x.n, 0.0, 0.025):.4%}; rho 0,25 → {falsa_promozione_ingenua(x.n, 0.25, 0.025):.4%}"
          f"\n")
    print("| media vera | rho | metodo | promosse / repliche | tasso | Clopper–Pearson 95% |")
    print("|---|---|---|---|---|---|")
    for i, (mu, rho) in enumerate(CELLE):
        for j, metodo in enumerate(METODI):
            r = cella(x.n, mu, rho, metodo, x.repliche, x.seme + 100 * i + j, x.bootstrap)
            lo, hi = clopper_pearson(r["promosse"], r["repliche"])
            print(f"| {mu:+.2f} | {rho} | {metodo} | {r['promosse']} / {r['repliche']} | "
                  f"{r['promosse'] / r['repliche']:.2%} | {lo:.2%} – {hi:.2%} |")
    print("\nAl confine (+0,15) il tasso è la falsa promozione da confrontare con a = 2,5%; a +0,30 è la potenza.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
