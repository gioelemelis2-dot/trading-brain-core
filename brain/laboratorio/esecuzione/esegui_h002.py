"""Esecutore di H-002 v3.1 (rottura del range di apertura di Londra su XAUUSD): §6–§8 della scheda.

Sviluppo (screening): per ogni variante dichiarata (V-T, V-S) calcola metriche, confronto casuale (1.000
ripetizioni, seme fisso, 95° percentile), benchmark «compro sempre» e «vendo sempre» sui giorni comuni, scenario di
stress, robustezza (SEMPRE eseguita) con il veto, e il verdetto sui 9 criteri.
Verifica sigillata: solo le varianti indicate (le promosse), una volta sola, con il DSR e N = prove nel registro.

Riga di comando: si rifiuta di partire se la scheda non è sigillata con la stessa impronta (§10: il sigillo viene
prima di qualunque esecuzione); ogni esecuzione viene registrata nel registro delle prove.
Il programma è riusabile: le varianti, le prove di robustezza e il simulatore sono parametri.

Esempio (SOLO dopo il sigillo deciso dall'utente):
  python3 -m brain.laboratorio.esecuzione.esegui_h002 --modalita sviluppo --inizio 2023-11-15 --fine 2026-11-12 \\
      --rapporto brain/laboratorio/ipotesi/H-002-RISULTATI-SVILUPPO.md
"""
import argparse
import hashlib
import sys
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from ..simulatori import orb_londra as O
from . import caricatore as C
from . import criteri as K
from . import sigillo as S

RADICE = Path(__file__).resolve().parents[3]
IPOTESI = "H-002"
SCHEDA = RADICE / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md"
REGISTRO = RADICE / "brain" / "laboratorio" / "registro_prove.json"
CACHE = RADICE / "brain" / "dati" / "reali" / "cache_dukascopy"
SIMBOLO = "XAUUSD"

VARIANTI = {"V-T": O.V_T, "V-S": O.V_S}
_RANGE_TETTO = {"range 20'": {"or_minuti": 20}, "range 45'": {"or_minuti": 45},
                "tetto 1,6": {"tetto": 1.6}, "tetto 2,5": {"tetto": 2.5}}
ROBUSTEZZA = {"V-T": dict(_RANGE_TETTO, **{"target 1,2": {"target_r": 1.2}, "target 2,0": {"target_r": 2.0}}),
              "V-S": dict(_RANGE_TETTO)}
STRESS = 0.20


class _Giorni:
    """`prepara` una volta per insieme di parametri che la cambiano (non dipende da target, stress e dimensione)."""

    def __init__(self, sim, bid, ask):
        self.sim, self.bid, self.ask, self.memo = sim, bid, ask, {}

    def __call__(self, par):
        chiave = replace(par, target_r=None, stress=0.0)
        if chiave not in self.memo:
            self.memo[chiave] = self.sim.prepara(self.bid, self.ask, chiave)
        return self.memo[chiave]


def _r_medio(sim, giorni, par) -> Optional[float]:
    return sim.metriche(sim.trade(giorni, par)).get("r_medio")


def valuta_variante(sim, prep: _Giorni, par, robustezza: Dict[str, dict], stress: float, ripetizioni: int,
                    seme: int) -> dict:
    giorni = prep(par)
    tr = sim.trade(giorni, par)
    m = sim.metriche(tr)
    strategia = {x["data"]: x["r"] for x in tr}
    compro = {x["data"]: x["r"] for x in sim.specchio(giorni, par, lato_fisso="acquisto")}
    vendo = {x["data"]: x["r"] for x in sim.specchio(giorni, par, lato_fisso="vendita")}
    benchmark = K.confronto_benchmark(strategia, compro, vendo)
    esiti = [(compro[d], vendo[d]) for d in sorted(strategia) if d in compro and d in vendo]
    casuale = K.confronto_casuale(esiti, m["r_medio"], ripetizioni, seme) if esiti else None
    r_stress = _r_medio(sim, giorni, replace(par, stress=stress))
    rob = {}
    for nome, cambi in robustezza.items():                       # SEMPRE, qualunque sia il risultato base
        p = replace(par, **cambi)
        rob[nome] = _r_medio(sim, prep(p), p)
    veto, motivi = K.veto_robustezza(m.get("r_medio"), rob)
    return {"metriche": m, "casuale": casuale, "benchmark": benchmark, "r_stress": r_stress, "robustezza": rob,
            "veto": veto, "motivi_veto": motivi,
            "screening": K.screening(m, casuale or {}, benchmark, veto, r_stress)}


