"""Mandato R18 — Compito B: prove empiriche di TUTTE le 7 classi di manomissione sul perimetro (e476a9a).

Tutte le prove girano SOLO su copie temporanee (repository git clonati in cartelle temporanee, registri finti,
dati sintetici), MAI sul repository di lavoro né su GitHub, con HTTPS_PROXY=http://127.0.0.1:9.
"""
import datetime as dt
import hashlib
import json
import lzma
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.dati.pipeline import dukascopy as DK  # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SYN  # noqa: E402

NO_NET = dict(
    os.environ,
    HTTPS_PROXY="http://127.0.0.1:9",
    HTTP_PROXY="http://127.0.0.1:9",
    https_proxy="http://127.0.0.1:9",
    http_proxy="http://127.0.0.1:9",
    NO_PROXY="",
    no_proxy="",
)


def _git(cwd: Path, *args, env=None, check=True):
    r = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        env=env or NO_NET,
    )
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args} fallito: {r.stderr.strip()}")
    return r


def _mk_repo_con_remoto(td: Path):
    """Crea un bare remote locale + clone con brain/ copiato, scheda, registro_prove.json sigillato e pushato."""
    bare = td / "remote.git"
    work = td / "work"
    bare.mkdir()
    _git(bare, "init", "--bare")
    _git(bare, "config", "uploadpack.allowFilter", "true")
    _git(td, "clone", f"file://{bare}", str(work))
    _git(work, "config", "user.name", "test-r18")
    _git(work, "config", "user.email", "test@invalid")
    _git(work, "checkout", "-b", "feat/prova")
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(
            ROOT / "brain" / parte,
            work / "brain" / parte,
            ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"),
        )
    (work / "brain" / "__init__.py").write_text("", encoding="utf-8")
    scheda = work / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md"
    scheda.parent.mkdir(parents=True, exist_ok=True)
    scheda.write_text("# Scheda finta R18\n", encoding="utf-8")
    reg = work / E.REL_REGISTRO
    if reg.exists():
        reg.unlink()
    codice = E.impronte_codice(work)
    S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], "2026-11-15T10:00:00Z",
              codice=codice, robustezza=E.nomi_robustezza())
    # Aggiungiamo una terza prova selezionabile per testare riduzione di N
    d = S.leggi(reg)
    d["prove"].append({"id": "H-001/V-0", "ipotesi": "H-001", "ruolo": "selezionabile", "ora": "2026-11-14T10:00:00Z"})
    S._scrivi(reg, d)
    # Aggiungiamo uno sviluppo finto con promossa=False per testare alterazione esito
    S.registra_esecuzione(reg, "H-002", {
        "ruolo": "sviluppo", "variante": "V-T", "promossa": False,
        "periodo": ["2023-11-15", "2026-11-12"], "cache": "/tmp/fake", "dati_sha256": "aa" * 32,
    }, "2026-11-15T11:00:00Z")
    _git(work, "add", "brain")
    _git(work, "commit", "-m", "init sigillo e sviluppo")
    _git(work, "push", "-u", "origin", "feat/prova")
    return bare, work, reg, scheda


def _worker_verifica(reg_str: str) -> str:
    try:
        S.registra_esecuzione(Path(reg_str), "H-002", {"ruolo": "verifica", "variante": "V-T"}, "2026-11-16T10:00:00Z")
        return "OK"
    except Exception as e:
        return f"ERR:{type(e).__name__}"


def _worker_autorizza(reg_str: str) -> str:
    try:
        RV.autorizza(Path(reg_str), "id-1", n_globale=3, hash_dati="a" * 64, ora="2026-11-16T10:00:00Z", m=1)
        return "OK"
    except Exception as e:
        return f"ERR:{type(e).__name__}"


