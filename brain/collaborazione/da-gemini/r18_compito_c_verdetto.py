"""Mandato R18 — Compito C: primo giro di revisione di `verdetto_d31.py` (errori E e manomissioni M).

Contiene 6 sonde (C-VD-1..C-VD-6) e 7 mutanti NUOVI (M-VD-01..M-VD-07, non presenti in `mutazioni_verdetto.py`).
Soli dati inventati; esecuzione su copie temporanee con HTTPS_PROXY=http://127.0.0.1:9.
"""
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brain.laboratorio.studi import pilota_ia02 as P  # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V  # noqa: E402

NO_NET = dict(
    os.environ,
    HTTPS_PROXY="http://127.0.0.1:9",
    HTTP_PROXY="http://127.0.0.1:9",
    https_proxy="http://127.0.0.1:9",
    http_proxy="http://127.0.0.1:9",
    NO_PROXY="",
    no_proxy="",
)


def _costanti(media: float, n: int = 1000, delta: float = 0.1):
    s = [media + delta] * (n // 2) + [media - delta] * (n - n // 2)
    random.Random(7).shuffle(s)
    return [(x, 1) for x in s]


def sonde():
    su = _costanti(0.6)
    giu = _costanti(-0.3)

    # C-VD-1: Contratto D-31/D-35/D-37/D-44 + bug nel rapporto su intervallo invalido D-44 (#119)!
    assert V.segnale((0.3, 0.3 + 9.99e-10)) == "invalido"
    assert V.segnale((0.3, 0.3 + 1.01e-9)) == "favorevole"
    with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.25, 0.25 + 1e-13)):
        v_deg = V.verdetto(su, 5)
    voci_deg = V.voci_rapporto(v_deg)
    voce_st = [x for x in voci_deg if x["etichetta"] == "vantaggio della strategia"][0]
    testo_deg = V.rapporto(v_deg)
    bug_rapporto_d44 = (voce_st["valore"] is not None and "valido nel dominio" in voce_st["incertezza"])
    # Anche con estremo a filo 0.20 su intervallo invalido D-44: vicini_soglia popolato!
    with mock.patch.object(P, "intervallo_bootstrap", return_value=(0.20, 0.20 + 1e-13)):
        v_deg_filo = V.verdetto(su, 5)
    print(
        f"[SONDA C-VD-1] D-44 (#119) in verdetto()+rapporto(): esito={v_deg['esito']!r}, causa={v_deg['causa']!r}, "
        f"voce_stima_valore={voce_st['valore']}, dice_valido_invece_di_NON_STIMABILE={bug_rapporto_d44}, "
        f"vicini_su_invalido={v_deg_filo['vicini_soglia']}"
    )

    # C-VD-2: seme=None non validato -> random.Random(None) non deterministico (os.urandom)!
    # Usiamo una serie rumorosa da 1000 sedute con 2 chiamate con seme=None
    rng = random.Random(42)
    inc = [(rng.gauss(0.15, 1.25), 1) for _ in range(1000)]
    iv1 = V.intervallo(inc, None)
    iv2 = V.intervallo(inc, None)
    v_none = V.verdetto(su, None)
    print(
        f"[SONDA C-VD-2] seme=None accettato senza errore: iv1!=iv2 -> {iv1 != iv2} (NON deterministico!), "
        f"verdetto(seme=None) esito={v_none['esito']!r}, seme_riportato={v_none['seme']!r}"
    )

    # C-VD-3: contesto_prove e confine di fiducia
    with tempfile.TemporaryDirectory(prefix="r18_cvd3_") as td:
        tmp = Path(td)
        # (a) registro ereditato rinominato con schema Binario B -> rifiutato da S.leggi
        leg = tmp / "trial_registry.json"
        leg.write_text(json.dumps({"trials": [{"id": 1}]}), encoding="utf-8")
        rinom = tmp / "registro_prove.json"
        shutil.copy2(leg, rinom)
        try:
            V.contesto_prove(rinom)
            r_rinom = "ACCETTATO"
        except ValueError as e:
            r_rinom = f"RIFIUTATO ({type(e).__name__})"
        # (b) symlink registro_prove.json -> trial_registry.json con schema registro-prove/1
        leg_s1 = tmp / "trial_registry.json"
        leg_s1.write_text(json.dumps({"schema": "registro-prove/1", "prove": [], "sigilli": [], "esecuzioni": []}),
                          encoding="utf-8")
        sym = tmp / "link_canonico.json"
        sym.symlink_to(leg_s1)
        c_sym = V.contesto_prove(sym)
        # (c) registro falso valido in cartella arbitraria (nessun controllo percorso canonico né ancora git)
        falso = tmp / "falso.json"
        falso.write_text(json.dumps({"schema": "registro-prove/1", "prove": [], "sigilli": [], "esecuzioni": []}),
                         encoding="utf-8")
        c_falso = V.contesto_prove(falso)
        # (d) contesto costruito a mano dal chiamante (anche malformato o con N=-5)
        v_fake = V.verdetto(su, 5, contesto={"registro": "finto.json", "n_prove": -5, "impronta": "0" * 64})
        t_fake = V.rapporto(v_fake)
        v_bad = V.verdetto(su, 5, contesto={"chiave_sbagliata": 1})
        try:
            V.rapporto(v_bad)
            err_bad = "NESSUNO"
        except Exception as ex:
            err_bad = f"{type(ex).__name__}: {ex}"
        v_no_ctx = V.verdetto(su, 5, contesto=None)
        print(
            f"[SONDA C-VD-3] rinominato_schema_legacy={r_rinom} | symlink_a_trial_registry_con_schema1={c_sym['n_prove']} | "
            f"registro_falso_non_canonico_accettato={c_falso['n_prove']} | "
            f"contesto_mano_N=-5_etichettato_MISURA={'-5 prove [MISURA]' in t_fake} | "
            f"contesto_malformato_in_rapporto->{err_bad} | promossa_senza_contesto={v_no_ctx['esito'] == 'promossa'}"
        )

    # C-VD-4: Rapporti tipizzati (voci_rapporto, rapporto, voci_screening, rapporto_screening)
    # Verifica numeri nelle righe senza tag [TIPO] e comportamento con veto su dati inidonei
    v_veto_inid = V.verdetto([(0.5, 0)] * 1000, 5, [{"id": "blocchi", "veto": True, "esito": "fallito"}])
    t_veto = V.rapporto(v_veto_inid)
    voci_veto = V.voci_rapporto(v_veto_inid)
    sed_veto = [x for x in voci_veto if x["etichetta"] == "sedute"][0]
    s_no = V.screening(_costanti(0.25, 780, 0.25), 9, 0.30)
    t_scr = V.rapporto_screening(s_no)
    # Righe con numeri ma senza '[MISURA]/[DERIVATO]/[STIMA]/[IPOTESI]/[REGOLA]'
    righe_senza_tipo_v = [r for r in V.rapporto(v_deg_filo).splitlines()
                          if any(ch.isdigit() for ch in r) and not any(f"[{t}]" in r for t in V.TIPI)]
    righe_senza_tipo_s = [r for r in t_scr.splitlines()
                          if any(ch.isdigit() for ch in r) and not any(f"[{t}]" in r for t in V.TIPI)]
    print(
        f"[SONDA C-VD-4] veto_su_dati_inidonei sedute_incertezza={sed_veto['incertezza']!r} | "
        f"righe_numeriche_senza_tag_in_rapporto={len(righe_senza_tipo_v)} | "
        f"righe_numeriche_senza_tag_in_screening={len(righe_senza_tipo_s)}"
    )

    # C-VD-5: Generatore in coppie e overflow somma in media
    try:
        V.verdetto((x for x in su), 5)
        r_gen = "ACCETTATO"
    except TypeError as e:
        r_gen = f"TypeError: {e}"
    v_ovf = V.verdetto([(1e308, 1)] * 1000, 5)
    print(f"[SONDA C-VD-5] coppie_generatore->{r_gen} | overflow_1e308 esito={v_ovf['esito']!r}, media={v_ovf['media']!r}")

    # C-VD-6: veto_blocchi: priorità fallito > non valutabile, e assenza delle medie blocchi nel rapporto
    coppie_vb = [(-0.5, 1)] * 250 + [(0.1, 1)] * 10 + [(0.0, 0)] * 240 + [(0.5, 1)] * 500
    vb = V.veto_blocchi(coppie_vb, soglia=-0.25, minimo_trade_blocco=50)
    assert vb["esito"] == "fallito"
    v_vb = V.verdetto(su, 5, requisiti=[vb])
    assert v_vb["esito"] == "bocciata" and v_vb["causa"] == "veto: blocchi"
    # Anche bool in S, potenza_stimata, soglia, ampiezza
    for fn, args in (
        (V.controlla_coppie, ([(True, 1)],)),
        (V.screening, (su[:780], 9, True)),
        (V.veto_blocchi, (su, True, 50)),
        (V.veto_blocchi, (su, -0.25, 50, True)),
    ):
        try:
            fn(*args)
            raise AssertionError(f"Bool accettato da {fn.__name__}")
        except ValueError:
            pass
    print("[SONDA C-VD-6] veto_blocchi priorità fallito>sottile OK; bool rifiutato su S, potenza, soglia, ampiezza")


