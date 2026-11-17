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

Stampa SOLO conteggi, numeri di passo, ore, date e un estratto dei campi «comando o percorso» delle chiamate (con i
numeri da prezzo mascherati e la cartella personale abbreviata in ~). Non stampa mai il contenuto delle uscite né
quello dei file scritti o modificati: di quei campi dice solo il nome (rilievo R12bis-C-03, #57).

Dopo R12-bis (#56): argomenti letti da qualunque campo della chiamata; ogni record che non è testo dell'utente o del
pianificatore conta come uscita; esecuzioni anche come `bash x.sh`, `source`, `./binario`, awk, perl, node e
sottoagenti; date anche come 03/01/2005 (entrambe le letture), 03.01.2005, 2005.01.03, 20150615, timestamp Unix in
secondi o millisecondi, percorsi Dukascopy senza BID/ASK; prezzi anche con virgola decimale, separatore delle
migliaia, fino a 4 decimali, da 100 a 9.999.

Uso (sul Mac, da una copia del repository; legge soltanto):
  python3 -I -s -B brain/governance/censimento/riconta.py ~/.gemini/antigravity ~/.claude/projects > ~/Downloads/riconta.txt
"""
import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

INIZIO_RISERVA, FINE_RISERVA = date(2005, 1, 1), date(2023, 10, 31)
SENSIBILE = re.compile(r"cache_dukascopy|dati/reali|partizioni|\.bi5|xauusd|dukascopy|periodo_verifica|verifica|"
                       r"caricatore|carica\(", re.I)
ESECUZIONE = re.compile(r"(?<![\w-])(?:[\w./~-]*/)?(?:python[\d.]*|pytest|ipython|node|perl|ruby|Rscript|g?awk)(?![\w-])"
                        r"|(?<![\w./-])\./[\w./-]+"
                        r"|(?<![\w-])(?:sh|bash|zsh|source)\s+[\w./~$-]+"
                        # #77: altri esecutori; «make» solo a inizio comando (non dentro un messaggio di commit)
                        r"|(?<![\w-])(?:npx|php|deno|bun)\s+[\w./~$-]+"
                        r"|(?<![\w-])(?:npm|uv|cargo|poetry|pipenv|yarn|pnpm)\s+run(?![\w-])"
                        r"|(?:^|(?<=[;&|]))\s*make(?![\w-])", re.I | re.M)
# input a un processo già aperto (può essere codice) e sottoagenti (eseguono a loro volta)
SEMPRE_ESECUZIONE = {"send_command_input", "invoke_subagent", "Agent", "Task"}
DATA_ISO = re.compile(r"(?<!\d)((?:19|20)\d{2})-(\d{2})-(\d{2})(?!\d)")
# Dukascopy: /AAAA/MM/GG/ seguito da BID, ASK o NNh_ticks, oppure preceduto dal simbolo in maiuscolo (es. XAUUSD/)
DATA_DUKA = re.compile(r"(?<!\d)((?:19|20)\d{2})/(\d{2})/(\d{2})(?=/(?:(?i:bid|ask)|\d{2}h_ticks))"
                       r"|(?<=[A-Z]{6}/)((?:19|20)\d{2})/(\d{2})/(\d{2})(?!\d)")
# AAAA.MM.GG e AAAA/MM/GG generici (anche dentro un percorso), esclusi i casi Dukascopy qui sopra
DATA_AMG = re.compile(r"(?<![\d.])(?<![A-Z]{6}/)((?:19|20)\d{2})([./])(\d{2})\2(\d{2})(?!\d|[./]\d|/(?i:bid|ask))")
DATA_GMA = re.compile(r"(?<![\d./-])(\d{2})([./-])(\d{2})\2((?:19|20)\d{2})(?![\d./-])")
# #68; #78: attaccata a lettere, «_» o «T» è ancora una data (XAUUSD_20150615, 20231031T120000)
DATA_COMPATTA = re.compile(r"(?<!\d)(?<!\d\.)((?:19|20)\d{2})(\d{2})(\d{2})(?!\d)(?!\.\d)")
TIMESTAMP = re.compile(r"(?<![\w.])(\d{13}|\d{10})(?![\w.])")
# #79: fino a 17 decimali (rappresentazione di un float, es. 427.35000000000002)
PREZZO = re.compile(r"(?<!\d)(?<!\d[.,])(?:[1-9]\d{0,2}[.,]\d{3}[.,]\d{1,4}|[1-9]\d{2,3}[.,]\d{1,17})(?!\d|[.,]\d)")
# #80: oro 2005–2023 sotto 1.900 USD; dal 15/11/2023 (sviluppo) sopra. Euristica: non vede la riserva sopra 1.900
SOTTO_SVILUPPO, MIN_PREZZI_SENZA_DATE = 1900.0, 5
TESTO_ANTIGRAVITY = {"USER_INPUT", "PLANNER_RESPONSE"}          # tutto il resto è un'uscita
CAMPI_DA_MOSTRARE = {"CommandLine", "command", "cmd", "Path", "AbsolutePath", "path", "file_path", "TargetFile",
                     "Input", "query", "url", "Url", "pattern", "description", "toolSummary"}


def date_riserva(testo: str) -> list:
    trovate = set()

    def aggiungi(a, m, g):
        try:
            d = date(int(a), int(m), int(g))
        except ValueError:
            return
        if INIZIO_RISERVA <= d <= FINE_RISERVA:
            trovate.add(d.isoformat())
    for a, m, g in DATA_ISO.findall(testo):
        aggiungi(a, m, g)
    for t in DATA_DUKA.findall(testo):                             # negli URL di Dukascopy i mesi partono da 0
        a, m, g = t[:3] if t[0] else t[3:]
        aggiungi(a, int(m) + 1, g)
    for a, _sep, m, g in DATA_AMG.findall(testo):
        aggiungi(a, m, g)
    for x, sep, y, a in DATA_GMA.findall(testo):                   # 03/01/2005: giorno/mese e mese/giorno
        aggiungi(a, y, x)
        if sep == "/":
            aggiungi(a, x, y)
    for a, m, g in DATA_COMPATTA.findall(testo):
        aggiungi(a, m, g)
    for t in TIMESTAMP.findall(testo):
        try:
            d = datetime.fromtimestamp(int(t) / (1000 if len(t) == 13 else 1), timezone.utc).date()
        except (OverflowError, OSError, ValueError):
            continue
        if INIZIO_RISERVA <= d <= FINE_RISERVA:
            trovate.add(d.isoformat())
    return sorted(trovate)


def numeri_prezzo(testo: str) -> list:
    return PREZZO.findall(testo)


def _valore(prezzo: str) -> float:
    """Valore di un numero da prezzo («1.234,5», «1,234.5», «427.35»): l'ultimo separatore è quello decimale."""
    i = max(prezzo.rfind("."), prezzo.rfind(","))
    return float(prezzo[:i].replace(".", "").replace(",", "") + "." + prezzo[i + 1:])


def _testo(x) -> str:
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return "\n".join(_testo(y.get("text", y.get("content", y)) if isinstance(y, dict) else y) for y in x)
    return json.dumps(x, ensure_ascii=False)


def _voci(riga: dict, n: int):
    """(formato, passo, ora, chiamate [(nome, argomenti)], uscite [testo], testi [testo]) di una riga di trascrizione."""
    if "step_index" in riga or "tool_calls" in riga:
        chiamate = [(c.get("name", "?"), {k: v for k, v in c.items() if k != "name"})
                    for c in (riga.get("tool_calls") or []) if isinstance(c, dict)]
        contenuto = _testo(riga.get("content", ""))
        testi = [contenuto] if riga.get("type") in TESTO_ANTIGRAVITY else []
        uscite = [] if testi else [contenuto]
        return "antigravity", riga.get("step_index", n), riga.get("created_at", ""), chiamate, uscite, testi
    if "message" in riga:
        c = (riga.get("message") or {}).get("content")
        chiamate, uscite, testi = [], [], []
        for x in (c if isinstance(c, list) else [c]):
            if isinstance(x, dict) and x.get("type") == "tool_use":
                chiamate.append((x.get("name", "?"), {k: v for k, v in x.items() if k not in ("type", "id", "name")}))
            elif isinstance(x, dict) and x.get("type") == "tool_result":
                uscite.append(_testo(x.get("content", "")))
            elif x is not None:
                testi.append(_testo(x.get("text", "") if isinstance(x, dict) else x))
        if riga.get("toolUseResult") is not None:                  # #81: può avere l'uscita intera
            extra = _valori(riga["toolUseResult"])
            if uscite:
                uscite[-1] = uscite[-1] + "\n" + extra                 # stessa uscita, non una seconda
            else:
                uscite.append(extra)
        return "claude", n, riga.get("timestamp", ""), chiamate, uscite, testi
    return None, n, "", [], [_testo(riga)], []                     # formato sconosciuto: per prudenza, un'uscita


def _uscita(passo, ora, testo):
    d = date_riserva(testo)
    prezzi = numeri_prezzo(testo)
    p = len(prezzi)
    if not d:
        bassi = {x for x in prezzi if _valore(x) < SOTTO_SVILUPPO}
        if len(bassi) < MIN_PREZZI_SENZA_DATE:
            return None
        return {"passo": passo, "ora": ora, "date": 0, "prima": "-", "ultima": "-", "numeri_prezzo": p,
                "da_guardare": True}
    return {"passo": passo, "ora": ora, "date": len(d), "prima": d[0], "ultima": d[-1], "numeri_prezzo": p,
            "da_guardare": p >= 3 or len(d) >= 10}


def esamina_file(percorso: Path) -> dict:
    percorso = Path(percorso)
    r = {"file": str(percorso), "formato": None, "righe": 0, "righe_illeggibili": 0, "strumenti": {},
         "chiamate_sensibili": [], "esecuzioni": [], "uscite_riserva": [], "testo_con_date_riserva": 0}
    if percorso.suffix == ".log":
        r["formato"], r["righe"] = "log", 1
        u = _uscita(percorso.name, "", percorso.read_text(encoding="utf-8", errors="replace"))
        if u:
            u["da"] = "file di log"
        r["uscite_riserva"] = [u] if u else []
        return r
    strumenti = Counter()
    ultime = "(nessuna chiamata prima)"            # origine delle uscite: le chiamate più recenti (17/11)
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
            if chiamate:
                ultime = PREZZO.sub("#", "; ".join(f"{nome}: {_mostrabile(arg)}" for nome, arg in chiamate))
            for nome, arg in chiamate:
                strumenti[nome] += 1
                t = arg if isinstance(arg, str) else json.dumps(arg, ensure_ascii=False)
                voce = {"passo": passo, "ora": ora, "strumento": nome, "estratto": _mostrabile(arg)}
                parole = sorted({m.lower() for m in SENSIBILE.findall(t)})
                if parole:
                    r["chiamate_sensibili"].append(dict(voce, parole=parole))
                if nome in SEMPRE_ESECUZIONE or ESECUZIONE.search(_valori(arg)):   # #75: a capo veri, non «\\n»
                    r["esecuzioni"].append(voce)
            for t in uscite:
                u = _uscita(passo, ora, t)
                if u:
                    u["da"] = ultime                   # solo comandi e percorsi (_mostrabile), mai contenuti
                    r["uscite_riserva"].append(u)
            r["testo_con_date_riserva"] += sum(1 for t in testi if date_riserva(t))
    r["strumenti"] = dict(strumenti)
    return r


def _valori(arg) -> str:
    """Le stringhe dell'argomento, decodificate (nel JSON l'a capo è «\\n» e nasconde il comando che segue)."""
    if isinstance(arg, str):
        return arg
    if isinstance(arg, dict):
        return "\n".join(_valori(v) for v in arg.values())
    if isinstance(arg, list):
        return "\n".join(_valori(v) for v in arg)
    return str(arg)


def _mostrabile(arg) -> str:
    """Solo i campi «comando o percorso»; degli altri (contenuti di file, sostituzioni, prompt) solo il nome."""
    if not isinstance(arg, dict):
        return "[argomento non leggibile]"
    mostrati, altri = [], []

    def visita(d):
        for k, v in d.items():
            if isinstance(v, dict):
                visita(v)
            elif k in CAMPI_DA_MOSTRARE:
                mostrati.append(f"{k}={v}")
            else:
                altri.append(k)
    visita(arg)
    return " ; ".join(mostrati) + (f" [altri campi: {', '.join(sorted(set(altri)))}]" if altri else "")


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
    mancanti = [str(p) for p in x.percorsi if not p.expanduser().exists()]
    if mancanti:                                                       # #76: audit incompleto in silenzio
        print(f"ERRORE: percorsi inesistenti: {', '.join(mancanti)}", file=sys.stderr)
        return 2
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
                  f"numeri_prezzo={u['numeri_prezzo']}{'  DA GUARDARE' if u['da_guardare'] else ''}"
                  f" | da: {_breve(u.get('da', ''), casa, 220)}")
        print()
    print("TOTALE: " + ", ".join(f"{k}={tot[k]}" for k in
                                 ("file", "righe", "esecuzioni", "sensibili", "uscite_riserva", "da_guardare")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
