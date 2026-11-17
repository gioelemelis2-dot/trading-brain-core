"""Sigillo delle schede e registro delle prove (DA-19, DA-28; scheda H-002 v3.1 §7 e §10).

Il registro è un file JSON, scritto solo in aggiunta e in modo atomico:
- `prove`: le prove dichiarate al sigillo (ruolo «selezionabile»). Sono loro il numero N del DSR;
- `sigilli`: un sigillo per ipotesi, con l'impronta SHA-256 della scheda;
- `esecuzioni`: ogni esecuzione (sviluppo, robustezza, verifica). Le esecuzioni NON entrano in N: N conta le
  varianti fra cui si sceglie, dichiarate prima.

Lo strumento è pronto ma NON va eseguito sul registro vero senza la decisione dell'utente (mandato del 14/11/2026).
"""
import fcntl
import hashlib
import json
import os
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

SCHEMA = "registro-prove/1"
RADICE = Path(__file__).resolve().parents[3]
RUOLI_ESECUZIONE = ("sviluppo", "robustezza", "verifica", "esito")       # esito: risultato della verifica


class NonSigillata(RuntimeError):
    """La scheda non risulta sigillata nel registro: niente esecuzioni."""


def impronta(scheda: Path) -> str:
    return hashlib.sha256(Path(scheda).read_bytes()).hexdigest()


def leggi(registro: Path) -> dict:
    """Contenuto del registro; se il file non esiste, un registro vuoto (il file NON viene creato)."""
    registro = Path(registro)
    if not registro.exists():
        return {"schema": SCHEMA, "prove": [], "sigilli": [], "esecuzioni": []}
    dati = json.loads(registro.read_text(encoding="utf-8"))
    if dati.get("schema") != SCHEMA:
        raise ValueError(f"{registro}: schema {dati.get('schema')!r}, atteso {SCHEMA!r}")
    for chiave in ("prove", "sigilli", "esecuzioni"):
        if not isinstance(dati.get(chiave), list):
            raise ValueError(f"{registro}: manca l'elenco {chiave!r}")
    return dati


