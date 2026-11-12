# REVISIONE ESTERNA DEL PACCHETTO TRADING BRAIN
**Data:** 12 novembre 2026  
**Revisore:** ChatGPT  
**Perimetro:** pacchetto `REVISIONE_ESTERNA_TRADING_BRAIN.zip`, `ISTRUZIONI_PER_REVISORE_ESTERNO.md`, `DECISIONI-APERTE.md`  
**Natura:** revisione documentale, controlli matematici indipendenti, ispezione statica e prove mirate sul codice incluso. Non è una certificazione del sistema né una validazione di strategie redditizie.

---

## 1. Sintesi

1. Il pacchetto è integro: tutti i 26 file elencati nel manifest interno corrispondono agli SHA-256 dichiarati.
2. Le principali correzioni bibliografiche di Claude e Gemini sono fondate, ma le schede STR-001 e soprattutto STR-002 continuano a usare alcune fonti oltre ciò che esse dimostrano.
3. I numeri 594 e 1.417 trade sono riproducibili come approssimazioni normali sotto ipotesi molto restrittive; non sono soglie universali né una durata obbligatoria del paper trading.
4. La somma dei rischi nominali a stop è uno stress conservativo utile, ma chiamarla «comonotonicità» non è una giustificazione matematica sufficiente.
5. Un rischio allo stop è deterministico soltanto condizionatamente alle regole e all'esecuzione ipotizzata; la formula universale proposta da Gemini è ancora incompleta per strumenti e broker diversi.
6. Il protocollo delle stime sigillate richiede un nonce casuale segreto; l'hash non è una firma e non crea da solo indipendenza tra modelli.
7. Il modello epistemico a più assi è una buona direzione, ma la sua integrazione con `STANDARD.md` non è ancora specificata abbastanza da essere implementabile senza ambiguità.
8. Ho trovato nel codice V3.3 almeno un comportamento da correggere: l'intervallo Wilson con zero osservazioni restituisce `(0, 0)`, risultato fuorviante.
9. Non sono presenti nel pacchetto la suite completa dei test, lo script di mutazione, i dati reali o il repository Git: alcune dichiarazioni di Gemini e Claude non sono quindi riproducibili da questo pacchetto.
10. Le decisioni aperte sono utili, ma alcune opzioni si sovrappongono a decisioni già prese e devono essere riformulate senza riaprire i vincoli dell'utente.

## 2. Integrità e perimetro della verifica

### Integrità

- Ho verificato i 26 hash elencati in `MANIFEST_PACCHETTO.sha256`: **26/26 corrispondenti**.
- Lo ZIP ricevuto ha SHA-256 `00a7c30515d4e5fa409aef5458ebc5dffcdc890b308327af6b465b6a4dfccf1e`.
- Il manifest interno verifica i file estratti, non autentica da solo l'autore, la data di creazione o la provenienza del pacchetto.
- Il pacchetto contiene i documenti di Gemini e Claude, il codice `prop_risk_engine_v3_3.py`, `STANDARD.md`, `rulebook.yaml`, le due schede STR e l'estratto del Manuale v1.

### Materiali mancanti che limitano la verifica

Non sono inclusi:
- la suite completa di test V3.3 e i relativi output;
- lo script di mutation testing citato nei rapporti;
- i dati e i file necessari a riprodurre integralmente le simulazioni;
- il repository Git, il suo stato, i branch e la cronologia;
- il testo autentico della Master Mission §§0–25;
- il rapporto strategico V1 di Gemini richiamato nel changelog;
- l'intera bibliografia primaria delle 28 discipline.

Di conseguenza, non certifico le dichiarazioni «20/20 test», «21 mutanti uccisi», «18/18 manifest» o l'intera storia dei branch: posso constatare che sono riportate nei documenti, non riprodurle tutte con i materiali qui consegnati.

---

## 3. Tabella dei rilievi