def esegui_sviluppo(bid, ask, varianti=None, robustezza=None, stress: float = STRESS,
                    ripetizioni: int = K.RIPETIZIONI, seme: int = K.SEME, sim=O) -> dict:
    varianti = VARIANTI if varianti is None else varianti
    robustezza = ROBUSTEZZA if robustezza is None else robustezza
    prep = _Giorni(sim, bid, ask)
    base = next(iter(varianti.values()))
    return {"modalita": "sviluppo", "resoconto": sim.resoconto(bid, ask, base),
            "varianti": {v: valuta_variante(sim, prep, par, robustezza.get(v, {}), stress, ripetizioni, seme)
                         for v, par in varianti.items()}}


def esegui_verifica(bid, ask, promosse: List[str], n_prove: int, varianti=None, sim=O) -> dict:
    """Solo le varianti `promosse` girano sul periodo di verifica. V del DSR: Sharpe delle altre promosse."""
    varianti = VARIANTI if varianti is None else varianti
    ignote = [v for v in promosse if v not in varianti]
    if not promosse or ignote:
        raise ValueError(f"varianti da verificare non valide: {promosse!r} (dichiarate: {list(varianti)})")
    prep = _Giorni(sim, bid, ask)
    trade = {v: sim.trade(prep(varianti[v]), varianti[v]) for v in promosse}
    metriche = {v: sim.metriche(trade[v]) for v in promosse}
    sharpe = {v: metriche[v].get("sharpe") for v in promosse}
    out = {}
    for v in promosse:
        altri = [s for k, s in sharpe.items() if k != v and s is not None]
        out[v] = {"metriche": metriche[v], "verifica": K.verifica(trade[v], n_prove, sharpe_prove=altri)}
    return {"modalita": "verifica", "n_prove": n_prove, "sharpe_prove": sharpe,
            "resoconto": sim.resoconto(bid, ask, varianti[promosse[0]]), "varianti": out}


# ---------------------------------------------------------------------------------------------------------------
# Rapporto in Markdown
# ---------------------------------------------------------------------------------------------------------------
def _f(x, cifre=4) -> str:
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.{cifre}f}"
    return str(x)


def _metriche(m: dict) -> List[str]:
    if not m.get("n"):
        return ["Nessun trade."]
    righe = [f"- Trade: {m['n']} · vinti {m['vinti']:.1%} · R medio netto {_f(m['r_medio'])} · "
             f"Sharpe per trade {_f(m['sharpe'])} · errore standard {_f(m['errore_std'])}",
             f"- Drawdown massimo {_f(m['dd_max'], 2)} R · serie peggiore di perdite {m['serie_perdite']}",
             f"- Acquisti: {m['n_acquisti']}, R medio {_f(m['r_acquisti'])} · "
             f"vendite: {m['n_vendite']}, R medio {_f(m['r_vendite'])}",
             "", "| anno | trade | R medio | somma R |", "|---|---|---|---|"]
    righe += [f"| {a} | {n} | {_f(media)} | {_f(somma, 2)} |" for a, (n, media, somma) in m["per_anno"].items()]
    return righe


def rapporto(ris: dict, titolo: str, info: dict) -> str:
    righe = [f"# {titolo}", ""]
    righe += [f"- **{k}:** {v}" for k, v in info.items()]
    righe += ["", "## Dati e giorni", "", "| motivo | giorni |", "|---|---|"]
    righe += [f"| {k} | {v} |" for k, v in sorted(ris["resoconto"]["giorni_per_motivo"].items())]
    righe += ["", f"Minuti con spread negativo nelle sessioni di base: {ris['resoconto']['minuti_spread_negativo']}."]
    for v, x in ris["varianti"].items():
        righe += ["", f"## Variante {v}", ""] + _metriche(x["metriche"])
        if ris["modalita"] == "verifica":
            righe += ["", K.rapporto_verifica(f"{v}, verifica sigillata", x["verifica"])]
            continue
        c, b = x["casuale"], x["benchmark"]
        righe += ["", "**Confronto casuale:** " + (
            "nessun giorno." if c is None else
            f"{c['n_giorni']} giorni, {c['ripetizioni']} ripetizioni, seme {c['seme']}; media casuale "
            f"{_f(c['media_casuale'])}, 95° percentile {_f(c['percentile_95'])}.")]
        righe += [f"**Benchmark sui giorni comuni ({b['n_comuni']}):** strategia {_f(b['r_strategia'])}, "
                  f"compro sempre {_f(b['r_compro'])}, vendo sempre {_f(b['r_vendo'])}."]
        righe += [f"**Scenario di stress (+{STRESS:.2f} USD contro su ingresso e uscita):** R medio {_f(x['r_stress'])}."]
        righe += ["", "**Prove di robustezza (fuori da N, sempre eseguite):**", "", "| prova | R medio |", "|---|---|"]
        righe += [f"| {k} | {_f(r)} |" for k, r in x["robustezza"].items()]
        righe += ["", "Veto: " + ("sì — " + "; ".join(x["motivi_veto"]) if x["veto"] else "no"), ""]
        righe += [K.rapporto_screening(f"{v}, screening", x["screening"])]
    return "\n".join(righe) + "\n"