def _run_mut(nome: str, old: str, new: str) -> str:
    with tempfile.TemporaryDirectory(prefix="r18_mvd_") as td:
        tmp = Path(td)
        for parte in ("dati", "laboratorio", "guardian"):
            shutil.copytree(
                ROOT / "brain" / parte,
                tmp / "brain" / parte,
                ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"),
            )
        target = tmp / "brain" / "laboratorio" / "verdetto" / "verdetto_d31.py"
        txt = target.read_text(encoding="utf-8")
        cnt = txt.count(old)
        assert cnt == 1, f"{nome}: target trovato {cnt} volte"
        target.write_text(txt.replace(old, new), encoding="utf-8")
        compile(target.read_text(encoding="utf-8"), "verdetto_d31.py", "exec")
        r = subprocess.run(
            [sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f",
             "brain.laboratorio.tests.test_verdetto_d31"],
            cwd=tmp, env=NO_NET, capture_output=True, text=True, timeout=120,
        )
        esito = "SOPRAVVISSUTO" if r.returncode == 0 else "UCCISO"
        print(f"  [{esito:13s}] {nome} -> rc={r.returncode}")
        return esito


def mutanti_nuovi():
    print("\n[COMPITO C — 7 mutanti nuovi su verdetto_d31.py]")
    muts = [
        (
            "M-VD-01 vicinanza di L non riportata",
            '        out.append("L")',
            '        pass',
        ),
        (
            "M-VD-02 S booleano accettato in controlla_coppie",
            "        if type(s) not in (int, float) or not math.isfinite(s):",
            "        if not isinstance(s, (int, float)) or not math.isfinite(s):",
        ),
        (
            "M-VD-03 potenza_stimata booleana accettata in screening",
            "    if type(potenza_stimata) not in (int, float) or not 0.0 <= potenza_stimata <= 1.0:",
            "    if not isinstance(potenza_stimata, (int, float)) or not 0.0 <= potenza_stimata <= 1.0:",
        ),
        (
            "M-VD-04 soglia booleana accettata in veto_blocchi",
            "    if type(soglia) not in (int, float) or not math.isfinite(soglia):",
            "    if not isinstance(soglia, (int, float)) or not math.isfinite(soglia):",
        ),
        (
            "M-VD-05 ampiezza booleana accettata in veto_blocchi",
            "    if type(ampiezza) is not int or ampiezza < 1 or not coppie or len(coppie) % ampiezza:",
            "    if not isinstance(ampiezza, int) or ampiezza < 1 or not coppie or len(coppie) % ampiezza:",
        ),
        (
            "M-VD-06 id requisito non stringa accettato in _requisiti",
            '        if not isinstance(r, dict) or not isinstance(r.get("id"), str) or type(r.get("veto")) is not bool \\',
            '        if not isinstance(r, dict) or r.get("id") is None or type(r.get("veto")) is not bool \\',
        ),
        (
            "M-VD-07 sedute etichettate DERIVATO invece di MISURA",
            '        _voce("sedute", v["sedute"], "sedute", "MISURA", "esatto", "coppie giornaliere della prova"),',
            '        _voce("sedute", v["sedute"], "sedute", "DERIVATO", "esatto", "coppie giornaliere della prova"),',
        ),
    ]
    esiti = [(nome, _run_mut(nome, old, new)) for nome, old, new in muts]
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"[RIEPILOGO MUTANTI NUOVI VD] {uccisi}/{len(esiti)} uccisi")


def main() -> int:
    sonde()
    mutanti_nuovi()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
