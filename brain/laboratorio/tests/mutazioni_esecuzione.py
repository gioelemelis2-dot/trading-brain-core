"""Mutation testing del pacchetto laboratorio/esecuzione (sigillo, criteri, caricatore, esecutore di H-002).
Ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve superare i test; ogni sostituzione deve
comparire una sola volta. Il generatore di mercati inventati (sintetico.py) è strumento di prova: non si muta.
Uso (dalla radice del repository): python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella> [processi] [prefissi]
  prefissi: per esempio «S,C» per far girare solo i mutanti che iniziano con S o C (utile con poco tempo).
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if len(sys.argv) not in (2, 3, 4):
    sys.exit(__doc__)
BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve()
PROCESSI = int(sys.argv[2]) if len(sys.argv) >= 3 else 2
PREFISSI = tuple(sys.argv[3].split(",")) if len(sys.argv) == 4 else ("",)
SUITE = ["brain.laboratorio.tests.test_esecuzione", "brain.laboratorio.tests.test_esegui_h002"]
SG = "laboratorio/esecuzione/sigillo.py"
K = "laboratorio/esecuzione/criteri.py"
C = "laboratorio/esecuzione/caricatore.py"
E = "laboratorio/esecuzione/esegui_h002.py"
M = {
    "S01 doppio sigillo ammesso": [(SG, "    if _sigillo(dati, ipotesi) is not None:\n", "    if False:\n")],
    "S02 impronta della scheda non controllata": [(SG, "if impronta(scheda) != s[\"scheda_sha256\"]:", "if False:")],
    "S03 verifica ripetibile": [(SG, "if ruolo == \"verifica\" and any(", "if False and any(")],
    "S04 esecuzione senza sigillo": [(SG, "raise NonSigillata(f\"{ipotesi} non risulta sigillata: nessuna esecuzione\")",
                                      "pass")],
    "S05 N conta anche le esecuzioni": [(SG, "return sum(1 for p in dati[\"prove\"] if p[\"ruolo\"] == \"selezionabile\")",
                                         "return len(dati[\"prove\"]) + len(dati[\"esecuzioni\"])")],
    "S06 ruolo dell'esecuzione non controllato": [(SG, "if ruolo not in RUOLI_ESECUZIONE:", "if False:")],
    "S07 varianti duplicate ammesse": [(SG, "len(set(varianti)) != len(varianti)", "False")],
    "S08 sigillo dopo esecuzioni ammesso": [(SG, "if any(e[\"ipotesi\"] == ipotesi for e in dati[\"esecuzioni\"]):",
                                             "if False:")],
    "S09 schema del registro non controllato": [(SG, "if dati.get(\"schema\") != SCHEMA:", "if False:")],
    "K01 percentile al rango sbagliato": [(K, "k = max(1, math.ceil(q * len(ordinati) - 1e-9))",
                                           "k = max(1, math.floor(q * len(ordinati)))")],
    "K02 confronto casuale con >=": [(K, "\"sopra\": r_strategia > p}", "\"sopra\": r_strategia >= p}")],
    "K03 seme ignorato": [(K, "rng = random.Random(seme)", "rng = random.Random()")],
    "K04 benchmark sull'unione dei giorni": [(K, "comuni = sorted(set(strategia) & set(compro) & set(vendo))",
                                              "comuni = sorted(set(strategia) | set(compro) | set(vendo))")],
    "K05 basta battere un benchmark": [(K, "\"batte_entrambi\": rs > rc and rs > rv}", "\"batte_entrambi\": rs > rc or rs > rv}")],
    "K06 veto: base non positiva ignorata": [(K, "if r_base is None or r_base <= 0:", "if r_base is None:")],
    "K07 veto: metà esatta bocciata": [(K, "elif r_base is not None and r_base > 0 and r < quota * r_base:",
                                        "elif r_base is not None and r_base > 0 and r <= quota * r_base:")],
    "K08 veto: prova senza trade non gestita": [(K, "if r is None or r <= 0:", "if r <= 0:")],
    "K09 R medio con >": [(K, "_criterio(\"R medio netto\", r, f\"≥ {r_min}\", _ge(r, r_min))",
                           "_criterio(\"R medio netto\", r, f\"≥ {r_min}\", r is not None and r > r_min)")],
    "K10 Sharpe ignorato": [(K, "_ge(m.get(\"sharpe\"), sharpe_min)", "True")],
    "K11 trade minimi con >": [(K, "m.get(\"n\", 0) >= trade_min", "m.get(\"n\", 0) > trade_min")],
    "K12 confronto casuale ignorato": [(K, "casuale.get(\"sopra\", False)),", "True),")],
    "K13 benchmark ignorati": [(K, "benchmark.get(\"batte_entrambi\", False)),", "True),")],
    "K14 vendite ignorate": [(K, "_ge(m.get(\"r_vendite\"), vendite_min)", "True")],
    "K15 drawdown dello screening a 13R": [(K, "dd_max: float = 12.0", "dd_max: float = 13.0")],
    "K16 veto ignorato": [(K, "\"nessun veto\", not veto),", "\"nessun veto\", True),")],
    "K17 stress ignorato": [(K, "r_stress is not None and r_stress > 0),", "True),")],
    "K18 anno senza trade positivo": [(K, "if somme.get(a, 0.0) > 0) / len(tutti)", "if somme.get(a, 0.0) >= 0) / len(tutti)")],
    "K19 DSR con N = 1": [(K, "calculate_dsr_analytical(sr, n_prove, len(rs)", "calculate_dsr_analytical(sr, 1, len(rs)")],
    "K20 varianza empirica ignorata": [(K, "            v = max(v, variance(list(sharpe_prove) + [sr]))\n",
                                        "            v = v\n")],
    "K21 ultimi 5 anni diventano 6": [(K, "if x[\"data\"].year > ultimo - ultimi)", "if x[\"data\"].year >= ultimo - ultimi)")],
    "K22 quota degli anni con >": [(K, "qa >= quota_anni),", "qa > quota_anni),")],
    "K23 R medio della verifica ignorato": [(K, "\"> 0\", r is not None and r > 0),", "\"> 0\", True),")],
    "K24 curtosi in eccesso": [(K, "return m3 / m2 ** 1.5, m4 / m2 ** 2", "return m3 / m2 ** 1.5, m4 / m2 ** 2 - 3")],
    "K25 trade non ordinati per data": [(K, "rs = [x[\"r\"] for x in sorted(tr, key=lambda x: x[\"data\"])]",
                                         "rs = [x[\"r\"] for x in tr]")],
    "K26 percentile al 90%": [(K, "seme: int = SEME, q: float = 0.95)", "seme: int = SEME, q: float = 0.90)")],
    "K27 ripetizioni 999": [(K, "RIPETIZIONI = 1000", "RIPETIZIONI = 999")],
    "C01 sviluppo nel periodo sigillato": [(C, "if inizio < INIZIO_SVILUPPO:", "if False:")],
    "C02 verifica senza sigillo": [(C, "        S.controlla_sigillo(registro, ipotesi, scheda)\n", "")],
    "C03 verifica senza il 31/10 compreso": [(C, "if fine > FINE_VERIFICA:", "if fine >= FINE_VERIFICA:")],
    "C09 embargo aperto (P7 di Gemini)": [(C, "if fine > FINE_VERIFICA:", "if fine >= INIZIO_SVILUPPO:")],
    "C04 high e low scambiati": [(C, "out[t] = (float(o), float(h), float(l), float(c))",
                                  "out[t] = (float(o), float(l), float(h), float(c))")],
    "C05 giorni mancanti non contati": [(C, "            mancanti += 1\n", "            pass\n")],
    "C06 ASK letti dalla cartella BID": [(C, "ask, ma = _leggi_cache(cartella_ask,", "ask, ma = _leggi_cache(cartella_bid,")],
    "C07 modalità non controllata": [(C, "if modalita not in MODALITA:", "if False:")],
    "C08 periodo rovesciato ammesso": [(C, "if fine < inizio:", "if False:")],
    "E01 robustezza solo se la base è positiva": [(E, "for nome, cambi in robustezza.items():",
                                                    "for nome, cambi in (robustezza.items() if (m.get(\"r_medio\") or 0) > 0 else []):")],
    "E02 memoria di prepara senza range e tetto": [(E, "chiave = replace(par, target_r=None, stress=0.0)",
                                                     "chiave = replace(par, target_r=None, stress=0.0, or_minuti=30, tetto=2.0)")],
    "E03 stress non applicato": [(E, "_r_medio(sim, giorni, replace(par, stress=stress))", "_r_medio(sim, giorni, par)")],
    "E04 casuale con un solo benchmark": [(E, "esiti = [(compro[d], vendo[d])", "esiti = [(compro[d], compro[d])")],
    "E05 vendo sempre = compro sempre": [(E, "sim.specchio(giorni, par, lato_fisso=\"vendita\")",
                                          "sim.specchio(giorni, par, lato_fisso=\"acquisto\")")],
    "E06 sigillo non controllato dalla riga di comando": [
        (E, "sigillo = S.controlla_sigillo(x.registro, x.ipotesi, x.scheda)", "sigillo = {\"scheda_sha256\": \"-\"}")],
    "E07 robustezza non registrata": [(E, "for nome, rm in r[\"robustezza\"].items():", "for nome, rm in []:")],
    "E08 rapporto senza impronta": [(E, "\"scheda\": f\"{x.scheda.name}, SHA-256 {sigillo['scheda_sha256']}\",",
                                     "\"scheda\": x.scheda.name,")],
    "E09 target nella robustezza di V-S": [(E, "\"V-S\": dict(_RANGE_TETTO)}",
                                            "\"V-S\": dict(_RANGE_TETTO, **{\"target 1,2\": {\"target_r\": 1.2}})}")],
    "E10 stress a 0,10": [(E, "STRESS = 0.20", "STRESS = 0.10")],
    "E11 verifica di varianti non promosse": [(E, "trade = {v: sim.trade(prep(varianti[v]), varianti[v]) for v in promosse}\n"
                                                  "    metriche = {v: sim.metriche(trade[v]) for v in promosse}\n"
                                                  "    sharpe = {v: metriche[v].get(\"sharpe\") for v in promosse}",
                                               "trade = {v: sim.trade(prep(varianti[v]), varianti[v]) for v in varianti}\n"
                                               "    metriche = {v: sim.metriche(trade[v]) for v in varianti}\n"
                                               "    sharpe = {v: metriche[v].get(\"sharpe\") for v in varianti}")],
    "E12 verifica senza --varianti ammessa": [(E, "if not promosse or ignote:\n                raise",
                                               "if ignote:\n                raise")],
    "E13 basta una promozione (P1 di Gemini)": [(E, "esiti_sviluppo.get(v) and all(esiti_sviluppo[v])",
                                                 "esiti_sviluppo.get(v) and any(esiti_sviluppo[v])")],
    "E14 verifica di una parte delle promosse (P2 di Gemini)": [
        (E, "if sorted(promosse) != sorted(da_verificare):", "if not set(promosse) <= set(da_verificare):")],
    "E15 sigillo con varianti diverse ammesso (P3 di Gemini)": [
        (E, "if sorted(sigillo[\"varianti\"]) != sorted(VARIANTI):", "if False:")],
    "E16 anni del periodo non passati (P4 di Gemini)": [
        (E, "anni=range(x.inizio.year, x.fine.year + 1)", "anni=None")],
    "E17 casuale contro l'R di tutti i trade (P5 di Gemini)": [
        (E, "r_comuni = mean(strategia[d] for d in comuni)", "r_comuni = m[\"r_medio\"]")],
    "E18 dati incompleti ammessi (P6 di Gemini)": [
        (E, "if info[\"giorni_bid_mancanti\"] or info[\"giorni_ask_mancanti\"] or not info[\"minuti_bid\"] \\\n"
            "                or not info[\"minuti_ask\"]:",
         "if not info[\"minuti_bid\"] and not info[\"minuti_ask\"]:")],
    "K28 ultimi 5 anni dall'ultimo trade (P4 di Gemini)": [
        (K, "ultimo = max(anni) if anni is not None else max(x[\"data\"].year for x in tr)",
         "ultimo = max(x[\"data\"].year for x in tr)")],
    "S10 registro senza blocco (P8 di Gemini)": [
        (SG, "    with _bloccato(registro):\n        return _registra(", "    if True:\n        return _registra(")],
    "MG01 V senza gli Sharpe delle altre promosse (Gemini)": [
        (E, "        altri = [s for k, s in sharpe.items() if k != v and s is not None]", "        altri = []")],
    "MG03 R medio della verifica con >= (Gemini)": [(K, "r is not None and r > 0),", "r is not None and r >= 0),")],
    "MG04 drawdown della verifica con <= (Gemini)": [
        (K, "cumulato is not None and cumulato > 0),\n        _criterio(\"drawdown massimo (R)\", dd, f\"< {dd_max}\", dd is not None and dd < dd_max),",
         "cumulato is not None and cumulato > 0),\n        _criterio(\"drawdown massimo (R)\", dd, f\"< {dd_max}\", dd is not None and dd <= dd_max),")],
    "MG06 varianza nulla 1/T (Gemini)": [(K, "        v = 1.0 / (len(rs) - 1)", "        v = 1.0 / len(rs)")],
    "MG07 ultimi 5 anni con >= (Gemini)": [(K, "cumulato is not None and cumulato > 0),", "cumulato is not None and cumulato >= 0),")],
}


def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f", *SUITE], cwd=radice,
                          capture_output=True, text=True, timeout=900).returncode == 0


def mutante(i, nome, sost):
    dest = OUT / f"M{i:02d}"
    copia(dest)
    for f, vecchio, nuovo in sost:
        testo = (dest / "brain" / f).read_text(encoding="utf-8")
        if testo.count(vecchio) != 1:
            shutil.rmtree(dest)
            return nome, f"ERRORE: la sostituzione compare {testo.count(vecchio)} volte in {f}"
        (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
    vivo = suite(dest)
    shutil.rmtree(dest)
    return nome, "VIVO" if vivo else "UCCISO"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    copia(OUT / "M00")
    if not suite(OUT / "M00"):
        sys.exit("M00 NON supera la suite: fermo")
    shutil.rmtree(OUT / "M00")
    print("M00 copia non mutata: suite verde", flush=True)
    with ThreadPoolExecutor(PROCESSI) as ex:
        esiti = list(ex.map(lambda a: mutante(*a), [(i, n, s) for i, (n, s) in enumerate(M.items(), 1) if n.startswith(PREFISSI)]))
    for nome, esito in esiti:
        print(f"{esito:6} {nome}")
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]})")
    return 0 if uccisi == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
