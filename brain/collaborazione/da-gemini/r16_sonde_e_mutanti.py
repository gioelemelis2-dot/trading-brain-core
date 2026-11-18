#!/usr/bin/env python3
"""MANDATO R16 (Compiti A & C) — Riprova sonde C1/C2/S5, verifica K15c e ottavo attacco (7 sonde + 6 mutanti).

Solo dati inventati in cartelle temporanee, rete bloccata con HTTPS_PROXY=http://127.0.0.1:9.
"""
import argparse
import io
import json
import lzma
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from contextlib import redirect_stdout
from datetime import date, time as ora_t, timedelta
from pathlib import Path


def verifica_rete_bloccata() -> None:
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        raise RuntimeError("HTTPS_PROXY non impostato")
    try:
        urllib.request.urlopen("https://example.com", timeout=2)
    except Exception as exc:
        print(f"[RETE] bloccata ({proxy}): {type(exc).__name__}")
        return
    raise RuntimeError("RETE NON BLOCCATA")


def esegui_sonde_compito_a(radice: Path, td: Path) -> None:
    print("\n=== COMPITO A: Rilancio sonde C1, C2, S5 sul candidato 303890b ===")
    sys.path.insert(0, str(radice))
    from brain.dati.pipeline import dukascopy as DK
    from brain.laboratorio.esecuzione import criteri as K, riserva as RV
    from brain.laboratorio.studi import potenza_soglia as PS

    # C1 (#107): screening con casuale={} -> copertura deve valere 0.0
    scr0 = K.screening({"n": 0}, {}, {"n_comuni": 0, "batte_entrambi": False}, True, None)
    c4_val = scr0["criteri"][3]["valore"]
    print(f"[C1 #107 screening casuale={{}}] criterio4_val={c4_val} (copertura={c4_val[1]})")

    # C2 (#110): anni=[], sharpe_prove=[None], percentile fuori da (0, 1] -> ValueError espliciti
    tr_base = [{"data": date(2015 + (i % 8), 1 + (i % 12), 1 + (i % 27)), "lato": "acquisto", "r": 0.5 if i % 2 == 0 else -0.2}
               for i in range(40)]
    out_c2 = {}
    for nome, fn in (
        ("anni_vuoti", lambda: K.verifica(tr_base, 2, anni=[])),
        ("anni_vuoti_tr_vuoto", lambda: K.verifica([], 2, anni=[])),
        ("sharpe_None", lambda: K.verifica(tr_base, 2, anni=range(2005, 2024), sharpe_prove=[None])),
        ("q_neg", lambda: K.percentile([1.0, 2.0, 3.0], -0.5)),
        ("q_0", lambda: K.percentile([1.0, 2.0, 3.0], 0.0)),
        ("q_15", lambda: K.percentile([1.0, 2.0, 3.0], 1.5)),
    ):
        try:
            res = fn()
            out_c2[nome] = f"NESSUN_ERRORE({res})"
        except Exception as e:
            out_c2[nome] = f"{type(e).__name__}: {e}"
    # Caso collaterale: iteratore a consumo singolo passato come anni -> consumato da list(anni)!
    try:
        K.verifica(tr_base, 2, anni=(y for y in range(2005, 2024)))
        out_c2["anni_generatore"] = "OK"
    except Exception as e:
        out_c2["anni_generatore"] = f"{type(e).__name__}: {e}"
    print(f"[C2 #110] {out_c2}")

    # S5 (#89, #111, #93, #94a/e, #101)
    g = date(2024, 1, 2)
    def mk(recs):
        b = bytearray()
        for r in recs:
            b += DK.RECORD.pack(*r)
        return lzma.compress(bytes(b))

    s5 = {}
    for label, recs in (
        ("non60", [(601, 2000000, 2000100, 1999900, 2000200, 1.0)]),
        ("dup", [(600, 2000000, 2000100, 1999900, 2000200, 0.0), (600, 2000000, 2000200, 1999900, 2000300, 1.0)]),
        ("desc", [(1200, 2000000, 2000100, 1999900, 2000200, 1.0), (600, 2000000, 2000100, 1999900, 2000200, 1.0)]),
    ):
        try:
            DK.decodifica(mk(recs), g, 3)
            s5[f"d_{label}"] = "ACCETTATO"
        except DK.ErroreDati as e:
            s5[f"d_{label}"] = f"RIFIUTATO({e})"

    reg_ris = td / "s5_ris.json"
    reg_ris.write_text(json.dumps({
        "schema": "riserva/1",
        "riserva": {"inizio": "2005-01-01", "fine": "2023-10-31", "alfa_tot": 5.0, "protetta": None},
        "eventi": [],
    }))
    try:
        RV.stato(reg_ris)
        s5["d93"] = "ACCETTATO"
    except ValueError as e:
        s5["d93"] = f"RIFIUTATO({e})"

    reg_j = td / "s5_j.json"
    RV.crea(reg_j, date(2005, 1, 1), date(2023, 10, 31), 0.05, "2026-11-17T00:00:00Z")
    RV.prenota(reg_j, "id1", "H-002", date(2005, 1, 1), date(2005, 12, 31), "h", "2026-11-17T00:00:00Z")
    dj = json.loads(reg_j.read_text())
    dj["eventi"].append({"tipo": "autorizzazione", "id": "id1", "j": True, "n_globale": 2,
                         "hash_dati": "abc", "m": 1, "alfa_j": 0.025, "ora": "2026-11-17T00:00:00Z"})
    reg_j.write_text(json.dumps(dj))
    try:
        RV.stato(reg_j)
        s5["d94a"] = "ACCETTATO"
    except ValueError as e:
        s5["d94a"] = f"RIFIUTATO({e})"

    try:
        PS.n_per_potenza(-0.1, -5.0, 0.15, 0.8, "stima")
        s5["n_neg_sigma"] = "ACCETTATO"
    except ValueError as e:
        s5["n_neg_sigma"] = f"RIFIUTATO({e})"
    print(f"[S5 #89/#111/#93/#94/#101] {s5}")
    sys.path.remove(str(radice))


