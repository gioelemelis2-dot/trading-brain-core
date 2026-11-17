"""Mutation testing del controllo d'integrità della cache (dati/pipeline/controlla_cache.py).
Ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve superare i test; ogni sostituzione deve
comparire una sola volta. Uso (dalla radice del repository): python3 -s -B brain/dati/tests/mutazioni_controlla_cache.py <cartella> [processi] [prefissi]
  prefissi: per esempio «S,C» per far girare solo i mutanti che iniziano con S o C (utile con poco tempo).
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if len(sys.argv) not in (2, 3, 4):
    sys.exit(__doc__)
BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve()
PROCESSI = int(sys.argv[2]) if len(sys.argv) >= 3 else 2
PREFISSI = tuple(sys.argv[3].split(",")) if len(sys.argv) == 4 else ("",)
SUITE = ["brain.dati.tests.test_controlla_cache"]
CC = "dati/pipeline/controlla_cache.py"
CAL = "dati/pipeline/calendario.py"
M = {
    "Q12 confronto: BID senza ASK non visto": [(CC, "        if fb.exists() and not fa.exists():", "        if False:")],
    "Q13 confronto: vuoto da un lato non visto": [(CC, "and (fb.stat().st_size > 0) != (fa.stat().st_size > 0):", "and False:")],
    "Q14 confronto: sempre allineati": [(CC, "            \"allineati\": not (senza_ask or senza_bid or vuoto_lato)}", "            \"allineati\": True}")],
    "Q15 confronto: --ask senza periodo accettato": [(CC, "    if x.ask and not (x.inizio and x.fine):", "    if False:")],
    "Q17 periodo invertito accettato (#74)": [(CC, "    if x.inizio and x.fine and x.inizio > x.fine:", "    if False:")],
    "Q18 nomi non AAAA-MM-GG.bi5 come giorni (#82)": [(CC, "    if not NOME_GIORNO.fullmatch(nome):\n        return None\n", "")],
    "Q19 file messi da parte non stampati (#82)": [(CC, "        if e.get(chiave):\n            righe.append(f\"{nome}: {len(e[chiave])}", "        if False:\n            righe.append(f\"{nome}: {len(e[chiave])}")],
    "Q20 .bi5 validi fra gli estranei (#82)": [(CC, "if p.name.endswith(\".bi5\") and _data(p.name) is None", "if p.name.endswith(\".bi5\")")],
    # Q21 «minuti contati per record (#85)» DICHIARATO EQUIVALENTE il 17/11 e tolto dall'elenco: dopo #89 decodifica
    # rifiuta i minuti ripetuti, quindi contare i minuti distinti o i record dà lo stesso numero. Il conteggio dei
    # distinti resta come difesa in profondità. (Sopravvissuto nella corsa del 17/11 su 3.13 e 3.9.)
    "Q16 confronto: esito ignorato nel codice d'uscita": [(CC, "    return 0 if all(e.get(\"pulito\", True) for e in esiti) and allineati else 1", "    return 0 if all(e.get(\"pulito\", True) for e in esiti) else 1")],
    "Q01 file mancanti non contati": [(CC, "            a[\"mancanti\"] += 1\n", "            pass\n")],
    "Q02 illeggibili ignorati": [(CC, "                    a[\"illeggibili\"].append(g.isoformat())\n", "                    pass\n")],
    "Q03 chiusure note anche il 24/12": [(CAL, "        g |= {cap, nat, date(a, 12, 26), ", "        g |= {cap, nat, date(a, 12, 24), date(a, 12, 26), ")],
    "Q04 Venerdì Santo dimenticato": [(CAL, "date(a, 12, 26), pasqua(a) - timedelta(days=2), ", "date(a, 12, 26), ")],
    "Q05 soglia dei corti al 25%": [(CC, "QUOTA_CORTI = 0.5", "QUOTA_CORTI = 0.25")],
    "Q06 temporanei ignorati nel verdetto": [(CC, "pulito = bool(file) and not tmp and all(", "pulito = bool(file) and all(")],
    "Q07 feriali vuoti ignorati nel verdetto": [(CC, "a[\"mancanti\"] == 0 and not a[\"feriali_vuoti\"] and not a[\"illeggibili\"]",
                                                 "a[\"mancanti\"] == 0 and not a[\"illeggibili\"]")],
    "Q08 minuti non sommati": [(CC, "                a[\"minuti\"] += n\n", "                pass\n")],
    "Q09 periodo esplicito ignorato": [(CC, "    inizio = inizio or min(file)\n    fine = fine or max(file)\n",
                                         "    inizio = min(file)\n    fine = max(file)\n")],
    "Q10 fine settimana contati come feriali vuoti": [(CC, "            elif n == 0 and g.weekday() < 5:", "            elif n == 0:")],
    "Q11 prezzi nell'esito": [(CC, "                    n = len({m[0] for m in DK.decodifica(dati, g, DK.SCALA[simbolo])})   # minuti distinti (#85)\n",
                                "                    _m = DK.decodifica(dati, g, DK.SCALA[simbolo]); n = len(_m); a.setdefault(\"p\", str(_m[0][1]) if _m else None)\n")],
}


def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    """Suite sul mutante, con la RETE BLOCCATA (#66: un mutante che esce in rete deve fallire subito, non scaricare né
    aspettare 20 minuti). Tempo scaduto: contato come ucciso, ma segnalato da guardare."""
    senza_rete = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9",
                      https_proxy="http://127.0.0.1:9", http_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")
    try:
        return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f", *SUITE], cwd=radice,
                              capture_output=True, text=True, timeout=900, env=senza_rete).returncode == 0
    except subprocess.TimeoutExpired:
        print(f"ATTENZIONE: tempo scaduto in {Path(radice).name}: contato come ucciso, da guardare", flush=True)
        return False


def mutante(i, nome, sost):
    dest = OUT / f"M{i:02d}"
    copia(dest)
    for f, vecchio, nuovo in sost:
        testo = (dest / "brain" / f).read_text(encoding="utf-8")
        if testo.count(vecchio) != 1:
            shutil.rmtree(dest)
            return nome, f"ERRORE: la sostituzione compare {testo.count(vecchio)} volte in {f}"
        (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
        try:                                               # #59: una sintassi rotta non è un mutante ucciso
            compile((dest / "brain" / f).read_text(encoding="utf-8"), str(f), "exec")
        except SyntaxError:
            shutil.rmtree(dest)
            return nome, "NON VALIDO: sintassi rotta"
    vivo = suite(dest)
    shutil.rmtree(dest)
    return nome, "VIVO" if vivo else "UCCISO"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    copia(OUT / "M00")
    if not suite(OUT / "M00"):
        sys.exit("M00 NON supera la suite: fermo")
    shutil.rmtree(OUT / "M00")
    print("M00 copia non mutata: suite verde", flush=True)
    with ThreadPoolExecutor(PROCESSI) as ex:
        esiti = list(ex.map(lambda a: mutante(*a), [(i, n, s) for i, (n, s) in enumerate(M.items(), 1) if n.startswith(PREFISSI)]))
    for nome, esito in esiti:
        print(f"{esito:6} {nome}")
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]})")
    return 0 if uccisi == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
