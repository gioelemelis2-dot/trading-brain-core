"""Partizione per DATE in blocchi, con embargo e sigillo dei blocchi di verifica (DA-26).

Sostituisce, per i dati reali, la divisione 70/30 per numero di candele di `DatasetPartitioner`: i confini sono date
UTC scritte PRIMA in un file di partizione (TOML), non una proporzione che dipende da quanti dati arrivano.

File di partizione (schema "partizione-date/1"):
    schema = "partizione-date/1"
    simbolo = "XAUUSD"
    embargo_giorni = 14              # giorni minimi fra la fine di un blocco e l'inizio del successivo
    [[blocco]]
    nome = "verifica_vecchia"        # [a-z][a-z0-9_]*, unico: diventa il nome del file
    ruolo = "verifica"               # "sviluppo" (in chiaro) o "verifica" (sigillato)
    inizio = "2010-01-01"            # UTC, incluso
    fine = "2013-01-01"              # UTC, escluso

Una candela appartiene a un blocco se open_time >= inizio e close_time <= fine; le altre (embargo e fuori dai
blocchi) sono escluse e contate. Ogni blocco è scritto in <nome>.jsonl (righe canoniche, come DatasetPartitioner);
commitment.json riporta per ogni blocco SHA-256 e, per i blocchi di verifica, commitment_hash =
SHA256(nonce_hex + testo), stessa formula di partitioning.py e del journal. Il nonce (256 bit) è scritto per primo,
in modo esclusivo, in una cartella separata: se esiste già ci si ferma, perché un nuovo nonce renderebbe
inverificabile un sigillo già pubblicato.
"""
import hashlib
import json
import re
import secrets
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from brain.guardian.g0 import _toml

from .models import Candle

SCHEMA = "partizione-date/1"
PROTOCOLLO = "SEALED_RESEARCH_COMMITMENT_V3_BLOCCHI_DATE"
RUOLI = ("sviluppo", "verifica")
_NOME = re.compile(r"[a-z][a-z0-9_]{0,40}")
_DATA = re.compile(r"\d{4}-\d{2}-\d{2}")
NONCE = "sealed_nonce.secret"


