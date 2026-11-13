"""Simulazione riproducibile delle regole di arresto in demo (DA-29) e della probabilità di passare la fase 1 FTMO.

COSA SIMULA (dati inventati, non strategie reali): sequenze di trade il cui risultato in R è estratto da una normale
con media `mu` (il vantaggio vero, 0 / 0,05 / 0,10 / 0,20 R) e deviazione standard 1R. Nessun dato di mercato.

1. Test sequenziale di Wald (SPRT): H0 mu = 0, H1 mu = 0,10R, alfa 5%, beta 20%. Dopo 600 trade senza decisione la
   strategia è «indecisa» (non dimostrata).
2. Vecchia regola di Claude: dopo 100 trade, fermata se il totale è <= 0 o se il drawdown ha raggiunto 10R.
3. Fase 1 FTMO (+10% prima di -10%, senza limite giornaliero): formula della passeggiata casuale con deriva tra due
   barriere, confrontata con una simulazione diretta.

Uso (dalla radice del repository): python3 -s -B brain/laboratorio/studi/simulazione_sprt.py
Seme fisso: lo stesso Python dà gli stessi numeri.
"""
import math
import random

N_SIM = 6000
SEME = 20261113
MU1, SIGMA, ALFA, BETA, N_MAX = 0.10, 1.0, 0.05, 0.20, 600
A, B = math.log((1 - BETA) / ALFA), math.log(BETA / (1 - ALFA))


def sprt(rng, mu):
    s = 0.0
    for n in range(1, N_MAX + 1):
        s += rng.gauss(mu, SIGMA)
        llr = (MU1 / SIGMA ** 2) * (s - n * MU1 / 2)
        if llr >= A:
            return "promossa", n
        if llr <= B:
            return "fermata", n
    return "indecisa", N_MAX


def vecchia_regola(rng, mu):
    s = picco = 0.0
    for _ in range(100):
        s += rng.gauss(mu, SIGMA)
        picco = max(picco, s)
        if s - picco <= -10:
            return "fermata"
    return "fermata" if s <= 0 else "sopravvive"


def ftmo_formula(mu, a, b):
    if mu == 0:
        return b / (a + b)
    return (1 - math.exp(2 * mu * b / SIGMA ** 2)) / (math.exp(-2 * mu * a / SIGMA ** 2) - math.exp(2 * mu * b / SIGMA ** 2))


def ftmo_simulata(rng, mu, a, b, n_sim=4000):
    passate = 0
    for _ in range(n_sim):
        s = 0.0
        while -b < s < a:
            s += rng.gauss(mu, SIGMA)
        passate += s >= a
    return passate / n_sim


def main():
    rng = random.Random(SEME)
    print(f"Soglie SPRT: ferma se totale <= {B * SIGMA ** 2 / MU1:.2f} + {MU1 / 2:.3f} n; "
          f"promuovi se totale >= {A * SIGMA ** 2 / MU1:.2f} + {MU1 / 2:.3f} n\n")
    print(f"1-2. {N_SIM} sequenze per livello di vantaggio")
    for mu in (0.0, 0.05, 0.10, 0.20):
        r = [sprt(rng, mu) for _ in range(N_SIM)]
        v = [vecchia_regola(rng, mu) for _ in range(N_SIM)]
        pct = lambda lista, k: 100 * sum(1 for x in lista if (x[0] if isinstance(x, tuple) else x) == k) / N_SIM
        print(f"  mu = {mu:.2f}R  SPRT: promossa {pct(r, 'promossa'):5.1f}%  fermata {pct(r, 'fermata'):5.1f}%  "
              f"indecisa {pct(r, 'indecisa'):5.1f}%  trade medi {sum(x[1] for x in r) / N_SIM:5.0f}   |  "
              f"vecchia regola: sopravvive {pct(v, 'sopravvive'):5.1f}%")
    print("\n3. Fase 1 FTMO (+10% prima di -10%), formula e simulazione (4000 sequenze)")
    for rischio in (0.005, 0.01):
        a = b = 0.10 / rischio
        for mu in (0.0, 0.05, 0.10):
            print(f"  rischio {rischio * 100:.1f}%  mu = {mu:.2f}R  formula {100 * ftmo_formula(mu, a, b):5.1f}%  "
                  f"simulata {100 * ftmo_simulata(rng, mu, a, b):5.1f}%")


if __name__ == "__main__":
    main()
