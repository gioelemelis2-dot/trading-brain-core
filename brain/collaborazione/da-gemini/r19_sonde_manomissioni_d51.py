"""Mandato R19 — Sonde indipendenti, manomissioni (Compiti B, C) e matrice D-51 (Compito D) su 1431190.

Solo dati e registri sintetici in cartelle temporanee; rete bloccata; nessuna modifica al repository di lavoro.
"""
import contextlib
import hashlib
import io
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from fractions import Fraction
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as EH  # noqa: E402
from brain.laboratorio.esecuzione import esegui_verifica as EV  # noqa: E402
from brain.laboratorio.esecuzione import manifesto as MF  # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.simulatori import orb_londra as O  # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as M  # noqa: E402
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

ORA = "2026-11-23T10:00:00Z"
LETTURA = date(2010, 1, 4)
ACCESSORIE = 35
INIZIO = LETTURA + timedelta(days=ACCESSORIE)
FINE = M.fine_per_sedute(INIZIO, 1000)
B_INIZIO = date(2015, 1, 5)
B_FINE = M.fine_per_sedute(B_INIZIO + timedelta(days=ACCESSORIE), 1000)
SVILUPPO = (date(2024, 1, 1), date(2024, 12, 31))


def contratto(ipotesi="H-R19", **k):
    c = {
        "modello": "H-003",
        "ipotesi": ipotesi,
        "destinazione": "test",
        "simulatore": "orb_londra",
        "variante": "V-T",
        "m": 1,
        "mercato": "XAUUSD",
        "metro": "D-31",
        "seme": 20261123,
        "screening_seme": 9,
        "potenza_stimata": 0.6,
        "date_accessorie": ACCESSORIE,
        "sedute": 1000,
        "veto_blocchi": {"soglia": -0.25, "minimo_trade": 50},
        "sviluppo": [SVILUPPO[0].isoformat(), SVILUPPO[1].isoformat()],
    }
    c.update(k)
    return c


def testo_scheda(c):
    return (
        f"# {c.get('ipotesi', 'H-X')} — scheda test R19\n\n"
        f"```json contratto-h003\n{json.dumps(c, indent=2, ensure_ascii=False)}\n```\n"
    )


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "ASSENTE"


def stato_breve(reg: Path, ris: Path) -> str:
    esec = len(S.leggi(reg)["esecuzioni"]) if reg.exists() else 0
    if ris.exists():
        st = RV.stato(ris)
        return (
            f"prove_sha={sha_file(reg)}(esec={esec}) | "
            f"riserva_sha={sha_file(ris)}(ap={len(st['aperture'])},rif={len(st['rifiuti'])},"
            f"pren={st['giorni']['prenotato']},cons={st['giorni']['consumato']})"
        )
    return f"prove_sha={sha_file(reg)}(esec={esec}) | riserva=ASSENTE"


def prepara_repo_copia(base: Path, cache: Path, cache_sv: Path, ipotesi="H-R19", id_="P1",
                       alfa_tot=0.05, con_git=True, anche_h002=False):
    """Copia completa di brain/ in un repo git temporaneo con bare remote."""
    repo = base / "repo"
    remoto = base / "remoto.git"
    if con_git:
        subprocess.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
        subprocess.run(["git", "clone", "-q", str(remoto), str(repo)], check=True, capture_output=True)
        g = ["git", "-C", str(repo), "-c", "user.name=r19", "-c", "user.email=r19@invalid"]
        subprocess.run(g + ["checkout", "-q", "-b", "principale"], check=True)
    else:
        repo.mkdir(parents=True)
        g = []
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(
            ROOT / "brain" / parte,
            repo / "brain" / parte,
            ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"),
        )
    if (ROOT / "brain" / "__init__.py").exists():
        (repo / "brain" / "__init__.py").write_bytes((ROOT / "brain" / "__init__.py").read_bytes())
    reg = repo / EV.REL_REGISTRO_PROVE
    ris = repo / EV.REL_RISERVA
    if reg.exists():
        reg.unlink()
    if ris.exists():
        ris.unlink()
    RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), alfa_tot, ORA)
    scheda = repo / "brain" / "laboratorio" / "ipotesi" / f"{ipotesi}.md"
    scheda.write_text(testo_scheda(contratto(ipotesi)), encoding="utf-8")
    if anche_h002:
        scheda_h002 = repo / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md"
        S.sigilla(reg, "H-002", scheda_h002, ["V-T", "V-S"], ORA, codice=EH.impronte_codice(repo))
    S.sigilla(reg, ipotesi, scheda, ["V-T"], ORA, codice=EV.impronte_codice(repo))
    RV.prenota(ris, id_, ipotesi, LETTURA, FINE, S.impronta(scheda), ORA)
    if con_git:
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-q", "-m", "base r19"], check=True)
        subprocess.run(g + ["push", "-q", "-u", "origin", "principale"], check=True, capture_output=True)
    return repo, reg, ris, scheda, g


def sezione_1_avvio_critici(cache: Path, cache_sv: Path):
    print("\n================ 1. SONDE CRITICHE SU avvio.py E esegui_verifica ================")
    with tempfile.TemporaryDirectory(prefix="r19_avvio_") as td:
        base = Path(td)
        repo, reg, ris, scheda, g = prepara_repo_copia(base, cache, cache_sv, anche_h002=True)
        rap = base / "rapporto_reale.txt"

        # 1A: Verifica se avvio.py è incluso in EV.impronte_codice()
        imp_ev = EV.impronte_codice(repo)
        imp_eh = EH.impronte_codice(repo)
        print(f"  [R19-01 check] avvio.py in EH.impronte_codice: {'brain/laboratorio/esecuzione/avvio.py' in imp_eh}")
        print(f"  [R19-01 check] avvio.py in EV.impronte_codice: {'brain/laboratorio/esecuzione/avvio.py' in imp_ev}")

        # 1B: Corsa REALE valida attraverso l'ingresso OBBLIGATORIO `python3 -I -S -B avvio.py verifica`!
        cmd = [
            sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
            "--scheda", str(scheda), "--registro", str(reg), "--riserva", str(ris),
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", ORA,
        ]
        r = subprocess.run(cmd, cwd=str(repo), env=NO_NET, capture_output=True, text=True, timeout=120)
        print(f"  [R19-01 END-TO-END VALIDO via avvio.py verifica] rc={r.returncode}")
        print(f"    stderr: {r.stderr.strip()}")
        print(f"    stdout: {r.stdout.strip()[:200]}")

        # 1C: Modifica di avvio.py dopo il sigillo H-003 (testa che S.controlla_sigillo non lo rileva!)
        avvio_f = repo / "brain/laboratorio/esecuzione/avvio.py"
        orig_avvio = avvio_f.read_text(encoding="utf-8")
        try:
            avvio_f.write_text(orig_avvio + "\n# MANOMISSIONE NON RILEVATA\n", encoding="utf-8")
            # S.controlla_sigillo senza codice esplicito e con EV.impronte_codice
            S.controlla_sigillo(reg, "H-R19", scheda, codice=EV.impronte_codice(repo), radice=repo)
            print("  [R19-01b MANOMISSIONE avvio.py] S.controlla_sigillo H-R19: SUPERATO SENZA ERRORE (NON RILEVATO!)")
        except Exception as e:
            print(f"  [R19-01b MANOMISSIONE avvio.py] RILEVATO: {e}")
        finally:
            avvio_f.write_text(orig_avvio, encoding="utf-8")

        # 1D: Sintassi --scheda=PATH (valida per argparse)
        cmd_eq = [
            sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
            f"--scheda={scheda}", "--registro", str(reg), "--riserva", str(ris),
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(rap), "--ora", ORA,
        ]
        r_eq = subprocess.run(cmd_eq, cwd=str(repo), env=NO_NET, capture_output=True, text=True, timeout=30)
        print(f"  [R19-02a --scheda=PATH] rc={r_eq.returncode} | stderr={r_eq.stderr.strip()}")

        # 1E: BYPASS PRE-IMPORT con DOPPIO --scheda (--scheda esca_H002 --scheda H-R19) + esegui_verifica.py MANOMESSO!
        esca = base / "esca_h002.md"
        esca.write_text(testo_scheda(contratto("H-002")), encoding="utf-8")
        ev_f = repo / "brain/laboratorio/esecuzione/esegui_verifica.py"
        orig_ev = ev_f.read_text(encoding="utf-8")
        marker = base / "pwned_preimport.txt"
        try:
            payload = f"\nimport pathlib as _pl; _pl.Path({str(marker)!r}).write_text('ESEGUITO_CODICE_NON_SIGILLATO')\n"
            ev_f.write_text(payload + orig_ev, encoding="utf-8")
            cmd_dup = [
                sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
                "--scheda", str(esca), "--scheda", str(scheda),
                "--registro", str(reg), "--riserva", str(ris),
                "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
                "--rapporto", str(rap), "--ora", ORA,
            ]
            r_dup = subprocess.run(cmd_dup, cwd=str(repo), env=NO_NET, capture_output=True, text=True, timeout=60)
            pwn = marker.exists()
            print(f"  [R19-02b BYPASS DOPPIO --scheda] rc={r_dup.returncode} | codice_manomesso_eseguito={pwn} | stderr={r_dup.stderr.strip()[:160]}")
        finally:
            ev_f.write_text(orig_ev, encoding="utf-8")


