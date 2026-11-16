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
            codice: Optional[Dict[str, str]] = None) -> dict:
    """Registra l'impronta della scheda e le sue prove dichiarate. Rifiuta il doppio sigillo e un'ipotesi che ha
    già esecuzioni registrate (nessuna esecuzione prima del sigillo)."""
    if not varianti or len(set(varianti)) != len(varianti) or not all(isinstance(v, str) and v for v in varianti):
        raise ValueError(f"varianti non valide: {varianti!r} (servono nomi distinti, almeno uno)")
    with _bloccato(registro):
        return _sigilla(registro, ipotesi, scheda, varianti, ora, codice)


def _sigilla(registro: Path, ipotesi: str, scheda: Path, varianti: List[str], ora: str,
             codice: Optional[Dict[str, str]]) -> dict:
    dati = leggi(registro)
    if _sigillo(dati, ipotesi) is not None:
        raise ValueError(f"{ipotesi} è già sigillata: ogni cambiamento è un'ipotesi nuova")
    if any(e["ipotesi"] == ipotesi for e in dati["esecuzioni"]):
        raise ValueError(f"{ipotesi} ha già esecuzioni registrate prima del sigillo")
    s = {"ipotesi": ipotesi, "scheda": Path(scheda).name, "scheda_sha256": impronta(scheda),
         "varianti": list(varianti), "ora": ora, "codice": dict(codice or {})}
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


def controlla_ancora(registro: Path, radice: Path) -> None:
    """Il registro deve essere versionato in git e CONTINUARE la versione dell'ultimo commit: le voci già su git non
    si cambiano né si tolgono, si aggiungono solo voci nuove in fondo (#51, rilievo R12bis-A3-04). Il registro va
    committato (e spinto su GitHub) dopo ogni esecuzione: così una manomissione si vede nella storia."""
    registro, radice = Path(registro).resolve(), Path(radice).resolve()
    try:
        rel = registro.relative_to(radice).as_posix()
    except ValueError:
        raise ValueError(f"il registro {registro} è fuori dal repository {radice}: non è ancorato a git") from None
    r = subprocess.run(["git", "-C", str(radice), "show", f"HEAD:{rel}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise ValueError(f"il registro {rel} non è versionato in git: committarlo prima di eseguire")
    su_git = json.loads(r.stdout)
    ora = leggi(registro)
    for chiave in ("prove", "sigilli", "esecuzioni"):
        vecchie = su_git.get(chiave) or []
        if ora[chiave][:len(vecchie)] != vecchie:
            raise ValueError(f"il registro {rel} non continua la versione su git ({chiave}: voci cambiate o tolte)")


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
    if ruolo == "robustezza":                          # «<variante> <prova>»: R11-S7, poi #51 (niente suffissi liberi)
        base, _, prova = variante.partition(" ")
        valida = base in dichiarate and bool(prova.strip())
    else:
        valida = variante in dichiarate
    if not valida:
        raise ValueError(f"variante {voce.get('variante')!r} non dichiarata nel sigillo di {ipotesi}")
    if ruolo == "verifica" and any(e["ipotesi"] == ipotesi and e["ruolo"] == "verifica"
                                   and e.get("variante") == voce.get("variante") for e in dati["esecuzioni"]):
        raise ValueError(f"verifica di {ipotesi} {voce.get('variante')} già eseguita: si fa una volta sola")
    e = dict(voce, ipotesi=ipotesi, ora=ora)
    dati["esecuzioni"].append(e)
    _scrivi(registro, dati)
    return e
