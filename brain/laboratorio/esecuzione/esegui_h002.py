"""Esecutore di H-002 v3.1 (rottura del range di apertura di Londra su XAUUSD): §6–§8 della scheda.

Sviluppo (screening): per ogni variante dichiarata (V-T, V-S) calcola metriche, confronto casuale (1.000
ripetizioni, seme fisso, 95° percentile), benchmark «compro sempre» e «vendo sempre» sui giorni comuni, scenario di
stress, robustezza (SEMPRE eseguita) con il veto, e il verdetto sui 9 criteri.
Verifica sigillata: solo le varianti indicate (le promosse), una volta sola, con il DSR e N = prove nel registro.

Riga di comando: si rifiuta di partire se la scheda non è sigillata con la stessa impronta (§10: il sigillo viene
prima di qualunque esecuzione); ogni esecuzione viene registrata nel registro delle prove.
Il programma è riusabile: le varianti, le prove di robustezza e il simulatore sono parametri.

Esempio (SOLO dopo il sigillo deciso dall'utente), dalla radice del repository, in modalità isolata (#61: niente
PYTHONPATH, pacchetti dell'utente, .pth, sitecustomize; con -I la cartella corrente non è nel percorso, quindi la si
aggiunge esplicitamente):
  python3 -I -S -B -c "import sys; sys.path.insert(0, '.'); from brain.laboratorio.esecuzione.esegui_h002 import main; sys.exit(main())" \\
      --modalita sviluppo --rapporto brain/laboratorio/ipotesi/H-002-RISULTATI-SVILUPPO.md
Prima di ogni esecuzione il registro delle prove deve essere committato e spinto su GitHub (#51, #62).
Periodi, ripetizioni, seme e varianti sono costanti di questo file, che è sigillato con la scheda.
"""
import argparse
import ast
import hashlib
import importlib.util
import os
import re
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
REL_REGISTRO = "brain/laboratorio/registro_prove.json"                    # #86: il solo registro valido
REGISTRO = RADICE / REL_REGISTRO
CACHE = RADICE / "brain" / "dati" / "reali" / "cache_dukascopy"
SIMBOLO = "XAUUSD"
# Periodi FISSI nel codice (DA-26; R11-S1 di Gemini). La fine della verifica è provvisoria finché DA-26 non la fissa.
PERIODO_SVILUPPO = (date(2023, 11, 15), date(2026, 11, 12))
PERIODO_VERIFICA = (date(2005, 1, 1), C.FINE_VERIFICA)
ANCORA_GIT = True              # il registro deve continuare la versione su git (#51); i test con registri temporanei
                               # la spengono. Cambiarla nel codice vero cambia le impronte del codice sigillato.
CONTROLLO_AMBIENTE = True      # #61: python3 -I -S e solo moduli della libreria standard o sigillati; i test che
                               # chiamano main nello stesso processo lo spengono (le prove vere sono in processi a parte)
_ORA_ISO = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


def _file_modulo(radice: Path, modulo: str) -> Optional[Path]:
    p = Path(radice) / modulo.replace(".", "/")
    if p.with_suffix(".py").is_file():
        return p.with_suffix(".py")
    if (p / "__init__.py").is_file():
        return p / "__init__.py"
    return None