| ID | Documento / punto | Affermazione esaminata | Verifica eseguita | Esito | Gravità |
|---|---|---|---|---|---|
| R-01 | Manifest del pacchetto | I file consegnati corrispondono agli hash dichiarati | Ricalcolo SHA-256 di tutti i 26 file elencati | **Corretta** | Bassa |
| R-02 | `potenza_campione.py` | 594 trade per potenza 80%, test unilaterale α=5% | Ricalcolo indipendente della media, deviazione standard e formula normale | **Corretta con limiti** | Alta |
| R-03 | `potenza_campione.py`; Gemini F.1 | 1.417 trade con soglia t>3 | Riprodotta l'approssimazione normale `((3 + z80)σ/μ)^2` | **Corretta con limiti** | Alta |
| R-04 | Gemini E.1; Convergenze §2 | Il worst case di portafoglio è «comonotonicità: tutti gli stop insieme» | Distinzione tra stress scenario, dipendenza statistica e limiti effettivi delle perdite | **Parzialmente corretta** | Alta |
| R-05 | Gemini E.2–E.3 | Perdita a stop deterministica sotto `H_esec`; formula generale | Ispezione formula e confronto con specifiche contrattuali necessarie | **Parzialmente corretta** | Alta |
| R-06 | Fonti Lo, Repin, Steenbarger | Il lavoro del 2005 è AER e usa questionari; quello fisiologico è Lo–Repin 2002 | Consultazione AEA, NBER e articolo 2002 | **Corretta** | Media |
| R-07 | Almgren–Chriss | DOI corretto `10.21314/JOR.2001.041` | Verifica pagina dell'editore/Risk.net e DOI | **Corretta** | Media |
| R-08 | STR-002; Lou, Polk, Skouras | Il paper sostiene la spiegazione proposta per i gap ES M5 | Controllo titolo, abstract e perimetro del paper | **Errata per eccesso di attribuzione** | Alta |
| R-09 | STR-002; Branch e Ma | La fonte è «Opening Gap» e dimostra che la chiusura del gap cala con la sua ampiezza | Controllo titolo e abstract disponibili | **Errata / non supportata** | Alta |
| R-10 | Bouchaud, Farmer, Lillo | Sede editoriale citata in modo discordante | Verifica pagina dell'editore | **Discordanza risolta** | Media |
| R-11 | Pine Script | V5 è ancora il riferimento corrente | Verifica annuncio ufficiale e release notes TradingView | **Superata, non falsa storicamente** | Bassa |
| R-12 | Gemini A.1; `STANDARD.md` | I cinque assi sono già armonizzati con lo standard | Confronto delle tassonomie e dei campi richiesti | **Parzialmente corretta** | Alta |
| R-13 | Gemini D.2; DA-07 | Hash SHA-256 basta per sigillare una stima breve | Analisi del commitment e attacco a bassa entropia | **Errata senza nonce casuale segreto** | Alta |
| R-14 | Gemini Area C | Dati successivi al cutoff e alla preregistrazione sono OOS pulito | Valutazione delle fonti di contaminazione e dei limiti del cutoff | **Parzialmente corretta** | Alta |
| R-15 | Gemini E.4; DA-12 | Se il pattern comportamentale correla con perdite, è confermato | Analisi osservazionale, confondenti e test multipli | **Errata come criterio di conferma** | Alta |
| R-16 | `prop_risk_engine_v3_3.py`, righe 39–56 | Wilson con n=0 | Esecuzione diretta della funzione | **Errata** | Alta |
| R-17 | `prop_risk_engine_v3_3.py`, righe 59–100 | Funzione Kelly calcola Kelly | Ispezione della funzione e test mirato | **Errata nel nome; calcola un IC dell'aspettativa** | Media |
| R-18 | STR-001 e STR-002 | Le metriche attese e le soglie sono sostenute dalle fonti citate | Confronto tra regole, fonti e costi dichiarati | **Non dimostrata / parzialmente contraddittoria** | Alta |
| R-19 | `DECISIONI-APERTE.md` | Il registro contiene tutte le decisioni ancora aperte senza riaprire quelle già prese | Confronto con i vincoli riportati nel contesto e con i file effettivamente allegati | **Parzialmente corretta** | Alta |
| R-20 | V3.3 e audit precedenti | La revisione esterna può confermare tutti i test e i mutanti | Verifica dei file effettivamente inclusi | **Non verificabile integralmente** | Alta |

