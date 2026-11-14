"""Mutation testing del simulatore di H-002 (laboratorio/simulatori/orb_londra.py). Ogni mutante è una copia di
brain/ con UN difetto; la copia non mutata deve superare i test; ogni sostituzione deve comparire una sola volta.
Uso (dalla radice del repository): python3 -s -B brain/laboratorio/tests/mutazioni_orb.py <cartella dei mutanti>
"""
import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(__doc__)
BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve()
F = "laboratorio/simulatori/orb_londra.py"
SUITE = ["brain.laboratorio.tests.test_orb_londra"]
M = {
    "O01 mediana con la sessione corrente (sguardo al futuro)": [
        (F, "        rif = median(storico_a[-par.sessioni_rif:]) if len(storico_a) >= par.sessioni_rif else None\n",
         "        rif = median((storico_a + [a])[-par.sessioni_rif:]) if len(storico_a) >= par.sessioni_rif else None\n")],
    "O02 tetto con >=": [(F, "if a > par.tetto * rif:", "if a >= par.tetto * rif:")],
    "O03 minimo dei costi ignorato": [(F, "if a < par.molt_costi * costo:", "if False:")],
    "O04 minuti del range non controllati": [(F, "len(or_t) < par.minuti_or_min * par.or_minuti", "False")],
    "O05 festivi non esclusi": [(F, "or g in esclusi(g.year) ", "")],
    "O06 chiusura della candela dal primo minuto": [(F, "chiusura = bid[dentro[-1]][3]", "chiusura = bid[dentro[0]][3]")],
    "O07 ultimo segnale escluso": [(F, "while t_candela <= ultimo:", "while t_candela < ultimo:")],
    "O08 acquisto al BID": [(F, "entrata = a0[0] + par.slip_ingresso + par.stress", "entrata = b0[0] + par.slip_ingresso + par.stress")],
    "O09 stop della vendita sul BID": [(F, "tocca_stop = b[2] <= stop if su else a[1] >= stop",
                                         "tocca_stop = b[2] <= stop if su else b[1] >= stop")],
    "O10 target anche nel minuto d'ingresso": [(F, "if k > 0 and target is not None:", "if target is not None:")],
    "O11 target prima dello stop": [(F, "        if tocca_stop:                                                   # in salto", "        if tocca_stop and not ((b[1] >= target) if (su and target) else False):  # in salto")],
    "O12 fine sessione con >": [(F, "        if t >= fine:", "        if t > fine:")],
    "O13 slittamento dello stop ignorato": [(F, "(min(stop, b[0]) - par.slip_uscita - par.stress)",
                                              "(min(stop, b[0]) - par.stress)")],
    "O14 commissione ignorata": [(F, "netto = once * (per_oncia - par.commissione)", "netto = once * per_oncia")],
    "O15 dimensione senza commissione": [(F, "round((perdita_allo_stop + par.commissione) * MICRO)",
                                           "round(perdita_allo_stop * MICRO)")],
    "O16 filtro del rischio minimo ignorato": [(F, "if rischio < par.rischio_min_a * giorno.a:", "if False:")],
    "O17 prezzo già oltre lo stop ammesso": [(F, "        if b0[0] <= stop:\n            return None\n", "")],
    "O18 stress non applicato": [(F, "entrata = a0[0] + par.slip_ingresso + par.stress", "entrata = a0[0] + par.slip_ingresso")],
    "O19 specchio: stop non alla stessa distanza": [(F, "stop = entrata - distanza if lato == \"acquisto\" else entrata + distanza",
                                                       "stop = entrata - 2 * distanza if lato == \"acquisto\" else entrata + 2 * distanza")],
    "O20 drawdown dal minimo invece che dal picco": [(F, "dd = max(dd, picco - cum)", "dd = max(dd, -cum)")],
    "O21 stop dell'acquisto in salto eseguito al livello": [(F, "(min(stop, b[0]) - par.slip_uscita", "(stop - par.slip_uscita")],
    "O22 stop della vendita in salto eseguito al livello": [(F, "(max(stop, a[0]) + par.slip_uscita", "(stop + par.slip_uscita")],
    "O23 uscita di fine sessione senza limite di attesa": [(F, "fine <= t < fine + par.attesa_max", "fine <= t")],
    "O24 ingresso in ritardo ammesso": [(F, "elif sessione[0] >= fine_candela + par.attesa_max:", "elif False:")],
    "O25 spread negativo eseguibile": [(F, "return t in ask_t and ask[t][0] >= bid[t][0] and ask[t][3] >= bid[t][3]",
                                         "return t in ask_t")],
    "O26 costo di riferimento senza lo spread": [(F, "costo = median(spread_prec) + par.commissione", "costo = par.commissione")],
    "O27 festivi inglesi ignorati": [(F, "return festivi_inglesi(anno) | {", "return set() | {")],
    "O28 Natale di sabato senza secondo sostituto": [(F, "s |= {date(anno, 12, 27), date(anno, 12, 28)}", "s |= {date(anno, 12, 27)}")],
    "O30 spread richiesti: basta uno": [(F, "if len(spread_prec) < par.spread_min:", "if not spread_prec:")],
    "O31 Sharpe con deviazione di popolazione": [(F, "sd = stdev(rs) if len(rs) > 1 else 0.0", "sd = (sum((r - mean(rs)) ** 2 for r in rs) / len(rs)) ** 0.5 if len(rs) > 1 else 0.0")],
    "O32 ultimi anni contati male": [(F, 'if x["data"].year > ultimo - anni)', 'if x["data"].year >= ultimo - anni)')],
    "O33 resoconto senza minuti con spread negativo": [(F, "            negativi += sum(", "            negativi += 0 * sum(")],
    "O34 spread di riferimento dalla fine del range (D1 di Gemini)": [
        (F, "if t >= inizio_spread and eseguibile(t)", "if t >= fine_or and eseguibile(t)")],
    "O35 once in virgola mobile (D2 di Gemini)": [
        (F, "once = round(par.rischio_usd * MICRO) // round((perdita_allo_stop + par.commissione) * MICRO)",
         "once = int(par.rischio_usd // (perdita_allo_stop + par.commissione))")],
    "O36 segnale dalla chiusura della giornata (sguardo al futuro)": [
        (F, "chiusura = bid[dentro[-1]][3]", "chiusura = bid[per_data[g][-1]][3]")],
    "O37 slittamento d'ingresso della vendita a favore": [
        (F, "entrata = b0[0] - par.slip_ingresso - par.stress", "entrata = b0[0] + par.slip_ingresso - par.stress")],
    "O38 ora legale ignorata": [
        (F, "return datetime.combine(giorno, ora, tzinfo=LONDRA).astimezone(timezone.utc)",
         "return datetime.combine(giorno, ora, tzinfo=timezone.utc)")],
    "O39 servono 25 minuti su 30": [
        (F, "len(or_t) < par.minuti_or_min * par.or_minuti", "len(or_t) <= par.minuti_or_min * par.or_minuti")],
    "O40 vendita con ASK già allo stop ammessa": [(F, "if a0[0] >= stop:", "if a0[0] > stop:")],
    "O29 festivi spostati ignorati": [(F, "        s.discard(vecchio)\n        s.add(nuovo)", "        pass")],
}


def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", *SUITE], cwd=radice,
                          capture_output=True, text=True, timeout=600).returncode == 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    copia(OUT / "M00")
    if not suite(OUT / "M00"):
        sys.exit("M00 NON supera la suite: fermo")
    print("M00 copia non mutata: suite verde")
    uccisi = 0
    for i, (nome, sost) in enumerate(M.items(), 1):
        dest = OUT / f"M{i:02d}"
        copia(dest)
        for f, vecchio, nuovo in sost:
            testo = (BRAIN / f).read_text(encoding="utf-8")
            if testo.count(vecchio) != 1:
                sys.exit(f"{nome}: la sostituzione compare {testo.count(vecchio)} volte")
            (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
        vivo = suite(dest)
        uccisi += not vivo
        print(f"{'VIVO  ' if vivo else 'UCCISO'} {nome}")
        shutil.rmtree(dest)
    print(f"\n{uccisi}/{len(M)} mutanti uccisi")
    return 0 if uccisi == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
