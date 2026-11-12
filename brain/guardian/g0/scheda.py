"""Scheda consultiva pre-trade del Guardian G0 (D-16: calcola, avvisa, registra; non blocca nulla).

Uso: python3 -m g0.scheda <situazione.toml>     (dalla cartella guardian/)

Ordine fisso della scheda: stato di riconciliazione → misure → regole → limiti deterministici → perdita allo stop
→ scenario di stress → riserve (ipotesi o stime) → avvisi → raccomandazione → decisione (dell'utente).
"""
from __future__ import annotations

import sys
import tomllib
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from . import limiti as L
from .strumenti import H_ESEC, Strumento, perdita_allo_stop
from .valori import Valore, combina, ipotesi, misura

ABBREV = {H_ESEC: "H_esec"}
FILE_REGOLE_PERSONALI = Path(__file__).resolve().parent.parent / "regole" / "regole_personali.toml"
# Regole personali con controllo automatico: id → (parametro atteso, dato richiesto)
CONTROLLI_PERSONALI = {
    "P-01": ("rischio_per_trade_frazione", "trade previsto"),
    "P-05": ("limite_personale_giornaliero_frazione", "conto"),
    "P-11": ("pausa_dopo_perdita_minuti", "sessione.minuti_da_ultima_perdita"),
    "P-14": ("ore_sonno_minime", "sessione.ore_sonno"),
    "P-15": ("perdite_consecutive_max", "sessione.perdite_consecutive_oggi"),
}


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
            s["simbolo"], s["classe"], s["valuta_profitto"],
            Decimal(str(s["dimensione_contratto"])) if "dimensione_contratto" in s else None,
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


def _numero(x):
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return None


def _pct(x: Decimal) -> str:
    return f"{(x * 100).quantize(Decimal('0.001'), ROUND_HALF_UP)}%".replace(".", ",")


def _regole_personali(regole: dict, dati: dict, cap, saldo0, eq, pt, st, f_g, tp):
    """Applica SOLO le regole con `confermata = true`. Restituisce (avvisi, righe della sezione).
    Le regole confermate senza controllo automatico restano domande della checklist; i dati di sessione mancanti
    sono dichiarati, non inventati."""
    elenco = regole.get("regola", [])
    conf = [r for r in elenco if r.get("confermata") is True]
    avvisi, righe = [], [f"{len(conf)} regole personali confermate su {len(elenco)} (le altre sono una proposta, non applicate)"]
    sess = dati.get("sessione", {})
    fonte = "regole_personali.toml"
    for r in conf:
        rid = r["id"]
        if rid not in CONTROLLI_PERSONALI:
            righe.append(f"{rid} confermata: controllo non automatico (domanda della checklist)")
            continue
        param, serve = CONTROLLI_PERSONALI[rid]
        v = _numero(r.get("valore"))
        if r.get("parametro") != param or v is None:
            avvisi.append(f"{rid}: regola confermata senza valore numerico per «{param}»: non applicata")
            continue
        soglia = Valore(v, param, "REGOLA", "norma", f"{fonte} {rid}", stato_verifica="V")
        if rid == "P-01":
            if pt is None:
                righe.append(f"{rid}: nessun trade previsto da controllare")
                continue
            frac = combina([pt, cap, soglia], pt.valore / cap.valore, "frazione del capitale", "calcolo deterministico",
                           fonte=f"{rid} rischio del trade previsto")
            righe.append(fmt(frac, f"{rid} rischio del trade previsto (soglia {_pct(v)})"))
            if frac.valore > v:
                avvisi.append(f"{rid}: il trade previsto rischia {_pct(frac.valore)} del capitale iniziale, "
                              f"oltre il limite personale di {_pct(v)}.")
            # Seconda parte di P-01 (regole_personali.toml): «size maggiore del trade precedente dopo una perdita»
            in_perdita, size_prec = sess.get("ultima_operazione_in_perdita"), sess.get("size_precedente")
            if in_perdita is None or size_prec is None:
                righe.append(f"{rid} (seconda parte) non verificata: servono sessione.ultima_operazione_in_perdita "
                             f"e sessione.size_precedente")
            elif not isinstance(in_perdita, bool) or _numero(size_prec) is None or _numero(size_prec) <= 0:
                avvisi.append(f"{rid}: dati di sessione non validi per la seconda parte (vero/falso e size positiva)")
            elif in_perdita and _numero(tp["quantita"]) > _numero(size_prec):
                avvisi.append(f"{rid}: size maggiore della precedente dopo una perdita "
                              f"({_numero(tp['quantita'])} contro {_numero(size_prec)}).")
            else:
                righe.append(f"{rid} (seconda parte): verificata, nessuna violazione")
        elif rid == "P-05":
            # Regola aurea: un limite personale può solo restringere quello della prop firm, mai allargarlo.
            if v >= f_g.valore:
                avvisi.append(f"{rid}: il limite personale giornaliero ({_pct(v)}) non è più stretto del limite della "
                              f"prop firm ({_pct(f_g.valore)}): vale il limite della prop firm; correggere la regola.")
            margine_p = combina([eq, saldo0, cap, soglia], eq.valore - (saldo0.valore - v * cap.valore), eq.unita,
                                "calcolo deterministico", fonte=f"{rid} margine personale giornaliero")
            righe.append(fmt(margine_p, f"{rid} margine rispetto al limite personale giornaliero ({_pct(v)})"))
            if margine_p.valore < 0:
                avvisi.append(f"{rid}: limite personale giornaliero già superato: kill switch personale.")
            else:
                if pt is not None and pt.valore > margine_p.valore:
                    avvisi.append(f"{rid}: se lo stop del trade previsto viene colpito, il limite personale giornaliero viene superato.")
                if st is not None and st.valore > margine_p.valore:
                    avvisi.append(f"{rid}: nello scenario di stress il limite personale giornaliero viene superato.")
        else:
            chiave = serve.split(".")[1]
            if chiave not in sess:
                righe.append(f"{rid} confermata: dato «{serve}» non fornito, regola non verificata")
                continue
            x = _numero(sess[chiave])
            if x is None:
                avvisi.append(f"{rid}: dato «{serve}» non numerico")
                continue
            violata = (x < v) if rid in ("P-11", "P-14") else (x >= v)
            righe.append(f"{rid}: {chiave} = {x} (soglia {v}){' → regola violata' if violata else ''}")
            if violata:
                avvisi.append(f"{rid}: {r['testo']}")
    return avvisi, righe


