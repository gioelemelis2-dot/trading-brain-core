"""Criteri scritti prima (schede delle ipotesi, H-002 v3.1 §6–§8), in forma riusabile.

Lavora solo su risultati in R: liste di trade `{"data": date, "lato": "acquisto"|"vendita", "r": float}` e metriche
nel formato di `simulatori.orb_londra.metriche`. Le soglie sono parametri con i valori di H-002 come predefiniti.
"""
import math
import random
from statistics import NormalDist, mean, stdev, variance
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ..backtester.dsr import DSRCalculator

RIPETIZIONI = 1000
SEME = 20261115
T_MIN_DSR = 30            # sotto i 30 trade il DSR non si stima (come backtester/dsr.py)
COPERTURA_MIN = 0.9       # quota minima dei giorni della strategia nei confronti (A23, in via prudenziale)
Z95 = NormalDist().inv_cdf(0.975)


def stats_serie(valori: Sequence[float]) -> dict:
    """Media, errore standard e IC 95% (normale) di una serie di R."""
    n = len(valori)
    if n == 0:
        return {"n": 0, "r_medio": None, "errore_std": None, "ic95": None}
    mu = mean(valori)
    if n < 2:
        return {"n": n, "r_medio": mu, "errore_std": None, "ic95": None}
    es = stdev(valori) / math.sqrt(n)
    return {"n": n, "r_medio": mu, "errore_std": es, "ic95": (mu - Z95 * es, mu + Z95 * es)}


def _ic95(r: Optional[float], es: Optional[float]) -> Optional[Tuple[float, float]]:
    if r is None or es is None:
        return None
    return (r - Z95 * es, r + Z95 * es)


def _verdetto_ic(r: Optional[float], es: Optional[float], soglia: float, stretto: bool = False) -> Tuple[bool, str, Optional[Tuple[float, float]]]:
    """Valuta un R medio rispetto alla soglia con eventuale IC 95%: promossa / bocciata / non decidibile."""
    if r is None:
        return False, "bocciata", None
    passa = (r > soglia) if stretto else (r >= soglia)
    ic = _ic95(r, es)
    if ic is None:
        return passa, ("promossa" if passa else "bocciata"), None
    lo, hi = ic
    tutto_sopra = (lo > soglia) if stretto else (lo >= soglia)
    tutto_sotto = (hi <= soglia) if stretto else (hi < soglia)
    if tutto_sopra:
        return True, "promossa", ic
    if tutto_sotto:
        return False, "bocciata", ic
    return passa, "non decidibile", ic


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
    mc = mean(medie)
    sdc = stdev(medie) if len(medie) >= 2 else 0.0
    pct_sotto = 100.0 * sum(1 for m in medie if m < r_strategia) / len(medie)
    z = ((r_strategia - mc) / sdc) if sdc > 0 else None
    return {"n_giorni": len(esiti), "ripetizioni": ripetizioni, "seme": seme, "media_casuale": mc,
            "sd_casuale": sdc, "percentile_95": p, "percentile_esatto": pct_sotto, "z_casuale": z,
            "sopra": r_strategia > p}


def confronto_benchmark(strategia: Dict, compro: Dict, vendo: Dict) -> dict:
    """R medi sui giorni in cui entrano la strategia e tutti e due i benchmark (dizionari data → R)."""
    comuni = sorted(set(strategia) & set(compro) & set(vendo))
    if not comuni:
        return {"n_comuni": 0, "r_strategia": None, "r_compro": None, "r_vendo": None, "batte_entrambi": False,
                "es_strategia": None, "ic95_strategia": None, "es_compro": None, "ic95_compro": None,
                "es_vendo": None, "ic95_vendo": None, "diff_compro": None, "es_diff_compro": None,
                "ic95_diff_compro": None, "diff_vendo": None, "es_diff_vendo": None, "ic95_diff_vendo": None}
    st_s = stats_serie([strategia[g] for g in comuni])
    st_c = stats_serie([compro[g] for g in comuni])
    st_v = stats_serie([vendo[g] for g in comuni])
    st_dc = stats_serie([strategia[g] - compro[g] for g in comuni])
    st_dv = stats_serie([strategia[g] - vendo[g] for g in comuni])
    rs, rc, rv = st_s["r_medio"], st_c["r_medio"], st_v["r_medio"]
    return {"n_comuni": len(comuni), "r_strategia": rs, "r_compro": rc, "r_vendo": rv,
            "batte_entrambi": rs > rc and rs > rv,
            "es_strategia": st_s["errore_std"], "ic95_strategia": st_s["ic95"],
            "es_compro": st_c["errore_std"], "ic95_compro": st_c["ic95"],
            "es_vendo": st_v["errore_std"], "ic95_vendo": st_v["ic95"],
            "diff_compro": st_dc["r_medio"], "es_diff_compro": st_dc["errore_std"], "ic95_diff_compro": st_dc["ic95"],
            "diff_vendo": st_dv["r_medio"], "es_diff_vendo": st_dv["errore_std"], "ic95_diff_vendo": st_dv["ic95"]}


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


