"""Mandato R13 · Compito C2: verifica indipendente e primo attacco a potenza_soglia.py e potenza_IA-02.md.

Sonde (>= 5):
- PS-P1: Ricalcolo completamente indipendente (math.erf + bisezione, senza chiamare potenza_soglia.py)
         di TUTTE le celle della tabella di potenza_IA-02.md (32 probabilità + 10 n_per_potenza) su sigma=1.25.
- PS-P2: Verifica matematica vs simulazione indipendente (20.000 prove) + calcolo Binomiale esatto su:
         (a) binario T=1.5 con n=300/450/2500 e righe piccole di tabella (n=10 su +0.50 R, n=101);
         (b) binario asimmetrico T=3.0 (dove Cov(Xbar, S) > 0 riduce/altera scarto vs approssimazione normale);
         (c) modello realistico a 3 stati (stop -1, uscita intermedia N(0, 0.35), target +1.5).
- PS-P3: Errori di dominio / assenza di validazione in potenza_soglia.py (sigma_esiti con mu fuori [-1, target],
         n=1 in simula -> ZeroDivisionError, sigma<=0, potenza<=0 o >=1, tabella mu=0.50 con target=1.5 vs 3.0).
- PS-P4: Impatto quantitativo dell'autocorrelazione AR(1) (rho=0.25) sui falsi positivi e sulla potenza rispetto
         al modello i.i.d. di potenza_IA-02.md.
- PS-P5: Verifica incrociata sulle tre tabelle (sigma=1.0, 1.25, 1.5) e arrotondamento 2.5% -> 3% a mu=0.15 R.

Nuovi mutanti (>= 5): MPS01..MPS06 su potenza_soglia.py in copia isolata.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import math
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from brain.laboratorio.studi import potenza_soglia as P  # noqa: E402


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _inv_phi(p: float) -> float:
    lo, hi = -10.0, 10.0
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if _phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _binom_cdf_ge(n: int, k_min: int, p: float) -> float:
    if k_min <= 0:
        return 1.0
    if k_min > n:
        return 0.0
    tot = 0.0
    for k in range(k_min, n + 1):
        tot += math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))
    return tot


# Valori attesi letteralmente scritti in brain/laboratorio/studi/risultati/potenza_IA-02.md
TABELLA_DOC_PROB = {
    0.00: ("2% / 0%", "0% / 0%", "0% / 0%", "0% / 0%"),
    0.05: ("8% / 0%", "4% / 0%", "1% / 0%", "0% / 0%"),
    0.10: ("24% / 0%", "19% / 0%", "10% / 0%", "2% / 0%"),
    0.15: ("50% / 3%", "50% / 3%", "50% / 3%", "50% / 3%"),
    0.20: ("76% / 10%", "81% / 14%", "90% / 24%", "98% / 52%"),
    0.25: ("92% / 28%", "96% / 43%", "99% / 72%", "100% / 98%"),
    0.30: ("98% / 55%", "100% / 77%", "100% / 97%", "100% / 100%"),
    0.40: ("100% / 93%", "100% / 99%", "100% / 100%", "100% / 100%"),
}
TABELLA_DOC_N = {
    0.20: (443, 4906),
    0.25: (111, 1227),
    0.30: (50, 546),
    0.40: (18, 197),
    0.50: (10, 101),
}


def sonda_ps_p1_verifica_indipendente_tabella() -> dict:
    z95_ind = _inv_phi(0.975)
    z80_ind = _inv_phi(0.80)
    sigma, soglia = 1.25, 0.15
    ns = (300, 500, 1000, 2500)
    diff_prob = []
    for mu, attese in TABELLA_DOC_PROB.items():
        for n, att in zip(ns, attese):
            p_st = _phi((mu - soglia) * math.sqrt(n) / sigma)
            p_lim = _phi((mu - soglia) * math.sqrt(n) / sigma - z95_ind)
            riga_ind = f"{p_st:.0%} / {p_lim:.0%}"
            riga_cod = (f"{P.prob_promozione(mu, sigma, n, soglia, 'stima'):.0%} / "
                        f"{P.prob_promozione(mu, sigma, n, soglia, 'limite'):.0%}")
            if riga_ind != att or riga_cod != att:
                diff_prob.append((mu, n, att, riga_ind, riga_cod))

    diff_n = []
    for mu, (ns_doc, nl_doc) in TABELLA_DOC_N.items():
        ns_ind = math.ceil((z80_ind * sigma / (mu - soglia)) ** 2)
        nl_ind = math.ceil(((z95_ind + z80_ind) * sigma / (mu - soglia)) ** 2)
        ns_cod = P.n_per_potenza(mu, sigma, soglia, 0.8, "stima")
        nl_cod = P.n_per_potenza(mu, sigma, soglia, 0.8, "limite")
        if (ns_ind, nl_ind) != (ns_doc, nl_doc) or (ns_cod, nl_cod) != (ns_doc, nl_doc):
            diff_n.append((mu, (ns_doc, nl_doc), (ns_ind, nl_ind), (ns_cod, nl_cod)))

    p_15_lim = _phi(-z95_ind)
    return {
        "celle_prob_diverse": diff_prob,
        "celle_n_diverse": diff_n,
        "tutte_le_42_voci_corrispondono": not diff_prob and not diff_n,
        "arrotondamento_mu_015_limite": {"valore_esatto": p_15_lim, "formattato_pct": f"{p_15_lim:.0%}"},
    }


def _mc_binario_indip(mu: float, target: float, n: int, soglia: float, regola: str, prove: int, seme: int) -> float:
    z = 1.959963984540054 if regola == "limite" else 0.0
    p = (mu + 1.0) / (target + 1.0)
    rng = random.Random(seme)
    passa = 0
    for _ in range(prove):
        xs = [target if rng.random() < p else -1.0 for _ in range(n)]
        media = sum(xs) / n
        var = sum((x - media) ** 2 for x in xs) / (n - 1)
        if media - z * math.sqrt(var / n) >= soglia:
            passa += 1
    return passa / prove


def _mc_3stati_indip(mu: float, target: float, n: int, soglia: float, regola: str, prove: int, seme: int) -> tuple:
    # Stop=-1 (prob qs), uscita sessione~N(0, 0.35) (prob qm), target=+target (prob qt)
    # Fissiamo qm=0.25 => E[X]=0 sulla sessione, quindi qt*(target+1) = mu + 1 - qm -> qt = (mu + 1 - qm)/(target + 1)
    z = 1.959963984540054 if regola == "limite" else 0.0
    qm = 0.25
    qt = (mu + 1.0 - qm) / (target + 1.0)
    qs = 1.0 - qm - qt
    rng = random.Random(seme)
    passa = 0
    var_teor = qs * (-1.0 - mu) ** 2 + qt * (target - mu) ** 2 + qm * (0.35 ** 2 + (0.0 - mu) ** 2)
    sigma_teor = math.sqrt(var_teor)
    for _ in range(prove):
        xs = []
        for _ in range(n):
            u = rng.random()
            if u < qt:
                xs.append(target)
            elif u < qt + qs:
                xs.append(-1.0)
            else:
                xs.append(rng.gauss(0.0, 0.35))
        media = sum(xs) / n
        var = sum((x - media) ** 2 for x in xs) / (n - 1)
        if media - z * math.sqrt(var / n) >= soglia:
            passa += 1
    return passa / prove, P.prob_promozione(mu, sigma_teor, n, soglia, regola), sigma_teor


def sonda_ps_p2_simulazione_e_scarto_asimmetrico() -> dict:
    # 1. Confronto su binario T=1.5 e su n=10 (+0.50 R stima in potenza_IA-02) vs Binomiale esatta
    p050 = (0.50 + 1.0) / (1.5 + 1.0)  # 0.6
    # Con n=10: vinte*1.5 - (10-vinte) >= 1.5 <=> 2.5*vinte >= 11.5 <=> vinte >= 5
    bin_n10 = _binom_cdf_ge(10, 5, p050)
    norm_n10 = P.prob_promozione(0.50, P.sigma_esiti(0.50, 1.5), 10, 0.15, "stima")
    # Con n=10 e sigma=1.25 usata dal documento
    norm_n10_doc = P.prob_promozione(0.50, 1.25, 10, 0.15, "stima")

    # 2. Confronto su T=1.5 per n=450 e n=2500
    casi_15 = {}
    for mu in (0.10, 0.15, 0.20, 0.25):
        sig = P.sigma_esiti(mu, 1.5)
        for n in (450, 2500):
            for reg in ("stima", "limite"):
                teo = P.prob_promozione(mu, sig, n, 0.15, reg)
                mc = _mc_binario_indip(mu, 1.5, n, 0.15, reg, prove=5000, seme=42 + n)
                casi_15[f"mu={mu}_n={n}_{reg}"] = {"teo": round(teo, 4), "mc": round(mc, 4), "diff": round(mc - teo, 4)}

    # 3. Caso fortemente asimmetrico (T=4.0, n=30, reg='limite'): Cov(Xbar, S) > 0 + asimmetria fanno divergere limite!
    sig4 = P.sigma_esiti(0.15, 4.0)
    teo4 = P.prob_promozione(0.15, sig4, 30, 0.15, "limite")
    mc4 = _mc_binario_indip(0.15, 4.0, 30, 0.15, "limite", prove=10000, seme=99)

    # 4. Modello realistico a 3 stati (stop=-1, uscita intermedia N(0,0.35), target=+1.5)
    mc3, teo3, sig3 = _mc_3stati_indip(0.20, 1.5, 450, 0.15, "stima", prove=5000, seme=77)
    mc3_lim, teo3_lim, _ = _mc_3stati_indip(0.25, 1.5, 2500, 0.15, "limite", prove=5000, seme=78)
    return {
        "n10_mu050_bin_esatta": round(bin_n10, 4),
        "n10_mu050_norm_sigma_esiti": round(norm_n10, 4),
        "n10_mu050_norm_sigma_125": round(norm_n10_doc, 4),
        "scarto_massimo_T1_5_450_2500": max(abs(v["diff"]) for v in casi_15.values()),
        "asimmetrico_T4_n30_mu015_limite": {"teo": round(teo4, 4), "mc_10k": round(mc4, 4), "diff": round(mc4 - teo4, 4)},
        "modello_3stati": {
            "sigma_teor": round(sig3, 4),
            "mu020_n450_stima": {"mc": round(mc3, 4), "teo": round(teo3, 4)},
            "mu025_n2500_limite": {"mc": round(mc3_lim, 4), "teo": round(teo3_lim, 4)},
        },
    }


def sonda_ps_p3_errori_dominio_e_bordi() -> dict:
    esiti = {}
    for nome, fn in (
        ("sigma_esiti_mu_fuori_range", lambda: P.sigma_esiti(-1.5, 1.5)),
        ("sigma_esiti_target_neg", lambda: P.sigma_esiti(0.2, -2.0)),
        ("simula_n_1", lambda: P.simula(0.2, 1.5, 1, 0.15, "stima", prove=10)),
        ("prob_sigma_zero", lambda: P.prob_promozione(0.2, 0.0, 100, 0.15, "stima")),
        ("n_per_potenza_1_0", lambda: P.n_per_potenza(0.3, 1.25, 0.15, 1.0, "stima")),
    ):
        try:
            v = fn()
            esiti[nome] = f"OK:{v}"
        except Exception as exc:
            esiti[nome] = f"{type(exc).__name__}:{exc}"
    return esiti


def sonda_ps_p4_impatto_autocorrelazione() -> dict:
    # Serie AR(1) giornaliera con rho=0.25, deviazione marginale sigma=1.25, n=450 e n=2500
    rho = 0.25
    sigma = 1.25
    sd_inn = sigma * math.sqrt(1.0 - rho ** 2)
    z95 = 1.959963984540054

    def sim_ar1(mu: float, n: int, regola: str, prove: int = 4000, seme: int = 123) -> float:
        z = z95 if regola == "limite" else 0.0
        rng = random.Random(seme)
        passa = 0
        for _ in range(prove):
            x = rng.gauss(0.0, sigma)
            xs = []
            for _ in range(n):
                x = rho * x + rng.gauss(0.0, sd_inn)
                xs.append(mu + x)
            media = sum(xs) / n
            var = sum((v - media) ** 2 for v in xs) / (n - 1)
            if media - z * math.sqrt(var / n) >= 0.15:
                passa += 1
        return passa / prove

    fp_mu010_iid = P.prob_promozione(0.10, 1.25, 450, 0.15, "stima")
    fp_mu010_ar1 = sim_ar1(0.10, 450, "stima", seme=11)
    lim_mu025_iid = P.prob_promozione(0.25, 1.25, 2500, 0.15, "limite")
    lim_mu025_ar1 = sim_ar1(0.25, 2500, "limite", seme=12)
    return {
        "mu010_n450_stima_iid": round(fp_mu010_iid, 4),
        "mu010_n450_stima_AR1_rho025": round(fp_mu010_ar1, 4),
        "mu025_n2500_limite_iid": round(lim_mu025_iid, 4),
        "mu025_n2500_limite_AR1_rho025": round(lim_mu025_ar1, 4),
    }


def sonda_ps_p5_consistenza_altri_sigma() -> dict:
    # Controllo monotonia su sigma=1.0, 1.25, 1.5 e coerenza n_per_potenza
    bad = []
    for sig in (1.0, 1.25, 1.5):
        for reg in ("stima", "limite"):
            for mu in (0.20, 0.25, 0.30, 0.40, 0.50):
                n_req = P.n_per_potenza(mu, sig, 0.15, 0.80, reg)
                if P.prob_promozione(mu, sig, n_req, 0.15, reg) < 0.80:
                    bad.append((sig, reg, mu, n_req))
                if n_req > 1 and P.prob_promozione(mu, sig, n_req - 1, 0.15, reg) >= 0.80:
                    bad.append((sig, reg, mu, n_req, "non_minimo"))
    # Calcola esattamente la soglia n per mu=0.20, reg=limite su sigma=1.0 vs 1.25 vs 1.5
    n_mu020_lim = {s: P.n_per_potenza(0.20, s, 0.15, 0.80, "limite") for s in (1.0, 1.25, 1.5)}
    return {"anomalie": bad, "n_per_potenza_mu020_limite": n_mu020_lim}


NUOVI_MUTANTI_PS = [
    ("MPS01", "brain/laboratorio/studi/potenza_soglia.py",
     "return (target + 1.0) * math.sqrt(p * (1.0 - p))",
     "return target * math.sqrt(p * (1.0 - p))",
     "sottostima sigma_esiti usando target invece di target + 1"),
    ("MPS02", "brain/laboratorio/studi/potenza_soglia.py",
     "return _N.cdf((mu - soglia) * math.sqrt(n) / sigma - z)",
     "return _N.cdf((mu - soglia) * math.sqrt(n) / sigma + z)",
     "somma z invece di sottrarre z in prob_promozione"),
    ("MPS03", "brain/laboratorio/studi/potenza_soglia.py",
     "if mu <= soglia:",
     "if mu < soglia:",
     "cambia mu <= soglia in mu < soglia in n_per_potenza"),
    ("MPS04", "brain/laboratorio/studi/potenza_soglia.py",
     "var = (vinte * (target - media) ** 2 + (n - vinte) * (-1.0 - media) ** 2) / (n - 1)",
     "var = (vinte * (target - media) ** 2 + (n - vinte) * (-1.0 - media) ** 2) / n",
     "divide per n invece che n-1 nella varianza campionaria di simula"),
    ("MPS05", "brain/laboratorio/studi/potenza_soglia.py",
     "passa += media - z * math.sqrt(var / n) >= soglia",
     "passa += media - z * math.sqrt(var) >= soglia",
     "toglie divisione / n nell'errore standard di simula"),
    ("MPS06", "brain/laboratorio/studi/potenza_soglia.py",
     "Z95 = 1.959963984540054",
     "Z95 = 1.6448536269514722",
     "sostituisce Z95 bilaterale (1.96) con unilaterale (1.645)"),
]


def _run_mut(args):
    cod, rel, target, repl, desc = args
    with tempfile.TemporaryDirectory() as tmp:
        rad = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT / "brain", rad / "brain",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "cache_dukascopy", "partizioni", "*.csv", "da-gemini"))
        p = rad / rel
        orig = p.read_text(encoding="utf-8")
        assert orig.count(target) == 1, f"{cod}: target non univoco"
        p.write_text(orig.replace(target, repl, 1), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_potenza_soglia"],
            cwd=str(rad), env=dict(os.environ, PYTHONPATH=str(rad)),
            capture_output=True, text=True, timeout=120,
        )
        return {"codice": cod, "stato": "VIVO" if proc.returncode == 0 else "UCCISO", "rc": proc.returncode, "desc": desc}


def main() -> None:
    print("PS-P1:", sonda_ps_p1_verifica_indipendente_tabella())
    print("PS-P2:", sonda_ps_p2_simulazione_e_scarto_asimmetrico())
    print("PS-P3:", sonda_ps_p3_errori_dominio_e_bordi())
    print("PS-P4:", sonda_ps_p4_impatto_autocorrelazione())
    print("PS-P5:", sonda_ps_p5_consistenza_altri_sigma())
    print("=== C2 MUTANTI POTENZA (MPS01..MPS06) ===")
    with ThreadPoolExecutor(max_workers=2) as pool:
        for m in pool.map(_run_mut, NUOVI_MUTANTI_PS):
            print("MUTANTE:", m)


if __name__ == "__main__":
    main()
