"""Mandato R17 — Sonde su #114/K15c/PI10 (Compito A) e nono attacco (Compito C) su protocollo_ia02 e pilota_ia02.

SOLO errori in buona fede (E); soli dati inventati; nessun file reale toccato; eseguire con HTTPS_PROXY=http://127.0.0.1:9.
"""
import datetime as dt
import decimal
import hashlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.studi import collaudo_ia02 as C  # noqa: E402
from brain.laboratorio.studi import pilota_ia02 as P  # noqa: E402
from brain.laboratorio.studi import protocollo_ia02 as PR  # noqa: E402


def _no_net_env():
    return dict(
        os.environ,
        HTTPS_PROXY="http://127.0.0.1:9",
        HTTP_PROXY="http://127.0.0.1:9",
        https_proxy="http://127.0.0.1:9",
        http_proxy="http://127.0.0.1:9",
        NO_PROXY="",
        no_proxy="",
    )


def _decimal_binom_cdf(k: int, M: int, p: decimal.Decimal) -> decimal.Decimal:
    """Somma esatta P[Bin(M, p) <= k] via ricorrenza in aritmetica Decimal ad alta precisione."""
    ctx = decimal.getcontext()
    old_prec = ctx.prec
    ctx.prec = 70
    try:
        if p <= 0:
            return decimal.Decimal(1)
        if p >= 1:
            return decimal.Decimal(1 if k >= M else 0)
        q = decimal.Decimal(1) - p
        term = q ** M
        tot = term
        ratio = p / q
        for i in range(1, k + 1):
            term = term * decimal.Decimal(M - i + 1) / decimal.Decimal(i) * ratio
            tot += term
        return tot
    finally:
        ctx.prec = old_prec


def _trade(anno: int, mese: int, r: float) -> dict:
    return {"data": dt.date(anno, mese, 1), "r": r}


def _dati_finti(M: int, per_metodo: dict, fase: int = 1, metodi=("hac", "bootstrap")) -> dict:
    celle = {}
    for c in range(1, 13):
        celle[str(c)] = {}
        for m in metodi:
            v = per_metodo.get(m, {}).get(c)
            if v is None:
                v = ([[0.3, 0.4]] + [[0.1, 0.2]] * (M - 1)) if c in PR.CELLE_POTENZA else ([[0.1, 0.2]] * M)
            celle[str(c)][m] = v
    return {
        "versione": "prova-r17",
        "fase": fase,
        "repliche": M,
        "ricampionamenti": 3999,
        "master": P.MASTER,
        "celle": celle,
    }