def _criterio(nome: str, valore, soglia: str, passa: bool, verdetto: Optional[str] = None,
              errore_std: Optional[float] = None, ic95: Optional[Tuple[float, float]] = None) -> dict:
    v = verdetto if verdetto is not None else ("promossa" if passa else "bocciata")
    return {"nome": nome, "valore": valore, "soglia": soglia, "passa": bool(passa),
            "verdetto": v, "errore_std": errore_std, "ic95": ic95}


def _aggrega_verdetto(criteri: List[dict]) -> str:
    verdetti = [c["verdetto"] for c in criteri]
    if "bocciata" in verdetti:
        return "bocciata"
    if "non decidibile" in verdetti:
        return "non decidibile"
    return "promossa"


def _ge(x, s) -> bool:
    return x is not None and x >= s


def screening(m: dict, casuale: dict, benchmark: dict, veto: bool, r_stress: Optional[float],
              r_min: float = 0.05, sharpe_min: float = 0.06, trade_min: int = 300, vendite_min: float = -0.05,
              dd_max: float = 12.0, copertura_min: float = COPERTURA_MIN,
              es_stress: Optional[float] = None) -> dict:
    """I 9 criteri dello screening sullo sviluppo, nell'ordine della scheda, con verdetto a 3 stati
    (promossa / bocciata / non decidibile quando l'IC 95% dell'R medio contiene la soglia)."""
    r = m.get("r_medio")
    es_r = m.get("errore_std")
    dd = m.get("dd_max")
    n = m.get("n", 0)
    cop_casuale = casuale.get("copertura", 1.0)                                    # R11-S5: copertura vincolante
    cop_bench = (benchmark.get("n_comuni", n) / n) if n else 0.0
    p1, v1, ic1 = _verdetto_ic(r, es_r, r_min, stretto=False)
    p6, v6, ic6 = _verdetto_ic(m.get("r_vendite"), m.get("es_vendite"), vendite_min, stretto=False)
    p9, v9, ic9 = _verdetto_ic(r_stress, es_stress, 0.0, stretto=True)
    # Benchmark appaiato: entrambi > 0; se almeno una differenza è certamente <= 0 (o copertura bassa) -> bocciata
    passa_bench = benchmark.get("batte_entrambi", False) and cop_bench >= copertura_min
    dc, dv = benchmark.get("diff_compro"), benchmark.get("diff_vendo")
    edc, edv = benchmark.get("es_diff_compro"), benchmark.get("es_diff_vendo")
    if cop_bench < copertura_min or not benchmark.get("n_comuni", 1):
        v5, ic5 = "bocciata", None
    elif edc is not None and edv is not None:
        _, v_dc, ic_dc = _verdetto_ic(dc, edc, 0.0, stretto=True)
        _, v_dv, ic_dv = _verdetto_ic(dv, edv, 0.0, stretto=True)
        v5 = "bocciata" if ("bocciata" in (v_dc, v_dv)) else ("promossa" if v_dc == "promossa" and v_dv == "promossa" else "non decidibile")
        ic5 = (ic_dc, ic_dv)
    else:
        v5, ic5 = ("promossa" if passa_bench else "bocciata"), None
    criteri = [
        _criterio("R medio netto", r, f"≥ {r_min}", p1, v1, es_r, ic1),
        _criterio("Sharpe per trade", m.get("sharpe"), f"≥ {sharpe_min}", _ge(m.get("sharpe"), sharpe_min)),
        _criterio("numero di trade", m.get("n", 0), f"≥ {trade_min}", m.get("n", 0) >= trade_min),
        _criterio("sopra il 95° percentile del confronto casuale", (casuale.get("percentile_95"), cop_casuale),
                  f"> percentile, copertura ≥ {copertura_min:.0%}",
                  casuale.get("sopra", False) and cop_casuale >= copertura_min),
        _criterio("batte «compro sempre» e «vendo sempre»",
                  (benchmark.get("r_compro"), benchmark.get("r_vendo"), cop_bench),
                  f"> entrambi, copertura ≥ {copertura_min:.0%}",
                  passa_bench, v5, None, ic5),
        _criterio("R medio delle vendite", m.get("r_vendite"), f"≥ {vendite_min}", p6, v6, m.get("es_vendite"), ic6),
        _criterio("drawdown massimo (R)", dd, f"< {dd_max}", dd is not None and dd < dd_max),
        _criterio("nessun veto di robustezza", veto, "nessun veto", not veto),
        _criterio("R medio nello scenario di stress", r_stress, "> 0", p9, v9, es_stress, ic9),
    ]
    verdetto = _aggrega_verdetto(criteri)
    verdetto_attesa = _aggrega_verdetto([criteri[0], criteri[4], criteri[5], criteri[8]])
    return {"promossa": all(c["passa"] for c in criteri) and verdetto == "promossa",
            "verdetto": verdetto, "verdetto_attesa": verdetto_attesa, "criteri": criteri}


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
             dd_max: float = 15.0, anni: Optional[Iterable[int]] = None,
             sharpe_prove: Optional[List[float]] = None) -> dict:
    """I 5 criteri della verifica sigillata. DSR di Bailey e López de Prado sullo Sharpe per trade, con N = prove
    nel registro, T = numero di trade, asimmetria e curtosi degli R per trade.
    V (varianza degli Sharpe delle prove) come in backtester/dsr.py: max(1/(T − 1), varianza empirica degli Sharpe
    `sharpe_prove` delle ALTRE varianti eseguite sullo stesso periodo più quello di questa)."""
    rs = [x["r"] for x in sorted(tr, key=lambda x: x["data"])]
    dsr = sr = None
    if len(rs) >= T_MIN_DSR and stdev(rs) > 0:                          # R11-S1: niente DSR con pochi trade
        sr = mean(rs) / stdev(rs)
        asim, curt = _momenti(rs)
        v = 1.0 / (len(rs) - 1)
        if sharpe_prove:
            v = max(v, variance(list(sharpe_prove) + [sr]))
        dsr, _ = DSRCalculator.calculate_dsr_analytical(sr, n_prove, len(rs), asim, curt, varianza_sr_prove=v)
    st_r = stats_serie(rs)
    r, es_r = st_r["r_medio"], st_r["errore_std"]
    _, v_r, ic_r = _verdetto_ic(r, es_r, 0.0, stretto=True)
    if rs:
        ultimo = max(anni) if anni is not None else max(x["data"].year for x in tr)     # fine del periodo (P4)
        cumulato = sum(x["r"] for x in tr if x["data"].year > ultimo - ultimi)
    else:
        cumulato = None
    qa = quota_anni_positivi(tr, anni)
    dd = _drawdown(rs) if rs else None
    criteri = [
        _criterio(f"DSR (N = {n_prove})", dsr, f"≥ {dsr_min}", _ge(dsr, dsr_min)),
        _criterio("R medio netto", r, "> 0", r is not None and r > 0, v_r, es_r, ic_r),
        _criterio("quota di anni solari positivi", qa, f"≥ {quota_anni:.0%}", qa >= quota_anni),
        _criterio(f"ultimi {ultimi} anni solari, risultato cumulato", cumulato, "> 0",
                  cumulato is not None and cumulato > 0),
        _criterio("drawdown massimo (R)", dd, f"< {dd_max}", dd is not None and dd < dd_max),
    ]
    verdetto = _aggrega_verdetto(criteri)
    return {"promossa": all(c["passa"] for c in criteri) and verdetto == "promossa", "verdetto": verdetto,
            "criteri": criteri, "dsr": dsr, "sharpe": sr, "r_medio": r, "errore_std": es_r, "ic95": ic_r,
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


def _fmt_ic(ic) -> str:
    if ic is None:
        return "—"
    if isinstance(ic, tuple) and len(ic) == 2 and (isinstance(ic[0], tuple) or ic[0] is None or isinstance(ic[1], tuple)):
        return " ; ".join(_fmt_ic(x) for x in ic)
    return f"[{ic[0]:.4f}, {ic[1]:.4f}]"


def _simbolo_esito(c: dict) -> str:
    v = c.get("verdetto")
    if v == "non decidibile":
        return "⏸️"
    return "✅" if c["passa"] else "❌"


def tabella_criteri(criteri: List[dict]) -> str:
    righe = ["| # | criterio | valore | IC 95% | soglia | esito |", "|---|---|---|---|---|---|"]
    for k, c in enumerate(criteri, 1):
        righe.append(f"| {k} | {c['nome']} | {_fmt(c['valore'])} | {_fmt_ic(c.get('ic95'))} | {c['soglia']} | {_simbolo_esito(c)} |")
    return "\n".join(righe)


def _etichetta_verdetto(esito: dict, suffisso: str = "") -> str:
    v = esito.get("verdetto", "promossa" if esito["promossa"] else "bocciata")
    if v == "promossa":
        return f"PROMOSSA{suffisso}"
    if v == "non decidibile":
        return f"NON DECIDIBILE{suffisso}"
    return f"BOCCIATA{suffisso}"


def rapporto_screening(titolo: str, esito: dict) -> str:
    verdetto = _etichetta_verdetto(esito)
    attesa = esito.get("verdetto_attesa")
    nota = f"\n\nVerdetto sui soli criteri di attesa (`R medio`): **{attesa.upper()}**." if attesa else ""
    return f"### {titolo}: {verdetto}\n\n{tabella_criteri(esito['criteri'])}{nota}\n"


def rapporto_verifica(titolo: str, esito: dict) -> str:
    verdetto = _etichetta_verdetto(esito, " IN VERIFICA")
    return f"### {titolo}: {verdetto}\n\n{tabella_criteri(esito['criteri'])}\n"
