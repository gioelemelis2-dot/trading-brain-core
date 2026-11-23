"""Prova positiva COMPLETA dal lanciatore (DGS-18 Q4; revisione critica del 23/11, punto B.8), 23/11/2026.

Strumento di ricevuta, fuori dal perimetro. Solo dati sintetici e rete bloccata. Passi:
1. un repository git di prova con un remoto finto (bare); dentro, una COPIA di `brain` presa dal candidato (argomento
   --sorgente, un worktree bloccato sul commit);
2. cache sintetiche fuori dal repository (mercato_sintetico, gli stessi parametri dei test del percorso);
3. scheda H-003 di test, sigillo con il codice della copia, registro della riserva canonico con la prenotazione P1;
   commit e push sul remoto finto, come farebbe il titolare;
4. `python3 -I -S -B brain/laboratorio/esecuzione/avvio.py verifica …` in un processo separato, con ANCORA_GIT e
   CONTROLLO_AMBIENTE accesi come nel codice (nessuna sostituzione);
5. commit e push dei registri aggiornati; seconda chiamata identica: deve dare «rapporto rigenerato» senza letture;
6. riconciliazione dal solo record (byte del rapporto compresi) e riga della potenza nel rapporto (#141).
Scrive in <uscita>/prova_lanciatore.json: comandi, codici d'uscita, esiti, impronte dei registri prima e dopo, storia
git, impegno, record, rapporto. Uso:
  python3 -s -B prova_lanciatore.py --sorgente <worktree del candidato> --uscita <cartella vuota>
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

a = argparse.ArgumentParser()
a.add_argument("--sorgente", required=True, type=Path)
a.add_argument("--uscita", required=True, type=Path)
x = a.parse_args()
SORG, OUT = x.sorgente.resolve(), x.uscita.resolve()
OUT.mkdir(parents=True, exist_ok=False)
sys.path.insert(0, str(SORG))

from brain.laboratorio.esecuzione import esegui_verifica as EV      # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV             # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S              # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as M         # noqa: E402
from brain.laboratorio.tests import test_esegui_verifica as T     # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V           # noqa: E402

AMB = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()   # noqa: E731


def git(*arg, out=False):
    r = subprocess.run(["git", "-C", str(REPO), "-c", "user.name=prova", "-c", "user.email=prova@invalid", *arg],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip() if out else None


def spingi(msg):
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    git("push", "-q", "-u", "origin", "principale")
    return git("rev-parse", "HEAD", out=True)


# 1. repository di prova
remoto, REPO = OUT / "remoto.git", OUT / "repo"
subprocess.run(["git", "init", "-q", "--bare", str(remoto)], check=True)
subprocess.run(["git", "clone", "-q", str(remoto), str(REPO)], check=True, capture_output=True)
git("checkout", "-q", "-b", "principale")
shutil.copytree(SORG / "brain", REPO / "brain", ignore=shutil.ignore_patterns("__pycache__", "reali"))
(REPO / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")

# 2. cache sintetiche fuori dal repository
cache, cache_sv = OUT / "cache", OUT / "cache_sviluppo"
vere = M.scrivi(cache, T.LETTURA, T.FINE, 0.6, 11)
M.scrivi(cache_sv, *T.SVILUPPO, 0.6, 13)

# 3. scheda, sigillo, prenotazione nei registri canonici, poi commit e push
lab = REPO / "brain" / "laboratorio"
registro, riserva = REPO / EV.REL_REGISTRO_PROVE, REPO / EV.REL_RISERVA
scheda = REPO / "H-T127.md"
scheda.write_text(T.testo_scheda(T.contratto("H-T127")), encoding="utf-8")
codice = EV.impronte_codice(REPO)
S.sigilla(registro, "H-T127", scheda, ["V-T"], T.ORA, codice=codice)
RV.crea(riserva, M.date(2005, 1, 1), M.date(2023, 10, 31), 0.05, T.ORA)
RV.prenota(riserva, "P1", "H-T127", T.LETTURA, T.FINE, S.impronta(scheda), T.ORA)
commit_prima = spingi("sigillo e prenotazione P1")
prima = {"registro_prove": sha(registro), "riserva": sha(riserva)}

# 4. il lanciatore, in un processo separato
rapporto = OUT / "rapporto_P1.txt"
comando = [sys.executable, "-I", "-S", "-B", "brain/laboratorio/esecuzione/avvio.py", "verifica",
           "--scheda", str(scheda), "--registro", EV.REL_REGISTRO_PROVE, "--riserva", EV.REL_RISERVA,
           "--prenotazione", "P1", "--cache", str(cache), "--cache-sviluppo", str(cache_sv),
           "--rapporto", str(rapporto), "--ora", T.ORA]
r1 = subprocess.run(comando, cwd=str(REPO), capture_output=True, text=True, env=AMB)
dopo = {"registro_prove": sha(registro), "riserva": sha(riserva)}
uscita1 = json.loads(r1.stdout) if r1.returncode == 0 else None

# 5. registri pubblicati, poi ripresa identica
commit_dopo = spingi("esito della verifica P1") if r1.returncode == 0 else None
byte_rapporto_1 = rapporto.read_bytes() if rapporto.exists() else b""
r2 = subprocess.run(comando, cwd=str(REPO), capture_output=True, text=True, env=AMB)
uscita2 = json.loads(r2.stdout) if r2.returncode == 0 else None
ripresa_senza_scritture = sha(riserva) == dopo["riserva"]

# 6. riconciliazione dal solo record e riga della potenza
p = RV.prenotazione(riserva, "P1")
rec = p["record"] or {}
imp = (p["autorizzazione"] or {}).get("impegno") or {}
coppie = rec.get("coppie") or []
controlli = {}
if rec:
    controlli["identita"] = rec["impronta_impegno"] == RV.impronta_impegno(imp) == p["autorizzazione"]["hash_dati"]
    controlli["sedute"] = [c[0] for c in coppie] == imp["sedute"] and len(set(imp["sedute"])) == 1000
    esatta = sum(Fraction(c[1]) for c in coppie) / sum(c[2] for c in coppie)
    controlli["media"] = rec["verdetto"]["media"] == float(esatta)
    vb = imp["contratto"]["veto_blocchi"]
    cp = [(c[1], c[2]) for c in coppie]
    ctx = {k: rec["verdetto"]["contesto_prove"][k] for k in ("registro", "n_prove", "impronta")}
    w = json.loads(json.dumps(V.verdetto(cp, imp["seme"], [V.veto_blocchi(cp, vb["soglia"], vb["minimo_trade"])],
                                         contesto=ctx), default=str))
    controlli["verdetto"] = all(w[k] == rec["verdetto"][k] for k in ("L", "U", "segnale", "esito", "causa", "requisiti"))
    controlli["rapporto_byte"] = rapporto.read_bytes() == EV.rapporto_da_record(rec).encode("utf-8")
    controlli["ripresa_byte_identici"] = byte_rapporto_1 == rapporto.read_bytes()
riga_potenza = [r for r in rapporto.read_text(encoding="utf-8").splitlines() if "potenza" in r] if rapporto.exists() else []

esito = {
    "candidato": subprocess.run(["git", "-C", str(SORG), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "python": sys.version.split()[0],
    "comando": " ".join(c if not c.startswith(str(OUT)) else "<uscita>" + c[len(str(OUT)):] for c in comando),
    "prima_chiamata": {"codice": r1.returncode, "uscita": uscita1, "stderr": r1.stderr[-800:]},
    "seconda_chiamata": {"codice": r2.returncode, "uscita": uscita2, "stderr": r2.stderr[-800:],
                         "riserva_invariata": ripresa_senza_scritture},
    "registri": {"prima": prima, "dopo": dopo, "commit_prima": commit_prima, "commit_dopo": commit_dopo,
                 "storia": git("log", "--format=%h %s", out=True).splitlines()},
    "stato_riserva": RV.stato(riserva)["aperture"],
    "esecuzioni_registro_prove": [{k: e.get(k) for k in ("ruolo", "variante", "esito", "prenotazione")}
                                  for e in S.leggi(registro)["esecuzioni"]],
    "controlli_dal_record": controlli,
    "tutti": bool(controlli) and all(controlli.values()) and r1.returncode == 0 and r2.returncode == 0
             and (uscita1 or {}).get("esito") == "promossa"
             and (uscita2 or {}).get("esito_tecnico") == "rapporto rigenerato" and ripresa_senza_scritture,
    "riga_potenza_nel_rapporto": riga_potenza,
    "impegno_impronta": RV.impronta_impegno(imp) if imp else None,
}
(OUT / "prova_lanciatore.json").write_text(json.dumps(esito, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
(OUT / "record_P1.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
(OUT / "impegno_P1.json").write_text(json.dumps(imp, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
print(json.dumps({k: esito[k] for k in ("candidato", "python", "tutti", "controlli_dal_record", "riga_potenza_nel_rapporto")},
                 ensure_ascii=False, indent=1))
print("prima:", r1.returncode, (uscita1 or {}).get("esito_tecnico"), (uscita1 or {}).get("esito"), r1.stderr[-300:])
print("seconda:", r2.returncode, (uscita2 or {}).get("esito_tecnico"))
sys.exit(0 if esito["tutti"] else 1)
