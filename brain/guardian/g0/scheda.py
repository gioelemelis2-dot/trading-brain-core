"""Scheda consultiva pre-trade del Guardian G0 (D-16: calcola, avvisa, registra; non blocca nulla).

Uso: python3 -m g0.scheda <situazione.toml>     (dalla cartella guardian/)

Ordine fisso della scheda: stato di riconciliazione → misure → regole → limiti deterministici → perdita allo stop
→ scenario di stress → riserve (ipotesi o stime) → avvisi → raccomandazione → decisione (dell'utente).
"""
from __future__ import annotations

import sys
import tomllib
from decimal import Decimal, ROUND_HALF_UP

from . import limiti as L
from .strumenti import H_ESEC, Strumento, perdita_allo_stop
from .valori import Valore, combina, ipotesi, misura

ABBREV = {H_ESEC: "H_esec"}


def fmt(v: Valore, etichetta: str) -> str:
    cond = sorted(ABBREV.get(c, c.split(":")[0]) for c in v.condizioni)
    testa = v.tipo + (" | " + ", ".join(cond) if cond else "")
    if v.valore is None:
        num = "NON STIMABILE"
    else:
        q = Decimal("0.01") if v.unita not in ("stop",) else Decimal("1")
        num = f"{v.valore.quantize(q, ROUND_HALF_UP):,}".replace(",", "_").replace(".", ",").replace("_", ".") + f" {v.unita}"
    inc = "" if v.incertezza in ("esatto", "NON STIMABILE") else f" [{v.incertezza}]"
    return f"[{testa}] {etichetta}: {num}{inc}  (verifica: {v.stato_verifica})"


def _strumenti(dati):
    out = {}
    for s in dati.get("strumento", []):
        out[s["simbolo"]] = Strumento(
            s["simbolo"], s["classe"], s["valuta_profitto"], Decimal(str(s.get("dimensione_contratto", 1))),
            s["fonte"], s.get("stato_verifica", "C"), s.get("valuta_base"),
            Decimal(str(s["passo_tick"])) if "passo_tick" in s else None,
            Decimal(str(s["valore_tick"])) if "valore_tick" in s else None)
    return out


def _perdita(p, strumenti, valuta, cambi, fonte, aperta=False):
    """Trade previsto: dal prezzo d'ingresso allo stop. Posizione APERTA: dal prezzo attuale allo stop, perché
    l'equity include già il P/L flottante; `commissioni` = costi ancora da pagare alla chiusura."""
    s = strumenti[p["simbolo"]]
    if aperta and "prezzo_attuale" not in p:
        raise ValueError(f"posizione aperta {p['simbolo']}: serve prezzo_attuale (la perdita si misura dal prezzo attuale)")
    da = p["prezzo_attuale"] if aperta else p["ingresso"]
    cambio = None
    if s.valuta_profitto != valuta and not (s.classe == "fx" and s.valuta_base == valuta):
        chiave = f"{s.valuta_profitto}/{valuta}"
        if chiave not in cambi:
            raise ValueError(f"manca il cambio {chiave} nella sezione [cambi]")
        cambio = misura(cambi[chiave], chiave, fonte + " [cambi]")
    comm = misura(p["commissioni"], valuta, fonte) if "commissioni" in p else None
    return perdita_allo_stop(s, misura(da, "prezzo", fonte), misura(p["stop"], "prezzo", fonte),
                             misura(p["quantita"], "lotti/contratti", fonte), valuta, cambio, comm)


