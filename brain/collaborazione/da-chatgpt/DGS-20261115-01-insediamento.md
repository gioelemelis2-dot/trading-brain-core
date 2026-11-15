# DGS-20261115-01-insediamento

[OPINIONE] **Continuare in ricerca e demo. H-002 non è sigillabile su questo snapshot.** Il primo risultato utile è un verdetto riproducibile su una regola eseguibile, anche se negativo. Il rendimento mensile atteso e la probabilità personale di superare una sfida restano non stimabili (§4).

[VERIFICATO: `MANIFEST.tsv:1–3`, mandato e data di sessione] Base dichiarata `83c89561e39271263e36fadaa5b479658f80953e`, ramo `feat/esecutore-h002`, più 11 file Gemini provenienti da rami separati. Il nome del rapporto e la data dello snapshot sono quelli del mandato. La data della sessione è 14/11/2026. [NON VERIFICATO] La cronologia Git e quella dei sigilli richiedono un'attestazione separata.

1. [VERIFICATO: §0] Integrità interna dello ZIP confermata su tutti i 327 record del manifest.
2. [DEDOTTO: DGS-01–04] Prima del sigillo della scheda servono una regola di uscita eseguibile e il conteggio deciso dall'utente. Prima della verifica servono dati BID/ASK M1 legati all'impegno e un'unica apertura della coorte.
3. [OPINIONE: §4 e §6] Nessuna sfida a pagamento con le evidenze disponibili. La prima prova deve poter anche chiudere H-002.

## 0. Inventario

[VERIFICATO: Python `zipfile` e `hashlib`, poi `sha256sum`] Lo ZIP contiene **328 file ordinari** e 75 voci di directory. I **327** percorsi elencati in `MANIFEST.tsv` coincidono con i file estratti, con dimensioni e impronte corrette. Il solo percorso fuori lista è il manifest stesso. Sono corretti anche i conteggi di righe dei 325 file con un conteggio dichiarato. I due ZIP interni hanno `-1` in quella colonna. Il controllo CRC dello ZIP è riuscito. Le nove copie Markdown consegnate fuori dallo ZIP, compreso il mandato, corrispondono byte per byte ai rispettivi file interni.

| Oggetto | SHA-256 misurato |
| --- | --- |
| [VERIFICATO: `hashlib.sha256`] `trading_brain_completo.zip` | `6a3bd9c4f080f6a5c09001e2ae3f105236f058e64a493976493a1d261b903e87` |
| [VERIFICATO: `hashlib.sha256`] `MANIFEST.tsv` | `7b5a1744d28ac19c83a84417760d189f7ed066e389aabe31726ce14f4969cae5` |

[VERIFICATO: dalla radice estratta] Riscontro indipendente delle impronte. Il comando ha restituito codice 0.

```bash
awk -F '\t' '!/^#/ {printf "%s  %s\n", $1, $4}' MANIFEST.tsv | sha256sum --check --quiet --strict
```

[DEDOTTO] L'accordo fra i byte e il manifest dimostra integrità interna. Per autenticare la relazione con Git servono un riferimento ottenuto separatamente e l'identità dei file aggiunti dai rami Gemini. [NON VERIFICATO] Manca un secondo archivio con cui fare il diff. [VERIFICATO: `REGISTRO-MODIFICHE.md:345–397`, `H-002-REVISIONI.md:241–274`] Rispetto al riferimento storico del 13/11 indicato nel piano, lo snapshot documenta esecutore e sigillo scheda, replica D1/D2, esiti R9/R10 con P1–P8, proposta v3.2 e istituzione del DGS. Sono cambiamenti registrati nel progetto. Lo stato corrente di `main` resta da attestare.

[VERIFICATO: tracciato delle letture, elenco in appendice] Dei 327 file indicizzati ho letto **35 integralmente, 34 in parte, 258 senza lettura di merito**. Ho elaborato tutte le righe del manifest come inventario. Calcolo di hash, ricerche di stringhe e import durante i test non equivalgono a una lettura critica. Dei due ZIP interni ho ispezionato nomi e struttura, senza leggere integralmente i contenuti.

[VERIFICATO: inventario dei percorsi] Nello ZIP esterno non figurano file `.bi5`, `.csv`, `.jsonl`, `.parquet` o `.secret`, né `commitment.json` o il nuovo `registro_prove.json`. [NON VERIFICATO] L'inventario non attesta lo stato della cache sul Mac o l'assenza di segreti incorporati in altri formati. Nessun grafico, prezzo o output di strategia del periodo chiuso è stato aperto per questa relazione.

### 0.1 Stato dei documenti

| Tema | Stato che emerge dalle evidenze |
| --- | --- |
| Partizione | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:89–97`, `LOCK.md:10`, `DECISIONI-APERTE.md:280–289`] Il 70/30 appartiene alla versione storica. DA-26 fissa sviluppo dal 15/11/2023, verifica dal 2005 a circa il 31/10/2023 ed embargo, con demo futura come ultima prova. La fine esatta va ancora registrata. L'esempio 70/30 si trova nello **schema del Progetto generale**. `brain/architettura/ARCHITETTURA.md` tratta l'architettura didattica. |
| Gate 1 e broker | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:103–121`, `CONTINUITA.md:107–119`, `DECISIONI-APERTE.md:245–258`, `demo_broker_mt5_50k_xauusd.toml:21–39`] Il piano lo dice chiuso e reca una nota che supera easyMarkets. La scheda del conto da 50.000 USD è da riconciliare. FP Markets MT5 Raw è la scelta registrata per il nuovo demo. [NON VERIFICATO] Apertura effettiva di quel demo e ultime specifiche. |
| Disponibilità dati | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:119,427`, `CONTINUITA.md:120–137,153`] Le note più recenti del piano danno l'ASK recente per scaricato. La continuità e un'altra sezione del piano lo lasciano pendente. [NON VERIFICATO] Copertura sul Mac, per lato e risoluzione, soprattutto dello storico ASK. |
| H-001 | [VERIFICATO: `H-001-range-1m-BOZZA.md:1–5`, `REGISTRO-ESPLORAZIONI.md:17–18`, `DECISIONI-APERTE.md:359–361`] Chiusa dopo E-002, prima del sigillo. `CONTINUITA.md:142–144,167` conserva le richieste della fase precedente. DA-30 conserva uno schema per una futura candidata. Non risulta approvato un trasferimento automatico del mandato di H-001 a H-002. |
| H-002 | [VERIFICATO: `H-002-ORB-v3.md:3–16`, `H-002-v3.2-PROPOSTA.md:3–7,17–41`, `H-002-REVISIONI.md:253–274`] La v3.1 è la specifica di riferimento. L'esecutore che la scheda dice ancora da scrivere è presente sul ramo. La v3.2 resta proposta, con scelte A2, A3, A8 e parte di A11 anticipate nel ramo. R10 supera i conteggi e le pendenze R7 della continuità. I 119 test e i 40/40 + 70/70 mutanti sono esiti **dichiarati** in R10. |
| Journal, registro e arresto | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:78,113,359,374`, `CONTINUITA.md:149,185`, `DECISIONI-APERTE.md:334–353`] Il journal è implementato e risulta mai usato. I due JSON precedenti sono vuoti. Il registro nuovo è assente nello snapshot. DA-29 sostituisce la vecchia regola dei 100 trade e −10R con fedeltà e SPRT. Il numero 100 può essere discusso come requisito di osservazione operativa, se separato dall'arresto statistico. |
| Deposito del journal e Pine | [VERIFICATO: `DECISIONI-APERTE.md:238–243,287–289`, `DECISIONI.md:24`, mandato] DA-24 lascia aperte anche opzioni con dati nel repository. Il mandato attuale prescrive custodia locale dei dati personali. D-18 descrive le funzioni di TradingView. DA-26 vieta di guardare il periodo chiuso e di provare idee nello Strategy Tester fuori dal registro. L'adozione generale di DA-14 resta aperta. |
| Ruoli e regole | [VERIFICATO: `DECISIONI.md:15–29`, `PROTOCOLLO-OPERATIVO.md:3–7,18–41`, `guardian/LEGGIMI.md:9–13`] Il protocollo provvisorio assegna a Claude la scrittura canonica. D-15 assegna pari responsabilità di ricerca ai due centri, con registri di ricerca separati. Il TOML delle regole personali ha 14 conferme su 15, mentre il LEGGIMI le chiama ancora «proposta». D-20 è una revoca mirata della sospensione, con mandati successivi da tracciare. |
| Documenti storici e provenienza | [VERIFICATO: `PIANO-MIGRAZIONE.md:3`, `CONTINUITA.md:71–75`, `INDICE-PER-IL-DGS.md:58–62`, `ERRATA_V3_3.md:4` e `sha256sum` sullo ZIP interno] Il vecchio piano di migrazione è storico dopo D-19. L'indice dà la V3.3 come assente. È presente in `da-gemini/consegne/TRADING_BRAIN_V3_3_PACKAGE.zip` con impronta `6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638`, coerente con l'errata. |
| Difetti | [VERIFICATO: conteggio delle righe 22–53 di `REGISTRO-DIFETTI.md`] **32** rilevazioni storiche, 12 critiche, 13 importanti e 7 minori. La tabella riassuntiva a riga 60 attribuisce 5 importanti al simulatore, mentre le righe di dettaglio ne elencano 6. Le righe 63–66 smentiscono la precedente generalizzazione «nessun critico dal 15/11». Il conteggio non indica quanti difetti sono tuttora aperti. |

## 1. Mandato del DGS

[OPINIONE] Adotto il nucleo della bozza di Claude: parere prima dei gate, verifiche avversariali, registro dei limiti, controllo delle affermazioni di rendimento, campioni di correzioni e proposte. Le prove sono il criterio di giudizio dei revisori, incluso il DGS. Il parere è riferito a una versione precisa e riporta esito, evidenze, limiti, rilievi aperti e condizioni per una nuova valutazione.

| Ambito | Compito e frequenza proposta |
| --- | --- |
| Sigilli e passaggi di gate | [OPINIONE] Parere prima di ogni sigillo o promozione, e dopo modifiche sostanziali di scheda, input, criteri o codice. Un critico aperto produce parere **sospendere**, con conseguenza pratica e prova per chiuderlo. L'utente decide e registra eventuale deroga, con motivazione e condizioni. |
| Revisioni | [OPINIONE] Per ogni pacchetto nuovo, confronto con la versione precedente e controllo dei punti che possono cambiare il verdetto. Su ogni correzione critica, chiedere un oracolo indipendente e un caso che distingue il comportamento vecchio dal nuovo. Due revisioni utili devono coprire lo stesso candidato, con perimetri ed esiti distinguibili. |
| Consegne | [OPINIONE] Un Markdown `DGS-AAAAMMGG-NN-<tema>.md` per evento, con commit, inventario, rilievi, prove e disaccordi. Il DGS controlla in sola lettura la copia ricevuta. Claude archivia il rapporto intatto e aggiunge esiti e correzioni a parte. Aggiornamento del registro dei limiti quando emerge una nuova evidenza e a ogni decisione di gate. |
| Collaborazione | [OPINIONE] Claude implementa in TDD e mantiene i documenti canonici. Gemini replica dalla specifica fissata prima di vedere implementazione e risultati dell'altro. DeepSeek verifica un campione del rapporto DGS con gli stessi riferimenti e riporta i dissensi. I report recano impegni separati prima del confronto. L'utente risolve le divergenze che cambiano una regola. |
| Perimetro e capacità | [VERIFICATO: strumenti e inventario della sessione] Ho una copia locale, Python 3.12.14 e 3.13.5. Il comando `python3.9` non è disponibile. [OPINIONE] Il lavoro DGS comprende lettura, calcoli, test isolati su dati inventati e richieste scritte. Scrittura nel repository, merge, regole, uso del conto, sblocco dei dati e autorizzazioni restano nei ruoli stabiliti. [NON VERIFICATO] Non posso attestare stato del Mac, accessi alla cache o disponibilità del repository vivo da questo archivio. |

[DEDOTTO] La migliore ragione per il veto proposto da Claude, `2-MESSAGGIO-1-MANDATO.md:109–116`, è impedire che lo stesso autore corregga, collaudi e approvi una regola che può passare per errore. L'obiezione è che un DGS con una copia parziale può sbagliare diagnosi o bloccare su un rilievo già risolto. Propongo l'obbligo di una decisione tracciata davanti a un rilievo critico, con una sonda indipendente e la gravità ricalibrata se la sonda lo smentisce. Questo preserva l'autorità dell'utente e impedisce che un «procedi» generico faccia sparire il rischio.