def classe_1_registro():
    print("\n=== CLASSE 1: Registro delle prove (registro_prove.json) ===")
    with tempfile.TemporaryDirectory(prefix="r18_b1_") as td:
        _, work, reg, scheda = _mk_repo_con_remoto(Path(td))
        base = reg.read_text(encoding="utf-8")

        # B1.1: N ridotto (tolta una prova selezionabile, committato su HEAD)
        d = json.loads(base)
        d["prove"] = d["prove"][:2]
        reg.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        _git(work, "commit", "-am", "riduci N")
        try:
            S.controlla_ancora(reg, work)
            r1 = "NON_RILEVATO"
        except ValueError as e:
            r1 = f"RILEVATO ({e})"
        _git(work, "reset", "--hard", "origin/feat/prova")
        print(f"  [B1.1 N ridotto dopo push] {r1}")

        # B1.2: esito sviluppo cambiato promossa False -> True dopo push
        d = json.loads(base)
        d["esecuzioni"][0]["promossa"] = True
        reg.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        _git(work, "commit", "-am", "cambia esito")
        try:
            S.controlla_ancora(reg, work)
            r2 = "NON_RILEVATO"
        except ValueError as e:
            r2 = f"RILEVATO ({e})"
        _git(work, "reset", "--hard", "origin/feat/prova")
        print(f"  [B1.2 esito cambiato dopo push] {r2}")

        # B1.3: prove riordinate
        d = json.loads(base)
        d["prove"] = list(reversed(d["prove"]))
        reg.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        _git(work, "commit", "-am", "riordina prove")
        try:
            S.controlla_ancora(reg, work)
            r3 = "NON_RILEVATO"
        except ValueError as e:
            r3 = f"RILEVATO ({e})"
        _git(work, "reset", "--hard", "origin/feat/prova")
        print(f"  [B1.3 prove riordinate dopo push] {r3}")

        # B1.4: sigillo riscritto dopo push
        d = json.loads(base)
        d["sigilli"][0]["scheda_sha256"] = "0" * 64
        reg.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        _git(work, "commit", "-am", "riscrivi sigillo")
        try:
            S.controlla_ancora(reg, work)
            r4 = "NON_RILEVATO"
        except ValueError as e:
            r4 = f"RILEVATO ({e})"
        _git(work, "reset", "--hard", "origin/feat/prova")
        print(f"  [B1.4 sigillo riscritto dopo push] {r4}")

        # B1.5: limite dichiarato #90: aggiunta di un falso sviluppo coerente prima del push (nuova variante V-S)
        d = json.loads(base)
        d["esecuzioni"].append({
            "ipotesi": "H-002", "ruolo": "sviluppo", "variante": "V-S", "promossa": True,
            "periodo": ["2023-11-15", "2026-11-12"], "cache": "/tmp/fake", "dati_sha256": "aa" * 32,
            "ora": "2026-11-15T12:00:00Z",
        })
        reg.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
        _git(work, "commit", "-am", "finto sviluppo V-S promossa")
        S.controlla_ancora(reg, work)
        S.controlla_sigillo(reg, "H-002", scheda, codice=E.impronte_codice(work))
        print("  [B1.5 falso sviluppo coerente aggiunto in fondo (#90)] NON_RILEVATO (passa ancora + sigillo)")