def _scrivi(registro: Path, dati: dict) -> None:
    registro = Path(registro)
    registro.parent.mkdir(parents=True, exist_ok=True)
    tmp = registro.with_name(f".{registro.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=2, ensure_ascii=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, registro)


@contextmanager
def _bloccato(registro: Path):
    """Blocco esclusivo per leggere, modificare e riscrivere il registro senza perdere scritture concorrenti
    (rilievo P8 di Gemini). Il file .lock sta accanto al registro."""
    registro = Path(registro)
    registro.parent.mkdir(parents=True, exist_ok=True)
    with open(registro.with_name(registro.name + ".lock"), "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _sigillo(dati: dict, ipotesi: str):
    trovati = [s for s in dati["sigilli"] if s["ipotesi"] == ipotesi]
    return trovati[0] if trovati else None


def n_prove(dati: dict) -> int:
    """N per il DSR: tutte le prove selezionabili nel registro, di tutte le ipotesi."""
    return sum(1 for p in dati["prove"] if p["ruolo"] == "selezionabile")


def sigilla(registro: Path, ipotesi: str, scheda: Path, varianti: List[str], ora: str,
            codice: Optional[Dict[str, str]] = None, robustezza: Optional[List[str]] = None) -> dict:
    """Registra l'impronta della scheda e le sue prove dichiarate. Rifiuta il doppio sigillo e un'ipotesi che ha
    già esecuzioni registrate (nessuna esecuzione prima del sigillo)."""
    if not varianti or len(set(varianti)) != len(varianti) or not all(isinstance(v, str) and v for v in varianti):
        raise ValueError(f"varianti non valide: {varianti!r} (servono nomi distinti, almeno uno)")
    with _bloccato(registro):
        return _sigilla(registro, ipotesi, scheda, varianti, ora, codice, robustezza)


def _sigilla(registro: Path, ipotesi: str, scheda: Path, varianti: List[str], ora: str,
             codice: Optional[Dict[str, str]], robustezza: Optional[List[str]] = None) -> dict:
    dati = leggi(registro)
    if _sigillo(dati, ipotesi) is not None:
        raise ValueError(f"{ipotesi} è già sigillata: ogni cambiamento è un'ipotesi nuova")
    if any(e["ipotesi"] == ipotesi for e in dati["esecuzioni"]):
        raise ValueError(f"{ipotesi} ha già esecuzioni registrate prima del sigillo")
    s = {"ipotesi": ipotesi, "scheda": Path(scheda).name, "scheda_sha256": impronta(scheda),
         "varianti": list(varianti), "ora": ora, "codice": dict(codice or {}),
         "robustezza": sorted(robustezza or [])}                         # #69: prove di robustezza dichiarate
    dati["sigilli"].append(s)
    dati["prove"] += [{"id": f"{ipotesi}/{v}", "ipotesi": ipotesi, "ruolo": "selezionabile", "ora": ora}
                      for v in varianti]
    _scrivi(registro, dati)
    return s


def controlla_sigillo(registro: Path, ipotesi: str, scheda: Path, codice: Optional[Dict[str, str]] = None,
                      radice: Optional[Path] = None) -> dict:
    """Il sigillo dell'ipotesi, solo se la scheda sul disco è ancora quella sigillata e il codice è quello sigillato:
    - con `codice`, le impronte date devono essere esattamente quelle registrate (stessi file, stesse impronte);
    - senza `codice` (es. il caricatore chiamato da altri script, #48), si ricalcolano dal disco le impronte dei file
      registrati al sigillo: un file cambiato o sparito ferma tutto."""
    s = _sigillo(leggi(registro), ipotesi)
    if s is None:
        raise NonSigillata(f"{ipotesi} non risulta sigillata nel registro {registro}")
    if impronta(scheda) != s["scheda_sha256"]:
        raise ValueError(f"la scheda {scheda} è stata modificata dopo il sigillo di {ipotesi}")
    if codice is not None and s.get("codice") != codice:
        diversi = sorted(k for k in set(codice) | set(s.get("codice") or {}) if codice.get(k) != (s.get("codice") or {}).get(k))
        raise ValueError(f"il codice che esegue {ipotesi} non è quello sigillato: {diversi}")
    if codice is None and s.get("codice"):
        r = Path(radice or RADICE)
        diversi = sorted(f for f, h in s["codice"].items()
                         if not (r / f).is_file() or hashlib.sha256((r / f).read_bytes()).hexdigest() != h)
        if diversi:
            raise ValueError(f"il codice che esegue {ipotesi} è cambiato dopo il sigillo: {diversi}")
    return s


def _git(radice: Path, *argomenti) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(radice), *argomenti], capture_output=True, text=True)


