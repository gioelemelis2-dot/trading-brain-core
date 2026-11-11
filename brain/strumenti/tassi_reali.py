"""Esempi numerici della lezione L2.4 (tassi reali e inflazione attesa). Tutti [ESEMPIO]: numeri didattici."""


def reale_esatto(i: float, pi: float) -> float:
    return (1 + i) / (1 + pi) - 1


def inflazione_attesa(nominale: float, reale: float, premio_inflazione: float, premio_liquidita: float) -> float:
    return (nominale - reale) - premio_inflazione + premio_liquidita


def gordon(d: float, r: float, premio: float, g: float) -> float:
    return d / (r + premio - g)


def main() -> None:
    print("Es.1 Fisher: esatto %.3f%% (approx 2,0%%); alta inflazione %.2f%% (approx 5%%)"
          % (100 * reale_esatto(0.045, 0.025), 100 * reale_esatto(0.40, 0.35)))
    print("Es.2 breakeven 2,35%%: π attesa %.2f%% (liq 0,20) / %.2f%% (liq 0,50)"
          % (100 * inflazione_attesa(0.043, 0.0195, 0.001, 0.002), 100 * inflazione_attesa(0.043, 0.0195, 0.001, 0.005)))
    for premio in (0.04, 0.05):
        g1, g2 = gordon(3, 0.01, premio, 0.03), gordon(3, 0.02, premio, 0.03)
        v1, v2 = gordon(3, 0.01, premio, 0.0), gordon(3, 0.02, premio, 0.0)
        print(f"Es.4 premio {premio:.0%}: growth {g1:.1f}->{g2:.1f} ({g2/g1-1:+.1%}); g=0 {v1:.1f}->{v2:.1f} ({v2/v1-1:+.1%})")
    print("Esercizio 1: esatto %.3f%%" % (100 * reale_esatto(0.06, 0.04)))
    print("Esercizio 2: π attesa %.2f%%" % (100 * inflazione_attesa(0.038, 0.016, 0.0015, 0.0025)))


if __name__ == "__main__":
    main()
