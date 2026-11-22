"""Registro della riserva di verifica (richiesta 3 a Claude di DGS-20261114-04), 16/11/2026.

PRESENTATO PER RATIFICA: il meccanismo è collaudato su dati inventati; le regole di spesa (α totale, scelta delle
finestre, parte protetta) le decide l'utente. Non va creato il registro vero senza la sua decisione.

Il registro conosce solo DATE, mai prezzi. Il consumo è per calendario: una data letta per una verifica è consumata
per tutto l'universo dichiarato (un «alias» di un altro mercato sulle stesse date viene rifiutato).

File JSON (schema `riserva/1`), solo in aggiunta, scritto in modo atomico sotto blocco esclusivo:
- `riserva`: inizio, fine, α totale, parte protetta (decisi una volta alla creazione);
- `eventi`: prenotazione, rilascio, autorizzazione, quarantena, esito.
Lo stato si RICOSTRUISCE rigiocando gli eventi, con gli stessi controlli usati per scriverli: un file manomesso
(evento sconosciuto, autorizzazione senza prenotazione, contatore j o quota falsificati) viene rifiutato.

Regole (DGS-04 §6):
- prenotazione: solo su date disponibili, dentro la riserva, fuori dalla parte protetta salvo sblocco esplicito;
- rilascio: solo prima dell'autorizzazione; le date tornano disponibili, nulla è speso;
- autorizzazione: va scritta SUBITO PRIMA della prima lettura dei dati. Incrementa j, fissa N globale, hash dei dati,
  numero m di promozioni possibili e la quota α_j = α_tot / [j(j+1)] / m. Da quel momento le date sono consumate per
  sempre: un'interruzione, un esito negativo o non decidibile non restituiscono nulla. Una ripetizione tecnica con la
  stessa identità, gli stessi byte e lo stesso N restituisce la stessa autorizzazione, senza nuovo j;
- esito: uno solo, dopo l'autorizzazione (promossa, bocciata, non decidibile);
- quarantena: date disponibili escluse per qualità o calendario, con motivo.

Schema `riserva/2` (22/11/2026; D-50, DGS-14 Q1-Q2, DGS-15 punto 4):
- rifiuto: una prenotazione aperta si chiude con un rifiuto durevole (per esempio una quota non collaudata),
  PRIMA di qualunque autorizzazione o lettura dei dati. Registra j previsto, m, quota calcolata e collaudata,
  motivo, fase e impronta della scheda. Le date tornano disponibili; j, N e α non cambiano. Una nuova richiesta
  vuole una prenotazione nuova (proposta (b) del messaggio 14, in attesa del parere del DGS);
- autorizzazione: con `quota_attesa` la quota si ricontrolla sotto il blocco (due richieste che avevano visto la
  stessa quota non la spendono due volte); con `impegno` (scheda, codice, metro, finestra, registro dello
  scaricamento, elenco ordinato con le impronte, N, quota) l'impronta dei dati deve essere quella dell'impegno;
- esito: può portare il record del verdetto, da cui il rapporto si rigenera senza rileggere la finestra.
"""
import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Tuple

from .sigillo import _bloccato, _scrivi, ancora_git

SCHEMA = "riserva/2"
ESITI = ("promossa", "bocciata", "non decidibile")
TIPI = ("prenotazione", "rilascio", "autorizzazione", "quarantena", "esito", "rifiuto")


def _d(x) -> date:
    return x if isinstance(x, date) else date.fromisoformat(x)


def _giorni(a: date, b: date):
    g = a
    while g <= b:
        yield g
        g += timedelta(days=1)


def quota(alfa_tot: float, j: int, m: int = 1) -> float:
    return alfa_tot / (j * (j + 1)) / m


