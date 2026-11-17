#!/usr/bin/env python3
"""BANCO-02 (#89): file .bi5 inventato con secondi non allineati al minuto (% 60 != 0) o istanti ripetuti.

Verifica cosa accettano dukascopy.decodifica e caricatore.carica su dati inventati (1 giorno in sviluppo).
Stampa la riga finale ATTACCO RIUSCITO oppure ATTACCO RESPINTO.
"""
import argparse
import lzma
import os
import struct
import sys
import tempfile
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

RECORD = struct.Struct(">iiiiif")


def verifica_rete_bloccata() -> None:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato: eseguire con HTTPS_PROXY=http://127.0.0.1:9")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        print(f"[RETE] bloccata ({proxy}): {type(exc).__name__}")
        return
    raise RuntimeError("rete NON bloccata nonostante HTTPS_PROXY")


def crea_bi5_anomalo(con_non_allineati: bool, con_ripetuti: bool) -> bytes:
    """Costruisce un giorno feriale completo in finestra Londra [08:00, 16:45) UTC più anomalie."""
    records = []
    # Base completa: minuti 08:00..16:44 UTC (525 minuti regolari)
    for m in range(8 * 60, 16 * 60 + 45):
        sec = m * 60
        if con_ripetuti and m == 8 * 60:
            # Prima occorrenza alle 08:00:00 (sec=28800)
            records.append((sec, 2000000, 2000000, 1999500, 2000500, 1.0))
            # Seconda occorrenza identica alle 08:00:00 (sec=28800) con chiusura alterata a 2500.000
            records.append((sec, 2000000, 2500000, 1999500, 2500500, 2.0))
        else:
            records.append((sec, 2000000, 2000000, 1999500, 2000500, 1.0))
    if con_non_allineati:
        # Secondi non multipli di 60 (es. 00:10:05, 00:10:17, 00:10:59)
        for sec in (605, 617, 659):
            records.append((sec, 2001000, 2001200, 2000800, 2001500, 1.0))
    buf = bytearray()
    for sec, o, c, lo, hi, vol in records:
        buf += RECORD.pack(sec, o, c, lo, hi, vol)
    return lzma.compress(bytes(buf))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[4])
    args = ap.parse_args()

    verifica_rete_bloccata()
    sys.path.insert(0, str(args.radice.resolve()))
    from brain.dati.pipeline import dukascopy as DK
    from brain.laboratorio.esecuzione import caricatore as C, sigillo as S, esegui_h002 as E

    giorno = date(2024, 1, 2)  # martedì nel periodo sviluppo

    # Caso 1: secondi non allineati al minuto (% 60 != 0)
    raw_non_all = crea_bi5_anomalo(con_non_allineati=True, con_ripetuti=False)
    accettato_dec_non_all = False
    accettato_car_non_all = False
    try:
        dec1 = DK.decodifica(raw_non_all, giorno, DK.SCALA["XAUUSD"])
        off_min = [t for (t, *_rest) in dec1 if t.second != 0]
        accettato_dec_non_all = len(off_min) > 0
        print(f"[CASO 1a decodifica non allineati] record={len(dec1)} secondi!=0={len(off_min)} esempio={off_min}")
    except Exception as exc:
        print(f"[CASO 1a decodifica non allineati] RIFIUTATO: {type(exc).__name__}: {exc}")

    # Caso 2: istanti ripetuti (sec=28800 duplicato con close 2000.0 -> 2500.0)
    raw_rip = crea_bi5_anomalo(con_non_allineati=False, con_ripetuti=True)
    accettato_dec_rip = False
    accettato_car_rip = False
    try:
        dec2 = DK.decodifica(raw_rip, giorno, DK.SCALA["XAUUSD"])
        t0 = datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)
        occ_0800 = [r for r in dec2 if r[0] == t0]
        accettato_dec_rip = len(occ_0800) == 2
        print(f"[CASO 2a decodifica ripetuti] record={len(dec2)} occ_08_00={len(occ_0800)}")
    except Exception as exc:
        print(f"[CASO 2a decodifica ripetuti] RIFIUTATO: {type(exc).__name__}: {exc}")

    with tempfile.TemporaryDirectory(prefix="banco02_d89_") as td_str:
        td = Path(td_str)
        reg = td / "reg.json"
        scheda = td / "scheda.md"
        scheda.write_text("# scheda finta d89\n", encoding="utf-8")
        S.sigilla(reg, E.IPOTESI, scheda, ["V-T", "V-S"], "2026-11-17T00:00:00Z")

        # Test caricatore caso 1
        c1_bid, c1_ask = td / "c1_bid", td / "c1_ask"
        c1_bid.mkdir(); c1_ask.mkdir()
        (c1_bid / f"{giorno.isoformat()}.bi5").write_bytes(raw_non_all)
        (c1_ask / f"{giorno.isoformat()}.bi5").write_bytes(raw_non_all)
        try:
            bid1, _ask1, info1 = C.carica(c1_bid, c1_ask, giorno, giorno, "sviluppo", reg, E.IPOTESI, scheda)
            off_car = [t for t in bid1 if t.second != 0]
            accettato_car_non_all = len(off_car) > 0
            print(f"[CASO 1b caricatore non allineati] minuti={len(bid1)} secondi!=0={len(off_car)} incomp={info1['feriali_incompleti_bid']}")
        except Exception as exc:
            print(f"[CASO 1b caricatore non allineati] RIFIUTATO: {type(exc).__name__}: {exc}")

        # Test caricatore caso 2
        c2_bid, c2_ask = td / "c2_bid", td / "c2_ask"
        c2_bid.mkdir(); c2_ask.mkdir()
        (c2_bid / f"{giorno.isoformat()}.bi5").write_bytes(raw_rip)
        (c2_ask / f"{giorno.isoformat()}.bi5").write_bytes(raw_rip)
        try:
            bid2, _ask2, info2 = C.carica(c2_bid, c2_ask, giorno, giorno, "sviluppo", reg, E.IPOTESI, scheda)
            val_0800 = bid2.get(datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc))
            accettato_car_rip = (val_0800 is not None)
            print(f"[CASO 2b caricatore ripetuti] minuti={len(bid2)} val_08_00={val_0800} incomp={info2['feriali_incompleti_bid']}")
        except Exception as exc:
            print(f"[CASO 2b caricatore ripetuti] RIFIUTATO: {type(exc).__name__}: {exc}")

    if any((accettato_dec_non_all, accettato_car_non_all, accettato_dec_rip, accettato_car_rip)):
        print("ATTACCO RIUSCITO")
    else:
        print("ATTACCO RESPINTO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
