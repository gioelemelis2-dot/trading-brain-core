"""Mutation testing del Guardian G0 e del journal (mandato notturno, 12/11/2026), modellato su mutazioni_v3_3.py.

Ogni mutante è una copia di `guardian/` con UN difetto in UNO dei 6 file operativi (g0/valori.py, g0/strumenti.py,
g0/limiti.py, g0/scheda.py, journal/journal.py, journal/indicatori.py), in una cartella separata; l'originale non è
toccato. Nella copia ci sono anche i 3 documenti di continuità letti da TestAudit7 (altrimenti fallirebbe per ogni
mutante e lo «ucciderebbe» per il motivo sbagliato).

Controlli prima di contare un mutante:
1. la copia NON mutata (M00) deve superare tutta la suite: se fallisce, lo script si ferma (uccisioni non credibili);
2. ogni sostituzione deve comparire esattamente una volta nel file originale;
3. il modulo mutato deve essere importato DALLA COPIA e contenere la mutazione (percorso e testo controllati).

Un mutante è ucciso se la suite (python3 -s -B -W error -m unittest discover -s test) fallisce.
I mutanti «E» sono dichiarati equivalenti, con la motivazione: non entrano nel conteggio dei non equivalenti.

Uso: python3 -s -B mutazioni_g0_journal.py [<cartella brain>] <cartella dei mutanti>
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) == 2:
    BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1])
elif len(sys.argv) == 3:
    BRAIN, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
else:
    sys.exit(__doc__)
GUARDIAN = BRAIN / "guardian"
DOCUMENTI = ("CONTINUITA.md", "governance/DECISIONI-APERTE.md", "governance/REGISTRO-MODIFICHE.md")
VA, ST, LI, SC, JO, IN = ("g0/valori.py", "g0/strumenti.py", "g0/limiti.py", "g0/scheda.py",
                          "journal/journal.py", "journal/indicatori.py")

M = {
    # --- g0/valori.py: schema epistemico ---
    "V01 tipo del risultato = il PIÙ FORTE fra gli input": [
        (VA, "tipo = min(candidati, key=ORDINE_TIPO.__getitem__)", "tipo = max(candidati, key=ORDINE_TIPO.__getitem__)")],
    "V02 NON STIMABILE non più contagioso": [
        (VA, "    if any(not v.stimabile for v in ins):", "    if False:")],
    "V03 restringi può allargare il limite": [
        (VA, "if not candidato.stimabile or candidato.valore >= limite.valore:", "if not candidato.stimabile:")],
    "V04 stato di verifica = il PIÙ FORTE": [
        (VA, "stato = min((v.stato_verifica for v in ins), key=ORDINE_VERIFICA.__getitem__)",
         "stato = max((v.stato_verifica for v in ins), key=ORDINE_VERIFICA.__getitem__)")],
    # --- g0/strumenti.py: perdita allo stop ---
    "V05 commissioni omesse dalla perdita": [(ST, "perdita += commissioni.valore", "perdita += 0")],
    "V06 commissioni negative ammesse": [
        (ST, "if not (commissioni.valore.is_finite() and commissioni.valore >= 0):",
         "if not commissioni.valore.is_finite():")],
    "V07 cambio FX: * invece di /": [(ST, "perdita = perdita_prof / cambio.valore", "perdita = perdita_prof * cambio.valore")],
    "V08 valuta base convertita al prezzo d'ingresso invece che allo stop": [
        (ST, "perdita = perdita_prof / stop.valore", "perdita = perdita_prof / ingresso.valore")],
    "V09 controllo is_finite() rimosso su prezzi, quantità e cambio": [
        (ST, "        if not (v.valore.is_finite() and v.valore > 0):", "        if not (v.valore > 0):")],
    "V10 distanza non multipla del tick ammessa": [(ST, "if tick != tick.to_integral_value():", "if False:")],
    "V11 stop uguale all'ingresso ammesso": [(ST, "if ingresso.valore == stop.valore:", "if False:")],
    # --- g0/limiti.py: limiti FTMO e stress ---
    "V12 limite giornaliero: frazione applicata al saldo invece che al capitale iniziale": [
        (LI, "v = saldo_mezzanotte.valore - f_g.valore * capitale_iniziale.valore",
         "v = saldo_mezzanotte.valore - f_g.valore * saldo_mezzanotte.valore")],
    "V13 frazioni FTMO scambiate (giornaliero con la frazione totale)": [
        (LI, "    f_g, _ = _frazioni(prodotto)", "    _, f_g = _frazioni(prodotto)")],
    "V14 trailing 1-Step/Instant ignorato": [(LI, 'if prodotto != "ftmo_2step" and saldi:', "if False:")],
    "V15 2-Step trattato come trailing": [(LI, 'if prodotto != "ftmo_2step" and saldi:', "if saldi:")],
    "V16 capitale iniziale non positivo ammesso": [
        (LI, "if not (capitale_iniziale.valore.is_finite() and capitale_iniziale.valore > 0):", "if False:")],
    "V17 scenario di stress senza le riserve dichiarate": [
        (LI, "ins = list(perdite_allo_stop) + list(riserve)", "ins = list(perdite_allo_stop)")],
    # --- g0/scheda.py: avvisi e regole personali ---
    "V18 P-05 regola aurea: >= diventa > (limite personale UGUALE a quello FTMO accettato)": [
        (SC, "if v >= f_g.valore:", "if v > f_g.valore:")],
    "V19 P-01: > diventa >= (rischio uguale alla soglia segnalato)": [(SC, "if frac.valore > v:", "if frac.valore >= v:")],
    "V20 P-11/P-14: < diventa <= (valore uguale alla soglia = violazione)": [
        (SC, 'violata = (x < v) if rid in ("P-11", "P-14") else (x >= v)',
         'violata = (x <= v) if rid in ("P-11", "P-14") else (x >= v)')],
    "V21 P-15: >= diventa > (raggiunto il massimo di perdite: nessun avviso)": [
        (SC, 'violata = (x < v) if rid in ("P-11", "P-14") else (x >= v)',
         'violata = (x < v) if rid in ("P-11", "P-14") else (x > v)')],
    "V22 P-05: avvisi su trade soppressi a margine personale negativo (difetto reintrodotto)": [
        (SC, "if pt is not None and pt.valore > margine_p.valore:",
         "if margine_p.valore >= 0 and pt is not None and pt.valore > margine_p.valore:")],
    "V23 trade previsto: > diventa >= sul margine giornaliero (equity AL limite = violazione)": [
        (SC, "if pt.valore > mg.valore:", "if pt.valore >= mg.valore:")],
    "V24 posizione aperta misurata dal prezzo d'ingresso": [
        (SC, 'da = p["prezzo_attuale"] if aperta else p["ingresso"]', 'da = p["ingresso"]')],
    "V25 dati di sessione negativi ammessi": [(SC, "if x is None or x < 0:", "if x is None:")],
    "V26 _numero accetta NaN e infiniti": [(SC, "return d if d.is_finite() else None", "return d")],
    "V27 stress: < diventa <= sul margine giornaliero dopo lo scenario": [
        (SC, "if dopo.valore < 0:", "if dopo.valore <= 0:")],
    "V28 stress: margine totale dopo lo scenario non controllato": [(SC, "if dopo_t.valore < 0:", "if False:")],
    # --- journal/journal.py ---
    "V29 versioni_finali: catene di correzioni non risolte": [
        (JO, 'r = radice.get(d["corregge"], d["corregge"]) if "corregge" in d else rec["id"]',
         'r = d["corregge"] if "corregge" in d else rec["id"]')],
    "V30 impronta esterna non controllata": [(JO, "elif _sha(_canonico(ancora)) != impronta_attesa:", "elif False:")],
    "V31 doppia chiusura di una previsione ammessa": [(JO, "    if gia:\n", "    if False:\n")],
    "V32 chiude verso una correzione ammesso": [(JO, 'if "corregge" in bersaglio:', "if False:")],
    "V33 corregge fra record di natura diversa ammesso": [(JO, 'if ("chiude" in corretto) != esito:', "if False:")],
    "V34 catena di hash non controllata": [(JO, 'if rec.get("prec_hash") != prec:', "if False:")],
    "V35 Brier: errore assoluto invece del quadrato": [
        (JO, '(d["probabilita"] - esiti[pid]) ** 2', 'abs(d["probabilita"] - esiti[pid])')],
    "V36 journal: orari non UTC ammessi": [
        (JO, "if t.tzinfo is None or t.utcoffset() != timedelta(0):", "if t.tzinfo is None:")],
    "V37 journal: chiusura nello stesso istante dell'apertura rifiutata (< diventa <=)": [
        (JO, 'orari["chiuso_utc"] < orari["aperto_utc"]', 'orari["chiuso_utc"] <= orari["aperto_utc"]')],
    "V38 journal: probabilità booleana ammessa": [
        (JO, "if isinstance(p, bool) or not isinstance(p, (int, float))", "if not isinstance(p, (int, float))")],
    "V39 sigillo verificato senza nonce": [
        (JO, "return secrets.compare_digest(impegno, _sha(nonce + _canonico(payload)))",
         "return secrets.compare_digest(impegno, _sha(_canonico(payload)))")],
    "V40 ancora non controllata da verifica()": [(JO, "    problemi += _verifica_ancora(cartella)\n", "")],
    # --- journal/indicatori.py ---
    "V41 indicatori: microsecondi ignorati nelle durate": [
        (IN, " + Decimal(d.microseconds) / Decimal(1_000_000)", "")],
    "V42 indicatori: orari non UTC ammessi": [
        (IN, "if t.tzinfo is None or t.utcoffset() != timedelta(0):", "if t.tzinfo is None:")],
    "V43 R1: < invece di <= sui minuti (rientro esattamente al limite escluso)": [
        (IN, 'm["minuti_dopo_perdita"] <= minuti_max', 'm["minuti_dopo_perdita"] < minuti_max')],
    "V44 indicatori: un pareggio conta come perdita": [
        (IN, 'if _dec(prec["pnl_conto"]) < 0:', 'if _dec(prec["pnl_conto"]) <= 0:')],
    # --- equivalenti dichiarati ---
    "E01 ancora: confronto del numero di righe rimosso (EQUIVALENTE)": [
        (JO, 'if a["righe"] != len(righe) or a["ultimo_hash"] != ultimo:', 'if a["ultimo_hash"] != ultimo:')],
}
EQUIVALENTI = {
    "E01": "Se l'ultima riga coincide con quella ancorata, il suo prec_hash fissa la riga precedente e così via fino "
           "alla genesi: la catena determina tutte le righe e quindi il loro numero. Ogni file con lo stesso ultimo "
           "hash ma un numero di righe diverso rompe la catena, che verifica() segnala comunque. Cambia solo il "
           "testo del messaggio, non l'esito della verifica (salvo collisioni di SHA-256).",
}


def copia(dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(GUARDIAN, dest / "brain" / "guardian",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "dati"))
    for doc in DOCUMENTI:
        (dest / "brain" / doc).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BRAIN / doc, dest / "brain" / doc)
    return dest / "brain" / "guardian"


def esegui(g: Path):
    dati = g.parent.parent / "journal_dati"
    env = {"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1", "TRADING_JOURNAL_DIR": str(dati)}
    r = subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "discover", "-s", "test"],
                       cwd=g, capture_output=True, text=True, timeout=600, env=env)
    falliti = [l.split()[1] for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    return r.returncode, falliti, r.stderr


def importato(g: Path, modulo: str, prima: str, dopo: str) -> None:
    """Il modulo deve venire dalla copia e contenere la mutazione: il testo nuovo presente oppure, per una
    cancellazione, il testo originale assente."""
    nome = modulo[:-3].replace("/", ".")
    env = {"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}
    r = subprocess.run([sys.executable, "-s", "-B", "-c", f"import {nome} as m; print(m.__file__)"],
                       cwd=g, capture_output=True, text=True, env=env)
    percorso = Path(r.stdout.strip())
    assert percorso == g / modulo, (modulo, r.stdout, r.stderr)
    testo = percorso.read_text(encoding="utf-8")
    assert (dopo in testo) if dopo.strip() else (prima not in testo), (modulo, "mutazione assente nel modulo importato")


OUT.mkdir(parents=True, exist_ok=True)
g0 = copia(OUT / "M00")
rc, falliti, err = esegui(g0)
print(f"{'CONTROLLO' if rc == 0 else 'ERRORE':13s} M00 copia non mutata: suite {'verde' if rc == 0 else 'ROSSA'}")
if rc:
    sys.exit("la copia non mutata fallisce: uccisioni non credibili\n" + err[-3000:])

ris = []
for nome, subs in M.items():
    mid = nome.split()[0]
    g = copia(OUT / mid)
    for f, a, b in subs:
        p = g / f
        c = p.read_text(encoding="utf-8")
        assert c.count(a) == 1, (nome, f, a[:60], c.count(a))
        p.write_text(c.replace(a, b, 1), encoding="utf-8")
        assert p.read_text(encoding="utf-8") != (GUARDIAN / f).read_text(encoding="utf-8"), nome
        importato(g, f, a, b)
    rc, falliti, _ = esegui(g)
    esito = "UCCISO" if rc else ("EQUIVALENTE" if mid in EQUIVALENTI else "SOPRAVVISSUTO")
    ris.append((mid, esito))
    file_ = ", ".join(sorted({f for f, _, _ in subs}))
    print(f"{esito:13s} {nome}  ({file_})" + (f"  [{', '.join(falliti)}]" if falliti else ""))
    shutil.rmtree(OUT / mid)
shutil.rmtree(OUT / "M00")

non_eq = [x for x in ris if x[0] not in EQUIVALENTI]
uccisi = sum(1 for _, e in non_eq if e == "UCCISO")
print()
for k, v in EQUIVALENTI.items():
    print(f"{k} equivalente: {v}")
print(f"\nMutanti non equivalenti uccisi: {uccisi}/{len(non_eq)}")
per_file = {}
for (mid, e), subs in zip(ris, M.values()):
    if mid not in EQUIVALENTI:
        for f in {f for f, _, _ in subs}:
            t = per_file.setdefault(f, [0, 0])
            t[0] += e == "UCCISO"
            t[1] += 1
print("Per file: " + "; ".join(f"{f} {u}/{n}" for f, (u, n) in sorted(per_file.items())))
sys.exit(0 if uccisi == len(non_eq) else 1)
