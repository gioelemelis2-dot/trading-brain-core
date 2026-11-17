#!/usr/bin/env python3
"""MANDATO R15 (Compito C) — Settimo attacco (errori E su criteri.py, caricatore.py, orb_londra.py).

Almeno 5 sonde e 5 mutanti nuovi su dati inventati in cartelle temporanee con rete bloccata.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

LONDRA = ZoneInfo("Europe/London")
UTC = timezone.utc


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


def sonde_compito_c(radice: Path, td: Path) -> None:
    sys.path.insert(0, str(radice))
    from brain.dati.pipeline import dukascopy as DK
    from brain.laboratorio.esecuzione import caricatore as C, criteri as K, sigillo as S, esegui_h002 as E
    from brain.laboratorio.simulatori import orb_londra as O
    import lzma

    print("\n=== SONDE COMPITO C (criteri.py, caricatore.py, orb_londra.py) ===")

    # Sonda C1: criteri.screening con casuale={} -> copertura criterio 4 diventa 1.0 (100%) mentre criterio 5 e' 0.0
    scr0 = K.screening({"n": 0}, {}, {"n_comuni": 0, "batte_entrambi": False}, True, None)
    c4 = scr0["criteri"][3]
    c5 = scr0["criteri"][4]
    print(f"[C1 screening casuale={{}}] criterio4_val={c4['valore']} (atteso cop=0.0, osservato={c4['valore'][1]}) | criterio5_val={c5['valore']}")

    # Sonda C2: criteri.verifica (anni=[], sharpe_prove=[None]) e percentile(q<0 o q>1)
    tr_base = [{"data": date(2015 + (i % 8), 1 + (i % 12), 1 + (i % 27)), "lato": "acquisto", "r": 0.5 if i % 2 == 0 else -0.2}
               for i in range(40)]
    res_anni_vuoti = "OK"
    try:
        K.verifica(tr_base, 2, anni=[])
    except Exception as e:
        res_anni_vuoti = f"{type(e).__name__}: {e}"
    res_sp_none = "OK"
    try:
        K.verifica(tr_base, 2, anni=range(2005, 2024), sharpe_prove=[None])
    except Exception as e:
        res_sp_none = f"{type(e).__name__}: {e}"
    res_q_neg = K.percentile([1.0, 2.0, 3.0], -0.5)
    try:
        K.percentile([1.0, 2.0, 3.0], 1.5)
        res_q_big = "OK"
    except Exception as e:
        res_q_big = f"{type(e).__name__}: {e}"
    # DSR con anni senza trade nei 5 anni finali (2019-2023)
    tr_vecchi = [{"data": date(2006 + (i % 8), 1 + (i % 12), 1 + (i % 27)), "lato": "acquisto", "r": 1.0 if i % 3 else -0.5}
                 for i in range(40)]
    v_ultimi = K.verifica(tr_vecchi, 2, anni=range(2005, 2024))
    print(f"[C2 criteri.verifica edge] anni=[]->{res_anni_vuoti} | sharpe_prove=[None]->{res_sp_none} | q=-0.5->{res_q_neg} | q=1.5->{res_q_big} | cumulato_2019_23={v_ultimi['criteri'][3]['valore']}(pass={v_ultimi['criteri'][3]['passa']})")

    # Sonda C3: caricatore.carica accetta giorno con 0 minuti nell'OR [08:00, 08:30) e BID/ASK disallineati
    g_svil = date(2024, 1, 2)
    # 08:30..16:44 -> 495 minuti, 145 nel 1o terzo [08:30, 10:55), 0 nell'OR [08:00, 08:30)!
    buf_no_or = bytearray()
    for m in range(8 * 60 + 30, 16 * 60 + 45):
        buf_no_or += DK.RECORD.pack(m * 60, 2000000, 2000000, 1999500, 2000500, 1.0)
    raw_no_or = lzma.compress(bytes(buf_no_or))

    reg = td / "reg_c.json"
    sh = td / "sh_c.md"
    sh.write_text("# H-002 finta\n")
    S.sigilla(reg, E.IPOTESI, sh, ["V-T", "V-S"], "2026-11-17T00:00:00Z")
    cb, ca = td / "c3_bid", td / "c3_ask"
    cb.mkdir(); ca.mkdir()
    (cb / f"{g_svil.isoformat()}.bi5").write_bytes(raw_no_or)
    (ca / f"{g_svil.isoformat()}.bi5").write_bytes(raw_no_or)
    bid3, ask3, info3 = C.carica(cb, ca, g_svil, g_svil, "sviluppo", reg, E.IPOTESI, sh)
    res3 = O.resoconto(bid3, ask3)
    print(f"[C3 caricatore senza OR] incompleti={info3['feriali_incompleti_bid']} minuti={info3['minuti_bid']} -> orb_londra={res3['giorni_per_motivo']}")

    # Sonda C4: giorni_corti (24/12) con ASK mancante nella mattina e presente solo il pomeriggio + cambio ora legale
    g_corto = date(2024, 12, 24)
    buf_am = bytearray()
    buf_pm = bytearray()
    for m in range(8 * 60, 10 * 60 + 55):  # primo terzo: 175 min
        buf_am += DK.RECORD.pack(m * 60, 2000000, 2000000, 1999500, 2000500, 1.0)
    for m in range(11 * 60, 16 * 60 + 45):  # pomeriggio
        buf_pm += DK.RECORD.pack(m * 60, 2000000, 2000000, 1999500, 2000500, 1.0)
    cb4, ca4 = td / "c4_bid", td / "c4_ask"
    cb4.mkdir(); ca4.mkdir()
    (cb4 / f"{g_corto.isoformat()}.bi5").write_bytes(lzma.compress(bytes(buf_am)))
    (ca4 / f"{g_corto.isoformat()}.bi5").write_bytes(lzma.compress(bytes(buf_pm)))
    # _completo guarda bid e ask separatamente, ma su giorno corto controlla solo terzi[0] >= 44 -> ask fallisce su terzi[0]!
    # Cosa succede se ask ha 44 minuti alle 08:00..08:43 SOLO DOPO che bid finisce alle 08:44..10:54? ZERO sovrapposizione!
    buf_b_dis = bytearray()
    buf_a_dis = bytearray()
    for m in range(8 * 60, 8 * 60 + 44):
        buf_a_dis += DK.RECORD.pack(m * 60, 2000000, 2000000, 1999500, 2000500, 1.0)
    for m in range(8 * 60 + 44, 10 * 60 + 55):
        buf_b_dis += DK.RECORD.pack(m * 60, 2000000, 2000000, 1999500, 2000500, 1.0)
    (cb4 / f"{g_corto.isoformat()}.bi5").write_bytes(lzma.compress(bytes(buf_b_dis)))
    (ca4 / f"{g_corto.isoformat()}.bi5").write_bytes(lzma.compress(bytes(buf_a_dis)))
    bid4, ask4, info4 = C.carica(cb4, ca4, g_corto, g_corto, "sviluppo", reg, E.IPOTESI, sh)
    overlap4 = len(set(bid4) & set(ask4))
    # Verifica DST 2024: 2024-03-11 (US gia EDT, Londra ancora GMT 0) e 2024-04-01 (Londra BST +1)
    dst_gmt = O._utc(date(2024, 3, 11), time(8, 0)).hour
    dst_bst = O._utc(date(2024, 4, 1), time(8, 0)).hour
    print(f"[C4 giorni_corti BID/ASK disgiunti + DST] incomp_bid={info4['feriali_incompleti_bid']} incomp_ask={info4['feriali_incompleti_ask']} overlap={overlap4} | UTC_0800_GMT={dst_gmt} UTC_0800_BST={dst_bst}")

    # Sonda C5: orb_londra.eseguibile e minuti_spread_negativo con spread intra-minuto invertito su high/low (open/close positivi)
    bid5, ask5 = {}, {}
    for k in range(25):
        g = date(2024, 1, 2) + timedelta(days=k)
        if g.weekday() >= 5:
            continue
        t0 = datetime.combine(g, time(8, 0), tzinfo=LONDRA).astimezone(UTC)
        for m in range(9 * 60):
            t = t0 + timedelta(minutes=m)
            # Open e Close di ASK >= BID (+0.20), MA high di ASK (2000.5) < high di BID (2005.0)!
            if m < 30:
                bid5[t] = (2000.0, 2002.0, 1998.0, 2000.0)
                ask5[t] = (2000.2, 2002.2, 1998.2, 2000.2)
            elif m == 30:
                bid5[t] = (2000.0, 2003.0, 2000.0, 2003.0)
                ask5[t] = (2000.2, 2003.2, 2000.2, 2003.2)
            else:
                bid5[t] = (2003.0, 2009.0, 2002.5, 2003.0)
                ask5[t] = (2003.2, 2003.3, 2002.6, 2003.2)  # ask high < bid high!
    res5 = O.resoconto(bid5, ask5)
    print(f"[C5 spread high invertito] minuti_spread_negativo_segnalati={res5['minuti_spread_negativo']} (atteso >0 se high/low controllati)")

    # Sonda C6: verifica indipendente costi in orb_londra.simula (commissione, slip, stress, once, gap stop, specchio)
    t_base = datetime.combine(date(2024, 1, 2), time(9, 16), tzinfo=UTC)
    par = O.V_T
    # Costruiamo Giorno manuale: ra_alto=2002.0, ra_basso=1998.0 (a=4.0)
    # Entrata su minuto 0: b0=(2002.5, 2003, 2002, 2002.5), a0=(2002.8, 2003.3, 2002.3, 2002.8)
    # Minuto 1: colpisce target!
    entrata_att = 2002.8 + par.slip_ingresso + par.stress  # 2002.9
    stop = 1998.0
    rischio_att = entrata_att - stop  # 4.9
    target_att = entrata_att + par.target_r * rischio_att  # 2002.9 + 7.35 = 2010.25
    perdita_stop_att = entrata_att - (stop - par.slip_uscita - par.stress)  # 4.9 + 0.20 = 5.10
    once_att = round(par.rischio_usd * O.MICRO) // round((perdita_stop_att + par.commissione) * O.MICRO)  # 500 // 5.17 = 96
    r_att = (once_att * ((target_att - entrata_att) - par.commissione)) / par.rischio_usd

    g_sim = O.Giorno(
        data=date(2024, 1, 2), a=4.0, ra_alto=2002.0, ra_basso=1998.0, valido=True, motivo="valido", lato="acquisto",
        minuti=[
            (t_base, (2002.5, 2003.0, 2002.0, 2002.5), (2002.8, 2003.3, 2002.3, 2002.8)),
            (t_base + timedelta(minutes=1), (2003.0, 2011.0, 2002.5, 2010.5), (2003.3, 2011.3, 2002.8, 2010.8)),
        ],
    )
    tr_sim = O.simula(g_sim, "acquisto", par)
    diff_r = abs(tr_sim["r"] - r_att)
    assert tr_sim["once"] == once_att and diff_r < 1e-12, (tr_sim, once_att, r_att)
    print(f"[C6 verifica esatta costi simula] once={tr_sim['once']}=={once_att}, R={tr_sim['r']:.8f}=={r_att:.8f} (diff={diff_r:.2e})")

    sys.path.remove(str(radice))


def mutanti_compito_c(radice: Path, td: Path) -> None:
    print("\n=== MUTANTI NUOVI COMPITO C (6 mutanti su criteri, caricatore, orb_londra) ===")
    mutanti = [
        (
            "M-R15-01",
            "criteri.py: percentile usa troncamento int(q*n) anziché math.ceil",
            "brain/laboratorio/esecuzione/criteri.py",
            "    k = max(1, math.ceil(q * len(ordinati) - 1e-9))",
            "    k = max(1, int(q * len(ordinati)))",
            ["brain.laboratorio.tests.test_esecuzione"],
        ),
        (
            "M-R15-02",
            "criteri.py: ultimi 5 anni usa >= (include 6 anni invece di 5)",
            "brain/laboratorio/esecuzione/criteri.py",
            '        cumulato = sum(x["r"] for x in tr if x["data"].year > ultimo - ultimi)',
            '        cumulato = sum(x["r"] for x in tr if x["data"].year >= ultimo - ultimi)',
            ["brain.laboratorio.tests.test_esecuzione"],
        ),
        (
            "M-R15-03",
            "criteri.py: verifica usa min(v, variance(...)) anziché max per V del DSR",
            "brain/laboratorio/esecuzione/criteri.py",
            "        if sharpe_prove:\n            v = max(v, variance(list(sharpe_prove) + [sr]))",
            "        if sharpe_prove:\n            v = min(v, variance(list(sharpe_prove) + [sr]))",
            ["brain.laboratorio.tests.test_esecuzione", "brain.laboratorio.tests.test_esegui_h002.TestVarianzaDelleProve"],
        ),
        (
            "M-R15-04",
            "caricatore.py: giorni corti controlla terzi[2] anziché terzi[0]",
            "brain/laboratorio/esecuzione/caricatore.py",
            "    if corto:\n        return terzi[0] >= minimo_terzo",
            "    if corto:\n        return terzi[2] >= minimo_terzo",
            ["brain.laboratorio.tests.test_esecuzione", "brain.laboratorio.tests.test_taratura_completezza"],
        ),
        (
            "M-R15-05",
            "orb_londra.py: simula omette commissione nel calcolo di once",
            "brain/laboratorio/simulatori/orb_londra.py",
            "    once = round(par.rischio_usd * MICRO) // round((perdita_allo_stop + par.commissione) * MICRO)",
            "    once = round(par.rischio_usd * MICRO) // round(perdita_allo_stop * MICRO)",
            ["brain.laboratorio.tests.test_orb_londra"],
        ),
        (
            "M-R15-06",
            "orb_londra.py: simula permette di colpire target al minuto d'ingresso k==0",
            "brain/laboratorio/simulatori/orb_londra.py",
            "        if k > 0 and target is not None:                                 # nel minuto d'ingresso conta solo lo stop",
            "        if target is not None:",
            ["brain.laboratorio.tests.test_orb_londra"],
        ),
    ]

    visti = set()
    for *_rest, suite in mutanti:
        chiave = tuple(suite)
        if chiave in visti:
            continue
        visti.add(chiave)
        m00 = td / f"M00_c_{len(visti)}"
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
        mutato = testo.replace(vecchia, nuova, 1)
        compile(mutato, str(target), "exec")
        target.write_text(mutato, encoding="utf-8")
        r = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *suite],
                           cwd=str(copia), capture_output=True, text=True)
        stato = "UCCISO" if r.returncode != 0 else "SOPRAVVISSUTO"
        if r.returncode != 0:
            uccisi += 1
        else:
            vivi += 1
        print(f"[{stato}] {mid} ({desc}) -> rc={r.returncode}")
    print(f"RIEPILOGO MUTANTI COMPITO C: uccisi={uccisi}/{len(mutanti)}, sopravvissuti={vivi}/{len(mutanti)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", type=Path, default=Path(__file__).resolve().parents[3])
    args = ap.parse_args()
    radice = args.radice.resolve()

    verifica_rete_bloccata()
    with tempfile.TemporaryDirectory(prefix="r15_compito_c_") as td_str:
        td = Path(td_str)
        sonde_compito_c(radice, td)
        mutanti_compito_c(radice, td)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