def scheda(dati: dict) -> list[str]:
    c = dati["conto"]
    valuta, prodotto, fonte = c["valuta"], c["prodotto"], c["fonte"]
    righe = []
    if not c.get("riconciliato", False):
        righe.append("G0 · CONSULTIVO · NON RICONCILIATO con un estratto conto reale: NON usare questi numeri per decidere.")
    else:
        righe.append(f"G0 · CONSULTIVO · riconciliato: {c['riconciliato']}")
    cap = misura(c["capitale_iniziale"], valuta, fonte)
    saldo0 = misura(c["saldo_mezzanotte"], valuta, fonte)
    eq = misura(c["equity"], valuta, fonte)
    rif = [misura(x, valuta, fonte) for x in c.get("saldi_riferimento", [])]
    righe += ["", "MISURE", fmt(cap, "capitale iniziale"), fmt(saldo0, "saldo alle 00:00 CE(S)T"), fmt(eq, "equity attuale")]

    f_g, f_t = L._frazioni(prodotto)
    righe += ["", "REGOLE DELLA PROP FIRM", fmt(f_g, f"perdita giornaliera massima ({prodotto})"),
              fmt(f_t, f"perdita massima ({prodotto})")]

    lg = L.limite_giornaliero(prodotto, cap, saldo0)
    lt = L.limite_totale(prodotto, cap, rif)
    mg, mt = L.margine(eq, lg), L.margine(eq, lt)
    righe += ["", "LIMITI DETERMINISTICI (prima di ogni stima)", fmt(lg, "limite giornaliero"), fmt(mg, "margine giornaliero"),
              fmt(lt, "limite totale"), fmt(mt, "margine totale")]

    strumenti, cambi = _strumenti(dati), {k: v for k, v in dati.get("cambi", {}).items()}
    avvisi = []
    if mg.valore < 0 or mt.valore < 0:
        avvisi.append("Equity già sotto un limite della prop firm: verificare subito sulla piattaforma.")
    perdite_aperte = [_perdita(p, strumenti, valuta, cambi, fonte, aperta=True) for p in dati.get("posizione", [])]
    tp = dati.get("trade_previsto")
    if tp:
        pt = _perdita(tp, strumenti, valuta, cambi, fonte)
        sr = L.stop_residui(mg, pt)
        righe += ["", "TRADE PREVISTO", fmt(pt, f"perdita allo stop ({tp['simbolo']})"),
                  fmt(sr, "stop pieni di questa dimensione, dato il margine attuale (posizioni aperte escluse)")]
        if pt.valore > mg.valore:
            avvisi.append("Se lo stop del trade previsto viene colpito, il limite giornaliero viene violato.")
    tutte = perdite_aperte + ([pt] if tp else [])
    if tutte:
        st = L.scenario_di_stress(tutte)
        eq_dopo = combina([eq, st], eq.valore - st.valore, valuta, "calcolo deterministico",
                          fonte="equity dopo lo scenario di stress")
        dopo = L.margine(eq_dopo, lg)
        righe += ["", "SCENARIO DI STRESS (tutte le posizioni allo stop, incluso il trade previsto)",
                  fmt(st, "perdita nello scenario"), fmt(dopo, "margine giornaliero dopo lo scenario")]
        if dopo.valore < 0:
            avvisi.append("Nello scenario di stress il limite giornaliero viene violato.")
    rg = dati.get("riserva_gap")
    riserva = ipotesi(rg["valore"] if rg else None, valuta, (rg or {}).get("fonte", "nessun dato di esecuzione"),
                      "H_gap: riserva per gap e slippage oltre lo stop")
    righe += ["", "RISERVE (non deterministiche)", fmt(riserva, "riserva per gap e slippage")]

    righe += ["", "AVVISI"] + (avvisi or ["nessun avviso dalle regole della prop firm"])
    righe += ["", "REGOLE PERSONALI", "nessuna regola personale attiva: sono una proposta da confermare (regole/regole_personali.toml)"]
    righe += ["", "RACCOMANDAZIONE", "non entrare" if avvisi else "nessuna obiezione dalle regole verificate",
              "", "DECISIONE: dell'utente, da registrare nel journal (con eventuale deroga e motivo)"]
    return righe


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        return 2
    with open(argv[0], "rb") as f:
        print("\n".join(scheda(tomllib.load(f))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