def moduli_brain(radice: Path = RADICE, partenza: str = "brain.laboratorio.esecuzione.esegui_h002") -> List[str]:
    """Tutti i file `brain` che l'esecutore può eseguire: chiusura degli import (anche quelli dentro le funzioni),
    più gli `__init__.py` di ogni pacchetto attraversato (R12bis-A3-01, #48: l'elenco scritto a mano ne lasciava
    fuori 14, compreso `esecuzione/__init__.py`). Percorsi relativi alla radice, con «/»."""
    visti, da_fare, file = set(), [partenza], set()
    while da_fare:
        modulo = da_fare.pop()
        if modulo in visti:
            continue
        visti.add(modulo)
        parti = modulo.split(".")
        for k in range(1, len(parti)):                                    # pacchetti attraversati
            init = Path(radice).joinpath(*parti[:k]) / "__init__.py"
            if init.is_file():
                file.add(init)
                da_fare.append(".".join(parti[:k]))
        f = _file_modulo(radice, modulo)
        if f is None:
            continue
        file.add(f)
        pacchetto = modulo if f.name == "__init__.py" else ".".join(parti[:-1])
        for nodo in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
            nomi = []
            if isinstance(nodo, ast.Import):
                nomi = [a.name for a in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                if nodo.level:
                    base = pacchetto.split(".")[:len(pacchetto.split(".")) - (nodo.level - 1)]
                    obiettivo = ".".join(base + ([nodo.module] if nodo.module else []))
                else:
                    obiettivo = nodo.module or ""
                nomi = [obiettivo] + [f"{obiettivo}.{a.name}" for a in nodo.names]
            da_fare += [n for n in nomi if n == "brain" or n.startswith("brain.")]
    return sorted(f.relative_to(radice).as_posix() for f in file)


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
    comuni = [d for d in sorted(strategia) if d in compro and d in vendo]
    esiti = [(compro[d], vendo[d]) for d in comuni]
    casuale = None
    if esiti:                                   # strategia e casuale sugli STESSI giorni (P5 di Gemini, A2)
        r_comuni = mean(strategia[d] for d in comuni)
        casuale = dict(K.confronto_casuale(esiti, r_comuni, ripetizioni, seme), r_strategia=r_comuni,
                       copertura=len(comuni) / len(strategia))
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
        out[v] = {"metriche": metriche[v], "verifica": K.verifica(trade[v], n_prove, anni=anni, sharpe_prove=altri)}
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
            f"{c['n_giorni']} giorni ({c['copertura']:.1%} dei giorni della strategia), {c['ripetizioni']} "
            f"ripetizioni, seme {c['seme']}; R della strategia sugli stessi giorni {_f(c['r_strategia'])}; "
            f"media casuale {_f(c['media_casuale'])}, 95° percentile {_f(c['percentile_95'])}.")]
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
def nomi_robustezza() -> List[str]:
    """Le prove di robustezza che l'esecutore registra (#69: si dichiarano al sigillo)."""
    return sorted({nome for prove in ROBUSTEZZA.values() for nome in prove})


def _dentro(p: Path, cartella: Path) -> bool:
    try:
        p.relative_to(cartella)
        return True
    except ValueError:
        return False


def _libreria_standard() -> Path:
    """La libreria standard VERA: la cartella da cui l'interprete ha caricato `encodings` all'avvio, prima di ogni
    modifica di sys.path. #88: prima la si chiedeva a `sysconfig`, che si può ombrare dalla cartella di lancio."""
    return Path(sys.modules["encodings"].__file__).resolve().parent.parent


def _fuori_standard(p: Path, standard: Path) -> bool:
    """Fuori dalla libreria standard, o dentro ma in site-packages/dist-packages (pacchetti installati)."""
    return bool({"site-packages", "dist-packages"} & set(p.parts)) or not _dentro(p, standard)


def controlla_ambiente(sigillati: Dict[str, str], isolato_richiesto: bool = True) -> None:
    """#61 (R13-B-01): l'ambiente non deve far eseguire codice non sigillato.
    - modalità isolata (`python3 -I -S`): niente PYTHONPATH, pacchetti dell'utente, file .pth, sitecustomize;
    - ogni modulo caricato viene dalla libreria standard (fuori da site-packages) oppure è un file `brain` sigillato,
      con l'impronta del file DAVVERO caricato uguale a quella del sigillo.
    Si chiama all'avvio e di nuovo prima di scrivere i risultati (moduli caricati durante l'esecuzione)."""
    if isolato_richiesto and not (sys.flags.isolated and sys.flags.no_site):
        raise ValueError("eseguire con python3 -I -S -B (modalità isolata, senza site): l'ambiente potrebbe "
                         "far eseguire codice non sigillato")
    if getattr(sys, "pycache_prefix", None):                         # #87: bytecode da una cartella esterna
        raise ValueError("eseguire senza -X pycache_prefix: il bytecode verrebbe letto da un'altra cartella")
    standard = _libreria_standard()
    radice = RADICE.resolve()
    problemi = []
    for nome, modulo in list(sys.modules.items()):
        f = getattr(modulo, "__file__", None)
        if not f:
            continue
        p = Path(f).resolve()
        if _dentro(p, radice / "brain"):
            rel = p.relative_to(radice).as_posix()
            if rel not in sigillati:
                problemi.append(f"{rel}: modulo brain non sigillato")
            elif hashlib.sha256(p.read_bytes()).hexdigest() != sigillati[rel]:
                problemi.append(f"{rel}: diverso da quello sigillato")
            elif Path(importlib.util.cache_from_source(str(p))).exists():
                problemi.append(f"{rel}: c'è un bytecode in __pycache__ (-B non impedisce di leggerlo e non è "
                                f"sigillato): cancellare le cartelle __pycache__ di brain")       # #87
        elif _fuori_standard(p, standard):
            problemi.append(f"{nome} da {p}: fuori dalla libreria standard")
    if problemi:
        raise ValueError(f"ambiente non pulito: {problemi[:10]}")


