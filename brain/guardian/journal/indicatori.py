"""Indicatori comportamentali dal journal (DA-12): misure oggettive e pattern pre-definiti.

- Le metriche (minuti tra la chiusura di una perdita e l'ingresso successivo; rapporto tra le size) sono DERIVATI
  dei record del journal.
- Il pattern R1 («rientro rapido con size maggiore dopo una perdita») è un'IPOTESI: «compatibile con un rientro
  impulsivo», non una diagnosi. Va validato sui dati dell'utente, con pre-registrazione, attenzione ai confondenti
  (regime di mercato, orario, qualità del setup) e correzione per test multipli se gli indicatori sono più d'uno.
- I parametri (minuti, rapporto di size) li fissa l'UTENTE prima della raccolta. Se non sono numeri confermati,
  l'indicatore resta spento e lo dice.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Optional


def _t(s: str) -> datetime:
    """Orario UTC in ISO-8601: `2026-11-12T09:30:00Z`, con o senza frazioni di secondo (`…:00.120Z`), oppure con
    offset esplicito `+00:00`. Orari senza fuso o con fuso diverso da UTC sono rifiutati."""
    t = datetime.fromisoformat(s)
    if t.tzinfo is None or t.utcoffset() != timedelta(0):
        raise ValueError(f"orario non in UTC: {s!r}")
    return t.astimezone(timezone.utc)


def _dec(x) -> Decimal:
    """Numero del journal come Decimal, dalla sua rappresentazione testuale (niente float)."""
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _secondi(d: timedelta) -> Decimal:
    """Durata esatta in secondi (giorni, secondi e microsecondi interi: nessun arrotondamento binario)."""
    return Decimal(d.days * 86400 + d.seconds) + Decimal(d.microseconds) / Decimal(1_000_000)


def trade_da_journal(path: Path) -> list[dict]:
    """Trade chiusi, in ordine di apertura, nell'ultima versione (correzioni applicate con journal.versioni_finali,
    anche quando una correzione corregge una correzione precedente)."""
    from .journal import versioni_finali
    if not path.exists():
        return []
    chiusi = [d for d in versioni_finali(path).values() if "chiuso_utc" in d and "pnl_conto" in d]
    return sorted(chiusi, key=lambda d: _t(d["aperto_utc"]))


def metriche_dopo_perdita(trades: list[dict]) -> list[dict]:
    """Per ogni trade che segue una perdita: minuti dalla chiusura della perdita e rapporto tra le size."""
    out = []
    for prec, succ in zip(trades, trades[1:]):
        if _dec(prec["pnl_conto"]) < 0:
            minuti = _secondi(_t(succ["aperto_utc"]) - _t(prec["chiuso_utc"])) / Decimal(60)
            out.append({"trade": succ.get("id_piattaforma", succ["aperto_utc"]), "tipo": "DERIVATO",
                        "minuti_dopo_perdita": minuti,
                        "rapporto_size": _dec(succ["quantita"]) / _dec(prec["quantita"])})
    return out


def pattern_r1(trades: list[dict], minuti_max: Optional[Decimal], rapporto_min: Optional[Decimal]) -> dict:
    """R1: ingresso entro `minuti_max` minuti dalla chiusura di una perdita, con size >= `rapporto_min` volte la
    precedente. Restituisce i casi come IPOTESI, oppure lo stato «spento» se i parametri non sono definiti."""
    if minuti_max is None or rapporto_min is None:
        return {"stato": "spento", "motivo": "parametri non definiti dall'utente (regole_personali.toml, P-11 e P-01)"}
    minuti_max, rapporto_min = _dec(minuti_max), _dec(rapporto_min)
    casi = [dict(m, tipo="IPOTESI", interpretazione="compatibile con un rientro impulsivo (R1), non una diagnosi")
            for m in metriche_dopo_perdita(trades)
            if m["minuti_dopo_perdita"] <= minuti_max and m["rapporto_size"] >= rapporto_min]
    return {"stato": "attivo", "parametri": {"minuti_max": minuti_max, "rapporto_min": rapporto_min}, "casi": casi}