def ancora_git(file: Path, radice: Path, continua) -> None:
    """Il file JSON deve essere ancorato alla versione su GitHub (#51, #62, R13-B-02):
    - non un collegamento simbolico, dentro il repository;
    - HEAD su un ramo (non staccata) con una versione remota (`@{u}`), e HEAD che la CONTIENE (niente storia
      riscritta con --amend o rebase dopo il push);
    - il file sul disco IDENTICO a quello della HEAD (nessuna modifica non committata);
    - la versione della HEAD che CONTINUA quella remota secondo `continua(remota, head)`, che solleva ValueError.
    Limite dichiarato: la versione remota è quella dell'ultimo `git fetch`; chi riscrive anche il riferimento locale
    del ramo remoto va visto confrontando con GitHub stesso."""
    file = Path(file)
    if file.is_symlink():
        raise ValueError(f"{file} è un collegamento simbolico: non è ancorato a git")
    file, radice = file.resolve(), Path(radice).resolve()
    try:
        rel = file.relative_to(radice).as_posix()
    except ValueError:
        raise ValueError(f"il file {file} è fuori dal repository {radice}: non è ancorato a git") from None
    if _git(radice, "symbolic-ref", "-q", "HEAD").returncode != 0:
        raise ValueError("HEAD staccata: eseguire da un ramo")
    remoto = _git(radice, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if remoto.returncode != 0:
        raise ValueError("il ramo non ha una versione remota (GitHub): spingerlo prima con git push -u")
    remoto = remoto.stdout.strip()
    if _git(radice, "merge-base", "--is-ancestor", remoto, "HEAD").returncode != 0:
        raise ValueError(f"la HEAD non contiene {remoto}: storia riscritta o ramo indietro")
    head = _git(radice, "show", f"HEAD:{rel}")
    if head.returncode != 0:
        raise ValueError(f"{rel} non è versionato in git: committarlo e spingerlo prima di eseguire")
    if json.loads(head.stdout) != json.loads(file.read_text(encoding="utf-8")):
        raise ValueError(f"{rel} ha modifiche non committate: committarlo e spingerlo prima di eseguire")
    su_github = _git(radice, "show", f"{remoto}:{rel}")
    if su_github.returncode != 0:
        raise ValueError(f"{rel} non è ancora su {remoto}: spingerlo prima di eseguire")
    continua(json.loads(su_github.stdout), json.loads(head.stdout))


def versioni_nella_storia(radice: Path, rel: str) -> List[dict]:
    """Ogni versione del file JSON `rel` in ogni commit raggiungibile da un riferimento qualsiasi (rami locali, rami
    remoti, etichette): #86, una verifica fatta su un ramo non si rifà su un altro ramo né da un commit precedente.
    Limite dichiarato: vede i riferimenti presenti nel repository locale (dopo l'ultimo `git fetch`); un ramo
    cancellato anche su GitHub va impedito con la protezione dei rami."""
    elenco = _git(radice, "rev-list", "--all", "--", rel)
    if elenco.returncode != 0:
        raise ValueError(f"storia git di {rel} non leggibile: {elenco.stderr.strip()}")
    versioni = []
    for commit in elenco.stdout.split():
        v = _git(radice, "show", f"{commit}:{rel}")
        if v.returncode == 0:
            try:
                versioni.append(json.loads(v.stdout))
            except ValueError:
                continue
    return versioni


def controlla_ancora(registro: Path, radice: Path) -> None:
    """Registro delle prove ancorato alla versione su GitHub (vedi `ancora_git`): le voci già spinte non si cambiano
    né si tolgono; si aggiungono solo voci nuove in fondo, committate."""
    def continua(remota: dict, head: dict) -> None:
        for chiave in ("prove", "sigilli", "esecuzioni"):
            vecchie = remota.get(chiave) or []
            if (head.get(chiave) or [])[:len(vecchie)] != vecchie:
                raise ValueError(f"il registro non continua la versione su GitHub ({chiave}: voci cambiate o tolte)")
    ancora_git(registro, radice, continua)


def registra_esecuzione(registro: Path, ipotesi: str, voce: dict, ora: str) -> dict:
    """Aggiunge un'esecuzione. La verifica sigillata si esegue una volta sola per variante."""
    with _bloccato(registro):
        return _registra(registro, ipotesi, voce, ora)


def _registra(registro: Path, ipotesi: str, voce: dict, ora: str) -> dict:
    dati = leggi(registro)
    if _sigillo(dati, ipotesi) is None:
        raise NonSigillata(f"{ipotesi} non risulta sigillata: nessuna esecuzione")
    ruolo = voce.get("ruolo")
    if ruolo not in RUOLI_ESECUZIONE:
        raise ValueError(f"ruolo {ruolo!r} non in {RUOLI_ESECUZIONE}")
    variante = str(voce.get("variante") or "")
    dichiarate = _sigillo(dati, ipotesi)["varianti"]
    if ruolo == "robustezza":                          # «<variante> <prova>»: R11-S7, #51, #69 (prove dichiarate)
        base, _, prova = variante.partition(" ")
        prove = _sigillo(dati, ipotesi).get("robustezza") or []
        valida = base in dichiarate and bool(prova.strip()) and (not prove or prova in prove)
    else:
        valida = variante in dichiarate
    if not valida:
        raise ValueError(f"variante {voce.get('variante')!r} non dichiarata nel sigillo di {ipotesi}")
    if ruolo == "verifica" and any(e["ipotesi"] == ipotesi and e["ruolo"] == "verifica"
                                   and e.get("variante") == voce.get("variante") for e in dati["esecuzioni"]):
        raise ValueError(f"verifica di {ipotesi} {voce.get('variante')} già eseguita: si fa una volta sola")
    if ruolo == "esito":                                   # #90: uno solo, e solo dopo la verifica
        stessa = [x for x in dati["esecuzioni"] if x["ipotesi"] == ipotesi and x.get("variante") == variante]
        if not any(x["ruolo"] == "verifica" for x in stessa):
            raise ValueError(f"esito di {ipotesi} {variante} senza verifica registrata")
        if any(x["ruolo"] == "esito" for x in stessa):
            raise ValueError(f"esito di {ipotesi} {variante} già registrato: uno solo")
    e = dict(voce, ipotesi=ipotesi, ora=ora)
    dati["esecuzioni"].append(e)
    _scrivi(registro, dati)
    return e
