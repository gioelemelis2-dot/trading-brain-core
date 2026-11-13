"""Mutation testing della correzione del DSR e della partizione per date (13/11/2026), sul modello di
guardian/test/mutazioni_g0_journal.py.

Ogni mutante è una copia di `brain/` (solo dati/, laboratorio/, guardian/) con UN difetto, in una cartella separata;
l'originale non è toccato. Controlli prima di contare un mutante:
1. la copia NON mutata (M00) deve superare la suite, altrimenti ci si ferma;
2. ogni sostituzione deve comparire esattamente una volta nel file originale;
3. il file mutato nella copia deve contenere la mutazione.
Un mutante è ucciso se la suite (i 6 moduli di test di dati/ e laboratorio/) fallisce.

Uso (dalla radice del repository): python3 -s -B brain/dati/tests/mutazioni_dsr_partizione.py <cartella dei mutanti>
"""
import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(__doc__)
BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve()
DS, PD, DK = "laboratorio/backtester/dsr.py", "dati/pipeline/partizione_date.py", "dati/pipeline/dukascopy.py"
SUITE = ["brain.dati.tests.test_pipeline", "brain.dati.tests.test_dukascopy", "brain.dati.tests.test_partizione_date",
         "brain.laboratorio.tests.test_backtester", "brain.laboratorio.tests.test_anti_frode_statico",
         "brain.laboratorio.tests.test_dsr_scala"]

M = {
    # --- DSR ---
    "D01 soglia senza scala sqrt(V) (il difetto originale)": [(DS, "sr_star = math.sqrt(v) * (", "sr_star = 1.0 * (")],
    "D02 varianza nulla 1/T invece di 1/(T-1)": [
        (DS, "else 1.0 / (track_record_length - 1)", "else 1.0 / track_record_length")],
    "D03 varianza empirica ignorata": [(DS, "varianza = max(v_nulla, v_emp)", "varianza = v_nulla")],
    "D04 varianza = min invece di max": [(DS, "varianza = max(v_nulla, v_emp)", "varianza = min(v_nulla, v_emp)")],
    "D05 varianza non valida accettata": [
        (DS, "not (math.isfinite(varianza_sr_prove) and varianza_sr_prove > 0)", "False")],
    "D06 Sharpe registrati ignorati": [(DS, "campione = sr_registrati + [sharpe_float]", "campione = [sharpe_float]")],
    "D07 secondo termine con N invece di N e": [
        (DS, "inv_cdf(1.0 - 1.0 / (num_trials * math.e))", "inv_cdf(1.0 - 1.0 / num_trials)")],
    # --- partizione per date ---
    "P01 embargo ignorato": [(PD, 'inizio < prec["fine_utc"] + timedelta(days=emb)', 'inizio < prec["fine_utc"]')],
    "P02 ordine dei blocchi non controllato": [(PD, 'if inizio < prec["inizio_utc"]:', "if False:")],
    "P03 nomi ripetuti ammessi": [(PD, "or nome in nomi:", "or False:")],
    "P04 ruolo non controllato": [(PD, 'if b.get("ruolo") not in RUOLI:', "if False:")],
    "P05 nessun blocco di verifica ammesso": [
        (PD, 'if not any(b["ruolo"] == "verifica" for b in out):', "if False:")],
    "P06 fine inclusa (candele oltre il confine)": [
        (PD, 'c.close_time <= b["fine_utc"]', 'c.open_time <= b["fine_utc"]')],
    "P07 nonce sovrascrivibile": [(PD, 'open(cartella_nonce / NONCE, "x"', 'open(cartella_nonce / NONCE, "w"')],
    "P08 anche lo sviluppo sigillato": [(PD, 'if b["ruolo"] == "verifica":\n            d["commitment_hash"]',
                                          'if True:\n            d["commitment_hash"]')],
    "P09 blocchi vuoti ammessi": [(PD, "if vuoti:", "if False:")],
    "P10 simbolo non controllato": [(PD, 'if simboli != {partizione["simbolo"]}:', "if False:")],
    "P11 verifica ignora il sigillo": [
        (PD, 'valido = all(e["sha256"] and e["commitment"] is not False for e in esito.values())',
         'valido = all(e["sha256"] for e in esito.values())')],
    "P12 embargo negativo ammesso": [(PD, "or emb < 0:", "or False:")],
    "P13 candele escluse non contate": [(PD, "            escluse += 1", "            escluse += 0")],
    # --- scaricatore ---
    "K01 banda ignorata": [(DK, "if not prezzo_min <= c[k] <= prezzo_max:", "if False:")],
    "K02 salto di scala ignorato": [(DK, "if rapporto > SALTO_MAX or rapporto < 1 / SALTO_MAX:", "if False:")],
    "K03 salto solo verso l'alto": [(DK, "if rapporto > SALTO_MAX or rapporto < 1 / SALTO_MAX:",
                                     "if rapporto > SALTO_MAX:")],
    "K04 anno senza banda accettato": [
        (DK, '    raise ErroreDati(f"{simbolo}: nessuna banda', '    return Decimal(0), Decimal(10**9)\n    raise ErroreDati(f"{simbolo}: nessuna banda')],
    "K05 sigillo anche senza partizione decisa": [(DK, "    if partizione is None:\n        info_partizione",
                                                   "    if False:\n        info_partizione")],
    "K06 periodo fino alla fine esclusa": [
        (DK, 'blocchi[-1]["fine_utc"].date() - timedelta(days=1)', 'blocchi[-1]["fine_utc"].date()')],
}


def copia(dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,      # niente dati scaricati né sigilli reali
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv",
                                                      "*.secret"))


def suite(radice: Path) -> bool:
    r = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *SUITE], cwd=radice,
                       capture_output=True, text=True, timeout=600)
    return r.returncode == 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = OUT / "M00"
    copia(base)
    if not suite(base):
        sys.exit("M00 (copia non mutata) NON supera la suite: uccisioni non credibili, fermo.")
    print("M00 copia non mutata: suite verde")
    uccisi = 0
    for i, (nome, sostituzioni) in enumerate(M.items(), 1):
        dest = OUT / f"M{i:02d}"
        copia(dest)
        for f, vecchio, nuovo in sostituzioni:
            testo = (BRAIN / f).read_text(encoding="utf-8")
            if testo.count(vecchio) != 1:
                sys.exit(f"{nome}: la sostituzione compare {testo.count(vecchio)} volte in {f}, non 1")
            (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
            if nuovo not in (dest / "brain" / f).read_text(encoding="utf-8"):
                sys.exit(f"{nome}: mutazione non applicata nella copia")
        vivo = suite(dest)
        uccisi += not vivo
        print(f"{'VIVO  ' if vivo else 'UCCISO'} {nome}")
        shutil.rmtree(dest)
    print(f"\n{uccisi}/{len(M)} mutanti uccisi")
    return 0 if uccisi == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
