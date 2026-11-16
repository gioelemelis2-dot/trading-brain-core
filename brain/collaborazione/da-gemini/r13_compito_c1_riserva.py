"""Mandato R13 · Compito C1: primo attacco a brain/laboratorio/esecuzione/riserva.py.

Sonde (>= 5):
- RV-P1: Manomissioni che _ricostruisci / stato() NON vedono:
         (a) protetta=null / fine esteso / alfa_tot gonfiato in testa "riserva";
         (b) esito="bocciata"->"promossa", n_globale, hash_dati, ipotesi, usa_protetta modificati in-place;
         (c) troncamento di eventi autorizzazione/esito in coda (date consumate tornano disponibili!);
         (d) assenza di controllo git (controlla_ancora) o hash chain.
- RV-P2: Campi non validati: bool m=True / j=True accettati; n_globale <= 0 / None / decrescente accettati;
         hash_dati vuoto accettato; autorizza() chiamato DOPO rendiconta() continua a rispondere ok.
- RV-P3: Parte protetta e quarantena: quarantena accetta date protette senza usa_protetta; usa_protetta=True
         sblocca senza motivo né conferma extra; adiacenze al bordo.
- RV-P4: Ripetizione tecnica e doppie autorizzazioni: verifica con ripetizione su stesso id vs nuovo id
         dopo rilascia; tolleranza 1e-15 su alfa_j.
- RV-P5: Concorrenza reale fra PROCESSI (multiprocessing.get_context("spawn"), non solo thread):
         8 processi su perimetro sovrapposto (solo 1 vince) e 10 processi su date disgiunte (nessuna perdita).
- RV-P6: Verifica indipendente della somma telescopica alfa_speso e quota_famiglia con m=1..5.

Nuovi mutanti (>= 5): MRV01..MRV06 su riserva.py in copia isolata.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import json
import multiprocessing as mp
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.esecuzione import riserva as RV  # noqa: E402

ORA = "2026-11-16T01:30:00Z"


def _mp_race_overlap(reg_str: str, k: int, barriera, coda) -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from brain.laboratorio.esecuzione import riserva as _RV
    reg = Path(reg_str)
    barriera.wait()
    try:
        _RV.prenota(reg, f"P{k}", f"H-{k}", date(2005, 3, 1 + k), date(2005, 3, 20 + k), "d", ORA)
        _RV.autorizza(reg, f"P{k}", 10, "hash", ORA)
        coda.put(("WIN", k))
    except ValueError as exc:
        coda.put(("LOSS", k, str(exc)))


def _mp_race_disjoint(reg_str: str, k: int, barriera, coda) -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from brain.laboratorio.esecuzione import riserva as _RV
    reg = Path(reg_str)
    a = date(2005, 4, 1) + timedelta(days=5 * k)
    b = a + timedelta(days=2)
    barriera.wait()
    _RV.prenota(reg, f"D{k}", "H-D", a, b, "d", ORA)
    coda.put(k)


def sonda_rv_p1_manomissioni_non_viste(base: Path) -> dict:
    d = base / "rv_p1"
    d.mkdir()
    reg = d / "riserva.json"
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), 0.05, ORA, protetta=(date(2005, 11, 1), date(2005, 12, 31)))
    RV.prenota(reg, "A", "H-1", date(2005, 1, 1), date(2005, 1, 31), "q1", ORA)
    RV.autorizza(reg, "A", 20, "datiA", ORA)
    RV.rendiconta(reg, "A", "bocciata", ORA)

    # 1. Mutazione testa "riserva": tolgo protetta, estendo fine al 2099
    raw = json.loads(reg.read_text(encoding="utf-8"))
    raw["riserva"]["protetta"] = None
    raw["riserva"]["fine"] = "2099-12-31"
    # 2. Mutazione eventi in-place: esito bocciata->promossa, n_globale 20->1, hash_dati, ipotesi
    raw["eventi"][0]["ipotesi"] = "H-TAROCCATA"
    raw["eventi"][1]["n_globale"] = 1
    raw["eventi"][1]["hash_dati"] = "ALTRO"
    raw["eventi"][2]["esito"] = "promossa"
    reg.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    st_tampered = RV.stato(reg)

    # 3. Troncamento in coda: tolgo autorizzazione ed esito di A, poi autorizzo A di nuovo sullo stesso perimetro!
    raw2 = json.loads(reg.read_text(encoding="utf-8"))
    raw2["eventi"] = raw2["eventi"][:1]  # resta solo prenotazione A
    reg.write_text(json.dumps(raw2, indent=2), encoding="utf-8")
    a_reopen = RV.autorizza(reg, "A", 1, "datiA_v2", ORA)

    return {
        "stato_accetta_testa_e_eventi_manomessi": (
            st_tampered["giorni_protetti"] == 0
            and st_tampered["aperture"][0]["esito"] == "promossa"
            and st_tampered["aperture"][0]["n_globale"] == 1
        ),
        "troncamento_coda_permette_seconda_autorizzazione": a_reopen["hash_dati"] == "datiA_v2" and a_reopen["j"] == 1,
    }


def sonda_rv_p2_validazione_campi_e_autorizza_dopo_esito(base: Path) -> dict:
    d = base / "rv_p2"
    d.mkdir()
    reg = d / "riserva.json"
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), 0.05, ORA)
    RV.prenota(reg, "A", "H-1", date(2005, 1, 1), date(2005, 1, 10), "q", ORA)
    # m=True (bool è sottoclasse int in Python!), n_globale=-5, hash_dati=""
    a = RV.autorizza(reg, "A", n_globale=-5, hash_dati="", ora=ORA, m=True)
    RV.rendiconta(reg, "A", "bocciata", ORA)
    # Ripetizione tecnica dopo chiusura esito="bocciata": ancora consentita!
    a_after_esito = RV.autorizza(reg, "A", n_globale=-5, hash_dati="", ora="2026-11-16T09:00:00Z", m=True)
    # Secondo j con n_globale inferiore (se prima era 20 -> ora 1)
    RV.prenota(reg, "B", "H-2", date(2005, 2, 1), date(2005, 2, 10), "q2", ORA)
    b = RV.autorizza(reg, "B", n_globale=0, hash_dati="x", ora=ORA)
    return {
        "m_bool_accettato": a["m"] is True,
        "n_globale_negativo_o_zero_accettati": (a["n_globale"], b["n_globale"]),
        "hash_dati_vuoto_accettato": a["hash_dati"] == "",
        "autorizza_dopo_esito_bocciata_passa": a_after_esito["j"] == 1,
    }


def sonda_rv_p3_parte_protetta_e_quarantena(base: Path) -> dict:
    d = base / "rv_p3"
    d.mkdir()
    reg = d / "riserva.json"
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), 0.05, ORA, protetta=(date(2005, 11, 1), date(2005, 12, 31)))
    # Adiacenza esatta: 31 ottobre ok, 1 novembre bloccato
    RV.prenota(reg, "OCT", "H-1", date(2005, 10, 20), date(2005, 10, 31), "q", ORA)
    try:
        RV.prenota(reg, "NOV_BLOCK", "H-1", date(2005, 11, 1), date(2005, 11, 2), "q", ORA)
        bordo_bloccato = False
    except ValueError:
        bordo_bloccato = True
    # Quarantena su date protette SENZA usa_protetta -> consentita!
    RV.quarantena(reg, date(2005, 11, 1), date(2005, 11, 5), "test quarantena su protetta", ORA)
    # usa_protetta=True sblocca programmativamente senza extra check
    RV.prenota(reg, "PROT_OK", "H-2", date(2005, 11, 6), date(2005, 11, 10), "q", ORA, usa_protetta=True)
    return {"bordo_protetta_bloccato": bordo_bloccato, "quarantena_su_protetta_consentita": RV.stato(reg)["giorni"]["quarantena"] == 5}


def sonda_rv_p4_ripetizione_tecnica_e_tolleranza(base: Path) -> dict:
    d = base / "rv_p4"
    d.mkdir()
    reg = d / "riserva.json"
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), 0.05, ORA)
    RV.prenota(reg, "A", "H-1", date(2005, 1, 1), date(2005, 1, 5), "q", ORA)
    a1 = RV.autorizza(reg, "A", 10, "h1", ORA, m=2)
    a2 = RV.autorizza(reg, "A", 10, "h1", "ALTRO_ORARIO", m=2)
    try:
        RV.autorizza(reg, "A", 10, "h1", ORA, m=3)  # m diverso -> bloccato
        m_diverso_bloccato = False
    except ValueError:
        m_diverso_bloccato = True
    # Verifica tolleranza 1e-15: alfa_j alterato di 5e-16 non visto da _ricostruisci
    raw = json.loads(reg.read_text(encoding="utf-8"))
    raw["eventi"][1]["alfa_j"] += 5e-16
    reg.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    st_eps = RV.stato(reg)
    return {
        "ripetizione_con_ora_diversa_ritorna_stessa_auth": a1 == a2,
        "ripetizione_m_diverso_bloccata": m_diverso_bloccato,
        "eps_5e16_tollerato": st_eps["aperture"][0]["alfa_j"] == a1["alfa_j"] + 5e-16,
    }


def sonda_rv_p5_concorrenza_processi(base: Path) -> dict:
    d = base / "rv_p5"
    d.mkdir()
    reg = d / "riserva.json"
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), 0.05, ORA)
    ctx = mp.get_context("spawn")
    bar = ctx.Barrier(8)
    q = ctx.Queue()
    procs = [ctx.Process(target=_mp_race_overlap, args=(str(reg), k, bar, q)) for k in range(8)]
    for p in procs:
        p.start()
    for p in procs:
        p.join(timeout=30)
    ris_ov = [q.get(timeout=5) for _ in range(8)]
    wins = [r for r in ris_ov if r[0] == "WIN"]

    # Ora 10 processi su date disgiunte: nessuna scrittura persa
    bar2 = ctx.Barrier(10)
    q2 = ctx.Queue()
    procs2 = [ctx.Process(target=_mp_race_disjoint, args=(str(reg), k, bar2, q2)) for k in range(10)]
    for p in procs2:
        p.start()
    for p in procs2:
        p.join(timeout=30)
    done2 = [q2.get(timeout=5) for _ in range(10)]
    st = RV.stato(reg)
    return {
        "processi_sovrapposti_vincitori": len(wins),
        "aperture_registrate": len(st["aperture"]),
        "processi_disgiunti_finiti": len(done2),
        "prenotazioni_attive_disgiunte": len(st["prenotazioni_attive"]),
    }


def sonda_rv_p6_somma_telescopica(base: Path) -> dict:
    d = base / "rv_p6"
    d.mkdir()
    reg = d / "riserva.json"
    alfa_tot = 0.05
    RV.crea(reg, date(2005, 1, 1), date(2005, 12, 31), alfa_tot, ORA)
    for k in range(1, 6):
        RV.prenota(reg, f"K{k}", f"H-{k}", date(2005, k, 1), date(2005, k, 5), "q", ORA)
        RV.autorizza(reg, f"K{k}", 10 + k, f"h{k}", ORA, m=k)
    st = RV.stato(reg)
    atteso_telescopico = alfa_tot * (5 / 6)  # sum_{j=1..5} 1/(j(j+1)) = 1 - 1/6 = 5/6
    return {
        "alfa_speso": st["alfa_speso"],
        "atteso_telescopico": atteso_telescopico,
        "diff": abs(st["alfa_speso"] - atteso_telescopico),
    }


NUOVI_MUTANTI_RV = [
    ("MRV01", "brain/laboratorio/esecuzione/riserva.py",
     "if self.protetta and a <= self.protetta[1] and b >= self.protetta[0] and not e.get(\"usa_protetta\"):",
     "if False:",
     "disattiva il blocco sulla parte protetta"),
    ("MRV02", "brain/laboratorio/esecuzione/riserva.py",
     "if b < a:",
     "if b < a and False:",
     "ammette intervallo rovesciato fine < inizio"),
    ("MRV03", "brain/laboratorio/esecuzione/riserva.py",
     "if (a[\"hash_dati\"], a[\"n_globale\"], a[\"m\"]) == (hash_dati, n_globale, m):",
     "if a[\"n_globale\"] == n_globale:",
     "accetta ripetizione tecnica anche con hash_dati o m diversi"),
    ("MRV04", "brain/laboratorio/esecuzione/riserva.py",
     "\"alfa_speso\": sum(a[\"quota_famiglia\"] for a in aperture),",
     "\"alfa_speso\": sum(a[\"alfa_j\"] for a in aperture),",
     "somma alfa_j al posto di quota_famiglia in stato()"),
    ("MRV05", "brain/laboratorio/esecuzione/riserva.py",
     "if p[\"stato\"] != \"prenotato\":\n                raise ValueError(f\"rilascio di {id_!r} impossibile: è {p['stato']}\")",
     "if False:",
     "consente rilascio anche dopo autorizzazione"),
    ("MRV06", "brain/laboratorio/esecuzione/riserva.py",
     "if e.get(\"j\") != self.j + 1:",
     "if False:",
     "non controlla sequenzialità j = self.j + 1 nella ricostruzione"),
]


def _run_mut(args):
    cod, rel, target, repl, desc = args
    with tempfile.TemporaryDirectory() as tmp:
        rad = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT / "brain", rad / "brain",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
        p = rad / rel
        orig = p.read_text(encoding="utf-8")
        assert orig.count(target) == 1, f"{cod}: target non univoco"
        p.write_text(orig.replace(target, repl, 1), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_riserva"],
            cwd=str(rad), env=dict(os.environ, PYTHONPATH=str(rad)),
            capture_output=True, text=True, timeout=120,
        )
        return {"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode, "desc": desc}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        print("RV-P1:", sonda_rv_p1_manomissioni_non_viste(base))
        print("RV-P2:", sonda_rv_p2_validazione_campi_e_autorizza_dopo_esito(base))
        print("RV-P3:", sonda_rv_p3_parte_protetta_e_quarantena(base))
        print("RV-P4:", sonda_rv_p4_ripetizione_tecnica_e_tolleranza(base))
        print("RV-P5:", sonda_rv_p5_concorrenza_processi(base))
        print("RV-P6:", sonda_rv_p6_somma_telescopica(base))
    print("=== C1 MUTANTI RISERVA (MRV01..MRV06) ===")
    with ThreadPoolExecutor(max_workers=2) as pool:
        for m in pool.map(_run_mut, NUOVI_MUTANTI_RV):
            print("MUTANTE:", m)


if __name__ == "__main__":
    main()
