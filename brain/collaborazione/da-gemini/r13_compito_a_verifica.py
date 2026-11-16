"""Mandato R13 · Compito A: verifica delle correzioni R12-bis su origin/feat/esecutore-h002 (fd879ed).

- Controlla prima che la rete sia bloccata (HTTPS_PROXY=http://127.0.0.1:9).
- Riesegue le sonde R12-bis (A3, B, C) sul codice nuovo e verifica rilievo per rilievo
  se #48-#59 risultano chiusi, chiusi in parte o ancora aperti.
- Rilancia il mutante MC05 contro brain.laboratorio.tests.test_esegui_h002.
- Verifica con controprova tecnica la motivazione con cui Claude ha respinto R12bis-B-04.
"""
from __future__ import annotations

import contextlib
import csv
from datetime import date
import io
import json
import lzma
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
DA_GEMINI = Path(__file__).resolve().parent
if str(DA_GEMINI) not in sys.path:
    sys.path.insert(0, str(DA_GEMINI))

from brain.dati.pipeline import calendario as CAL  # noqa: E402
from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.dati.pipeline import scarica_cache as SC  # noqa: E402
from brain.governance.censimento import riconta as RIC  # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402

import r12bis_attacco_criteri as A3_MOD  # noqa: E402
import r12bis_attacco_riconta as C_MOD  # noqa: E402