def classe_2_git():
    print("\n=== CLASSE 2: Storia git ===")
    with tempfile.TemporaryDirectory(prefix="r18_b2_") as td:
        td = Path(td)
        bare, work, reg, _ = _mk_repo_con_remoto(td)

        # B2.1: amend dopo push (senza toccare refs/remotes)
        _git(work, "commit", "--amend", "-m", "amended")
        try:
            S.controlla_ancora(reg, work)
            r1 = "NON_RILEVATO"
        except ValueError as e:
            r1 = f"RILEVATO ({e})"
        _git(work, "reset", "--hard", "origin/feat/prova")
        print(f"  [B2.1 git commit --amend] {r1}")

        # Aggiungiamo una verifica, committiamo e pushiamo
        S.registra_esecuzione(reg, "H-002", {"ruolo": "verifica", "variante": "V-T"}, "2026-11-16T10:00:00Z")
        _git(work, "commit", "-am", "verifica V-T")
        _git(work, "push")

        # B2.2: clone parziale --depth 1
        shallow = td / "shallow"
        _git(td, "clone", "--depth", "1", "--branch", "feat/prova", f"file://{bare}", str(shallow))
        sh_flag = _git(shallow, "rev-parse", "--is-shallow-repository").stdout.strip()
        try:
            S.versioni_nella_storia(shallow, E.REL_REGISTRO)
            r2 = f"NON_RILEVATO (is_shallow={sh_flag})"
        except ValueError as e:
            r2 = f"RILEVATO (is_shallow={sh_flag}, {e})"
        print(f"  [B2.2 clone --depth 1] {r2}")

        # B2.3: branch -D + update-ref con reflog intatto (#98)
        old_sha = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        _git(work, "checkout", "-b", "feat/pulito", old_sha)
        _git(work, "branch", "-D", "feat/prova")
        _git(work, "update-ref", "refs/remotes/origin/feat/prova", old_sha)
        vers = S.versioni_nella_storia(work, E.REL_REGISTRO)
        vista_ver = any(e.get("ruolo") == "verifica" for v in vers for e in v.get("esecuzioni", []))
        print(f"  [B2.3 branch -D + update-ref con reflog intatto] RILEVATO={vista_ver} (versioni={len(vers)})")

        # B2.4: cancellazione reflog + gc --prune=now (limite dichiarato #98)
        _git(work, "reflog", "expire", "--expire=now", "--all")
        _git(work, "gc", "--prune=now")
        vers_dopo = S.versioni_nella_storia(work, E.REL_REGISTRO)
        vista_dopo = any(e.get("ruolo") == "verifica" for v in vers_dopo for e in v.get("esecuzioni", []))
        print(f"  [B2.4 update-ref + reflog expire + gc --prune (#98)] vista_verifica={vista_dopo} (NON_RILEVATO localmente)")

        # B2.5: clone parziale BLOBLESS (--filter=blob:none) + scollegamento remoto (rete bloccata)!
        # Ri-prepariamo un bare con 2 commit: commit1 (N=5, verifica V-T) e commit2 (registro resettato o ramo)
        bare2 = td / "remote2.git"
        work2 = td / "work2"
        bare2.mkdir()
        _git(bare2, "init", "--bare")
        _git(bare2, "config", "uploadpack.allowFilter", "true")
        _git(td, "clone", f"file://{bare2}", str(work2))
        _git(work2, "config", "user.name", "t")
        _git(work2, "config", "user.email", "t@invalid")
        _git(work2, "checkout", "-b", "feat/p2")
        reg2 = work2 / E.REL_REGISTRO
        reg2.parent.mkdir(parents=True, exist_ok=True)
        reg2.write_text(json.dumps({
            "schema": "registro-prove/1",
            "prove": [{"id": f"H-{i}", "ipotesi": "H-002", "ruolo": "selezionabile", "ora": "2026-11-15T00:00:00Z"}
                      for i in range(5)],
            "sigilli": [],
            "esecuzioni": [{"ipotesi": "H-002", "ruolo": "verifica", "variante": "V-T", "ora": "2026-11-15T01:00:00Z"}],
        }), encoding="utf-8")
        _git(work2, "add", ".")
        _git(work2, "commit", "-m", "c1 con verifica e N=5")
        # Secondo commit dove togliamo la verifica (es. merge/storia)
        reg2.write_text(json.dumps({
            "schema": "registro-prove/1",
            "prove": [{"id": "H-0", "ipotesi": "H-002", "ruolo": "selezionabile", "ora": "2026-11-15T00:00:00Z"}],
            "sigilli": [],
            "esecuzioni": [],
        }), encoding="utf-8")
        _git(work2, "commit", "-am", "c2 senza verifica e N=1")
        _git(work2, "push", "-u", "origin", "feat/p2")

        blobless = td / "blobless"
        _git(td, "clone", "--filter=blob:none", f"file://{bare2}", str(blobless))
        # Scolleghiamo il remoto (simula rete bloccata HTTPS_PROXY=127.0.0.1:9)
        _git(blobless, "remote", "set-url", "origin", "https://127.0.0.1:9/repo.git")
        is_shallow = _git(blobless, "rev-parse", "--is-shallow-repository").stdout.strip()
        vers_blob = S.versioni_nella_storia(blobless, E.REL_REGISTRO)
        vista_ver_blob = any(e.get("ruolo") == "verifica" for v in vers_blob for e in v.get("esecuzioni", []))
        max_n_blob = max((S.n_prove(v) for v in vers_blob), default=0)
        print(
            f"  [B2.5 clone --filter=blob:none (rete bloccata)] is_shallow={is_shallow}, "
            f"versioni_lette={len(vers_blob)}/2, vista_verifica={vista_ver_blob}, max_N={max_n_blob} "
            f"({'NON_RILEVATO!' if not vista_ver_blob else 'RILEVATO'})"
        )

        # B2.6: data commit falsa + --ora anteriore al sigillo
        env_date = dict(NO_NET, GIT_AUTHOR_DATE="2020-01-01T00:00:00Z", GIT_COMMITTER_DATE="2020-01-01T00:00:00Z")
        _git(work2, "commit", "--allow-empty", "-m", "data falsa", env=env_date)
        dt_comm = _git(work2, "log", "-1", "--format=%cI").stdout.strip()
        ora_ok = bool(E._ORA_ISO.fullmatch("2020-01-01T00:00:00Z"))
        print(f"  [B2.6 data commit falsa / --ora retrodatata] git_committer_date={dt_comm}, ora_regex_ok={ora_ok} (NON_RILEVATO su data)")