---

## 4. Verifiche matematiche

### 4.1 Potenza: 594 trade

Con le ipotesi dichiarate:
- probabilità di vincita `p = 0,40`;
- vincita `+2R`, perdita `−1R`;
- costo fisso `0,05R` per trade;
- trade indipendenti e identicamente distribuiti;
- edge vero assunto pari a `0,15R`;
- test unilaterale con `α = 0,05`;
- potenza desiderata `0,80`.

I payoff netti diventano:
- vincita: `+1,95R`;
- perdita: `−1,05R`.

Quindi:
- `E[R] = 0,40 × 1,95 − 0,60 × 1,05 = 0,15R`;
- `σ = (2 + 1) × √(0,40 × 0,60) = 1,4697R`.

L'approssimazione normale fornisce:

`N = ((z(0,95) + z(0,80)) × σ / 0,15)² ≈ 594`.

Il codice di Claude riproduce il risultato. **Il numero è corretto come approssimazione condizionata alle ipotesi dichiarate.**

Non è però il numero «necessario» per ogni strategia:
- se l'edge vero è più piccolo, N cresce molto;
- se i trade sono serialmente dipendenti, l'ipotesi i.i.d. non vale;
- se payoff, costi e slippage variano, la varianza va stimata diversamente;
- se la strategia viene selezionata dopo molte prove, serve considerare la selezione e il numero di tentativi;
- il calcolo non misura la qualità dei fill, la stabilità per regime o la correttezza operativa.

Come controllo aggiuntivo, un test binomiale esatto unilaterale sul modello a due soli payoff, con `p0 = 0,35` e `p1 = 0,40`, raggiunge circa l'80% di potenza intorno a 584 osservazioni. La differenza rispetto a 594 è compatibile con l'approssimazione normale e la discrezione del test. Non rende 584 una nuova soglia universale.

**Conclusione:** 594 è una pianificazione di potenza per un modello specifico, non una durata automatica del paper trading.

### 4.2 Soglia t > 3 e 1.417 trade

Il codice calcola:

`N = ((3 + z(0,80)) × σ / 0,15)² ≈ 1.417`.

L'aritmetica è riproducibile come approssimazione normale. Ma Harvey, Liu e Zhu discutono soglie più severe per la scoperta di nuovi fattori nella letteratura empirica di asset pricing, in risposta al multiple testing. Non stabiliscono che ogni strategia intraday, swing, ogni mercato o ogni paper trading debba superare universalmente `t > 3`.

Il valore deve essere inserito in una procedura più completa:
- conteggio dei tentativi effettivamente eseguiti;
- DSR o altra correzione coerente con il processo di selezione;
- potenza e dimensione dell'effetto;
- dipendenza temporale;
- costi e stabilità per regime;
- validazione prospettica.

**Conclusione:** non adottare `1.417` come soglia fissa del progetto. Conservare il calcolo come esempio condizionale.

### 4.3 Rischio di portafoglio: rho=1 e tutti gli stop

Claude e Gemini correggono giustamente l'uso di `ρ = 1` come sinonimo di scenario peggiore. La correlazione tra rendimenti degli strumenti non coincide automaticamente con la correlazione dei P&L delle posizioni: direzione long/short, valuta, contratto e sensibilità cambiano il segno dell'esposizione.

Tuttavia, la nuova formulazione di Gemini («comonotonicità = tutti gli stop colpiti insieme») va precisata.

La somma:

`L_stress = Σ L_i`

