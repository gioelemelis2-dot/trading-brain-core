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

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


def _t(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def trade_da_journal(path: Path) -> list[dict]:
    """Trade chiusi, in ordine di apertura; applica le correzioni (`corregge`) sostituendo il record corretto."""
    if not path.exists():
        return []
    per_id, ordine = {}, []
    with open(path, encoding="utf-8") as f:
        for riga in f:
            if not riga.strip():
                continue
            rec = json.loads(riga)
            d = rec["dati"]
            bersaglio = d.get("corregge", rec["id"])
            if bersaglio not in per_id:
                ordine.append(bersaglio)
            per_id[bersaglio] = d
    chiusi = [per_id[i] for i in ordine if "chiuso_utc" in per_id[i] and "pnl_conto" in per_id[i]]
    return sorted(chiusi, key=lambda d: d["aperto_utc"])


def metriche_dopo_perdita(trades: list[dict]) -> list[dict]:
    """Per ogni trade che segue una perdita: minuti dalla chiusura della perdita e rapporto tra le size."""
    out = []
    for prec, succ in zip(trades, trades[1:]):
        if float(prec["pnl_conto"]) < 0:
            minuti = (_t(succ["aperto_utc"]) - _t(prec["chiuso_utc"])).total_seconds() / 60
            out.append({"trade": succ.get("id_piattaforma", succ["aperto_utc"]), "tipo": "DERIVATO",
                        "minuti_dopo_perdita": round(minuti, 2),
                        "rapporto_size": float(succ["quantita"]) / float(prec["quantita"])})
    return out


def pattern_r1(trades: list[dict], minuti_max: Optional[float], rapporto_min: Optional[float]) -> dict:
    """R1: ingresso entro `minuti_max` minuti dalla chiusura di una perdita, con size >= `rapporto_min` volte la
    precedente. Restituisce i casi come IPOTESI, oppure lo stato «spento» se i parametri non sono definiti."""
    if minuti_max is None or rapporto_min is None:
        return {"stato": "spento", "motivo": "parametri non definiti dall'utente (regole_personali.toml, P-11 e P-01)"}
    casi = [dict(m, tipo="IPOTESI", interpretazione="compatibile con un rientro impulsivo (R1), non una diagnosi")
            for m in metriche_dopo_perdita(trades)
            if m["minuti_dopo_perdita"] <= minuti_max and m["rapporto_size"] >= rapporto_min]
    return {"stato": "attivo", "parametri": {"minuti_max": minuti_max, "rapporto_min": rapporto_min}, "casi": casi}
