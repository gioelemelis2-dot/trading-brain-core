"""Esecutore di H-002 v3.1 (rottura del range di apertura di Londra su XAUUSD): §6–§8 della scheda.

Sviluppo (screening): per ogni variante dichiarata (V-T, V-S) calcola metriche, confronto casuale (1.000
ripetizioni, seme fisso, 95° percentile), benchmark «compro sempre» e «vendo sempre» sui giorni comuni, scenario di
stress, robustezza (SEMPRE eseguita) con il veto, e il verdetto sui 9 criteri.
Verifica sigillata: solo le varianti indicate (le promosse), una volta sola, con il DSR e N = prove nel registro.

Riga di comando: si rifiuta di partire se la scheda non è sigillata con la stessa impronta (§10: il sigillo viene
prima di qualunque esecuzione); ogni esecuzione viene registrata nel registro delle prove.
Il programma è riusabile: le varianti, le prove di robustezza e il simulatore sono parametri.

Esempio (SOLO dopo il sigillo deciso dall'utente):
  python3 -m brain.laboratorio.esecuzione.esegui_h002 --modalita sviluppo \\
      --rapporto brain/laboratorio/ipotesi/H-002-RISULTATI-SVILUPPO.md
Periodi, ripetizioni, seme e varianti sono costanti di questo file, che è sigillato con la scheda.
"""
import argparse
import hashlib
import os
import sys
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import mean
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
# Periodi FISSI nel codice (DA-26; R11-S1 di Gemini). La fine della verifica è provvisoria finché DA-26 non la fissa.
PERIODO_SVILUPPO = (date(2023, 11, 15), date(2026, 11, 12))
PERIODO_VERIFICA = (date(2005, 1, 1), C.FINE_VERIFICA)
FILE_CODICE = ("brain/laboratorio/simulatori/orb_londra.py", "brain/laboratorio/esecuzione/criteri.py",
               "brain/laboratorio/esecuzione/caricatore.py", "brain/laboratorio/esecuzione/sigillo.py",
               "brain/laboratorio/esecuzione/esegui_h002.py", "brain/laboratorio/backtester/dsr.py",
               "brain/dati/pipeline/dukascopy.py")

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


def _stat_trade(sim, giorni, par) -> dict:
    tr = sim.trade(giorni, par)
    return K.stats_serie([x["r"] for x in tr])


def _arricchisci_metriche(m: dict, tr: list) -> dict:
    out = dict(m)
    if not m.get("n"):
        return out
    out["ic95"] = K.stats_serie([x["r"] for x in tr])["ic95"]
    for lato, k_es, k_ic in (("acquisto", "es_acquisti", "ic95_acquisti"),
                             ("vendita", "es_vendite", "ic95_vendite")):
        st = K.stats_serie([x["r"] for x in tr if x["lato"] == lato])
        out[k_es] = st["errore_std"]
        out[k_ic] = st["ic95"]
    per_anno_stats = {}
    for anno, (n_a, media_a, somma_a) in m.get("per_anno", {}).items():
        st_a = K.stats_serie([x["r"] for x in tr if x["data"].year == anno])
        per_anno_stats[anno] = (n_a, media_a, somma_a, st_a["errore_std"], st_a["ic95"])
    out["per_anno_stats"] = per_anno_stats
    return out