def sezione_2_regressioni_e_bug(cache: Path, cache_sv: Path):
    print("\n================ 2. REGRESSIONI E BUG IN esegui_verifica / manifesto / riserva ================")

    # 2A: Dati feriali INCOMPLETI / VUOTI ignorati da esegui_verifica (info mai controllato!)
    with tempfile.TemporaryDirectory(prefix="r19_incomp_") as td:
        base = Path(td)
        c_inc = base / "cache_inc"
        shutil.copytree(cache, c_inc)
        # Sovrascrive 20 giorni feriali della verifica con file vuoti b"" (e aggiorna il CSV con sha256 del vuoto ed esito="vuoto-200")
        giorni_sv = [g for g in EV.sedute(INIZIO, FINE)][:20]
        vuoto_sha = hashlib.sha256(b"").hexdigest()
        for lato, sub in (("BID", "XAUUSD"), ("ASK", "XAUUSD_ASK")):
            reg_csv = c_inc / f"registro_scaricamento_XAUUSD_{lato}.csv"
            righe = reg_csv.read_text(encoding="utf-8").splitlines()
            nuove = [righe[0]]
            target_set = {g.isoformat() for g in giorni_sv}
            for riga in righe[1:]:
                parti = riga.split(",")
                if parti[1] in target_set:
                    (c_inc / sub / f"{parti[1]}.bi5").write_bytes(b"")
                    parti[4] = "200"
                    parti[5] = "vuoto-200"
                    parti[6] = "0"
                    parti[7] = vuoto_sha
                nuove.append(",".join(parti))
            reg_csv.write_text("\n".join(nuove) + "\n", encoding="utf-8")

        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-INC.md"
        scheda.write_text(testo_scheda(contratto("H-INC")), encoding="utf-8")
        S.sigilla(reg, "H-INC", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-INC", LETTURA, FINE, S.impronta(scheda), ORA)
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            r = EV.esegui(scheda, reg, ris, "P1", c_inc, cache_sv, base / "rap.txt", ORA)
        rec = RV.record_esito(ris, "P1")
        print(
            f"  [R19-03 20 feriali vuoti in verifica] esito_tecnico={r['esito_tecnico']}, esito={r['esito']}, "
            f"trade={rec['verdetto']['trade']} (attesi 1000 senza buchi; 20 feriali vuoti passati silenziosamente come 0 trade!)"
        )

    # 2B: Ripresa dopo caduta tra RV.rendiconta (r.328) e _registra_una_volta('esito') (r.329)
    with tempfile.TemporaryDirectory(prefix="r19_ripresa_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-RIP.md"
        scheda.write_text(testo_scheda(contratto("H-RIP")), encoding="utf-8")
        S.sigilla(reg, "H-RIP", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-RIP", LETTURA, FINE, S.impronta(scheda), ORA)
        orig_reg = EV._registra_una_volta

        def cadi_su_esito(r_path, ip, voce, ora):
            if voce.get("ruolo") == "esito":
                raise RuntimeError("caduta simulata tra rendiconta e registrazione esito")
            return orig_reg(r_path, ip, voce, ora)

        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            with mock.patch.object(EV, "_registra_una_volta", side_effect=cadi_su_esito):
                try:
                    EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, base / "rap.txt", ORA)
                except RuntimeError:
                    pass
            # Ora ripresa normale!
            r2 = EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, base / "rap.txt", ORA)
        ruoli = [e["ruolo"] for e in S.leggi(reg)["esecuzioni"]]
        print(f"  [R19-05 caduta tra rendiconta e esito] ripresa={r2['esito_tecnico']}, ruoli_in_registro_prove={ruoli} (manca 'esito'!)")

    # 2C: Rami divergenti con stesso j=1:
    #   (i) alfa_tot=0.15, m=1 -> RV.quota(0.15, 2, 1) == 0.024999999999999998 != 0.025 (trappola float64 + bypass §3.4)
    #   (ii) alfa_tot=0.30, m=2 -> RV.quota(0.30, 2, 2) == 0.025 esatto -> SECONDA VERIFICA COMPLETA (promossa!)
    print(
        f"  [R19-04b float64 quota] RV.quota(0.15, 2, 1)={RV.quota(0.15, 2, 1)!r} "
        f"(==0.025? {RV.quota(0.15, 2, 1) == V.QUOTA}) | "
        f"RV.quota(0.75, 2, 5)={RV.quota(0.75, 2, 5)!r} (==0.025? {RV.quota(0.75, 2, 5) == V.QUOTA})"
    )
    for etichetta, alfa_t, m_val in (("alfa=0.15,m=1", 0.15, 1), ("alfa=0.75,m=5", 0.75, 5)):
        with tempfile.TemporaryDirectory(prefix="r19_rami_") as td:
            base = Path(td)
            repo, reg, ris, scheda, g = prepara_repo_copia(base, cache, cache_sv, ipotesi="H-R19", id_="P1", alfa_tot=alfa_t)
            if m_val != 1:
                c_m = contratto("H-R19")
                c_m["m"] = m_val
                scheda.write_text(testo_scheda(c_m), encoding="utf-8")
                reg.unlink()
                ris.unlink()
                S.sigilla(reg, "H-R19", scheda, ["V-T"], ORA, codice=EV.impronte_codice(repo))
                RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), alfa_t, ORA)
                RV.prenota(ris, "P1", "H-R19", LETTURA, FINE, S.impronta(scheda), ORA)
            scheda_alt = repo / "brain/laboratorio/ipotesi/H-ALT.md"
            c_alt = contratto("H-ALT")
            c_alt["m"] = m_val
            scheda_alt.write_text(testo_scheda(c_alt), encoding="utf-8")
            S.sigilla(reg, "H-ALT", scheda_alt, ["V-T"], ORA, codice=EV.impronte_codice(repo))
            RV.prenota(ris, "P_ALT", "H-ALT", B_INIZIO, B_FINE, S.impronta(scheda_alt), ORA)
            subprocess.run(g + ["add", "-A"], check=True)
            subprocess.run(g + ["commit", "-q", "-m", "due ipotesi"], check=True)
            subprocess.run(g + ["push", "-q", "origin", "principale"], check=True, capture_output=True)
            base_sha = subprocess.run(g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

            # Ramo principale: autorizza P1 (H-R19 V-T) e registra verifica in registro_prove.json (j=1)
            RV.autorizza(ris, "P1", 2, "a" * 64, ORA, m=m_val)
            S.registra_esecuzioni(reg, "H-R19", [{"ruolo": "verifica", "variante": "V-T", "prenotazione": "P1"}], ORA)
            subprocess.run(g + ["add", "-A"], check=True)
            subprocess.run(g + ["commit", "-q", "-m", "H-R19 verificata su principale"], check=True)
            subprocess.run(g + ["push", "-q", "origin", "principale"], check=True, capture_output=True)

            # Ramo divergente B da base_sha: autorizza P_ALT (j_attuale=1 == s.j di principale!), rilascia P1,
            # prenota P2 per H-R19 (stessa scheda, stessa variante V-T!)
            subprocess.run(g + ["checkout", "-q", "-b", "ramo_b", base_sha], check=True)
            RV.autorizza(ris, "P_ALT", 2, "b" * 64, ORA, m=m_val)
            RV.rilascia(ris, "P1", ORA)
            RV.prenota(ris, "P2", "H-R19", LETTURA, FINE, S.impronta(scheda), ORA)
            subprocess.run(g + ["add", "-A"], check=True)
            subprocess.run(g + ["commit", "-q", "-m", "ramo B con j=1 su H-ALT e P2 per H-R19"], check=True)
            subprocess.run(g + ["push", "-q", "-u", "origin", "ramo_b"], check=True, capture_output=True)

            with mock.patch.object(EV, "RADICE", repo), mock.patch.object(EV, "ANCORA_GIT", True), \
                    mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
                try:
                    r_dup_branch = EV.esegui(scheda, reg, ris, "P2", cache, cache_sv, base / "rap_b.txt", ORA)
                    print(
                        f"  [R19-04 RAMI DIVERGENTI {etichetta}] BYPASS §3.4! "
                        f"esito_tecnico={r_dup_branch['esito_tecnico']}, esito={r_dup_branch['esito']}, "
                        f"chiamate={r_dup_branch['chiamate_caricatore']}"
                    )
                except Exception as e:
                    print(f"  [R19-04 RAMI DIVERGENTI {etichetta}] RIFIUTATA: {type(e).__name__}: {e}")

    # 2D: Regressioni in esegui_verifica: veto_blocchi.soglia=NaN/-Inf, --ora invalida, --rapporto cartella, fuso, 2° controlla_ambiente
    with tempfile.TemporaryDirectory(prefix="r19_reg_") as td:
        base = Path(td)
        # 2D.1: veto_blocchi.soglia = -Infinity nel JSON
        s_inf = base / "H-INF.md"
        c_inf = contratto("H-INF")
        c_inf["veto_blocchi"]["soglia"] = float("-inf")
        s_inf.write_text(f"# H-INF\n```json contratto-h003\n{json.dumps(c_inf)}\n```\n", encoding="utf-8")
        try:
            parsed = EV.leggi_contratto(s_inf)
            print(f"  [R19-06d leggi_contratto soglia=-inf] ACCETTATO da leggi_contratto! soglia={parsed['veto_blocchi']['soglia']}")
        except Exception as e:
            print(f"  [R19-06d leggi_contratto soglia=-inf] RIFIUTATO: {e}")

        # Test completo con soglia=-inf: legge lo sviluppo e scrive nel registro prove prima di fallire!
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        S.sigilla(reg, "H-INF", s_inf, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-INF", LETTURA, FINE, S.impronta(s_inf), ORA)
        ch = []
        vero_c = C.carica
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(C, "carica", side_effect=lambda *a, **k: (ch.append(a[4]), vero_c(*a, **k))[1]):
            try:
                EV.esegui(s_inf, reg, ris, "P1", cache, cache_sv, base / "r.txt", ORA)
                print("  [R19-06d esegui soglia=-inf] COMPLETATA?!")
            except Exception as e:
                print(
                    f"  [R19-06d esegui soglia=-inf] fallita tardi ({type(e).__name__}: {e}) | "
                    f"chiamate={ch} | esecuzioni_scritte={len(S.leggi(reg)['esecuzioni'])}"
                )

        # 2D.2: ipotesi="" in leggi_contratto
        s_vuota = base / "H-VUOTA.md"
        s_vuota.write_text(testo_scheda(contratto("")), encoding="utf-8")
        try:
            EV.leggi_contratto(s_vuota)
            print("  [R19-06e leggi_contratto ipotesi=''] ACCETTATO da leggi_contratto!")
        except Exception as e:
            print(f"  [R19-06e leggi_contratto ipotesi=''] RIFIUTATO: {e}")

        # 2D.3: --ora invalida + --rapporto cartella esistente
        reg2 = base / "reg2.json"
        ris2 = base / "ris2.json"
        RV.crea(ris2, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_ok = base / "H-OK.md"
        s_ok.write_text(testo_scheda(contratto("H-OK")), encoding="utf-8")
        S.sigilla(reg2, "H-OK", s_ok, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris2, "P1", "H-OK", LETTURA, FINE, S.impronta(s_ok), ORA)
        rap_dir = base / "rapporto_e_cartella"
        rap_dir.mkdir()
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            try:
                EV.esegui(s_ok, reg2, ris2, "P1", cache, cache_sv, rap_dir, "NON-UNA-DATA")
            except Exception as e:
                st = RV.stato(ris2)
                print(
                    f"  [R19-06c+R19-08 --ora invalida + --rapporto cartella] "
                    f"eccezione={type(e).__name__}: {e} | "
                    f"riserva_consumata={st['giorni']['consumato']} | ora_scritta={st['aperture'][0]['ora']!r}"
                )

        # 2D.4: controlla_fuso assente in esegui_verifica
        txt_ev = (ROOT / "brain/laboratorio/esecuzione/esegui_verifica.py").read_text(encoding="utf-8")
        print(f"  [R19-06a controlla_fuso in esegui_verifica.py] presente={'controlla_fuso' in txt_ev}")
        print(f"  [R19-06b chiamate controlla_ambiente in esegui_verifica.py] count={txt_ev.count('controlla_ambiente(')}")

    # 2E: Manifesto: sha256="" su riga "dati" (brucia riserva!) + URL con data sbagliata
    with tempfile.TemporaryDirectory(prefix="r19_man_") as td:
        base = Path(td)
        c_man = base / "cache_man"
        shutil.copytree(cache, c_man)
        reg_csv = c_man / "registro_scaricamento_XAUUSD_BID.csv"
        righe = reg_csv.read_text(encoding="utf-8").splitlines()
        # 2E.1: URL con data di un altro anno (2019/05/05) sul giorno INIZIO
        nuove_url = [righe[0]]
        for riga in righe[1:]:
            p = riga.split(",")
            if p[1] == INIZIO.isoformat():
                p[3] = "https://evil.invalid/XAUUSD/2019/05/05/BID_candles_min_1.bi5"
            nuove_url.append(",".join(p))
        reg_csv.write_text("\n".join(nuove_url) + "\n", encoding="utf-8")
        m_url = MF.manifesto(c_man, "XAUUSD", LETTURA, FINE)
        print(f"  [R19-07a manifesto URL data/dominio falsi] anomalie={m_url['anomalie']}")

        # 2E.2: sha256="" su riga esito="dati" → passa manifesto, autorizza e brucia riserva!
        nuove_sha = [righe[0]]
        for riga in righe[1:]:
            p = riga.split(",")
            if p[1] == INIZIO.isoformat():
                p[7] = ""
            nuove_sha.append(",".join(p))
        reg_csv.write_text("\n".join(nuove_sha) + "\n", encoding="utf-8")
        m_sha = MF.manifesto(c_man, "XAUUSD", LETTURA, FINE)
        reg3 = base / "reg3.json"
        ris3 = base / "ris3.json"
        RV.crea(ris3, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_sha = base / "H-SHA.md"
        s_sha.write_text(testo_scheda(contratto("H-SHA")), encoding="utf-8")
        S.sigilla(reg3, "H-SHA", s_sha, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris3, "P1", "H-SHA", LETTURA, FINE, S.impronta(s_sha), ORA)
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            r_sha = EV.esegui(s_sha, reg3, ris3, "P1", c_man, cache_sv, base / "r.txt", ORA)
        st3 = RV.stato(ris3)
        print(
            f"  [R19-07b manifesto sha256='' su dati] anomalie_manifesto={m_sha['anomalie']} | "
            f"esito_tecnico={r_sha['esito_tecnico']} | riserva_bruciata_giorni={st3['giorni']['consumato']}"
        )


def sezione_3_concorrenza_reale(cache: Path, cache_sv: Path):
    print("\n================ 3. CONCORRENZA REALE MULTI-PROCESSO (2 Popen) ================")
    with tempfile.TemporaryDirectory(prefix="r19_conc_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_a = base / "H-CA.md"
        s_b = base / "H-CB.md"
        s_a.write_text(testo_scheda(contratto("H-CA")), encoding="utf-8")
        s_b.write_text(testo_scheda(contratto("H-CB")), encoding="utf-8")
        S.sigilla(reg, "H-CA", s_a, ["V-T"], ORA, codice=EV.impronte_codice())
        S.sigilla(reg, "H-CB", s_b, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "PA", "H-CA", LETTURA, FINE, S.impronta(s_a), ORA)
        RV.prenota(ris, "PB", "H-CB", B_INIZIO, B_FINE, S.impronta(s_b), ORA)

        runner = "\n".join([
            "import json, sys",
            "from pathlib import Path",
            "from unittest import mock",
            f"sys.path.insert(0, {str(ROOT)!r})",
            "from brain.laboratorio.esecuzione import esegui_verifica as EV",
            "a = sys.argv[1:]",
            "with mock.patch.object(EV, 'ANCORA_GIT', False), mock.patch.object(EV, 'CONTROLLO_AMBIENTE', False):",
            "    r = EV.esegui(Path(a[0]), Path(a[1]), Path(a[2]), a[3], Path(a[4]), Path(a[5]), Path(a[6]), a[7])",
            "print(json.dumps(r))",
        ])
        p1 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner, str(s_a), str(reg), str(ris), "PA",
             str(cache), str(cache_sv), str(base / "ra.txt"), ORA],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        p2 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner, str(s_b), str(reg), str(ris), "PB",
             str(cache), str(cache_sv), str(base / "rb.txt"), ORA],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        out1, err1 = p1.communicate(timeout=180)
        out2, err2 = p2.communicate(timeout=180)
        st = RV.stato(ris)
        print(
            f"  [CONC-1 due prenotazioni PA/PB parallele] rc=({p1.returncode},{p2.returncode}) | "
            f"aperture={[(x['id'], x['j'], x['esito']) for x in st['aperture']]} | "
            f"rifiuti={[(x['id'], x['j_previsto'], x['fase']) for x in st['rifiuti']]}"
        )
        if err1.strip() or err2.strip():
            print(f"    err1={err1.strip()[:120]} | err2={err2.strip()[:120]}")

        # CONC-2: Due processi concorrenti sulla STESSA prenotazione P1!
        reg2 = base / "reg2.json"
        ris2 = base / "ris2.json"
        RV.crea(ris2, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        S.sigilla(reg2, "H-CA", s_a, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris2, "P1", "H-CA", LETTURA, FINE, S.impronta(s_a), ORA)
        q1 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner, str(s_a), str(reg2), str(ris2), "P1",
             str(cache), str(cache_sv), str(base / "r1.txt"), ORA],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        q2 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner, str(s_a), str(reg2), str(ris2), "P1",
             str(cache), str(cache_sv), str(base / "r2.txt"), ORA],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        o1, e1 = q1.communicate(timeout=180)
        o2, e2 = q2.communicate(timeout=180)
        st2 = RV.stato(ris2)
        print(
            f"  [CONC-2 stessa prenotazione P1 parallela] rc=({q1.returncode},{q2.returncode}) | "
            f"aperture={[(x['id'], x['j'], x['esito']) for x in st2['aperture']]} | "
            f"esecuzioni_prove={len(S.leggi(reg2)['esecuzioni'])} | "
            f"err_secondo={(e1.strip() or e2.strip()).splitlines()[-1] if (e1.strip() or e2.strip()) else 'nessuno'}"
        )

        # CONC-3: Barriera sincronizzata proprio prima di RV.autorizza (entrambi superano passo 5 con j=1, q=0.025)
        reg3 = base / "reg3.json"
        ris3 = base / "ris3.json"
        RV.crea(ris3, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        S.sigilla(reg3, "H-CA", s_a, ["V-T"], ORA, codice=EV.impronte_codice())
        S.sigilla(reg3, "H-CB", s_b, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris3, "PA", "H-CA", LETTURA, FINE, S.impronta(s_a), ORA)
        RV.prenota(ris3, "PB", "H-CB", B_INIZIO, B_FINE, S.impronta(s_b), ORA)
        barriera = base / "barriera"
        barriera.mkdir()
        runner_bar = "\n".join([
            "import json, sys, time",
            "from pathlib import Path",
            "from unittest import mock",
            f"sys.path.insert(0, {str(ROOT)!r})",
            "from brain.laboratorio.esecuzione import esegui_verifica as EV, riserva as RV",
            "a = sys.argv[1:]",
            "bar = Path(a[8]); orig_aut = RV.autorizza",
            "def aut_bar(*args, **kwargs):",
            "    (bar / a[3]).write_text('ok')",
            "    t0 = time.time()",
            "    while len(list(bar.iterdir())) < 2 and time.time() - t0 < 20:",
            "        time.sleep(0.02)",
            "    return orig_aut(*args, **kwargs)",
            "with mock.patch.object(EV, 'ANCORA_GIT', False), mock.patch.object(EV, 'CONTROLLO_AMBIENTE', False), \\",
            "        mock.patch.object(RV, 'autorizza', side_effect=aut_bar):",
            "    r = EV.esegui(Path(a[0]), Path(a[1]), Path(a[2]), a[3], Path(a[4]), Path(a[5]), Path(a[6]), a[7])",
            "print(json.dumps(r))",
        ])
        b1 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner_bar, str(s_a), str(reg3), str(ris3), "PA",
             str(cache), str(cache_sv), str(base / "ba.txt"), ORA, str(barriera)],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        b2 = subprocess.Popen(
            [sys.executable, "-s", "-B", "-c", runner_bar, str(s_b), str(reg3), str(ris3), "PB",
             str(cache), str(cache_sv), str(base / "bb.txt"), ORA, str(barriera)],
            env=NO_NET, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        bo1, be1 = b1.communicate(timeout=180)
        bo2, be2 = b2.communicate(timeout=180)
        st3 = RV.stato(ris3)
        print(
            f"  [CONC-3 barriera su RV.autorizza (DGS-15 p.4)] rc=({b1.returncode},{b2.returncode}) | "
            f"aperture={[(x['id'], x['j'], x['esito']) for x in st3['aperture']]} | "
            f"rifiuti={[(x['id'], x['j_previsto'], x['fase']) for x in st3['rifiuti']]}"
        )
        if be1.strip() or be2.strip():
            print(f"    be1={be1.strip()[:120]} | be2={be2.strip()[:120]}")


def sezione_4_verdetto_124():
    print("\n================ 4. RIESECUZIONE SONDE #124 (D1..D6) SU verdetto_d31.py (1431190) ================")
    xs_d1 = [0.25] * 299 + [0.25 + math.ldexp(1.0, -48)]
    with mock.patch.object(V.P, "intervallo_bootstrap", return_value=(0.1, 0.4)):
        s_d1 = V.screening([(x, 1) for x in xs_d1], 9, 0.9)
    print(f"  [D1 screening 75+2^-48] ammessa={s_d1['ammessa']} (atteso True) | cause={s_d1['cause']}")

    xs_d2 = [-0.25] * 249 + [-0.25 - math.ldexp(1.0, -49)]
    vb_d2 = V.veto_blocchi([(x, 1) for x in xs_d2], soglia=-0.25, minimo_trade_blocco=50, ampiezza=250)
    print(f"  [D2 veto_blocchi -62.5-2^-49] esito={vb_d2['esito']} (atteso fallito)")

    vb_d3 = V.veto_blocchi([(-0.4, 1)] * 3, soglia=-0.4, minimo_trade_blocco=1, ampiezza=3)
    print(f"  [D3 veto_blocchi serie costante k=3 x=-0.4] esito={vb_d3['esito']} (atteso superato)")

    for nome, cp in (
        ("D6a perm1", [(1.5e308, 1), (-1.5e308, 1), (1.5e308, 1)]),
        ("D6b perm2", [(1.5e308, 1), (1.5e308, 1), (-1.5e308, 1)]),
    ):
        try:
            V.controlla_coppie(cp)
            es = "ACCETTATO"
        except Exception as e:
            es = f"{type(e).__name__}: {e}"
        print(f"  [{nome}] {es}")


def sezione_5_matrice_d51(cache: Path, cache_sv: Path):
    print("\n================ 5. MATRICE PROTEZIONI D-51 (PIANO-D51 §1, §2, §3.1-§3.5) ================")

    def riga(cod, nome, esito, fase, chiamate, stato_p, stato_d, nota=""):
        print(
            f"  [{cod}] {nome}\n"
            f"        esito={esito} | fase={fase} | caricatore={chiamate}\n"
            f"        prima: {stato_p}\n"
            f"        dopo : {stato_d}" + (f"\n        nota : {nota}" if nota else "")
        )

    # D51-01 (§1): esegui_h002 --modalita verifica disattivato
    with tempfile.TemporaryDirectory(prefix="d51_01_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        reg.write_text(json.dumps({"schema": S.SCHEMA, "prove": [], "sigilli": [], "esecuzioni": []}), encoding="utf-8")
        rap = base / "rap.md"
        sp = stato_breve(reg, base / "none.json")
        ch = []
        err = io.StringIO()
        with mock.patch.object(C, "carica", side_effect=lambda *a, **k: ch.append(a[4])), \
                contextlib.redirect_stderr(err):
            rc = EH.main(["--modalita", "verifica", "--rapporto", str(rap), "--registro", str(reg)])
        sd = stato_breve(reg, base / "none.json")
        riga("D51-01", "esegui_h002 --modalita verifica (D-51 §1)", f"rc={rc} ({err.getvalue().strip()[:90]})",
             "prima di sigillo/registri/caricatore", ch, sp, sd, f"rapporto_creato={rap.exists()}")

    # D51-02..D51-06 (§3.1): ancora git, registri canonici, storia completa, prenotazione consumata altrove, j e N
    with tempfile.TemporaryDirectory(prefix="d51_git_") as td:
        base = Path(td)
        repo, reg, ris, scheda, g = prepara_repo_copia(base, cache, cache_sv)
        rap = base / "rap.txt"
        ch = []
        vero_c = C.carica

        def conta(*a, **k):
            ch.append(a[4])
            return vero_c(*a, **k)

        # Caso valido (con CONTROLLO_AMBIENTE=False per isolare §3.1 — nota che con True cade per R19-01!)
        with mock.patch.object(EV, "RADICE", repo), mock.patch.object(EV, "ANCORA_GIT", True), \
                mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), mock.patch.object(C, "carica", side_effect=conta):
            # 1) Riserva non canonica
            altro = repo / "riserva_finta.json"
            altro.write_bytes(ris.read_bytes())
            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(scheda, reg, altro, "P1", cache, cache_sv, rap, ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-02a", "riserva non canonica (§3.1)", es, "passo 2 (_ancora)", list(ch), sp, stato_breve(reg, ris))

            # 2) Registro riserva con modifica non committata
            RV.quarantena(ris, date(2005, 1, 3), date(2005, 1, 3), "locale", ORA)
            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, rap, ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-02b", "riserva non committata (§3.1)", es, "passo 2 (_ancora)", list(ch), sp, stato_breve(reg, ris))
            subprocess.run(g + ["checkout", "--", EV.REL_RISERVA], check=True)

            # 3) Copia git parziale (extensions.partialclone / promisor)
            subprocess.run(g + ["config", "remote.origin.promisor", "true"], check=True)
            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, rap, ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-03", "copia git parziale --filter (#125, §3.1)", es, "passo 2 (versioni_nella_storia)", list(ch), sp, stato_breve(reg, ris))
            subprocess.run(g + ["config", "--unset", "remote.origin.promisor"], check=True)

            # 4) Prenotazione consumata in un altro ramo + reflog
            base_c = subprocess.run(g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            RV.autorizza(ris, "P1", 1, "c" * 64, ORA)
            subprocess.run(g + ["add", "-A"], check=True)
            subprocess.run(g + ["commit", "-q", "-m", "cons P1"], check=True)
            subprocess.run(g + ["push", "-q", "origin", "principale"], check=True, capture_output=True)
            subprocess.run(g + ["checkout", "-q", "-b", "alt", base_c], check=True)
            subprocess.run(g + ["push", "-q", "-u", "origin", "alt"], check=True, capture_output=True)
            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, rap, ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-04", "prenotazione consumata su altro ramo (§3.1)", es, "passo 2 (_gia_consumata)", list(ch), sp, stato_breve(reg, ris))

    # D51-07..08 (§3.2): sviluppo con byte difformi + screening registrato con altra impronta sviluppo
    with tempfile.TemporaryDirectory(prefix="d51_sv_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        scheda = base / "H-SV.md"
        scheda.write_text(testo_scheda(contratto("H-SV")), encoding="utf-8")
        S.sigilla(reg, "H-SV", scheda, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-SV", LETTURA, FINE, S.impronta(scheda), ORA)
        c_sv_mod = base / "csv_mod"
        shutil.copytree(cache_sv, c_sv_mod)
        f_mod = c_sv_mod / "XAUUSD" / "2024-03-05.bi5"
        f_mod.write_bytes(f_mod.read_bytes() + b"\x00")
        ch = []
        vero_c = C.carica
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(C, "carica", side_effect=lambda *a, **k: (ch.append(a[4]), vero_c(*a, **k))[1]):
            sp = stato_breve(reg, ris)
            try:
                EV.esegui(scheda, reg, ris, "P1", cache, c_sv_mod, base / "r.txt", ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-05a", "sviluppo con byte modificati (§3.2)", es, "passo 6 (caricatore sviluppo)", list(ch), sp, stato_breve(reg, ris))

            S.registra_esecuzioni(reg, "H-SV", [{"ruolo": "sviluppo", "variante": "V-T", "impronta_sviluppo": "0" * 64}], ORA)
            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(scheda, reg, ris, "P1", cache, cache_sv, base / "r.txt", ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-05b", "screening registrato con altro sviluppo (§3.2)", es, "passo 6 (_registra_una_volta)", list(ch), sp, stato_breve(reg, ris))

    # D51-06 (§3.4): seconda verifica stessa variante + due ipotesi nello stesso registro + esito senza verifica/duplicato
    with tempfile.TemporaryDirectory(prefix="d51_reg_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s1 = base / "H-1.md"
        s2 = base / "H-2.md"
        s1.write_text(testo_scheda(contratto("H-1")), encoding="utf-8")
        s2.write_text(testo_scheda(contratto("H-2")), encoding="utf-8")
        S.sigilla(reg, "H-1", s1, ["V-T"], ORA, codice=EV.impronte_codice())
        S.sigilla(reg, "H-2", s2, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-1", LETTURA, FINE, S.impronta(s1), ORA)
        RV.prenota(ris, "P2", "H-1", B_INIZIO, B_FINE, S.impronta(s1), ORA)
        ch = []
        vero_c = C.carica
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(C, "carica", side_effect=lambda *a, **k: (ch.append(a[4]), vero_c(*a, **k))[1]):
            sp0 = stato_breve(reg, ris)
            r1 = EV.esegui(s1, reg, ris, "P1", cache, cache_sv, base / "r1.txt", ORA)
            riga("D51-06v", "CASO VALIDO base (H-1 P1, senza avvio.py)", f"{r1['esito_tecnico']} / {r1['esito']}",
                 "completo", list(ch), sp0, stato_breve(reg, ris))

            sp = stato_breve(reg, ris)
            ch.clear()
            try:
                EV.esegui(s1, reg, ris, "P2", cache, cache_sv, base / "r2.txt", ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
            riga("D51-06a", "seconda verifica stessa ipotesi/variante (§3.4)", es, "passo 3 (altre)", list(ch), sp, stato_breve(reg, ris))

            # Due ipotesi diverse nello stesso registro: H-2 non è bloccata da H-1 (arriva al controllo quota j=2 -> rifiuto)
            RV.rilascia(ris, "P2", ORA)
            RV.prenota(ris, "P3", "H-2", B_INIZIO, B_FINE, S.impronta(s2), ORA)
            sp = stato_breve(reg, ris)
            ch.clear()
            r3 = EV.esegui(s2, reg, ris, "P3", cache, cache_sv, base / "r3.txt", ORA)
            riga("D51-06b", "seconda ipotesi H-2 nello stesso registro (§3.4)", f"{r3['esito_tecnico']} ({r3['motivo']})",
                 "passo 5 (quota j=2, NON bloccata da H-1)", list(ch), sp, stato_breve(reg, ris))

    # D51-07 (§3.5): separazione sviluppo/riserva — prenotazione su date di sviluppo rifiutata
    with tempfile.TemporaryDirectory(prefix="d51_sep_") as td:
        base = Path(td)
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), C.FINE_VERIFICA, 0.05, ORA)
        sp = stato_breve(base / "none.json", ris)
        try:
            RV.prenota(ris, "PSV", "H-SV", date(2023, 11, 15), date(2024, 1, 31), "0" * 64, ORA)
            es = "NON RIFIUTATO"
        except Exception as e:
            es = f"{type(e).__name__}: {e}"
        riga("D51-07", "prenotazione su date di sviluppo (§3.5)", es, "RV.prenota (_intervallo)", [], sp, stato_breve(base / "none.json", ris))

    # D51-07b (§3.5): contratto con sviluppo che invade date di verifica (caricatore rifiuta)
    with tempfile.TemporaryDirectory(prefix="d51_sep2_") as td:
        base = Path(td)
        reg = base / "registro_prove.json"
        ris = base / "riserva.json"
        RV.crea(ris, date(2005, 1, 1), C.FINE_VERIFICA, 0.05, ORA)
        c_bad_sv = contratto("H-SEP")
        c_bad_sv["sviluppo"] = ["2023-10-01", "2023-10-31"]
        s_bad = base / "H-SEP.md"
        s_bad.write_text(testo_scheda(c_bad_sv), encoding="utf-8")
        S.sigilla(reg, "H-SEP", s_bad, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris, "P1", "H-SEP", LETTURA, FINE, S.impronta(s_bad), ORA)
        c_sv_overlap = base / "csv_ov"
        M.scrivi(c_sv_overlap, date(2023, 10, 1), date(2023, 10, 31), 0.6, 15)
        ch = []
        vero_c = C.carica
        sp = stato_breve(reg, ris)
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(C, "carica", side_effect=lambda *a, **k: (ch.append(a[4]), vero_c(*a, **k))[1]):
            try:
                EV.esegui(s_bad, reg, ris, "P1", cache, c_sv_overlap, base / "r.txt", ORA)
                es = "NON RIFIUTATO"
            except Exception as e:
                es = f"{type(e).__name__}: {e}"
        riga("D51-07b", "sviluppo su date protette della riserva (§3.5)", es, "passo 1 (leggi_contratto)", ch, sp, stato_breve(reg, ris))

    # D51-03b (§3.3): esegui_verifica.main diretto senza avvio.py (CONTROLLO_AMBIENTE=True)
    with tempfile.TemporaryDirectory(prefix="d51_dir_") as td:
        base = Path(td)
        cmd_dir = [
            sys.executable, "-I", "-S", "-B", "-m", "brain.laboratorio.esecuzione.esegui_verifica",
            "--scheda", str(base / "s.md"), "--registro", str(base / "r.json"), "--riserva", str(base / "ris.json"),
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(base / "rap.txt"), "--ora", ORA,
        ]
        # Nota: -I toglie cwd da sys.path, quindi testiamo via main() con sys._tb_avvio_controllato assente
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = EV.main([
                "--scheda", str(base / "s.md"), "--registro", str(base / "r.json"), "--riserva", str(base / "ris.json"),
                "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
                "--rapporto", str(base / "rap.txt"), "--ora", ORA,
            ])
        riga("D51-08", "esegui_verifica.main senza avvio.py (§3.3)", f"rc={rc} ({err.getvalue().strip()[:90]})",
             "main() prima di esegui()", [], "n/d", "n/d")


def sezione_6_manomissioni_complete(cache: Path, cache_sv: Path):
    print("\n================ 6. MATRICE COMPLETA MANOMISSIONI (COMPITO C) ================")

    def check_err(label, fn):
        try:
            res = fn()
            print(f"  [NON RILEVATO!] {label} -> {res!r}")
        except Exception as e:
            print(f"  [RILEVATO]      {label} -> {type(e).__name__}: {str(e)[:110]}")

    # 6.1 Registro della riserva (riserva/2)
    with tempfile.TemporaryDirectory(prefix="r19_m_ris_") as td:
        base = Path(td)
        ris_base = base / "ris_base.json"
        RV.crea(ris_base, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA, protetta=(date(2005, 1, 1), date(2006, 12, 31)))
        RV.prenota(ris_base, "P1", "H-1", LETTURA, FINE, "a" * 64, ORA)

        def clona_e_modifica(nome, mutatore):
            p = base / f"{nome}.json"
            dati = json.loads(ris_base.read_text(encoding="utf-8"))
            mutatore(dati)
            p.write_text(json.dumps(dati), encoding="utf-8")
            return p

        # schema riserva/1
        p_s1 = clona_e_modifica("s1", lambda d: d.__setitem__("schema", "riserva/1"))
        check_err("riserva: schema riserva/1", lambda: RV.stato(p_s1))

        # j=True (bool)
        p_jb = clona_e_modifica("jb", lambda d: d["eventi"].append({
            "tipo": "autorizzazione", "id": "P1", "j": True, "n_globale": 1, "hash_dati": "b" * 64,
            "m": 1, "alfa_j": 0.025, "ora": ORA,
        }))
        check_err("riserva: j=True (bool)", lambda: RV.stato(p_jb))

        # j saltato (j=2 invece di 1)
        p_j2 = clona_e_modifica("j2", lambda d: d["eventi"].append({
            "tipo": "autorizzazione", "id": "P1", "j": 2, "n_globale": 1, "hash_dati": "b" * 64,
            "m": 1, "alfa_j": RV.quota(0.05, 2, 1), "ora": ORA,
        }))
        check_err("riserva: j saltato (2 invece di 1)", lambda: RV.stato(p_j2))

        # alfa_j falsificata
        p_af = clona_e_modifica("af", lambda d: d["eventi"].append({
            "tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 1, "hash_dati": "b" * 64,
            "m": 1, "alfa_j": 0.03, "ora": ORA,
        }))
        check_err("riserva: alfa_j alterata (0.03)", lambda: RV.stato(p_af))

        # alfa_j NaN
        p_an = clona_e_modifica("an", lambda d: d["eventi"].append({
            "tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 1, "hash_dati": "b" * 64,
            "m": 1, "alfa_j": float("nan"), "ora": ORA,
        }))
        check_err("riserva: alfa_j NaN", lambda: RV.stato(p_an))

        # impegno manomesso rispetto a hash_dati
        p_imp = clona_e_modifica("imp", lambda d: d["eventi"].append({
            "tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 1, "hash_dati": "b" * 64,
            "m": 1, "alfa_j": 0.025, "impegno": {"finto": 1}, "ora": ORA,
        }))
        check_err("riserva: impegno != hash_dati", lambda: RV.stato(p_imp))

        # rifiuto con j_previsto falsificato
        p_rj = clona_e_modifica("rj", lambda d: d["eventi"].append({
            "tipo": "rifiuto", "id": "P1", "j_previsto": 2, "m": 1,
            "quota_calcolata": 0.025, "quota_collaudata": 0.025, "motivo": "x", "fase": "y",
            "impronta_scheda": "a" * 64, "ora": ORA,
        }))
        check_err("riserva: rifiuto j_previsto falsificato", lambda: RV.stato(p_rj))

        # rifiuto con motivo vuoto
        p_rm = clona_e_modifica("rm", lambda d: d["eventi"].append({
            "tipo": "rifiuto", "id": "P1", "j_previsto": 1, "m": 1,
            "quota_calcolata": 0.025, "quota_collaudata": 0.025, "motivo": "", "fase": "y",
            "impronta_scheda": "a" * 64, "ora": ORA,
        }))
        check_err("riserva: rifiuto motivo vuoto", lambda: RV.stato(p_rm))

        # autorizzazione dopo rifiuto
        p_ar = clona_e_modifica("ar", lambda d: d["eventi"].extend([
            {"tipo": "rifiuto", "id": "P1", "j_previsto": 1, "m": 1,
             "quota_calcolata": 0.025, "quota_collaudata": 0.025, "motivo": "q", "fase": "f",
             "impronta_scheda": "a" * 64, "ora": ORA},
            {"tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 1, "hash_dati": "b" * 64,
             "m": 1, "alfa_j": 0.025, "ora": ORA},
        ]))
        check_err("riserva: autorizzazione dopo rifiuto", lambda: RV.stato(p_ar))

        # record incoerente con esito
        p_rec = clona_e_modifica("rec", lambda d: d["eventi"].extend([
            {"tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 1, "hash_dati": "b" * 64,
             "m": 1, "alfa_j": 0.025, "ora": ORA},
            {"tipo": "esito", "id": "P1", "esito": "promossa", "record": {"esito": "bocciata"}, "ora": ORA},
        ]))
        check_err("riserva: record.esito != esito", lambda: RV.stato(p_rec))

        # parte protetta senza sblocco (prenotazione e quarantena)
        check_err("riserva: prenota parte protetta senza usa_protetta",
                  lambda: RV.prenota(ris_base, "PP", "H-P", date(2005, 6, 1), date(2005, 6, 30), "a" * 64, ORA))
        check_err("riserva: quarantena parte protetta senza usa_protetta",
                  lambda: RV.quarantena(ris_base, date(2005, 6, 1), date(2005, 6, 30), "test", ORA))

        # N globale decrescente fra autorizzazioni
        p_nd = clona_e_modifica("nd", lambda d: d["eventi"].extend([
            {"tipo": "autorizzazione", "id": "P1", "j": 1, "n_globale": 5, "hash_dati": "b" * 64,
             "m": 1, "alfa_j": 0.025, "ora": ORA},
            {"tipo": "prenotazione", "id": "P2", "ipotesi": "H-2", "inizio": B_INIZIO.isoformat(),
             "fine": B_FINE.isoformat(), "hash_domanda": "a" * 64, "usa_protetta": False, "ora": ORA},
            {"tipo": "autorizzazione", "id": "P2", "j": 2, "n_globale": 4, "hash_dati": "c" * 64,
             "m": 1, "alfa_j": RV.quota(0.05, 2, 1), "ora": ORA},
        ]))
        check_err("riserva: N globale decrescente (5 -> 4)", lambda: RV.stato(p_nd))

    # 6.2 Manifesto e caricatore
    with tempfile.TemporaryDirectory(prefix="r19_m_man_") as td:
        base = Path(td)

        def clona_cache(nome):
            d = base / nome
            shutil.copytree(cache, d)
            return d

        # giorno omesso dal CSV
        c1 = clona_cache("c1")
        csv1 = c1 / "registro_scaricamento_XAUUSD_BID.csv"
        righe = csv1.read_text(encoding="utf-8").splitlines()
        csv1.write_text("\n".join([r for r in righe if f",{INIZIO.isoformat()}," not in r]) + "\n", encoding="utf-8")
        an1 = MF.manifesto(c1, "XAUUSD", LETTURA, FINE)["anomalie"]
        print(f"  [{'RILEVATO' if an1 else 'NON RILEVATO!'}]      manifesto: giorno feriale omesso -> {an1[:1]}")

        # riga duplicata nel CSV
        c2 = clona_cache("c2")
        csv2 = c2 / "registro_scaricamento_XAUUSD_BID.csv"
        r2 = csv2.read_text(encoding="utf-8").splitlines()
        csv2.write_text("\n".join(r2 + [r2[1]]) + "\n", encoding="utf-8")
        an2 = MF.manifesto(c2, "XAUUSD", LETTURA, FINE)["anomalie"]
        print(f"  [{'RILEVATO' if an2 else 'NON RILEVATO!'}]      manifesto: riga duplicata -> {an2[:1]}")

        # lato sbagliato / esito http-403 / file extra
        c3 = clona_cache("c3")
        csv3 = c3 / "registro_scaricamento_XAUUSD_BID.csv"
        r3 = csv3.read_text(encoding="utf-8").splitlines()
        p = r3[1].split(",")
        p[2] = "ASK"
        r3[1] = ",".join(p)
        csv3.write_text("\n".join(r3) + "\n", encoding="utf-8")
        an3 = MF.manifesto(c3, "XAUUSD", LETTURA, FINE)["anomalie"]
        print(f"  [{'RILEVATO' if an3 else 'NON RILEVATO!'}]      manifesto: lato sbagliato -> {an3[:1]}")

        c4 = clona_cache("c4")
        csv4 = c4 / "registro_scaricamento_XAUUSD_BID.csv"
        r4 = csv4.read_text(encoding="utf-8").splitlines()
        p4 = r4[1].split(",")
        p4[5] = "http-403"
        r4[1] = ",".join(p4)
        csv4.write_text("\n".join(r4) + "\n", encoding="utf-8")
        an4 = MF.manifesto(c4, "XAUUSD", LETTURA, FINE)["anomalie"]
        print(f"  [{'RILEVATO' if an4 else 'NON RILEVATO!'}]      manifesto: esito http-403 -> {an4[:1]}")

        c5 = clona_cache("c5")
        (c5 / "XAUUSD" / "2020-01-01.bi5").write_bytes(b"extra")
        an5 = MF.manifesto(c5, "XAUUSD", LETTURA, FINE)["anomalie"]
        print(f"  [{'RILEVATO' if an5 else 'NON RILEVATO!'}]      manifesto: file extra non nel registro -> {an5[:1]}")

        # symlink su CSV e su .bi5 e ASK == BID
        c6 = clona_cache("c6")
        csv6 = c6 / "registro_scaricamento_XAUUSD_BID.csv"
        real_csv = base / "real_bid.csv"
        shutil.move(str(csv6), str(real_csv))
        os.symlink(real_csv, csv6)
        check_err("manifesto: symlink su CSV", lambda: MF.manifesto(c6, "XAUUSD", LETTURA, FINE))

        c7 = clona_cache("c7")
        bi5 = c7 / "XAUUSD" / f"{INIZIO.isoformat()}.bi5"
        real_b = base / "real.bi5"
        shutil.move(str(bi5), str(real_b))
        os.symlink(real_b, bi5)
        reg7 = base / "reg7.json"
        s7 = base / "H-7.md"
        s7.write_text(testo_scheda(contratto("H-7")), encoding="utf-8")
        S.sigilla(reg7, "H-7", s7, ["V-T"], ORA, codice=EV.impronte_codice())
        check_err("caricatore: symlink su file .bi5",
                  lambda: C.carica(c7 / "XAUUSD", c7 / "XAUUSD_ASK", LETTURA, FINE, "verifica", reg7, "H-7", s7))

        check_err("caricatore: ASK == BID (#126)",
                  lambda: C.carica(cache / "XAUUSD", cache / "XAUUSD", LETTURA, FINE, "verifica", reg7, "H-7", s7))

        # File sostituito DOPO autorizzazione -> non decidibile + riserva consumata
        c8 = clona_cache("c8")
        reg8 = base / "reg8.json"
        ris8 = base / "ris8.json"
        RV.crea(ris8, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s8 = base / "H-8.md"
        s8.write_text(testo_scheda(contratto("H-8")), encoding="utf-8")
        S.sigilla(reg8, "H-8", s8, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris8, "P1", "H-8", LETTURA, FINE, S.impronta(s8), ORA)
        orig_aut = RV.autorizza

        def manometti_dopo_aut(*a, **k):
            res = orig_aut(*a, **k)
            target = c8 / "XAUUSD" / f"{INIZIO.isoformat()}.bi5"
            target.write_bytes(target.read_bytes() + b"\xff")
            return res

        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False), \
                mock.patch.object(RV, "autorizza", side_effect=manometti_dopo_aut):
            r8 = EV.esegui(s8, reg8, ris8, "P1", c8, cache_sv, base / "r8.txt", ORA)
        st8 = RV.stato(ris8)
        print(
            f"  [RILEVATO]      file sostituito dopo autorizzazione -> esito_tecnico={r8['esito_tecnico']}, "
            f"esito={r8['esito']}, riserva_consumata={st8['giorni']['consumato']}"
        )

    # 6.3 Contratto H-003, sigillo, ripresa
    with tempfile.TemporaryDirectory(prefix="r19_m_sig_") as td:
        base = Path(td)
        # Doppio blocco contratto
        s_dop = base / "H-DOP.md"
        bl = f"```json contratto-h003\n{json.dumps(contratto('H-DOP'))}\n```"
        s_dop.write_text(f"{bl}\n{bl}\n", encoding="utf-8")
        check_err("contratto: doppio blocco json contratto-h003", lambda: EV.leggi_contratto(s_dop))

        # Variante non nel sigillo (#137) + scheda modificata + sedute sbagliate
        reg = base / "reg.json"
        ris = base / "ris.json"
        RV.crea(ris, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_ok = base / "H-S.md"
        s_ok.write_text(testo_scheda(contratto("H-S")), encoding="utf-8")
        S.sigilla(reg, "H-S", s_ok, ["V-B"], ORA, codice=EV.impronte_codice())  # solo V-B, contratto chiede V-T
        RV.prenota(ris, "P1", "H-S", LETTURA, FINE, S.impronta(s_ok), ORA)
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            check_err("sigillo: variante contratto non nel sigillo (#137)",
                      lambda: EV.esegui(s_ok, reg, ris, "P1", cache, cache_sv, base / "r.txt", ORA))

        # sigillo: esito senza verifica + doppio esito
        reg_e = base / "reg_e.json"
        S.sigilla(reg_e, "H-E", s_ok, ["V-T"], ORA, codice=EV.impronte_codice())
        check_err("sigillo: esito senza verifica",
                  lambda: S.registra_esecuzioni(reg_e, "H-E", [{"ruolo": "esito", "variante": "V-T", "esito": "promossa"}], ORA))
        S.registra_esecuzioni(reg_e, "H-E", [{"ruolo": "verifica", "variante": "V-T"}], ORA)
        S.registra_esecuzioni(reg_e, "H-E", [{"ruolo": "esito", "variante": "V-T", "esito": "promossa"}], ORA)
        check_err("sigillo: doppio esito",
                  lambda: S.registra_esecuzioni(reg_e, "H-E", [{"ruolo": "esito", "variante": "V-T", "esito": "bocciata"}], ORA))

        # Ripresa valida + ripresa con seme/codice diversi + ripetizione tecnica dopo caduta tra autorizza e rendiconta
        reg_r = base / "reg_r.json"
        ris_r = base / "ris_r.json"
        RV.crea(ris_r, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)
        s_r = base / "H-R.md"
        s_r.write_text(testo_scheda(contratto("H-R")), encoding="utf-8")
        S.sigilla(reg_r, "H-R", s_r, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(ris_r, "P1", "H-R", LETTURA, FINE, S.impronta(s_r), ORA)
        with mock.patch.object(EV, "ANCORA_GIT", False), mock.patch.object(EV, "CONTROLLO_AMBIENTE", False):
            # Prima caduta simulata tra autorizza e rendiconta -> ripetizione tecnica
            with mock.patch.object(RV, "rendiconta", side_effect=RuntimeError("caduta post-aut")):
                try:
                    EV.esegui(s_r, reg_r, ris_r, "P1", cache, cache_sv, base / "r0.txt", ORA)
                except RuntimeError:
                    pass
            r_tec = EV.esegui(s_r, reg_r, ris_r, "P1", cache, cache_sv, base / "r1.txt", ORA)
            print(f"  [RILEVATO/OK]   ripetizione tecnica post-autorizzazione -> {r_tec['esito_tecnico']}/{r_tec['esito']}, j={RV.stato(ris_r)['aperture'][0]['j']}")
            # Ripresa valida dopo verdetto
            r_rig = EV.esegui(s_r, reg_r, ris_r, "P1", cache, cache_sv, base / "r2.txt", ORA)
            print(f"  [RILEVATO/OK]   ripresa valida dopo verdetto -> {r_rig['esito_tecnico']}, chiamate={r_rig['chiamate_caricatore']}")
            # Ripresa con codice modificato
            with mock.patch.object(EV, "impronte_codice", return_value={"finto.py": "0" * 64}):
                check_err("ripresa: codice diverso dal record",
                          lambda: EV.esegui(s_r, reg_r, ris_r, "P1", cache, cache_sv, base / "r3.txt", ORA))

    # 6.4 Lanciatore avvio.py: flag mancanti, -X pycache_prefix, file .py in radice, cartella importabile, __pycache__
    with tempfile.TemporaryDirectory(prefix="r19_m_avv_") as td:
        base = Path(td)
        repo, reg, ris, scheda, g = prepara_repo_copia(base, cache, cache_sv, ipotesi="H-AV")
        cmd_base = [
            sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
            "--scheda", str(scheda), "--registro", str(reg), "--riserva", str(ris),
            "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
            "--rapporto", str(base / "rap.txt"), "--ora", ORA,
        ]
        # senza -I -S -B
        r_noflag = subprocess.run([sys.executable] + cmd_base[4:], cwd=str(repo), env=NO_NET, capture_output=True, text=True)
        print(f"  [{'RILEVATO' if r_noflag.returncode == 2 else 'NON RILEVATO!'}]      avvio: senza -I -S -B -> rc={r_noflag.returncode} | {r_noflag.stderr.strip()[:90]}")
        # -X pycache_prefix
        r_xp = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={base / 'pc'}"] + cmd_base[4:],
                              cwd=str(repo), env=NO_NET, capture_output=True, text=True)
        print(f"  [{'RILEVATO' if r_xp.returncode == 2 else 'NON RILEVATO!'}]      avvio: -X pycache_prefix -> rc={r_xp.returncode} | {r_xp.stderr.strip()[:90]}")
        # .py estraneo in radice
        estr = repo / "statistics.py"
        estr.write_text("x = 1\n", encoding="utf-8")
        r_py = subprocess.run(cmd_base, cwd=str(repo), env=NO_NET, capture_output=True, text=True)
        estr.unlink()
        print(f"  [{'RILEVATO' if r_py.returncode == 2 else 'NON RILEVATO!'}]      avvio: .py estraneo in radice -> rc={r_py.returncode} | {r_py.stderr.strip()[:90]}")
        # cartella importabile in radice
        cimp = repo / "statistics"
        cimp.mkdir()
        r_dir = subprocess.run(cmd_base, cwd=str(repo), env=NO_NET, capture_output=True, text=True)
        cimp.rmdir()
        print(f"  [{'RILEVATO' if r_dir.returncode == 2 else 'NON RILEVATO!'}]      avvio: cartella importabile in radice -> rc={r_dir.returncode} | {r_dir.stderr.strip()[:90]}")
        # __pycache__ dentro brain/
        pc = repo / "brain/laboratorio/esecuzione/__pycache__"
        pc.mkdir()
        r_pc = subprocess.run(cmd_base, cwd=str(repo), env=NO_NET, capture_output=True, text=True)
        pc.rmdir()
        print(f"  [{'RILEVATO' if r_pc.returncode == 2 else 'NON RILEVATO!'}]      avvio: __pycache__ in brain/ -> rc={r_pc.returncode} | {r_pc.stderr.strip()[:90]}")


def main() -> int:
    print(f"Python: {sys.version.splitlines()[0]} | Platform: {platform.platform()}")
    with tempfile.TemporaryDirectory(prefix="r19_cache_") as tc:
        base_c = Path(tc)
        cache, cache_sv = base_c / "cache", base_c / "cache_sviluppo"
        M.scrivi(cache, LETTURA, FINE, 0.6, 11)
        M.scrivi(cache, B_INIZIO, B_FINE, 0.6, 12)
        M.scrivi(cache_sv, *SVILUPPO, 0.6, 13)
        sezione_1_avvio_critici(cache, cache_sv)
        sezione_2_regressioni_e_bug(cache, cache_sv)
        sezione_3_concorrenza_reale(cache, cache_sv)
        sezione_4_verdetto_124()
        sezione_5_matrice_d51(cache, cache_sv)
        sezione_6_manomissioni_complete(cache, cache_sv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