è uno **scenario di stress conservativo** nel quale ogni posizione raggiunge il proprio livello di stop e viene eseguita alle condizioni assunte. Non è necessario chiamarlo comonotonicità. La comonotonicità è una proprietà della struttura di dipendenza delle variabili aleatorie, non semplicemente il nome di uno scenario scelto dal progettista.

Inoltre la somma è un limite superiore valido solo se ogni `L_i` è un limite effettivo e finito della perdita della posizione. Se gap, slippage, sospensioni, liquidità insufficiente o strumenti con perdita non limitata possono superare lo stop, la perdita reale può eccedere la somma dei rischi nominali.

**Formulazione consigliata:** «Scenario conservativo di stress: tutte le posizioni raggiungono gli stop e vengono eseguite secondo un'ipotesi esplicita di fill. Il rischio nominale aggregato è la somma delle perdite stimate a stop; va affiancato da scenari separati di gap, slippage e mancata esecuzione».

---

## 5. Fonti bibliografiche

### 5.1 Lo, Repin e Steenbarger (2005)

Confermo la correzione: *Fear and Greed in Financial Markets: A Clinical Study of Day-Traders* è in **American Economic Review**, 95(2), 352–359, DOI `10.1257/000282805774670095`. Lo studio usa questionari quotidiani sullo stato emotivo e inventari di personalità su un campione di 80 day trader.

Le misure fisiologiche (conduttanza cutanea, battito e altre variabili) appartengono invece a Lo e Repin, **2002**, *The Psychophysiology of Real-Time Financial Risk Processing*, *Journal of Cognitive Neuroscience*, 14(3), 323–339, DOI `10.1162/089892902317361877`.

Quindi la confusione di Gemini tra i due lavori è materiale, non una semplice differenza di formattazione.

### 5.2 Almgren e Chriss

Il DOI `10.21314/JOR.2001.041` è quello associato a *Optimal Execution of Portfolio Transactions*. La correzione di Claude e Gemini è fondata.

### 5.3 Lou, Polk e Skouras (2019)

Il titolo è *A Tug of War: Overnight versus Intraday Expected Returns*, *Journal of Financial Economics*, 134(1), 192–213, DOI `10.1016/j.jfineco.2019.03.011`. Il terzo autore è **Spyros Skouras**, non «Skona».

Il lavoro studia la persistenza e la componente overnight/intraday dei rendimenti di titoli e strategie. Non dimostra direttamente che:
- i piccoli gap del future ES siano squilibri temporanei di inventario;
- i market maker istituzionali li riassorbano verso il VWAP precedente;
- i gap grandi siano causati da rivalutazioni macro e continuino nella stessa sessione.

La citazione è pertinente al tema overnight/intraday in senso ampio, ma non sostiene da sola il meccanismo specifico STR-002.

### 5.4 Branch e Ma (2012)

Il titolo riscontrato è *Overnight Return, the Invisible Hand behind Intraday Returns?*, pubblicato nel *Journal of Applied Finance*, 22(2), 2012. Non è il titolo «Overnight Return, the Opening Gap, and the Day Return» né il *Journal of Financial and Quantitative Analysis* riportato nella scheda STR-002.

L'abstract disponibile riferisce una forte autocorrelazione negativa tra rendimenti overnight e intraday. Non basta a sostenere la specifica affermazione che la probabilità di chiusura del gap decresca drasticamente con l'ampiezza normalizzata per volatilità.

### 5.5 Bouchaud, Farmer e Lillo

La sede editoriale corretta riscontrata è il capitolo *How Markets Slowly Digest Changes in Supply and Demand*, in *Handbook of Financial Markets: Dynamics and Evolution*, 2009, pp. 57–160, DOI `10.1016/B978-012374258-2.50006-3`. La citazione in «Quantitative Finance» va corretta; la voce del capitolo nel Handbook è quella supportata dalla pagina dell'editore.

### 5.6 Pine Script

