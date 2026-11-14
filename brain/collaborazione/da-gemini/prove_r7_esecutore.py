"""Prove riproducibili e verifica di nuovi mutanti per la revisione R7 (feat/esecutore-h002)."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
import contextlib
import io
import json
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.esecuzione import caricatore as C  # noqa: E402
from brain.laboratorio.esecuzione import criteri as K  # noqa: E402
from brain.laboratorio.esecuzione import esegui_h002 as E  # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S  # noqa: E402
from brain.laboratorio.esecuzione import sintetico as SN  # noqa: E402

ORA = "2026-11-15T03:00:00Z"


def prova_1_verifica_su_variante_bocciata_o_senza_sviluppo() -> dict:
    """Dimostra che esegui_h002.main accetta --modalita verifica anche senza sviluppo o con sviluppo bocciato."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg = d / "reg.json"
        cache = d / "cache"
        rap_sv = d / "sviluppo.md"
        rap_vf = d / "verifica.md"
        bid_s, ask_s = SN.mercato(date(2024, 1, 1), 120, seme=3, sd=0.7)  # casuale -> sviluppo boccia
        SN.scrivi_cache(bid_s, cache / "XAUUSD")
        SN.scrivi_cache(ask_s, cache / "XAUUSD_ASK")
        bid_v, ask_v = SN.mercato(date(2010, 1, 1), 120, seme=4, sd=0.7, spinta=0.01)
        SN.scrivi_cache(bid_v, cache / "XAUUSD")
        SN.scrivi_cache(ask_v, cache / "XAUUSD_ASK")

        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc_sv = E.main([
                "--modalita", "sviluppo", "--inizio", "2024-01-01", "--fine", "2024-04-29",
                "--rapporto", str(rap_sv), "--registro", str(reg), "--scheda", str(scheda),
                "--cache", str(cache), "--ora", ORA, "--ripetizioni", "50",
            ])
            rc_vf = E.main([
                "--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-04-29",
                "--rapporto", str(rap_vf), "--registro", str(reg), "--scheda", str(scheda),
                "--cache", str(cache), "--ora", ORA,
            ])
        dati = S.leggi(reg)
        prom_sv = {e["variante"]: e["promossa"] for e in dati["esecuzioni"] if e["ruolo"] == "sviluppo"}
        esec_vf = [e for e in dati["esecuzioni"] if e["ruolo"] == "verifica"]
        return {"rc_sv": rc_sv, "prom_sviluppo": prom_sv, "rc_verifica_su_bocciata": rc_vf, "esec_verifica": len(esec_vf)}