def _canonico(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def leggi(path: Path) -> Tuple[dict, str]:
    """Legge il file di partizione; restituisce (contenuto, SHA-256 dei byte del file)."""
    dati = Path(path).read_bytes()
    return _toml.loads(dati.decode("utf-8")), hashlib.sha256(dati).hexdigest()


def _data(valore: Any, campo: str) -> datetime:
    if not isinstance(valore, str) or not _DATA.fullmatch(valore):
        raise ValueError(f"{campo}: data non valida {valore!r} (serve \"AAAA-MM-GG\")")
    try:
        g = date.fromisoformat(valore)
    except ValueError:
        raise ValueError(f"{campo}: data non valida {valore!r}") from None
    return datetime(g.year, g.month, g.day, tzinfo=timezone.utc)


def valida(p: dict) -> List[dict]:
    """Controlla il file di partizione e restituisce i blocchi con `inizio_utc` e `fine_utc` (datetime UTC)."""
    if not isinstance(p, dict) or p.get("schema") != SCHEMA:
        raise ValueError(f"schema della partizione: serve {SCHEMA!r}")
    if not isinstance(p.get("simbolo"), str) or not p["simbolo"]:
        raise ValueError("simbolo mancante")
    emb = p.get("embargo_giorni")
    if isinstance(emb, bool) or not isinstance(emb, int) or emb < 0:
        raise ValueError(f"embargo_giorni deve essere un intero >= 0: {emb!r}")
    blocchi = p.get("blocco")
    if not isinstance(blocchi, list) or len(blocchi) < 2:
        raise ValueError("servono almeno due blocchi")
    out, nomi = [], set()
    for i, b in enumerate(blocchi):
        if not isinstance(b, dict):
            raise ValueError(f"blocco {i}: non è una tabella")
        nome = b.get("nome")
        if not isinstance(nome, str) or not _NOME.fullmatch(nome) or nome in nomi:
            raise ValueError(f"blocco {i}: nome non valido o ripetuto {nome!r}")
        nomi.add(nome)
        if b.get("ruolo") not in RUOLI:
            raise ValueError(f"blocco {nome}: ruolo {b.get('ruolo')!r} non in {RUOLI}")
        inizio, fine = _data(b.get("inizio"), f"blocco {nome}.inizio"), _data(b.get("fine"), f"blocco {nome}.fine")
        if inizio >= fine:
            raise ValueError(f"blocco {nome}: inizio {b['inizio']} non precede fine {b['fine']}")
        if out:
            prec = out[-1]
            if inizio < prec["inizio_utc"]:
                raise ValueError(f"blocchi fuori ordine: {nome} prima di {prec['nome']}")
            if inizio < prec["fine_utc"] + timedelta(days=emb):
                raise ValueError(f"blocco {nome}: inizia prima della fine di {prec['nome']} più l'embargo di {emb} giorni")
        out.append(dict(nome=nome, ruolo=b["ruolo"], inizio=b["inizio"], fine=b["fine"], inizio_utc=inizio, fine_utc=fine))
    if not any(b["ruolo"] == "verifica" for b in out):
        raise ValueError("serve almeno un blocco di verifica")
    if not any(b["ruolo"] == "sviluppo" for b in out):
        raise ValueError("serve almeno un blocco di sviluppo")
    return out


def partiziona(candele: List[Candle], partizione: dict, cartella: Path, cartella_nonce: Path,
               partizione_sha256: str) -> Dict[str, Any]:
    """Scrive i blocchi e commitment.json in `cartella`, il nonce in `cartella_nonce`; restituisce il commitment."""
    blocchi = valida(partizione)
    if not candele:
        raise ValueError("nessuna candela")
    simboli = {c.symbol for c in candele}
    if simboli != {partizione["simbolo"]}:
        raise ValueError(f"simbolo delle candele {sorted(simboli)} diverso da quello della partizione "
                         f"{partizione['simbolo']!r}")
    righe: Dict[str, List[str]] = {b["nome"]: [] for b in blocchi}
    prime: Dict[str, Candle] = {}
    ultime: Dict[str, Candle] = {}
    escluse = 0
    for c in candele:
        for b in blocchi:
            if c.open_time >= b["inizio_utc"] and c.close_time <= b["fine_utc"]:
                righe[b["nome"]].append(_canonico(c.to_dict()))
                prime.setdefault(b["nome"], c)
                ultime[b["nome"]] = c
                break
        else:
            escluse += 1
    vuoti = [n for n, r in righe.items() if not r]
    if vuoti:
        raise ValueError(f"blocchi senza candele: {vuoti}")

    cartella_nonce = Path(cartella_nonce)
    cartella_nonce.mkdir(parents=True, exist_ok=True)
    nonce_hex = secrets.token_hex(32)
    with open(cartella_nonce / NONCE, "x", encoding="utf-8") as f:          # mai sovrascrivere un nonce
        f.write(nonce_hex + "\n")

    cartella = Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    descrizione = []
    for b in blocchi:
        testo = "\n".join(righe[b["nome"]]) + "\n"
        (cartella / f"{b['nome']}.jsonl").write_text(testo, encoding="utf-8")
        d = {"nome": b["nome"], "ruolo": b["ruolo"], "inizio": b["inizio"], "fine": b["fine"],
             "candele": len(righe[b["nome"]]), "prima_utc": prime[b["nome"]].open_time.isoformat(),
             "ultima_utc": ultime[b["nome"]].close_time.isoformat(),
             "sha256": hashlib.sha256(testo.encode("utf-8")).hexdigest()}
        if b["ruolo"] == "verifica":
            d["commitment_hash"] = hashlib.sha256((nonce_hex + testo).encode("utf-8")).hexdigest()
        descrizione.append(d)
    commitment = {
        "protocol": PROTOCOLLO, "epistemic_type": "REGOLA", "condition_h": "{H_verifica_sigillata}",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbol": partizione["simbolo"], "timeframe": candele[0].timeframe,
        "partizione_sha256": partizione_sha256, "embargo_giorni": partizione["embargo_giorni"],
        "candele_totali": len(candele), "candele_escluse": escluse, "blocchi": descrizione,
        "status": "SEALED_LOCKED",
    }
    (cartella / "commitment.json").write_text(json.dumps(commitment, ensure_ascii=False, indent=2) + "\n",
                                              encoding="utf-8")
    return commitment


def verifica(cartella: Path, file_nonce: Path) -> Dict[str, Any]:
    """Ricalcola SHA-256 e sigilli di ogni blocco. `commitment` è None per i blocchi di sviluppo."""
    cartella = Path(cartella)
    comm = json.loads((cartella / "commitment.json").read_text(encoding="utf-8"))
    nonce_hex = Path(file_nonce).read_text(encoding="utf-8").strip()
    esito: Dict[str, Dict[str, Optional[bool]]] = {}
    for d in comm["blocchi"]:
        testo = (cartella / f"{d['nome']}.jsonl").read_text(encoding="utf-8")
        ok_sha = secrets.compare_digest(hashlib.sha256(testo.encode("utf-8")).hexdigest(), d["sha256"])
        ok_comm = None
        if d["ruolo"] == "verifica":
            ok_comm = secrets.compare_digest(hashlib.sha256((nonce_hex + testo).encode("utf-8")).hexdigest(),
                                             d["commitment_hash"])
        esito[d["nome"]] = {"sha256": ok_sha, "commitment": ok_comm}
    valido = all(e["sha256"] and e["commitment"] is not False for e in esito.values())
    return {"valido": valido, "blocchi": esito}