TradingView ha annunciato Pine Script v6 il 10 dicembre 2024 e le note ufficiali indicano che gli aggiornamenti futuri vengono applicati alla v6. La documentazione v5 non è falsa o inutilizzabile per gli script v5 esistenti: è semplicemente superata come riferimento per lo sviluppo nuovo.

---

## 6. Errori condivisi o non risolti dai due modelli

### 6.1 «Tutti gli stop insieme» non equivale a comonotonicità

La correzione di `ρ=1` è giusta, ma l'etichetta comonotonicità rischia di sostituire un errore con un altro. Va descritto come stress scenario. La fattibilità simultanea degli stop, i gap e le esecuzioni devono essere modellati separatamente.

### 6.2 La formula G0 non può essere universale

La formula proposta da Gemini include differenza di prezzo, moltiplicatore, lotti, conversione FX e commissioni. È un miglioramento, ma occorre un adattatore per tipo di strumento e specifiche del broker/exchange:
- Forex: unità del contratto, valuta base/quotata, lato bid/ask, conversione della valuta di P&L nella valuta conto;
- futures: numero contratti, tick size, tick value, moltiplicatore e valuta del contratto;
- CFD: dimensione del contratto e metodo di quotazione del broker;
- costi: spread, commissioni, swap/finanziamento e conversioni;
- ordini stop: prezzo di trigger, prezzo di esecuzione e regole specifiche della piattaforma.

Il tasso FX di conversione non è sempre una misura indipendente: dipende dalla valuta di P&L e dal momento di conversione. Se la valuta quotata coincide con la valuta conto, il fattore è 1. La formula va quindi specificata per strumento, non generalizzata con un unico campo `ContractSize`.

### 6.3 L'epistemologia a cinque assi è una proposta, non uno schema pronto

La struttura a più assi è migliore del singolo ordinamento. Ma `STANDARD.md` contiene già:
- gerarchia delle fonti F1–F7;
- livelli di evidenza E1–E7;
- stati di verifica V/V-sec/C/X;
- classi di contenuto `[VERIFICATO]`, `[IN VERIFICA]`, `[IPOTESI]`, `[ESERCIZIO]`, `[SIMULATO]`, `[REALE]`;
- ciclo di vita della lezione;
- livelli di padronanza L1–L5.

La controverifica dichiara che tutto è armonizzato, ma non fornisce una matrice di mapping completa né un modello dati. Restano da definire:
- qualità della misura e qualità del dato grezzo;
- fonte, timestamp, unità, precisione/errore;
- natura dell'operazione e tipo epistemico del risultato;
- condizioni H ereditate;
- incertezza numerica e sua propagazione;
- stato di verifica e stato di validazione;
- classe di contenuto di `STANDARD.md`;
- provenienza/versione e ciclo di vita.

La regola dell'utente sulla propagazione del tipo più debole va mantenuta. Una stima calcolata da ipotesi non diventa una misura; un risultato deterministico resta condizionato alle ipotesi dei suoi input.

### 6.4 Le stime sigillate

Un hash di un valore breve senza sale è vulnerabile a enumerazione: chi vede l'hash può provare tutte le risposte plausibili.

Un commitment minimo dovrebbe essere calcolato, ad esempio, come:

`SHA256(nonce_casuale_segreto_256_bit || payload_canonicalizzato)`

Il nonce si rivela solo all'apertura. Inoltre:
- l'hash non è una firma digitale;
- non prova chi ha creato il commitment;
- non prova quando è stato creato se manca un timestamp affidabile;
- non impedisce che il modello abbia già visto la risposta dell'altro;
- non elimina conoscenze condivise o contaminazione da fonti esterne.

Serve un registro append-only con timestamp e identità/autenticazione, più separazione degli accessi fino alla doppia registrazione. Il protocollo riduce il condizionamento reciproco, non rende i modelli epistemicamente indipendenti.

### 6.5 Contaminazione LLM: il cutoff non crea un OOS automaticamente pulito