def impronte_codice(radice: Path = RADICE) -> Dict[str, str]:
    """Impronte SHA-256 di tutti i file `brain` che l'esecutore può eseguire (`moduli_brain`): si registrano al
    sigillo e si controllano a ogni esecuzione (dopo il sigillo il codice non cambia: un errore trovato dopo vuol
    dire un'ipotesi nuova). L'elenco si ricalcola ogni volta: un file nuovo importato cambia le chiavi e ferma tutto."""
    radice = Path(radice)
    return {f: hashlib.sha256((radice / f).read_bytes()).hexdigest() for f in moduli_brain(radice)}


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
        if not _ORA_ISO.fullmatch(ora):                                       # #51: orario nel formato del registro
            raise ValueError(f"--ora {ora!r} non è nel formato AAAA-MM-GGThh:mm:ssZ")
        datetime.strptime(ora, "%Y-%m-%dT%H:%M:%SZ")
        storia: List[dict] = []
        if ANCORA_GIT:
            if x.registro.resolve() != (RADICE / REL_REGISTRO).resolve():     # #86: niente registri alternativi
                raise ValueError(f"il registro deve essere quello canonico del repository ({REL_REGISTRO}), non "
                                 f"{x.registro}")
            S.controlla_ancora(x.registro, RADICE)
            storia = S.versioni_nella_storia(RADICE, REL_REGISTRO)
        sigillo = S.controlla_sigillo(x.registro, IPOTESI, x.scheda, codice=impronte_codice())   # §10 e codice
        if sorted(sigillo["varianti"]) != sorted(VARIANTI):                    # N giusto (P3 di Gemini)
            raise ValueError(f"il sigillo dichiara {sigillo['varianti']}, l'esecutore esegue {list(VARIANTI)}")
        if sorted(sigillo.get("robustezza") or []) != nomi_robustezza():     # #69
            raise ValueError(f"il sigillo dichiara le prove di robustezza {sigillo.get('robustezza')}, l'esecutore "
                             f"esegue {nomi_robustezza()}")
        if CONTROLLO_AMBIENTE:                                                 # #61: all'avvio
            controlla_ambiente(sigillo["codice"])
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
            altrove = sorted({e.get("variante") for d in storia for e in d.get("esecuzioni", [])
                              if e.get("ipotesi") == IPOTESI and e.get("ruolo") == "verifica"} & set(promosse))
            if altrove:                                                       # #86: su un altro ramo o commit
                raise ValueError(f"verifica già eseguita per {altrove} in un'altra versione del registro (storia "
                                 f"git, tutti i rami): si fa una volta sola")
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
            impronte_sviluppo = {e.get("dati_sha256") for v in da_verificare for e in esiti_sviluppo[v]}
            adesso = C.impronta_cache(cache / SIMBOLO, cache / f"{SIMBOLO}_ASK", *PERIODO_SVILUPPO)
            if impronte_sviluppo != {adesso}:                                     # #51: stessa cartella, stessi dati
                raise ValueError(f"i dati dello sviluppo in {cache} non sono più quelli registrati: la cartella è la "
                                 f"stessa ma il contenuto è cambiato")
        inizio, fine = PERIODO_SVILUPPO if x.modalita == "sviluppo" else PERIODO_VERIFICA     # R11-S1
        bid, ask, info = C.carica(cache / SIMBOLO, cache / f"{SIMBOLO}_ASK", inizio, fine, x.modalita,
                                  x.registro, IPOTESI, x.scheda)
        if info["giorni_bid_mancanti"] or info["giorni_ask_mancanti"] or not info["minuti_bid"] \
                or not info["minuti_ask"] or info["feriali_vuoti_bid"] or info["feriali_vuoti_ask"] \
                or info["feriali_incompleti_bid"] or info["feriali_incompleti_ask"]:  # P6, R11-S2, #49
            vuoti = sorted(set(info["feriali_vuoti_bid"]) | set(info["feriali_vuoti_ask"]))
            incompleti = sorted(set(info["feriali_incompleti_bid"]) | set(info["feriali_incompleti_ask"]))
            raise ValueError(f"dati incompleti in {cache}: giorni senza file BID/ASK "
                             f"{info['giorni_bid_mancanti']}/{info['giorni_ask_mancanti']}, minuti "
                             f"{info['minuti_bid']}/{info['minuti_ask']}, giorni feriali vuoti {len(vuoti)} "
                             f"(primi: {vuoti[:10]}), feriali incompleti {len(incompleti)} (primi: {incompleti[:10]}): "
                             f"scaricarli o controllarli prima")
        periodo = [inizio.isoformat(), fine.isoformat()]
        traccia = {"periodo": periodo, "cache": str(cache), "dati_sha256": info["dati_sha256"]}
        intestazione = {"ipotesi": IPOTESI, "modalità": x.modalita, "periodo": f"{periodo[0]} → {periodo[1]}",
                        "scheda": f"{x.scheda.name}, SHA-256 {sigillo['scheda_sha256']}",
                        "dati": f"cache Dukascopy {cache} (BID e ASK al minuto), SHA-256 {info['dati_sha256']}",
                        "minuti BID / ASK": f"{info['minuti_bid']} / {info['minuti_ask']}",
                        "registrato": ora}
        if x.modalita == "verifica":
            n = max([S.n_prove(S.leggi(x.registro))] + [S.n_prove(d) for d in storia])   # #86: N non scende
            S.registra_esecuzioni(x.registro, IPOTESI, [dict(traccia, ruolo="verifica", variante=v, n_prove=n)
                                                        for v in promosse], ora)   # prima del calcolo, tutte (#94)
            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))
            if CONTROLLO_AMBIENTE:                                             # #61, #91: prima dell'esito
                controlla_ambiente(sigillo["codice"])
            intestazione["N (prove nel registro)"] = n
            testo = rapporto(ris, f"{IPOTESI}: verifica sigillata", intestazione)
            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()
            for v, r in ris["varianti"].items():                                  # R11-S4: esito nel registro
                ver = r["verifica"]
                quota = [c["valore"] for c in ver["criteri"] if c["nome"].startswith("quota")][0]
                S.registra_esecuzione(x.registro, IPOTESI, {
                    "ruolo": "esito", "variante": v, "promossa": ver["promossa"], "dsr": ver["dsr"],
                    "r_medio": r["metriche"].get("r_medio"), "quota_anni": quota, "rapporto_sha256": impronta}, ora)
        else:
            ris = esegui_sviluppo(bid, ask)
            if CONTROLLO_AMBIENTE:                                             # #61, #91: prima degli esiti
                controlla_ambiente(sigillo["codice"])
            testo = rapporto(ris, f"{IPOTESI}: screening sullo sviluppo", intestazione)
            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()
            for v, r in ris["varianti"].items():
                m = r["metriche"]
                S.registra_esecuzione(x.registro, IPOTESI, dict(
                    traccia, ruolo="sviluppo", variante=v, n=m["n"], r_medio=m.get("r_medio"), sharpe=m.get("sharpe"),
                    promossa=r["screening"]["promossa"], ripetizioni=K.RIPETIZIONI, seme=K.SEME,
                    rapporto_sha256=impronta), ora)
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