def valuta_variante(sim, prep: _Giorni, par, robustezza: Dict[str, dict], stress: float, ripetizioni: int,
                    seme: int) -> dict:
    giorni = prep(par)
    tr = sim.trade(giorni, par)
    m = _arricchisci_metriche(sim.metriche(tr), tr)
    strategia = {x["data"]: x["r"] for x in tr}
    compro = {x["data"]: x["r"] for x in sim.specchio(giorni, par, lato_fisso="acquisto")}
    vendo = {x["data"]: x["r"] for x in sim.specchio(giorni, par, lato_fisso="vendita")}
    benchmark = K.confronto_benchmark(strategia, compro, vendo)
    comuni = [d for d in sorted(strategia) if d in compro and d in vendo]
    esiti = [(compro[d], vendo[d]) for d in comuni]
    casuale = None
    if esiti:                                   # strategia e casuale sugli STESSI giorni (P5 di Gemini, A2)
        r_comuni = mean(strategia[d] for d in comuni)
        casuale = dict(K.confronto_casuale(esiti, r_comuni, ripetizioni, seme), r_strategia=r_comuni,
                       copertura=len(comuni) / len(strategia))
    stress_stat = _stat_trade(sim, giorni, replace(par, stress=stress))
    r_stress = stress_stat["r_medio"]
    rob, rob_stat = {}, {}
    for nome, cambi in robustezza.items():                       # SEMPRE, qualunque sia il risultato base
        p = replace(par, **cambi)
        st = _stat_trade(sim, prep(p), p)
        rob[nome] = st["r_medio"]
        rob_stat[nome] = st
    veto, motivi = K.veto_robustezza(m.get("r_medio"), rob)
    return {"metriche": m, "casuale": casuale, "benchmark": benchmark, "r_stress": r_stress,
            "r_stress_stat": stress_stat, "robustezza": rob, "robustezza_stat": rob_stat,
            "veto": veto, "motivi_veto": motivi,
            "screening": K.screening(m, casuale or {}, benchmark, veto, r_stress,
                                     es_stress=stress_stat["errore_std"])}


def esegui_sviluppo(bid, ask, varianti=None, robustezza=None, stress: float = STRESS,
                    ripetizioni: int = K.RIPETIZIONI, seme: int = K.SEME, sim=O) -> dict:
    varianti = VARIANTI if varianti is None else varianti
    robustezza = ROBUSTEZZA if robustezza is None else robustezza
    prep = _Giorni(sim, bid, ask)
    base = next(iter(varianti.values()))
    return {"modalita": "sviluppo", "resoconto": sim.resoconto(bid, ask, base),
            "varianti": {v: valuta_variante(sim, prep, par, robustezza.get(v, {}), stress, ripetizioni, seme)
                         for v, par in varianti.items()}}


def esegui_verifica(bid, ask, promosse: List[str], n_prove: int, anni, varianti=None, sim=O) -> dict:
    """Solo le varianti `promosse` girano sul periodo di verifica. V del DSR: Sharpe delle altre promosse.
    `anni`: tutti gli anni solari del periodo (anni senza trade = non positivi; ultimi 5 anni dalla fine)."""
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
        out[v] = {"metriche": _arricchisci_metriche(metriche[v], trade[v]),
                  "verifica": K.verifica(trade[v], n_prove, anni=anni, sharpe_prove=altri)}
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


def _ic(ic) -> str:
    if ic is None:
        return "—"
    return f"[{ic[0]:.4f}, {ic[1]:.4f}]"