È corretto distinguere storico esplorativo, validazione storica e validazione prospettica. Ma non basta registrare un cutoff dichiarato:
- i cutoff dei fornitori possono essere approssimativi o non granulari;
- il modello può usare web, file o strumenti aggiornati;
- il prompt può contenere dati recenti;
- l'utente e gli analisti possono conoscere già l'esito del periodo;
- l'ipotesi può essere stata raffinata dopo aver visto il periodo.

Un periodo successivo al cutoff dichiarato non è automaticamente incontaminato. La prova prospettica più forte richiede ipotesi congelata, dati futuri non ancora osservati al momento della formulazione, accessi registrati e nessuna modifica opportunistica. Lo storico rimane utile per esplorazione, robustezza e falsificazione, ma non va etichettato come prova prospettica pulita.

### 6.6 Gli indicatori comportamentali non si «confermano» con una correlazione

Un indicatore R1 può essere misurato e preregistrato. Se correla con perdite, non è automaticamente dimostrato che rappresenti revenge trading o causi perdite:
- regime di mercato, volatilità, orario e qualità del setup possono confondere la relazione;
- più indicatori e soglie aumentano il rischio di falsi positivi;
- i dati di una persona possono essere pochi e dipendenti nel tempo;
- soglie scelte dopo aver visto i dati sono soggette a overfitting.

La soglia 60–90 secondi e la pausa 10–15 minuti sono presenti nell'estratto del Manuale v1 dell'utente: possono essere trattate come regole personali di partenza, non come soglie scientifiche universali. La soglia 180 secondi e «size raddoppiata» non risulta giustificata dall'estratto.

### 6.7 La strategia STR-002 ha un problema di supporto empirico

La scheda STR-002 presenta come fondamento:
- piccoli gap = squilibrio temporaneo di inventario e ritorno al VWAP;
- grandi gap = rivalutazione macro e continuazione;
- una relazione tra ampiezza del gap e probabilità di chiusura.

Le fonti citate non dimostrano direttamente queste proposizioni per ES, per le soglie 0,35/0,80 ATR o per il trigger M5/M15. Sono ipotesi testabili, non fatti documentati. Le metriche attese (65% e 42% WR, expectancy e profit factor) non sono risultati empirici nel pacchetto.

Inoltre la scheda stima costi per circa `0,15R` per trade. Il ramo Fade con WR 65% e reward/risk 0,8 produce circa `+0,17R` lordo; dopo `0,15R` di costo resterebbe circa `+0,02R`, prima di altre differenze di esecuzione. La stima netta dichiarata `+0,18R` non è riconciliata con questi numeri. Il ramo Continuation va ricalcolato con una definizione non ambigua di R:R e costi effettivi.

### 6.8 STR-001 non è validata dai paper sul trend following

La letteratura sul time-series momentum/trend following sostiene una famiglia di fenomeni su futures e orizzonti specifici; non valida automaticamente questa combinazione di SMA200, momentum 60 giorni, Donchian 20, ATR 2,5, Donchian 10, SMA50 e filtro VIX<12.

Il filtro VIX<12 persistente, le soglie, i costi, il periodo di detenzione e le metriche obiettivo devono restare ipotesi progettuali fino a backtest riproducibile e validazione fuori campione appropriata. La scheda chiama OOS periodi storici anteriori alla preregistrazione del 2026: possono essere test storici non visti dal ricercatore umano in un determinato workflow, ma non sono forward validation rispetto alla data di preregistrazione e possono essere contaminati dalla conoscenza del modello.

---

## 7. Controlli mirati sul codice V3.3

### 7.1 Errore: Wilson con zero osservazioni

La funzione `wilson_confidence_interval(k, n)` restituisce `(0.0, 0.0)` quando `n == 0`.

Ho eseguito direttamente:

`wilson_confidence_interval(0, 0) -> (0.0, 0.0)`

Questo non è un intervallo valido: con zero osservazioni la proporzione non è stimabile. Il risultato può essere letto come certezza che la probabilità sia zero. La funzione dovrebbe rifiutare `n=0` oppure restituire uno stato esplicito non stimabile, secondo l'interfaccia scelta. È un caso da aggiungere ai test.

