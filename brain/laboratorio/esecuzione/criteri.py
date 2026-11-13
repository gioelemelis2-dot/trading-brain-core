"""Criteri scritti prima (schede delle ipotesi, H-002 v3.1 §6–§8), in forma riusabile.

Lavora solo su risultati in R: liste di trade `{"data": date, "lato": "acquisto"|"vendita", "r": float}` e metriche
nel formato di `simulatori.orb_londra.metriche`. Le soglie sono parametri con i valori di H-002 come predefiniti.
"""
import math
import random
from statistics import mean, stdev
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ..backtester.dsr import DSRCalculator

RIPETIZIONI = 1000
SEME = 20261115


def percentile(valori: Sequence[float], q: float) -> float:
    """Percentile a rango più vicino: il valore di rango ceil(q·n) fra quelli ordinati."""
    if not valori:
        raise ValueError("percentile di un elenco vuoto")
    ordinati = sorted(valori)
    k = max(1, math.ceil(q * len(ordinati) - 1e-9))
    return ordinati[k - 1]


def confronto_casuale(esiti: List[Tuple[float, float]], r_strategia: float, ripetizioni: int = RIPETIZIONI,
                      seme: int = SEME, q: float = 0.95) -> dict:
    """`esiti`: per ogni giorno della strategia, (R se si compra, R se si vende) con gli stessi minuti d'ingresso,
    stop alla stessa distanza dalla parte giusta e le stesse uscite. Ogni ripetizione estrae a caso la direzione di
    ogni giorno e calcola l'R medio; la strategia deve stare SOPRA il percentile q delle ripetizioni."""
    if not esiti:
        raise ValueError("confronto casuale senza giorni")
    rng = random.Random(seme)
    medie = [sum(e[rng.randrange(2)] for e in esiti) / len(esiti) for _ in range(ripetizioni)]
    p = percentile(medie, q)
    return {"n_giorni": len(esiti), "ripetizioni": ripetizioni, "seme": seme, "media_casuale": mean(medie),
            "percentile_95": p, "sopra": r_strategia > p}


def confronto_benchmark(strategia: Dict, compro: Dict, vendo: Dict) -> dict:
    """R medi sui giorni in cui entrano la strategia e tutti e due i benchmark (dizionari data → R)."""
    comuni = sorted(set(strategia) & set(compro) & set(vendo))
    if not comuni:
        return {"n_comuni": 0, "r_strategia": None, "r_compro": None, "r_vendo": None, "batte_entrambi": False}
    rs, rc, rv = (mean(d[g] for g in comuni) for d in (strategia, compro, vendo))
    return {"n_comuni": len(comuni), "r_strategia": rs, "r_compro": rc, "r_vendo": rv,
            "batte_entrambi": rs > rc and rs > rv}


def veto_robustezza(r_base: Optional[float], prove: Dict[str, Optional[float]],
                    quota: float = 0.5) -> Tuple[bool, List[str]]:
    """Veto se in una prova di robustezza l'R medio è ≤ 0 o scende di oltre il 50% rispetto alla base.
    Con la base ≤ 0 (o senza trade) il veto scatta comunque: non c'è nulla da proteggere."""
    motivi = []
    if r_base is None or r_base <= 0:
        motivi.append(f"base non positiva ({r_base})")
    for nome, r in prove.items():
        if r is None or r <= 0:
            motivi.append(f"{nome}: R medio {r} ≤ 0")
        elif r_base is not None and r_base > 0 and r < quota * r_base:
            motivi.append(f"{nome}: R medio {r:.4f} sotto il {quota:.0%} della base {r_base:.4f}")
    return bool(motivi), motivi


def _criterio(nome: str, valore, soglia: str, passa: bool) -> dict:
    return {"nome": nome, "valore": valore, "soglia": soglia, "passa": bool(passa)}


def _ge(x, s) -> bool:
    return x is not None and x >= s


def screening(m: dict, casuale: dict, benchmark: dict, veto: bool, r_stress: Optional[float],
              r_min: float = 0.05, sharpe_min: float = 0.06, trade_min: int = 300, vendite_min: float = -0.05,
              dd_max: float = 12.0) -> dict:
    """I 9 criteri dello screening sullo sviluppo, nell'ordine della scheda. Un valore mancante boccia."""
    r = m.get("r_medio")
    dd = m.get("dd_max")
    criteri = [
        _criterio("R medio netto", r, f"≥ {r_min}", _ge(r, r_min)),
        _criterio("Sharpe per trade", m.get("sharpe"), f"≥ {sharpe_min}", _ge(m.get("sharpe"), sharpe_min)),
        _criterio("numero di trade", m.get("n", 0), f"≥ {trade_min}", m.get("n", 0) >= trade_min),
        _criterio("sopra il 95° percentile del confronto casuale", casuale.get("percentile_95"), "> percentile",
                  casuale.get("sopra", False)),
        _criterio("batte «compro sempre» e «vendo sempre»",
                  (benchmark.get("r_compro"), benchmark.get("r_vendo")), "> entrambi",
                  benchmark.get("batte_entrambi", False)),
        _criterio("R medio delle vendite", m.get("r_vendite"), f"≥ {vendite_min}", _ge(m.get("r_vendite"), vendite_min)),
        _criterio("drawdown massimo (R)", dd, f"< {dd_max}", dd is not None and dd < dd_max),
        _criterio("nessun veto di robustezza", veto, "nessun veto", not veto),
        _criterio("R medio nello scenario di stress", r_stress, "> 0", r_stress is not None and r_stress > 0),
    ]
    return {"promossa": all(c["passa"] for c in criteri), "criteri": criteri}


