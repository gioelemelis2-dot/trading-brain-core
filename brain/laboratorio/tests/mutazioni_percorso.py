"""Mutation testing del percorso ordinario di verifica (#127, DGS-15): riserva/2, manifesto, byte nel caricatore,
esecutore ordinario. 22/11/2026.
Stesso meccanismo di mutazioni_esecuzione.py: ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve
superare i test; ogni sostituzione deve comparire una sola volta; una sintassi rotta non conta come ucciso.
Uso (dalla radice del repository): python3 -s -B brain/laboratorio/tests/mutazioni_percorso.py <cartella> [processi] [prefissi]
"""
import os
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
SUITE = ["brain.laboratorio.tests.test_riserva", "brain.laboratorio.tests.test_manifesto",
         "brain.laboratorio.tests.test_esegui_verifica"]
RV = "laboratorio/esecuzione/riserva.py"
MF = "laboratorio/esecuzione/manifesto.py"
C = "laboratorio/esecuzione/caricatore.py"
EV = "laboratorio/esecuzione/esegui_verifica.py"
M = {
    # riserva/2
    "PR01 rifiuto che non libera le date": [(RV, "            for g in _giorni(a, b):\n                del self.giorni[g]\n            p[\"stato\"], p[\"rifiuto\"]", "            p[\"stato\"], p[\"rifiuto\"]")],
    "PR02 rifiuto con j previsto non controllato": [(RV, "e.get(\"j_previsto\") != self.j + 1:", "False:")],
    "PR03 rifiuto con quota calcolata non controllata": [(RV, "abs(qc - quota(self.alfa_tot, self.j + 1, m)) > 1e-15:", "False:")],
    "PR04 rifiuto senza motivo ammesso": [(RV, "for campo in (\"motivo\", \"fase\", \"impronta_scheda\"):", "for campo in (\"fase\", \"impronta_scheda\"):")],
    "PR05 rifiuto dopo l'autorizzazione": [(RV, "                raise ValueError(f\"rifiuto di {id_!r} impossibile: è {p['stato']}\")\n", "                pass\n")],
    "PR06 quota attesa non ricontrollata": [(RV, "if quota_attesa is not None and alfa != quota_attesa:", "if False:")],
    "PR07 impegno non legato all'impronta": [(RV, "impronta_impegno(e[\"impegno\"]) != h)", "False)")],
    "PR08 ripetizione tecnica senza l'impegno": [(RV, "(hash_dati, n_globale, m, impegno)", "(hash_dati, n_globale, m, a.get(\"impegno\"))")],
    "PR09 record incoerente con l'esito": [(RV, "r.get(\"esito\") != e[\"esito\"])", "False)")],
    "PR10 impronta dell'impegno senza ordine delle chiavi": [(RV, "json.dumps(impegno, sort_keys=True,", "json.dumps(impegno, sort_keys=False,")],
    "PR11 vecchio schema accettato": [(RV, 'SCHEMA = "riserva/2"', 'SCHEMA = "riserva/1"')],
    "PR12 due autorizzazioni della stessa domanda": [(RV, "            if gia:                                                            # #139: unicità al consumo", "            if False:")],
    "PR13 unicità senza l'impronta della domanda": [(RV, "                   and q[\"evento\"][\"hash_domanda\"] == p[\"evento\"][\"hash_domanda\"]]", "]")],
    "PR14 unicità solo fra le verifiche senza esito": [(RV, 'if q["stato"] == "autorizzato" and i != id_', 'if q["stato"] == "autorizzato" and q["esito"] is None and i != id_')],
    "PR15 rilascio senza autore né motivo accettato": [(RV, '            if not all(isinstance(e.get(k), str) and e[k].strip() for k in ("chi", "motivo")):   # DGS-19, caso B', '            if False:')],
    "PR16 tentativo anche dopo l'autorizzazione": [(RV, "            if p[\"stato\"] != \"prenotato\":\n                raise ValueError(f\"tentativo di {id_!r} impossibile", "            if False:\n                raise ValueError(f\"tentativo di {id_!r} impossibile")],
    "PR17 ritentativo identico duplicato": [(RV, "                return None\n        e = {\"tipo\": \"tentativo\"", "                pass\n        e = {\"tipo\": \"tentativo\"")],
    "PR18 tentativo senza snapshot dei registri": [(RV, "and isinstance(reg, list) and reg\n", "and isinstance(reg, list)\n")],
    # manifesto
    "MF01 date accessorie ignorate": [(MF, "inizio - timedelta(days=accessorie)", "inizio")],
    "MF02 voce doppia non vista": [(MF, "if len(righe) > 1:", "if False:")],
    "MF03 giorno omesso non visto": [(MF, "        if not righe:\n            anomalie.append", "        if False:\n            anomalie.append")],
    "MF04 riga dell'altro lato accettata": [(MF, "if r.get(\"lato\") != lato:", "if False:")],
    "MF05 indirizzo dell'altro lato accettato": [(MF, "if _lato_dell_indirizzo(url) != lato:", "if False:")],
    "MF06 altro mercato accettato": [(MF, "if f\"/{simbolo}/\" not in url:", "if False:")],
    "MF07 esiti http accettati come dati": [(MF, "if r.get(\"esito\") not in VALIDI:", "if not r.get(\"esito\"):")],
    "MF08 quarantena ignorata": [(MF, "\"quarantena\" if giorno in quarantena else ", "")],
    "MF09 insieme atteso senza ordinamento (atteso EQUIVALENTE: lati e giorni sono già generati in ordine)": [(MF, "return sorted((simbolo, lato, x)", "return list((simbolo, lato, x)")],
    # caricatore
    "CB01 byte non confrontati": [(C, "hashlib.sha256(dati).hexdigest() != atteso:", "False:")],
    "CB02 giorno fuori dal manifesto letto": [(C, "if attese is not None and atteso is None:", "if False:")],
    "CB03 file sparito contato come mancante": [(C, "            if atteso is not None:\n                raise FileDifforme", "            if False:\n                raise FileDifforme")],
    "CB04 lato scambiato nel controllo": [(C, "impronta, \"ASK\", attese)", "impronta, \"BID\", attese)")],
    # esecutore ordinario
    "EV01 contratto senza modello H-003": [(EV, "if c[\"modello\"] != \"H-003\":", "if False:")],
    "EV02 metro non controllato": [(EV, "if c[\"metro\"] != \"D-31\":", "if False:")],
    "EV03 prenotazione di un'altra scheda": [(EV, "or p[\"evento\"][\"hash_domanda\"] != sha_scheda", "")],
    "EV04 ripresa senza controllo d'identità": [(EV, "if p[\"record\"][\"identita\"] != _json(identita):", "if False:")],
    "EV05 sigillo non controllato": [(EV, "    sigillo = S.controlla_sigillo(registro, c[\"ipotesi\"], scheda, codice=identita[\"codice\"])", "    sigillo = {\"varianti\": [c[\"variante\"]]}")],
    "EV17 variante non controllata prima di leggere": [(EV, "if c[\"variante\"] not in sigillo[\"varianti\"]:", "if False:")],
    "EV18 sedute fuori dall'impegno": [(EV, "               \"sedute\": [g.isoformat() for g in giorni_verifica],", "")],
    "EV20 sviluppo letto senza i byte attesi": [(EV, "\"sviluppo\", MF.attese(man_sv))", "\"sviluppo\")")],
    "EV21 manifesto dello sviluppo con anomalie accettato": [(EV, "    if man_sv[\"anomalie\"]:", "    if False:")],
    "EV22 impronta dello sviluppo non confrontata": [(EV, "for chiave in (\"impronta_impegno\", \"impronta_sviluppo\"):", "for chiave in (\"impronta_impegno\",):")],
    "EV23 ancora spenta nel codice": [(EV, "ANCORA_GIT = True              # PIANO-D51", "ANCORA_GIT = False             # PIANO-D51")],
    "EV24 registro della riserva non canonico accettato": [(EV, "        if Path(f).resolve() != (Path(RADICE) / rel).resolve():", "        if False:")],
    "EV25 riserva non ancorata a GitHub": [(EV, "    RV.controlla_ancora(riserva, RADICE)\n", "")],
    "EV26 prenotazione consumata altrove accettata": [(EV, "if q is not None and q[\"stato\"] == \"autorizzato\" and stato_attuale != \"autorizzato\":", "if False:")],
    "EV27 N della sola versione corrente": [(EV, "ctx = dict(ctx, n_prove=max([ctx[\"n_prove\"]] + [S.n_prove(d) for d in storia]))", "pass")],
    "EV28 aperture perse rispetto a un'altra versione": [(EV, "        if s.j > j_attuale:", "        if False:")],
    "EV29 seconda verifica della stessa variante ammessa": [(EV, "    if altre:                                                                            # PIANO-D51 §3.4", "    if False:")],
    "EV30 esecutore senza lanciatore": [(EV, "    if CONTROLLO_AMBIENTE and not getattr(sys, \"_tb_avvio_controllato\", False):", "    if False:")],
    "EV31 ambiente non ricontrollato prima di leggere": [(EV, "        controlla_ambiente(sigillo[\"codice\"])\n", "        pass\n")],
    "EV32 controllo dell'ambiente spento nel codice": [(EV, "CONTROLLO_AMBIENTE = True      # PIANO-D51 §3.3", "CONTROLLO_AMBIENTE = False     # PIANO-D51 §3.3")],
    "EV33 ripresa senza riconciliare il registro delle prove": [(EV, "            _registra_una_volta(registro, c[\"ipotesi\"], voce, ora)\n        _scrivi_rapporto(rapporto, rapporto_da_record(p[\"record\"]))", "            pass\n        _scrivi_rapporto(rapporto, rapporto_da_record(p[\"record\"]))")],
    "EV34 lanciatore fuori dal codice sigillato": [(EV, "    file = list(moduli_brain(radice, PARTENZA)) + [AVVIO]", "    file = list(moduli_brain(radice, PARTENZA))")],
    "EV35 metriche descrittive di H-002 etichettate MISURA (#141)": [(EV, '" [DERIVATO]")             # #141 (b)', '" [MISURA]")             # #141 (b)')],
    "EV36 tentativo rifiutato non registrato": [(EV, '            RV.tentativo(riserva, id_, "manifesto", "; ".join(man["anomalie"][:10]), man["registri"], ora)', '            pass')],
    "EV37 impegno senza i tentativi precedenti": [(EV, '               "tentativi_precedenti": p["tentativi"]}', '               "tentativi_precedenti": []}')],
    "AV01 verifica senza leggere il contratto": [("laboratorio/esecuzione/avvio.py", "        problemi = [problema] if problema else controlla(RADICE, ipotesi, RICHIESTI_VERIFICA)", "        problemi = []")],
    "AV02 codice sigillato di H-002 per ogni verifica": [("laboratorio/esecuzione/avvio.py", "controlla(RADICE, ipotesi, RICHIESTI_VERIFICA)", "controlla(RADICE, IPOTESI, RICHIESTI_VERIFICA)")],
    "AV03 doppia --scheda accettata (#143)": [("laboratorio/esecuzione/avvio.py", "    if len(trovate) != 1:\n", "    if not trovate:\n")],
    "AV04 sigillo senza esegui_verifica.py accettato (#143)": [("laboratorio/esecuzione/avvio.py", "        if mancanti:\n", "        if False:\n")],
    "AV05 forma --scheda=X ignorata (#143)": [("laboratorio/esecuzione/avvio.py", '        if a.startswith("--scheda="):', '        if False:')],
    "AV06 nessuna scheda controllata registrata (#143)": [("laboratorio/esecuzione/avvio.py", "        sys._tb_scheda_controllata = os.path.realpath(scheda_indicata(argv)[0])", "        pass")],
    "EV38 esecutore senza controllo dell'identità della scheda (#143)": [(EV, '    if CONTROLLO_AMBIENTE and getattr(sys, "_tb_scheda_controllata", None) != os.path.realpath(x.scheda):', '    if False:')],
    "EV39 abbreviazioni delle opzioni accettate (#143)": [(EV, "allow_abbrev=False)", "allow_abbrev=True)")],
    "EV19 coppie del record senza le sedute in ordine": [(EV, "for g, (s, k) in zip(giorni_verifica, cp)]", "for g, (s, k) in zip(sorted(giorni_verifica, reverse=True), cp)]")],
    "EV06 sedute non controllate": [(EV, "if len(giorni_verifica) != c[\"sedute\"]:", "if False:")],
    "EV07 quota non controllata prima della lettura": [(EV, "        if q != V.QUOTA:", "        if False:")],
    "EV08 manifesto con anomalie accettato": [(EV, "    if man[\"anomalie\"]:", "    if False:")],
    "EV09 autorizzazione senza quota attesa": [(EV, "impegno=impegno, quota_attesa=q)", "impegno=impegno)")],
    "EV10 lettura senza i byte attesi": [(EV, "\"verifica\", MF.attese(man))", "\"verifica\")")],
    "EV11 date accessorie dentro le coppie": [(EV, "dentro = [x for x in tr if verifica[0] <= x[\"data\"] <= verifica[1]]", "dentro = tr")],
    "EV12 verdetto senza veto per blocchi": [(EV, "v = V.verdetto(cp, c[\"seme\"], [veto], contesto=ctx)", "v = V.verdetto(cp, c[\"seme\"], [], contesto=ctx)")],
    "EV13 esito senza record": [(EV, "RV.rendiconta(riserva, id_, rec[\"esito\"], ora, record=rec)", "RV.rendiconta(riserva, id_, rec[\"esito\"], ora)")],
    "EV14 screening non bloccante": [(EV, "    if not scr[\"ammessa\"]:", "    if False:")],
    "EV15 rifiuto non scritto al ricontrollo": [(EV, "        RV.rifiuta(riserva, id_, c[\"m\"], V.QUOTA, f\"quota {q2!r}", "        (lambda *a: None)(riserva, id_, c[\"m\"], V.QUOTA, f\"quota {q2!r}")],
    "EV16 file difforme non registrato": [(EV, "    except C.FileDifforme as e:", "    except ZeroDivisionError as e:")],
}

