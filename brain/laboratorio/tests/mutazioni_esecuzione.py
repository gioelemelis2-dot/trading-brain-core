"""Mutation testing del pacchetto laboratorio/esecuzione (sigillo, criteri, caricatore, esecutore di H-002).
Ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve superare i test; ogni sostituzione deve
comparire una sola volta. Il generatore di mercati inventati (sintetico.py) è strumento di prova: non si muta.
Uso (dalla radice del repository): python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella> [processi] [prefissi]
  prefissi: per esempio «S,C» per far girare solo i mutanti che iniziano con S o C (utile con poco tempo).
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
SUITE = ["brain.laboratorio.tests.test_esecuzione", "brain.laboratorio.tests.test_esegui_h002",
         "brain.laboratorio.tests.test_riserva", "brain.laboratorio.tests.test_potenza_soglia",
         "brain.laboratorio.tests.test_taratura_completezza"]
SG = "laboratorio/esecuzione/sigillo.py"
K = "laboratorio/esecuzione/criteri.py"
C = "laboratorio/esecuzione/caricatore.py"
E = "laboratorio/esecuzione/esegui_h002.py"
CAL = "dati/pipeline/calendario.py"
RV = "laboratorio/esecuzione/riserva.py"
PS = "laboratorio/studi/potenza_soglia.py"
TA = "laboratorio/studi/taratura_completezza.py"
M = {
    "TA01 taratura: chiusure note contate": [(TA, "if g.weekday() < 5 and g not in chiusure_note(g.year) and f.exists():", "if g.weekday() < 5 and f.exists():")],
    "TA02 taratura: fine settimana contato": [(TA, "if g.weekday() < 5 and g not in chiusure_note(g.year) and f.exists():", "if g not in chiusure_note(g.year) and f.exists():")],
    "TA03 taratura: minuti fuori sessione contati": [(TA, "        if a <= t < b:\n            t3[min(2, int((t - a) / durata))] += 1", "        if True:\n            t3[min(2, abs(int((t - a) / durata)) % 3)] += 1")],
    "TA04 taratura: vigilie mischiate": [(TA, "(vigilie if g in giorni_corti(g.year) else per_giorno).append(voce)", "per_giorno.append(voce)")],
    "TA05 taratura: soglia di sessione ignorata": [(TA, "             if g[\"sessione\"] < min_s or any(t < min_t for t in g[\"terzi\"])]", "             if any(t < min_t for t in g[\"terzi\"])]")],
    "TA07 taratura: record ripetuti contati (#85)": [(TA, "    for t in set(tempi):                                            # #85: minuti distinti\n        if a <= t < b:\n            t3[", "    for t in tempi:\n        if a <= t < b:\n            t3[")],
    "TA06 taratura: percentili non ordinati": [(TA, "    v = sorted(valori)", "    v = list(valori)")],
    'N23 terzi della sessione ignorati': [(C, ' and all(n >= minimo_terzo for n in terzi)', '')],
    'N24 HEAD staccata accettata': [(SG, '    if _git(radice, "symbolic-ref", "-q", "HEAD").returncode != 0:', '    if False:')],
    'N25 ramo senza versione remota accettato': [(SG, '    if remoto.returncode != 0:\n        raise ValueError("il ramo non ha', '    if remoto.returncode != 0:\n        return\n        raise ValueError("il ramo non ha')],
    'N26 storia riscritta accettata': [(SG, '    if _git(radice, "merge-base", "--is-ancestor", remoto, "HEAD").returncode != 0:', '    if False:')],
    'N27 modifiche non committate accettate': [(SG, '    if json.loads(head.stdout) != json.loads(file.read_text(encoding="utf-8")):', '    if False:')],
    'N28 collegamento simbolico accettato': [(SG, '    if file.is_symlink():', '    if False:')],
    "N29 ambiente non controllato all'avvio": [(E, '        if CONTROLLO_AMBIENTE:                                                 # #61: all\'avvio\n            controlla_ambiente(sigillo["codice"])', '        pass')],
    'N30 modalità isolata non richiesta': [(E, '    if isolato_richiesto and not (sys.flags.isolated and sys.flags.no_site):', '    if False:')],
    'N31 libreria standard ombrata accettata': [(E, '        elif any(_dentro(p, s) for s in siti) or not any(_dentro(p, s) for s in standard):', '        elif any(_dentro(p, s) for s in siti):')],
    'N32 modulo brain caricato non confrontato': [(E, '            elif hashlib.sha256(p.read_bytes()).hexdigest() != sigillati[rel]:', '            elif False:')],
    'N33 robustezza del sigillo non controllata': [(E, '        if sorted(sigillo.get("robustezza") or []) != nomi_robustezza():     # #69', '        if False:     # #69')],
    'N34 robustezza non dichiarata accettata': [(SG, ' and (not prove or prova in prove)', '')],
    'N36 completezza per record, non per minuti (#85)': [(C, '    for t in set(tempi):                                            # #85: minuti distinti\n        if a <= t < b:\n            terzi[', '    for t in tempi:\n        if a <= t < b:\n            terzi[')],
    'N47 esito senza verifica accettato (#90)': [(SG, '        if not any(x["ruolo"] == "verifica" for x in stessa):', '        if False:')],
    'N48 secondo esito accettato (#90)': [(SG, '        if any(x["ruolo"] == "esito" for x in stessa):', '        if False:')],
    'N49 testa della riserva non ricontrollata (#93)': [(RV, '        _controlla_testa(self.inizio, self.fine, testa["alfa_tot"], self.protetta)\n', '')],
    'N50 alfa totale booleano accettato (#93)': [(RV, '    if type(alfa_tot) not in (int, float) or not 0.0 < alfa_tot < 1.0:', '    if not 0.0 < alfa_tot < 1.0:')],
    'N51 contatore j non intero accettato (#94)': [(RV, 'if type(e.get("j")) is not int or e.get("j") != self.j + 1:', 'if e.get("j") != self.j + 1:')],
    'N52 verifiche registrate una per volta (#94)': [(SG, '        nuove = [_controlla_e_aggiungi(dati, ipotesi, v, ora) for v in voci]\n        _scrivi(registro, dati)\n', '        nuove = []\n        for v in voci:\n            nuove.append(_controlla_e_aggiungi(dati, ipotesi, v, ora))\n            _scrivi(registro, dati)\n')],
    'N35 ambiente non ricontrollato prima dell\'esito (#91)': [(E, '            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))\n            if CONTROLLO_AMBIENTE:', '            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))\n            if False:')],
    'N37 registro non canonico accettato (#86)': [(E, '            if x.registro.resolve() != (RADICE / REL_REGISTRO).resolve():', '            if False:')],
    'N38 storia git ignorata (#86)': [(E, '            storia = S.versioni_nella_storia(RADICE, REL_REGISTRO)', '            storia = []')],
    'N39 verifica su un altro ramo ignorata (#86)': [(E, '            if altrove:  ', '            if False:  ')],
    'N40 N della sola versione corrente (#86)': [(E, 'n = max([S.n_prove(S.leggi(x.registro))] + [S.n_prove(d) for d in storia])', 'n = S.n_prove(S.leggi(x.registro))')],
    'N41 storia del solo ramo corrente (#86)': [(SG, '_git(radice, "rev-list", "--all", "--", rel)', '_git(radice, "rev-list", "HEAD", "--", rel)')],
    'N42 ambiente non ricontrollato prima degli esiti dello sviluppo (#91)': [(E, '            ris = esegui_sviluppo(bid, ask)\n            if CONTROLLO_AMBIENTE:', '            ris = esegui_sviluppo(bid, ask)\n            if False:')],
    'N43 bytecode in __pycache__ accettato (#87)': [(E, '            elif Path(importlib.util.cache_from_source(str(p))).exists():', '            elif False:')],
    'N44 pycache_prefix accettato (#87)': [(E, '    if getattr(sys, "pycache_prefix", None):', '    if False:')],
    'N45 libreria standard troppo larga (#88)': [(E, '    return Path(sys.modules["encodings"].__file__).resolve().parent.parent', '    return Path("/")')],
    'N46 pacchetti installati come standard (#88)': [(E, '    return bool({"site-packages", "dist-packages"} & set(p.parts)) or not _dentro(p, standard)', '    return not _dentro(p, standard)')],
    'V01 riserva: sovrapposizioni ignorate': [(RV, '        if occupate:\n            raise', '        if False:\n            raise')],
    'V02 riserva: fuori dalla riserva': [(RV, '        if a < self.inizio or b > self.fine:', '        if a < self.inizio:')],
    'V03 riserva: intervallo rovesciato': [(RV, '        if b < a:\n            raise ValueError(f"intervallo rovesciato', '        if False:\n            raise ValueError(f"intervallo rovesciato')],
    'V04 riserva: protetta senza sblocco': [(RV, 'not e.get("usa_protetta"):\n                raise ValueError(f"{a} → {b} tocca', 'False:\n                raise ValueError(f"{a} → {b} tocca')],
    'V05 riserva: identità riusata': [(RV, '            if p is not None:\n                raise ValueError(f"identità', '            if False:\n                raise ValueError(f"identità')],
    "V06 riserva: rilascio dopo l'autorizzazione": [(RV, '            if p["stato"] != "prenotato":\n                raise ValueError(f"rilascio', '            if p["stato"] == "rilasciato":\n                raise ValueError(f"rilascio')],
    'V07 riserva: rilascio non libera': [(RV, '            for g in _giorni(a, b):\n                del self.giorni[g]\n', '')],
    'V08 riserva: autorizzazione dopo il rilascio': [(RV, '            if p["stato"] != "prenotato":\n                raise ValueError(f"autorizzazione', '            if p["stato"] == "autorizzato":\n                raise ValueError(f"autorizzazione')],
    'V09 riserva: j non controllato': [(RV, '            if e.get("j") != self.j + 1:', '            if False:')],
    'V10 riserva: quota non controllata': [(RV, '            if abs(float(e.get("alfa_j", -1)) - quota(self.alfa_tot, self.j + 1, m)) > 1e-15:', '            if False:')],
    'V11 riserva: quota senza m': [(RV, '    return alfa_tot / (j * (j + 1)) / m', '    return alfa_tot / (j * (j + 1))')],
    'V12 riserva: quota 1/j': [(RV, '    return alfa_tot / (j * (j + 1)) / m', '    return alfa_tot / j / m')],
    "V13 riserva: l'autorizzazione non consuma": [(RV, '                self.giorni[g] = "consumato"', '                self.giorni[g] = "prenotato"')],
    'V14 riserva: due esiti': [(RV, '            if p["esito"] is not None:\n                raise ValueError(f"esito', '            if False:\n                raise ValueError(f"esito')],
    'V15 riserva: esito sconosciuto': [(RV, '            if e.get("esito") not in ESITI:', '            if False:')],
    'V16 riserva: evento sconosciuto': [(RV, '        if tipo not in TIPI:', '        if False:')],
    'V17 riserva: ripetizione con byte diversi': [(RV, '            if (a["hash_dati"], a["n_globale"], a["m"]) == (hash_dati, n_globale, m):', '            if True:')],
    'V18 riserva: ripetizione con N diverso': [(RV, '            if (a["hash_dati"], a["n_globale"], a["m"]) == (hash_dati, n_globale, m):', '            if (a["hash_dati"], a["m"]) == (hash_dati, m):')],
    'V19 riserva: senza blocco': [(RV, '    with _bloccato(registro):\n        dati = _leggi(registro)\n        _ricostruisci(dati).applica(evento)', '    if True:\n        dati = _leggi(registro)\n        _ricostruisci(dati).applica(evento)')],
    'V20 riserva: creazione ripetuta': [(RV, '        if Path(registro).exists():', '        if False:')],
    'V21 riserva: α speso diviso per m': [(RV, '            "alfa_speso": sum(a["quota_famiglia"] for a in aperture),', '            "alfa_speso": sum(a["alfa_j"] for a in aperture),')],
    'V22 riserva: quarantena su prenotate': [(RV, '            a, b = self._intervallo(e)\n            if not e.get("motivo"):', '            a, b = _d(e["inizio"]), _d(e["fine"])\n            if not e.get("motivo"):')],
    "V23 riserva: esito prima dell'autorizzazione": [(RV, '            if p["stato"] != "autorizzato":\n                raise ValueError(f"esito', '            if p["stato"] == "rilasciato":\n                raise ValueError(f"esito')],
    'V24 riserva: m zero accettato': [(RV, '        if type(m) is not int or m < 1:\n            raise ValueError(f"m = {m!r}: serve un intero ≥ 1")\n        e = {', '        e = {')],
    'V25 riserva: m booleano nel file': [(RV, '            if type(m) is not int or m < 1:                                    # #65', '            if not isinstance(m, int) or m < 1:                                    # #65')],
    'V26 riserva: N globale non controllato': [(RV, '            if type(n) is not int or n < 1 or n < self.n_max:', '            if False:')],
    'V27 riserva: N globale che scende': [(RV, ' or n < 1 or n < self.n_max:', ' or n < 1:')],
    'V28 riserva: impronta dei dati vuota': [(RV, '            if not isinstance(h, str) or not h:', '            if False:')],
    "V29 riserva: ripetizione dopo l'esito": [(RV, '            if p["esito"] is not None:                                         # #65', '            if False:                                         # #65')],
    'V30 riserva: quarantena sulla protetta': [(RV, 'not e.get("usa_protetta"):\n                raise ValueError(f"quarantena', 'False:\n                raise ValueError(f"quarantena')],
    'V31 riserva: testa cambiata accettata': [(RV, '        if head.get("schema") != remota.get("schema") or head.get("riserva") != remota.get("riserva"):', '        if False:')],
    'V32 riserva: eventi cambiati accettati': [(RV, '        if (head.get("eventi") or [])[:len(vecchi)] != vecchi:', '        if False:')],
    'V33 riserva: ancora non controllata': [(RV, '    ancora_git(registro, radice, continua)', '    return')],
    'P01 potenza: limite senza 1,96': [(PS, 'return Z95 if regola == "limite" else 0.0', 'return 0.0')],
    'P02 potenza: stima con 1,96': [(PS, 'return Z95 if regola == "limite" else 0.0', 'return Z95')],
    'P03 potenza: radice di n mancante': [(PS, '(mu - soglia) * math.sqrt(n) / sigma', '(mu - soglia) * n / sigma')],
    'P04 potenza: sigma degli esiti sbagliata': [(PS, '    return (target + 1.0) * math.sqrt(p * (1.0 - p))', '    return target * math.sqrt(p * (1.0 - p))')],
    'P05 potenza: simulazione con la varianza vera': [(PS, '        passa += media - z * math.sqrt(_varianza_campionaria(vinte, n, target) / n) >= soglia', '        passa += media - z * sigma_esiti(mu, target) / math.sqrt(n) * 0.8 >= soglia')],
    'P06 potenza: senza ricerca del minimo': [(PS, '    while n > 1 and prob_promozione(mu, sigma, n - 1, soglia, regola) >= potenza:\n        n -= 1\n', '    n += 1\n')],
    'P07 potenza: None non restituito': [(PS, '    if mu <= soglia:\n        return None\n', '    if mu < soglia:\n        return None\n')],
    'P08 potenza: regola sconosciuta accettata': [(PS, '        raise ValueError(f"regola {regola!r} non in {REGOLE}")', '        pass')],
    'P14 potenza: regola non controllata con mu sotto soglia (#94)': [(PS, '    _spostamento(regola)                                               # #94: regola controllata sempre\n', '')],
    'P15 potenza: dominio di simula non controllato (#94)': [(PS, '    sigma_esiti(mu, target)                                            # #94: mu in (−1, target)\n', '')],
    'P09 potenza: varianza divisa per n (MPS04 di Gemini)': [(PS, '    return (vinte * (target - media) ** 2 + (n - vinte) * (-1.0 - media) ** 2) / (n - 1)', '    return (vinte * (target - media) ** 2 + (n - vinte) * (-1.0 - media) ** 2) / n')],
    'P10 potenza: media fuori dominio': [(PS, '    if not -1.0 < mu < target:', '    if False:')],
    'P11 potenza: sigma o n fuori dominio': [(PS, '    if sigma <= 0 or n < 1:', '    if False:')],
    'P12 potenza: potenza fuori dominio': [(PS, '    if not 0.0 < potenza < 1.0:', '    if False:')],
    'P13 potenza: simulazione con un trade': [(PS, '    if n < 2:\n        raise ValueError("servono', '    if False:\n        raise ValueError("servono')],
    'N01 __init__ fuori dalle impronte': [(E, '    return {f: hashlib.sha256((radice / f).read_bytes()).hexdigest() for f in moduli_brain(radice)}', '    return {f: hashlib.sha256((radice / f).read_bytes()).hexdigest() for f in moduli_brain(radice) if not f.endswith("__init__.py")}')],
    'N02 import dentro le funzioni ignorati': [(E, '        for nodo in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):', '        for nodo in ast.parse(f.read_text(encoding="utf-8")).body:')],
    'N03 pacchetti attraversati ignorati': [(E, '            if init.is_file():\n                file.add(init)\n                da_fare.append(".".join(parti[:k]))', '            if False:\n                file.add(init)\n                da_fare.append(".".join(parti[:k]))')],
    'N04 import relativi risolti male': [(E, '(nodo.level - 1)', 'nodo.level')],
    'N05 codice non ricalcolato senza impronte date': [(SG, '    if codice is None and s.get("codice"):', '    if False:')],
    'N06 registro su git non confrontato': [(SG, '            if (head.get(chiave) or [])[:len(vecchie)] != vecchie:\n                raise ValueError(f"il registro non continua', '            if False:\n                raise ValueError(f"il registro non continua')],
    'N07 registro non versionato accettato': [(SG, '    if head.returncode != 0:\n        raise', '    if head.returncode != 0:\n        return\n        raise')],
    'N08 registro fuori dal repository accettato': [(SG, '    except ValueError:\n        raise ValueError(f"il file {file} è fuori dal repository', '    except ValueError:\n        return\n        raise ValueError(f"il file {file} è fuori dal repository')],
    'N09 ancora git ignorata': [(E, '        if ANCORA_GIT:\n            S.controlla_ancora(x.registro, RADICE)', '        if False:\n            S.controlla_ancora(x.registro, RADICE)')],
    'N10 --ora non controllata': [(E, '        if not _ORA_ISO.fullmatch(ora):                                       # #51: orario nel formato del registro\n            raise ValueError(f"--ora {ora!r} non è nel formato AAAA-MM-GGThh:mm:ssZ")\n        datetime.strptime(ora, "%Y-%m-%dT%H:%M:%SZ")\n', '')],
    'N11 dati dello sviluppo non ricontrollati': [(E, '            if impronte_sviluppo != {adesso}:', '            if False:')],
    'N12 robustezza senza nome della prova': [(SG, '        valida = base in dichiarate and bool(prova.strip())', '        valida = base in dichiarate')],
    'N13 suffissi liberi nello sviluppo': [(SG, '        valida = variante in dichiarate', '        valida = variante.split(" ")[0] in dichiarate')],
    'N14 completezza non controllata': [(C, '                elif not _completo(', '                elif False and not _completo(')],
    'N15 minuti contati fuori sessione': [(C, '        if a <= t < b:\n            terzi[', '        if True:\n            terzi[')],
    'N16 vigilie non tollerate': [(C, '    if corto:\n        return terzi[0] >= minimo_terzo', '    if corto:\n        return True')],
    'N17 incompleti non bloccano': [(E, ' \\\n                or info["feriali_incompleti_bid"] or info["feriali_incompleti_ask"]:  # P6, R11-S2, #49', ':  # P6, R11-S2, #49')],
    'N18 Natale di domenica senza martedì 27': [(CAL, '        elif nat.weekday() == 6:\n            g.add(nat + timedelta(days=2))', '        elif nat.weekday() == 6:\n            pass')],
    "N19 Lunedì dell'Angelo mancante": [(CAL, 'pasqua(a) + timedelta(days=1)}', 'pasqua(a) - timedelta(days=2)}')],
    'N20 Capodanno di sabato senza il 31': [(CAL, '            g |= {cap - timedelta(days=1), cap + timedelta(days=2)}', '            g |= {cap + timedelta(days=2)}')],
    "N21 solo l'anno stesso": [(CAL, '    for a in (anno - 1, anno, anno + 1):', '    for a in (anno,):')],
    'N22 impronta della cache diversa dal caricatore': [(C, '    for cartella in (cartella_bid, cartella_ask):', '    for cartella in (cartella_ask, cartella_bid):')],
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
    "K12 confronto casuale ignorato": [(K, "casuale.get(\"sopra\", False) and cop_casuale >= copertura_min),", "True),")],
    "K13 benchmark ignorati": [(K, "benchmark.get(\"batte_entrambi\", False) and cop_bench >= copertura_min),", "True),")],
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
    "C02 dati senza sigillo, in sviluppo e in verifica (difetto #41)": [
        (C, "    S.controlla_sigillo(registro, ipotesi, scheda)\n", "")],
    "C03 verifica senza il 31/10 compreso": [(C, "if fine > FINE_VERIFICA:", "if fine >= FINE_VERIFICA:")],
    "C09 embargo aperto (P7 di Gemini)": [(C, "if fine > FINE_VERIFICA:", "if fine >= INIZIO_SVILUPPO:")],
    "C04 high e low scambiati": [(C, "out[t] = (float(o), float(h), float(l), float(c))",
                                  "out[t] = (float(o), float(l), float(h), float(c))")],
    "C05 giorni mancanti non contati": [(C, "            mancanti += 1\n", "            pass\n")],
    "C06 ASK letti dalla cartella BID": [(C, "ask, ma, va, ia = _leggi_cache(cartella_ask,", "ask, ma, va, ia = _leggi_cache(cartella_bid,")],
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
        (E, "sigillo = S.controlla_sigillo(x.registro, IPOTESI, x.scheda, codice=impronte_codice())",
         "sigillo = {\"scheda_sha256\": \"-\", \"varianti\": list(VARIANTI)}")],
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
    "E13 basta una promozione (P1 di Gemini)": [(E, "and all(bool(e.get(\"promossa\")) for e in esiti_sviluppo[v])",
                                                 "and any(bool(e.get(\"promossa\")) for e in esiti_sviluppo[v])")],
    "E14 verifica di una parte delle promosse (P2 di Gemini)": [
        (E, "if sorted(promosse) != sorted(da_verificare):", "if not set(promosse) <= set(da_verificare):")],
    "E15 sigillo con varianti diverse ammesso (P3 di Gemini)": [
        (E, "if sorted(sigillo[\"varianti\"]) != sorted(VARIANTI):", "if False:")],
    "E16 anni del periodo non passati (P4 di Gemini)": [
        (E, "esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))",
         "esegui_verifica(bid, ask, promosse, n, None)")],
    "E17 casuale contro l'R di tutti i trade (P5 di Gemini)": [
        (E, "r_comuni = mean(strategia[d] for d in comuni)", "r_comuni = m[\"r_medio\"]")],
    "E18 dati incompleti ammessi (P6 di Gemini)": [
        (E, "if info[\"giorni_bid_mancanti\"] or info[\"giorni_ask_mancanti\"] or not info[\"minuti_bid\"] \\\n",
         "if not info[\"minuti_bid\"] \\\n")],
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
    "R01 DSR anche con 2 trade (R11-S1 di Gemini)": [(K, "T_MIN_DSR = 30", "T_MIN_DSR = 2")],
    "R02 giorni feriali vuoti ammessi (R11-S2)": [
        (E, "or not info[\"minuti_ask\"] or info[\"feriali_vuoti_bid\"] or info[\"feriali_vuoti_ask\"] \\",
         "or not info[\"minuti_ask\"] \\")],
    "R03 feriali vuoti non contati (R11-S2)": [
        (C, "                if not minuti:\n                    feriali_vuoti.append(giorno.isoformat())",
         "                if False:\n                    feriali_vuoti.append(giorno.isoformat())")],
    "R04 chiusure note ignorate (R11-S2)": [
        (CAL, "    return {d for d in g if d.year == anno}", "    return set()")],
    "R05 rapporto non controllato prima di registrare (R11-S4)": [(E, "if x.rapporto.is_dir():", "if False:")],
    "R06 esito della verifica non registrato (R11-S4)": [
        (E, "for v, r in ris[\"varianti\"].items():                                  # R11-S4: esito nel registro",
         "for v, r in []:                                  # R11-S4: esito nel registro")],
    "R07 copertura del casuale ignorata (R11-S5)": [
        (K, "casuale.get(\"sopra\", False) and cop_casuale >= copertura_min),", "casuale.get(\"sopra\", False)),")],
    "R08 copertura dei benchmark ignorata (R11-S5)": [
        (K, "benchmark.get(\"batte_entrambi\", False) and cop_bench >= copertura_min),",
         "benchmark.get(\"batte_entrambi\", False)),")],
    "R09 cache della verifica diversa da quella dello sviluppo (R11-S6)": [
        (E, "if cache_sviluppo != {str(cache)}:", "if False:")],
    "R10 variante fuori dal sigillo (R11-S7)": [
        (SG, "    if not valida:\n        raise ValueError(f\"variante", "    if False:\n        raise ValueError(f\"variante")],
    "R11 codice non controllato": [(SG, "if codice is not None and s.get(\"codice\") != codice:", "if False:")],
    "R12 ripetizioni e seme non registrati (R11-S3)": [
        (E, "ripetizioni=K.RIPETIZIONI, seme=K.SEME,", "ripetizioni=1, seme=1,")],
    "R13 impronta dei dati vuota (R11-S6)": [
        (C, "    impronta.update(f\"{Path(cartella).name}", "    (lambda *a: None)(f\"{Path(cartella).name}")],
    "MR01 ASK mancanti non controllati (Gemini R11)": [
        (E, "info[\"giorni_bid_mancanti\"] or info[\"giorni_ask_mancanti\"] or not info[\"minuti_bid\"]",
         "info[\"giorni_bid_mancanti\"] or not info[\"minuti_bid\"]")],
    "MR02 zero minuti ASK ammessi (Gemini R11)": [
        (E, "or not info[\"minuti_ask\"] or info[\"feriali_vuoti_bid\"]", "or info[\"feriali_vuoti_bid\"]")],
    "MR03 sviluppo di un'altra ipotesi (Gemini R11)": [
        (E, "if e[\"ipotesi\"] == IPOTESI and e[\"ruolo\"] == \"sviluppo\":", "if e[\"ruolo\"] == \"sviluppo\":")],
    "MR04 verifica di un'altra ipotesi (Gemini R11)": [
        (E, "if e[\"ipotesi\"] == IPOTESI\n                     and e[\"ruolo\"] == \"verifica\"",
         "if True\n                     and e[\"ruolo\"] == \"verifica\"")],
    "MR06 DSR con > (Gemini R11)": [(K, "_ge(dsr, dsr_min)", "dsr is not None and dsr > dsr_min")],
    "MR07 promossa sempre vera nel registro (Gemini R11)": [
        (E, "promossa=r[\"screening\"][\"promossa\"],", "promossa=True,")],
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
        esiti = list(ex.map(lambda a: mutante(*a), [(i, n, s) for i, (n, s) in enumerate(M.items(), 1) if n.startswith(PREFISSI)]))
    for nome, esito in esiti:
        print(f"{esito:6} {nome}")
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]})")
    return 0 if uccisi == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