def impronta_impegno(impegno: dict) -> str:
    """SHA-256 della forma canonica dell'impegno (chiavi ordinate, nessuno spazio): la stessa su ogni macchina."""
    testo = json.dumps(impegno, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(testo.encode("ascii")).hexdigest()


def _controlla_testa(inizio: date, fine: date, alfa_tot, protetta) -> None:
    """Gli stessi controlli alla creazione e a ogni ricostruzione (#93: un file scritto a mano non li saltava)."""
    if fine < inizio:
        raise ValueError(f"riserva rovesciata {inizio} → {fine}")
    if type(alfa_tot) not in (int, float) or not 0.0 < alfa_tot < 1.0:
        raise ValueError(f"α totale {alfa_tot!r} fuori da (0, 1)")
    if protetta and not (inizio <= protetta[0] <= protetta[1] <= fine):
        raise ValueError(f"parte protetta {protetta} fuori dalla riserva")


class _Stato:
    def __init__(self, testa: dict):
        self.inizio, self.fine = _d(testa["inizio"]), _d(testa["fine"])
        p = testa.get("protetta")
        self.protetta = (_d(p[0]), _d(p[1])) if p else None
        _controlla_testa(self.inizio, self.fine, testa["alfa_tot"], self.protetta)
        self.alfa_tot = float(testa["alfa_tot"])
        self.giorni = {}                       # data -> "prenotato" | "consumato" | "quarantena"
        self.prenotazioni = {}                 # id -> dict(evento, stato, autorizzazione, esito)
        self.j = 0
        self.n_max = 0                         # N globale non scende fra un'autorizzazione e l'altra (#65)

    def _intervallo(self, e) -> Tuple[date, date]:
        a, b = _d(e["inizio"]), _d(e["fine"])
        if b < a:
            raise ValueError(f"intervallo rovesciato {a} → {b}")
        if a < self.inizio or b > self.fine:
            raise ValueError(f"{a} → {b} fuori dalla riserva {self.inizio} → {self.fine}")
        occupate = [g for g in _giorni(a, b) if g in self.giorni]
        if occupate:
            raise ValueError(f"{a} → {b}: {len(occupate)} date non disponibili (dalla {occupate[0]}, "
                             f"{self.giorni[occupate[0]]})")
        return a, b

    def applica(self, e: dict) -> None:
        tipo = e.get("tipo")
        if tipo not in TIPI:
            raise ValueError(f"evento sconosciuto {tipo!r}")
        if tipo == "quarantena":
            a, b = self._intervallo(e)
            if not e.get("motivo"):
                raise ValueError("quarantena senza motivo")
            if self.protetta and a <= self.protetta[1] and b >= self.protetta[0] and not e.get("usa_protetta"):
                raise ValueError(f"quarantena {a} → {b} sulla parte protetta: serve uno sblocco esplicito (#65)")
            for g in _giorni(a, b):
                self.giorni[g] = "quarantena"
            return
        id_ = e.get("id")
        p = self.prenotazioni.get(id_)
        if tipo == "prenotazione":
            if p is not None:
                raise ValueError(f"identità {id_!r} già usata")
            a, b = self._intervallo(e)
            if self.protetta and a <= self.protetta[1] and b >= self.protetta[0] and not e.get("usa_protetta"):
                raise ValueError(f"{a} → {b} tocca la parte protetta {self.protetta[0]} → {self.protetta[1]}: "
                                 f"serve uno sblocco esplicito")
            for g in _giorni(a, b):
                self.giorni[g] = "prenotato"
            self.prenotazioni[id_] = {"evento": e, "stato": "prenotato", "autorizzazione": None, "esito": None}
            return
        if p is None:
            raise ValueError(f"{tipo}: identità {id_!r} sconosciuta")
        a, b = _d(p["evento"]["inizio"]), _d(p["evento"]["fine"])
        if tipo == "rilascio":
            if p["stato"] != "prenotato":
                raise ValueError(f"rilascio di {id_!r} impossibile: è {p['stato']}")
            for g in _giorni(a, b):
                del self.giorni[g]
            p["stato"] = "rilasciato"
        elif tipo == "autorizzazione":
            if p["stato"] != "prenotato":
                raise ValueError(f"autorizzazione di {id_!r} impossibile: è {p['stato']}")   # anche «rifiutato»
            m, n, h = e.get("m"), e.get("n_globale"), e.get("hash_dati")
            if type(m) is not int or m < 1:                                    # #65: True non è un intero valido
                raise ValueError(f"m = {m!r}: serve un intero ≥ 1")
            if type(n) is not int or n < 1 or n < self.n_max:
                raise ValueError(f"N globale = {n!r}: serve un intero ≥ 1 e non minore di {self.n_max}")
            if not isinstance(h, str) or not h:
                raise ValueError("impronta dei dati vuota")
            if "impegno" in e and (not isinstance(e["impegno"], dict) or impronta_impegno(e["impegno"]) != h):
                raise ValueError("l'impronta dei dati non è quella dell'impegno registrato")
            if type(e.get("j")) is not int or e.get("j") != self.j + 1:          # #94: True == 1, 1.0 == 1
                raise ValueError(f"contatore j = {e.get('j')!r}, atteso {self.j + 1}")
            alfa = e.get("alfa_j")                                               # #128: NaN, testo, booleano
            if type(alfa) is not float or not math.isfinite(alfa) or \
                    abs(alfa - quota(self.alfa_tot, self.j + 1, m)) > 1e-15:
                raise ValueError(f"quota alfa_j = {e.get('alfa_j')!r} diversa da α_tot/[j(j+1)]/m")
            self.j += 1
            self.n_max = n
            for g in _giorni(a, b):
                self.giorni[g] = "consumato"
            p["stato"], p["autorizzazione"] = "autorizzato", e
        elif tipo == "rifiuto":
            if p["stato"] != "prenotato":
                raise ValueError(f"rifiuto di {id_!r} impossibile: è {p['stato']}")
            m = e.get("m")
            if type(m) is not int or m < 1:
                raise ValueError(f"m = {m!r}: serve un intero ≥ 1")
            if type(e.get("j_previsto")) is not int or e.get("j_previsto") != self.j + 1:
                raise ValueError(f"j previsto = {e.get('j_previsto')!r}, atteso {self.j + 1}")
            qc, qs = e.get("quota_calcolata"), e.get("quota_collaudata")
            if type(qc) is not float or not math.isfinite(qc) or abs(qc - quota(self.alfa_tot, self.j + 1, m)) > 1e-15:
                raise ValueError(f"quota calcolata {qc!r} diversa da α_tot/[j(j+1)]/m")
            if type(qs) is not float or not math.isfinite(qs):
                raise ValueError(f"quota collaudata {qs!r} non valida")
            for campo in ("motivo", "fase", "impronta_scheda"):
                if not isinstance(e.get(campo), str) or not e[campo]:
                    raise ValueError(f"rifiuto senza {campo}")
            for g in _giorni(a, b):
                del self.giorni[g]
            p["stato"], p["rifiuto"] = "rifiutato", e
        else:                                                          # esito
            if p["stato"] != "autorizzato":
                raise ValueError(f"esito di {id_!r} impossibile: è {p['stato']}")
            if p["esito"] is not None:
                raise ValueError(f"esito di {id_!r} già registrato")
            if e.get("esito") not in ESITI:
                raise ValueError(f"esito {e.get('esito')!r} non in {ESITI}")
            r = e.get("record")
            if r is not None and (not isinstance(r, dict) or r.get("esito") != e["esito"]):
                raise ValueError(f"record del verdetto incoerente con l'esito {e['esito']!r}")
            p["esito"], p["record"] = e["esito"], r


def _leggi(registro: Path) -> dict:
    registro = Path(registro)
    if not registro.exists():
        raise ValueError(f"{registro}: registro della riserva inesistente")
    dati = json.loads(registro.read_text(encoding="utf-8"))
    if dati.get("schema") != SCHEMA or not isinstance(dati.get("eventi"), list):
        raise ValueError(f"{registro}: non è un registro {SCHEMA}")
    return dati


def _ricostruisci(dati: dict) -> _Stato:
    s = _Stato(dati["riserva"])
    for e in dati["eventi"]:
        s.applica(e)
    return s


def _aggiungi(registro: Path, evento: dict) -> dict:
    with _bloccato(registro):
        dati = _leggi(registro)
        _ricostruisci(dati).applica(evento)
        dati["eventi"].append(evento)
        _scrivi(registro, dati)
    return evento


def crea(registro: Path, inizio: date, fine: date, alfa_tot: float, ora: str,
         protetta: Optional[Tuple[date, date]] = None) -> None:
    _controlla_testa(inizio, fine, alfa_tot, protetta)
    with _bloccato(registro):
        if Path(registro).exists():
            raise ValueError(f"{registro}: registro della riserva già creato")
        _scrivi(registro, {"schema": SCHEMA, "riserva": {
            "inizio": inizio.isoformat(), "fine": fine.isoformat(), "alfa_tot": alfa_tot, "ora": ora,
            "protetta": [protetta[0].isoformat(), protetta[1].isoformat()] if protetta else None}, "eventi": []})


def prenota(registro: Path, id_: str, ipotesi: str, inizio: date, fine: date, hash_domanda: str, ora: str,
            usa_protetta: bool = False) -> dict:
    return _aggiungi(registro, {"tipo": "prenotazione", "id": id_, "ipotesi": ipotesi, "inizio": inizio.isoformat(),
                                "fine": fine.isoformat(), "hash_domanda": hash_domanda,
                                "usa_protetta": bool(usa_protetta), "ora": ora})


def rilascia(registro: Path, id_: str, ora: str) -> dict:
    return _aggiungi(registro, {"tipo": "rilascio", "id": id_, "ora": ora})


def autorizza(registro: Path, id_: str, n_globale: int, hash_dati: str, ora: str, m: int = 1,
              impegno: Optional[dict] = None, quota_attesa: Optional[float] = None) -> dict:
    """Da chiamare SUBITO PRIMA della prima lettura dei dati della finestra."""
    with _bloccato(registro):
        dati = _leggi(registro)
        s = _ricostruisci(dati)
        p = s.prenotazioni.get(id_)
        if p is not None and p["stato"] == "autorizzato":
            if p["esito"] is not None:                                         # #65: dopo l'esito non si ripete
                raise ValueError(f"{id_!r} ha già l'esito {p['esito']!r}: nessuna ripetizione tecnica")
            a = p["autorizzazione"]
            if (a["hash_dati"], a["n_globale"], a["m"], a.get("impegno")) == (hash_dati, n_globale, m, impegno):
                return a                                               # ripetizione tecnica: stessa autorizzazione
            raise ValueError(f"{id_!r} già autorizzata con dati, N, m o impegno diversi: non è una ripetizione tecnica")
        if type(m) is not int or m < 1:
            raise ValueError(f"m = {m!r}: serve un intero ≥ 1")
        alfa = quota(s.alfa_tot, s.j + 1, m)
        if quota_attesa is not None and alfa != quota_attesa:          # DGS-15 punto 4: ricontrollo sotto il blocco
            raise ValueError(f"quota cambiata: {alfa!r} invece di {quota_attesa!r} (un'altra apertura è arrivata prima)")
        e = {"tipo": "autorizzazione", "id": id_, "j": s.j + 1, "n_globale": n_globale, "hash_dati": hash_dati,
             "m": m, "alfa_j": alfa, "ora": ora}
        if impegno is not None:
            e["impegno"] = impegno
        s.applica(e)
        dati["eventi"].append(e)
        _scrivi(registro, dati)
    return e


def rendiconta(registro: Path, id_: str, esito: str, ora: str, record: Optional[dict] = None) -> dict:
    e = {"tipo": "esito", "id": id_, "esito": esito, "ora": ora}
    if record is not None:
        e["record"] = record
    return _aggiungi(registro, e)


def quota_prevista(registro: Path, m: int) -> Tuple[int, float]:
    """j e quota della prossima apertura, senza scrivere nulla (controllo prima di autorizzare)."""
    if type(m) is not int or m < 1:
        raise ValueError(f"m = {m!r}: serve un intero ≥ 1")
    s = _ricostruisci(_leggi(registro))
    return s.j + 1, quota(s.alfa_tot, s.j + 1, m)


def rifiuta(registro: Path, id_: str, m: int, quota_collaudata: float, motivo: str, fase: str,
            impronta_scheda: str, ora: str) -> dict:
    """Rifiuto durevole di una prenotazione aperta, PRIMA di autorizzare e di leggere i dati (D-50)."""
    with _bloccato(registro):
        dati = _leggi(registro)
        s = _ricostruisci(dati)
        if type(m) is not int or m < 1:
            raise ValueError(f"m = {m!r}: serve un intero ≥ 1")
        e = {"tipo": "rifiuto", "id": id_, "j_previsto": s.j + 1, "m": m,
             "quota_calcolata": quota(s.alfa_tot, s.j + 1, m), "quota_collaudata": quota_collaudata,
             "motivo": motivo, "fase": fase, "impronta_scheda": impronta_scheda, "ora": ora}
        s.applica(e)
        dati["eventi"].append(e)
        _scrivi(registro, dati)
    return e


def record_esito(registro: Path, id_: str) -> Optional[dict]:
    """Il record del verdetto scritto con l'esito (None se l'esito non c'è ancora): rapporto senza rileggere i dati."""
    p = _ricostruisci(_leggi(registro)).prenotazioni.get(id_)
    if p is None or p["stato"] != "autorizzato":
        raise ValueError(f"{id_!r}: nessuna apertura autorizzata con questa identità")
    return p.get("record")


def quarantena(registro: Path, inizio: date, fine: date, motivo: str, ora: str, usa_protetta: bool = False) -> dict:
    return _aggiungi(registro, {"tipo": "quarantena", "inizio": inizio.isoformat(), "fine": fine.isoformat(),
                                "motivo": motivo, "usa_protetta": bool(usa_protetta), "ora": ora})


def controlla_ancora(registro: Path, radice: Path) -> None:
    """#64 (R13-C1-01): il file della riserva ancorato alla versione su GitHub come il registro delle prove
    (`sigillo.ancora_git`): testa identica, eventi già spinti invariati, solo eventi nuovi in fondo e committati.
    Va chiamato prima di ogni autorizzazione; dopo ogni scrittura il file si committa e si spinge."""
    def continua(remota: dict, head: dict) -> None:
        if head.get("schema") != remota.get("schema") or head.get("riserva") != remota.get("riserva"):
            raise ValueError("la testa della riserva (periodo, α totale, parte protetta) è cambiata rispetto a GitHub")
        vecchi = remota.get("eventi") or []
        if (head.get("eventi") or [])[:len(vecchi)] != vecchi:
            raise ValueError("la riserva non continua la versione su GitHub (eventi cambiati o tolti)")
    ancora_git(registro, radice, continua)


def stato(registro: Path) -> dict:
    """Riconciliazione: giorni per stato, aperture con j, quota ed esito, α speso. Nessun prezzo."""
    s = _ricostruisci(_leggi(registro))
    conta = {"disponibile": 0, "prenotato": 0, "consumato": 0, "quarantena": 0}
    for g in _giorni(s.inizio, s.fine):
        conta[s.giorni.get(g, "disponibile")] += 1
    aperture = sorted(({"id": i, "ipotesi": p["evento"]["ipotesi"], "inizio": p["evento"]["inizio"],
                        "fine": p["evento"]["fine"], "j": p["autorizzazione"]["j"],
                        "n_globale": p["autorizzazione"]["n_globale"], "m": p["autorizzazione"]["m"],
                        "alfa_j": p["autorizzazione"]["alfa_j"], "quota_famiglia": quota(s.alfa_tot, p["autorizzazione"]["j"]),
                        "hash_dati": p["autorizzazione"]["hash_dati"], "ora": p["autorizzazione"]["ora"],
                        "esito": p["esito"]} for i, p in s.prenotazioni.items() if p["stato"] == "autorizzato"),
                      key=lambda x: x["j"])
    protetti = (s.protetta[1] - s.protetta[0]).days + 1 if s.protetta else 0
    rifiuti = [dict(p["rifiuto"]) for i, p in s.prenotazioni.items() if p["stato"] == "rifiutato"]
    return {"giorni": conta, "giorni_protetti": protetti, "aperture": aperture, "alfa_tot": s.alfa_tot, "rifiuti": rifiuti,
            "alfa_speso": sum(a["quota_famiglia"] for a in aperture),
            "prenotazioni_attive": sorted(i for i, p in s.prenotazioni.items() if p["stato"] == "prenotato")}
