"""Mutanti della diagnosi del manifesto (strumento di contorno, 23/11/2026). Ogni mutante deve far fallire
test_diagnosi_manifesto. Lavora su una COPIA del repository (argomento), mai sui file originali.
Uso: python3 -s -B brain/laboratorio/tests/mutazioni_diagnosi_manifesto.py <cartella vuota>
"""
import shutil
import subprocess
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
FILE = "brain/laboratorio/studi/diagnosi_manifesto.py"
MUTANTI = [
    ("DM01", 'reg.group(1) if reg else', 'LATO.search(anomalia).group(1) if reg else'),
    ("DM02", ' and r.get("lato") == lato', ''),
    ("DM03", 'byte: bool = True', 'byte: bool = False'),
    ("DM04", 'if not f.is_file():', 'if f.is_dir():'),
    ("DM05", '!= impronta', '== impronta'),
    ("DM06", 'return 0 if d["pulito"] else 1', 'return 0'),
    ("DM07", 'd["pulito"] = not d["per_tipo"]', 'd["pulito"] = True'),
    ("DM08", 'giorno[:4]] = anni.get(giorno[:4], 0) + 1', 'giorno[:4]] = 1'),
    ("DM09", 'if x.fine < x.inizio:', 'if x.fine < x.fine:'),
    ("DM10", 'if not x.cache.is_dir():', 'if False:'),
    ("DM11", 'byte=not x.senza_byte', 'byte=x.senza_byte'),
    ("DM12", '"+".join(', '"".join('),
    ("DM13", 'if r.get("esito") in MF.VALIDI', 'if True'),
]


def main() -> int:
    copia = Path(sys.argv[1]) / "repo"
    shutil.copytree(RADICE / "brain", copia / "brain")
    originale = (copia / FILE).read_text(encoding="utf-8")
    vivi = 0
    for nome, prima, dopo in MUTANTI:
        if originale.count(prima) != 1:
            print(f"NON VALIDO {nome}", flush=True)
            vivi += 1
            continue
        (copia / FILE).write_text(originale.replace(prima, dopo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-s", "-B", "-m", "unittest", "brain.laboratorio.tests.test_diagnosi_manifesto"],
                           cwd=copia, capture_output=True)
        print(f"{'UCCISO' if r.returncode else 'SOPRAVVISSUTO'} {nome}", flush=True)
        vivi += r.returncode == 0
    (copia / FILE).write_text(originale, encoding="utf-8")
    print(f"uccisi {len(MUTANTI) - vivi}/{len(MUTANTI)}")
    return 1 if vivi else 0


if __name__ == "__main__":
    sys.exit(main())