def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    """Suite sul mutante, con la RETE BLOCCATA (#66: un mutante che esce in rete deve fallire subito, non scaricare né
    aspettare 20 minuti). Tempo scaduto: contato come ucciso, ma segnalato da guardare."""
    senza_rete = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9",
                      https_proxy="http://127.0.0.1:9", http_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")
    try:
        return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f", *SUITE], cwd=radice,
                              capture_output=True, text=True, timeout=900, env=senza_rete).returncode == 0
    except subprocess.TimeoutExpired:
        print(f"ATTENZIONE: tempo scaduto in {Path(radice).name}: contato come ucciso, da guardare", flush=True)
        return False


def mutante(i, nome, sost):
    dest = OUT / f"M{i:02d}"
    copia(dest)
    for f, vecchio, nuovo in sost:
        testo = (dest / "brain" / f).read_text(encoding="utf-8")
        if testo.count(vecchio) != 1:
            shutil.rmtree(dest)
            return nome, f"ERRORE: la sostituzione compare {testo.count(vecchio)} volte in {f}"
        (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
        try:                                               # #59: una sintassi rotta non è un mutante ucciso
            compile((dest / "brain" / f).read_text(encoding="utf-8"), str(f), "exec")
        except SyntaxError:
            shutil.rmtree(dest)
            return nome, "NON VALIDO: sintassi rotta"
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
        esiti = []
        for nome, esito in ex.map(lambda a: mutante(*a), [(i, n, s) for i, (n, s) in enumerate(M.items(), 1) if n.startswith(PREFISSI)]):
            esiti.append((nome, esito))                    # R17: ogni esito si stampa appena è pronto
            print(f"{esito:6} {nome}", flush=True)
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    equivalenti = [n for n, e in esiti if e == "VIVO" and "atteso EQUIVALENTE" in n]   # dichiarati, non nascosti
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]}); "
          f"equivalenti dichiarati vivi: {len(equivalenti)}")
    return 0 if uccisi + len(equivalenti) == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
