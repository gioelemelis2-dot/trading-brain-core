"""Riconteggio indipendente delle esecuzioni dalle trascrizioni (Antigravity di Gemini e Claude Code), 15/11/2026.

Perché esiste: il censimento di Gemini (G-20261115-03) conta le esecuzioni di Gemini con script di Gemini. Quegli script
guardano solo `run_command`, riconoscono Python solo in alcune forme e contano i comandi, non ciò che è stato VISTO.
Questo strumento, scritto da un'altra parte, legge le trascrizioni originali e conta:
- TUTTI gli strumenti usati (non solo i comandi del terminale: anche letture di file, input a processi aperti, ...);
- le chiamate che toccano dati o parole sensibili (cache, dati reali, verifica, caricatore, ...);
- le esecuzioni, anche nella forma `(cd x; python3 ...)`, `/usr/bin/python3`, `.venv/bin/python`, script di shell, e ogni
  input mandato a un processo già aperto;
- le USCITE (risultati dei comandi, log dei task) che contengono date della riserva sigillata (2005-01-01 → 2023-10-31)
  e quanti numeri hanno la forma di un prezzo dell'oro di quegli anni: è il controllo che conta per la riserva.
Il testo libero (messaggi, ragionamenti) è contato a parte: citare il periodo non è vederne i dati.

Stampa SOLO conteggi, numeri di passo, ore, date e un estratto dei COMANDI (con i numeri da prezzo mascherati e la
cartella personale abbreviata in ~). Non stampa mai il contenuto delle uscite.

Uso (sul Mac, da una copia del repository; legge soltanto):
  python3 -I -s -B brain/governance/censimento/riconta.py ~/.gemini/antigravity ~/.claude/projects > ~/Downloads/riconta.txt
"""
import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

INIZIO_RISERVA, FINE_RISERVA = date(2005, 1, 1), date(2023, 10, 31)
SENSIBILE = re.compile(r"cache_dukascopy|dati/reali|partizioni|\.bi5|xauusd|dukascopy|periodo_verifica|verifica|"
                       r"caricatore|carica\(", re.I)
ESECUZIONE = re.compile(r"(?<![\w-])(?:[\w./~-]*/)?(?:python[\d.]*|pytest|ipython)(?![\w-])"
                        r"|(?:^|[\s;&|(])\./[\w./-]+\.py\b"
                        r"|(?:^|[\s;&|(])(?:sh|bash|zsh)\s+[\w./~$-]+", re.I)
SEMPRE_ESECUZIONE = {"send_command_input"}          # input a un processo già aperto: può essere codice
DATA_ISO = re.compile(r"(?<!\d)((?:19|20)\d{2})-(\d{2})-(\d{2})(?!\d)")
DATA_DUKA = re.compile(r"(?<!\d)((?:19|20)\d{2})/(\d{2})/(\d{2})/(?:BID|ASK)", re.I)
PREZZO = re.compile(r"(?<![\d.])(?:[4-9]\d{2}|1\d{3}|20\d{2})\.\d{1,3}(?![\d.])")
USCITE_ANTIGRAVITY = {"GENERIC", "SYSTEM_MESSAGE"}


def date_riserva(testo: str) -> list:
    trovate = set()
    for rx, scarto in ((DATA_ISO, 0), (DATA_DUKA, 1)):            # negli URL di Dukascopy i mesi partono da 0
        for a, m, g in rx.findall(testo):
            try:
                d = date(int(a), int(m) + scarto, int(g))
            except ValueError:
                continue
            if INIZIO_RISERVA <= d <= FINE_RISERVA:
                trovate.add(d.isoformat())
    return sorted(trovate)


def _testo(x) -> str:
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return "\n".join(_testo(y.get("text", y.get("content", y)) if isinstance(y, dict) else y) for y in x)
    return json.dumps(x, ensure_ascii=False)


def _voci(riga: dict, n: int):
    """(formato, passo, ora, chiamate [(nome, argomenti)], uscite [testo], testi [testo]) di una riga di trascrizione."""
    if "step_index" in riga or "tool_calls" in riga:
        chiamate = [(c.get("name", "?"), c.get("args") or {}) for c in (riga.get("tool_calls") or [])]
        contenuto = _testo(riga.get("content", ""))
        uscite = [contenuto] if riga.get("type") in USCITE_ANTIGRAVITY else []
        testi = [] if uscite else [contenuto]
        return "antigravity", riga.get("step_index", n), riga.get("created_at", ""), chiamate, uscite, testi
    if "message" in riga:
        c = (riga.get("message") or {}).get("content")
        chiamate, uscite, testi = [], [], []
        for x in (c if isinstance(c, list) else [c]):
            if isinstance(x, dict) and x.get("type") == "tool_use":
                chiamate.append((x.get("name", "?"), x.get("input") or {}))
            elif isinstance(x, dict) and x.get("type") == "tool_result":
                uscite.append(_testo(x.get("content", "")))
            elif x is not None:
                testi.append(_testo(x.get("text", "") if isinstance(x, dict) else x))
        return "claude", n, riga.get("timestamp", ""), chiamate, uscite, testi
    return None, n, "", [], [], [_testo(riga)]


