"""Mutation testing del scaricatore solo-cache (dati/pipeline/scarica_cache.py) e di dukascopy.richiesta_http.
Ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve superare i test; ogni sostituzione deve
comparire una sola volta. Uso (dalla radice del repository): python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella> [processi] [prefissi]
  prefissi: per esempio «S,C» per far girare solo i mutanti che iniziano con S o C (utile con poco tempo).
"""
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
SUITE = ["brain.dati.tests.test_scarica_cache", "brain.dati.tests.test_dukascopy"]
SC = "dati/pipeline/scarica_cache.py"
DK = "dati/pipeline/dukascopy.py"
M = {
    "W01 cache non saltata": [(SC, "        if f.exists():\n            conta[\"in_cache\"] += 1", "        if False:\n            conta[\"in_cache\"] += 1")],
    "W02 404 e vuoto scambiati": [(SC, "(\"404\" if codice == 404 else \"vuoto-200\")", "(\"vuoto-200\" if codice == 404 else \"404\")")],
    "W03 file non controllato prima di salvarlo": [(SC, "                DK.decodifica(corpo, g, DK.SCALA[simbolo])                # solo controllo: nessun prezzo esce\n",
                                                     "                pass\n")],
    "W04 errore HTTP sconosciuto non ferma": [(SC, "        except urllib.error.HTTPError as e:", "        except ValueError as e:")],
    "W05 errore HTTP non registrato": [(SC, "            _registra(registro, dict(riga, http=e.code, esito=f\"http-{e.code}\"))\n", "            pass\n")],
    "W06 impronta sbagliata nel registro": [(SC, "sha256=hashlib.sha256(corpo).hexdigest()", "sha256=hashlib.sha256(b\"\").hexdigest()")],
    "W07 rete assente non registrata": [(SC, "            _registra(registro, dict(riga, esito=\"nessuna-risposta\"))\n", "            pass\n")],
    "W08 attesa anche sui giorni in cache": [(SC, "            conta[\"in_cache\"] += 1\n", "            conta[\"in_cache\"] += 1\n            pausa()\n")],
    "W09 tentativi contati male": [(DK, "            return 200, dati, n + 1\n", "            return 200, dati, n\n")],
    "W10 404 trattato come 200": [(DK, "                return 404, None, n + 1\n", "                return 200, None, n + 1\n")],
    "W11 risposta vuota non più None nella vecchia interfaccia": [(DK, "    return dati or None\n", "    return dati\n")],
    "W12 4xx con nuovi tentativi": [(DK, "            if e.code != 429 and e.code < 500:\n                raise\n", "            if False:\n                raise\n")],
}


def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f", *SUITE], cwd=radice,
                          capture_output=True, text=True, timeout=900).returncode == 0


def mutante(i, nome, sost):
    dest = OUT / f"M{i:02d}"
    copia(dest)
    for f, vecchio, nuovo in sost:
        testo = (dest / "brain" / f).read_text(encoding="utf-8")
        if testo.count(vecchio) != 1:
            shutil.rmtree(dest)
            return nome, f"ERRORE: la sostituzione compare {testo.count(vecchio)} volte in {f}"
        (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
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