def esegui_sonde_compito_c(radice: Path, td: Path) -> None:
    print("\n=== COMPITO C: Sonde su intersezione_bid_ask, collaudo_ia02, pilota_ia02 ===")
    sys.path.insert(0, str(radice))
    from brain.laboratorio.esecuzione import sintetico as SN
    from brain.laboratorio.simulatori.orb_londra import _utc
    from brain.laboratorio.studi import intersezione_bid_ask as IX, collaudo_ia02 as CO, pilota_ia02 as PI

    # C-R16-1: intersezione_bid_ask su sola vigilia (sedute=[]) + ora legale (2024-03-11 GMT, 2024-04-01 BST)
    # + file vuoto da un lato + minuti fuori sessione (07:30 e 16:45 Londra) + nessun prezzo in stdout/JSON
    c1_dir = td / "ix_edge"
    prezzo_spia = 4321.987
    bid, ask = {}, {}
    # Giorno vigilia unica 2024-12-24 (sedute sarà []!)
    vig = date(2024, 12, 24)
    t_vig = _utc(vig, ora_t(7, 30))
    for k in range(10 * 60):  # dalle 07:30 alle 17:30 Londra (include fuori sessione + 2o/3o terzo)
        t = t_vig + timedelta(minutes=k)
        bid[t] = (prezzo_spia, prezzo_spia + 0.5, prezzo_spia - 0.5, prezzo_spia)
        ask[t] = (prezzo_spia + 0.3, prezzo_spia + 0.8, prezzo_spia - 0.2, prezzo_spia + 0.3)
    SN.scrivi_cache(bid, c1_dir / "XAUUSD", inizio=vig, fine=vig)
    SN.scrivi_cache(ask, c1_dir / "XAUUSD_ASK", inizio=vig, fine=vig)
    e_vig = IX.esamina(c1_dir, vig, vig)
    tab_vig = IX.tabella(e_vig)
    js_vig = json.dumps(e_vig, ensure_ascii=False)
    nessun_prezzo_vig = ("4321" not in tab_vig and "4321" not in js_vig and "4322" not in tab_vig)
    print(f"[C-R16-1a sola vigilia (sedute=[])] vigilie={len(e_vig['vigilie'])} sedute={len(e_vig['sedute'])} quota_comuni_anno={e_vig['anni']['2024']['quota_comuni']} tab_ok={'2024' in tab_vig} no_prezzi={nessun_prezzo_vig}")

    # Ora legale (2024-03-11 GMT +0 e 2024-04-02 BST +1), minuti fuori sessione e file vuoto da un lato
    c1b_dir = td / "ix_dst"
    bid2, ask2 = {}, {}
    g_gmt, g_bst, g_vuoto = date(2024, 3, 11), date(2024, 4, 2), date(2024, 4, 3)
    for g in (g_gmt, g_bst):
        # 30 min prima delle 08:00 Londra + 525 min in sessione + 30 min dopo le 16:45 Londra
        t0 = _utc(g, ora_t(7, 30))
        for k in range(30 + 525 + 30):
            t = t0 + timedelta(minutes=k)
            bid2[t] = (prezzo_spia, prezzo_spia + 0.4, prezzo_spia - 0.4, prezzo_spia)
            ask2[t] = (prezzo_spia + 0.2, prezzo_spia + 0.6, prezzo_spia - 0.2, prezzo_spia + 0.2)
    SN.scrivi_cache(bid2, c1b_dir / "XAUUSD", inizio=g_gmt, fine=g_bst)
    SN.scrivi_cache(ask2, c1b_dir / "XAUUSD_ASK", inizio=g_gmt, fine=g_bst)
    # 2024-04-03: BID pieno, ASK vuoto
    bid3 = {_utc(g_vuoto, ora_t(8, 0)) + timedelta(minutes=k): (prezzo_spia, prezzo_spia + 0.4, prezzo_spia - 0.4, prezzo_spia)
            for k in range(525)}
    SN.scrivi_cache(bid3, c1b_dir / "XAUUSD", inizio=g_vuoto, fine=g_vuoto)
    (c1b_dir / "XAUUSD_ASK" / f"{g_vuoto.isoformat()}.bi5").write_bytes(b"")
    e_dst = IX.esamina(c1b_dir, g_gmt, g_vuoto)
    s_gmt = [s for s in e_dst["sedute"] if s["giorno"] == g_gmt.isoformat()][0]
    s_bst = [s for s in e_dst["sedute"] if s["giorno"] == g_bst.isoformat()][0]
    s_v = [s for s in e_dst["sedute"] if s["giorno"] == g_vuoto.isoformat()][0]
    buf_cli = io.StringIO()
    out_js = td / "ix_out.json"
    with redirect_stdout(buf_cli):
        rc_ix = IX.main(["--cache", str(c1b_dir), "--inizio", g_gmt.isoformat(), "--fine", g_vuoto.isoformat(), "--json", str(out_js)])
    no_p = "4321" not in buf_cli.getvalue() and "4321" not in out_js.read_text()
    print(f"[C-R16-1b DST+vuoto+fuori_sess] gmt={s_gmt['comuni_validi']}/{s_gmt['griglia']} bst={s_bst['comuni_validi']}/{s_bst['griglia']} vuoto_ask=(solo_bid={s_v['solo_bid']},stati={s_v['stati']}) cli_rc={rc_ix} no_prezzi={no_p}")

    # C-R16-2: collaudo_ia02 riferimenti analitici (formula chiusa F_AR1) e Clopper-Pearson edge
    def f_ar1_chiusa(n, rho):
        if rho == 0:
            return 1.0
        return 1.0 + 2.0 * rho / (1.0 - rho) * (1.0 - (1.0 - rho ** n) / (n * (1.0 - rho)))
    diffs_f = [abs(CO.fattore_ar1(n, r) - f_ar1_chiusa(n, r)) for n in (100, 450, 1000) for r in (0.0, 0.25, 0.5)]
    lo0, hi0 = CO.clopper_pearson(0, 100)
    lo100, hi100 = CO.clopper_pearson(100, 100)
    # Verifica edge limite_bootstrap quando blocco non divide n (es. n=300, b=7 -> blocchi=43, 43*7=301)
    x_cost = [2.0] * 300
    lb_cost = CO.limite_bootstrap(x_cost, 0.025, 99, random.Random(1))
    print(f"[C-R16-2 collaudo_ia02] max_diff_F={max(diffs_f):.2e} cp0=({lo0},{hi0:.6f}) cp100=({lo100:.6f},{hi100}) boot_const_300={lb_cost:.12f}")

    # C-R16-3: pilota_ia02 semi SHA-256 (indipendenza componenti 0..3) e coppie (S_d, K_d)
    cols = [[PI.flusso(1, 9, r, comp).random() for r in range(1, 501)] for comp in range(4)]
    max_corr = 0.0
    for i in range(4):
        for j in range(i + 1, 4):
            mi, mj = sum(cols[i]) / 500, sum(cols[j]) / 500
            num = sum((a - mi) * (b - mj) for a, b in zip(cols[i], cols[j]))
            den = math.sqrt(sum((a - mi) ** 2 for a in cols[i]) * sum((b - mj) ** 2 for b in cols[j]))
            max_corr = max(max_corr, abs(num / den))
    # Conteggi cella 9 e rare cella 11 medie su 200 repliche
    tot_s9 = tot_k9 = tot_s11 = tot_k11 = 0.0
    for r in range(1, 201):
        for s, k in PI.genera(9, 1, r):
            tot_s9 += s; tot_k9 += k
        for s, k in PI.genera(11, 1, r):
            tot_s11 += s; tot_k11 += k
    print(f"[C-R16-3 pilota semi & generatori] max_corr_comp={max_corr:.4f} mu_hat_c9={tot_s9/tot_k9:.4f}(att=0.15) mu_hat_c11={tot_s11/tot_k11:.4f}(att=0.15)")

    # C-R16-4: pilota_ia02 HAC ritardi/pesi, bootstrap circolare (n % blocco != 0 e sum_K=0), classificazione ai bordi
    # Verifica circolare con blocco che avvolge la coda e ΣK = 0 solo nelle finestre di coda
    coppie_sk0 = [(1.0, 1)] * 10 + [(0.0, 0)] * 90  # se il bootstrap pesca solo in [10..99], TK=0!
    iv_sk0 = PI.intervallo_bootstrap(coppie_sk0, PI.flusso(9, 1, 1, 3), ricampionamenti=299, blocco=10)
    # Verifica edge p=0.0 in pilota_ia02 quantile (non chiamato con A=0.025, ma nota comportamento)
    # Verifica cella 9 su benchmark ridotto (fase 0, 10 repliche) e coerenza totale
    res_c9 = PI.esegui_cella(9, fase=0, repliche=10, ricampionamenti=99)
    coer = {m: res_c9[m]["promosse"] + res_c9[m]["bocciate"] + res_c9[m]["attraversamenti"] + res_c9[m]["errori"]
            for m in ("hac", "bootstrap")}
    # C-R16-5: collaudo vs pilota HAC su K_d = 1 identico a meno della media/scarto su Z
    serie_t = [0.2 * math.sin(i) + 0.15 for i in range(100)]
    lo_p, hi_p = PI.intervallo_hac([(x, 1) for x in serie_t], ritardi=4)
    lo_c = CO.limite_hac(serie_t, 0.025, ritardi=4)
    print(f"[C-R16-4/5 pilota HAC=collaudo + SK=0] diff_lo_hac={abs(lo_p - lo_c):.2e} boot_sk0={iv_sk0} coer_c9={coer}")

    sys.path.remove(str(radice))