def _metriche(m: dict) -> List[str]:
    if not m.get("n"):
        return ["Nessun trade."]
    righe = [f"- Trade: {m['n']} · vinti {m['vinti']:.1%} · R medio netto {_f(m['r_medio'])} "
             f"(ES {_f(m['errore_std'])}, IC 95% {_ic(m.get('ic95'))}) · Sharpe per trade {_f(m['sharpe'])}",
             f"- Drawdown massimo {_f(m['dd_max'], 2)} R · serie peggiore di perdite {m['serie_perdite']}",
             f"- Acquisti: {m['n_acquisti']}, R medio {_f(m['r_acquisti'])} "
             f"(ES {_f(m.get('es_acquisti'))}, IC 95% {_ic(m.get('ic95_acquisti'))}) · "
             f"vendite: {m['n_vendite']}, R medio {_f(m['r_vendite'])} "
             f"(ES {_f(m.get('es_vendite'))}, IC 95% {_ic(m.get('ic95_vendite'))})",
             "", "| anno | trade | R medio | ES | IC 95% | somma R |", "|---|---|---|---|---|---|"]
    per_anno = m.get("per_anno_stats") or {a: (n, mu, somma, None, None) for a, (n, mu, somma) in m["per_anno"].items()}
    righe += [f"| {a} | {n} | {_f(media)} | {_f(es)} | {_ic(ic)} | {_f(somma, 2)} |"
              for a, (n, media, somma, es, ic) in per_anno.items()]
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
            f"{c['n_giorni']} giorni ({c['copertura']:.1%} dei giorni della strategia), {c['ripetizioni']} "
            f"ripetizioni, seme {c['seme']}; R della strategia sugli stessi giorni {_f(c['r_strategia'])}; "
            f"media casuale {_f(c['media_casuale'])}, SD casuale {_f(c.get('sd_casuale'))}, "
            f"95° percentile {_f(c['percentile_95'])}, percentile esatto {_f(c.get('percentile_esatto'), 1)}° "
            f"(z = {_f(c.get('z_casuale'), 2)}).")]
        righe += [f"**Benchmark sui giorni comuni ({b['n_comuni']}):** strategia {_f(b['r_strategia'])} "
                  f"(ES {_f(b.get('es_strategia'))}, IC 95% {_ic(b.get('ic95_strategia'))}), "
                  f"compro sempre {_f(b['r_compro'])} (ES {_f(b.get('es_compro'))}, IC 95% {_ic(b.get('ic95_compro'))}), "
                  f"vendo sempre {_f(b['r_vendo'])} (ES {_f(b.get('es_vendo'))}, IC 95% {_ic(b.get('ic95_vendo'))}); "
                  f"diff vs compro {_f(b.get('diff_compro'))} (ES {_f(b.get('es_diff_compro'))}, IC 95% {_ic(b.get('ic95_diff_compro'))}), "
                  f"diff vs vendo {_f(b.get('diff_vendo'))} (ES {_f(b.get('es_diff_vendo'))}, IC 95% {_ic(b.get('ic95_diff_vendo'))})."]
        rs_stat = x.get("r_stress_stat") or {"errore_std": None, "ic95": None}
        righe += [f"**Scenario di stress (+{STRESS:.2f} USD contro su ingresso e uscita):** R medio {_f(x['r_stress'])} "
                  f"(ES {_f(rs_stat.get('errore_std'))}, IC 95% {_ic(rs_stat.get('ic95'))})."]
        righe += ["", "**Prove di robustezza (fuori da N, sempre eseguite):**", "",
                  "| prova | R medio | ES | IC 95% |", "|---|---|---|---|"]
        rob_stat = x.get("robustezza_stat") or {}
        for k, r in x["robustezza"].items():
            st = rob_stat.get(k) or {}
            righe.append(f"| {k} | {_f(r)} | {_f(st.get('errore_std'))} | {_ic(st.get('ic95'))} |")
        righe += ["", "Veto: " + ("sì — " + "; ".join(x["motivi_veto"]) if x["veto"] else "no"), ""]
        righe += [K.rapporto_screening(f"{v}, screening", x["screening"])]
    return "\n".join(righe) + "\n"


# ---------------------------------------------------------------------------------------------------------------
# Riga di comando
# ---------------------------------------------------------------------------------------------------------------
def impronte_codice() -> Dict[str, str]:
    """Impronte SHA-256 dei file che eseguono la scheda: si registrano al sigillo e si controllano a ogni esecuzione
    (dopo il sigillo il codice non cambia: un errore trovato dopo vuol dire un'ipotesi nuova)."""
    return {f: hashlib.sha256((RADICE / f).read_bytes()).hexdigest() for f in FILE_CODICE}


