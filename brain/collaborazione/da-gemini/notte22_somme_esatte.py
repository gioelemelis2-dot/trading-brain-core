"""Mandato notte 22/11/2026 — Compito A (#124): confronto in aritmetica ESATTA (fractions.Fraction)
per tutte le somme e medie in virgola mobile di `brain/laboratorio/verdetto/verdetto_d31.py`.

I calcoli di riferimento NON importano `verdetto_d31` né `pilota_ia02`: usano solo `fractions.Fraction`,
`math` e `random.Random` della libreria standard, poi confrontano la decisione del modulo con quella esatta.
Solo dati inventati; eseguire con HTTPS_PROXY=http://127.0.0.1:9.
"""
import math
import platform
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.laboratorio.verdetto import verdetto_d31 as V  # noqa: E402

# Costanti di riferimento (esatte, indipendenti dal modulo)
EX_PROM = Fraction(20, 100)       # +0,20 R
EX_BOCC = Fraction(10, 100)       # +0,10 R
EX_SCR_M = Fraction(25, 100)      # +0,25 R
EX_SCR_P = Fraction(50, 100)      # 50%
EX_AMP_MIN = Fraction(1, 10**9)   # 1e-9 R
EX_A = Fraction(25, 1000)         # 0,025
EX_B = 3999
EX_BLOCCO = 10


def _ref_bootstrap_exact(coppie_frac, seme: int, ricampionamenti: int = EX_B, blocco: int = EX_BLOCCO):
    """Bootstrap circolare a blocchi (intervallo basic) interamente in fractions.Fraction esatte."""
    n = len(coppie_frac)
    sk = sum(k for _, k in coppie_frac)
    if sk == 0:
        return None
    estese = coppie_frac + coppie_frac[:blocco - 1]
    cs = [Fraction(0)]
    ck = [0]
    for s, k in estese:
        cs.append(cs[-1] + s)
        ck.append(ck[-1] + k)
    blocchi = n // blocco
    rnd = random.Random(seme)
    medie = []
    for _ in range(ricampionamenti):
        ts = Fraction(0)
        tk = 0
        for _ in range(blocchi):
            i = rnd.randrange(n)
            ts += cs[i + blocco] - cs[i]
            tk += ck[i + blocco] - ck[i]
        if tk == 0:
            return None
        medie.append(ts / tk)
    mu = sum((s for s, _ in coppie_frac), Fraction(0)) / sk
    o = sorted(medie)
    idx_hi = math.ceil(float(1 - EX_A) * ricampionamenti) - 1
    idx_lo = math.ceil(float(EX_A) * ricampionamenti) - 1
    lo = 2 * mu - o[idx_hi]
    hi = 2 * mu - o[idx_lo]
    if not lo < hi:
        return None
    return lo, hi


def _ref_segnale(iv):
    if iv is None or iv[1] - iv[0] < EX_AMP_MIN:
        return "invalido"
    if iv[0] > EX_PROM:
        return "favorevole"
    if iv[1] < EX_BOCC:
        return "sfavorevole"
    return "inconclusivo"


def _fmt_frac(f: Fraction) -> str:
    if f is None:
        return "None"
    return f"{float(f):.17g} (num={f.numerator}/{f.denominator})" if f.denominator <= 10**6 else f"{float(f):.17g}"


def _trova_caso_sum_diverge(target: Fraction, n: int, segno_voluto: int):
    """Costruisce n float ESATTI IN BINARIO (Fraction.from_float(x) == valore esatto) in [-2, +2]
    la cui media ESATTA è esattamente `target`, ma `sum(xs) / n` in Python corrente devia con segno `segno_voluto`
    (+1 => sum/n > target; -1 => sum/n < target). Usa piccole potenze di 2 (2^-52)."""
    t = float(target)
    assert Fraction.from_float(t) == target, f"target {target} deve essere diadico"
    eps = math.ldexp(1.0, -52)  # 2^-52, esatto in binario
    # Costruzione deterministica: 1 seduta grande per spostare l'esponente di accumulo + residui diadici esatti
    # Es: primo elemento = 2.0 (sposta ULP dell'accumulatore a 2^-51 -> 2^-45), poi m copie di (t + c*eps),
    # poi compensazione esatta in modo che somma esatta == n * target.
    for amp in (2.0, 4.0, 8.0, 16.0):
        for step_k in (1, 2, 3, 5, 7, 11, 13):
            for sgn in (1, -1):
                delta = sgn * step_k * eps
                # m elementi a (t + delta), m elementi a (t - delta), piu' (amp, -amp) per forzare arrotondamento
                # Somma esatta = n * t esattamente!
                m = (n - 2) // 2
                xs = [t + amp] + [t + delta] * m + [t - amp] + [t - delta] * m
                while len(xs) < n:
                    xs.append(t)
                ex_mean = sum((Fraction.from_float(x) for x in xs), Fraction(0)) / n
                assert ex_mean == target
                fl_mean = sum(xs) / n
                if segno_voluto > 0 and fl_mean > t:
                    return xs, ex_mean, fl_mean
                if segno_voluto < 0 and fl_mean < t:
                    return xs, ex_mean, fl_mean
    return None