def classe_3_ambiente():
    print("\n=== CLASSE 3: Ambiente d'esecuzione ===")
    with tempfile.TemporaryDirectory(prefix="r18_b3_") as td:
        td = Path(td)
        _, work, reg, _ = _mk_repo_con_remoto(td)
        avvio = work / "brain" / "laboratorio" / "esecuzione" / "avvio.py"

        # B3.1: PYTHONPATH avvelenato con -I -S -B vs senza -I
        evil = td / "evil_py"
        evil.mkdir()
        (evil / "statistics.py").write_text("raise RuntimeError('POISONED')\n", encoding="utf-8")
        env_p = dict(NO_NET, PYTHONPATH=str(evil))
        r_no_i = subprocess.run([sys.executable, "-S", "-B", str(avvio), "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                                cwd=work, env=env_p, capture_output=True, text=True)
        print(f"  [B3.1a PYTHONPATH senza -I] rc={r_no_i.returncode} ({'RILEVATO' if r_no_i.returncode == 2 else 'NON_RILEVATO'})")
        r_con_i = subprocess.run([sys.executable, "-I", "-S", "-B", "-c",
                                  "import sys, statistics; print('OK', statistics.__file__)"],
                                 cwd=work, env=env_p, capture_output=True, text=True)
        print(f"  [B3.1b PYTHONPATH con -I -S -B] rc={r_con_i.returncode}, poisoned={'POISONED' in r_con_i.stderr} (BLOCCATO)")

        # B3.2: file .pth e sitecustomize.py nella radice
        pth = work / "veleno.pth"
        pth.write_text("import os\n", encoding="utf-8")
        r_pth = subprocess.run([sys.executable, "-I", "-S", "-B", str(avvio), "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                               cwd=work, env=NO_NET, capture_output=True, text=True)
        pth.unlink()
        print(f"  [B3.2 file .pth nella radice] rc={r_pth.returncode} ({'RILEVATO' if r_pth.returncode == 2 else 'NON_RILEVATO'})")

        # B3.3: .pyc in brain/__pycache__ e -X pycache_prefix
        pc = work / "brain" / "laboratorio" / "esecuzione" / "__pycache__"
        pc.mkdir()
        (pc / "criteri.cpython-39.pyc").write_bytes(b"fake")
        r_pyc = subprocess.run([sys.executable, "-I", "-S", "-B", str(avvio), "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                               cwd=work, env=NO_NET, capture_output=True, text=True)
        shutil.rmtree(pc)
        r_pref = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", f"pycache_prefix={td}/pcx", str(avvio),
                                 "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                                cwd=work, env=NO_NET, capture_output=True, text=True)
        print(f"  [B3.3 .pyc in brain / -X pycache_prefix] rc_pyc={r_pyc.returncode}, rc_prefix={r_pref.returncode} (RILEVATO)")

        # B3.4: cartella statistics/ con __init__.pyc + statistics.zip nella radice (#95, #96, #103)
        st_dir = work / "statistics"
        st_dir.mkdir()
        (st_dir / "__init__.pyc").write_bytes(b"fake")
        r_dir = subprocess.run([sys.executable, "-I", "-S", "-B", str(avvio), "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                               cwd=work, env=NO_NET, capture_output=True, text=True)
        shutil.rmtree(st_dir)
        zf = work / "statistics.zip"
        zf.write_bytes(b"PK\x05\x06" + b"\x00" * 18)
        r_zip = subprocess.run([sys.executable, "-I", "-S", "-B", str(avvio), "--modalita", "sviluppo", "--rapporto", str(td / "r.md")],
                               cwd=work, env=NO_NET, capture_output=True, text=True)
        zf.unlink()
        print(f"  [B3.4 cartella statistics/ e .zip nella radice] rc_dir={r_dir.returncode}, rc_zip={r_zip.returncode} (RILEVATO)")

        # B3.5: PYTHONHASHSEED e TZ=America/New_York
        # Verifica determinismo di confronto_casuale con PYTHONHASHSEED=1 vs 999 e TZ diversi
        out_hashes = []
        for hs, tz in (("1", "UTC"), ("999", "America/New_York")):
            env_t = dict(NO_NET, PYTHONHASHSEED=hs, TZ=tz)
            r_t = subprocess.run(
                [sys.executable, "-s", "-B", "-c",
                 "from brain.laboratorio.esecuzione import criteri as K, esegui_h002 as E; "
                 "E.controlla_fuso(); "
                 "print(K.confronto_casuale([(1.0,-1.0),(-0.5,0.5),(0.8,-0.8)]*20, 0.2, 200, 42))"],
                cwd=ROOT, env=env_t, capture_output=True, text=True,
            )
            assert r_t.returncode == 0, r_t.stderr
            out_hashes.append(r_t.stdout.strip())
        print(f"  [B3.5 PYTHONHASHSEED + TZ=America/New_York] identico={out_hashes[0] == out_hashes[1]} (PROTETTO)")


def _bi5_giorno(giorno: dt.date, prezzo_base: float) -> bytes:
    """Crea un .bi5 valido per tutti i 525 minuti della sessione 08:00-16:45 Londra."""
    from brain.laboratorio.simulatori.orb_londra import _utc
    a = _utc(giorno, dt.time(8, 0))
    mezzanotte = dt.datetime(giorno.year, giorno.month, giorno.day, tzinfo=dt.timezone.utc)
    buf = bytearray()
    for m in range(525):
        t = a + dt.timedelta(minutes=m)
        sec = int((t - mezzanotte).total_seconds())
        p = int(round((prezzo_base + 0.01 * (m % 5)) * 1000))
        buf += DK.RECORD.pack(sec, p, p, p - 50, p + 50, 1.0)
    return lzma.compress(bytes(buf), format=lzma.FORMAT_ALONE)


def classe_4_dati():
    print("\n=== CLASSE 4: Dati (cache BID/ASK, partizione, buchi, symlink, ..) ===")
    with tempfile.TemporaryDirectory(prefix="r18_b4_") as td:
        td = Path(td)
        # Generiamo un piccolo mercato sintetico (40 giorni di sviluppo) su disco in formato bi5
        bid, ask = SYN.mercato(dt.date(2024, 1, 2), giorni=60, seme=7, spinta=0.01, deriva=0.0, spread=0.5)
        res_ok = E.esegui_sviluppo(bid, ask)
        r_ok = res_ok["varianti"]["V-T"]["metriche"]["r_medio"]
        n_ok = res_ok["varianti"]["V-T"]["metriche"]["n"]

        # B4.1: BID e ASK scambiati (ask < bid ovunque)
        res_swap = E.esegui_sviluppo(ask, bid)
        n_swap = res_swap["varianti"]["V-T"]["metriche"]["n"]
        neg_swap = res_swap["resoconto"]["minuti_spread_negativo"]
        print(f"  [B4.1 BID/ASK scambiati] n_trade={n_swap} (vs {n_ok}), minuti_spread_negativo={neg_swap} (RILEVATO da orb_londra: 0 trade)")

        # B4.2: ASK identico a BID (copia o symlink XAUUSD_ASK -> XAUUSD: spread=0!)
        res_zero = E.esegui_sviluppo(bid, bid)
        r_zero = res_zero["varianti"]["V-T"]["metriche"]["r_medio"]
        n_zero = res_zero["varianti"]["V-T"]["metriche"]["n"]
        neg_zero = res_zero["resoconto"]["minuti_spread_negativo"]
        print(
            f"  [B4.2 ASK==BID (spread=0,00)] n_trade={n_zero} (vs {n_ok}), R_medio={r_zero:.4f} (vs {r_ok:.4f}, "
            f"delta={r_zero - r_ok:+.4f} R!), minuti_spread_neg={neg_zero} -> NON_RILEVATO!"
        )

        # Verifica che caricatore.carica accetti anche symlink XAUUSD_ASK -> XAUUSD e giorno duplicato e giorno riserva rinominato
        reg = td / "registro_prove.json"
        scheda = td / "scheda.md"
        scheda.write_text("# finta\n", encoding="utf-8")
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], "2026-11-15T00:00:00Z")

        cache = td / "cache"
        cbid = cache / "XAUUSD"
        cbid.mkdir(parents=True)
        g1, g2 = dt.date(2024, 1, 2), dt.date(2024, 1, 3)
        b_bytes = _bi5_giorno(g1, 2000.0)
        (cbid / f"{g1.isoformat()}.bi5").write_bytes(b_bytes)
        (cbid / f"{g2.isoformat()}.bi5").write_bytes(b_bytes)  # giorno duplicato identico!
        cask_link = cache / "XAUUSD_ASK"
        cask_link.symlink_to(cbid)
        b_car, a_car, info = C.carica(cbid, cask_link, g1, g2, "sviluppo", reg, "H-002", scheda)
        print(
            f"  [B4.3/B4.5/B4.6 symlink XAUUSD_ASK->XAUUSD + giorno duplicato] "
            f"caricatore accetta senza errore: min_bid={info['minuti_bid']}, min_ask={info['minuti_ask']}, "
            f"incompleti={info['feriali_incompleti_bid']} -> NON_RILEVATO"
        )

        # B4.4: date della partizione fuori finestra
        try:
            C.carica(cbid, cask_link, dt.date(2023, 10, 1), dt.date(2023, 10, 2), "sviluppo", reg, "H-002", scheda)
            r_part = "NON_RILEVATO"
        except ValueError as e:
            r_part = f"RILEVATO ({e})"
        print(f"  [B4.4 data riserva in sviluppo] {r_part}")

        # B4.5b: buco mascherato (giorno feriale con 263 minuti tutti nel pomeriggio)
        g3 = dt.date(2024, 1, 4)
        from brain.laboratorio.simulatori.orb_londra import _utc
        a_p = _utc(g3, dt.time(12, 0))
        m_p = dt.datetime(g3.year, g3.month, g3.day, tzinfo=dt.timezone.utc)
        buf = bytearray()
        for m in range(263):
            t = a_p + dt.timedelta(minutes=m)
            sec = int((t - m_p).total_seconds())
            buf += DK.RECORD.pack(sec, 2000000, 2000000, 1999950, 2000050, 1.0)
        (cbid / f"{g3.isoformat()}.bi5").write_bytes(lzma.compress(bytes(buf), format=lzma.FORMAT_ALONE))
        _, _, info3 = C.carica(cbid, cask_link, g1, g3, "sviluppo", reg, "H-002", scheda)
        print(f"  [B4.5b buco mascherato nel mattino] incompleti_bid={info3['feriali_incompleti_bid']} (RILEVATO)")

        # B4.6b: symlink sul registro -> rifiutato da ancora_git
        reg_link = td / "link_reg.json"
        reg_link.symlink_to(reg)
        try:
            S.controlla_ancora(reg_link, td)
            r_sl = "NON_RILEVATO"
        except ValueError as e:
            r_sl = f"RILEVATO ({e})"
        print(f"  [B4.6b symlink sul registro] {r_sl}")


def classe_5_riserva():
    print("\n=== CLASSE 5: Registro della riserva (riserva.py) ===")
    with tempfile.TemporaryDirectory(prefix="r18_b5_") as td:
        td = Path(td)
        reg = td / "riserva.json"
        RV.crea(reg, dt.date(2005, 1, 1), dt.date(2023, 10, 31), 0.05, "2026-11-16T00:00:00Z",
                protetta=(dt.date(2020, 1, 1), dt.date(2023, 10, 31)))
        RV.prenota(reg, "p1", "H-002", dt.date(2005, 1, 1), dt.date(2008, 12, 31), "h1", "2026-11-16T00:01:00Z")
        RV.autorizza(reg, "p1", n_globale=2, hash_dati="a" * 64, ora="2026-11-16T00:02:00Z", m=1)

        # B5.1: alias di mercato sulle stesse date consumate
        try:
            RV.prenota(reg, "p2-alias", "H-999-GBPJPY", dt.date(2007, 1, 1), dt.date(2010, 12, 31), "h2", "2026-11-16T00:03:00Z")
            r_alias = "NON_RILEVATO"
        except ValueError as e:
            r_alias = f"RILEVATO ({e})"
        print(f"  [B5.1 alias di mercato sulle stesse date] {r_alias}")

        # B5.2: parte protetta senza sblocco
        try:
            RV.prenota(reg, "p3-prot", "H-003", dt.date(2020, 6, 1), dt.date(2021, 6, 1), "h3", "2026-11-16T00:04:00Z")
            r_prot = "NON_RILEVATO"
        except ValueError as e:
            r_prot = f"RILEVATO ({e})"
        print(f"  [B5.2 parte protetta senza sblocco] {r_prot}")

        # B5.3: alfa_j = NaN nel JSON!
        raw = reg.read_text(encoding="utf-8")
        raw_nan = raw.replace('"alfa_j": 0.025', '"alfa_j": NaN')
        assert raw_nan != raw
        reg_nan = td / "riserva_nan.json"
        reg_nan.write_text(raw_nan, encoding="utf-8")
        try:
            st_nan = RV.stato(reg_nan)
            r_nan = f"NON_RILEVATO! alfa_j={st_nan['aperture'][0]['alfa_j']!r}"
        except Exception as e:
            r_nan = f"RILEVATO ({type(e).__name__}: {e})"
        print(f"  [B5.3 alfa_j=NaN nel JSON della riserva] {r_nan}")

        # B5.4: j falsificato (j=1 ripetuto o j=True)
        d = json.loads(raw)
        d["eventi"][1]["j"] = True
        reg_j = td / "riserva_j.json"
        reg_j.write_text(json.dumps(d), encoding="utf-8")
        try:
            RV.stato(reg_j)
            r_j = "NON_RILEVATO"
        except ValueError as e:
            r_j = f"RILEVATO ({e})"
        print(f"  [B5.4 j booleano nel JSON] {r_j}")

        # B5.5: consumo dimenticato: esegui_h002.py non importa riserva.py
        uses_riserva = "riserva" in (ROOT / "brain" / "laboratorio" / "esecuzione" / "esegui_h002.py").read_text(encoding="utf-8")
        print(f"  [B5.5 consumo dimenticato: esegui_h002 chiama riserva] chiama_riserva={uses_riserva} (NON_RILEVATO: non collegato)")


def classe_6_concorrenza():
    print("\n=== CLASSE 6: Concorrenza (lock e atomicità) ===")
    with tempfile.TemporaryDirectory(prefix="r18_b6_") as td:
        td = Path(td)
        reg = td / "registro_prove.json"
        scheda = td / "scheda.md"
        scheda.write_text("# s\n", encoding="utf-8")
        S.sigilla(reg, "H-002", scheda, ["V-T"], "2026-11-15T00:00:00Z")
        with ProcessPoolExecutor(max_workers=2) as ex:
            esiti = list(ex.map(_worker_verifica, [str(reg), str(reg)]))
        ver_cnt = sum(1 for e in S.leggi(reg)["esecuzioni"] if e["ruolo"] == "verifica")
        print(f"  [B6.1 due verifiche concorrenti] esiti={sorted(esiti)}, verifiche_registrate={ver_cnt} (PROTETTO)")

        # B6.2: aggiramento advisory lock (unlink di .lock mentre è acquisito)
        import fcntl
        lock_p = reg.with_name(reg.name + ".lock")
        f1 = open(lock_p, "a")
        fcntl.flock(f1, fcntl.LOCK_EX)
        lock_p.unlink()  # secondo processo elimina .lock e ne crea un nuovo inode
        f2 = open(lock_p, "a")
        try:
            fcntl.flock(f2, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_aggirato = True
            fcntl.flock(f2, fcntl.LOCK_UN)
        except BlockingIOError:
            lock_aggirato = False
        finally:
            fcntl.flock(f1, fcntl.LOCK_UN)
            f1.close()
            f2.close()
        print(f"  [B6.2 advisory flock aggirato via unlink(.lock)] secondo_lock_ottenuto={lock_aggirato} (NON_RILEVATO)")


def classe_7_ci_github():
    print("\n=== CLASSE 7: Test automatici su GitHub (test.yml e esegui_test.py) ===")
    yml = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
    ha_paths_ignore = "paths-ignore" in yml
    mutanti_solo_manuali = "if: github.event_name == 'workflow_dispatch'" in yml
    cod = E.impronte_codice(ROOT)
    ci_sigillati = any(k.startswith(".github/") for k in cod)
    print(f"  [B7.1 analisi test.yml] paths_ignore_su_push={ha_paths_ignore}, mutanti_solo_manuali={mutanti_solo_manuali}, ci_nel_sigillo={ci_sigillati}")

    # B7.2: copia temporanea di esegui_test.py con test_costi_tick.py svuotato (0 test) e test_riserva rinominato
    with tempfile.TemporaryDirectory(prefix="r18_b7_") as td:
        tmp = Path(td)
        (tmp / ".github" / "scripts").mkdir(parents=True)
        shutil.copy2(ROOT / ".github" / "scripts" / "esegui_test.py", tmp / ".github" / "scripts" / "esegui_test.py")
        (tmp / "brain" / "dati" / "tests").mkdir(parents=True)
        (tmp / "brain" / "__init__.py").write_text("", encoding="utf-8")
        (tmp / "brain" / "dati" / "__init__.py").write_text("", encoding="utf-8")
        (tmp / "brain" / "dati" / "tests" / "__init__.py").write_text("", encoding="utf-8")
        (tmp / "brain" / "guardian" / "test").mkdir(parents=True)
        # Suite vuota (0 test!) e suite con solo skip
        (tmp / "brain" / "dati" / "tests" / "test_svuotato.py").write_text("import unittest\n", encoding="utf-8")
        (tmp / "brain" / "dati" / "tests" / "test_saltato.py").write_text(
            "import unittest\nclass T(unittest.TestCase):\n    @unittest.skip('saltato')\n    def test_a(self): self.fail()\n",
            encoding="utf-8",
        )
        r = subprocess.run([sys.executable, "-s", "-B", ".github/scripts/esegui_test.py"],
                           cwd=tmp, env=NO_NET, capture_output=True, text=True)
        verde = (r.returncode == 0 and "TUTTO VERDE" in r.stdout)
        print(f"  [B7.2 esegui_test.py su suite svuotata (0 test) e saltata] rc={r.returncode}, TUTTO_VERDE={verde} (NON_RILEVATO!)")


def main() -> int:
    classe_1_registro()
    classe_2_git()
    classe_3_ambiente()
    classe_4_dati()
    classe_5_riserva()
    classe_6_concorrenza()
    classe_7_ci_github()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
