"""Limiti della prop firm, margini, stop residui e scenario di stress (regole: guardian/regole/prop_firm_ftmo.toml).

Definizioni FTMO (pagine ufficiali, 12/11/2026):
- limite giornaliero = saldo alle 00:00 CE(S)T − frazione × capitale iniziale (il primo giorno: capitale iniziale);
- 2-Step: limite totale statico = capitale iniziale × (1 − 0,10);
- 1-Step: limite totale = max(capitale iniziale, massimo saldo alle 00:00 dei giorni precedenti) − 0,10 × capitale;
- Instant: limite totale = max(capitale iniziale, massimo saldo da posizioni chiuse) − 0,10 × capitale;
- violazione: l'EQUITY (saldo + P/L aperto ± swap − commissioni) scende SOTTO il limite.
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Iterable

from . import _toml
from .valori import Valore, combina, regola

FILE_REGOLE = Path(__file__).resolve().parent.parent / "regole" / "prop_firm_ftmo.toml"
PRODOTTI = ("ftmo_2step", "ftmo_1step", "ftmo_instant")


def _frazioni(prodotto: str, file_regole: Path = FILE_REGOLE):
    """Frazioni del limite giornaliero e totale come REGOLE, con fonte e stato di verifica letti dal file."""
    if prodotto not in PRODOTTI:
        raise ValueError(f"prodotto non gestito: {prodotto}")
    with open(file_regole, "rb") as f:
        dati = _toml.load(f)
    p = dati["prodotti"][prodotto]
    fonte = f"{file_regole.name} [{prodotto}] consultato {dati['meta']['consultato']}"
    mdl = p["max_daily_loss"]
    f_g = mdl["frazione"] if isinstance(mdl, dict) else mdl
    s_g = mdl.get("stato", p.get("stato", "C")) if isinstance(mdl, dict) else p.get("stato", "C")
    ml = p["max_loss"]
    f_t = ml["frazione"] if isinstance(ml, dict) else Decimal("0.10")
    s_t = ml.get("stato", "C") if isinstance(ml, dict) else p.get("stato", "C")
    return (regola(f_g, "frazione del capitale iniziale", fonte + " max_daily_loss", s_g),
            regola(f_t, "frazione del capitale iniziale", fonte + " max_loss", s_t))


def _capitale_positivo(capitale_iniziale: Valore) -> None:
    if not (capitale_iniziale.valore.is_finite() and capitale_iniziale.valore > 0):
        raise ValueError(f"il capitale iniziale deve essere positivo ({capitale_iniziale.valore})")


def limite_giornaliero(prodotto: str, capitale_iniziale: Valore, saldo_mezzanotte: Valore) -> Valore:
    _capitale_positivo(capitale_iniziale)
    f_g, _ = _frazioni(prodotto)
    v = saldo_mezzanotte.valore - f_g.valore * capitale_iniziale.valore
    return combina([capitale_iniziale, saldo_mezzanotte, f_g], v, capitale_iniziale.unita, "calcolo deterministico",
                   fonte=f"limite_giornaliero({prodotto})")


def limite_totale(prodotto: str, capitale_iniziale: Valore, saldi_di_riferimento: Iterable[Valore] = ()) -> Valore:
    """`saldi_di_riferimento`: 1-Step → saldi alle 00:00 dei giorni precedenti; Instant → saldi dopo ogni chiusura;
    2-Step → ignorati (limite statico)."""
    _capitale_positivo(capitale_iniziale)
    _, f_t = _frazioni(prodotto)
    saldi = list(saldi_di_riferimento)
    ins = [capitale_iniziale, f_t]
    base = capitale_iniziale.valore
    if prodotto != "ftmo_2step" and saldi:
        base = max([base] + [s.valore for s in saldi])
        ins += saldi
    return combina(ins, base - f_t.valore * capitale_iniziale.valore, capitale_iniziale.unita,
                   "calcolo deterministico", fonte=f"limite_totale({prodotto})")


def margine(equity: Valore, limite: Valore) -> Valore:
    """Distanza dell'equity dal limite. Negativo = limite già violato."""
    return combina([equity, limite], equity.valore - limite.valore, equity.unita, "calcolo deterministico",
                   fonte=f"margine({limite.fonte})")


def stop_residui(margine_: Valore, perdita_per_stop: Valore) -> Valore:
    """Quanti stop pieni si possono subire restando sopra il limite (l'equity può arrivare AL limite, non sotto).
    Condizionato alle condizioni della perdita (H_esec)."""
    if perdita_per_stop.valore <= 0:
        raise ValueError("la perdita per stop deve essere positiva")
    n = max(0, int(margine_.valore // perdita_per_stop.valore)) if margine_.valore >= 0 else 0
    return combina([margine_, perdita_per_stop], Decimal(n), "stop", "calcolo deterministico",
                   fonte="stop_residui")


def scenario_di_stress(perdite_allo_stop: Iterable[Valore], riserve: Iterable[Valore] = ()) -> Valore:
    """Scenario di stress: TUTTE le posizioni raggiungono lo stop ed eseguono secondo H_esec, più le riserve dichiarate.
    Non è un limite superiore se gap o mancata esecuzione superano le riserve; non è «correlazione 1»."""
    ins = list(perdite_allo_stop) + list(riserve)
    if not ins:
        raise ValueError("nessuna posizione")
    unita = {v.unita for v in ins}
    if len(unita) != 1:
        raise ValueError(f"unità diverse: {unita}")
    tot = sum((v.valore for v in ins if v.valore is not None), Decimal(0))
    inc = None if all(v.incertezza == "esatto" for v in ins) else "include riserve non esatte: vedi input"
    return combina(ins, tot, unita.pop(), "calcolo deterministico", fonte="scenario_di_stress", incertezza=inc,
                   condizioni_aggiunte=["scenario di stress: tutte le posizioni raggiungono lo stop insieme"])