def main() -> int:
    print(f"Python: {sys.version.splitlines()[0]} | Platform: {platform.platform()}")
    print(f"math.fsum disponibile: {hasattr(math, 'fsum')}\n")

    righe = []

    def registra(codice, punto, desc, val_ex, val_mod, val_fsum, dec_ex, dec_mod):
        div = dec_ex != dec_mod
        righe.append((codice, punto, desc, val_ex, val_mod, val_fsum, dec_ex, dec_mod, div))
        print(
            f"[{codice}] ({punto}) {desc}\n"
            f"   esatto={val_ex} | modulo={val_mod} | fsum={val_fsum}\n"
            f"   dec_esatta={dec_ex!r} | dec_modulo={dec_mod!r} | DIVERGE={'SI' if div else 'NO'}"
        )

    # =========================================================================
    # 1. SCREENING: media > +0,25 R (verdetto_d31.py:229-230)
    # =========================================================================
    # S1: 250 sedute con media decimale esatta 0,25 da 0,3 e 0,2 (input decimali -> float64)
    coppie_s1 = [(0.3, 1)] * 125 + [(0.2, 1)] * 125
    ex_dec_s1 = (Fraction(3, 10) * 125 + Fraction(2, 10) * 125) / 250  # 1/4 esatto
    ex_flt_s1 = sum((Fraction.from_float(s) for s, _ in coppie_s1), Fraction(0)) / 250
    s1 = V.screening(coppie_s1, 9, 0.9)
    registra(
        "S1", "screening:229-230", "125×0.3 + 125×0.2 (media decimale=0.25)",
        f"dec={float(ex_dec_s1):.17g}; flt={float(ex_flt_s1):.17g}",
        f"{s1['media']:.17g}",
        f"{math.fsum(s for s, _ in coppie_s1) / 250:.17g}",
        ex_dec_s1 > EX_SCR_M,
        not any("media" in c for c in s1["cause"]),
    )

    # S2: 300 sedute [(0.1,1), (0.2,1), (0.45,1)]*100 -> media decimale ESATTA 0.25 (0.75/3)
    coppie_s2 = [(0.1, 1), (0.2, 1), (0.45, 1)] * 100
    ex_dec_s2 = (Fraction(1, 10) + Fraction(2, 10) + Fraction(45, 100)) / 3  # 1/4 esatto
    ex_flt_s2 = sum((Fraction.from_float(s) for s, _ in coppie_s2), Fraction(0)) / 300
    s2 = V.screening(coppie_s2, 9, 0.9)
    registra(
        "S2", "screening:229-230", "100×(0.1, 0.2, 0.45) (media decimale=0.25)",
        f"dec={float(ex_dec_s2):.17g}; flt={float(ex_flt_s2):.17g}",
        f"{s2['media']:.17g}",
        f"{math.fsum(s for s, _ in coppie_s2) / 300:.17g}",
        ex_dec_s2 > EX_SCR_M,
        not any("media" in c for c in s2["cause"]),
    )

    # S3: SOLO errore di sum() (float ESATTI in binario con media esatta == 0.25, ma sum()/n > 0.25!)
    trov_s3 = _trova_caso_sum_diverge(EX_SCR_M, 250, +1)
    assert trov_s3 is not None, "Non trovato caso S3"
    xs_s3, ex_s3, fl_s3 = trov_s3
    coppie_s3 = [(x, 1) for x in xs_s3]
    s3 = V.screening(coppie_s3, 9, 0.9)
    registra(
        "S3", "screening:229-230", "250 float binari esatti, media=0.25 esatto, sum()>0.25",
        f"{float(ex_s3):.17g} (1/4 esatto)",
        f"{s3['media']:.17g}",
        f"{math.fsum(xs_s3) / 250:.17g}",
        ex_s3 > EX_SCR_M,
        not any("media" in c for c in s3["cause"]),
    )

    # S4: media esatta = 0.25 + 1 ulp (passa), media esatta = 0.25 - 1 ulp (non passa)
    m_plus = math.nextafter(0.25, 1.0)
    m_minus = math.nextafter(0.25, 0.0)
    for cid, mval in (("S4a", m_plus), ("S4b", m_minus)):
        cp = [(mval, 1)] * 250
        ex_v = Fraction.from_float(mval)
        sr = V.screening(cp, 9, 0.9)
        registra(
            cid, "screening:229-230", f"250×({mval:.17g}) (±1 ulp da 0.25)",
            f"{float(ex_v):.17g}",
            f"{sr['media']:.17g}",
            f"{math.fsum(s for s, _ in cp) / 250:.17g}",
            ex_v > EX_SCR_M,
            not any("media" in c for c in sr["cause"]),
        )

    # =========================================================================
    # 2. VETO PER BLOCCHI: media blocco < soglia (verdetto_d31.py:261, 265)
    # =========================================================================
    # B1: 250 sedute con S = 0.3 contro soglia = 0.3 (esempio esplicito del mandato!)
    cp_b1 = [(0.3, 1)] * 250
    ex_dec_b1 = Fraction(3, 10)
    ex_flt_b1 = Fraction.from_float(0.3)
    vb1 = V.veto_blocchi(cp_b1, soglia=0.3, minimo_trade_blocco=50, ampiezza=250)
    registra(
        "B1", "veto_blocchi:261,265", "250×0.3 contro soglia=0.3 (uguaglianza esatta)",
        f"dec={float(ex_dec_b1):.17g}; flt={float(ex_flt_b1):.17g}",
        f"{vb1['medie'][0]:.17g}",
        f"{math.fsum([0.3] * 250) / 250:.17g}",
        "superato",
        vb1["esito"],
    )

    # B2: 250 sedute con S = -0.3 contro soglia = -0.3 (uguaglianza esatta, segno negativo!)
    cp_b2 = [(-0.3, 1)] * 250
    vb2 = V.veto_blocchi(cp_b2, soglia=-0.3, minimo_trade_blocco=50, ampiezza=250)
    registra(
        "B2", "veto_blocchi:261,265", "250×(-0.3) contro soglia=-0.3 (uguaglianza esatta)",
        f"dec={float(Fraction(-3, 10)):.17g}; flt={-0.3:.17g}",
        f"{vb2['medie'][0]:.17g}",
        f"{math.fsum([-0.3] * 250) / 250:.17g}",
        "superato",
        vb2["esito"],
    )

    # B3: 250 sedute con S in {-0.3, -0.2} (media decimale = -0.25) contro soglia = -0.25
    cp_b3 = [(-0.3, 1)] * 125 + [(-0.2, 1)] * 125
    vb3 = V.veto_blocchi(cp_b3, soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
    registra(
        "B3", "veto_blocchi:261,265", "125×(-0.3)+125×(-0.2) contro soglia=-0.25",
        f"dec=-0.25; flt={float(sum((Fraction.from_float(s) for s, _ in cp_b3), Fraction(0)) / 250):.17g}",
        f"{vb3['medie'][0]:.17g}",
        f"{math.fsum(s for s, _ in cp_b3) / 250:.17g}",
        "superato",
        vb3["esito"],
    )

    # B4: SOLO errore di sum() (250 float binari esatti, media ESATTA == -0.25, ma sum()/250 < -0.25 -> FALSO VETO!)
    trov_b4 = _trova_caso_sum_diverge(Fraction(-1, 4), 250, -1)
    assert trov_b4 is not None, "Non trovato caso B4"
    xs_b4, ex_b4, fl_b4 = trov_b4
    cp_b4 = [(x, 1) for x in xs_b4]
    vb4 = V.veto_blocchi(cp_b4, soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
    registra(
        "B4", "veto_blocchi:261,265", "250 float binari esatti, media=-0.25 esatto, sum()<-0.25",
        f"{float(ex_b4):.17g} (-1/4 esatto)",
        f"{vb4['medie'][0]:.17g}",
        f"{math.fsum(xs_b4) / 250:.17g}",
        "superato",
        vb4["esito"],
    )

    # B5: 250 sedute con media esatta = -0.25 - 1e-15 (deve fallire) e -0.25 + 1e-15 (deve superare)
    for cid, shift, att in (("B5a", -1e-15, "fallito"), ("B5b", +1e-15, "superato")):
        v_s = -0.25 + shift
        cp = [(v_s, 1)] * 250
        vb = V.veto_blocchi(cp, soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
        ex_m = Fraction.from_float(v_s)
        registra(
            cid, "veto_blocchi:261,265", f"250×(-0.25{shift:+.0e}) contro soglia=-0.25",
            f"{float(ex_m):.17g}",
            f"{vb['medie'][0]:.17g}",
            f"{math.fsum(s for s, _ in cp) / 250:.17g}",
            att,
            vb["esito"],
        )

    # =========================================================================
    # 3. SEGNALE D-31 / D-44: L > +0,20, U < +0,10, ampiezza < 1e-9 (righe 50, 52, 54)
    # =========================================================================
    # V1: ampiezza esatta a filo 1e-9 (D-44): (0.3, 0.3 + 1e-9) vs (1.0, 1.0 + 1e-9) vs (0.3, math.nextafter(0.3+1e-9, 0))
    for cid, lo_f, hi_f in (
        ("A1", 0.3, 0.3 + 1e-9),
        ("A2", 1.0, 1.0 + 1e-9),
        ("A3", 2.0, 2.0 + 1e-9),
        ("A4", 0.3, math.nextafter(0.3 + 1e-9, 0.0)),
    ):
        ex_w = Fraction.from_float(hi_f) - Fraction.from_float(lo_f)
        fl_w = hi_f - lo_f
        dec_ex = _ref_segnale((Fraction.from_float(lo_f), Fraction.from_float(hi_f)))
        dec_mod = V.segnale((lo_f, hi_f))
        registra(
            cid, "segnale:50", f"ampiezza iv=({lo_f}, {hi_f:.17g})",
            f"w_ex={float(ex_w):.17g} ({'<' if ex_w < EX_AMP_MIN else '>='} 1e-9)",
            f"w_fl={fl_w:.17g}",
            "—",
            dec_ex,
            dec_mod,
        )

    # V2: Bootstrap end-to-end (1000 sedute) costruito per avere L esattamente a filo di +0.20 R
    # (usiamo blocchi costanti di periodo 1000 con 2 valori: media calibrata così L_exact == 0.20!)
    # Costruzione: 500 blocchi da 10 con valore a, 500 blocchi da 10 con valore b (oppure 100 blocchi: 50 a, 50 b),
    # poi trasliamo tutti i valori di (0.20 - L_base) in float per centrare L esattamente su 0.20!
    base_1000 = [0.25 if (i // 10) % 2 == 0 else 0.15 for i in range(1000)]
    iv_base_ex = _ref_bootstrap_exact([(Fraction.from_float(x), 1) for x in base_1000], seme=11)
    assert iv_base_ex is not None
    # Shift esatto per portare L_ex esattamente a 0.20 (EX_PROM)
    shift_prom = EX_PROM - iv_base_ex[0]
    coppie_prom_ex = [(Fraction.from_float(x) + shift_prom, 1) for x in base_1000]
    coppie_prom_fl = [(float(s), 1) for s, _ in coppie_prom_ex]
    iv_p_ex = _ref_bootstrap_exact([(Fraction.from_float(s), 1) for s, _ in coppie_prom_fl], seme=11)
    iv_p_mod = V.intervallo(coppie_prom_fl, seme=11)
    registra(
        "V1", "segnale:52 + pilota", "1000 sedute bootstrap con L a filo +0.20 R (seme 11)",
        f"L_ex={float(iv_p_ex[0]):.17g} ({'>' if iv_p_ex[0] > EX_PROM else '<='} 0.20)",
        f"L_mod={iv_p_mod[0]:.17g}",
        "—",
        _ref_segnale(iv_p_ex),
        V.segnale(iv_p_mod),
    )

    # V1b: 1000 sedute bootstrap con L_ex = +0.20 + 1e-15 (> 0.20, favorevole) ma L_mod <= 0.20 (inconclusivo)
    coppie_p1b_fl = [(float(s + Fraction(1, 10**15)), 1) for s, _ in coppie_prom_ex]
    iv_p1b_ex = _ref_bootstrap_exact([(Fraction.from_float(s), 1) for s, _ in coppie_p1b_fl], seme=11)
    iv_p1b_mod = V.intervallo(coppie_p1b_fl, seme=11)
    registra(
        "V1b", "segnale:52 + pilota", "1000 sedute bootstrap con L_ex≈0.20+1e-15 (seme 11)",
        f"L_ex={float(iv_p1b_ex[0]):.17g} ({'>' if iv_p1b_ex[0] > EX_PROM else '<='} 0.20)",
        f"L_mod={iv_p1b_mod[0]:.17g}",
        "—",
        _ref_segnale(iv_p1b_ex),
        V.segnale(iv_p1b_mod),
    )

    # V2: Stesso test con U a filo +0.10 R (soglia bocciatura)
    shift_bocc = EX_BOCC - iv_base_ex[1]
    coppie_bocc_ex = [(Fraction.from_float(x) + shift_bocc, 1) for x in base_1000]
    coppie_bocc_fl = [(float(s), 1) for s, _ in coppie_bocc_ex]
    iv_b_ex = _ref_bootstrap_exact([(Fraction.from_float(s), 1) for s, _ in coppie_bocc_fl], seme=11)
    iv_b_mod = V.intervallo(coppie_bocc_fl, seme=11)
    registra(
        "V2", "segnale:54 + pilota", "1000 sedute bootstrap con U a filo +0.10 R (seme 11)",
        f"U_ex={float(iv_b_ex[1]):.17g} ({'<' if iv_b_ex[1] < EX_BOCC else '>='} 0.10)",
        f"U_mod={iv_b_mod[1]:.17g}",
        "—",
        _ref_segnale(iv_b_ex),
        V.segnale(iv_b_mod),
    )

    # V2b: 1000 sedute bootstrap con U_ex = +0.10 + 4e-16 (>= 0.10, inconclusivo) ma U_mod < 0.10 (sfavorevole)
    coppie_b2b_fl = [(float(s + Fraction(4, 10**16)), 1) for s, _ in coppie_bocc_ex]
    iv_b2b_ex = _ref_bootstrap_exact([(Fraction.from_float(s), 1) for s, _ in coppie_b2b_fl], seme=11)
    iv_b2b_mod = V.intervallo(coppie_b2b_fl, seme=11)
    registra(
        "V2b", "segnale:54 + pilota", "1000 sedute bootstrap con U_ex≈0.10+4e-16 (seme 11)",
        f"U_ex={float(iv_b2b_ex[1]):.17g} ({'<' if iv_b2b_ex[1] < EX_BOCC else '>='} 0.10)",
        f"U_mod={iv_b2b_mod[1]:.17g}",
        "—",
        _ref_segnale(iv_b2b_ex),
        V.segnale(iv_b2b_mod),
    )

    # V3: Screening L > 0 (riga 237) con L a filo 0.0 R
    shift_zero = Fraction(0) - iv_base_ex[0]
    coppie_z_ex = [(Fraction.from_float(x) + shift_zero, 1) for x in base_1000]
    coppie_z_fl = [(float(s), 1) for s, _ in coppie_z_ex]
    iv_z_ex = _ref_bootstrap_exact([(Fraction.from_float(s), 1) for s, _ in coppie_z_fl], seme=11)
    iv_z_mod = V.intervallo(coppie_z_fl, seme=11)
    registra(
        "V3", "screening:237 + pilota", "1000 sedute bootstrap con L a filo 0.0 R (seme 11)",
        f"L_ex={float(iv_z_ex[0]):.17g} ({'>' if iv_z_ex[0] > 0 else '<='} 0)",
        f"L_mod={iv_z_mod[0]:.17g}",
        "—",
        iv_z_ex[0] > 0,
        iv_z_mod[0] > 0,
    )

    # =========================================================================
    # 4. SCREENING: potenza >= 50% (verdetto_d31.py:239, D-47)
    # =========================================================================
    cp_ok = [(0.6, 1) if i % 2 == 0 else (0.4, 1) for i in range(300)]
    for cid, p_val, ex_p, desc in (
        ("P1", 0.50, Fraction(1, 2), "potenza = 0.50 esatto (D-47)"),
        ("P2", math.nextafter(0.5, 0.0), Fraction.from_float(math.nextafter(0.5, 0.0)), "potenza = 0.50 - 1 ulp"),
        ("P3", sum([0.1] * 5), Fraction(1, 2), "potenza = sum([0.1]*5) (in decimale = 0.50)"),
    ):
        sr = V.screening(cp_ok, 9, p_val)
        registra(
            cid, "screening:239", desc,
            f"{float(ex_p):.17g}",
            f"{p_val:.17g}",
            f"{math.fsum([0.1]*5):.17g}" if cid == "P3" else "—",
            ex_p >= EX_SCR_P,
            not any("potenza" in c for c in sr["cause"]),
        )

    div_list = [r for r in righe if r[-1]]
    print(f"\n=== RIEPILOGO: {len(div_list)}/{len(righe)} casi con DIVERGENZA DI DECISIONE ===")
    for r in div_list:
        print(f"  - {r[0]} ({r[1]}): {r[2]} | esatto={r[6]!r} vs modulo={r[7]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