## 2. Roadmap e ingegneria

[VERIFICATO: prove eseguite sulla copia, Python 3.13.5] **151 test selezionati sono passati**. Dalla radice: 47 con `python3.13 -s -B -W error -m unittest brain.dati.tests.test_pipeline brain.dati.tests.test_dukascopy brain.dati.tests.test_partizione_date` e 27 con `python3.13 -s -B -W error -m unittest brain.laboratorio.tests.test_backtester brain.laboratorio.tests.test_dsr_scala`. Da `brain/guardian`: 77 con `python3.13 -s -B -W error -m unittest discover -s test`. I controlli coprono i casi delle suite su questa copia. [NON VERIFICATO] Suite e mutanti di H-002, esiti su 3.9, riscontri sulla piattaforma MT5 e rami su GitHub.

| Gate | Stato dello snapshot ed esito di uscita proposto |
| --- | --- |
| **0 · Codice** | [VERIFICATO: `CONTINUITA.md:99–108`] Chiusura storica riportata, con conteggi riferiti a fasi diverse. [OPINIONE] Per ogni componente nuovo destinato a decidere un passaggio, stessa versione su Python 3.13 e 3.9, prove di integrazione e replica, registro dei mutanti equivalenti motivati. Le prove di integrazione devono coprire il percorso dati → rapporto. |
| **1 · Demo e G0** | [VERIFICATO: `CONTINUITA.md:109–119`] Configurato, riconciliazione pendente. [OPINIONE] Sul Mac, confrontare per XAUUSD saldo ed equity al reset, costi di andata e ritorno, valore del tick, lotto minimo e incrementi, orari e margine dopo un esempio per acquisto e vendita. Tolleranze dichiarate prima dalla precisione del broker. Uscita con nessuna discrepanza inspiegata e fonte distinta per limiti interni e limiti FTMO. |
| **2 · Dati e sigillo** | [VERIFICATO: `DECISIONI-APERTE.md:260–289`, `dukascopy.py:269–272,283–328`] Confini deliberati in linea di principio. Il sigillo esistente in codice è per BID 15m. [OPINIONE] Uscita con date UTC esatte e calendario, inventario immutabile di **BID e ASK M1** effettivamente usati, hash e attestazione locale prima dell'apertura, rapporto di copertura per lato e motivi dei buchi, seconda fonte nello sviluppo e licenza verificata. La verifica automatica di integrità può produrre esiti essenziali sul Mac sotto custodia del periodo chiuso. |
| **3 · Screening** | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:111`, `H-002-ORB-v3.md:115–156`] Proposto. Le esplorazioni sullo sviluppo sono già avvenute e la scheda è dichiarata pre-sigillo. [OPINIONE] Prima di eseguire: DA-19 e DA-20 risolte, scheda, snapshot del codice e parametri congelati, replica e revisione riferite all'identica versione, spesa N registrata. Sviluppo con criteri per questa ipotesi, esito «bocciata», «candidata» o «dati insufficienti». |
| **4 · Verifica storica** | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:112`, `H-002-ORB-v3.md:137–142`] Proposto, con soglie ma senza gestione esplicita del campione dopo una bocciatura. [OPINIONE] Congelare l'elenco delle candidate già promosse nello sviluppo, i confini, il registro N, il test, i requisiti di copertura, il rapporto e la politica di arresto. Un'apertura per la coorte predefinita. Solo output stabiliti prima. Se si esaurisce la verifica, una nuova candidata richiede dati futuri intatti o un blocco indipendente già riservato dall'utente prima dell'apertura. |
| **5 · Forward demo** | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:113` e `DECISIONI-APERTE.md:334–353`] Proposto. «Costi e aderenza come nel backtest» non specifica tolleranze, trattamento dei dati mancanti o denominatori. [OPINIONE] Fissare prima le tolleranze per orari, scarti, fill, spread e slippage. Nei primi 20–30 trade controllare questi aspetti e registrare i segnali mancati. Poi protocollo prospettico fissato per l'edge e arresti di rischio sempre attivi. Contare tutti i segnali, inclusi saltati e rifiutati, e giorni senza trade. Due broker con gli stessi segnali sono repliche di esecuzione, con campioni di P/L dipendenti. |
| **6 · Sfida** | [VERIFICATO: `DECISIONI.md:20`, `DECISIONI-APERTE.md:315–319`] Proposta, subordinata all'autorizzazione esplicita e a più strategie testate. [OPINIONE] Due requisiti indipendenti: evidenza economica prospettica compatibile con il costo totale e conformità operativa al prodotto selezionato, misurata su equity e affiancata da prove di stress. Versionare regole, costi e criterio di abbandono. Il pagamento della sfida richiede una decisione distinta dell'utente. |
| **7 · FTMO Account** | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:116`, FAQ FTMO] Proposto. La soglia di ritorno al Gate 5 è da specificare. L'account FTMO usa fondi simulati e il premio può essere in denaro. [OPINIONE] Fissare orizzonte, soglie di deterioramento, perdita/violazione, cambio di regole o feed, e arresto indipendente dal P/L. Un superamento della sfida è un risultato operativo, con evidenza limitata sulla persistenza del rendimento. [FAQ sull'infrastruttura](https://ftmo.com/en/faq/how-does-the-ftmo-technical-infrastructure-work/) · [FAQ sui premi](https://ftmo.com/faq/how-do-i-withdraw-my-profits/) |

[DEDOTTO] Il Gate 1 è stato dichiarato chiuso prima della sua riconciliazione. Il Gate 2 deve attestare il formato del consumo effettivo. I Gate 3–7 richiedono decisioni sui criteri prima della rispettiva ammissione. Si possono svolgere in parallelo riconciliazione locale, raccolta autorizzata e test su dati inventati. L'ordine vincolante della prima prova è **regole e oggetto della prova fissati → screening sullo sviluppo → apertura della coorte predefinita → demo futura**. [VERIFICATO: `PROGETTO-GENERALE-20261115.md:32,170`] La regola del piano richiede il sigillo dello storico prima di qualsiasi backtest. [OPINIONE] Portare avanti in parallelo la finalizzazione del dataset storico e il collaudo sintetico. La preregistrazione della scheda e il sigillo dei dati sono due atti separati.

### 2.1 Rilievi

| ID | Gravità | Area | Prova e implicazione | Rimedio proposto |
| --- | --- | --- | --- | --- |
| DGS-01 | **Critica** | Dati e sigilli | [VERIFICATO: `dukascopy.py:269–272,295–319`, `caricatore.py:22–58`, `esegui_h002.py:211–230`] Gate 2 sigilla BID aggregato a 15 minuti. Il percorso di H-002 letto qui usa cache BID e ASK M1 e controlla l'impronta della scheda. Il controllo del BID aggregato non attesta la sequenza M1 o gli ASK che causano le uscite. | [OPINIONE] Legare la verifica effettiva a impronte e confini dei due lati M1, alla configurazione, al commit e alla specifica. A dati dichiarati diversi, arresto prima del calcolo decisivo. |
| DGS-02 | **Critica** | Apertura unica | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:32,112,123`, `sigillo.py:116–134`] Il piano dice apertura unica e ritorno al Gate 3. Il registro distingue verifiche per ipotesi e variante. [DEDOTTO] Se una nuova scheda usa i risultati del test già aperto, anche aggregati, la prossima promozione usa informazioni del test precedente. | [OPINIONE] Un'apertura per campione e coorte congelata, con stato di consumo del campione. Ripetizioni di ingegneria sulla stessa prova solo con output invariati e senza nuova decisione. |
| DGS-03 | **Critica** | Causalità della specifica H-002 | [VERIFICATO: `H-002-ORB-v3.md:79–81`, `H-002-v3.2-PROPOSTA.md:60–61`] In assenza di quotazioni dopo le 16:30 si prende un prezzo di prima delle 16:30. La decisione di usarlo dipende dall'assenza futura. È nella scheda e nei casi d'oro. | [OPINIONE] Definire un ordine causalmente eseguibile entro l'orario, dichiarare le uscite mancanti e valutarne l'impatto senza imputare un fill retroattivo. Confermare il rimedio nel giro R11 successivo. |
| DGS-04 | **Critica** | N e registro | [VERIFICATO: istruzioni del progetto, `H-002-ORB-v3.md:115–121,138`, `sigillo.py:77–101`, `esegui_h002.py:37–42,238–246`] Il contatore usa solo le prove selezionabili. Le configurazioni di robustezza restano eventi fuori da N. Ci sono due vecchi registri vuoti e il nuovo è assente. [DEDOTTO] Il valore di N riportato può cambiare un verdetto senza che cambi un solo R. | [OPINIONE] Un solo conteggio verificabile, invarianti sul registro e riconciliazione di E-001/E-002. Applicare a tutte le varianti dichiarate la regola del mandato e sottoporre all'utente ogni esclusione prima dei dati. |
| DGS-05 | **Importante** | Sigillo della ricerca e stato delle regole | [VERIFICATO: `sigillo.py:91–113`, `esegui_h002.py:174–190,235–246`, `H-002-v3.2-PROPOSTA.md:17–41,70–76`] L'impegno corrente contiene l'hash della scheda. Il ramo anticipa criteri della v3.2 e accetta date/seme/ripetizioni come argomenti. L'impronta proposta dei file operativi è una misura utile e copre solo parte della provenienza. | [OPINIONE] Fissare specifica ratificata, codice e dipendenze rilevanti, date, dati, criteri e parametri. Distinguere prova, replica e cambio sostanziale. Una nuova regola dopo il sigillo ha una nuova scheda e un nuovo costo N. |
| DGS-06 | **Importante** | Buchi e costi | [VERIFICATO: `H-002-ORB-v3.md:22–30,89–98`, `H-002-v3.2-PROPOSTA.md:31–33`, `caricatore.py:27–35`] Presenza dei file, completezza delle quotazioni e minuto realmente senza prezzi sono tre fatti diversi. A15 è ancora una proposta con soglia di tre minuti BID. Commissione e slippage della scheda richiedono misure distinte dal BID/ASK del feed. | [OPINIONE] Regola determinata prima dei dati per giorno di mercato vuoto, gap e minuti non eseguibili anche sul solo ASK, code di slippage e copertura minima. Trattare scenari e incertezza su entrambi i lati. |
| DGS-07 | **Importante** | Applicabilità in demo | [VERIFICATO: `H-002-ORB-v3.md:60–63,87,94`, `regole_personali.toml:87–95,125–132`, `guardian/LEGGIMI.md:3,18–22`] H-002 senza filtro notizie e con ingresso immediato è una ricerca offline. In manuale la finestra P-08 e il ritardo P-12 possono cambiare segnali e fill. Il G0 è consultivo. | [OPINIONE] Prima di usare la candidata in demo per inferenza, applicare il protocollo effettivo di esecuzione e misurare le differenze. Se cambia la regola, preregistrare la variante. Per training G0 usare il journal locale e tenere distinta la raccolta delle evidenze. |
| DGS-08 | **Importante** | Potenza e criterio economico | [CALCOLATO: §4] A 500 trade il valore 0,0471 citato nelle revisioni è il benchmark SR₀ del DSR, mentre la soglia osservata per arrivare a 0,95 è circa 0,1210 nell'esempio N=4. [VERIFICATO: `H-002-ORB-v3.md:137–142`] In verifica si chiede media > 0, senza esplicito margine economico sul rendimento mensile. | [OPINIONE] Per DA-20 distinguere R medio, Sharpe, potenza e margine economico dopo costi. Fissare trattamento di dipendenza, fasi di selezione e incertezza di N e V. |
| DGS-09 | **Importante** | Prop e rischio intratrade | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:156`, `H-002-ORB-v3.md:100–103`, fonte FTMO] Le barriere sui trade chiusi ignorano il percorso dell'equity. [DEDOTTO] Un trade che recupera prima della chiusura può aver già violato un limite giornaliero. | [OPINIONE] Prima del Gate 6, specificare prodotto e fase, reset e fuso, granulosità dell'equity, rischio intratrade, limiti personali e della prop firm. Calibrare sulle misure locali e rivalidare le regole ufficiali. [FTMO Trading Objectives](https://ftmo.com/en/trading-objectives/) |
| DGS-10 | **Importante** | Dati personali nell'export | [VERIFICATO: `0-GUIDA-PER-L-UTENTE.md:28–29`, ricerca di corrispondenza esatta nei testi dello ZIP esterno] Una stringa di nominativo del template ricorre 7 volte in 4 file. Percorsi e righe: `brain/dati/reali/TEMPLATE_RICONCILIAZIONE_DA25.toml:53`, `brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/AUDIT_OSTILE_SU_CLAUDE.md:6`, `brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md:7,19,562,615`, `brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md:7`. | [OPINIONE] Per i prossimi revisori rigenerare un export autorizzato e redatto, con segnaposto e scansione locale di file e archivi interni. Il rapporto riporta solo riferimenti. |
| DGS-11 | **Importante** | Provenienza e conflitti operativi | [VERIFICATO: tabella §0.1, `H-002-REVISIONI.md:4,100,122,221`] Invio a revisore diverso e file sbagliati ripetuti. Continuità, indice e piano hanno versioni discordanti. [DEDOTTO] Un esito associato al candidato sbagliato può autorizzare un passaggio ingiustificato. | [OPINIONE] Intestazione di consegna con destinatario, autore, commit e hash esatti di input e output. Una sola scheda di stato del gate legata a decisioni ed evidenze. Storico leggibile con nota di sostituzione. |
| DGS-12 | **Minore** | Contabilità dei difetti | [CALCOLATO: §0.1] 6 importanti nel gruppo simulatore, 5 nella tabella aggregata. | [OPINIONE] Generare il riepilogo dalle righe e aggiungere stato, versione scoperta e versione confermata corretta. |

### 2.2 Prove e priorità

1. [DEDOTTO] **DGS-01.** L'argomento più forte in favore del Gate 2 esistente è che il BID 15m costituisce già una serie verificabile, e la cache M1 sarebbe un suo antecedente. Il progetto ha due catene distinte, con verifiche di integrità diverse. [CALCOLATO: confronto per aggregazione su dati inventati] Due sequenze con apertura 100, chiusura 100 ed estremi 90/110, una con 110 prima di 90 e l'altra con 90 prima di 110, hanno lo stesso OHLC. Un'uscita al primo tocco può avere esito opposto. Anche un BID identico lascia indeterminati gli ASK. La prova da chiedere è il vincolo sulle **stesse** osservazioni che entrano nell'esecutore.
2. [DEDOTTO] **DGS-02.** Il ritorno al Gate 3 può essere inteso come ripartenza legittima con un esperimento nuovo. Funziona se il campione futuro resta indipendente dalle scelte. [CALCOLATO] Come controesempio illustrativo, con prove indipendenti al 5% la probabilità di almeno una falsa promozione vale `1 − 0,95^k`: 9,75% a due prove e 22,62% a cinque. Nel riuso adattivo dello stesso campione questo calcolo non si applica. Il problema è anche la scelta del prossimo test condizionata all'output precedente.
3. [DEDOTTO] **DGS-03.** La motivazione più forte della regola è rispettare «mai posizioni oltre» e gestire un feed mancante. Lo stesso ordine non può però dipendere da quello che succederà dopo il suo fill. [CALCOLATO: formula R della scheda e aritmetica Decimal] Dal caso d'oro 8, due traiettorie didattiche identiche fino alla chiusura delle 16:29 hanno ingresso 2.003,40, 88 once e commissione 0,07 per oncia. Con nessun minuto eseguibile nella finestra, l'uscita retroattiva a 2.011,80 dà **+1,46608R**. Con quotazione BID 2.000 alle 16:30, l'uscita a 1.999,80 dà **−0,64592R**. Per i due percorsi cambia l'esistenza del fill alle 16:29, quando le informazioni disponibili sono ancora identiche. Questo comprova il difetto della specifica. L'impatto sul codice e la frequenza restano al giro tecnico.
4. [DEDOTTO] **DGS-04.** Claude e Gemini sostengono che una robustezza fissata prima e usata esclusivamente come veto non offre una nuova scelta di vincitore. È una posizione statistica difendibile in un disegno che lo garantisce. Il mandato ricevuto include le varianti dichiarate e il DSR usa il registro globale. Prima di eseguire vanno esplicitati i 2 candidati, i 6 + 4 switch di robustezza, i 2 stress di esecuzione e tutte le esplorazioni che hanno orientato la scelta. Le 2 principali sono approvate come perimetro di H-002. [CALCOLATO] La lettura letterale delle configurazioni dichiarate porta a 12 prima degli stress e a 14 includendoli, prima di altre prove. Sono scenari di calcolo, con classificazione da ratificare. [CALCOLATO: `DSRCalculator.calculate_dsr_analytical(0.05, N, 2500)`] A momenti normali e V = 1/2499, esce 0,9761 con N=2 e 0,7979 con N=12. Lo stesso Sharpe osservato supererebbe la prima soglia e fallirebbe la seconda. I benchmark fissi e i test sintetici vanno comunque tracciati come controlli.
5. [DEDOTTO] **Punti singoli di rottura.** Cache, nonce e apertura dipendono dal Mac. Provare il ripristino localmente con dati inventati e copie protette. L'utente oggi trasferisce pacchetti e può attribuire un rapporto alla versione sbagliata. Usare una scheda di consegna comune con SHA-256, commit, data, fase e letture autorizzate, con ricevute dei revisori prima dello scambio delle conclusioni. Il registro delle prove richiede una sola cronologia con scritture serializzate e una ricevuta dell'intera coorte. Un lock serializza le singole scritture. Un'esecuzione con più scritture richiede stati predefiniti di avvio, consumo e interruzione. Il journal ha catena e ancora, con limite documentato se vengono riscritte insieme. La prova è un ripristino locale e confronto con l'ancora conservata separatamente. `journal/LEGGIMI.md:25–49`, `H-002-REVISIONI.md:253–272`.

[OPINIONE] La sequenza di correzione è DGS-01–05 prima dei rispettivi usi decisivi, poi riconciliazione DGS-06–07 prima di valutare trasferibilità alla demo. La correzione dell'export DGS-10 precede ogni nuova distribuzione. Rinviare portafoglio, altri broker e automazione finché un ciclo completo su dati inventati esercita i controlli previsti per il primo esperimento.


## 3. Registro dei limiti

[OPINIONE] Le gravità riguardano il verdetto che il limite può falsare. I rimedi sono proposte per i gate indicati. Il costo N di ogni intervento è in §7. Quando un dato manca, il suo stato rimane «non stimabile» per la decisione che ne dipende.

| Limite | Gravità ed evidenza | Rimedio o limite residuo |
| --- | --- | --- |
| Integrità e cecità del periodo chiuso | [DEDOTTO] **Critica**. Gli hash attestano i byte. Non attestano chi abbia visto i grafici, l'addestramento dei modelli o la bontà della data di fissazione. Il vecchio 70/30 includeva mesi già visti. DA-26 riduce l'esposizione, anche se i grandi eventi del periodo sono noti. `DECISIONI-APERTE.md:260–289,293–299`. | [OPINIONE] Scaricamento, convalida tecnica e custodia locale separati dalla ricerca, con attestazione di accessi, seconda persona o passaggio controllato quando disponibile. Se si perde la cecità, l'output storico diventa esplorativo e serve una nuova osservazione prospettica. Nessun rimedio retroattivo alla visione già avvenuta. |
| Dati BID/ASK, storia e calendario | [VERIFICATO: `CONTINUITA.md:120–137`, `H-002-ORB-v3.md:22–47`] **Critica** per la verifica se l'input effettivo non è sigillato. **Importante** per copertura e qualità. I documenti riportano 429, controlli dei buchi e revisione del formato. Gli ASK del blocco storico e i calendari anteriori al 2019 restano da attestare. | [OPINIONE] Rapporto locale aggregato per lato e finestre autorizzate, controlli M1 su doppioni, monotonia, sessioni, giorni legittimamente vuoti e ASK senza BID o viceversa. Distinguere prezzi non osservati, errore del feed e chiusura; una seconda fonte si confronta nello sviluppo. I termini Dukascopy e la comparabilità con MT5 restano da verificare prima di usare e redistribuire dati. |
| Prezzi a barre e fill | [DEDOTTO] **Importante**. BID/ASK OHLC separati non danno sequenza intraminuto, simultaneità delle quotazioni, disponibilità di size o fill al tocco di un limite. Il caso ambivalente stop e target è gestito nella scheda, mentre l'uscita retroattiva resta critica (DGS-03). | [OPINIONE] Fissare un modello causale conservativo. Se l'esito dipende dall'ordine o dai buchi, riportare scenari avversi, misura locale prospettica o «non stimabile». Anche la perfetta replica di un oracolo inventato non ricrea tick non conservati. |
| Costi e scala della posizione | [VERIFICATO: `H-002-ORB-v3.md:89–98`, `demo_broker_mt5_50k_xauusd.toml:23–48`] **Importante**. Spread del feed, commissione, slippage e finanziamento sono grandezze diverse. Il simulatore arrotonda in once su 100.000 USD fissi. Lotto minimo, step, tick, margine e condizioni del conto da 50.000 USD sono da convalidare. | [OPINIONE] Misurare localmente costi per ora, direzione, volatilità, size e tipo d'ordine, incluse le code e i rifiuti. Contabilità per lato senza doppio conteggio dello spread, separando qualità di esecuzione da strategia. Overnight solo con regola decisa e swap esplicito. P-01 è rischio nominale di size. Un gap e uno stop senza fill possono superarlo. |
| Statistica, potenza e stazionarietà | [CALCOLATO: §4] **Importante**. Per uno Sharpe netto 0,10 a trade, 785 osservazioni indipendenti con due prove, circa 1.211 con dodici, in un esempio parametrico. Dipendenza, selezione, regimi e costi incerti possono alzare il fabbisogno e cambiare persino il parametro che si sta stimando. | [OPINIONE] Obiettivo e intervallo dati fissati prima, serie giornaliera inclusi zeri, blocchi temporali o varianza di lungo periodo con taratura del test. Storico vecchio come trasferibilità di regime e demo prospettica per il mercato di oggi. Nessun rimedio che garantisca persistenza. |
| Contabilità e famiglie di test | [VERIFICATO: `REGISTRO-ESPLORAZIONI.md:3–18` e DGS-04] **Critica** se un N incompleto consente una falsa promozione. Prove implicite e selezione di periodi si possono perdere mentre il contatore sembra coerente. | [OPINIONE] Registro globale per il DSR, subregistri indipendenti per il lavoro cieco, distinzione fra progetto strategico, replica, robustezza, stress, ricerca descrittiva e comparatore. Esiti dei candidati respinti inclusi tra le evidenze. Mancanze pregresse annotate con intervallo o limite, senza inventare un conteggio. |
| Demo rispetto a esecuzione e premi | [VERIFICATO: FAQ FTMO sul capitale simulato, `DECISIONI-APERTE.md:334–353`] **Importante**. Più demo possono misurare differenze di feed, fill e disciplina. La replica dello stesso giorno non aumenta in modo indipendente il numero di opportunità. Una demo gratuita e un programma a pagamento possono avere regole diverse. | [OPINIONE] Stessi eventi identificati una volta, risultati per broker appaiati, campione comune e copertura degli eventi mancanti. Separare fedeltà della piattaforma, robustezza economica e condizioni contrattuali. [FAQ FTMO](https://ftmo.com/en/faq/how-does-the-ftmo-technical-infrastructure-work/) |
| Prop firm e profilo di rischio | [VERIFICATO: `DECISIONI.md:20–23`, `prop_firm_ftmo.toml:30–66` e fonte FTMO] **Importante**. Prodotto, fase, equity, orario del reset, limiti statici/trailing e restrizioni cambiano la decisione. Simulare solo trade chiusi non cattura tutte le violazioni. | [OPINIONE] Prima di un gate a pagamento, regole ufficiali del prodotto riconfermate, confronto fra sequenze di equity e piattaforma, simulazione condizionata a dati e ipotesi con intervalli di incertezza. P-05 1,5% distinto dai limiti della prop. [FTMO Trading Objectives](https://ftmo.com/en/trading-objectives/) |
| Comportamento e journal | [VERIFICATO: `PROGETTO-GENERALE-20261115.md:48,53,184–198`, `CONTINUITA.md:185`] **Importante**. Il progetto individua il rischio di decisioni impulsive. Il G0 ha avvisi, l'aderenza sul conto non è ancora misurata e un journal di soli trade eseguiti può omettere i segnali saltati. Un punteggio soggettivo può cambiare dopo il P/L. | [OPINIONE] In demo registrare sul Mac segnale, intenzione, avviso e decisione prima del risultato, con motivo per ogni deroga e riconciliazione di tutti i trade del conto. Valutare rispetto di P-01/P-05/P-08/P-12 e discrepanze di processo. Nessun indicatore è una diagnosi o una garanzia comportamentale. |
| IA, fonti e manutenzione | [VERIFICATO: `H-002-REVISIONI.md:3–7,99–122,220–238`, `QUADERNO-IPOTESI.md:3–6`] **Importante**. Chat e revisioni hanno visibilità e versioni diverse. Accordo fra fornitori può riflettere letteratura ed esempi comuni. Esiti in una chat non valgono come accesso al repository. | [OPINIONE] Impronta delle consegne, stime o rapporti sigillati prima del confronto, fonte primaria per ogni soglia o fatto esterno, campione controllato da DeepSeek o persona competente. Le fonti viste solo in abstract vanno indicate. Nessun rimedio che garantisca indipendenza degli errori delle IA. |
| Tempo e capacità del Mac | [NON VERIFICATO] **Importante**. Mancano ore effettive disponibili, durata e completezza della raccolta sui lati M1, frequenza della candidata e tasso di segnali che si possono eseguire. [CALCOLATO: §4] A tre trade a settimana, 600 richiedono circa 3,85 anni con 52 settimane utili. | [OPINIONE] Misurare capacità e frequenza nel periodo autorizzato, controllare i tempi per percorso, riportare finestre con trade assenti. Dedicare priorità al primo ciclo end-to-end. Se il campione richiesto eccede l'orizzonte, cambiare l'obiettivo della ricerca o attendere nuova evidenza. |

## 4. Aspettative contro prove

[VERIFICATO: `DECISIONI-APERTE.md:315–324`] L'1–2% al mese è un obiettivo dichiarato. [DEDOTTO] La migliore tesi favorevole è che bastano pochi R al mese e che un edge intraday, se stabile e trasferibile con costi misurati, può produrli. Oggi la previsione di ottenerli è **basata sul nulla** come stima specifica per il progetto. Non risulta una strategia pre-registrata con media netta, frequenza, code, copertura e rischio validati. [VERIFICATO: `H-002-ORB-v3.md:13–16`, `H-002-REVISIONI.md:146–162`, `REGISTRO-ESPLORAZIONI.md:9–18`] L'archivio documenta studi esplorativi, risultati sintetici e test di software.

[CALCOLATO: risultato E-002, righe 47 e 68] Con l'ampiezza mediana di 1,81 USD, p = 0,347, target 0,5 volte l'ampiezza e stop 0,25 volte l'ampiezza, l'esempio dà 1,81 × (0,75 × 0,347 − 0,25) ≈ **0,0186 USD/oncia lordi**. Sottraendo anche il costo ipotizzato più basso, 0,07 USD/oncia, si scende a circa −0,0514 USD/oncia. [DEDOTTO] Questo sostiene l'archiviazione di H-001 per i micro-range studiati. Il calcolo usa l'ampiezza mediana come esempio. Il risultato per trade richiederebbe fill e costi osservati. La conclusione è limitata ai micro-range studiati.

[CALCOLATO] Con size nominale fissa pari a 0,5% del capitale iniziale, **1% = +2R** e **2% = +4R** sul mese, dopo costi di trading. Nell'esempio di 100.000 USD simulati, 1R = 500 USD. Per un numero di trade mensile fissato nello scenario si usa `rendimento = 0,005 × m × μ_R`. L'esempio esclude compounding, variazione del conteggio, condizioni del premio, imposte e costo della sfida.

| Trade al mese, ipotesi | R netto medio per 1% | R netto medio per 2% |
| --- | --- | --- |
| [CALCOLATO] 10 | 0,200R | 0,400R |
| [CALCOLATO] 15 | 0,133R | 0,267R |
| [CALCOLATO] 20 | 0,100R | 0,200R |

[CALCOLATO] Con 15–20 trade e +0,05R medio netto, la media del modello è +0,375–0,50% mensile sul capitale iniziale. La soglia +0,05R dello screening è quindi insufficiente da sola per l'obiettivo mensile, anche se fosse una misura stabile. [NON VERIFICATO] Si ignorano frequenza, distribuzione e costi effettivi. «1–2% medio su più mesi», «raggiungerlo il più delle volte» e «premi incassati» richiedono obiettivi e misure diversi. Per verificare la prima affermazione serve una serie di rendimenti per mese, con i mesi senza trade inclusi e un margine economico dichiarato in anticipo.

### 4.1 Trade, anni e Sharpe netto

[CALCOLATO: `statistics.NormalDist`, controllo con t non centrale] Per la pianificazione, uso un test a una coda di media netta positiva, α di famiglia = 5%, potenza 80%, correzione Bonferroni e trade normali indipendenti nel calcolo parametrico. Definisco `δ = (μ_alternativa − μ_null)/σ_R`. Contro zero, δ è lo Sharpe per trade nel modello. Con \(\Phi^{-1}\) quantile normale:

\[
n \simeq \left\lceil \left(\frac{\Phi^{-1}(1-0.05/N)+\Phi^{-1}(0.80)}{\delta}\right)^2 \right\rceil .
\]

| N di pianificazione | δ = 0,05 | δ = 0,08 | δ = 0,10 | δ = 0,15 | δ = 0,20 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [CALCOLATO] 1 | 2.474 | 967 | 619 | 275 | 155 |
| [CALCOLATO] 2 | 3.140 | 1.227 | 785 | 349 | 197 |
| [CALCOLATO] 12 | 4.844 | 1.893 | 1.211 | 539 | 303 |
| [CALCOLATO] 14 | 4.990 | 1.949 | 1.248 | 555 | 312 |
| [CALCOLATO] 20 | 5.326 | 2.081 | 1.332 | 592 | 333 |

[CALCOLATO] La t non centrale con deviazione stimata dà, a δ = 0,10, rispettivamente **620, 787, 1.215, 1.251 e 1.336** trade. È un secondo calcolo nello stesso mondo gaussiano. Per N = 2 e 300, 600, 2.500 trade, l'effetto netto rilevabile contro zero all'80% è circa **0,162, 0,114 e 0,056** Sharpe per trade. Con N = 12 sale a **0,201, 0,142 e 0,070**. Queste sono soglie di potenza, distinte dalle soglie per un test osservato e dalle regole già adottate dal progetto. [DEDOTTO] 300 è un filtro di screening per H-002. Uno Sharpe osservato di 0,06 su 300 trade non prova un edge stabile. La tabella del piano usa il vecchio 70/30 e arrotondamenti nei profili. I fabbisogni vanno rifatti per DA-26 con la frequenza osservata e il protocollo finalizzato. `PROGETTO-GENERALE-20261115.md:125–155`, `H-002-ORB-v3.md:123–133`.

| Fabbisogno a δ = 0,10 | 250 trade/anno | 156 trade/anno, 3×52 | 52 trade/anno |
| --- | ---: | ---: | ---: |
| [CALCOLATO] 785 trade, N = 2 | 3,14 anni | 5,03 anni | 15,10 anni |
| [CALCOLATO] 1.211 trade, N = 12 | 4,84 anni | 7,76 anni | 23,29 anni |
| [CALCOLATO] 1.248 trade, N = 14 | 4,99 anni | 8,00 anni | 24,00 anni |
| [CALCOLATO] 1.332 trade, N = 20 | 5,33 anni | 8,54 anni | 25,62 anni |

[CALCOLATO] La finestra di sviluppo indicata in H-002 ha 782 giorni feriali inclusivi, prima di festività, 20 sessioni di riscaldamento e filtri. H-002 può fare al massimo un trade al giorno. È un tetto di calendario, non una stima della frequenza. [DEDOTTO] La verifica storica di circa 18 anni può contenere abbastanza osservazioni per alcuni effetti. Servono copertura reale e un campione con struttura e costi compatibili con il futuro. Il forward demo a tre trade/settimana può richiedere anni per risolvere un edge modesto. Anche assumendo 100 trade indipendenti e σ = 1R, il margine normale del 95% sulla media è 1,96 × 1/√100 = **0,196R**. 100 trade servono a studiare l'esecuzione e sono insufficienti per precisione di pochi centesimi di R in questo scenario.

[CALCOLATO] Per **superare** l'obiettivo dell'1% a 20 trade/mese, la null economica è μ ≤ 0,10R. Se l'alternativa è 0,15R e σ = 1R, δ = 0,05. Con N = 2 servono circa **3.140** trade (3.142 con t non centrale), cioè circa 13,1 anni a 240 trade/anno. Con verità esattamente sul target, al confine della null si rifiuta alla frequenza nominale del test. Per il 2% e 20 trade/mese la soglia è μ = 0,20R. La differenza fra l'alternativa e questa soglia determina la potenza, insieme a σ. [DEDOTTO] Misurare i rendimenti mensili e la frequenza con distribuzione congiunta è necessario per testare un obiettivo mensile effettivo. Il calcolo in R quantifica solo il costo informativo della differenza.

[VERIFICATO: fonte primaria e `dsr.py:167–221`] Bailey e López de Prado usano lunghezza della serie, asimmetria, curtosi, dispersione degli Sharpe e numero di prove indipendenti per correggere la selezione. Il progetto chiede N globale. Con candidati correlati, pochi candidati promossi, V stimato su serie eterogenee o dipendenza seriale, DSR ≥ 0,95 ha un significato condizionato. [DEDOTTO] Un controllo con blocchi temporali o test individuali calibrati e correzione di famiglia può misurare la sensibilità del verdetto al modello del DSR. Il disegno va fissato prima di aprire il campione. [CALCOLATO: formula separata e chiamata al calcolatore del progetto] Nel caso normale citato in `H-002-REVISIONI.md:53,117`, T = 500, N = 4, V = 1/499, **SR₀ = 0,04710**. Per DSR = 0,95 serve **SR osservato ≈ 0,12100**. Input illustrativo μ = 0,10R, σ ≈ 1,246R, SR ≈ 0,08026 dà **DSR = 0,77020**. Gemini distingue le soglie nel rilievo R-09. La sintesi di Claude mescola benchmark e soglia finale. Il rinvio del DSR alla verifica resta una scelta motivabile, da tarare sul disegno di DA-20. [Bailey e López de Prado, 2014, §3](https://davidhbailey.com/dhbpapers/deflated-sharpe.pdf) · [Lo, 2002](https://rpc.cfainstitute.org/research/financial-analysts-journal/2002/the-statistics-of-sharpe-ratios)

### 4.2 Arresto in demo e modello di sfida

[VERIFICATO: `python3.13 -s -B brain/laboratorio/studi/simulazione_sprt.py`] Con 6.000 serie normali indipendenti per condizione, σ = 1R e tetto 600, il programma stampa promozione **3,7%** sotto μ = 0 e **64,3%** sotto μ = +0,10R, con 17,1% di arresti e 18,6% di indecisioni in quest'ultimo scenario. [CALCOLATO: seconda simulazione, 20.000 sequenze, seme 812] Con dispersione marginale invariata e correlazione AR(1) = 0,30, le false promozioni a μ = 0 salgono dal **3,94%** in i.i.d. al **12,41%** nello scenario dipendente. A μ = 0,10 gli arresti salgono dal **17,08% al 32,99%**. La dipendenza è un'ipotesi del controesempio. [CALCOLATO] In quel modello la varianza di lungo periodo è circa 1,86 volte quella marginale, `(1+0,30)/(1-0,30)`. Le percentuali si riferiscono al solo scenario simulato. [OPINIONE] La fedeltà dei primi 20–30 trade è tecnica. Per il rendimento, fissare varianza di lungo periodo, unità temporale, test continuo e troncamento, con errori tarati per più strategie e costi di arresto. Un cambio di modello statistico deve essere deciso prima della demo. Il limite di rischio opera anche mentre si accumulano le osservazioni.

[VERIFICATO: fonte FTMO] Il 2-Step pubblica target +10% e +5%, limite giornaliero del 5% del capitale simulato iniziale sottratto al saldo a mezzanotte CE(S)T e verificato sull'equity, limite totale statico 10% e almeno quattro giorni con aperture in ciascuna fase. Il 1-Step ha regole diverse, fra cui limite giornaliero 3%, trailing a fine giornata e Best Day Rule. Le FAQ precisano restrizioni per fasi, tipo di conto, notizie selezionate, compreso XAUUSD per eventi USD indicati, e interruzioni di mercato. [DEDOTTO] Il Gate 6 deve legarsi al prodotto e alla fase. Il futuro FTMO Account usa ancora fondi simulati, pur potendo dare premi monetari. [Obiettivi FTMO](https://ftmo.com/en/trading-objectives/) · [Regole sulle notizie](https://ftmo.com/en/faq/can-i-trade-news/) · [Regole sulle posizioni](https://ftmo.com/faq/can-i-hold-positions-overnight-or-over-the-weekend/) · [Infrastruttura FTMO](https://ftmo.com/en/faq/how-does-the-ftmo-technical-infrastructure-work/)

[CALCOLATO: formula delle due barriere e script del progetto] A rischio fisso 0,5%, ±10% equivale a ±20R. Nel moto browniano con varianza di 1 R² per unità di tempo espressa in trade, la probabilità di arrivare a +a prima di −a è \(1/(1+\exp(-2\mu a/\sigma^2))\). Ne risultano **50,0% / 88,08% / 98,20%** a μ = 0 / 0,05 / 0,10R. Lo script, con 4.000 traiettorie gaussiane discrete per scenario, stampa **49,1% / 89,0% / 98,2%**. Nel modello continuo la durata media fino a una delle due barriere è 400 / 305 / 193 unità di tempo, per σ² = 1 e a = 20. [DEDOTTO] Moltiplicare questi esiti per una probabilità della fase successiva, oppure chiamarli tasso FTMO, non è giustificato dai dati. A parità di traiettorie, aggiungere un vincolo può ridurre il numero di percorsi ammessi. Cambiando distribuzione, size, condizionamento o comportamento si perde anche la lettura come limite superiore generale. La roadmap usa 50%, 88%, 98% in un modello con una sola fase e senza limite giornaliero. È una sensibilità teorica. `PROGETTO-GENERALE-20261115.md:156`, `simulazione_sprt.py:46–79`.

### 4.3 Frequenze di base

| Riferimento | Misura o dichiarazione | Inferenza consentita |
| --- | --- | --- |
| ESMA, 2018 | [VERIFICATO: analisi delle autorità UE riportata da ESMA] **74–89%** dei conti retail CFD tendeva a perdere nelle giurisdizioni studiate. [ESMA §2.1](https://www.esma.europa.eu/sites/default/files/library/esma35-43-1000_additional_information_on_the_agreed_product_intervention_measures_relating_to_contracts_for_differences_and_binary_options.pdf) | [DEDOTTO] Forte frequenza di perdita per CFD retail in quel contesto. Unità = conto. Esito = perdita. |
| Brasile, futures azionari | [VERIFICATO: Chague, De-Losso e Giovannetti, paper] **97%** in perdita fra i nuovi day trader che persistevano almeno 300 giorni nel campione studiato. [Paper degli autori](https://repositorio.fgv.br/bitstreams/0f00dd78-6909-4f91-84d5-aef8803e6436/download) | [DEDOTTO] L'allenamento prolungato non rende ragionevole presumere un guadagno. Il campione è condizionato alla persistenza e riguarda futures azionari brasiliani. |
| Taiwan, azioni | [VERIFICATO: Barber, Lee, Liu e Odean, 2014, abstract] **Meno dell'1%** degli operatori di day trading mostrava rendimenti anomali positivi netti prevedibili e affidabili, su dati 1992–2006. [Articolo originale](https://doi.org/10.1016/j.finmar.2013.05.006) | [DEDOTTO] Esistono eccezioni e il test di persistenza è più stringente del semplice saldo positivo. |
| FTMO, intervista ai fondatori | [VERIFICATO: risposta di Otakar Šuffner ripubblicata da FTMO] **8–10%** dichiarato per il superamento della Challenge. [Intervista](https://ftmo.com/en/blog/forbes-the-ftmo-cover-story/) | [NON VERIFICATO] Denominatore per tentativi o persone, finestra, prodotti, ripetizioni, passaggio di entrambe le fasi, permanenza e premi. Non c'è una stima auditabile per l'utente o per XAUUSD in queste fonti. |

[DEDOTTO] Le frequenze di base rendono poco plausibile assumere come scenario ordinario 1–2% mensile persistente dopo costi. Non permettono di assegnare una probabilità al progetto. Per stimarla servono dati campionati con le regole, le condizioni operative e i costi effettivi. La domanda quantitativa è quanto capitale simulato rende la strategia sotto condizioni e incertezza dichiarate e con quale conformità. I risultati di ricerca e l'eventuale decisione economica restano passi distinti.


## 5. Bias e qualità delle revisioni

[VERIFICATO: `H-002-REVISIONI.md:190–208,243–272`, rapporti Gemini sui rilievi R-09 e R7] Il miglior argomento a favore del processo è che una replica distinta ha fatto emergere D1 e D2 sul simulatore, e a R10 le sonde di integrazione hanno sollevato P1–P8 dopo test e mutanti verdi. Le correzioni di Claude sono registrate e si possono riesaminare. [DEDOTTO] La parità su mercati inventati misura accordo sul comportamento in quei casi. Se la specifica ha un errore, due implementazioni fedeli possono ripeterlo. Le 30 configurazioni del simulatore e le tre famiglie sintetiche dell'esecutore valutano perimetri diversi. Il DGS-03 offre un controesempio alla conclusione «replica uguale, quindi regola eseguibile».

| Bias da controllare | Indizio e controllo proposto |
| --- | --- |
| Conferma, autorità e giudizio sul proprio lavoro | [VERIFICATO: `H-002-REVISIONI.md:53,100,122,117,267`] Invii errati hanno tolto i test a DeepSeek in due giri. Claude ha inoltre corretto casi attesi propri e sintetizzato male SR₀. [OPINIONE] Revisore e autore consegnano esito e caso riproducibile separati. Una correzione autoapprovata resta in verifica. Anche i rilievi DGS vanno cercati in negativo da DeepSeek. Registrare i falsi allarmi come tali. |
| Sguardo al futuro | [VERIFICATO: scheda H-002 e DGS-03] La chiusura anteriore alle 16:30 dipende da quotazioni successive. Il registro documenta anche errori storici in mediana e test sullo spread. [OPINIONE] Confrontare prefissi identici con code diverse per ogni decisione già maturata. Verificare orari operativi, mercati correlati, disponibilità delle notizie e timestamp di fine candela. |
| Prove multiple, selezione e sentieri che si biforcano | [VERIFICATO: `REGISTRO-ESPLORAZIONI.md:3–18`, risultati E-002:84–88, `H-002-REVISIONI.md:25–29,49`] Si sono già guardati più modi, sessioni, timeframe, target e comparatori. Le scelte di H-002 hanno visto E-001/E-002. Una lettura benevola è chiamare descrittive le analisi senza selezione di rendimenti. [DEDOTTO] Una tabella descrittiva che influenza il filtro o il prossimo candidato è comunque un canale di selezione. [OPINIONE] Ricostruire cosa è stato calcolato, visto e usato. Predefinire come registrare ogni variante e come dichiarare selezione non ricostruibile. |
| Sovradattamento e ipotesi dopo i risultati | [VERIFICATO: `H-002-ORB-v3.md:13–16,49–55,115–156`] Soglie aggressive o prudenti sono motivate, con contaminazione dichiarata sullo sviluppo. [DEDOTTO] Fissare bene un'ipotesi ora non ripristina la cecità di ciò che si è già visto. [OPINIONE] I criteri puntuali sono ipotesi operative. Vietare ricalibrazioni sullo storico chiuso, scrivere budget e regola di chiusura della famiglia prima dello screening. |
| Sopravvivenza e denominatori | [VERIFICATO: `H-002-REVISIONI.md:253–266`, `criteri.py:102–105,146–158`] R10 documenta il passaggio a tutti gli anni della finestra. [CALCOLATO] Sei anni positivi su dieci con trade fanno 60%. Sei su diciannove fanno 31,6%. [DEDOTTO] La stessa distorsione può colpire giorni con cache vuota, trade saltati, conti demo chiusi o broker abbandonati. [OPINIONE] Rilevare dall'inizio tutti i giorni, tentativi, account e cause di mancata osservazione. Nelle ricerche future su azioni, includere universo e delisting point-in-time. |
| Costi sommersi, ancoraggio e narrazione | [VERIFICATO: `REGISTRO-DIFETTI.md:63–66`, `QUADERNO-IPOTESI.md:10–19`] Il progetto ha iterato a lungo su H-002 e il quaderno usa il filtro di 300 trade come riferimento generale. [DEDOTTO] L'investimento nel simulatore non rende più probabile l'edge. «Londra si muove» o una storia di coperture non stabiliscono segno, durata e profitto dopo costi. [OPINIONE] Una candidata bocciata si chiude come previsto. Ogni nuova idea ha una predizione falsificabile e un comparatore. Trattare 300 trade, 100 trade demo, 1–2% e il conto da 100.000 come soglie o obiettivi espliciti, con origine e conseguenze. |
| Frequenze di base ignorate | [VERIFICATO: §4.3] Gli studi di perdita, la dichiarazione del fondatore e le simulazioni della roadmap hanno denominatori diversi. [OPINIONE] Riportare sempre unità, periodo, popolazione e fase. Un risultato sintetico o il caso di un trader finanziato non autorizzano un giudizio sull'utente. |

## 6. Viabilità e percorsi alternativi

[DEDOTTO] Il caso favorevole è una pipeline già eseguibile in parte, con due centri di ricerca, un criterio di bocciatura e un blocco storico più lungo dello sviluppo. Il caso contrario è l'assenza di evidenza di un edge netto trasferibile per l'utente, mentre i tempi e i costi del test ricadono su un solo processo e su un solo conto umano. Lo stato del codice e la probabilità di rendimento sono domande diverse. Le alternative dipendono da obiettivo, scala temporale, mercato ed evidenza disponibile.

| Percorso | Classificazione e costo N | Che cosa deve dimostrare o cambiare |
| --- | --- | --- |
| Prima prova XAUUSD intraday con H-002, poi decidere | [OPINIONE] **Applicabile dopo** DGS-01–05, data e regole DA-19/20/26 ratificate. Due varianti base già dichiarate. Conto letterale del primo giro, 12 configurazioni prima dello stress e 14 con entrambi gli stress, più il pregresso rilevante. | [DEDOTTO] Misura direzione, esecuzione e limiti del metodo sul mercato scelto. Se non passa lo screening si archivia l'esito, senza aprire lo storico. Se supera la verifica resta la demo futura. |
| Ridurre il turnover restando intraday, oppure Q-01 | [OPINIONE] **Applicabile dopo** la decisione su H-002, una fonte primaria, costi/protocolli e disegno di potenza. +1 per un singolo orario fissato, più i controlli di robustezza e stress dichiarati che cambiano la regola. | [VERIFICATO: Baltussen et al., tabella 1 e appendice] Il quaderno dice che non ha trovato studi diretti sul COMEX. Il paper già citato include il future GC e l'orario 08:20–13:30. [DEDOTTO] Il risultato aggregato non dà alla scheda Q-01 un edge CFD XAUUSD netto. Verificare l'esito per GC e il trasferimento atteso prima di iscrivere la prova. [Articolo originale](https://pure.eur.nl/ws/portalfiles/portal/58145484/1_s2.0_S0304405X21001598_main.pdf) |
| Eventi macro e aste, Q-03/Q-04/Q-05 | [OPINIONE] Q-03 **non applicabile al metodo così scritta**. L'ingresso alle 08:35 cade cinque minuti dopo il dato, nella finestra vietata da P-08. Q-04 e Q-05 **applicabili dopo** convalida di dati e calendario. +1 base per ogni idea approvata e +1 per ogni ulteriore configurazione dichiarata. | [VERIFICATO: `QUADERNO-IPOTESI.md:81–134` e `regole_personali.toml:87–95`] Q-04 richiede timestamp e seconda serie azionaria. Q-05 deve trattare il cambio di meccanismo del 20/03/2015 già noto prima del test e la sovrapposizione oraria con H-002. Una reazione a notizie o fixing da sola non sostiene un ingresso economicamente sfruttabile. [LBMA](https://www.lbma.org.uk/prices-and-data/lbma-gold-price/lbma-gold-price) |
| Altre regole XAUUSD, Q-06/Q-07/Q-09, Fibonacci e order block | [OPINIONE] **Applicabile dopo** una motivazione verificabile, una definizione meccanica completa e il criterio di potenza della singola famiglia. +1 per configurazione dichiarata, e non si selezionano più orari dopo averne visto gli esiti. | [DEDOTTO] Famiglie simili a H-002 aggiungono poca evidenza indipendente. Un volume del singolo feed non è volume consolidato. Tenere nel quaderno le idee meno motivate e lasciare Fibonacci sospeso come indica la nota a riga 197. |
| Swing, tendenza multi-day e stagionalità Q-02/Q-08/Q-10 | [OPINIONE] **Non applicabile al metodo nelle forme proposte**, per incompatibilità con weekend chiuso o overnight in sospeso. +1 per una futura specifica dichiarata coerente. **Da scartare** Q-10 per la prima fase, N nuovo = 0. | [VERIFICATO: `QUADERNO-IPOTESI.md:60–79,165–172,184–192`, DA-29] Ridisegnare la gestione del venerdì, swap, gap e rischio di fase solo su decisione dell'utente. Con poche operazioni usare un'unità di osservazione e storia adeguate. Per Q-10 il quaderno prevede circa tre operazioni nello sviluppo. Non convertire mesi o finestre sovrapposte in osservazioni indipendenti. |
| Altro mercato CFD, un mercato alla volta | [OPINIONE] **Applicabile dopo** primo ciclo dell'oro, DA-27/28, storico compatibile, costi e licenza. +1 per coppia regola–mercato dichiarata. | [DEDOTTO] Valutare EURUSD ed eventualmente un cross senza USD per finire prima il confronto fonti, indice liquido per una sessione definita, XAGUSD come prova di trasferimento. DAX/energia richiedono sessioni e roll; cripto presenta calendario 24/7 e storico diverso. Scegliere prima un mercato. Non usare risultati o grafici di mercati correlati nello stesso blocco riservato. `PIANO-DIVERSIFICAZIONE.md:13–42`. |
| Future, ETF o altri strumenti come nuova domanda | [OPINIONE] **Applicabile dopo** mandato, accesso legittimo ai dati e verifica del costo. +1 per specifica e strumento dichiarati. | [DEDOTTO] Possono dare dati e processi esecutivi diversi, con costi, roll, orari e accesso propri. Un future dell'oro può essere un controllo di trasferibilità per l'ipotesi CFD. Per un progetto separato di studio a orizzonte lungo servono obiettivi e misura di rischio propri. Il risultato non si trasferisce in automatico a un prodotto FTMO. |
| Più strategie o apprendimento automatico | [OPINIONE] **Applicabile dopo** evidenza sulle regole singole, con vincoli su P-06, correlazione, code e conteggio. +1 per ciascuna regola nuova, +1 per ogni arbitro o allocazione selezionabile dichiarata. **Da scartare** la ricerca massiva nell'attuale finestra, N nuovo = 0. | [DEDOTTO] Ripetere il segnale su più strumenti o conti non offre un campione indipendente. Una combinazione di strategie senza edge individuale può ridurre la volatilità. Le correlazioni da sole non creano rendimento atteso. Con vincoli operativi, costi e selezione dei segnali, si misura la media netta del percorso aggregato. |
| Guardian e journal come strumento di disciplina | [OPINIONE] **Applicabile ora** in demo per raccolta locale e addestramento al processo, previa riconciliazione per usare i numeri G0 nelle decisioni. N = 0 per questa funzione. | [OPINIONE] Giudicare rispetto dei limiti, completezza degli eventi, frequenza di omissioni e qualità delle convalide. Si può ottenere un beneficio di processo anche se nessuna strategia passa. L'effetto comportamentale personale si misura localmente e resta separato dal vantaggio sui prezzi. |
| Pausa, obiettivo di ricerca o chiusura del percorso prop | [OPINIONE] **Applicabile ora**, N = 0. | [DEDOTTO] Se dati e costi non rendono fattibile il test, se l'incubazione necessaria eccede il tempo accettato o se la coorte fissata non produce candidate, si può chiudere la linea prop, estendere l'attesa o mantenere il progetto come formazione e disciplina. Ciascuna scelta conserva gli esiti negativi e le regole dell'utente. |

[OPINIONE] Verdetto finale di viabilità: **vale la pena completare un primo ciclo di ricerca correttamente vincolato. Non c'è oggi base per una sfida a pagamento o per aspettarsi 1–2% mensile.** La via più informativa è risolvere dati e controllo a lettura unica, chiudere il problema causale e decidere il conteggio prima dello screening. Una candidata che non passa il criterio fissato si chiude. Superare la verifica storica ammette la candidata alla demo. Il giudizio economico cambia dopo evidenza prospettica sulla tenuta netta, sulla fedeltà di esecuzione e sul rispetto delle regole personali. La fattibilità economica del prodotto si valuta solo dopo queste evidenze, con possibilità esplicita di fermarsi.

## 7. Proposte per l'utente e richieste di lavoro

[DEDOTTO] N qui è il costo per il registro e il DSR del progetto. Eseguire una stessa specifica con un oracolo diverso o sulla stessa coorte come replica tecnica non crea una nuova scelta strategica. Se il risultato serve a scegliere un altro periodo, orario, parametro, strumento o modello operativo, la configurazione è una nuova prova. I casi sintetici di collaudo vanno registrati come test, con dati inventati dichiarati.

| Ordine | Proposta | Classe e costo N | Criterio di accettazione |
| --- | --- | --- | --- |
| 1 | Versione unica del pacchetto, identità Git e export redatto | [OPINIONE] **Applicabile ora**. N = 0. | Impronta del pacchetto ottenuta su canale separato, elenco di aggiunte al commit con provenienza, scansione locale anche degli archivi interni. Zero occorrenze dei dati personali vietati nel pacchetto per revisori. |
| 2 | Approvare e tracciare DA-19/20/26 e i confini di ogni gate | [OPINIONE] **Applicabile ora** come proposta. N = 0 per formalizzare. N aumenta secondo le configurazioni dichiarate che entrano nel programma. | Un'unica decisione dell'utente per periodo, spesa N, criteri di promozione, definizione del campione e condizioni di consumo. Ogni variante e prova fallita ricostruibile. |
| 3 | Legare impegni, input M1, codice e apertura di coorte | [OPINIONE] **Applicabile ora** su dati inventati. N = 0. | A parità di input la verifica è riproducibile. Input BID o ASK non corrispondente all'impegno, date discordanti o versione non autorizzata rendono l'esito inammissibile. In caso di interruzione il registro dà uno stato univoco per la coorte. |
| 4 | Chiudere causalità e allineamento della scheda H-002 | [OPINIONE] **Applicabile ora** come correzione prima del primo sigillo, N nuovo = 0 se si converge su una sola regola per ciascuna variante già dichiarata, senza risultati di H-002 usati per scegliere. Il numero dichiarato del giro resta quello ratificato. +1 per ogni alternativa aggiunta come prova o per nuova versione sostanziale dopo il sigillo. | Il caso d'oro è compatibile con un ordine eseguibile. Test su due traiettorie con stesso prefisso e code diverse. Risultati e motivi di esclusione compatibili tra specifica, implementazione e replica. |
| 5 | Calendario notizie e replica delle regole effettive di demo | [OPINIONE] **Applicabile dopo** fonte con timestamp, scelta dell'utente e riconciliazione DA-25. N = 0 per acquisizione e costo. +1 per ciascuna variante della regola effettiva, fino a +2 se si aggiunge il filtro a entrambe le basi attuali. | P-08 rispettata e segnali mancati registrati anche in demo. Costi e restrizioni si confrontano localmente, tolleranze note prima. |
| 6 | Rendere l'arresto demo usabile nel calendario reale | [OPINIONE] **Applicabile dopo** frequenza, potenza e dispersione misurate, N = 0 come metodologia fissata prima di osservare gli esiti. Configurazioni concorrenti provate e scelte a posteriori si contano. | Piano per fedeltà operativa, limite di rischio e inferenza distinti. Potenza dichiarata al tetto e test tarato su dipendenza e costo della decisione. Stato «inconclusivo» al tetto. |
| 7 | Q-01 dopo il primo ciclo, poi un mercato aggiuntivo | [OPINIONE] **Applicabile dopo** i prerequisiti del §6. +1 per candidata e +1 per prova su ogni ulteriore mercato, più varianti dichiarate. | Ipotesi di trasferimento falsificabile, costi misurati, stessa cronologia protetta e nuovi dati di conferma se la verifica è già consumata. |
| 8 | Riutilizzare il blocco aperto o cercare centinaia di varianti | [OPINIONE] **Non applicabile al metodo** per una promozione successiva; **da scartare** in questo giro. N effettivo aggiunto = 0 se non si esegue. | Il registro deve poter attestare che lo storico già aperto genera al più analisi esplorative. |

**RICHIESTA A CLAUDE**

1. [OPINIONE] Preparare una scheda di stato di una pagina con commit, differenze da `main`, versione della specifica, coppia implementazione/replica e decisioni ancora aperte. Correggere i rimandi obsoleti elencati al §0.1 con note datate e marcare separatamente proposta e decisione. **Accettazione:** ogni stato associa una voce del registro o una prova, e un nuovo revisore identifica senza ambiguità cosa aprire.
2. [OPINIONE] Proporre integrazione dei vincoli DGS-01/02/04/05, con revisione esplicita dell'utente su N e apertura. Riconciliare costi e copertura sul Mac con soli esiti aggregati autorizzati, e preparare il materiale per il giro tecnico sul DGS-03. **Accettazione:** su dati inventati, versione e confini stabili, disaccordo onesto sull'unità di N ove resti, due input modificati uno per lato respinti rispetto all'impegno, e una prova di interruzione che indica lo stato della coorte. Per DGS-03, il rimedio va tradotto in una specifica causale che l'utente può ratificare prima della correzione.
3. [OPINIONE] Preparare il prossimo export per revisori con redazione dei testi e degli eventuali archivi interni. **Accettazione:** attestazione locale su percorsi e conteggio del manifest e nessun dato personale vietato. Nessun rapporto storico viene riscritto per correggere l'attribuzione. La redazione si applica alla copia di consegna.

**RICHIESTA A GEMINI**

1. [OPINIONE] Verificare DGS-01–04 sulla stessa versione e da specifiche fissate, con prova su input inventati. Preparare il controllo prima di vedere le nuove soluzioni di Claude. **Accettazione:** esito per ID, file e righe, una prova che smentirebbe ogni rilievo se il controllo regge e l'effetto su sigillo, campione e N. Per il DGS-03, due code con prefisso comune confrontate al tempo della decisione.
2. [OPINIONE] Presentare il caso migliore per escludere da N robustezze dichiarate e la taratura conseguente, poi testare il caso contrario. **Accettazione:** esempi dichiarati con N, V e Sharpe, separazione tra veto e selezione, significato del dato sotto dipendenza e raccomandazione con conseguenze. La scelta resta dell'utente.

## 8. Autocritica

1. [NON VERIFICATO] L’attribuzione Git, lo stato di `main`, sequenza dei commit rossi, cecità storica, hash dei dataset sul Mac, broker ed effettiva apertura demo restano senza riscontro diretto. I rapporti interni possono descrivere come aperto un problema corretto dopo il pacchetto o attribuire a un ramo informazioni superate.
2. [DEDOTTO] DGS-03 è certo come difetto di causalità nella specifica scritta. Frequenza, segno e impatto sui verdetti sono sconosciuti. La classificazione critica segue la definizione del progetto per lo sguardo al futuro. R11 deve verificare implementazione e correzione con un caso indipendente.
3. [DEDOTTO] La lettura del costo N è prudente e rispetta il testo del mandato. Un veto realmente non selezionabile può ridurre false promozioni. Includerlo come una prova indipendente rischia di gonfiare il minimo richiesto. Serve distinguere la regola di registrazione dell'utente dalla taratura inferenziale, anziché scegliere il conteggio più favorevole o più punitivo.
4. [NON VERIFICATO] Le distribuzioni di trade e comportamenti personali sono sconosciute. I calcoli di potenza, moto browniano e Wald sono condizionati a ipotesi. L'AR(1) è un controesempio, non una stima della dipendenza di H-002. Le fonti FTMO sono pagine pubbliche alla lettura, non una revisione di contratto, specifiche e qualità di esecuzione del conto dell'utente.
5. [OPINIONE] Potrei dare troppo peso ai casi limite rispetto alla loro frequenza operativa, perché qui posso dimostrare che sono possibili e non misurare quanto spesso accadano. Potrei anche condividere i presupposti degli altri modelli. Le prove eseguibili, il riesame DeepSeek e una smentita dal Mac devono avere più peso del mio verdetto. Ho scelto di limitare l'esecuzione a test selezionati e calcoli. La revisione tecnica di H-002, i suoi test e i suoi mutanti restano al giro assegnato.

## 9. Domande all'utente

1. [NON VERIFICATO] Per DA-25, il demo FP Markets MT5 Raw è già aperto e riconciliato localmente, oppure esiste soltanto la scelta del broker? Basta indicare lo stato.
2. [NON VERIFICATO] Quali blocchi BID/ASK M1 sono già completi e controllati sul Mac e quali date UTC intendi fissare per la verifica DA-26? Serve lo stato aggregato, senza quotazioni o nonce.
3. [OPINIONE] Per DA-19, confermi che i 6 + 4 controlli di robustezza e i due stress entrino nel N globale, oppure vuoi distinguere nel registro i veti predefiniti dalle varianti selezionabili? La scelta cambia la soglia. Va registrata prima dell'esecuzione.
4. [OPINIONE] Preferisci una sola apertura per la coorte storica definita prima, con nuove candidate valutate sul futuro, o vuoi riservare ora un secondo blocco intatto? La seconda scelta riduce il campione del primo giro.
5. [NON VERIFICATO] Quando dici 1–2% al mese, intendi media su un orizzonte lungo, frequenza dei mesi sopra soglia o premi incassati? Quale durata massima è ragionevole per il demo prima di dichiarare l'esito inconclusivo?
6. [NON VERIFICATO] La prima demo della candidata sarà manuale con P-08 e P-12, o vuoi valutare più avanti un percorso di esecuzione in demo autorizzato separatamente? La risposta decide quale replica di esecuzione preparare. Quale finestra settimanale pensi di poter dedicare alla demo?

### Appendice A. Inventario di lettura per percorso

[VERIFICATO: tracciato delle letture e incrocio con MANIFEST.tsv] I percorsi sono relativi alla radice dello ZIP. Le copie allegate identiche non sono contate di nuovo.

**Letti per intero (35)**

- `brain/CONTINUITA.md`
- `brain/README.md`
- `brain/architettura/ARCHITETTURA.md`
- `brain/collaborazione/LOCK.md`
- `brain/collaborazione/PROTOCOLLO-OPERATIVO.md`
- `brain/collaborazione/da-claude/ERRATA-V3_3/ERRATA_V3_3.md`
- `brain/collaborazione/da-claude/direttore-sicurezza/0-GUIDA-PER-L-UTENTE.md`
- `brain/collaborazione/da-claude/direttore-sicurezza/1-ISTRUZIONI-DEL-PROGETTO.md`
- `brain/collaborazione/da-claude/direttore-sicurezza/2-MESSAGGIO-1-MANDATO.md`
- `brain/collaborazione/da-claude/direttore-sicurezza/INDICE-PER-IL-DGS.md`
- `brain/dati/README.md`
- `brain/dati/operativo/trial_registry_xauusd.json`
- `brain/dati/reali/README.md`
- `brain/dati/reali/TEMPLATE_RICONCILIAZIONE_DA25.toml`
- `brain/dati/reali/demo_broker_mt5_50k_xauusd.toml`
- `brain/governance/DECISIONI-APERTE.md`
- `brain/governance/DECISIONI.md`
- `brain/governance/MODELLO-EPISTEMICO.md`
- `brain/governance/PIANO-DIVERSIFICAZIONE.md`
- `brain/governance/STANDARD.md`
- `brain/guardian/LEGGIMI.md`
- `brain/guardian/journal/LEGGIMI.md`
- `brain/guardian/regole/LEGGIMI.md`
- `brain/laboratorio/REGISTRO-DIFETTI.md`
- `brain/laboratorio/esecuzione/caricatore.py`
- `brain/laboratorio/ipotesi/H-001-range-1m-BOZZA.md`
- `brain/laboratorio/ipotesi/H-002-ORB-v3.md`
- `brain/laboratorio/ipotesi/H-002-REVISIONI.md`
- `brain/laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md`
- `brain/laboratorio/ipotesi/QUADERNO-IPOTESI.md`
- `brain/laboratorio/studi/REGISTRO-ESPLORAZIONI.md`
- `brain/laboratorio/studi/risultati/studio_range_2023-11-15_2026-11-12.md`
- `brain/laboratorio/studi/simulazione_sprt.py`
- `brain/laboratorio/trial_registry.json`
- `brain/piano/PROGETTO-GENERALE-20261115.md`

**Letti in parte (34)**

- `brain/audit/AUDIT-ARCH-20261111/RELAZIONE-AUDIT.md` — indice e passaggi su dati, rischio, decisioni.
- `brain/collaborazione/da-claude/ESITI.md` — risposte su partizione 70/30 e Gate 1.
- `brain/collaborazione/da-gemini/G-20261113-01-revisione-dati-e-diversificazione.md` — passaggio sul 70/30.
- `brain/collaborazione/da-gemini/G-20261113-03-revisione-fix-dsr-partizione.md` — G3-05 e G3-07.
- `brain/collaborazione/da-gemini/G-20261113-04-chiusura-fix-dsr-partizione.md` — sintesi e G3-05/G3-07/G4-01.
- `brain/collaborazione/da-gemini/G-20261114-01-sprt-ftmo-criteri.md` — 38–109, calibrazione e regole FTMO.
- `brain/collaborazione/da-gemini/G-20261114-02-revisione-H-002.md` — rilievi DSR, esplorazioni e conteggio.
- `brain/collaborazione/da-gemini/G-20261115-R7-esecutore-h002.md` — indice, verdetto e righe sui rilievi R1/R4.
- `brain/dati/pipeline/dukascopy.py` — interfaccia, aggregazione e 253–340.
- `brain/dati/pipeline/partitioning.py` — interfaccia e riferimenti a nonce e impegno.
- `brain/dati/pipeline/partizione_date.py` — 100–194 e dichiarazione del formato.
- `brain/dati/tests/test_dukascopy.py` — import e frammenti sui casi offline.
- `brain/dati/tests/test_partizione_date.py` — import e frammenti su date, hash e nonce.
- `brain/dati/tests/test_pipeline.py` — import e riferimenti.
- `brain/governance/REGISTRO-CONOSCENZE.md` — passaggi sullo stato delle verifiche.
- `brain/governance/REGISTRO-MODIFICHE.md` — 344–397 e riscontri sul 70/30.
- `brain/guardian/regole/prop_firm_ftmo.toml` — origine, dettagli parziali, limiti e FAQ.
- `brain/guardian/regole/regole_personali.toml` — flag di conferma, soglie e campi selezionati.
- `brain/guardian/test/test_compatibilita_e_concorrenza.py` — import e frammenti di concorrenza.
- `brain/guardian/test/test_fix_g0_journal.py` — import.
- `brain/guardian/test/test_g0.py` — import.
- `brain/guardian/test/test_journal.py` — import.
- `brain/guardian/test/test_mutanti_g0_journal.py` — import.
- `brain/guardian/test/test_red_team_guardian.py` — import e frammenti di isolamento e concorrenza.
- `brain/laboratorio/backtester/dsr.py` — 167–224 e passaggi su scala e registro.
- `brain/laboratorio/backtester/engine.py` — frammenti su stop, target, esecuzione e gap.
- `brain/laboratorio/esecuzione/criteri.py` — 102–179, criteri di verifica.
- `brain/laboratorio/esecuzione/esegui_h002.py` — 29–121 e 173–251, interfaccia e flusso.
- `brain/laboratorio/esecuzione/sigillo.py` — 73–142 e riferimenti ad hash e registro.
- `brain/laboratorio/studi/risultati/studio_sessioni_2025-11-13_2026-11-12.md` — 1–14 e 128–146.
- `brain/laboratorio/tests/test_backtester.py` — import e riferimenti.
- `brain/laboratorio/tests/test_dsr_scala.py` — import e riferimenti.
- `brain/piano/PIANO-ESPANSIONE.md` — passaggi su stato e sospensione.
- `brain/piano/PIANO-MIGRAZIONE.md` — intestazione di stato e titoli.

**Senza lettura di merito (258)**

L'eventuale verifica di hash, ricerca letterale, invocazione come test o ispezione del contenitore non attribuisce una lettura del contenuto.

```text
.gitignore
README.md
brain/PROMPT-RIPRESA.md
brain/audit/01-DIAGNOSI.md
brain/audit/02-VERIFICA-AFFERMAZIONI.md
brain/audit/03-MATRICE-LACUNE.md
brain/audit/AUDIT-ARCH-20261111/00-CHECKPOINT.md
brain/audit/AUDIT-ARCH-20261111/01-INVENTARIO-E-QUALITA.md
brain/audit/AUDIT-ARCH-20261111/02-INCOERENZE-E-DUPLICAZIONI.md
brain/audit/AUDIT-ARCH-20261111/03-COMPETENZE-QUANT-MANCANTI.md
brain/audit/AUDIT-ARCH-20261111/04-DIPENDENZE.md
brain/audit/AUDIT-ARCH-20261111/05-ARCHITETTURA-SDL-E-GUARDIAN.md
brain/audit/AUDIT-ARCH-20261111/06-FONTI-E-VALIDAZIONE.md
brain/audit/AUDIT-ARCH-20261111/07-PRIORITA-TRE-MESI.md
brain/audit/AUDIT-ARCH-20261111/strumenti/misure_20261111.txt
brain/audit/AUDIT-ARCH-20261111/strumenti/misure_brain.py
brain/bibliografia/BIBLIOGRAFIA.md
brain/collaborazione/DISACCORDI.md
brain/collaborazione/HANDOFF-GEMINI.md
brain/collaborazione/README.md
brain/collaborazione/da-chatgpt/LEGGIMI.md
brain/collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md
brain/collaborazione/da-claude/CONSEGNA_FIX_G0/AUDIT_OSTILE_SU_GEMINI.md
brain/collaborazione/da-claude/CONSEGNA_FIX_G0/MANIFEST.sha256
brain/collaborazione/da-claude/CONSEGNA_FIX_G0/RAPPORTO_FIX_G0.md
brain/collaborazione/da-claude/CONSEGNA_FIX_G0/diff_fix_g0.patch
brain/collaborazione/da-claude/CONSEGNA_FIX_G0/log_test_40_e_mutazioni_24.txt
brain/collaborazione/da-claude/CONTESTAZIONE_TECNICA_CLAUDE_PER_ANTIGRAVITY_V2.md
brain/collaborazione/da-claude/ERRATA-V3_3/MANIFEST.sha256
brain/collaborazione/da-claude/ERRATA-V3_3/mutazioni_v3_3.py
brain/collaborazione/da-claude/ERRATA-V3_3/output/esecuzione_errata.txt
brain/collaborazione/da-claude/ERRATA-V3_3/test_errata_v3_3.py
brain/collaborazione/da-claude/PROMPT-R11-GEMINI-E-CHATGPT.md
brain/collaborazione/da-claude/RICHIESTE-REVISIONE-ESECUTORE-H002.md
brain/collaborazione/da-claude/RICHIESTE.md
brain/collaborazione/da-claude/direttore-sicurezza/3-MESSAGGIO-2-REVISIONE-R11.md
brain/collaborazione/da-claude/direttore-sicurezza/4-PROMPT-DEEPSEEK-CONTROLLO-DEL-DGS.md
brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/AUDIT_OSTILE_SU_CLAUDE.md
brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/MANIFEST.sha256
brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/RAPPORTO_LAB_V2_ZERO_TRUST.md
brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/diff_lab_v2.patch
brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/log_test_e_mutazioni_lab_v2.txt
brain/collaborazione/da-gemini/G-20261113-02-vettori-dsr-e-revisione.md
brain/collaborazione/da-gemini/G-20261114-03-rilettura-H-002-v2.md
brain/collaborazione/da-gemini/G-20261115-01-replica-H-002.md
brain/collaborazione/da-gemini/G-20261115-02-verifica-fix-orb.md
brain/collaborazione/da-gemini/MODELLO-RAPPORTO.md
brain/collaborazione/da-gemini/README.md
brain/collaborazione/da-gemini/consegne/ERRATA_DOSSIER_E_HASH.md
brain/collaborazione/da-gemini/consegne/MANIFEST.sha256
brain/collaborazione/da-gemini/consegne/README.md
brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md
brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md
brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_V3_3_PACKAGE.zip
brain/collaborazione/da-gemini/prove_r7_esecutore.py
brain/collaborazione/da-gemini/replica_criteri_h002.py
brain/collaborazione/da-gemini/replica_h002/__init__.py
brain/collaborazione/da-gemini/replica_h002/confronto.py
brain/collaborazione/da-gemini/replica_h002/genera_dati.py
brain/collaborazione/da-gemini/replica_h002/replica.py
brain/collaborazione/da-gemini/replica_h002/test_replica.py
brain/collaborazione/fondamenti/README.md
brain/collaborazione/pacchetto-per-gemini/01-REVISIONE-L2.4-L2.6.md
brain/collaborazione/pacchetto-per-gemini/02-ARCHITETTURA-E-REGISTRI.md
brain/collaborazione/pacchetto-per-gemini/03-CONFRONTO-QUANTITATIVO.md
brain/collaborazione/pacchetto-per-gemini/MANIFEST.sha256
brain/collaborazione/pacchetto-per-gemini/README.md
brain/collaborazione/revisione-materiali-gemini/CHECKLIST-REVISIONE.md
brain/collaborazione/revisione-materiali-gemini/MODELLO-RAPPORTO-REVISIONE.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/CLAUDE_SECOND_REVIEW_ANTIGRAVITY_V2.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/ERRATA.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c10_test_aggiuntivi_mutanti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c10_test_aggiuntivi_originale.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c11_str002_aritmetica.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c1_esatto_vs_gemini.json
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c2_semi_multipli.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c3_v1_v2_e_orizzonte.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c4_markov.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c4b_markov_esatto.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c5_mae_browniano.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c6_impatto_mae_crn.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c7_pareto_slippage.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c8_kelly_barriera.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/c9_mutazioni.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/hash_ricevuti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/run_simulations_v2_stdout.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/simulations_v2_raw_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/output/verifica_manifest.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c11_str002_aritmetica.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c1_esatto_challenge.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c2_semi_multipli.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c3_v1_v2_e_orizzonte.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c4_markov.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c4b_markov_esatto.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c5_mae_browniano.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c6_impatto_mae_crn.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c7_pareto_slippage.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c8_kelly_barriera.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/c9_mutazioni.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche/test_aggiuntivi_claude.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/CLAUDE_FINAL_REVIEW_V3.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/PROPOSTE-CORREZIONE-V3.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/hash_v3_ricevuti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/run_simulations_v3_stdout.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/simulations_v3_raw_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/test_v3.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/v3_a_esatto.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/v3_b_crn_mae.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/v3_d_slippage.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/v3_f_kelly_wilson.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/output/verify_17_punti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/verifiche/v3_a_esatto.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/verifiche/v3_b_crn_mae.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/verifiche/v3_d_slippage.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/verifiche/v3_f_kelly_wilson.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/CLAUDE_FINAL_REVIEW_V3_1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/PROPOSTE-CORREZIONE-V3_1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/hash_v31_ricevuti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/prop_simulations_raw_v1_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/run_simulations_v31_stdout.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/run_v1_stdout.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/simulations_v3_1_raw_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/test_v31.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/v31_a_esatto_e_mae.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/v31_c_kelly.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/v31_d_mutazioni.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/output/v31_e_v1_archivio.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/verifiche/v31_a_esatto_e_mae.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/verifiche/v31_c_kelly.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/verifiche/v31_d_mutazioni.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/verifiche/v31_e_v1_archivio.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/CLAUDE_CORRECTION_PROPOSALS_V3_2.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/CLAUDE_FINAL_REVIEW_V3_2.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/CONFRONTO_AFFERMAZIONI_V3_2.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/REGISTRO_VERIFICHE_V3_2.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/hash_v32_ricevuti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/simulations_v3_2_raw_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/test_proposti_claude_v32.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_a_esatto.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_b_robustezza_test.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_c_kelly_q08_crn.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_d_mutazioni.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_e_v1_leggimi.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_runner.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/output/v32_test_suite.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/verifiche/test_proposti_claude_v32.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/verifiche/v32_a_esatto.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/verifiche/v32_b_robustezza_test.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/verifiche/v32_c_kelly_q08_crn.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/verifiche/v32_d_mutazioni.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/CLAUDE_CORRECTION_PROPOSALS_V3_3.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/CLAUDE_FINAL_REVIEW_V3_3.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/hash_v33_ricevuti.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/simulations_v3_3_raw_RIPRODOTTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/test_proposti_claude_v33.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_a_esatto.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_c_kelly_q08_crn.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_d_mutazioni.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_e_v1_leggimi.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_f_precisione.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_runner.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/output/v33_test_suite.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/verifiche/test_proposti_claude_v33.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/verifiche/v33_a_esatto.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/verifiche/v33_c_kelly_q08_crn.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/verifiche/v33_d_mutazioni.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/verifiche/v33_f_precisione.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/MANIFEST_REVISIONE_CLAUDE.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/PACCHETTO_AUDIT_ARCHITETTURA_V2_PER_CHAT.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/PACCHETTO_AUDIT_ARCHITETTURA_V2_PER_CHAT.zip
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/output/integrita_pacchetto.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/output/potenza_campione.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/output/verifica_fonti_web.txt
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/verifiche/potenza_campione.py
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/CLAUDE_EVALUATION_OF_GEMINI_COUNTERCHECK_V1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/CLAUDE_RISPOSTA_ALLA_REVISIONE_ESTERNA_V1.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/ISTRUZIONI_PER_REVISORE_ESTERNO.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/LEGGIMI.md
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/MANIFEST_PACCHETTO.sha256
brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md
brain/collaborazione/revisione-materiali-gemini/README.md
brain/collaborazione/revisione-materiali-gemini/strumenti/riferimento_rovina.py
brain/dati/RICHIESTA-DATI-0.17.md
brain/dati/operativo/journal_broker_mt5_50k/.gitignore
brain/dati/operativo/journal_broker_mt5_50k/LEGGIMI.md
brain/dati/pipeline/__init__.py
brain/dati/pipeline/ingestion.py
brain/dati/pipeline/models.py
brain/dati/riferimenti/uk_bank_holidays.json
brain/dati/simulati/README.md
brain/dati/tests/mutazioni_dsr_partizione.py
brain/glossario/DOMANDE-APERTE.md
brain/glossario/GLOSSARIO.md
brain/guardian/esempi/situazione_esempio.toml
brain/guardian/g0/__init__.py
brain/guardian/g0/_toml.py
brain/guardian/g0/limiti.py
brain/guardian/g0/scheda.py
brain/guardian/g0/strumenti.py
brain/guardian/g0/valori.py
brain/guardian/journal/__init__.py
brain/guardian/journal/dati/.gitignore
brain/guardian/journal/indicatori.py
brain/guardian/journal/journal.py
brain/guardian/regole/fonti/FTMO_REGOLE_ESTRATTO_20261112.txt
brain/guardian/test/mutazioni_g0_journal.py
brain/laboratorio/backtester/__init__.py
brain/laboratorio/backtester/events.py
brain/laboratorio/backtester/portfolio.py
brain/laboratorio/esecuzione/__init__.py
brain/laboratorio/esecuzione/sintetico.py
brain/laboratorio/ipotesi/H-002-ORB-BOZZA.md
brain/laboratorio/ipotesi/H-002-ORB-v2.md
brain/laboratorio/simulatori/__init__.py
brain/laboratorio/simulatori/orb_londra.py
brain/laboratorio/studi/__init__.py
brain/laboratorio/studi/studio_range.py
brain/laboratorio/studi/studio_sessioni.py
brain/laboratorio/tests/mutazioni_esecuzione.py
brain/laboratorio/tests/mutazioni_lab.py
brain/laboratorio/tests/mutazioni_orb.py
brain/laboratorio/tests/test_anti_frode_statico.py
brain/laboratorio/tests/test_esecuzione.py
brain/laboratorio/tests/test_esegui_h002.py
brain/laboratorio/tests/test_orb_londra.py
brain/laboratorio/tests/test_studio_range.py
brain/laboratorio/tests/test_studio_sessioni.py
brain/laboratorio/tradingview/tb_sessioni.pine
brain/mappa/DIPENDENZE.md
brain/mappa/MAPPA-COMPETENZE.md
brain/moduli/m02-macro/L2.1-banche-centrali-e-strumenti.md
brain/moduli/m02-macro/L2.2-aspettative-e-sorprese.md
brain/moduli/m02-macro/L2.3-trasmissione-ai-mercati.md
brain/moduli/m02-macro/L2.4-tassi-reali-e-inflazione-attesa.md
brain/moduli/m02-macro/L2.5-bilancio-banca-centrale-qe-qt.md
brain/moduli/m02-macro/L2.6-fed-bce-boj-boe.md
brain/moduli/m02-macro/PROTOCOLLO-ANALISI-MOVIMENTO.md
brain/moduli/m02-macro/README.md
brain/originale/manuale-v1.html
brain/originale/manuale-v1.txt
brain/strumenti/riproduci_017.py
brain/strumenti/sorpresa_monetaria.py
brain/strumenti/tassi_reali.py
brain/strumenti/verifica_m0.py
```

### Appendice B. Ricalcoli statisticamente riproducibili

[VERIFICATO: calcoli eseguiti con Python 3.12.14, SciPy 1.17.0 e NumPy 2.3.5] La cella seguente riunisce in un solo comando i calcoli della §4 su input teorici o inventati. Dalla radice dell'archivio, usare `python3 -s -B -` con questo testo su standard input. La simulazione originale DA-29 si ripete con il comando nella §4.2.

```python
from math import ceil, exp, log, sqrt
from statistics import NormalDist

import numpy as np
from scipy.stats import nct, t

from brain.laboratorio.backtester.dsr import DSRCalculator

normal = NormalDist()
for n_tests in (1, 2, 12, 14, 20):
    alpha = 0.05 / n_tests
    coefficient = normal.inv_cdf(1 - alpha) + normal.inv_cdf(0.8)
    samples = [ceil((coefficient / d) ** 2)
               for d in (0.05, 0.08, 0.10, 0.15, 0.20)]
    print("N, fabbisogni con normale:", n_tests, samples)
    n = samples[2]
    while nct.sf(t.isf(alpha, n - 1), n - 1, 0.10 * sqrt(n)) < 0.8:
        n += 1
    print("T con t non centrale a delta=0.10:", n)

gamma = 0.5772156649015329
v = 1 / 499
sr0 = sqrt(v) * ((1 - gamma) * normal.inv_cdf(1 - 1 / 4)
                 + gamma * normal.inv_cdf(1 - 1 / (4 * exp(1))))

def dsr_indipendente(sr):
    return normal.cdf((sr - sr0) / sqrt((1 + sr**2 / 2) * v))

low, high = 0.0, 1.0
for _ in range(60):
    middle = (low + high) / 2
    if dsr_indipendente(middle) >= 0.95:
        high = middle
    else:
        low = middle
print("SR0, SR per DSR=.95, riscontro progetto:",
      sr0, high, DSRCalculator.calculate_dsr_analytical(high, 4, 500)[0])

rng = np.random.default_rng(812)
reps = 20_000
upper, lower = log(0.8 / 0.05), log(0.2 / 0.95)
for rho in (0.0, 0.30):
    for mu in (0.0, 0.10):
        noise = rng.standard_normal(reps)
        path = np.zeros(reps)
        decision = np.zeros(reps, dtype=np.int8)
        for n in range(1, 601):
            noise = rho * noise + sqrt(1 - rho**2) * rng.standard_normal(reps)
            path += noise + mu
            ratio = 0.10 * (path - 0.05 * n)
            open_ = decision == 0
            decision[open_ & (ratio >= upper)] = 1
            decision[open_ & (ratio <= lower)] = -1
        print("rho, mu, promuove/ferma/indecisa in percentuale:",
              rho, mu, *[round(100 * np.mean(decision == d), 2) for d in (1, -1, 0)])
```

### Lista di controllo

[VERIFICATO: sezioni 0–9 e appendici] Tutte le sezioni del mandato sono trattate. Lo stato dei gate resta quello indicato nella §2.

- [x] 0 inventario e MANIFEST
- [x] 1 mandato
- [x] 2 roadmap e ingegneria
- [x] 3 limiti
- [x] 4 aspettative
- [x] 5 bias
- [x] 6 viabilità
- [x] 7 proposte
- [x] 8 autocritica
- [x] 9 domande

**AUTOCRITICA** [NON VERIFICATO] I punti aperti riguardano attribuzione Git, dati e operatività sul Mac, calibrazione prospettica e impatto empirico dei rilievi. [OPINIONE] I limiti e i possibili bias del mio giudizio sono esplicitati nella §8.