def prova_2_split_verifica_riduce_varianza_dsr() -> dict:
    """Dimostra che chiamare verifica separatamente (--varianti V-T poi V-S) evita sharpe_prove -> V=1/(T-1)."""
    # Costruiamo 2 serie di trade in verifica con Sharpe diversi (V-T leggermente sopra soglia a V=1/(T-1), sotto con variance([SR1, SR2]))
    tr_vt = [{"data": date(2005 + k // 200, 1 + (k % 12), 1 + (k % 28)), "lato": "acquisto",
              "r": 1.0 if (k % 11 != 0) else -9.0} for k in range(1000)]
    # Con sr fisso 0.08 e V-S disperso (-0.40), mostriamo l'effetto su K.verifica e su esegui_verifica
    import random
    rng = random.Random(7)
    tr_a = [{"data": date(2005 + k // 200, 1 + (k % 12), 1 + (k % 28)), "lato": "acquisto",
             "r": 0.13 + rng.gauss(0.0, 1.0)} for k in range(1000)]
    dsr_singolo = K.verifica(tr_a, n_prove=2, sharpe_prove=[])["dsr"]
    dsr_congiunto = K.verifica(tr_a, n_prove=2, sharpe_prove=[-0.40])["dsr"]
    return {"dsr_chiamata_singola": dsr_singolo, "dsr_chiamata_congiunta": dsr_congiunto,
            "promossa_singola": dsr_singolo >= 0.95, "promossa_congiunta": dsr_congiunto >= 0.95}


def prova_3_sigillo_con_n1_accettato_da_esecutore() -> dict:
    """Dimostra che esegui_h002.main accetta un sigillo con 1 sola variante (N=1 invece di 2)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg = d / "reg.json"
        cache = d / "cache"
        rap = d / "verifica.md"
        bid, ask = SN.mercato(date(2010, 1, 1), 60, seme=4, sd=0.7, spinta=0.01)
        SN.scrivi_cache(bid, cache / "XAUUSD")
        SN.scrivi_cache(ask, cache / "XAUUSD_ASK")
        S.sigilla(reg, "H-002", scheda, ["V-T"], ORA)  # N=1 invece di ["V-T", "V-S"]!
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = E.main([
                "--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-02-28",
                "--rapporto", str(rap), "--registro", str(reg), "--scheda", str(scheda),
                "--cache", str(cache), "--ora", ORA,
            ])
        return {"rc": rc, "n_prove_usato": S.n_prove(S.leggi(reg))}


def prova_4_cache_vuota_brucia_verifica() -> dict:
    """Dimostra che --cache errata/vuota brucia irreversibilmente l'unica verifica disponibile."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg = d / "reg.json"
        cache_vuota = d / "cache_inesistente"
        rap = d / "vf.md"
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc1 = E.main([
                "--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-02-28",
                "--rapporto", str(rap), "--registro", str(reg), "--scheda", str(scheda),
                "--cache", str(cache_vuota), "--ora", ORA,
            ])
            rc2 = E.main([
                "--modalita", "verifica", "--varianti", "V-T", "--inizio", "2010-01-01", "--fine", "2010-02-28",
                "--rapporto", str(rap), "--registro", str(reg), "--scheda", str(scheda),
                "--cache", str(cache_vuota), "--ora", ORA,
            ])
        return {"rc_vuota": rc1, "rc_secondo_tentativo": rc2, "esecuzioni": S.leggi(reg)["esecuzioni"]}


def prova_5_verifica_anni_senza_trade_ignorati_da_esegui() -> dict:
    """Dimostra che esegui_verifica non passa anni=... a K.verifica -> falsi positivi sulla quota anni."""
    tr = [{"data": date(a, 1, 2), "lato": "acquisto", "r": 1.0 if a <= 2010 else -0.2}
          for a in range(2005, 2015)]  # 10 anni con trade: 6 positivi (2005..2010) / 4 negativi -> 60%
    # Se il periodo di verifica va dal 2005 al 2023 (19 anni), 9 anni (2015..2023) sono senza trade!
    senza_anni = K.verifica(tr, n_prove=1)
    con_anni = K.verifica(tr, n_prove=1, anni=range(2005, 2024))
    q_senza = [c["valore"] for c in senza_anni["criteri"] if c["nome"].startswith("quota")][0]
    p_senza = [c["passa"] for c in senza_anni["criteri"] if c["nome"].startswith("quota")][0]
    q_con = [c["valore"] for c in con_anni["criteri"] if c["nome"].startswith("quota")][0]
    p_con = [c["passa"] for c in con_anni["criteri"] if c["nome"].startswith("quota")][0]
    u5_senza = [c["valore"] for c in senza_anni["criteri"] if c["nome"].startswith("ultimi 5")][0]
    return {"senza_anni": (q_senza, p_senza), "con_anni_2005_2023": (q_con, p_con), "ultimi_5_ancorati_a_2014": u5_senza}


def prova_6_confronto_casuale_asimmetria_giorni() -> dict:
    """Dimostra che confrontare r_medio su tutti i trade con esiti su S∩C∩V produce falsi positivi (A2)."""
    # 100 giorni comuni dove strategia = +0.02, acquisto = +0.50, vendita = -0.30 (media lato casuale = +0.10)
    # più 50 giorni in cui solo strategia entra (non coperti da benchmark su entrambi i lati) con R = +0.50:
    # r_medio su tutti i 150 giorni = (100*0.02 + 50*0.50)/150 = +0.1800 (batte p95 ≈ 0.164 di [+0.50, -0.30]),
    # mentre sui 100 giorni comuni r_strategia = +0.02 (sotto media casuale +0.10!).
    esiti_comuni = [(0.50, -0.30)] * 100
    r_su_tutti = (100 * 0.02 + 50 * 0.50) / 150.0
    r_su_comuni = 0.02
    c_tutti = K.confronto_casuale(esiti_comuni, r_su_tutti, ripetizioni=1000, seme=42)
    c_comuni = K.confronto_casuale(esiti_comuni, r_su_comuni, ripetizioni=1000, seme=42)
    return {
        "r_su_tutti": round(r_su_tutti, 6),
        "r_su_comuni": r_su_comuni,
        "p95_casuale_comuni": round(c_tutti["percentile_95"], 6),
        "passa_su_tutti": c_tutti["sopra"],
        "passa_su_comuni": c_comuni["sopra"],
    }


def prova_7_embargo_leggibile() -> dict:
    """Verifica che i giorni di embargo (2023-11-01..2023-11-14) sono leggibili in modalita verifica (A8)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        scheda = d / "H-002.md"
        scheda.write_text("# H-002\n", encoding="utf-8")
        reg = d / "reg.json"
        cache = d / "cache"
        bid, ask = SN.mercato(date(2023, 11, 1), 20, seme=9, sd=0.7)
        SN.scrivi_cache(bid, cache / "XAUUSD")
        SN.scrivi_cache(ask, cache / "XAUUSD_ASK")
        S.sigilla(reg, "H-002", scheda, ["V-T", "V-S"], ORA)
        _, _, info = C.carica(
            cache / "XAUUSD", cache / "XAUUSD_ASK",
            date(2023, 11, 1), date(2023, 11, 14), "verifica", reg, "H-002", scheda,
        )
        return {"minuti_bid_embargo_letti_in_verifica": info["minuti_bid"]}


NUOVI_MUTANTI = [
    (
        "MG01",
        "brain/laboratorio/esecuzione/esegui_h002.py",
        "        altri = [s for k, s in sharpe.items() if k != v and s is not None]",
        "        altri = []",
        "azzera sharpe_prove nella verifica (V = 1/(T-1) sempre)",
    ),
    (
        "MG02",
        "brain/laboratorio/esecuzione/criteri.py",
        "            v = max(v, variance(list(sharpe_prove) + [sr]))",
        "            v = variance(list(sharpe_prove) + [sr])",
        "toglie max(1/(T-1), variance(...)) quando le varianti hanno Sharpe quasi uguali",
    ),
    (
        "MG03",
        "brain/laboratorio/esecuzione/criteri.py",
        "        _criterio(\"R medio netto\", r, \"> 0\", r is not None and r > 0),",
        "        _criterio(\"R medio netto\", r, \"> 0\", r is not None and r >= 0),",
        "cambia > 0 in >= 0 per R medio netto in verifica",
    ),
    (
        "MG04",
        "brain/laboratorio/esecuzione/criteri.py",
        "                  cumulato is not None and cumulato > 0),\n"
        "        _criterio(\"drawdown massimo (R)\", dd, f\"< {dd_max}\", dd is not None and dd < dd_max),",
        "                  cumulato is not None and cumulato > 0),\n"
        "        _criterio(\"drawdown massimo (R)\", dd, f\"< {dd_max}\", dd is not None and dd <= dd_max),",
        "cambia < dd_max in <= dd_max in verifica",
    ),
    (
        "MG05",
        "brain/laboratorio/esecuzione/criteri.py",
        "    rs = [x[\"r\"] for x in sorted(tr, key=lambda x: x[\"data\"])]",
        "    rs = [x[\"r\"] for x in tr]",
        "toglie ordinamento cronologico dei trade in K.verifica (dd errato su input non ordinato)",
    ),
    (
        "MG06",
        "brain/laboratorio/esecuzione/criteri.py",
        "        v = 1.0 / (len(rs) - 1)",
        "        v = 1.0 / len(rs)",
        "cambia 1/(T-1) in 1/T nella varianza minima di DSR",
    ),
    (
        "MG07",
        "brain/laboratorio/esecuzione/criteri.py",
        "        _criterio(f\"ultimi {ultimi} anni solari, risultato cumulato\", cumulato, \"> 0\",\n                  cumulato is not None and cumulato > 0),",
        "        _criterio(f\"ultimi {ultimi} anni solari, risultato cumulato\", cumulato, \"> 0\",\n                  cumulato is not None and cumulato >= 0),",
        "cambia > 0 in >= 0 sul risultato cumulato degli ultimi 5 anni",
    ),
]


def _run_one_mutante(args):
    import os
    import shutil
    import subprocess
    cod, rel, target, repl, desc = args
    with tempfile.TemporaryDirectory() as tmp:
        radice = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT / "brain", radice / "brain",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "da-gemini"))
        p = radice / rel
        orig = p.read_text(encoding="utf-8")
        assert orig.count(target) == 1, f"{cod}: target non univoco in {rel}"
        p.write_text(orig.replace(target, repl, 1), encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(radice))
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_esecuzione", "brain.laboratorio.tests.test_esegui_h002"],
            cwd=str(radice), env=env, capture_output=True, text=True, timeout=240,
        )
        stato = "VIVO" if proc.returncode == 0 else "UCCISO"
        return {"codice": cod, "stato": stato, "rc": proc.returncode, "desc": desc}


def esegui_nuovi_mutanti() -> list:
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(pool.map(_run_one_mutante, NUOVI_MUTANTI))


def main() -> None:
    print("P1:", prova_1_verifica_su_variante_bocciata_o_senza_sviluppo())
    print("P2:", prova_2_split_verifica_riduce_varianza_dsr())
    print("P3:", prova_3_sigillo_con_n1_accettato_da_esecutore())
    print("P4:", prova_4_cache_vuota_brucia_verifica())
    print("P5:", prova_5_verifica_anni_senza_trade_ignorati_da_esegui())
    print("P6:", prova_6_confronto_casuale_asimmetria_giorni())
    print("P7:", prova_7_embargo_leggibile())
    for m in esegui_nuovi_mutanti():
        print("MUTANTE:", m)


if __name__ == "__main__":
    main()