def mutanti_nuovi_compito_c(radice: Path, td: Path) -> None:
    print("\n=== COMPITO C: 6 mutanti nuovi sui 3 strumenti di contorno ===")
    mutanti = [
        (
            "M-R16-01",
            "intersezione_bid_ask.py: mescola vigilie nei percentili annuali delle sedute",
            "brain/laboratorio/studi/intersezione_bid_ask.py",
            '        delle = [s for s in sedute if s["giorno"][:4] == anno]',
            '        delle = [s for s in sedute + vigilie if s["giorno"][:4] == anno]',
            ["brain.laboratorio.tests.test_intersezione_bid_ask"],
        ),
        (
            "M-R16-02",
            "intersezione_bid_ask.py: estremi_incrociati controlla solo minimo (dimentica massimo)",
            "brain/laboratorio/studi/intersezione_bid_ask.py",
            "                if a[2] < b[2] or a[3] < b[3]:",
            "                if a[3] < b[3]:",
            ["brain.laboratorio.tests.test_intersezione_bid_ask"],
        ),
        (
            "M-R16-03",
            "collaudo_ia02.py: limite_bootstrap divide per n invece di blocchi * b",
            "brain/laboratorio/studi/collaudo_ia02.py",
            "        medie.append(tot / (blocchi * b))",
            "        medie.append(tot / n)",
            ["brain.laboratorio.tests.test_collaudo_ia02"],
        ),
        (
            "M-R16-04",
            "collaudo_ia02.py: clopper_pearson estremo inferiore usa k invece di k - 1",
            "brain/laboratorio/studi/collaudo_ia02.py",
            "    basso = 0.0 if k == 0 else cerca(lambda p: (1 - _cdf_binomiale(k - 1, M, p)) - d)",
            "    basso = 0.0 if k == 0 else cerca(lambda p: (1 - _cdf_binomiale(k, M, p)) - d)",
            ["brain.laboratorio.tests.test_collaudo_ia02"],
        ),
        (
            "M-R16-05",
            "pilota_ia02.py: cella rare usa sqrt(Q_RARE) anziché sqrt(Q_RARE*(1-Q_RARE))",
            "brain/laboratorio/studi/pilota_ia02.py",
            "        scala = SIGMA / math.sqrt(Q_RARE * (1 - Q_RARE))",
            "        scala = SIGMA / math.sqrt(Q_RARE)",
            ["brain.laboratorio.tests.test_pilota_ia02"],
        ),
        (
            "M-R16-06",
            "pilota_ia02.py: esegui_cella dimentica - mu nella distorsione",
            "brain/laboratorio/studi/pilota_ia02.py",
            '        c["distorsione"] = (sum(stime) / len(stime) - mu) if stime else None',
            '        c["distorsione"] = (sum(stime) / len(stime)) if stime else None',
            ["brain.laboratorio.tests.test_pilota_ia02"],
        ),
    ]

    visti = set()
    for *_rest, suite in mutanti:
        k = tuple(suite)
        if k in visti:
            continue
        visti.add(k)
        m00 = td / f"M00_r16_{len(visti)}"
        shutil.copytree(radice / "brain", m00 / "brain", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        r0 = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                            cwd=str(m00), capture_output=True, text=True)
        print(f"[M00 BASE] suite={suite[0]} rc={r0.returncode}")
        if r0.returncode != 0:
            print(r0.stderr)
            return

    uccisi = vivi = 0
    for mid, desc, rel, vecchia, nuova, suite in mutanti:
        copia = td / mid
        shutil.copytree(radice / "brain", copia / "brain", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        target = copia / rel
        testo = target.read_text(encoding="utf-8")
        assert vecchia in testo, f"{mid}: pattern non trovato"
        mut = testo.replace(vecchia, nuova, 1)
        compile(mut, str(target), "exec")
        target.write_text(mut, encoding="utf-8")
        r = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                           cwd=str(copia), capture_output=True, text=True)
        stato = "UCCISO" if r.returncode != 0 else "SOPRAVVISSUTO"
        if r.returncode != 0:
            uccisi += 1
        else:
            vivi += 1
        print(f"[{stato}] {mid} ({desc}) -> rc={r.returncode}")
    print(f"RIEPILOGO MUTANTI NUOVI R16: uccisi={uccisi}/{len(mutanti)}, sopravvissuti={vivi}/{len(mutanti)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    radice = args.radice.resolve()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="r16_sonde_") as td_str:
        td = Path(td_str)
        esegui_sonde_compito_a(radice, td)
        esegui_sonde_compito_c(radice, td)
        mutanti_nuovi_compito_c(radice, td)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