def quota_anni_positivi(tr: List[dict], anni: Optional[Iterable[int]] = None) -> float:
    """Quota di anni solari con somma degli R > 0. Se `anni` è dato (tutti gli anni del periodo), un anno senza
    trade conta come NON positivo; altrimenti si contano solo gli anni con trade."""
    somme: Dict[int, float] = {}
    for x in tr:
        somme[x["data"].year] = somme.get(x["data"].year, 0.0) + x["r"]
    tutti = sorted(set(anni)) if anni is not None else sorted(somme)
    if not tutti:
        return 0.0
    return sum(1 for a in tutti if somme.get(a, 0.0) > 0) / len(tutti)


def _drawdown(rs: List[float]) -> float:
    cum = picco = dd = 0.0
    for r in rs:
        cum += r
        picco = max(picco, cum)
        dd = max(dd, picco - cum)
    return dd


def _momenti(rs: List[float]) -> Tuple[float, float]:
    """Asimmetria e curtosi (non in eccesso: normale = 3) degli R per trade, con i momenti della popolazione."""
    mu = mean(rs)
    m2 = sum((x - mu) ** 2 for x in rs) / len(rs)
    if m2 <= 0:
        return 0.0, 3.0
    m3 = sum((x - mu) ** 3 for x in rs) / len(rs)
    m4 = sum((x - mu) ** 4 for x in rs) / len(rs)
    return m3 / m2 ** 1.5, m4 / m2 ** 2


def verifica(tr: List[dict], n_prove: int, dsr_min: float = 0.95, quota_anni: float = 0.6, ultimi: int = 5,
             dd_max: float = 15.0, anni: Optional[Iterable[int]] = None) -> dict:
    """I 5 criteri della verifica sigillata. DSR di Bailey e López de Prado sullo Sharpe per trade, con N = prove
    nel registro, T = numero di trade, asimmetria e curtosi degli R per trade."""
    rs = [x["r"] for x in sorted(tr, key=lambda x: x["data"])]
    dsr = sr = None
    if len(rs) > 1 and stdev(rs) > 0:
        sr = mean(rs) / stdev(rs)
        asim, curt = _momenti(rs)
        dsr, _ = DSRCalculator.calculate_dsr_analytical(sr, n_prove, len(rs), asim, curt)
    r = mean(rs) if rs else None
    if rs:
        ultimo = max(x["data"].year for x in tr)
        cumulato = sum(x["r"] for x in tr if x["data"].year > ultimo - ultimi)
    else:
        cumulato = None
    qa = quota_anni_positivi(tr, anni)
    dd = _drawdown(rs) if rs else None
    criteri = [
        _criterio(f"DSR (N = {n_prove})", dsr, f"≥ {dsr_min}", _ge(dsr, dsr_min)),
        _criterio("R medio netto", r, "> 0", r is not None and r > 0),
        _criterio("quota di anni solari positivi", qa, f"≥ {quota_anni:.0%}", qa >= quota_anni),
        _criterio(f"ultimi {ultimi} anni solari, risultato cumulato", cumulato, "> 0",
                  cumulato is not None and cumulato > 0),
        _criterio("drawdown massimo (R)", dd, f"< {dd_max}", dd is not None and dd < dd_max),
    ]
    return {"promossa": all(c["passa"] for c in criteri), "criteri": criteri, "dsr": dsr, "sharpe": sr,
            "n": len(rs)}


def _fmt(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "sì" if v else "no"
    if isinstance(v, float):
        return f"{v:.4f}"
    if isinstance(v, tuple):
        return " / ".join(_fmt(x) for x in v)
    return str(v)


def tabella_criteri(criteri: List[dict]) -> str:
    righe = ["| # | criterio | valore | soglia | esito |", "|---|---|---|---|---|"]
    for k, c in enumerate(criteri, 1):
        righe.append(f"| {k} | {c['nome']} | {_fmt(c['valore'])} | {c['soglia']} | {'✅' if c['passa'] else '❌'} |")
    return "\n".join(righe)


def rapporto_screening(titolo: str, esito: dict) -> str:
    verdetto = "PROMOSSA" if esito["promossa"] else "BOCCIATA"
    return f"### {titolo}: {verdetto}\n\n{tabella_criteri(esito['criteri'])}\n"


def rapporto_verifica(titolo: str, esito: dict) -> str:
    verdetto = "PROMOSSA IN VERIFICA" if esito["promossa"] else "BOCCIATA IN VERIFICA"
    return f"### {titolo}: {verdetto}\n\n{tabella_criteri(esito['criteri'])}\n"