def verifica_rete_bloccata() -> dict:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato: bloccare la rete (es. HTTPS_PROXY=http://127.0.0.1:9)")
    bloccata = False
    err = ""
    try:
        urllib.request.urlopen("https://datafeed.dukascopy.com/", timeout=2)
    except Exception as exc:
        bloccata = True
        err = f"{type(exc).__name__}: {exc}"
    if not bloccata:
        raise RuntimeError("La rete NON risulta bloccata!")
    return {"HTTPS_PROXY": proxy, "rete_bloccata": bloccata, "err": err}


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


def _sample_bi5(val: int = 2000_000) -> bytes:
    raw = DK.RECORD.pack(60, val, val, val, val, 1.0)
    return lzma.compress(raw, format=lzma.FORMAT_ALONE)


def verifica_compito_a_3() -> dict:
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        with patch.object(E, "ANCORA_GIT", False):
            # #51 P1: ora non-ISO + swap cache sullo stesso path
            out["A3_P1_nuovo"] = A3_MOD.sonda_p1_scelte_e_cache_path(base)

            # #48 P2: moduli fuori FILE_CODICE + test reale di modifica esecuzione/__init__.py su copia con git init (ANCORA_GIT=True)
            sigillati = {str((REPO_ROOT / f).resolve()) for f in E.FILE_CODICE}
            caricati_non_sig = sorted({
                Path(m.__file__).resolve().relative_to(REPO_ROOT).as_posix()
                for name, m in sys.modules.items()
                if name.startswith("brain") and getattr(m, "__file__", None)
                and str(Path(m.__file__).resolve()) not in sigillati
            })
            d2 = base / "a3_p2_new"
            d2.mkdir()
            radice = d2 / "repo"
            shutil.copytree(REPO_ROOT / "brain", radice / "brain",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
            subprocess.run(["git", "init", "-q"], cwd=str(radice), check=True)
            subprocess.run(["git", "-C", str(radice), "config", "user.name", "T"], check=True)
            subprocess.run(["git", "-C", str(radice), "config", "user.email", "t@invalid"], check=True)
            marker = d2 / "pwned_marker.txt"
            scheda2 = d2 / "H-002.md"
            scheda2.write_text("# H-002\n", encoding="utf-8")
            reg2, cpath2, rsv2 = radice / "reg.json", d2 / "cache", d2 / "sv.md"
            sv_i, sv_f = E.PERIODO_SVILUPPO
            b_sv, a_sv = SN.mercato(sv_i, 10, seme=1, sd=0.7)
            A3_MOD._crea_cache_completa(cpath2, sv_i, sv_f, b_sv, a_sv)
            S.sigilla(reg2, "H-002", scheda2, ["V-T", "V-S"], "2026-11-16T01:00:00Z", codice=E.impronte_codice())
            subprocess.run(["git", "-C", str(radice), "add", "."], check=True)
            subprocess.run(["git", "-C", str(radice), "commit", "-q", "-m", "init"], check=True)
            init_esec = radice / "brain" / "laboratorio" / "esecuzione" / "__init__.py"
            init_esec.write_text(
                init_esec.read_text(encoding="utf-8")
                + f"\nfrom pathlib import Path as _P\n_P({str(marker)!r}).write_text('ESEGUITO', encoding='utf-8')\n",
                encoding="utf-8",
            )
            proc2 = subprocess.run(
                [sys.executable, "-s", "-B", "-m", "brain.laboratorio.esecuzione.esegui_h002",
                 "--modalita", "sviluppo", "--rapporto", str(rsv2), "--registro", str(reg2),
                 "--scheda", str(scheda2), "--cache", str(cpath2), "--ora", "2026-11-16T01:00:00Z"],
                cwd=str(radice), env=dict(os.environ, PYTHONPATH=str(radice)),
                capture_output=True, text=True, timeout=120,
            )
            reg_fake = d2 / "reg_badcode.json"
            S.sigilla(reg_fake, "H-002", scheda2, ["V-T", "V-S"], "2026-11-16T01:00:00Z", codice={"fake": "0" * 64})
            try:
                C.carica(cpath2 / "XAUUSD", cpath2 / "XAUUSD_ASK", sv_i, sv_f, "sviluppo", reg_fake, "H-002", scheda2)
                c_carica_ignora = True
            except ValueError as exc:
                c_carica_ignora = f"BLOCCATO:{exc}"
            out["A3_P2_nuovo"] = {
                "esecuzione___init___in_FILE_CODICE": "brain/laboratorio/esecuzione/__init__.py" in E.FILE_CODICE,
                "moduli_brain_caricati_fuori_FILE_CODICE": caricati_non_sig,
                "rc_con___init___manomesso": proc2.returncode,
                "stderr_init_manomesso": proc2.stderr.strip(),
                "marker_scritto_all_import": marker.exists(),
                "c_carica_controlla_codice": c_carica_ignora,
            }

            # #49 P3: 1 solo tick alle 00:00 UTC su tutti i feriali
            out["A3_P3_nuovo"] = A3_MOD.sonda_p3_aggira_feriali_vuoti(base)

            # #50 P4: chiusure osservate 2005-2023
            out["A3_P4_nuovo"] = A3_MOD.sonda_p4_falsi_positivi_chiusure_oro(base)

            # #51 P5: manomissione senza ANCORA_GIT (e poi test reale con ANCORA_GIT=True qui sotto)
            out["A3_P5_senza_git"] = A3_MOD.sonda_p5_manomissione_registro(base)

            # A3-P6: DGS-03
            out["A3_P6_dgs03"] = A3_MOD.sonda_p6_dgs03_fallback_indietro()

            # #48 P7: C.carica -> S.controlla_sigillo(codice=None) ora verifica i file su disco
            d7 = base / "a3_p7_new"
            d7.mkdir()
            sc7 = d7 / "H-002.md"
            sc7.write_text("# H-002\n", encoding="utf-8")
            reg7 = d7 / "reg.json"
            S.sigilla(reg7, "H-002", sc7, ["V-T", "V-S"], "2026-11-16T01:00:00Z", codice={"solo_chiave": "abc"})
            try:
                S.controlla_sigillo(reg7, "H-002", sc7)
                p7_no_code = False
            except ValueError as exc:
                p7_no_code = f"BLOCCATO:{exc}"
            out["A3_P7_nuovo"] = {"controlla_sigillo_senza_codice": p7_no_code}

        # Test P5 CON ANCORA_GIT=True in un mini repository git reale temporaneo
        repo = base / "git_reg"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=str(repo), check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@invalid"], check=True)
        reg = repo / "reg.json"
        scheda = repo / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], "2026-11-16T01:00:00Z")
        S.registra_esecuzione(reg, "H-002", {"ruolo": "sviluppo", "variante": "V-T", "promossa": False},
                              "2026-11-16T01:00:00Z")
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "init"], check=True)
        # Manomissione: cambio promossa False -> True sulla voce già committata!
        raw = json.loads(reg.read_text(encoding="utf-8"))
        raw["esecuzioni"][0]["promossa"] = True
        reg.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        try:
            S.controlla_ancora(reg, repo)
            bloccata_git = False
            err_git = ""
        except ValueError as exc:
            bloccata_git = True
            err_git = str(exc)
        out["A3_P5_con_ancora_git"] = {"bloccata": bloccata_git, "err": err_git}

    # MC05: rimuovere criteri.py da moduli_brain / FILE_CODICE ora DEVE morire!
    muts = [
        (
            "MC05_OLD",
            "brain/laboratorio/esecuzione/esegui_h002.py",
            'FILE_CODICE = tuple(moduli_brain())',
            'FILE_CODICE = tuple(f for f in moduli_brain() if not f.endswith("criteri.py"))',
            "rimuove criteri.py da FILE_CODICE via filtro",
        ),
        (
            "MC05_MODULI",
            "brain/laboratorio/esecuzione/esegui_h002.py",
            '    return sorted(f.relative_to(radice).as_posix() for f in file)',
            '    return sorted(f.relative_to(radice).as_posix() for f in file if not f.name == "criteri.py")',
            "esclude criteri.py da moduli_brain()",
        ),
    ]
    res_mc05 = []
    for cod, rel, target, repl, desc in muts:
        with tempfile.TemporaryDirectory() as tmp:
            rad = Path(tmp) / "repo"
            shutil.copytree(REPO_ROOT / "brain", rad / "brain",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
            p = rad / rel
            orig = p.read_text(encoding="utf-8")
            assert orig.count(target) == 1, cod
            p.write_text(orig.replace(target, repl, 1), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
                 "brain.laboratorio.tests.test_esegui_h002"],
                cwd=str(rad), env=dict(os.environ, PYTHONPATH=str(rad)),
                capture_output=True, text=True, timeout=240,
            )
            res_mc05.append({"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode})
    out["MC05_rilancio"] = res_mc05
    return out


def verifica_compito_b() -> dict:
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        # B-P1 (#53 corrotto in cache + #54 HTTP 204/206): usando patch su urllib.request.urlopen e time.sleep
        d1 = base / "bp1"
        d1.mkdir()
        cache, reg = d1 / "cache", d1 / "reg.csv"
        corrotto = cache / "XAUUSD" / "2024-01-02.bi5"
        corrotto.parent.mkdir(parents=True, exist_ok=True)
        corrotto.write_bytes(b"\x5d\x00\x00TRUNCATED_GARBAGE")
        chiamate = []

        def fake_urlopen_1(req, timeout=60):
            chiamate.append(req.full_url)
            if "/2024/00/02/" in req.full_url:
                return _FakeResp(200, _sample_bi5())
            if "/2024/00/03/" in req.full_url:
                return _FakeResp(204, b"")
            if "/2024/00/04/" in req.full_url:
                return _FakeResp(206, _sample_bi5())
            return _FakeResp(200, _sample_bi5())

        with patch.object(DK.urllib.request, "urlopen", side_effect=fake_urlopen_1), \
             patch.object(DK.time, "sleep"), patch.object(SC.time, "sleep"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc1 = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
                           "--cache", str(cache), "--registro", str(reg), "--pausa", "0"])
        righe1 = list(csv.DictReader(reg.read_text(encoding="utf-8").splitlines()))
        rovinato_backup = cache / "XAUUSD" / ".2024-01-02.rovinato"
        out["B_P1_nuovo"] = {
            "rc": rc1,
            "giorno_02_corrotto_quarantena_e_riscaricato": rovinato_backup.exists() and len(
                DK.decodifica((cache / "XAUUSD" / "2024-01-02.bi5").read_bytes(), date(2024, 1, 2), 3)) == 1,
            "http_204_registrato_204_e_vuoto_204": [
                (r["http"], r["esito"]) for r in righe1 if r["giorno"] == "2024-01-03"
            ],
            "http_206_ferma_come_errore_http": [
                (r["http"], r["esito"]) for r in righe1 if r["giorno"] == "2024-01-04"
            ] and rc1 == 4,
        }

        # B-P2 (#52 Retry-After HTTP-date)
        d2 = base / "bp2"
        d2.mkdir()
        sleep_calls = []

        def err_429_date(req, timeout=60):
            raise urllib.error.HTTPError(
                req.full_url, 429, "Too Many Requests",
                {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}, io.BytesIO(b""),
            )

        with patch.object(DK.urllib.request, "urlopen", side_effect=err_429_date), \
             patch.object(DK.time, "sleep", side_effect=lambda s: sleep_calls.append(s)), \
             patch.object(SC.time, "sleep"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            # Nota: teniamo tentativi=2 via patch su scarica_periodo -> richiesta_http o testiamo direttamente DK.richiesta_http
            try:
                DK.richiesta_http("https://example.invalid/x.bi5", tentativi=2)
                crashed = False
            except ConnectionError:
                crashed = "ConnectionError (atteso dopo backoff)"
            except ValueError as exc:
                crashed = f"ValueError:{exc}"
        out["B_P2_nuovo"] = {"esito_dk_richiesta_http_date": crashed, "sleep_calls": sleep_calls}

        # B-P3 pausa negativa (#54) + exit codes
        rc_pneg = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                           "--cache", str(base / "cpn"), "--pausa", "-1"])
        out["B_P3_pausa_neg"] = {"rc_pausa_negativa": rc_pneg}

        # CONTROPROVA B-04: blocco totale su tutti i giorni feriali (lun-ven HTTP 403), mentre sabato/domenica danno 404!
        # In un periodo di 60 giorni ci sono solo 5 feriali fra un weekend e l'altro -> di_fila non supera mai 5 < 20!
        d_b04 = base / "b04_counter"
        d_b04.mkdir()
        c_b04, r_b04 = d_b04 / "cache", d_b04 / "reg.csv"

        def mock_ban_feriali(url, **kw):
            # url termina .../AAAA/MM0/GG/BID_candles_min_1.bi5
            parti = url.split("/")
            a, m0, g = int(parti[-4]), int(parti[-3]), int(parti[-2])
            if date(a, m0 + 1, g).weekday() >= 5:
                return (404, None, 1)
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, io.BytesIO(b""))

        with patch.object(DK, "richiesta_http", side_effect=mock_ban_feriali), \
             patch.object(SC.time, "sleep"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc_ban = SC.main([
                "--simbolo", "XAUUSD", "--inizio", "2024-01-01", "--fine", "2024-02-29",
                "--cache", str(c_b04), "--registro", str(r_b04), "--pausa", "0", "--continua-su-http",
            ])
        righe_ban = list(csv.DictReader(r_b04.read_text(encoding="utf-8").splitlines()))
        out["B_04_controprova_ban_feriali"] = {
            "feriali_in_errore_403": sum(1 for r in righe_ban if r["esito"] == "http-403"),
            "weekend_404": sum(1 for r in righe_ban if r["esito"] == "404"),
            "rc": rc_ban,
            "max_http_di_fila_scattato": rc_ban == 4,
            "spiegazione": "100% dei giorni feriali in errore HTTP 403 su 60 giorni (44 errori totali) ma i weekend 404 azzerano di_fila ogni 5 giorni",
        }

        # B-P4 (#53 ripresa dopo crash tra _scrivi_atomico e _registra -> in-cache-non-registrato)
        d4 = base / "bp4"
        d4.mkdir()
        c4, r4 = d4 / "cache", d4 / "reg.csv"
        bi5_ok = _sample_bi5()
        n_reg = 0
        orig_reg = SC._registra

        def reg_cade(percorso, riga):
            nonlocal n_reg
            n_reg += 1
            if n_reg == 2:
                raise OSError("crash simulato")
            return orig_reg(percorso, riga)

        with patch.object(DK, "richiesta_http", return_value=(200, bi5_ok, 1)), \
             patch.object(SC, "_registra", side_effect=reg_cade), \
             patch.object(SC.time, "sleep"), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
                         "--cache", str(c4), "--registro", str(r4), "--pausa", "0"])
            except OSError:
                pass
        with patch.object(DK, "richiesta_http", return_value=(200, bi5_ok, 1)), \
             patch.object(SC.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            rc4_ok = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-04",
                              "--cache", str(c4), "--registro", str(r4), "--pausa", "0"])
        righe4 = list(csv.DictReader(r4.read_text(encoding="utf-8").splitlines()))
        out["B_P4_nuovo"] = {
            "rc_ripresa": rc4_ok,
            "esito_giorno_03": [r["esito"] for r in righe4 if r["giorno"] == "2024-01-03"],
            "giorni_nel_csv": sorted(r["giorno"] for r in righe4),
        }

        # B-P5 (#55 --riprova-vuoti riscarica un 404/vuoto feriale precedente)
        d5 = base / "bp5"
        d5.mkdir()
        c5, r5 = d5 / "cache", d5 / "reg.csv"
        with patch.object(DK, "richiesta_http", return_value=(404, None, 1)), \
             patch.object(SC.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                     "--cache", str(c5), "--registro", str(r5), "--pausa", "0"])
        with patch.object(DK, "richiesta_http", return_value=(200, bi5_ok, 1)), \
             patch.object(SC.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            rc5_rip = SC.main(["--simbolo", "XAUUSD", "--inizio", "2024-01-02", "--fine", "2024-01-02",
                               "--cache", str(c5), "--registro", str(r5), "--pausa", "0", "--riprova-vuoti"])
        out["B_P5_nuovo"] = {
            "rc_riprova_vuoti": rc5_rip,
            "byte_dopo_riprova": (c5 / "XAUUSD" / "2024-01-02.bi5").stat().st_size,
            "riparato_con_flag": (c5 / "XAUUSD" / "2024-01-02.bi5").stat().st_size > 0,
        }
    return out


def verifica_compito_c() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        return {
            "C_P1_nuovo": C_MOD.sonda_c_p1_campi_diversi_e_uscite_annidate(base),
            "C_P2_nuovo": C_MOD.sonda_c_p2_altre_sintassi_esecuzione(base),
            "C_P3_nuovo": C_MOD.sonda_c_p3_date_non_iso_e_duka(base),
            "C_P4_nuovo": C_MOD.sonda_c_p4_prezzi_non_coperti(),
            "C_P5_nuovo": C_MOD.sonda_c_p5_leak_contenuto_e_prezzi_su_stdout(base),
        }


def main() -> None:
    print("=== CHECK RETE ===")
    print(verifica_rete_bloccata())
    print("=== COMPITO A · VERIFICA A3 + MC05 ===")
    for k, v in verifica_compito_a_3().items():
        print(k, v)
    print("=== COMPITO A · VERIFICA B + CONTROPROVA B-04 ===")
    for k, v in verifica_compito_b().items():
        print(k, v)
    print("=== COMPITO A · VERIFICA C ===")
    for k, v in verifica_compito_c().items():
        print(k, v)


if __name__ == "__main__":
    main()
