"""Verifica numerica delle affermazioni quantitative del Modulo 0 (manuale v1).

Calcolo esatto (programmazione dinamica), non simulazione: per ogni combinazione
win rate / lunghezza striscia restituisce P(almeno k perdite consecutive in N trade).
Uso: python3 verifica_m0.py
"""
from math import sqrt, log


def p_striscia(p_vincita: float, k: int, n: int) -> float:
    """Probabilità esatta di almeno k perdite consecutive in n trade indipendenti."""
    q = 1 - p_vincita
    # stato = lunghezza della striscia di perdite corrente (0..k-1); k = assorbente
    stati = [0.0] * k
    stati[0] = 1.0
    assorbito = 0.0
    for _ in range(n):
        nuovi = [0.0] * k
        for j, pr in enumerate(stati):
            if pr == 0:
                continue
            nuovi[0] += pr * p_vincita
            if j + 1 == k:
                assorbito += pr * q
            else:
                nuovi[j + 1] += pr * q
        stati = nuovi
    return assorbito


def main() -> None:
    print("Lezione 13 · P(almeno k perdite di fila in 100 trade), calcolo esatto")
    manuale = {(0.50, 6): 0.54, (0.50, 8): 0.17, (0.40, 6): 0.87,
               (0.40, 8): 0.49, (0.40, 10): 0.20, (0.33, 10): 0.45}
    for (p, k), atteso in manuale.items():
        esatto = p_striscia(p, k, 100)
        print(f"  win {p:.0%}  k={k:2d}  esatto={esatto:.3f}  manuale={atteso:.2f}")

    print("\nFormula striscia massima attesa log(N)/log(1/(1-p))")
    for p in (0.5, 0.4, 0.33):
        print(f"  p={p:.2f} N=100 -> {log(100) / log(1 / (1 - p)):.1f}")

    print("\nLezione 14 · Sistema A (+2R al 40%, -1R al 60%)")
    media = 0.4 * 2 - 0.6 * 1
    var = 0.4 * 2 ** 2 + 0.6 * 1 ** 2 - media ** 2
    ds = sqrt(var)
    print(f"  E[R]={media:.2f}  dev.std={ds:.3f}")
    for n in (30, 100, 300):
        print(f"  N={n:3d}  t={media / (ds / sqrt(n)):.2f}")
    # numero di trade per t = 2 e t = 3
    for t in (2, 3):
        print(f"  trade necessari per t={t}: {(t * ds / media) ** 2:.0f}")

    print("\nLezione 15 · gioco di Peters")
    print(f"  media d'insieme={0.5 * 1.5 + 0.5 * 0.6:.3f}  media temporale={sqrt(1.5 * 0.6):.4f}")

    print("\nModulo 1 · sconto dei flussi (lezione 2)")
    for r in (0.04, 0.05):
        print(f"  100 fra 10 anni al {r:.0%}: {100 / (1 + r) ** 10:.2f}   fra 1 anno: {100 / (1 + r):.2f}")


if __name__ == "__main__":
    main()
