"""Mandato R12-bis (Compito B): attacco allo scaricatore solo-cache (scarica_cache.py, dukascopy.richiesta_http).

Zero rete, solo risposte HTTP finte (mock di urllib.request.urlopen e di richiesta_http).
Sonde:
- B-P1: File a metà/corrotti già in cache (in_cache li salta senza validarli) e HTTP 206/204
        (richiesta_http tratta qualunque risposta non-eccezione come status=200 -> 206 parziale o
        204 vuoto salvati in cache come validi/vuoti).
- B-P2: Retry-After in formato HTTP-date su HTTP 429/503 fa esplodere dukascopy.richiesta_http
        con ValueError non gestito da scarica_cache.main (esce con codice 1 anziché 3 o 4).
- B-P3: --continua-su-http: errori intermittenti (500, 500, 404, 500, 500, 404) azzerano di_fila
        su 404/vuoto-200 eludendo --max-errori-di-fila; verifica errore_http vs vuoto; verifica
        tutti i codici d'uscita (0, 2, 3, 4, 5) e ValueError non gestito su --pausa -1.
- B-P4: Crash/eccezione tra _scrivi_atomico e _registra: .bi5 scritto su disco ma assente dal
        registro CSV; alla ripresa l'ora viene saltata come in_cache senza mai comparire nel CSV.
- B-P5: Cache avvelenata da giorno odierno/temporaneamente 404: un b'' iniziale impedisce per
        sempre lo scaricamento successivo anche quando il server espone dati reali.

Nuovi mutanti (MB01..MB04) su scarica_cache.py / dukascopy.py in copia temporanea.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import contextlib
import csv
from datetime import date, datetime, timezone
import io
import lzma
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
import urllib.error

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.dati.pipeline import scarica_cache as SC  # noqa: E402


class _FakeResp:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@contextlib.contextmanager
def _fake_http_env(fake_urlopen):
    """Sostituisce il default `apri` di DK.richiesta_http (zero rete garantito)."""
    orig_defaults = DK.richiesta_http.__defaults__
    DK.richiesta_http.__defaults__ = (3, lambda _s: None, fake_urlopen)
    try:
        yield
    finally:
        DK.richiesta_http.__defaults__ = orig_defaults


def _sample_bi5(val: int = 2000_000) -> bytes:
    raw = DK.RECORD.pack(60, val, val, val, val, 1.0)
    return lzma.compress(raw, format=lzma.FORMAT_ALONE)


def sonda_b_p1_cache_corrotta_e_http_2xx_non_200(base: Path) -> dict:
    # 1. File a metà / corrotto già presente in cache (2024-01-02.bi5) viene saltato silenziosamente come in_cache
    # 2. HTTP 204 (su 2024-01-03) viene scambiato da richiesta_http per 200 vuoto e salvato come vuoto-200 in cache
    # 3. HTTP 206 (su 2024-01-04) con byte troncati viene rilevato solo dal decoder LZMA -> halt rc=4 (esito danneggiato)
    d = base / "bp1"
    d.mkdir()
    cache, reg = d / "cache", d / "reg.csv"
    corrotto = cache / "XAUUSD" / "2024-01-02.bi5"
    corrotto.parent.mkdir(parents=True, exist_ok=True)
    corrotto.write_bytes(b"\x5d\x00\x00TRUNCATED_GARBAGE")

    chiamate = []

    def fake_urlopen(req, timeout=30):
        chiamate.append(req.full_url)
        if "/2024/00/03/" in req.full_url:
            return _FakeResp(204, b"")
        if "/2024/00/04/" in req.full_url:
            return _FakeResp(206, b"\x5d\x00PARTIAL_206")
        return _FakeResp(200, _sample_bi5())

    out = io.StringIO()
    with _fake_http_env(fake_urlopen), patch("time.sleep"), contextlib.redirect_stdout(out):
        rc = SC.main([
            "--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
            "--cache", str(cache), "--registro", str(reg), "--pausa", "0",
        ])

    righe = list(csv.DictReader(reg.read_text(encoding="utf-8").splitlines()))
    f03 = cache / "XAUUSD" / "2024-01-03.bi5"
    f04 = cache / "XAUUSD" / "2024-01-04.bi5"
    r03 = [r for r in righe if r["giorno"] == "2024-01-03"]
    r04 = [r for r in righe if r["giorno"] == "2024-01-04"]
    return {
        "rc": rc,
        "giorno_02_corrotto_saltato_come_in_cache": corrotto.read_bytes().endswith(b"TRUNCATED_GARBAGE") and all(
            "/2024/00/02/" not in u for u in chiamate
        ),
        "http_204_salvato_vuoto_200": f03.exists() and f03.read_bytes() == b"" and bool(
            r03 and r03[0]["http"] == "200" and r03[0]["esito"] == "vuoto-200"
        ),
        "http_206_non_salvato_ferma_decoder": (not f04.exists()) and bool(
            r04 and r04[0]["http"] == "200" and r04[0]["esito"] == "danneggiato"
        ),
        "r03": r03,
        "r04": r04,
    }


def sonda_b_p2_retry_after_http_date_crash(base: Path) -> dict:
    d = base / "bp2"
    d.mkdir()
    cache, reg = d / "cache", d / "reg.csv"

    def err_429_http_date(req, timeout=30):
        raise urllib.error.HTTPError(
            req.full_url, 429, "Too Many Requests",
            {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}, io.BytesIO(b""),
        )

    crashed = None
    with _fake_http_env(err_429_http_date), patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
        try:
            SC.main([
                "--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                "--cache", str(cache), "--registro", str(reg), "--pausa", "0",
            ])
            rc = 0
        except ValueError as exc:
            crashed = f"{type(exc).__name__}: {exc}"
            rc = 1
    return {"crash_retry_after_http_date": crashed is not None, "eccezione": crashed, "rc_implicito": rc}


def sonda_b_p3_continua_su_http_di_fila_e_exit_codes(base: Path) -> dict:
    d = base / "bp3"
    d.mkdir()
    # 1. Su 25 giorni feriali: 19 HTTPError(500) + 1 singolo 404 + 5 HTTPError(500) (= 24 errori su 25) ->
    #    il 404 azzera di_fila, quindi MAX_HTTP_DI_FILA=20 NON scatta e chiude con rc=5 (invece di rc=4)!
    seq = [500] * 19 + [404] + [500] * 10

    def mock_req(url, **kw):
        st = seq.pop(0) if seq else 404
        if st == 404:
            return (404, None, 1)
        raise urllib.error.HTTPError(url, st, "Err", {}, io.BytesIO(b""))

    c1, r1 = d / "c1", d / "r1.csv"
    with patch.object(DK, "richiesta_http", side_effect=mock_req), patch("time.sleep"), \
         contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc_cont = SC.main([
            "--simbolo", "XAUUSD", "--inizio", "2024-01-01", "--fine", "2024-02-02",
            "--cache", str(c1), "--registro", str(r1), "--pausa", "0", "--continua-su-http",
        ])
    righe1 = list(csv.DictReader(r1.read_text(encoding="utf-8").splitlines()))
    f_err = c1 / "XAUUSD" / "2024-01-01.bi5"
    f_404 = [r["giorno"] for r in righe1 if r["esito"] == "404"]

    # 2. Exit codes ufficiali: 0 (ok), 2 (inizio > fine), 3 (ConnectionError rete assente),
    #    4 (Fermo: HTTP senza --continua o >=20 HTTP di fila), 5 (finito con giorni in errore http)
    def err_rete(url, **kw):
        raise ConnectionError("rete assente")

    def err_http_403(url, **kw):
        raise urllib.error.HTTPError(url, 403, "Forbidden", {}, io.BytesIO(b""))

    def ok_404(url, **kw):
        return (404, None, 1)

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        with patch.object(DK, "richiesta_http", side_effect=ok_404), patch("time.sleep"):
            rc0 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                           "--cache", str(d / "c0"), "--registro", str(d / "r0.csv"), "--pausa", "0"])
        rc2 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-05", "--fine", "2024-01-02",
                       "--cache", str(d / "c2"), "--registro", str(d / "r2.csv")])
        with patch.object(DK, "richiesta_http", side_effect=err_rete), patch("time.sleep"):
            rc3 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                           "--cache", str(d / "c3"), "--registro", str(d / "r3.csv"), "--pausa", "0"])
        with patch.object(DK, "richiesta_http", side_effect=err_http_403), patch("time.sleep"):
            rc4_singolo = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                                   "--cache", str(d / "c4a"), "--registro", str(d / "r4a.csv"), "--pausa", "0"])
            rc4_20fila = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-01", "--fine", "2024-01-31",
                                  "--cache", str(d / "c4b"), "--registro", str(d / "r4b.csv"), "--pausa", "0",
                                  "--continua-su-http"])
            rc5_http = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                                "--cache", str(d / "c5"), "--registro", str(d / "r5.csv"), "--pausa", "0",
                                "--continua-su-http"])

        try:
            with patch.object(DK, "richiesta_http", side_effect=ok_404):
                rc_pneg = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-03",
                                   "--cache", str(d / "cneg"), "--registro", str(d / "rneg.csv"),
                                   "--pausa", "-1"])
        except ValueError as exc:
            rc_pneg = f"ValueError:{exc}"

    return {
        "19_err_1_404_6_err_azzera_di_fila_rc": rc_cont,
        "errori_http_registrati": sum(1 for r in righe1 if str(r["esito"]).startswith("http-")),
        "vuoti_404_registrati": len(f_404),
        "errore_http_non_scrive_bi5": not f_err.exists(),
        "vuoto_404_scrive_bi5_vuoto": bool(f_404 and (c1 / "XAUUSD" / f"{f_404[0]}.bi5").stat().st_size == 0),
        "exit_codes": {"rc0": rc0, "rc2": rc2, "rc3": rc3, "rc4_singolo": rc4_singolo,
                       "rc4_20fila": rc4_20fila, "rc5_http": rc5_http},
        "pausa_negativa": rc_pneg,
    }


def sonda_b_p4_interruzione_fra_scrivi_e_registra(base: Path) -> dict:
    d = base / "bp4"
    d.mkdir()
    cache, reg = d / "cache", d / "reg.csv"
    bi5_ok = _sample_bi5()

    n_reg = 0
    orig_reg = SC._registra

    def registra_che_cade(percorso, riga):
        nonlocal n_reg
        n_reg += 1
        if n_reg == 2:
            raise OSError("crash simulato tra _scrivi_atomico e _registra")
        return orig_reg(percorso, riga)

    crash_exc = None
    with patch.object(DK, "richiesta_http", return_value=(200, bi5_ok, 1)), \
         patch.object(SC, "_registra", side_effect=registra_che_cade), \
         patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc1 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
                           "--cache", str(cache), "--registro", str(reg), "--pausa", "0"])
        except OSError as exc:
            crash_exc = str(exc)
            rc1 = 1

    with patch.object(DK, "richiesta_http", return_value=(200, bi5_ok, 1)), \
         patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
        rc2 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
                       "--cache", str(cache), "--registro", str(reg), "--pausa", "0"])

    f03 = cache / "XAUUSD" / "2024-01-03.bi5"
    righe = list(csv.DictReader(reg.read_text(encoding="utf-8").splitlines()))
    return {
        "rc_prima_esecuzione": rc1,
        "crash_exc": crash_exc,
        "rc_ripresa": rc2,
        "file_03_presente_in_cache": f03.exists(),
        "righe_csv": len(righe),
        "giorni_csv": [r["giorno"] for r in righe],
        "giorno_03_manca_nel_csv_dopo_ripresa": all(r["giorno"] != "2024-01-03" for r in righe),
    }


def sonda_b_p5_avvelenamento_404_temporaneo(base: Path) -> dict:
    d = base / "bp5"
    d.mkdir()
    cache, reg = d / "cache", d / "reg.csv"
    bi5_ok = _sample_bi5()

    with patch.object(DK, "richiesta_http", return_value=(404, None, 1)), \
         patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
        SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                 "--cache", str(cache), "--registro", str(reg), "--pausa", "0"])

    f02 = cache / "XAUUSD" / "2024-01-02.bi5"
    dim_prima = f02.stat().st_size

    chiamate = []

    def serve_reali(url, **kw):
        chiamate.append(url)
        return (200, bi5_ok, 1)

    with patch.object(DK, "richiesta_http", side_effect=serve_reali), \
         patch("time.sleep"), contextlib.redirect_stdout(io.StringIO()):
        SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                 "--cache", str(cache), "--registro", str(reg), "--pausa", "0"])

    return {
        "byte_dopo_404_iniziale": dim_prima,
        "chiamate_http_al_secondo_giro": len(chiamate),
        "cache_resta_vuota_per_sempre": f02.stat().st_size == 0 and len(chiamate) == 0,
    }


NUOVI_MUTANTI_B = [
    (
        "MB01",
        "brain/dati/pipeline/dukascopy.py",
        r'float\(e\.headers\.get\("Retry-After"\) or 0\) if e\.headers else 0\.0',
        "0.0",
        "ignora Retry-After in dukascopy.richiesta_http",
    ),
    (
        "MB02",
        "brain/dati/pipeline/scarica_cache.py",
        r'\bdi_fila = 0\b',
        "pass  # non azzera di_fila",
        "non azzera di_fila dopo risposta valida 200/404",
    ),
    (
        "MB03",
        "brain/dati/pipeline/scarica_cache.py",
        r'with open\(registro, "a",',
        'with open(registro, "w",',
        "sovrascrive il CSV del registro invece di accodare",
    ),
    (
        "MB04",
        "brain/dati/pipeline/scarica_cache.py",
        r'if continua_su_http:',
        "if False and continua_su_http:",
        "disattiva il flag --continua-su-http trattando gli errori HTTP come fatali",
    ),
]


def _run_mut(args):
    cod, rel, pattern, repl, desc = args
    with tempfile.TemporaryDirectory() as tmp:
        radice = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT / "brain", radice / "brain",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
        p = radice / rel
        orig = p.read_text(encoding="utf-8")
        # Sostituzione mirata (ultima occorrenza se di_fila = 0 compare due volte)
        matches = list(re.finditer(pattern, orig))
        if not matches:
            return {"codice": cod, "stato": "ERR_MATCH", "rc": -1, "desc": desc}
        m = matches[-1]
        mut = orig[:m.start()] + repl + orig[m.end():]
        assert mut != orig
        p.write_text(mut, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(radice))
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.dati.tests.test_scarica_cache", "brain.dati.tests.test_dukascopy"],
            cwd=str(radice), env=env, capture_output=True, text=True, timeout=180,
        )
        return {"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode, "desc": desc}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        print("B-P1:", sonda_b_p1_cache_corrotta_e_http_2xx_non_200(base))
        print("B-P2:", sonda_b_p2_retry_after_http_date_crash(base))
        print("B-P3:", sonda_b_p3_continua_su_http_di_fila_e_exit_codes(base))
        print("B-P4:", sonda_b_p4_interruzione_fra_scrivi_e_registra(base))
        print("B-P5:", sonda_b_p5_avvelenamento_404_temporaneo(base))
    print("=== B MUTANTI (MB01..MB04) ===")
    with ThreadPoolExecutor(max_workers=2) as pool:
        for m in pool.map(_run_mut, NUOVI_MUTANTI_B):
            print("MUTANTE:", m)


if __name__ == "__main__":
    main()