def sonde_compito_a():
    # A-114: anni da generatore, range, lista e iteratore singolo esauribile
    tr = [_trade(2005 + k // 12, 1 + k % 12, 1.4 if k % 2 else -0.9) for k in range(60)]

    class IterMonouso:
        def __init__(self, seq):
            self._it = iter(seq)

        def __iter__(self):
            return self

        def __next__(self):
            return next(self._it)

    r_lista = K.verifica(tr, n_prove=3, anni=list(range(2005, 2010)))
    r_range = K.verifica(tr, n_prove=3, anni=range(2005, 2010))
    r_gen = K.verifica(tr, n_prove=3, anni=(a for a in range(2005, 2010)))
    r_iter = K.verifica(tr, n_prove=3, anni=IterMonouso(range(2005, 2010)))
    assert r_gen == r_lista == r_range == r_iter, "A-114: esiti diversi per tipo di Iterable!"
    print(f"[SONDA A-114] anni list==range==gen==iter_monouso: True | promossa={r_lista['promossa']} n={r_lista['n']}")

    # A-K15c: anni vuoti (lista vuota, range(0), generatore vuoto) -> messaggio esplicito
    for nome_caso, val_anni in (("lista_vuota", []), ("range_vuoto", range(0)), ("gen_vuoto", (a for a in ()))):
        for tr_caso in (tr, []):
            try:
                K.verifica(tr_caso, n_prove=2, anni=val_anni)
            except ValueError as e:
                assert "elenco degli anni vuoto" in str(e), f"Messaggio inatteso: {e!r}"
            else:
                raise AssertionError(f"A-K15c non ha sollevato ValueError su {nome_caso}")
    print("[SONDA A-K15c] anni=[], range(0), gen vuoto con tr pieno/vuoto -> ValueError('verifica: elenco degli anni vuoto')")

    # A-PI10: equivalenza di PI10 dopo #112 su serie costante (V=0) e serie periodiche
    serie_cost = [(2.0, 1)] * 100
    assert P.intervallo_hac(serie_cost) is None
    # Simulazione esplicita di PI10 su serie costante: senza guard 'not v > 0', intervallo_valido(mu, mu) -> None
    mu = 2.0
    assert P.intervallo_valido(mu, mu) is None
    # Verifica segno di V_Bartlett su serie oscillanti/quasi-nulle
    v_min = 0.0
    for k_alt in (
        [(1.0, 1), (-1.0, 1)] * 50,
        [(1.0, 1), (0.0, 1), (-1.0, 1)] * 34,
        [(1e-9, 1), (-1e-9, 1)] * 500,
        [(0.123456789, 1), (-0.123456789, 1)] * 500,
    ):
        sk = sum(k for _, k in k_alt)
        m = sum(s for s, _ in k_alt) / sk
        e = [s - m * k for s, k in k_alt]
        n = len(e)
        L = P.ritardi_predefiniti(n)
        v = sum(x * x for x in e) / n
        for h in range(1, L + 1):
            v += 2 * (1 - h / (L + 1)) * sum(e[d] * e[d - h] for d in range(h, n)) / n
        if v < v_min:
            v_min = v
    print(f"[SONDA A-PI10] V=0 costante -> intervallo_valido(mu,mu) is None (True); min_V_oscillanti={v_min:.3e}")


def sonde_compito_c():
    # C-R17-1: Clopper-Pearson unilaterale U_CP e k_massimo con riferimento indipendente Decimal
    casi = [
        (60, 3000, "0.05", 0.025, True),
        (61, 3000, "0.05", 0.025, False),
        (248, 12000, "0.001", 0.025, True),
        (249, 12000, "0.001", 0.025, False),
    ]
    max_err_cdf = decimal.Decimal(0)
    for k, M, d_str, soglia, atteso in casi:
        u = PR.ucp(k, M, float(d_str))
        cdf_dec = _decimal_binom_cdf(k, M, decimal.Decimal(repr(u)))
        err = abs(cdf_dec - decimal.Decimal(d_str))
        if err > max_err_cdf:
            max_err_cdf = err
        assert (u <= soglia) is atteso
    assert PR.ucp(0, 3000, 0.05) - (1 - 0.05 ** (1 / 3000)) < 1e-14
    assert PR.ucp(3000, 3000, 0.05) == 1.0
    assert PR.k_massimo(3000, 0.05) == 60
    assert PR.k_massimo(12000, 0.001) == 248
    p_025_dec = _decimal_binom_cdf(248, 12000, decimal.Decimal("0.025"))
    diff_prob = abs(decimal.Decimal(repr(PR.prob_passare(0.025, 12000, 248))) - p_025_dec)
    print(f"[SONDA C-R17-1] U_CP max_err_CDF_Decimal={float(max_err_cdf):.2e} | diff_prob_passare={float(diff_prob):.2e}")

    # C-R17-2: Conteggi E/P/B/I con uguaglianze esatte su tutti e 4 i margini
    for delta in PR.MARGINI:
        alto = round(0.15 + delta, 10)
        basso = round(0.15 - delta, 10)
        limiti = [
            None,
            [alto, alto + 0.1],          # uguale ad alto -> I
            [alto + 1e-7, alto + 0.1],   # > alto -> P
            [0.0, basso],                # uguale a basso -> I
            [0.0, basso - 1e-7],         # < basso -> B
        ]
        res = PR.conta(limiti, delta)
        assert res == {"E": 1, "P": 1, "B": 1, "I": 2}, f"Errore conteggi Δ={delta}: {res}"
    print("[SONDA C-R17-2] uguaglianze esatte (L==0.15+Δ, U==0.15-Δ -> I) verificate su tutti e 4 i margini")

    # C-R17-3: Classifica, completezza, edge JSON (bool e M=0) e verdetto fase 2
    d_pieno = _dati_finti(12000, {}, fase=2, metodi=("bootstrap",))
    v_ok = PR.valuta(d_pieno, 2)
    assert PR.verdetto_fase2(v_ok, ("bootstrap", 0.05), True) == ("CONFERMATO NEL DOMINIO DEL PILOTA", [])
    # k=248 (247P + 1E = 248 <= 248) passa su cella 11 vs k=249 fallisce
    d_248 = _dati_finti(12000, {"bootstrap": {11: [[0.3, 0.4]] * 247 + [None] + [[0.1, 0.2]] * (12000 - 248)}},
                        fase=2, metodi=("bootstrap",))
    assert PR.verdetto_fase2(PR.valuta(d_248, 2), ("bootstrap", 0.05), True)[0] == "CONFERMATO NEL DOMINIO DEL PILOTA"
    d_249 = _dati_finti(12000, {"bootstrap": {11: [[0.3, 0.4]] * 248 + [None] + [[0.1, 0.2]] * (12000 - 249)}},
                        fase=2, metodi=("bootstrap",))
    esito_249, cause_249 = PR.verdetto_fase2(PR.valuta(d_249, 2), ("bootstrap", 0.05), True)
    assert esito_249 == "NON CONFERMATO" and any("cella 11" in c for c in cause_249)
    # Ogni cella di potenza con P=0 deve bocciare in fase 2
    for cp in PR.CELLE_POTENZA:
        d_p0 = _dati_finti(12000, {"bootstrap": {cp: [[0.1, 0.2]] * 12000}}, fase=2, metodi=("bootstrap",))
        e0, c0 = PR.verdetto_fase2(PR.valuta(d_p0, 2), ("bootstrap", 0.05), True)
        assert e0 == "NON CONFERMATO" and any(str(cp) in x for x in c0)

    # Sonde su input anomali in JSON/CLI in protocollo_ia02:
    # (a) bool in intervallo JSON [False, True]: isinstance(False, (int, float)) == True
    bool_accettato = PR._intervallo_ammesso([False, True])
    # (b) repliche=0 in JSON + liste vuote: completa=True ma tabella() solleva ZeroDivisionError
    d_m0 = {
        "versione": "x", "fase": 1, "repliche": 0, "ricampionamenti": 3999, "master": P.MASTER,
        "celle": {str(c): {"hac": []} for c in range(1, 13)},
    }
    v_m0 = PR.valuta(d_m0, 1)
    m0_err = None
    try:
        PR.tabella(v_m0, 1)
    except Exception as ex:
        m0_err = f"{type(ex).__name__}: {ex}"
    # (c) --candidato malformato senza ':' in CLI -> ValueError invece di rc=2
    with tempfile.TemporaryDirectory() as td:
        fp = Path(td) / "l.json"
        fp.write_text(json.dumps(d_pieno), encoding="utf-8")
        cli_err = None
        try:
            with redirect_stdout(io.StringIO()):
                PR.main(["--limiti", str(fp), "--fase", "2", "--candidato", "bootstrap"])
        except Exception as ex:
            cli_err = f"{type(ex).__name__}: {ex}"
    print(
        f"[SONDA C-R17-3] k248=CONFERMATO, k249=NON_CONFERMATO, P_c=0(3,7,10,12)=NON_CONFERMATO | "
        f"edge: bool_accettato={bool_accettato}, m0_completa={v_m0[('hac', 0.0)]['completa']}->{m0_err}, "
        f"candidato_senza_duepunti->{cli_err}"
    )

    # C-R17-4: Banda diagnostica flussi (con verifica Decimal) & inventario reale 720.000 semi
    assert PR.banda(10000, 0.01 / 216) == (4796, 5204)
    p4795 = float(_decimal_binom_cdf(4795, 10000, decimal.Decimal("0.5")) * 2)
    p4796 = float(_decimal_binom_cdf(4796, 10000, decimal.Decimal("0.5")) * 2)
    assert p4795 <= 0.01 / 216 < p4796
    conf = PR.diagnostica_flussi()
    segn = [x for x in conf if x["segnala"]]
    assert len(conf) == 216 and len(segn) == 0
    inv = PR.inventario_semi({1: 3000, 2: 12000})
    assert inv == {"chiavi": 720000, "semi_distinti": 720000}, inv
    print(f"[SONDA C-R17-4] banda=(4796, 5204) Decimal p(4795)={p4795:.3e} p(4796)={p4796:.3e} | "
          f"diag=216(0 segn) | inv={inv}")

    # C-R17-5: pilota_ia02 dopo #112 (contratto intervallo, casi degeneri, file limiti)
    for lo, hi in ((2.0, 2.0), (2.1, 2.0), (float("nan"), 1.0), (1.0, float("inf")), (float("-inf"), 1.0),
                   (float("-inf"), float("inf"))):
        assert P.intervallo_valido(lo, hi) is None
    cost = [(2.0, 1)] * 100
    assert P.intervallo_hac(cost) is None
    assert P.intervallo_bootstrap(cost, P.flusso(2, 11, 1, 3), ricampionamenti=99) is None
    orig_gen = P.genera
    try:
        P.genera = lambda cella, fase, rep: [(2.0, 1)] * 100
        rc_cost = P.esegui_cella(11, fase=2, repliche=3, ricampionamenti=99, metodi=("hac", "bootstrap"))
    finally:
        P.genera = orig_gen
    for m in ("hac", "bootstrap"):
        assert rc_cost[m]["errori"] == 3 and rc_cost[m]["promosse"] == 0 and rc_cost[m]["coperture"] == 0
        assert rc_cost["limiti"][m] == [None, None, None]
    assert rc_cost["bootstrap"]["distorsione"] is None
    print("[SONDA C-R17-5] contratto #112 verificato su NaN/inf/invertito/nullo e su replica costante -> errori=3, null")


def _run_suite_mutata(src_rel: str, old: str, new: str, nome: str) -> str:
    with tempfile.TemporaryDirectory(prefix="r17_mut_") as td:
        tmp = Path(td)
        for parte in ("dati", "laboratorio", "guardian"):
            shutil.copytree(
                ROOT / "brain" / parte,
                tmp / "brain" / parte,
                ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"),
            )
        target = tmp / "brain" / src_rel
        testo = target.read_text(encoding="utf-8")
        cnt = testo.count(old)
        assert cnt == 1, f"{nome}: target trovato {cnt} volte in {src_rel}"
        target.write_text(testo.replace(old, new), encoding="utf-8")
        compile(target.read_text(encoding="utf-8"), src_rel, "exec")
        proc = subprocess.run(
            [
                sys.executable,
                "-s",
                "-B",
                "-W",
                "error",
                "-m",
                "unittest",
                "-f",
                "brain.laboratorio.tests.test_pilota_ia02",
                "brain.laboratorio.tests.test_protocollo_ia02",
            ],
            cwd=tmp,
            env=_no_net_env(),
            capture_output=True,
            text=True,
            timeout=120,
        )
        esito = "SOPRAVVISSUTO" if proc.returncode == 0 else "UCCISO"
        print(f"  [{esito:13s}] {nome} -> rc={proc.returncode}")
        return esito


def mutanti_nuovi():
    print("\n[COMPITO C — 6 mutanti nuovi]")
    muts = [
        (
            "M-R17-01 protocollo: alto senza margine in _soglie",
            "laboratorio/studi/protocollo_ia02.py",
            "return round(SOGLIA + margine, 10), round(SOGLIA - margine, 10)",
            "return SOGLIA, round(SOGLIA - margine, 10)",
        ),
        (
            "M-R17-02 protocollo: cella 10 omessa dalle celle di potenza",
            "laboratorio/studi/protocollo_ia02.py",
            "CELLE_POTENZA = (3, 7, 10, 12)",
            "CELLE_POTENZA = (3, 7, 12)",
        ),
        (
            "M-R17-03 protocollo: verdetto_fase2 accetta P=0 in potenza",
            "laboratorio/studi/protocollo_ia02.py",
            "        for c, p in v[\"potenze\"].items():\n            if p < 1:",
            "        for c, p in v[\"potenze\"].items():\n            if p < 0:",
        ),
        (
            "M-R17-04 protocollo: diagnostica con range(0, N_BIT) e wrap b[-1]",
            "laboratorio/studi/protocollo_ia02.py",
            "x = sum(1 for t in range(1, N_BIT + 1) if a[t] == b[t + h])",
            "x = sum(1 for t in range(0, N_BIT) if a[t] == b[t + h])",
        ),
        (
            "M-R17-05 pilota: intervallo_valido ammette un estremo infinito",
            "laboratorio/studi/pilota_ia02.py",
            "if not (math.isfinite(lo) and math.isfinite(hi)) or not lo < hi:",
            "if not (math.isfinite(lo) or math.isfinite(hi)) or not lo < hi:",
        ),
        (
            "M-R17-06 pilota: HAC residuo senza *k (s - mu invece di s - mu*k)",
            "laboratorio/studi/pilota_ia02.py",
            "e = [s - mu * k for s, k in coppie]",
            "e = [s - mu for s, k in coppie]",
        ),
    ]
    esiti = []
    for nome, rel, old, new in muts:
        esiti.append((nome, _run_suite_mutata(rel, old, new, nome)))
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"[RIEPILOGO MUTANTI NUOVI] {uccisi}/{len(esiti)} uccisi")


def main() -> int:
    sonde_compito_a()
    sonde_compito_c()
    mutanti_nuovi()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