def scheda(dati: dict, regole_personali: dict | None = None) -> list[str]:
    """`regole_personali`: contenuto del file delle regole personali; se assente si legge FILE_REGOLE_PERSONALI."""
    if regole_personali is None:
        with open(FILE_REGOLE_PERSONALI, "rb") as f:
            regole_personali = tomllib.load(f)
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
    pt = st = None
    if tp:
        pt = _perdita(tp, strumenti, valuta, cambi, fonte)
        sr = L.stop_residui(mg, pt)
        righe += ["", "TRADE PREVISTO", fmt(pt, f"perdita allo stop ({tp['simbolo']})"),
                  fmt(sr, "stop pieni di questa dimensione, dato il margine attuale (posizioni aperte escluse)")]
        if pt.valore > mg.valore:
            avvisi.append("Se lo stop del trade previsto viene colpito, il limite giornaliero viene violato.")
        if pt.valore > mt.valore:
            avvisi.append("Se lo stop del trade previsto viene colpito, il limite totale viene violato.")
    tutte = perdite_aperte + ([pt] if tp else [])
    if tutte:
        st = L.scenario_di_stress(tutte)
        eq_dopo = combina([eq, st], eq.valore - st.valore, valuta, "calcolo deterministico",
                          fonte="equity dopo lo scenario di stress")
        dopo, dopo_t = L.margine(eq_dopo, lg), L.margine(eq_dopo, lt)
        righe += ["", "SCENARIO DI STRESS (tutte le posizioni allo stop, incluso il trade previsto)",
                  fmt(st, "perdita nello scenario"), fmt(dopo, "margine giornaliero dopo lo scenario"),
                  fmt(dopo_t, "margine totale dopo lo scenario")]
        if dopo.valore < 0:
            avvisi.append("Nello scenario di stress il limite giornaliero viene violato.")
        if dopo_t.valore < 0:
            avvisi.append("Nello scenario di stress il limite totale viene violato.")
    rg = dati.get("riserva_gap")
    riserva = ipotesi(rg["valore"] if rg else None, valuta, (rg or {}).get("fonte", "nessun dato di esecuzione"),
                      "H_gap: riserva per gap e slippage oltre lo stop")
    righe += ["", "RISERVE (non deterministiche)", fmt(riserva, "riserva per gap e slippage")]

    avvisi_p, righe_p = _regole_personali(regole_personali, dati, cap, saldo0, eq, pt, st, f_g, tp)
    avvisi += avvisi_p
    righe += ["", "AVVISI"] + (avvisi or ["nessun avviso dalle regole verificate"])
    righe += ["", "REGOLE PERSONALI"] + righe_p
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