def _esiti_sviluppo(dati: dict) -> Dict[str, list]:
    esiti: Dict[str, list] = {}
    for e in dati["esecuzioni"]:
        if e["ipotesi"] == IPOTESI and e["ruolo"] == "sviluppo":
            esiti.setdefault(e.get("variante"), []).append(e)
    return esiti


def main(argv=None) -> int:
    """Riga di comando. Nessuna scelta libera (R11 di Gemini): periodi, ripetizioni, seme e varianti sono nel codice,
    che è sigillato; si sceglie solo la modalità (e in verifica si conferma l'elenco delle promosse)."""
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    a.add_argument("--modalita", required=True, choices=C.MODALITA)
    a.add_argument("--varianti", default="", help="verifica: conferma delle varianti promosse, separate da virgole")
    a.add_argument("--rapporto", required=True, type=Path)
    a.add_argument("--registro", type=Path, default=REGISTRO)
    a.add_argument("--scheda", type=Path, default=SCHEDA)
    a.add_argument("--cache", type=Path, default=CACHE)
    a.add_argument("--ora", default=None, help="orario della registrazione (predefinito: adesso, UTC)")
    x = a.parse_args(argv)
    ora = x.ora or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cache = x.cache.resolve()
    try:
        sigillo = S.controlla_sigillo(x.registro, IPOTESI, x.scheda, codice=impronte_codice())   # §10 e codice
        if sorted(sigillo["varianti"]) != sorted(VARIANTI):                    # N giusto (P3 di Gemini)
            raise ValueError(f"il sigillo dichiara {sigillo['varianti']}, l'esecutore esegue {list(VARIANTI)}")
        if x.rapporto.is_dir():                                                # R11-S4: prima di registrare
            raise ValueError(f"--rapporto {x.rapporto} è una cartella")
        x.rapporto.parent.mkdir(parents=True, exist_ok=True)
        if not os.access(x.rapporto.parent, os.W_OK):
            raise ValueError(f"cartella del rapporto non scrivibile: {x.rapporto.parent}")
        promosse = [v.strip() for v in x.varianti.split(",") if v.strip()]
        if x.modalita == "verifica":
            ignote = [v for v in promosse if v not in VARIANTI]
            if not promosse or ignote:
                raise ValueError(f"la verifica richiede --varianti fra {list(VARIANTI)} (ricevute: {x.varianti!r})")
            fatte = [e for e in S.leggi(x.registro)["esecuzioni"] if e["ipotesi"] == IPOTESI
                     and e["ruolo"] == "verifica" and e.get("variante") in promosse]
            if fatte:
                raise ValueError(f"verifica già eseguita per {[e['variante'] for e in fatte]}: si fa una volta sola")
            esiti_sviluppo = _esiti_sviluppo(S.leggi(x.registro))
            da_verificare = [v for v in VARIANTI if esiti_sviluppo.get(v)
                             and all(bool(e.get("promossa")) for e in esiti_sviluppo[v])]          # P1
            if not da_verificare:
                raise ValueError("nessuna variante promossa nello screening registrato: la verifica non si fa")
            if sorted(promosse) != sorted(da_verificare):                         # P2: insieme, una volta
                raise ValueError(f"la verifica si fa una volta sola, con tutte e sole le promosse: {da_verificare}")
            cache_sviluppo = {e.get("cache") for v in da_verificare for e in esiti_sviluppo[v]}
            if cache_sviluppo != {str(cache)}:                                    # R11-S6: stessi dati
                raise ValueError(f"la verifica usa la cache {cache}, lo sviluppo {sorted(map(str, cache_sviluppo))}")
        inizio, fine = PERIODO_SVILUPPO if x.modalita == "sviluppo" else PERIODO_VERIFICA     # R11-S1
        bid, ask, info = C.carica(cache / SIMBOLO, cache / f"{SIMBOLO}_ASK", inizio, fine, x.modalita,
                                  x.registro, IPOTESI, x.scheda)
        if info["giorni_bid_mancanti"] or info["giorni_ask_mancanti"] or not info["minuti_bid"] \
                or not info["minuti_ask"] or info["feriali_vuoti_bid"] or info["feriali_vuoti_ask"]:  # P6, R11-S2
            vuoti = sorted(set(info["feriali_vuoti_bid"]) | set(info["feriali_vuoti_ask"]))
            raise ValueError(f"dati incompleti in {cache}: giorni senza file BID/ASK "
                             f"{info['giorni_bid_mancanti']}/{info['giorni_ask_mancanti']}, minuti "
                             f"{info['minuti_bid']}/{info['minuti_ask']}, giorni feriali vuoti {len(vuoti)} "
                             f"(primi: {vuoti[:10]}): scaricarli o controllarli prima")
        periodo = [inizio.isoformat(), fine.isoformat()]
        traccia = {"periodo": periodo, "cache": str(cache), "dati_sha256": info["dati_sha256"]}
        intestazione = {"ipotesi": IPOTESI, "modalità": x.modalita, "periodo": f"{periodo[0]} → {periodo[1]}",
                        "scheda": f"{x.scheda.name}, SHA-256 {sigillo['scheda_sha256']}",
                        "dati": f"cache Dukascopy {cache} (BID e ASK al minuto), SHA-256 {info['dati_sha256']}",
                        "minuti BID / ASK": f"{info['minuti_bid']} / {info['minuti_ask']}",
                        "registrato": ora}
        if x.modalita == "verifica":
            n = S.n_prove(S.leggi(x.registro))
            for v in promosse:                                    # prima del calcolo: una volta sola, anche se cade
                S.registra_esecuzione(x.registro, IPOTESI, dict(traccia, ruolo="verifica", variante=v, n_prove=n), ora)
            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))
            intestazione["N (prove nel registro)"] = n
            testo = rapporto(ris, f"{IPOTESI}: verifica sigillata", intestazione)
            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()
            for v, r in ris["varianti"].items():                                  # R11-S4: esito nel registro
                ver = r["verifica"]
                quota = [c["valore"] for c in ver["criteri"] if c["nome"].startswith("quota")][0]
                S.registra_esecuzione(x.registro, IPOTESI, {
                    "ruolo": "esito", "variante": v, "promossa": ver["promossa"], "verdetto": ver["verdetto"],
                    "dsr": ver["dsr"], "r_medio": r["metriche"].get("r_medio"),
                    "errore_std": r["metriche"].get("errore_std"), "ic95": r["metriche"].get("ic95"),
                    "quota_anni": quota, "rapporto_sha256": impronta}, ora)
        else:
            ris = esegui_sviluppo(bid, ask)
            testo = rapporto(ris, f"{IPOTESI}: screening sullo sviluppo", intestazione)
            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()
            for v, r in ris["varianti"].items():
                m = r["metriche"]
                S.registra_esecuzione(x.registro, IPOTESI, dict(
                    traccia, ruolo="sviluppo", variante=v, n=m["n"], r_medio=m.get("r_medio"),
                    errore_std=m.get("errore_std"), ic95=m.get("ic95"), sharpe=m.get("sharpe"),
                    promossa=r["screening"]["promossa"], verdetto=r["screening"]["verdetto"],
                    verdetto_attesa=r["screening"]["verdetto_attesa"],
                    ripetizioni=K.RIPETIZIONI, seme=K.SEME, rapporto_sha256=impronta), ora)
                for nome, rm in r["robustezza"].items():
                    S.registra_esecuzione(x.registro, IPOTESI, {"ruolo": "robustezza", "variante": f"{v} {nome}",
                                                                "periodo": periodo, "r_medio": rm}, ora)
        x.rapporto.write_text(testo, encoding="utf-8")
    except (S.NonSigillata, ValueError, OSError) as e:
        print(f"FERMO: {e}", file=sys.stderr)
        return 2
    print(f"rapporto scritto: {x.rapporto}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