### 7.2 Nome fuorviante: `calculate_kelly_confidence_interval`

La funzione non calcola una frazione di Kelly. Calcola:
- expectancy `E[R]`;
- errore standard;
- intervallo normale per `E[R]`.

Il nome `calculate_kelly_confidence_interval` è fuorviante e va rinominato o documentato chiaramente con compatibilità esplicita. Il suo intervallo è una costruzione Wald basata su WR e payoff fisso: non è una stima generale della distribuzione dei rendimenti e non incorpora automaticamente serial correlation, payoff variabili, slippage variabile o incertezza sui costi.

### 7.3 Test non riproducibili dal pacchetto

Il codice si importa e le funzioni mirate possono essere eseguite, ma non sono stati consegnati i test completi. Non posso quindi certificare la copertura dichiarata né la corrispondenza tra mutanti e test.

---

## 8. Decisioni aperte: osservazioni senza decidere al posto dell'utente

1. **Fonte di verità e repository (DA-01):** decisione realmente bloccante. Prima di scegliere A/B serve un test concreto di scrittura e lettura da parte di entrambi gli ambienti, verifica dei permessi e controllo del remote. Il pacchetto non dimostra direttamente lo stato Git dichiarato.
2. **Master Mission (DA-02):** il testo originale è assente dai materiali allegati. La nuova carta fondativa, se autorizzata, deve avere nome e numerazione nuovi; non va presentata come ricostruzione dell'originale.
3. **T-01…T-05 e codice futuro (DA-03 / DA-11):** non va riaperta la decisione dell'utente di congelare V3.3. Resta da chiarire l'ambito della frase «requisiti d'ingresso della successiva fase tecnica»: se significa qualsiasi nuovo codice, il G0 software non può precedere T-01…T-05; se significa solo riuso/modifica del simulatore, alcune attività di governance o dati potrebbero procedere. La scelta va esplicitata prima di autorizzare codice.
4. **G0 anticipato (DA-11):** è consultivo, ma non a rischio nullo. Un calcolo errato o una regola prop firm non aggiornata possono indurre l'utente a dimensionare male. Servono validazione con estratti conto reali, specifiche broker e test di riconciliazione prima dell'uso decisionale.
5. **Indicatori comportamentali (DA-12):** mantenere separati misura osservata, ipotesi di pattern e decisione dell'utente. Le soglie vanno fissate prima della raccolta e non dichiarate universali.
6. **Rulebook Q-09 (DA-13):** distinguere regole contrattuali della prop firm da regole personali. Le regole ufficiali richiedono fonte ufficiale, data e versione.
7. **Regola Pine (DA-14):** è una proposta di governance che limita l'uso dei segnali dell'utente; richiede approvazione esplicita, non è già una decisione.
8. **Dati e budget (DA-15):** il perimetro non può essere ristretto arbitrariamente a S&P 500 ed EUR/USD: STR-001 è multi-asset, STR-002 è ES. Il dataset deve essere deciso strategia per strategia, con licenze e costi verificati.
9. **Journal e previsioni (DA-16):** la raccolta precoce è utile perché il tempo non è recuperabile, ma i dati psicofisici sono personali. Minimizzazione, conservazione locale e consenso sono requisiti.
10. **Contaminazione e STR (DA-17):** la revisione delle schede storiche è utile; non trasformare però il cutoff del modello in garanzia di pulizia. La validazione prospettica va progettata per ipotesi.
11. **Correzioni documentali (DA-18):** non applicare automaticamente correzioni a file originali senza autorizzazione, soprattutto se la regola del progetto richiede approvazione umana.

### Decisioni mancanti o da rendere esplicite

