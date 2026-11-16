"""Mandato R12-bis (Compito C): attacco a brain/governance/censimento/riconta.py.

Usa ESCLUSIVAMENTE trascrizioni FINTE costruite in TemporaryDirectory().
Non apre né tocca mai trascrizioni reali di Antigravity o Claude.

Sonde:
- C-P1: Strumenti con argomenti in campi diversi da args/input (es. arguments dict/str, params) e uscite annidate.
- C-P2: Esecuzioni scritte in forme diverse da python/pytest/ipython/./x.py/send_command_input
        (bash script.sh, source x.sh, binario ./eseguibile senza .py, invoke_subagent).
- C-P3: Date riserva non viste (03/01/2005, 2005.01.03, 20150615, timestamp Unix, path Dukascopy senza /BID|ASK
        e bug mese 0-based Dukascopy 2015/00/03/BID rifiutato da date(2015, 0, 3)).
- C-P4: Prezzi non mascherati né riconosciuti da PREZZO (virgola decimale 1850,75, separatore migliaia
        1,850.75 / 1.850,75, oro >= 2100.00 come 2650.45, 4 decimali 1850.1234, sotto 400 come 395.50).
- C-P5: Perdita di contenuti e prezzi non mascherati sullo stdout di riconta.main (_breve su chiamate SENSIBILE).

Nuovi mutanti (MRC01..MRC04) su riconta.py in copia temporanea.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.governance.censimento import riconta as R  # noqa: E402


def _scrivi_jsonl(percorso: Path, righe: list) -> None:
    percorso.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in righe) + "\n", encoding="utf-8")


def sonda_c_p1_campi_diversi_e_uscite_annidate(base: Path) -> dict:
    f1 = base / "fake_p1.jsonl"
    righe = [
        # Antigravity-like step con 'arguments' e 'params' invece di 'args'
        {
            "step_index": 0,
            "type": "PLANNER_RESPONSE",
            "tool_calls": [
                {"name": "run_command", "arguments": {"CommandLine": "python3 run.py --cache cache_dukascopy --data 2010-05-03"}},
                {"name": "read_file", "params": {"Path": "/repo/brain/dati/reali/cache_dukascopy/2012-06-01.bi5"}},
            ],
        },
        # Claude-like assistant con dict annidati in arguments/args invece di input
        {
            "type": "assistant",
            "message": {"content": [
                {"type": "tool_use", "name": "Bash", "args": {"command": "python3 x.py 2011-07-04 cache_dukascopy"}}
            ]},
        },
        # Uscita Claude annidata in blocchi strutturati dict dentro list e type diverso
        {
            "type": "user",
            "message": {"content": [
                {"type": "tool_result", "content": [{"type": "json", "data": {"msg": "cache_dukascopy date 2014-08-15"}}]}
            ]},
        },
        # Uscita Antigravity con type non in {"SYSTEM_MESSAGE", "GENERIC"}
        {
            "step_index": 1,
            "type": "TOOL_OUTPUT",
            "content": "cache_dukascopy 2015-09-21 1234.56",
        },
    ]
    _scrivi_jsonl(f1, righe)
    res = R.esamina_file(f1)
    tot_str = sum(res["strumenti"].values())
    return {
        "strumenti_contati": tot_str,
        "esecuzioni_rilevate": len(res["esecuzioni"]),
        "sensibili_rilevate": len(res["chiamate_sensibili"]),
        "uscite_riserva": res["uscite_riserva"],
        "perse_arguments_params_e_uscite_annidate": (
            tot_str == 0 and len(res["uscite_riserva"]) == 0
        ),
    }


def sonda_c_p2_altre_sintassi_esecuzione(base: Path) -> dict:
    f2 = base / "fake_p2.jsonl"
    righe = [
        {"step_index": 0, "type": "PLANNER_RESPONSE", "tool_calls": [
            {"name": "run_command", "args": {"CommandLine": "bash /tmp/lancia.sh cache_dukascopy 2012-03-04"}},
            {"name": "run_command", "args": {"CommandLine": "source /tmp/run.sh && ./eseguibile_compilato"}},
            {"name": "run_command", "args": {"CommandLine": "awk '{print}' brain/dati/reali/xauusd.csv"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Prompt": "leggi cache_dukascopy 2018-04-05"}},
        ]},
    ]
    _scrivi_jsonl(f2, righe)
    res = R.esamina_file(f2)
    return {
        "strumenti_contati": sum(res["strumenti"].values()),
        "esecuzioni_rilevate": len(res["esecuzioni"]),
        "sensibili_rilevate": len(res["chiamate_sensibili"]),
        "esecuzioni_non_viste_tutte_e_4": len(res["esecuzioni"]) == 0,
    }


def sonda_c_p3_date_non_iso_e_duka(base: Path) -> dict:
    testi = {
        "dd_mm_yyyy": "dati dal 03/01/2005 al 31/10/2023",
        "yyyy_dot_mm_dot_dd": "periodo 2005.01.03 .. 2023.10.31",
        "yyyymmdd_compatto": "range 20150615..20160720",
        "unix_timestamp": "ts=1434326400 ms=1434326400000",
        "duka_bi5_senza_bid_ask": "cache_dukascopy/XAUUSD/2015/05/15/12h_ticks.bi5",
        "duka_mese_00_gennaio_bid": "XAUUSD/2015/00/03/BID",  # mese 00 = gennaio in Dukascopy!
        "duka_mese_05_giugno_off_by_one": "XAUUSD/2015/05/03/BID",
    }
    ris_date = {k: R.date_riserva(v) for k, v in testi.items()}
    f3 = base / "fake_p3.jsonl"
    _scrivi_jsonl(f3, [{
        "step_index": 0, "type": "SYSTEM_MESSAGE",
        "content": "03/01/2005 2005.01.03 20150615 ts=1434326400 XAUUSD/2015/00/03/BID XAUUSD/2015/05/15/12h_ticks.bi5",
    }])
    res = R.esamina_file(f3)
    return {"date_riserva_per_formato": ris_date, "uscite_riserva": res["uscite_riserva"]}


def sonda_c_p4_prezzi_non_coperti() -> dict:
    campioni = [
        "1850,75",      # virgola decimale
        "1,850.75",     # separatore migliaia US (solo 850.75 viene coperto -> resta '1,#')
        "1.850,75",     # separatore migliaia IT + virgola
        "2650.45",      # prezzo oro 2024-2026 (>= 2100)
        "1850.1234",    # 4 decimali
        "395.50",       # sotto 400
    ]
    dopo_breve = {c: R._breve(f"prezzo={c}", "/no/home") for c in campioni}
    non_mascherati = [c for c, b in dopo_breve.items() if b != "prezzo=#"]
    return {"dopo_breve": dopo_breve, "non_completamente_mascherati": non_mascherati}


def sonda_c_p5_leak_contenuto_e_prezzi_su_stdout(base: Path) -> dict:
    f5 = base / "fake_p5.jsonl"
    _scrivi_jsonl(f5, [{
        "step_index": 0, "type": "PLANNER_RESPONSE",
        "tool_calls": [{
            "name": "write_file",
            "args": {
                "Path": "/repo/brain/note.md",
                "Content": "cache_dukascopy 2012-05-04 prezzo_virgola=1850,75 prezzo_2025=2650.45 SEGRETO_IN_CHIARO",
            },
        }],
    }])
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = R.main([str(f5)])
    txt = out.getvalue()
    return {
        "rc": rc,
        "stampa_1850_75_in_chiaro": "1850,75" in txt,
        "stampa_2650_45_in_chiaro": "2650.45" in txt,
        "stampa_contenuto_write_file_in_chiaro": "SEGRETO_IN_CHIARO" in txt,
        "estratto_stampato": [line for line in txt.splitlines() if line.strip().startswith("S ")],
    }


NUOVI_MUTANTI_C = [
    (
        "MRC01",
        "brain/governance/censimento/riconta.py",
        r'SEMPRE_ESECUZIONE\s*=\s*\{"send_command_input"\}',
        "SEMPRE_ESECUZIONE = set()",
        "non classifica più send_command_input come esecuzione",
    ),
    (
        "MRC02",
        "brain/governance/censimento/riconta.py",
        r'INIZIO_RISERVA,\s*FINE_RISERVA\s*=\s*date\(2005,\s*1,\s*1\),\s*date\(2023,\s*10,\s*31\)',
        "INIZIO_RISERVA, FINE_RISERVA = date(2010, 1, 1), date(2023, 10, 31)",
        "restringe INIZIO_RISERVA dal 2005 al 2010",
    ),
    (
        "MRC03",
        "brain/governance/censimento/riconta.py",
        r'USCITE_ANTIGRAVITY\s*=\s*\{"GENERIC",\s*"SYSTEM_MESSAGE"\}',
        "USCITE_ANTIGRAVITY = set()",
        "ignora le uscite tool di Antigravity (GENERIC/SYSTEM_MESSAGE)",
    ),
    (
        "MRC04",
        "brain/governance/censimento/riconta.py",
        r'PREZZO\.sub\("#",',
        "(lambda _x, s: s)(",
        "disattiva il mascheramento # in _breve (leak completo di tutti i prezzi sullo stdout)",
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
        m = re.search(pattern, orig)
        if not m:
            return {"codice": cod, "stato": "ERR_MATCH", "rc": -1, "desc": desc}
        mut = orig[:m.start()] + repl + orig[m.end():]
        p.write_text(mut, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(radice))
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.governance.censimento.test_riconta"],
            cwd=str(radice), env=env, capture_output=True, text=True, timeout=120,
        )
        return {"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode, "desc": desc}


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        print("C-P1:", sonda_c_p1_campi_diversi_e_uscite_annidate(base))
        print("C-P2:", sonda_c_p2_altre_sintassi_esecuzione(base))
        print("C-P3:", sonda_c_p3_date_non_iso_e_duka(base))
        print("C-P4:", sonda_c_p4_prezzi_non_coperti())
        print("C-P5:", sonda_c_p5_leak_contenuto_e_prezzi_su_stdout(base))
    print("=== C MUTANTI (MRC01..MRC04) ===")
    with ThreadPoolExecutor(max_workers=2) as pool:
        for m in pool.map(_run_mut, NUOVI_MUTANTI_C):
            print("MUTANTE:", m)


if __name__ == "__main__":
    main()
