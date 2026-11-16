"""Calcolo di potenza per la soglia IA-02 (R medio netto ≥ +0,15 R per trade), 16/11/2026.

Domanda: con N trade, quanto spesso una strategia con vantaggio vero μ supera la soglia? Due regole possibili, da
scegliere nella scheda di H-003 PRIMA dei dati:
- «stima»: R medio misurato ≥ soglia;
- «limite»: limite inferiore dell'intervallo al 95% (R medio − 1,96 · errore standard) ≥ soglia.
Nessun dato vero: formule con l'approssimazione normale, e una simulazione su esiti inventati (stop a −1 R, target a
+T R, nessuna uscita intermedia) per controllarle. Le strategie vere hanno anche uscite a fine sessione e costi
variabili: la deviazione standard per trade va presa come ordine di grandezza (circa 1–1,5 R).

Uso: python3 -s -B -m brain.laboratorio.studi.potenza_soglia
"""
import math
import random
from statistics import NormalDist
from typing import Optional

Z95 = 1.959963984540054
_N = NormalDist()
REGOLE = ("stima", "limite")


def sigma_esiti(mu: float, target: float) -> float:
    """Deviazione standard di un esito −1 R / +target R con media mu (−1 < mu < target)."""
    if not -1.0 < mu < target:
        raise ValueError(f"media {mu} fuori da (−1, {target})")
    p = (mu + 1.0) / (target + 1.0)
    return (target + 1.0) * math.sqrt(p * (1.0 - p))


def _spostamento(regola: str) -> float:
    if regola not in REGOLE:
        raise ValueError(f"regola {regola!r} non in {REGOLE}")
    return Z95 if regola == "limite" else 0.0


def prob_promozione(mu: float, sigma: float, n: int, soglia: float, regola: str) -> float:
    """Probabilità che la regola promuova una strategia con vantaggio vero mu (approssimazione normale)."""
    if sigma <= 0 or n < 1:
        raise ValueError(f"serve sigma > 0 e n ≥ 1 (sigma = {sigma}, n = {n})")
    z = _spostamento(regola)
    return _N.cdf((mu - soglia) * math.sqrt(n) / sigma - z)


def n_per_potenza(mu: float, sigma: float, soglia: float, potenza: float, regola: str) -> Optional[int]:
    """Trade minimi perché la regola promuova con almeno quella probabilità; None se mu ≤ soglia."""
    if not 0.0 < potenza < 1.0:
        raise ValueError(f"potenza {potenza} fuori da (0, 1)")
    if mu <= soglia:
        return None
    z = _spostamento(regola) + _N.inv_cdf(potenza)
    n = max(1, math.ceil((z * sigma / (mu - soglia)) ** 2))
    while prob_promozione(mu, sigma, n, soglia, regola) < potenza:       # arrotondamenti
        n += 1
    while n > 1 and prob_promozione(mu, sigma, n - 1, soglia, regola) >= potenza:
        n -= 1
    return n


def _varianza_campionaria(vinte: int, n: int, target: float) -> float:
    """Varianza campionaria (n − 1) di `vinte` esiti +target e `n − vinte` esiti −1."""
    media = (vinte * target - (n - vinte)) / n
    return (vinte * (target - media) ** 2 + (n - vinte) * (-1.0 - media) ** 2) / (n - 1)


def simula(mu: float, target: float, n: int, soglia: float, regola: str, prove: int = 2000, seme: int = 1) -> float:
    """Frequenza di promozione su esiti inventati −1 / +target con media mu, errore standard stimato dal campione."""
    if n < 2:
        raise ValueError("servono almeno 2 trade per stimare la varianza")
    z = _spostamento(regola)
    p = (mu + 1.0) / (target + 1.0)
    rnd = random.Random(seme)
    passa = 0
    for _ in range(prove):
        vinte = sum(1 for _ in range(n) if rnd.random() < p)
        media = (vinte * target - (n - vinte)) / n
        passa += media - z * math.sqrt(_varianza_campionaria(vinte, n, target) / n) >= soglia
    return passa / prove


def tabella(soglia: float = 0.15, sigma: float = 1.25) -> str:
    righe = [f"Soglia {soglia} R, deviazione standard per trade {sigma} R (approssimazione normale).", "",
             "Probabilità di promozione (stima / limite inferiore 95%):", "",
             "| vantaggio vero | n = 300 | n = 500 | n = 1.000 | n = 2.500 |", "|---|---|---|---|---|"]
    for mu in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40):
        celle = [f"{prob_promozione(mu, sigma, n, soglia, 'stima'):.0%} / {prob_promozione(mu, sigma, n, soglia, 'limite'):.0%}"
                 for n in (300, 500, 1000, 2500)]
        righe.append(f"| {mu:+.2f} R | " + " | ".join(celle) + " |")
    righe += ["", "Trade necessari per promuovere con probabilità 80% (stima / limite inferiore 95%):", "",
              "| vantaggio vero | trade |", "|---|---|"]
    for mu in (0.20, 0.25, 0.30, 0.40, 0.50):
        righe.append(f"| {mu:+.2f} R | {n_per_potenza(mu, sigma, soglia, 0.8, 'stima'):,} / "
                     f"{n_per_potenza(mu, sigma, soglia, 0.8, 'limite'):,} |".replace(",", "."))
    return "\n".join(righe)


if __name__ == "__main__":
    for s in (1.0, 1.25, 1.5):
        print(tabella(sigma=s), "\n")
