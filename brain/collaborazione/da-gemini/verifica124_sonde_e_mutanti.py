"""Mandato 22/11/2026 (B) — Compito A: verifica indipendente della correzione di #124 in `verdetto_d31.py`.

1. Verifica V3 nello screening (L_vicino_a_zero=True e riga nel rapporto).
2. Cerca casi NUOVI non coperti da math.fsum:
   - doppio arrotondamento fsum()/k con k non potenza di 2 (screening, veto_blocchi, verdetto);
   - serie costante [(x, 1)]*k contro soglia=x con x non diadico;
   - segnalazione L_vicino_a_zero e vicini(lo, hi) esattamente a ±1e-9;
   - controlla_coppie:89 ancora con sum() invece di math.fsum().
3. Prova 4 mutanti NUOVI sulla correzione #124 contro `test_verdetto_d31.py`.

Riferimento esatto indipendente in `fractions.Fraction`. Solo dati inventati, rete bloccata.
"""
import math
import os
import platform
import random
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.laboratorio.studi import pilota_ia02 as P  # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V  # noqa: E402

NO_NET = dict(
    os.environ,
    HTTPS_PROXY="http://127.0.0.1:9",
    HTTP_PROXY="http://127.0.0.1:9",
    https_proxy="http://127.0.0.1:9",
    http_proxy="http://127.0.0.1:9",
    NO_PROXY="",
    no_proxy="",
)


def _ref_bootstrap_exact(coppie_frac, seme: int):
    n = len(coppie_frac)
    sk = sum(k for _, k in coppie_frac)
    estese = coppie_frac + coppie_frac[:9]
    cs, ck = [Fraction(0)], [0]
    for s, k in estese:
        cs.append(cs[-1] + s)
        ck.append(ck[-1] + k)
    blocchi = n // 10
    rnd = random.Random(seme)
    medie = []
    for _ in range(3999):
        ts, tk = Fraction(0), 0
        for _ in range(blocchi):
            i = rnd.randrange(n)
            ts += cs[i + 10] - cs[i]
            tk += ck[i + 10] - ck[i]
        medie.append(ts / tk)
    mu = sum((s for s, _ in coppie_frac), Fraction(0)) / sk
    o = sorted(medie)
    lo = 2 * mu - o[math.ceil(0.975 * 3999) - 1]
    hi = 2 * mu - o[math.ceil(0.025 * 3999) - 1]
    return lo, hi