# ---------------------------------------------------------------------------------------------------------------
# Riga di comando
# ---------------------------------------------------------------------------------------------------------------
def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--modalita", required=True, choices=C.MODALITA)
    a.add_argument("--inizio", required=True, type=date.fromisoformat)
    a.add_argument("--fine", required=True, type=date.fromisoformat)
    a.add_argument("--varianti", default="", help="verifica: varianti promosse, separate da virgole")
    a.add_argument("--rapporto", required=True, type=Path)
    a.add_argument("--registro", type=Path, default=REGISTRO)
    a.add_argument("--scheda", type=Path, default=SCHEDA)
    a.add_argument("--ipotesi", default=IPOTESI)
    a.add_argument("--cache", type=Path, default=CACHE)
    a.add_argument("--ora", default=None, help="orario della registrazione (predefinito: adesso, UTC)")
    a.add_argument("--ripetizioni", type=int, default=K.RIPETIZIONI)
    a.add_argument("--seme", type=int, default=K.SEME)
    x = a.parse_args(argv)
    ora = x.ora or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        sigillo = S.controlla_sigillo(x.registro, x.ipotesi, x.scheda)          # prima di tutto (§10)
        promosse = [v.strip() for v in x.varianti.split(",") if v.strip()]
        if x.modalita == "verifica":
            ignote = [v for v in promosse if v not in VARIANTI]
            if not promosse or ignote:
                raise ValueError(f"la verifica richiede --varianti fra {list(VARIANTI)} (ricevute: {x.varianti!r})")
            fatte = [e for e in S.leggi(x.registro)["esecuzioni"] if e["ipotesi"] == x.ipotesi
                     and e["ruolo"] == "verifica" and e.get("variante") in promosse]
            if fatte:
                raise ValueError(f"verifica già eseguita per {[e['variante'] for e in fatte]}: si fa una volta sola")
        bid, ask, info = C.carica(x.cache / SIMBOLO, x.cache / f"{SIMBOLO}_ASK", x.inizio, x.fine, x.modalita,
                                  x.registro, x.ipotesi, x.scheda)
        periodo = [x.inizio.isoformat(), x.fine.isoformat()]
        intestazione = {"ipotesi": x.ipotesi, "modalità": x.modalita, "periodo": f"{periodo[0]} → {periodo[1]}",
                        "scheda": f"{x.scheda.name}, SHA-256 {sigillo['scheda_sha256']}",
                        "dati": f"cache Dukascopy {x.cache} (BID e ASK al minuto)",
                        "minuti BID / ASK": f"{info['minuti_bid']} / {info['minuti_ask']}",
                        "giorni di calendario senza file BID / ASK":
                            f"{info['giorni_bid_mancanti']} / {info['giorni_ask_mancanti']}",
                        "registrato": ora}
        if x.modalita == "verifica":
            n = S.n_prove(S.leggi(x.registro))
            for v in promosse:                                    # prima del calcolo: una volta sola, anche se cade
                S.registra_esecuzione(x.registro, x.ipotesi, {"ruolo": "verifica", "variante": v,
                                                              "periodo": periodo, "n_prove": n}, ora)
            ris = esegui_verifica(bid, ask, promosse, n)
            intestazione["N (prove nel registro)"] = n
            testo = rapporto(ris, f"{x.ipotesi}: verifica sigillata", intestazione)
        else:
            ris = esegui_sviluppo(bid, ask, ripetizioni=x.ripetizioni, seme=x.seme)
            testo = rapporto(ris, f"{x.ipotesi}: screening sullo sviluppo", intestazione)
            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()
            for v, r in ris["varianti"].items():
                m = r["metriche"]
                S.registra_esecuzione(x.registro, x.ipotesi, {
                    "ruolo": "sviluppo", "variante": v, "periodo": periodo, "n": m["n"], "r_medio": m.get("r_medio"),
                    "sharpe": m.get("sharpe"), "promossa": r["screening"]["promossa"],
                    "rapporto_sha256": impronta}, ora)
                for nome, rm in r["robustezza"].items():
                    S.registra_esecuzione(x.registro, x.ipotesi, {"ruolo": "robustezza", "variante": f"{v} {nome}",
                                                                  "periodo": periodo, "r_medio": rm}, ora)
        x.rapporto.parent.mkdir(parents=True, exist_ok=True)
        x.rapporto.write_text(testo, encoding="utf-8")
    except (S.NonSigillata, ValueError, OSError) as e:
        print(f"FERMO: {e}", file=sys.stderr)
        return 2
    print(f"rapporto scritto: {x.rapporto}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