def _uscita(passo, ora, testo):
    d = date_riserva(testo)
    if not d:
        return None
    p = len(PREZZO.findall(testo))
    return {"passo": passo, "ora": ora, "date": len(d), "prima": d[0], "ultima": d[-1], "numeri_prezzo": p,
            "da_guardare": p >= 3 or len(d) >= 10}


def esamina_file(percorso: Path) -> dict:
    percorso = Path(percorso)
    r = {"file": str(percorso), "formato": None, "righe": 0, "righe_illeggibili": 0, "strumenti": {},
         "chiamate_sensibili": [], "esecuzioni": [], "uscite_riserva": [], "testo_con_date_riserva": 0}
    if percorso.suffix == ".log":
        r["formato"], r["righe"] = "log", 1
        u = _uscita(percorso.name, "", percorso.read_text(encoding="utf-8", errors="replace"))
        r["uscite_riserva"] = [u] if u else []
        return r
    strumenti = Counter()
    with open(percorso, encoding="utf-8", errors="replace") as f:
        for n, linea in enumerate(f, 1):
            if not linea.strip():
                continue
            r["righe"] += 1
            try:
                riga = json.loads(linea)
            except ValueError:
                r["righe_illeggibili"] += 1
                continue
            if not isinstance(riga, dict):
                continue
            formato, passo, ora, chiamate, uscite, testi = _voci(riga, n)
            r["formato"] = r["formato"] or formato
            for nome, arg in chiamate:
                strumenti[nome] += 1
                t = arg if isinstance(arg, str) else json.dumps(arg, ensure_ascii=False)
                voce = {"passo": passo, "ora": ora, "strumento": nome, "estratto": t}
                parole = sorted({m.lower() for m in SENSIBILE.findall(t)})
                if parole:
                    r["chiamate_sensibili"].append(dict(voce, parole=parole))
                if nome in SEMPRE_ESECUZIONE or ESECUZIONE.search(t):
                    r["esecuzioni"].append(voce)
            for t in uscite:
                u = _uscita(passo, ora, t)
                if u:
                    r["uscite_riserva"].append(u)
            r["testo_con_date_riserva"] += sum(1 for t in testi if date_riserva(t))
    r["strumenti"] = dict(strumenti)
    return r


def _breve(t: str, casa: str, n: int = 140) -> str:
    t = PREZZO.sub("#", t.replace(casa, "~")).replace("\n", " ⏎ ")
    return t[:n] + ("…" if len(t) > n else "")


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("percorsi", nargs="+", type=Path, help="cartelle o file di trascrizioni (.jsonl) e log (.log)")
    a.add_argument("--max-righe", type=int, default=400, help="righe massime per elenco, per file")
    x = a.parse_args(argv)
    casa = str(Path.home())
    file = []
    for p in x.percorsi:
        p = p.expanduser()
        file += [p] if p.is_file() else sorted(q for q in p.rglob("*") if q.is_file() and q.suffix in (".jsonl", ".log"))
    print("RICONTEGGIO (governance/censimento/riconta.py): solo conteggi, passi, ore, date ed estratti dei comandi "
          "(numeri da prezzo mascherati con #). Nessun contenuto delle uscite.")
    print(f"Riserva: {INIZIO_RISERVA} → {FINE_RISERVA}. File esaminati: {len(file)}\n")
    tot = Counter()
    for f in file:
        r = esamina_file(f)
        guardare = [u for u in r["uscite_riserva"] if u["da_guardare"]]
        tot.update(file=1, righe=r["righe"], esecuzioni=len(r["esecuzioni"]), sensibili=len(r["chiamate_sensibili"]),
                   uscite_riserva=len(r["uscite_riserva"]), da_guardare=len(guardare))
        if not (r["strumenti"] or r["uscite_riserva"] or r["righe_illeggibili"] or r["testo_con_date_riserva"]):
            continue
        print(f"== {_breve(r['file'], casa, 400)} [{r['formato']}] righe={r['righe']} illeggibili={r['righe_illeggibili']}")
        if r["strumenti"]:
            print("  strumenti: " + ", ".join(f"{k}={v}" for k, v in sorted(r["strumenti"].items(), key=lambda kv: -kv[1])))
        print(f"  esecuzioni={len(r['esecuzioni'])}  chiamate sensibili={len(r['chiamate_sensibili'])}  "
              f"uscite con date della riserva={len(r['uscite_riserva'])} (DA GUARDARE {len(guardare)})  "
              f"testo libero con date della riserva={r['testo_con_date_riserva']}")
        for c in r["chiamate_sensibili"][:x.max_righe]:
            print(f"  S [{c['passo']}] {c['ora']} {c['strumento']} {','.join(c['parole'])} | {_breve(c['estratto'], casa)}")
        for u in r["uscite_riserva"][:x.max_righe]:
            print(f"  U [{u['passo']}] {u['ora']} date={u['date']} {u['prima']}..{u['ultima']} "
                  f"numeri_prezzo={u['numeri_prezzo']}{'  DA GUARDARE' if u['da_guardare'] else ''}")
        print()
    print("TOTALE: " + ", ".join(f"{k}={tot[k]}" for k in
                                 ("file", "righe", "esecuzioni", "sensibili", "uscite_riserva", "da_guardare")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