def verifica_v3_screening():
    print("=== 1. VERIFICA V3 NELLO SCREENING (L_vicino_a_zero + rapporto) ===")
    base_1000 = [0.25 if (i // 10) % 2 == 0 else 0.15 for i in range(1000)]
    iv_base = _ref_bootstrap_exact([(Fraction.from_float(x), 1) for x in base_1000], seme=11)
    shift_zero = Fraction(0) - iv_base[0]
    coppie_z = [(float(Fraction.from_float(x) + shift_zero), 1) for x in base_1000]
    s = V.screening(coppie_z, seme=11, potenza_stimata=0.9)
    txt = V.rapporto_screening(s)
    riga_ok = "limite inferiore a meno di 1e-9 R [REGOLA] da 0" in txt
    print(f"  V3 screening: L={s['L']:.17g}, L_vicino_a_zero={s['L_vicino_a_zero']}, riga_in_rapporto={riga_ok}")
    assert s["L_vicino_a_zero"] is True and riga_ok


def casi_nuovi_non_coperti():
    print("\n=== 2. CASI NUOVI NON COPERTI DA math.fsum ===")
    trovati = []

    # D1: screening:229-230, k=300 (non potenza di 2), media esatta > 0.25 (somma esatta = 75 + 2^-48),
    # ma math.fsum() arrotonda 75 + 2^-48 -> 75.0 (ULP di 75.0 = 2^-46), quindi media modulo = 0.25 -> False!
    eps48 = math.ldexp(1.0, -48)  # 2^-48, esattamente rappresentabile in float64
    xs_d1 = [0.25] * 299 + [0.25 + eps48]
    # verifica che 0.25 + 2^-48 sia esattamente 0.25 + 2^-48 in float64 (ULP di 0.25 e' 2^-54!)
    assert Fraction.from_float(xs_d1[-1]) == Fraction(1, 4) + Fraction(1, 2**48)
    ex_d1 = sum((Fraction.from_float(x) for x in xs_d1), Fraction(0)) / 300
    assert ex_d1 > Fraction(1, 4)
    with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
        s_d1 = V.screening([(x, 1) for x in xs_d1], 9, 0.9)
    dec_ex_d1 = ex_d1 > Fraction(1, 4)
    dec_mod_d1 = not any("media" in c for c in s_d1["cause"])
    print(
        f"  [D1] screening k=300, somma esatta=75+2^-48: ex={float(ex_d1):.17g} (>0.25: {dec_ex_d1}) | "
        f"fsum={math.fsum(xs_d1):.17g}, mod={s_d1['media']:.17g} (>0.25: {dec_mod_d1}) | DIVERGE={dec_ex_d1 != dec_mod_d1}"
    )
    trovati.append(("D1", dec_ex_d1 != dec_mod_d1))

    # D2: veto_blocchi:261,265, k=250 (non potenza di 2), media esatta < -0.25 (somma esatta = -62.5 - 2^-49),
    # ma math.fsum() arrotonda -62.5 - 2^-49 -> -62.5 (ULP di 62.5 = 2^-47), quindi media modulo = -0.25 -> superato!
    eps49 = math.ldexp(1.0, -49)
    xs_d2 = [-0.25] * 249 + [-0.25 - eps49]
    assert Fraction.from_float(xs_d2[-1]) == Fraction(-1, 4) - Fraction(1, 2**49)
    ex_d2 = sum((Fraction.from_float(x) for x in xs_d2), Fraction(0)) / 250
    assert ex_d2 < Fraction(-1, 4)
    vb_d2 = V.veto_blocchi([(x, 1) for x in xs_d2], soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
    print(
        f"  [D2] veto_blocchi k=250, somma esatta=-62.5-2^-49: ex={float(ex_d2):.17g} (fallito) | "
        f"fsum={math.fsum(xs_d2):.17g}, mod={vb_d2['medie'][0]:.17g} ({vb_d2['esito']}) | DIVERGE={vb_d2['esito'] != 'fallito'}"
    )
    trovati.append(("D2", vb_d2["esito"] != "fallito"))

    # D3: Doppio arrotondamento fsum([x]*k)/k < x su SERIE COSTANTE [(x, 1)]*k contro soglia=x con k non potenza di 2!
    casi_cost = []
    for k in (3, 7, 29, 49, 250, 251, 300):
        for num in range(-400, 401):
            x = num / 1000.0
            m = math.fsum([x] * k) / k
            if m < x:
                casi_cost.append((k, x, math.fsum([x] * k), m))
        # anche razionali tipo -1/7, -1/3, -2/7
        for p, q in ((-1, 3), (-1, 7), (-2, 7), (-1, 6), (-1, 9), (-1, 11), (-1, 13)):
            x = p / q
            m = math.fsum([x] * k) / k
            if m < x:
                casi_cost.append((k, x, math.fsum([x] * k), m))
    print(f"  [D3] Scansione serie costanti [(x,1)]*k (x dec 0.001 e razionali, k non potenza di 2): {len(casi_cost)} casi con fsum([x]*k)/k < x!")
    for k, x, fs, m in casi_cost[:6]:
        vb = V.veto_blocchi([(x, 1)] * k, soglia=x, minimo_trade_blocco=1, ampiezza=k)
        print(f"       k={k}, x={x:.17g}: fsum={fs:.17g}, mod={m:.17g} (< {x:.17g}), esito={vb['esito']} (atteso: superato!)")
    trovati.append(("D3", len(casi_cost) > 0))

    # D4: Doppio arrotondamento in screening:229-230 su k=300 o k=251 con x > 0.25 di 1 ulp o media esatta <= 0.25
    # Testiamo anche media esatta = 0.25 + 2^-54 (1 ulp sopra 0.25? No, 0.25+2^-54 non è float; 0.25+2^-53 lo è):
    # con k=250, 1 elemento a 0.25+2^-48 e 249 a 0.25 -> somma esatta 62.5 + 2^-48 (esattamente 0.5 ULP di 62.5 -> round-to-even = 62.5!)
    xs_d4 = [0.25] * 249 + [0.25 + math.ldexp(1.0, -48)]
    ex_d4 = sum((Fraction.from_float(x) for x in xs_d4), Fraction(0)) / 250
    v_d4 = V.verdetto([(x, 1) for x in xs_d4] * 4, 5)  # 1000 sedute, media descrittiva in verdetto()
    ex_d4_1000 = sum((Fraction.from_float(x) for x in xs_d4 * 4), Fraction(0)) / 1000
    print(
        f"  [D4] verdetto() media descrittiva (k=1000, somma esatta=250+2^-46): "
        f"ex={float(ex_d4_1000):.17g}, v['media']={v_d4['media']:.17g}, uguale={Fraction.from_float(v_d4['media']) == ex_d4_1000}"
    )
    # Anche con k=300 e media esatta 250.0/1000? Testiamo k=3 in verdetto() con [0.1, 0.2, 0.45]:
    xs_v = [0.1, 0.2, 0.45] * 100
    ex_v = sum((Fraction.from_float(x) for x in xs_v), Fraction(0)) / 300
    v_v = V.verdetto([(x, 1) for x in xs_v], 5)
    print(f"  [D4b] verdetto() 100x(0.1,0.2,0.45) k=300: ex_flt={float(ex_v):.17g}, v['media']={v_v['media']:.17g}")

    # D5: Segnalazione "vicino a 0" esattamente a ±1e-9 e vicini(lo, hi) esattamente a 0.20±1e-9 e 0.10±1e-9
    cp_ok = [(0.6, 1) if i % 2 == 0 else (0.4, 1) for i in range(300)]
    print("\n  [D5] Bordi esatti ±1e-9:")
    for L_val in (1e-9, -1e-9, math.nextafter(1e-9, 0.0), math.nextafter(-1e-9, 0.0)):
        with mock.patch.object(P, "intervallo_bootstrap", return_value=(L_val, 0.5)):
            sr = V.screening(cp_ok, 9, 0.9)
        ex_vic = abs(Fraction.from_float(L_val)) < Fraction(1, 10**9)
        print(f"       screening L={L_val:.17g}: ex_vicino={ex_vic}, mod_vicino={sr['L_vicino_a_zero']}, DIVERGE={ex_vic != sr['L_vicino_a_zero']}")
    for nome, lo, hi, ref_soglia, quale in (
        ("L=0.20+1e-9", 0.20 + 1e-9, 0.5, Fraction(20, 100), "L"),
        ("L=0.20-1e-9", 0.20 - 1e-9, 0.5, Fraction(20, 100), "L"),
        ("U=0.10+1e-9", 0.0, 0.10 + 1e-9, Fraction(10, 100), "U"),
        ("U=0.10-1e-9", 0.0, 0.10 - 1e-9, Fraction(10, 100), "U"),
    ):
        val_f = lo if quale == "L" else hi
        sog_f = 0.20 if quale == "L" else 0.10
        ex_dist_dec = abs(Fraction.from_float(val_f) - ref_soglia)
        ex_dist_flt = abs(Fraction.from_float(val_f) - Fraction.from_float(sog_f))
        ex_vic_flt = ex_dist_flt < Fraction(1, 10**9)
        mod_vic = quale in V.vicini(lo, hi)
        print(
            f"       vicini {nome}: |val-sog|_flt={float(ex_dist_flt):.17g} (<1e-9: {ex_vic_flt}), "
            f"mod={mod_vic} (DIVERGE_vs_exact_1e-9_dec={mod_vic != False}, DIVERGE_vs_flt={mod_vic != ex_vic_flt})"
        )

    # D6: controlla_coppie:89 rimasto con sum() invece di math.fsum() + test OverflowError in math.fsum
    for nome_ovf, cp_ovf in (
        ("sum_inf_fsum_ovf", [(1e308, 1), (1e308, 1), (-1e308, 1)]),
        ("sum_finito_fsum_test", [(1.5e308, 1), (-1.5e308, 1), (1.5e308, 1)]),
        ("sum_perm_overflow", [(1.5e308, 1), (1.5e308, 1), (-1.5e308, 1)]),
    ):
        try:
            fsum_ovf = repr(math.fsum(s for s, _ in cp_ovf))
        except Exception as e:
            fsum_ovf = f"{type(e).__name__}: {e}"
        try:
            V.controlla_coppie(cp_ovf)
            cc_res = "ACCETTATO"
        except Exception as e:
            cc_res = f"{type(e).__name__}: {e}"
        print(f"  [D6 {nome_ovf}] math.fsum->{fsum_ovf} | controlla_coppie->{cc_res}")


def _run_mut(nome: str, old: str, new: str) -> str:
    with tempfile.TemporaryDirectory(prefix="r124_m_") as td:
        tmp = Path(td)
        for parte in ("dati", "laboratorio", "guardian"):
            shutil.copytree(
                ROOT / "brain" / parte,
                tmp / "brain" / parte,
                ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"),
            )
        target = tmp / "brain" / "laboratorio" / "verdetto" / "verdetto_d31.py"
        txt = target.read_text(encoding="utf-8")
        cnt = txt.count(old)
        assert cnt == 1, f"{nome}: target trovato {cnt} volte"
        target.write_text(txt.replace(old, new), encoding="utf-8")
        compile(target.read_text(encoding="utf-8"), "verdetto_d31.py", "exec")
        r = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_verdetto_d31",
             "brain.laboratorio.tests.test_prova_generale_dgs12"],
            cwd=tmp, env=NO_NET, capture_output=True, text=True, timeout=120,
        )
        esito = "SOPRAVVISSUTO" if r.returncode == 0 else "UCCISO"
        print(f"  [{esito:13s}] {nome} -> rc={r.returncode}")
        return esito


def mutanti_nuovi_124():
    print("\n=== 3. 4 MUTANTI NUOVI SULLA CORREZIONE #124 ===")
    muts = [
        (
            "M-124-01 screening: L_vicino_a_zero con <= invece di < (bordo ±1e-9)",
            's["L_vicino_a_zero"] = abs(iv[0]) < VICINANZA',
            's["L_vicino_a_zero"] = abs(iv[0]) <= VICINANZA',
        ),
        (
            "M-124-02 screening: L_vicino_a_zero con banda stretta 1e-10 invece di 1e-9",
            's["L_vicino_a_zero"] = abs(iv[0]) < VICINANZA',
            's["L_vicino_a_zero"] = abs(iv[0]) < 1e-10',
        ),
        (
            "M-124-03 screening: L_vicino_a_zero inizializzato a True (persiste su trade=0 / intervallo invalido)",
            '         "L_vicino_a_zero": False}',
            '         "L_vicino_a_zero": True}',
        ),
        (
            "M-124-04 screening: rapporto omette «non cambia l'esito; arrotondamento possibile, #124»",
            '        righe.append("- limite inferiore a meno di 1e-9 R [REGOLA] da 0 (non cambia l\'esito; arrotondamento possibile, #124)")',
            '        righe.append("- limite inferiore a meno di 1e-9 R [REGOLA] da 0")',
        ),
    ]
    esiti = [(nome, _run_mut(nome, old, new)) for nome, old, new in muts]
    sop = sum(1 for _, e in esiti if e == "SOPRAVVISSUTO")
    print(f"[RIEPILOGO MUTANTI NUOVI #124] {sop}/{len(esiti)} sopravvissuti")


def main() -> int:
    print(f"Python: {sys.version.splitlines()[0]} | Platform: {platform.platform()}\n")
    verifica_v3_screening()
    casi_nuovi_non_coperti()
    mutanti_nuovi_124()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
