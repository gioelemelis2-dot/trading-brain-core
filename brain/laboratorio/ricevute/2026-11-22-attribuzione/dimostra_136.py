"""Ricevuta #136 (DGS-15 punto 1): un caso VALIDO di partenza e lo stesso caso con il SOLO periodo errato, con la
causa osservata del rifiuto. Dati e registri inventati, in una cartella temporanea; nessuna rete.
Uso (dalla radice): python3 -s -B brain/laboratorio/ricevute/2026-11-22-attribuzione/dimostra_136.py
"""
import lzma
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from brain.dati.pipeline import dukascopy as DK                    # noqa: E402
from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402


def bi5(base):
    return lzma.compress(DK.RECORD.pack(480 * 60, base, base + 10, base - 10, base + 20, 1.0), format=lzma.FORMAT_ALONE)


def prova(nome, *args):
    try:
        bid, ask, _ = C.carica(*args)
        print(f"{nome}: ACCETTATO · minuti BID {len(bid)}, ASK {len(ask)}")
    except Exception as e:                                          # noqa: BLE001 - si riporta la causa osservata
        print(f"{nome}: RIFIUTATO · {type(e).__name__}: {e}")


print(f"Python {sys.version.split()[0]}")
with tempfile.TemporaryDirectory() as t:
    d = Path(t)
    scheda, registro = d / "H-999.md", d / "registro_prove.json"
    scheda.write_text("# H-999\nregole\n", encoding="utf-8")
    S.sigilla(registro, "H-999", scheda, ["V-T"], "2026-11-22T10:00:00Z")
    b, a = d / "bid", d / "ask"
    b.mkdir()
    a.mkdir()
    for g in (date(2023, 10, 31), date(2023, 11, 14), date(2023, 11, 15), date(2024, 1, 2)):
        (b / f"{g.isoformat()}.bi5").write_bytes(bi5(2000000))
        (a / f"{g.isoformat()}.bi5").write_bytes(bi5(2000300))           # ASK ≠ BID, cartelle distinte
    sig = (registro, "H-999", scheda)
    print("Precondizioni: cartelle BID e ASK distinte, ASK diverso dal BID, sigillo valido.")
    prova("A1 sviluppo 15/11/2023 (valido)", b, a, date(2023, 11, 15), date(2023, 11, 15), "sviluppo", *sig)
    prova("A2 sviluppo 14/11/2023 (solo l'inizio cambiato)", b, a, date(2023, 11, 14), date(2023, 11, 15), "sviluppo", *sig)
    prova("B1 verifica 31/10/2023 (valido)", b, a, date(2023, 10, 31), date(2023, 10, 31), "verifica", *sig)
    prova("B2 verifica fino al 01/11/2023 (solo la fine cambiata)", b, a, date(2023, 10, 31), date(2023, 11, 1),
          "verifica", *sig)
    prova("C1 sviluppo 02/01/2024 (valido)", b, a, date(2024, 1, 2), date(2024, 1, 2), "sviluppo", *sig)
    prova("C2 sviluppo 03/01 → 02/01/2024 (solo l'ordine rovesciato)", b, a, date(2024, 1, 3), date(2024, 1, 2),
          "sviluppo", *sig)
