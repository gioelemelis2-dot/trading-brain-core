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
         "brain.laboratorio.tests.test_taratura_completezza", "brain.laboratorio.tests.test_intersezione_bid_ask",
         "brain.laboratorio.tests.test_collaudo_ia02", "brain.laboratorio.tests.test_pilota_ia02",
         "brain.laboratorio.tests.test_protocollo_ia02"]
SG = "laboratorio/esecuzione/sigillo.py"
K = "laboratorio/esecuzione/criteri.py"
C = "laboratorio/esecuzione/caricatore.py"
E = "laboratorio/esecuzione/esegui_h002.py"
CAL = "dati/pipeline/calendario.py"
RV = "laboratorio/esecuzione/riserva.py"
AV = "laboratorio/esecuzione/avvio.py"
PS = "laboratorio/studi/potenza_soglia.py"
TA = "laboratorio/studi/taratura_completezza.py"
IX = "laboratorio/studi/intersezione_bid_ask.py"
CO = "laboratorio/studi/collaudo_ia02.py"
PI = "laboratorio/studi/pilota_ia02.py"
PR = "laboratorio/studi/protocollo_ia02.py"
M = {
    "IX19 intersezione: vigilie nei percentili annuali (M-R16-01 di Gemini)": [(IX, '        delle = [s for s in sedute if s["giorno"][:4] == anno]', '        delle = [s for s in sedute + vigilie if s["giorno"][:4] == anno]')],
    "CO12 collaudo: media del bootstrap divisa per n (M-R16-03 di Gemini)": [(CO, '        medie.append(tot / (blocchi * b))', '        medie.append(tot / n)')],
    "PI26 pilota: distorsione senza - μ (M-R16-06 di Gemini)": [(PI, '        c["distorsione"] = (sum(stime) / len(stime) - mu) if stime else None', '        c["distorsione"] = (sum(stime) / len(stime)) if stime else None')],
    "PI21 pilota: ampiezza nulla accettata (#112)": [(PI, '    if not (math.isfinite(lo) and math.isfinite(hi)) or not lo < hi:', '    if not (math.isfinite(lo) and math.isfinite(hi)) or not lo <= hi:')],
    "PI22 pilota: limiti non finiti accettati (#112)": [(PI, '    if not (math.isfinite(lo) and math.isfinite(hi)) or not lo < hi:', '    if not lo < hi:')],
    "PI23 pilota: HAC fuori dal contratto": [(PI, '    return intervallo_valido(mu - Z * se, mu + Z * se)', '    return mu - Z * se, mu + Z * se')],
    "PI24 pilota: limiti grezzi non salvati per l'errore": [(PI, '            out["limiti"][metodo].append(None if iv is None else [iv[0], iv[1]])', '            out["limiti"][metodo].append([0.0, 0.0] if iv is None else [iv[0], iv[1]])')],
    "PI25 pilota: file dei limiti senza versione": [(PI, '            json.dump({"versione": impronta_modulo(), "fase": x.fase,', '            json.dump({"versione": "", "fase": x.fase,')],
    "PR01 protocollo: Clopper–Pearson con la disuguaglianza rovesciata": [(PR, '        if _cdf_binomiale(k, M, mid) > delta:', '        if _cdf_binomiale(k, M, mid) < delta:')],
    "PR02 protocollo: soglia k con un evento in più": [(PR, '    while k + 1 < M and _cdf_binomiale(k + 1, M, TASSO) <= delta:', '    while k < M and _cdf_binomiale(k, M, TASSO) <= delta:')],
    "PR03 protocollo: uguaglianza alla soglia come promozione": [(PR, '        elif iv[0] > alto:', '        elif iv[0] >= alto:')],
    "PR04 protocollo: uguaglianza alla soglia come bocciatura": [(PR, '        elif iv[1] < basso:', '        elif iv[1] <= basso:')],
    "PR05 protocollo: margine non simmetrico": [(PR, '    return round(SOGLIA + margine, 10), round(SOGLIA - margine, 10)', '    return round(SOGLIA + margine, 10), SOGLIA')],
    "PR06 protocollo: errori fuori da k⁺": [(PR, 'per_cella[c] = dict(M=M, **n, kp=n["P"] + n["E"], km=n["B"] + n["E"])', 'per_cella[c] = dict(M=M, **n, kp=n["P"], km=n["B"] + n["E"])')],
    "PR07 protocollo: errori fuori da k⁻": [(PR, 'per_cella[c] = dict(M=M, **n, kp=n["P"] + n["E"], km=n["B"] + n["E"])', 'per_cella[c] = dict(M=M, **n, kp=n["P"] + n["E"], km=n["B"])')],
    "PR08 protocollo: celle sotto soglia non controllate": [(PR, '                for c in CELLE_SOTTO + CELLE_CONFINE:', '                for c in CELLE_CONFINE:')],
    "PR09 protocollo: falsa bocciatura non controllata": [(PR, '                    controlli.append(("falsa bocciatura", c, k, ucp(k, M, delta), k <= kmax))', '                    controlli.append(("falsa bocciatura", c, k, ucp(k, M, delta), True))')],
    "PR10 protocollo: cella 11 senza veto": [(PR, 'CELLE_CONFINE = (2, 6, 9, 11)', 'CELLE_CONFINE = (2, 6, 9)')],
    "PR11 protocollo: potenza non richiesta": [(PR, '            ammissibile = completa and all(x[4] for x in controlli) and all(v >= 1 for v in potenze.values())', '            ammissibile = completa and all(x[4] for x in controlli)')],
    "PR12 protocollo: completezza non controllata": [(PR, '                                        "potenze": potenze, "ammissibile": ammissibile, "kmax": kmax}', '                                        "potenze": potenze, "ammissibile": ammissibile or bool(controlli), "kmax": kmax}')],
    "PR13 protocollo: lunghezza delle liste non controllata": [(PR, '                       and len(celle[str(c)][metodo]) == M\n', '                       and len(celle[str(c)][metodo]) >= 1\n')],
    "PR14 protocollo: intervalli del file non controllati": [(PR, '                       and all(_intervallo_ammesso(iv) for iv in celle[str(c)][metodo]) for c in P.CELLE)', '                       for c in P.CELLE)')],
    "PR15 protocollo: classifica per somma prima del minimo": [(PR, '    ordine = sorted(ammessi, key=lambda kv: (-min(kv[1]["potenze"].values()), -sum(kv[1]["potenze"].values()),', '    ordine = sorted(ammessi, key=lambda kv: (-sum(kv[1]["potenze"].values()), -min(kv[1]["potenze"].values()),')],
    "PR16 protocollo: margine più grande a parità": [(PR, '                                             kv[0][1], P.METODI.index(kv[0][0])))', '                                             -kv[0][1], P.METODI.index(kv[0][0])))')],
    "PR17 protocollo: bootstrap prima di HAC a parità": [(PR, '                                             kv[0][1], P.METODI.index(kv[0][0])))', '                                             kv[0][1], -P.METODI.index(kv[0][0])))')],
    "PR18 protocollo: fase 2 senza 12.000 repliche": [(PR, '        if M != M_FASE2:', '        if M < 1:')],
    "PR19 protocollo: diagnostica ignorata nel verdetto": [(PR, '    if not diagnostica_ok:', '    if False:')],
    "PR20 protocollo: banda dei flussi allargata": [(PR, 'BANDA = (4796, 5204)', 'BANDA = (4790, 5210)')],
    "PR21 protocollo: ritardo non applicato": [(PR, '            x = sum(1 for t in range(1, N_BIT + 1) if a[t] == b[t + h])', '            x = sum(1 for t in range(1, N_BIT + 1) if a[t] == b[t])')],
    "PR22 protocollo: confronti di gruppo B solo in fase 1": [(PR, '        for f in (1, 2):', '        for f in (1, 1):')],
    "PR23 protocollo: semi duplicati non visti": [(PR, '    ok = inv["chiavi"] == inv["semi_distinti"] and not segnalati', '    ok = not segnalati')],
    "PR24 protocollo: fase del file non controllata": [(PR, '    if dati.get("fase") != x.fase:', '    if False:')],
    "PR25 protocollo: p-value senza il fattore 2": [(PR, '    return min(1.0, 2 * min(basso, alto))', '    return min(1.0, min(basso, alto))')],
    "PR26 protocollo: δ della fase 2 come la fase 1": [(PR, 'DELTA = {1: 0.05, 2: 0.001}', 'DELTA = {1: 0.05, 2: 0.05}')],
    "PR27 protocollo: inventario senza la componente": [(PR, '                    semi.add(hashlib.sha256(f"{P.MASTER}:{fase}:{c}:{r}:{g}".encode()).digest())', '                    semi.add(hashlib.sha256(f"{P.MASTER}:{fase}:{c}:{r}".encode()).digest())')],
    "PI01 pilota: componente fuori dal seme": [(PI, 'chiave = f"{master}:{fase}:{cella}:{replica}:{componente}".encode()', 'chiave = f"{master}:{fase}:{cella}:{replica}".encode()')],
    "PI02 pilota: AR(1) che parte da zero": [(PI, '    z = [rnd.gauss(0.0, 1.0)]  ', '    z = [0.0]  ')],
    "PI03 pilota: innovazioni AR(1) non scalate": [(PI, '    s = math.sqrt(1 - RHO * RHO)', '    s = 1.0')],
    "PI04 pilota: probabilità di K = 0 sbagliata": [(PI, '        k = 0 if u < 0.25 else', '        k = 0 if u < 0.30 else')],
    "PI05 pilota: conteggi senza componente comune": [(PI, 'math.sqrt(0.5) * zc[d] + math.sqrt(0.5) * ri.gauss(0.0, 1.0)', 'ri.gauss(0.0, 1.0)')],
    "PI06 pilota: perdite rare col segno invertito": [(PI, '(Q_RARE - (1 if r0.random() < Q_RARE else 0))', '((1 if r0.random() < Q_RARE else 0) - Q_RARE)')],
    "PI07 pilota: HAC senza pesi di Bartlett": [(PI, '        v += 2 * (1 - h / (L + 1)) * sum(', '        v += 2 * sum(')],
    "PI08 pilota: HAC con un ritardo in meno": [(PI, '    for h in range(1, L + 1):', '    for h in range(1, L):')],
    "PI09 pilota: HAC con K medio non al quadrato": [(PI, '    se = math.sqrt(v / (n * kbar * kbar))', '    se = math.sqrt(v / (n * kbar))')],
    # PI10 «pilota: varianza non positiva accettata» DICHIARATO EQUIVALENTE il 18/11: dopo #112, con V = 0 l'intervallo
    # ha ampiezza nulla e intervallo_valido lo rifiuta comunque; V < 0 non si presenta con i pesi di Bartlett. Il
    # controllo resta per evitare la radice di un numero negativo per arrotondamento.
    "PI11 pilota: ritardi predefiniti sbagliati": [(PI, '    return math.floor(4 * (d / 100) ** (2 / 9))', '    return math.floor(3 * (d / 100) ** (2 / 9))')],
    "PI12 pilota: bootstrap non circolare": [(PI, '    estese = coppie + coppie[:blocco - 1]', '    estese = coppie + [(0.0, 0)] * (blocco - 1)')],
    "PI13 pilota: ricampionamento con ΣK = 0 saltato": [(PI, '        if tk == 0:\n            return None\n        medie.append', '        if tk == 0:\n            continue\n        medie.append')],
    "PI14 pilota: rango del quantile spostato": [(PI, '    q = lambda p: o[math.ceil(p * ricampionamenti) - 1]', '    q = lambda p: o[min(len(o) - 1, math.ceil(p * ricampionamenti))]')],
    "PI15 pilota: intervallo percentile al posto del basic": [(PI, '    return intervallo_valido(2 * mu - q(1 - A), 2 * mu - q(A))', '    return intervallo_valido(q(A), q(1 - A))')],
    "PI16 pilota: promozione con limite vicino alla soglia": [(PI, '            c["promosse" if lo > SOGLIA else', '            c["promosse" if lo >= SOGLIA - 0.05 else')],
    "PI17 pilota: copertura solo dal basso": [(PI, '            c["coperture"] += lo <= mu <= hi', '            c["coperture"] += lo <= mu')],
    "PI18 pilota: bootstrap sul flusso dei dati": [(PI, 'intervallo_bootstrap(coppie, flusso(fase, cella, r, 3), ricampionamenti)', 'intervallo_bootstrap(coppie, flusso(fase, cella, r, 0), ricampionamenti)')],
    "PI19 pilota: avviso del pilota ridotto tolto": [(PI, '    if x.fase != 1 or x.repliche < 3000:', '    if False:')],
    "PI20 pilota: z del 95% unilaterale": [(PI, 'Z = NormalDist().inv_cdf(1 - A)', 'Z = NormalDist().inv_cdf(1 - 2 * A)')],
    "CO01 collaudo: F senza il peso (1 - k/n)": [(CO, "    return 1 + 2 * sum((1 - k / n) * rho ** k for k in range(1, n))", "    return 1 + 2 * sum(rho ** k for k in range(1, n))")],
    "CO02 collaudo: AR(1) non stazionario": [(CO, "    e = rnd.gauss(0.0, sigma)\n", "    e = 0.0\n")],
    "CO03 collaudo: innovazioni non scalate": [(CO, "    scala = sigma * math.sqrt(1 - rho * rho)", "    scala = sigma")],
    "CO04 collaudo: ingenuo con varianza su n": [(CO, "    s = math.sqrt(sum((v - m) ** 2 for v in x) / (n - 1))", "    s = math.sqrt(sum((v - m) ** 2 for v in x) / n)")],
    "CO05 collaudo: HAC senza pesi di Bartlett": [(CO, "        var += 2 * (1 - l / (L + 1)) * sum(", "        var += 2 * sum(")],
    "CO06 collaudo: HAC con un ritardo in meno": [(CO, "    for l in range(1, L + 1):", "    for l in range(1, L):")],
    "CO07 collaudo: bootstrap senza blocchi": [(CO, "    b = blocco or blocco_predefinito(n)", "    b = blocco or 1")],
    "CO08 collaudo: quantile del bootstrap spostato": [(CO, "    return medie[max(0, math.ceil(a * ricampionamenti) - 1)]", "    return medie[min(len(medie) - 1, math.ceil(a * ricampionamenti))]")],
    "CO09 collaudo: Clopper–Pearson su una coda intera": [(CO, "    d = (1 - livello) / 2", "    d = 1 - livello")],
    "CO10 collaudo: promozione con limite uguale alla soglia": [(CO, "        promosse += lim > SOGLIA", "        promosse += lim >= SOGLIA - 0.05")],
    "CO11 collaudo: avviso delle poche repliche tolto": [(CO, "    if x.repliche < 1000:", "    if False:")],
    "IX17 intersezione: estremi incrociati non contati (#108)": [(IX, "                if a[2] < b[2] or a[3] < b[3]:", "                if a[2] < b[2]:")],
    "IX18 intersezione: estremi incrociati non sommati per anno (#108)": [(IX, '        a["estremi_incrociati"] += s["estremi_incrociati"]\n', '')],
    "K15a copertura predefinita a 1 (#107)": [(K, 'cop_casuale = casuale.get("copertura", 0.0)', 'cop_casuale = casuale.get("copertura", 1.0)')],
    "K15b percentile fuori dominio accettato (#110)": [(K, "    if not 0.0 < q <= 1.0:                                               # #110\n", "    if False:                                               # #110\n")],
    "K15c anni vuoti accettati (#110)": [(K, "    if anni is not None and not list(anni):", "    if False:")],
    "K15d Sharpe non numerici accettati (#110)": [(K, "    if sharpe_prove is not None and not all(isinstance(x, (int, float)) for x in sharpe_prove):", "    if False:")],
    "IX01 intersezione: ASK sotto BID valido": [(IX, "            if a[0] >= b[0] and a[1] >= b[1]:", "            if True:")],
    "IX02 intersezione: solo la chiusura confrontata": [(IX, "            if a[0] >= b[0] and a[1] >= b[1]:", "            if a[1] >= b[1]:")],
    "IX03 intersezione: buco non azzerato": [(IX, "        buco = 0 if valido else buco + 1", "        buco = buco + (0 if valido else 1)")],
    "IX04 intersezione: buco dai bordi escluso": [(IX, "        buco_max = max(buco_max, buco)\n", "        buco_max = max(buco_max, buco) if valido or k < griglia - 1 else buco_max\n")],
    "IX05 intersezione: solo BID come comune": [(IX, "        elif b is not None:\n            conta[\"solo_bid\"] += 1", "        elif b is not None:\n            conta[\"comuni_validi\"] += 1")],
    "IX06 intersezione: vigilie piene": [(IX, "    griglia = terzo if corta else MINUTI_SESSIONE", "    griglia = MINUTI_SESSIONE")],
    "IX07 intersezione: chiusure note contate": [(IX, "        if g.weekday() < 5 and g not in chiusure_note(g.year):", "        if g.weekday() < 5:")],
    "IX08 intersezione: fine settimana contati": [(IX, "        if g.weekday() < 5 and g not in chiusure_note(g.year):", "        if g not in chiusure_note(g.year):")],
    "IX09 intersezione: file vuoto come mancante": [(IX, '        return "vuoto", {}', '        return "mancante", {}')],
    "IX10 intersezione: file rotto fa crollare": [(IX, "    except DK.ErroreDati:\n        return \"illeggibile\", {}", "    except ZeroDivisionError:\n        return \"illeggibile\", {}")],
    "IX11 intersezione: soglia per terzo ignorata": [(IX, "        if any(t < math.ceil(quota_terzo * (MINUTI_SESSIONE // 3) - 1e-9) for t in s[\"terzi\"]):", "        if False:")],
    "IX12 intersezione: buco massimo ignorato": [(IX, "        if s[\"buco_max\"] > buco_massimo:", "        if False:")],
    "IX13 intersezione: quota della seduta ignorata": [(IX, "        if s[\"comuni_validi\"] < math.ceil(quota_seduta * s[\"griglia\"] - 1e-9):", "        if False:")],
    "IX14 intersezione: prezzi nel rendiconto": [(IX, "    return dict(conta, giorno=giorno.isoformat(), stati=[stato_b, stato_a], griglia=griglia,", "    return dict(conta, prezzi=[str(v) for v in list(bid.values())[:2]], giorno=giorno.isoformat(), stati=[stato_b, stato_a], griglia=griglia,")],
    "IX15 intersezione: ASK mancante non controllato": [(IX, '    if not (x.cache / x.simbolo).is_dir() or not (x.cache / f"{x.simbolo}_ASK").is_dir():', '    if not (x.cache / x.simbolo).is_dir():')],
    "IX16 intersezione: stati non contati per anno": [(IX, '                a[f"{PLURALE[stato]}_{lato}"] += 1', '                pass')],
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
    "N29 ambiente non controllato all'avvio": [(E, '            controlla_ambiente(sigillo["codice"])\n            if not getattr(sys, "_tb_avvio_controllato", False):', '            pass\n            if not getattr(sys, "_tb_avvio_controllato", False):')],
    'N30 modalità isolata non richiesta': [(E, '    if isolato_richiesto and not (sys.flags.isolated and sys.flags.no_site):', '    if False:')],
    'N31 libreria standard ombrata accettata': [(E, '    return bool({"site-packages", "dist-packages"} & set(p.parts)) or not _dentro(p, standard)', '    return bool({"site-packages", "dist-packages"} & set(p.parts))')],
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
    'N53 fuso orario non controllato (#94)': [(E, '        controlla_fuso()                                                       # #94 (d)\n', '')],
    'N54 ultimo giorno d\'estate sbagliato (#94)': [(E, 'if estate[0] <= g < estate[1] else', 'if estate[0] <= g <= estate[1] else')],
    'N55 avvio diretto accettato (#95)': [(E, '            if not getattr(sys, "_tb_avvio_controllato", False):', '            if False:')],
    'N56 lanciatore non sigillato (#95)': [(E, '    file = list(moduli_brain(radice)) + [AVVIO]', '    file = list(moduli_brain(radice))')],
    # N57 «lanciatore: bytecode in brain accettato» DICHIARATO EQUIVALENTE il 17/11: i .pyc dentro __pycache__ sono
    # rifiutati comunque dal controllo dei file compilati (e il loro percorso contiene «__pycache__»). Il controllo
    # della cartella resta per un messaggio più chiaro.
    'N58 lanciatore: cartella di lancio non controllata (#95)': [(AV, '        elif nome.endswith(IMPORTABILI):', '        elif False:')],
    'N59 lanciatore: impronte non controllate (#95)': [(AV, '        if adesso != impronta:', '        if False:')],
    'N60 lanciatore: senza sigillo prosegue (#95)': [(AV, '        return problemi + [f"{REGISTRO}: nessun sigillo di {IPOTESI} con il codice: non si importa nulla"]', '        return problemi')],
    'N61 lanciatore: modalità non isolata accettata (#95)': [(AV, '    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):', '    if not (sys.flags.no_site and sys.flags.dont_write_bytecode):')],
    'N62 lanciatore: cartelle importabili nella radice ammesse (R14-01)': [(AV, '            if nome.isidentifier():', '            if False:')],
    'N63 lanciatore: -B non richiesto (R14-09)': [(AV, 'sys.flags.no_site and sys.flags.dont_write_bytecode)', 'sys.flags.no_site)')],
    'N64 storia parziale accettata (R14-03)': [(SG, '    if _git(radice, "rev-parse", "--is-shallow-repository").stdout.strip() == "true":', '    if False:')],
    'N65 reflog non letto (R14-03)': [(SG, '"rev-list", "--all", "--reflog", "--", rel)', '"rev-list", "--all", "--", rel)')],
    'N66 rapporto della verifica dopo gli esiti (R14-09)': [(E, '            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()\n            x.rapporto.write_text(testo, encoding="utf-8")                     # R14-09: prima degli esiti\n            for v, r in ris["varianti"].items():                                  # R11-S4', '            impronta = hashlib.sha256(testo.encode("utf-8")).hexdigest()\n            for v, r in ris["varianti"].items():                                  # R11-S4')],
    'N67 cartella esterna del bytecode fuori dalla lista (R14-02)': [(E, '        problemi.append("eseguire senza -X pycache_prefix: il bytecode verrebbe letto da un\'altra cartella")', '        raise ValueError("eseguire senza -X pycache_prefix: il bytecode verrebbe letto da un\'altra cartella")')],
    'P16 potenza: sigma non controllata sotto la soglia (R14-06)': [(PS, '    if sigma <= 0:                                                     # R14-06: anche sotto la soglia\n', '    if False:                                                     # R14-06: anche sotto la soglia\n')],
    'N68 lanciatore: archivi nella radice ammessi (M-R14-01 di Gemini)': [(AV, 'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth", ".zip", ".egg", ".whl")', 'IMPORTABILI = (".py", ".pyc", ".pyo", ".so", ".pyd", ".pth")')],
    'N69 lanciatore: cartella esterna del bytecode ammessa (M-R14-02 di Gemini)': [(AV, '    if getattr(sys, "pycache_prefix", None):\n        problemi.append("eseguire senza -X pycache_prefix")', '    if False:\n        problemi.append("eseguire senza -X pycache_prefix")')],
    'N35 ambiente non ricontrollato prima dell\'esito (#91)': [(E, '            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))\n            if CONTROLLO_AMBIENTE:', '            ris = esegui_verifica(bid, ask, promosse, n, range(inizio.year, fine.year + 1))\n            if False:')],
    'N37 registro non canonico accettato (#86)': [(E, '            if x.registro.resolve() != (RADICE / REL_REGISTRO).resolve():', '            if False:')],
    'N38 storia git ignorata (#86)': [(E, '            storia = S.versioni_nella_storia(RADICE, REL_REGISTRO)', '            storia = []')],
    'N39 verifica su un altro ramo ignorata (#86)': [(E, '            if altrove:  ', '            if False:  ')],
    'N40 N della sola versione corrente (#86)': [(E, 'n = max([S.n_prove(S.leggi(x.registro))] + [S.n_prove(d) for d in storia])', 'n = S.n_prove(S.leggi(x.registro))')],
    'N41 storia del solo ramo corrente (#86)': [(SG, '_git(radice, "rev-list", "--all", "--reflog", "--", rel)', '_git(radice, "rev-list", "HEAD", "--", rel)')],
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
    'V09 riserva: j non controllato': [(RV, '            if type(e.get("j")) is not int or e.get("j") != self.j + 1:', '            if False:')],
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
    'N01 __init__ fuori dalle impronte': [(E, '    file = list(moduli_brain(radice)) + [AVVIO]', '    file = [f for f in moduli_brain(radice) if not f.endswith("__init__.py")] + [AVVIO]')],
    'N02 import dentro le funzioni ignorati': [(E, '        for nodo in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):', '        for nodo in ast.parse(f.read_text(encoding="utf-8")).body:')],
    'N03 pacchetti attraversati ignorati': [(E, '            if init.is_file():\n                file.add(init)\n                da_fare.append(".".join(parti[:k]))', '            if False:\n                file.add(init)\n                da_fare.append(".".join(parti[:k]))')],
    'N04 import relativi risolti male': [(E, '(nodo.level - 1)', 'nodo.level')],
    'N05 codice non ricalcolato senza impronte date': [(SG, '    if codice is None and s.get("codice"):', '    if False:')],
    'N06 registro su git non confrontato': [(SG, '            if (head.get(chiave) or [])[:len(vecchie)] != vecchie:\n                raise ValueError(f"il registro non continua', '            if False:\n                raise ValueError(f"il registro non continua')],
    'N07 registro non versionato accettato': [(SG, '    if head.returncode != 0:\n        raise', '    if head.returncode != 0:\n        return\n        raise')],
    'N08 registro fuori dal repository accettato': [(SG, '    except ValueError:\n        raise ValueError(f"il file {file} è fuori dal repository', '    except ValueError:\n        return\n        raise ValueError(f"il file {file} è fuori dal repository')],
    'N09 ancora git ignorata': [(E, '            S.controlla_ancora(x.registro, RADICE)\n', '')],
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