- Come vengono conteggiati i tentativi di ricerca: includere tutte le varianti effettivamente eseguite e registrate, non pensieri non osservabili o non formalizzati.
- Quale criterio promuove una strategia da ricerca a candidata forward: DSR, trial count, potenza, robustezza, costi e criteri di falsificazione devono essere definiti insieme; `t>3` non va imposto come regola universale.
- Come vengono gestiti i dati point-in-time e le revisioni macroeconomiche, i contratti continui e i roll, i cambi di sessione e il daylight saving.
- Quali sono i limiti di accesso ai dati e ai registri dei due modelli, per evitare che un centro legga il registro dell'altro prima del commitment.
- Quale procedura approva modifiche a una regola personale a mercato chiuso e quale periodo di attesa si applica.

---

## 9. Limiti della revisione

- Ho verificato le pagine ufficiali/editoriali e gli abstract delle fonti elencate, ma non ho letto integralmente tutti i paper a pagamento. La pertinenza delle fonti è quindi valutata in base alle informazioni editoriali e agli abstract accessibili.
- Non ho verificato ogni voce delle bibliografie delle 28 discipline.
- Non ho dati di mercato né esportazioni reali del conto: non posso validare expectancy, slippage, drawdown, correlazioni o regole prop firm applicate al conto specifico.
- Non ho accesso al repository Git o ai workspace locali di Claude e Gemini; lo stato di sincronizzazione resta una dichiarazione nei documenti.
- Non ho potuto riprodurre la suite completa V3.3 o mutation testing perché non sono inclusi.
- L'ispezione del codice è mirata, non un audit formale completo di sicurezza o correttezza.

## 10. Conclusione operativa

La revisione esterna non giustifica ancora l'avvio di sviluppo o l'autorizzazione del G0.

Prima di procedere, i punti tecnici più importanti da portare a decisione sono:

1. correggere il comportamento `n=0` dell'intervallo Wilson e il nome Kelly fuorviante, quando l'utente autorizzerà la successiva fase tecnica;
2. formalizzare il modello epistemico con una matrice completa di mapping verso `STANDARD.md`;
3. riscrivere il rischio aggregato come stress scenario e definire ipotesi di esecuzione, gap e slippage;
4. correggere e declassare le affermazioni non supportate nelle schede STR-001/STR-002;
5. chiarire il gate T-01…T-05 rispetto a qualunque nuovo codice;
6. verificare la fonte di verità e la sincronizzazione prima di creare il patrimonio condiviso.

**Nessuna decisione dell'utente viene presa in questo rapporto. V3.3 resta congelata. Nessun codice o repository è stato modificato.**

---

## 11. Fonti esterne consultate

- American Economic Association, Lo, Repin & Steenbarger (2005): https://www.aeaweb.org/articles?id=10.1257/000282805774670095
- NBER, Lo & Repin, *The Psychophysiology of Real-Time Financial Risk Processing*: https://www.nber.org/papers/w8508
- PubMed, Lo & Repin (2002): https://pubmed.ncbi.nlm.nih.gov/11970795/
- Risk.net, Almgren & Chriss: https://doi.org/10.21314/JOR.2001.041
- ScienceDirect, Lou, Polk & Skouras (2019): https://www.sciencedirect.com/science/article/pii/S0304405X19300650
- RePEc, Lou, Polk & Skouras (2019): https://ideas.repec.org/a/eee/jfinec/v134y2019i1p192-213.html
- SSRN, Branch & Ma (2012): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2142962
- ScienceDirect, Bouchaud, Farmer & Lillo (2009): https://www.sciencedirect.com/science/article/pii/B9780123742582500063
- TradingView, annuncio Pine Script v6: https://www.tradingview.com/blog/en/pine-script-v6-has-landed-48830/
- TradingView, release notes: https://www.tradingview.com/pine-script-docs/release-notes/
- Harvey, Liu & Zhu (2016), *Review of Financial Studies*: https://academic.oup.com/rfs/article-abstract/29/1/5/1843824
- Bailey et al., *The Probability of Backtest Overfitting*: https://escholarship.org/uc/item/4w1110bb
