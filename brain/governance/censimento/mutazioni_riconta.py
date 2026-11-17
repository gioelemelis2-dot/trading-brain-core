"""Mutation testing del riconteggio (governance/censimento/riconta.py). Ogni mutante è una copia della cartella con UN
difetto; la copia non mutata deve superare i test; ogni sostituzione deve comparire una sola volta.
Uso (dalla radice del repository): python3 -s -B brain/governance/censimento/mutazioni_riconta.py <cartella> [processi]
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if len(sys.argv) not in (2, 3):
    sys.exit(__doc__)
QUI, OUT = Path(__file__).resolve().parent, Path(sys.argv[1]).resolve()
PROCESSI = int(sys.argv[2]) if len(sys.argv) == 3 else 2
M = {
    "Z01 solo run_command": ('                strumenti[nome] += 1\n', '                if nome != "run_command":\n                    continue\n                strumenti[nome] += 1\n'),
    "Z02 input a processo non contato": ('SEMPRE_ESECUZIONE = {"send_command_input", "invoke_subagent", "Agent", "Task"}', 'SEMPRE_ESECUZIONE = {"invoke_subagent", "Agent", "Task"}'),
    "Z03 python solo a inizio parola": ('(?<![\\w-])(?:[\\w./~-]*/)?(?:python', '(?:^|\\s)(?:python'),
    "Z04 mesi Dukascopy da 1": ('        aggiungi(a, int(m) + 1, g)', '        aggiungi(a, m, g)'),
    "Z05 fine riserva esclusa": ('        if INIZIO_RISERVA <= d <= FINE_RISERVA:\n            trovate.add(d.isoformat())\n    for a, m, g in DATA_ISO', '        if INIZIO_RISERVA <= d < FINE_RISERVA:\n            trovate.add(d.isoformat())\n    for a, m, g in DATA_ISO'),
    "Z06 testo trattato come uscita": ('        testi = [contenuto] if riga.get("type") in TESTO_ANTIGRAVITY else []', '        testi = []'),
    "Z07 log dei task ignorati": ('    if percorso.suffix == ".log":', '    if False:'),
    "Z08 prezzi non mascherati": ('    t = PREZZO.sub("#", t.replace(casa, "~"))', '    t = t.replace(casa, "~")'),
    "Z09 soglia prezzi": ('"da_guardare": p >= 3 or', '"da_guardare": p >= 30 or'),
    "Z10 tool_result ignorato": ('                uscite.append(_testo(x.get("content", "")))', '                pass'),
    "Z11 righe illeggibili non contate": ('                r["righe_illeggibili"] += 1\n', ''),
    "Z13 testo dell'uscita conservato": ('            "da_guardare": p >= 3 or len(d) >= 10}', '            "da_guardare": p >= 3 or len(d) >= 10, "testo": testo[:50]}'),
    "Z14 solo il campo args": ('        chiamate = [(c.get("name", "?"), {k: v for k, v in c.items() if k != "name"})', '        chiamate = [(c.get("name", "?"), c.get("args") or {})'),
    "Z15 solo il campo input (Claude)": ('chiamate.append((x.get("name", "?"), {k: v for k, v in x.items() if k not in ("type", "id", "name")}))', 'chiamate.append((x.get("name", "?"), x.get("input") or {}))'),
    "Z16 solo GENERIC come uscita": ('        uscite = [] if testi else [contenuto]', '        uscite = [contenuto] if riga.get("type") in ("GENERIC", "SYSTEM_MESSAGE") else []'),
    "Z17 bash solo dopo spazio": ('|(?<![\\w-])(?:sh|bash|zsh|source)\\s+', '|(?:^|[\\s;&|(])(?:sh|bash|zsh|source)\\s+'),
    "Z18 ./binario non visto": ('                        r"|(?<![\\w./-])\\./[\\w./-]+"\n', ''),
    "Z19 sottoagenti non contati": ('SEMPRE_ESECUZIONE = {"send_command_input", "invoke_subagent", "Agent", "Task"}', 'SEMPRE_ESECUZIONE = {"send_command_input"}'),
    "Z20 solo una lettura di 03/01/2005": ('        if sep == "/":\n            aggiungi(a, x, y)\n', ''),
    "Z21 date con punti non lette": ('    for a, _sep, m, g in DATA_AMG.findall(testo):\n        aggiungi(a, m, g)\n', ''),
    "Z22 date compatte non lette": ('    for a, m, g in DATA_COMPATTA.findall(testo):\n        aggiungi(a, m, g)\n', ''),
    "Z23 timestamp in millisecondi come secondi": ('int(t) / (1000 if len(t) == 13 else 1)', 'int(t) / 1'),
    "Z24 percorsi Dukascopy senza BID/ASK": ('(?=/(?:(?i:bid|ask)|\\d{2}h_ticks))', '(?=/(?:(?i:bid|ask)))'),
    "Z29 simbolo Dukascopy senza distinguere le maiuscole": ('|(?<=[A-Z]{6}/)((?:19|20)', '|(?<=[A-Za-z]{6}/)((?:19|20)'),
    "Z30 date generiche nei percorsi perse": ('(?<![\\d.])(?<![A-Z]{6}/)((?:19|20)', '(?<![\\d./])((?:19|20)'),
    "Z25 prezzi con virgola non visti": ('[1-9]\\d{2,3}[.,]\\d{1,17})', '[1-9]\\d{2,3}[.]\\d{1,17})'),
    "Z26 prezzi oltre 999 senza migliaia": ('[1-9]\\d{2,3}[.,]\\d{1,17})', '[1-9]\\d{2}[.,]\\d{1,17})'),
    "Z41 prezzi con più di 4 decimali (#79)": ('[1-9]\\d{2,3}[.,]\\d{1,17})', '[1-9]\\d{2,3}[.,]\\d{1,4})'),
    "Z27 contenuti dei file stampati": ('            elif k in CAMPI_DA_MOSTRARE:', '            elif True:'),
    "Z31 date compatte non lette vicino a un punto": ('(?<!\\d)(?<!\\d\\.)((?:19|20)\\d{2})(\\d{2})(\\d{2})(?!\\d)(?!\\.\\d)', '(?<![\\d.])((?:19|20)\\d{2})(\\d{2})(\\d{2})(?![\\d.])'),
    "Z32 date compatte dentro un decimale": ('(?<!\\d)(?<!\\d\\.)((?:19|20)\\d{2})(\\d{2})(\\d{2})(?!\\d)(?!\\.\\d)', '(?<!\\d)((?:19|20)\\d{2})(\\d{2})(\\d{2})(?!\\d)'),
    "Z40 date compatte attaccate a lettere perse (#78)": ('(?<!\\d)(?<!\\d\\.)((?:19|20)\\d{2})(\\d{2})(\\d{2})(?!\\d)(?!\\.\\d)', '(?<![\\w])(?<!\\d\\.)((?:19|20)\\d{2})(\\d{2})(\\d{2})(?![\\w])(?!\\.\\d)'),
    "Z33 comandi su più righe (#75)": ('ESECUZIONE.search(_valori(arg))', 'ESECUZIONE.search(t)'),
    "Z34 percorso inesistente accettato (#76)": ('    if mancanti:  ', '    if False:  '),
    "Z35 valori delle liste ignorati (#75)": ('        return "\\n".join(_valori(v) for v in arg)\n    return str(arg)', '        return ""\n    return str(arg)'),
    "Z36 make ovunque (#77)": ('r"|(?:^|(?<=[;&|]))\\s*make(?![\\w-])"', 'r"|(?<![\\w-])make(?![\\w-])"'),
    "Z37 npx non visto (#77)": ('(?:npx|php|deno|bun)', '(?:php|deno|bun)'),
    "Z38 uv run non visto (#77)": ('(?:npm|uv|cargo|poetry|pipenv|yarn|pnpm)\\s+run', '(?:npm|cargo|poetry|pipenv|yarn|pnpm)\\s+run'),
    "Z39 make dopo un a capo non visto (#77)": ('re.I | re.M)', 're.I)'),
    "Z42 soglia dei soli prezzi abbassata (#80)": ('if len(bassi) < MIN_PREZZI_SENZA_DATE:', 'if len(bassi) < MIN_PREZZI_SENZA_DATE - 1:'),
    "Z43 prezzi dello sviluppo contati (#80)": ('if _valore(x) < SOTTO_SVILUPPO}', 'if True}'),
    "Z44 soli prezzi non da guardare (#80)": ('"numeri_prezzo": p,\n                "da_guardare": True}', '"numeri_prezzo": p,\n                "da_guardare": False}'),
    "Z45 toolUseResult ignorato (#81)": ('if riga.get("toolUseResult") is not None:', 'if False:'),
    "Z46 toolUseResult come seconda uscita (#81)": ('                uscite[-1] = uscite[-1] + "\\n" + extra', '                uscite.append(extra)'),
    "Z47 separatore delle migliaia non tolto (#80)": ('prezzo[:i].replace(".", "").replace(",", "")', 'prezzo[:i]'),
    "Z28 formato sconosciuto come testo": ('    return None, n, "", [], [_testo(riga)], []', '    return None, n, "", [], [], [_testo(riga)]'),
}


def suite(radice):
    """Suite sul mutante, con la RETE BLOCCATA (#66: un mutante che esce in rete deve fallire subito, non scaricare né
    aspettare 20 minuti). Tempo scaduto: contato come ucciso, ma segnalato da guardare."""
    senza_rete = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9",
                      https_proxy="http://127.0.0.1:9", http_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")
    try:
        return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "test_riconta"], cwd=radice,
                              capture_output=True, text=True, timeout=300, env=senza_rete).returncode == 0
    except subprocess.TimeoutExpired:
        print(f"ATTENZIONE: tempo scaduto in {Path(radice).name}: contato come ucciso, da guardare", flush=True)
        return False


def mutante(i, nome, a, b):
    dest = OUT / f"M{i:02d}"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(QUI, dest, ignore=shutil.ignore_patterns("__pycache__"))
    testo = (dest / "riconta.py").read_text(encoding="utf-8")
    if testo.count(a) != 1:
        shutil.rmtree(dest)
        return nome, f"ERRORE: la sostituzione compare {testo.count(a)} volte"
    (dest / "riconta.py").write_text(testo.replace(a, b), encoding="utf-8")
    try:                                                   # #59: una sintassi rotta non è un mutante ucciso
        compile(testo.replace(a, b), "riconta.py", "exec")
    except SyntaxError:
        shutil.rmtree(dest)
        return nome, "NON VALIDO: sintassi rotta"
    vivo = suite(dest)
    shutil.rmtree(dest)
    return nome, "VIVO" if vivo else "UCCISO"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    zero = OUT / "M00"
    if zero.exists():
        shutil.rmtree(zero)
    shutil.copytree(QUI, zero, ignore=shutil.ignore_patterns("__pycache__"))
    if not suite(zero):
        sys.exit("M00 NON supera la suite: fermo")
    shutil.rmtree(zero)
    print("M00 copia non mutata: suite verde", flush=True)
    with ThreadPoolExecutor(PROCESSI) as ex:
        esiti = list(ex.map(lambda x: mutante(x[0], *x[1]), [(i, (n, a, b)) for i, (n, (a, b)) in enumerate(M.items(), 1)]))
    for nome, esito in esiti:
        print(f"{esito:6} {nome}")
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]})")
    return 0 if uccisi == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
