# DGS-07 · Protocollo candidato per la scelta e la validazione del metodo IA-02

17 novembre 2026 · Risposta al MESSAGGIO 5 · Solo metodo

**Stato: proposta completa da impegnare prima della lettura dei risultati. Nessuna decisione del titolare viene sostituita da questo documento.** Non ho visto risultati della fase 1, codice, dati di mercato o documenti sigillati. Ho letto il messaggio ricevuto e riletto le sezioni pertinenti del mio DGS-06. Non ho eseguito il pilota né il controllo dei generatori. I soli calcoli svolti qui sono soglie binomiali, limiti di confidenza e costi aritmetici.

## 1. Stato ricevuto e limiti del riscontro

Registro come **dichiarazioni di Claude, non verifiche indipendenti**: candidato `303890b`, correzioni #107/#110/#111, #109 metodologico, mutanti in corso, R15 non conteggiata, contatore 0/2, R16 pronta, implementazione del pilota e correzioni dei relativi test. Il commit del candidato del banco non identifica automaticamente anche l'esatta versione del pilota: occorre l'identificativo proprio del pilota, senza richiedermi accesso al codice.

Il costo riferito è aritmeticamente coerente: 12×3.000×0,13 = **4.680 secondi CPU**, circa 78 minuti, compatibili con «circa 4.700». È un benchmark riferito, non misurato da me. CPU e tempo trascorso non sono intercambiabili in presenza di parallelismo.

«BID pulito» riguarda i controlli descritti. Non certifica intersezione BID/ASK, completezza intraday, idoneità operativa o potenza. ASK è ancora incompleto secondo il messaggio. La cache riferita arriva all'11/11/2023, mentre la riserva dichiarata termina il 31/10/2023: la presenza di quei giorni aggiuntivi non li assegna alla riserva. Nessuna modifica dei confini è proposta qui.

## 2a. Regola preregistrabile: fase 1, margine e fase 2

### 2a.1 Anteriorità e campo della proposta

Il DGS-06 prevedeva un pilota descrittivo e rinviava la selezione al confronto. La richiesta attuale domanda una regola deterministica. **Le regole sotto sono nuove proposte, non decisioni già contenute nel DGS-06.** Non cambiano IA-02, α globale o DA-31. Per essere adottate serve l'impegno del soggetto autorizzato, con le scelte riservate al titolare lasciate a lui.

Prima di sbloccare i risultati, registrare versione e impronta di questo protocollo, versione del pilota, ambiente, serializzazione dei semi, matrice, tabella degli output richiesti e attestazione di chi ha accesso ai risultati. La dichiarazione «nessuno ha ancora visto» viene dal messaggio: io non posso certificarla. Se una persona che può modificare il protocollo ha già visto esiti, conteggi o diagnostiche rivelatrici, la fase 1 resta sviluppo, ma questa regola non va descritta come antecedente alla sua lettura. La fase 2 può comunque essere genuinamente prospettica rispetto alla scelta, se ancora non eseguita/esaminata.

La corsa della fase 1 già avviata non deve essere alterata per farla assomigliare alla proposta. Le nuove valutazioni dei margini si applicano ai suoi limiti grezzi conservati, senza nuove scelte di ritardo, blocco o seme. Se sono disponibili solo conteggi a margine zero, essi **non bastano** a ricostruire gli altri margini. Prima della lettura occorre predisporre il rendiconto sui limiti salvati o una riproduzione identica impegnata e documentata. Non inferire conteggi mancanti dalle percentuali.

Il protocollo conferma o non conferma **un metodo su questa matrice sintetica**, a D=1.000 e a=b=0,025. Non certifica tutti i processi con μ≤0,15, tutte le numerosità, le altre quote o una strategia reale. Non autorizza letture della riserva.

### 2a.2 Candidati e significato del margine

Due metodi base invariati: HAC e bootstrap come implementati secondo il disegno dichiarato. Griglia finita proposta:

**Δ ∈ {0; 0,01; 0,025; 0,05} R.**

Sono otto candidati metodo–margine, tutti valutati sulla stessa fase 1. Questi valori sono una scelta esplorativa proposta, non costanti statistiche validate. Non si aggiungono punti dopo la lettura.

Per limiti grezzi validi L e U:

- promozione statistica del candidato se **L > 0,15+Δ**;
- bocciatura statistica del candidato se **U < 0,15−Δ**;
- altrimenti esito statisticamente inconclusivo.

Equivalentemente si allarga l'intervallo a [L−Δ,U+Δ] e lo si confronta con 0,15. **Propongo il margine simmetrico anche per la bocciatura**, per verificare entrambe le code della futura regola a tre stati. È un'estensione esplicita della richiesta sul margine di promozione. L'uguaglianza a una soglia non produce attraversamento.

Il margine rende più severa l'evidenza richiesta. Non sostituisce la soglia economica IA-02 con una nuova media minima. Riduce sia le false promozioni sia la capacità di riconoscere vantaggi piccoli, e riduce anche la capacità di bocciare. Non va scalato con la SE o modificato tra celle: qui è un numero fisso in R. L'uso a numerosità diverse richiederà un'altra valutazione.

### 2a.3 Conteggi e celle obbligatorie

Per ciascuna replica e metodo, **errore** significa mancata produzione dell'intervallo previsto, non stimabilità o risultato non valido secondo il contratto congelato di DGS-06: per esempio denominatore nullo, limite non finito, intervallo invertito o di ampiezza nulla. Un'inconclusività con intervallo valido non è un errore.

Per cella i e candidato (h,Δ), registrare:

- E_i: numero di repliche in errore;
- P_i: numero di repliche valide con L>0,15+Δ;
- B_i: numero di repliche valide con U<0,15−Δ;
- I_i: numero delle altre repliche valide;
- riconciliazione obbligatoria **E_i+P_i+B_i+I_i=M**.

Nei controlli di falsa promozione si usa **k_i^+=P_i+E_i**. Nei controlli di falsa bocciatura si usa **k_i^−=B_i+E_i**. Ogni errore conta una volta nel rispettivo controllo, mai due volte nello stesso conteggio. Per la potenza gli errori sono insuccessi: si usa P_i/M, senza eliminarli dal denominatore.

| Controllo | Celle | Tasso massimo proposto |
|---|---|---:|
| Falsa promozione al confine μ=0,15 | **2, 6, 9, 11** | 0,025 in ciascuna |
| Falsa promozione sotto soglia μ=0,10 | **1, 5** | 0,025 in ciascuna |
| Falsa bocciatura al confine μ=0,15 | **2, 6, 9, 11** | 0,025 in ciascuna |

Totale **10 controlli obbligatori** per il candidato. I due casi sotto soglia e la coda di bocciatura sono aggiunti esplicitamente: le celle esistono già e non richiedono nuovi generatori. Servono a non dichiarare idonea l'intera regola a tre stati verificando soltanto una sua coda.

Celle per confrontare la potenza a μ=0,20: **3, 7, 10, 12**. Le celle 4 e 8 a μ=0,30 restano diagnostiche di potenza e non sono utilizzate per scegliere il vincitore.

Per ogni candidato devono esistere tutte le righe e tutti gli identificativi attesi. Duplicati, risultati di versioni mescolate, celle mancanti o una corsa interrotta senza riconciliazione completa producono **corsa incompleta/non valutabile**, non autorizzano denominatori ridotti. Le repliche terminate con errore ma registrate correttamente entrano invece in E_i.

### 2a.4 Clopper–Pearson, notazione unica

Per k eventi avversi su M repliche, utilizzare il **limite superiore unilaterale**:

**U_CP(k,M;δ)=BetaQuantile(1−δ; k+1,M−k)** per k<M; U_CP(M,M;δ)=1.

Per k=0 vale U_CP=1−δ^(1/M). Il controllo passa se **U_CP≤0,025**, inclusa l'uguaglianza. Non confrontare una percentuale arrotondata. L'inversione equivalente è P[Bin(M,0,025)≤k]≤δ. La fonte NIST descrive l'inversione binomiale [S1]. Le soglie numeriche sotto sono ricalcoli del DGS.

### 2a.5 FASE 1: filtro e selezione deterministica

**M₁=3.000 per cella.** Per i 10 controlli di ciascun candidato usare U_CP con **δ₁=0,05**, cioè limite superiore unilaterale al **95%**.

Un candidato è ammissibile alla selezione soltanto se:

1. la corsa è completa e identificata;
2. tutti i 10 controlli hanno U_CP≤0,025;
3. in ognuna delle quattro celle di potenza 3,7,10,12 si osserva almeno una promozione valida, P_i≥1.

Con M₁=3.000, il punto 2 equivale esattamente a **k≤60 in ognuno dei 10 controlli**. A k=60, U_CP≈0,0247368843; a k=61, U_CP≈0,0251039129.

Il requisito P_i≥1 elimina il caso banale di astensione completa in uno degli scenari di interesse. **Non è una soglia di potenza utile o economicamente sufficiente.** Qui non introduco un obiettivo di utilità non deciso dal titolare. La potenza osservata, con il suo intervallo, deve essere riportata anche quando è molto bassa.

Tra i candidati ammissibili, ordinare secondo questa sequenza, senza saltare criteri:

1. massimo **min(P_3,P_7,P_10,P_12)**;
2. a parità, massima somma **P_3+P_7+P_10+P_12**;
3. a parità, Δ più piccolo;
4. a parità completa, **HAC prima del bootstrap**.

Vince il primo. L'ultimo criterio è un semplice spareggio preregistrato, motivato dal minor costo riferito di HAC, non un'affermazione di superiorità statistica. Si usano conteggi interi e M uguali, quindi non esiste ambiguità da arrotondamento. Il margine zero non ha priorità su un candidato con potenza minima osservata maggiore, ma, per lo stesso metodo, aumentare Δ non può aumentare P_i sui medesimi limiti validi.

**Se nessuno è ammissibile: STOP di questa proposta, nessuna fase 2.** Non si allarga la griglia e non si elimina la cella sfavorevole. Una revisione del metodo è nuovo sviluppo documentato; prima di una validazione futura occorre una nuova preregistrazione.

Gli intervalli al 95% della fase 1 sono un **filtro esplorativo**. Non hanno copertura simultanea garantita su 8 candidati×10 controlli e non autorizzano una certificazione. La scelta su questi dati è intenzionale. L'evidenza confermativa viene dalla fase 2 indipendente dalla selezione nei termini discussi al §2b.

### 2a.6 FASE 2: un candidato, repliche nuove, nessun recupero

Congelare il solo candidato vincente, con Δ, versione e ambiente. Eseguire **M₂=12.000 repliche per ciascuna delle 12 celle**, namespace fase=2, master invariata 2026111706, replica=1…12.000. Si può riusare la numerazione della replica perché la fase entra nella chiave del seme. Non riusare le serie della fase 1.

Restano invariati D=1.000, a=b=0,025, generatori, gestione degli errori e, per il metodo scelto, L=6 oppure ℓ=10/B=3.999/intervallo basic/ranghi. Non si rivalutano gli altri sette candidati per cercare un sostituto. Nessuna lettura intermedia finalizzata a fermare, prolungare o ritoccare il metodo. Un'interruzione tecnica può riprendere gli identificativi mancanti senza cambiare versione e senza scegliere le repliche in base agli esiti.

Per i 10 controlli usare **δ₂=0,001**, limite superiore unilaterale al **99,9%**. Bonferroni dà copertura simultanea almeno **99%** per i 10 limiti, sotto il modello binomiale di repliche indipendenti. Non serve indipendenza fra celle o fra i due eventi della stessa cella per questa correzione. Serve invece la validità binomiale dentro ciascun controllo.

**Verdetto meccanico della fase 2:**

- **CONFERMATO NEL DOMINIO DEL PILOTA** se la corsa è completa, i requisiti strutturali/diagnostici del §2b sono soddisfatti, tutti i 10 controlli hanno U_CP≤0,025 e P_i≥1 nelle quattro celle 3,7,10,12.
- **NON CONFERMATO** in ogni altro caso, con causa riportata: corsa non valida/incompleta, controllo dei flussi non risolto, evidenza insufficiente sul tasso o nessuna promozione osservata in una cella di potenza richiesta.

Con M₂=12.000, ogni controllo del tasso passa se e solo se **k≤248**. A k=248, U_CP≈0,0249969661; a k=249, U_CP≈0,0250881441.

«Non confermato» non equivale automaticamente a «tasso vero superiore al 2,5%». Il limite superiore può non scendere abbastanza per scarsità di precisione. Questa proposta usa una decisione binaria di ammissione del metodo; non confonde quel mancato via libera con una prova statistica di invalidità.

Se la fase 2 non conferma il candidato, **STOP**. Vietati il passaggio al secondo classificato sui medesimi risultati, l'aumento di Δ, altre repliche aggiunte fino al passaggio o un nuovo tentativo con γ azzerato. Le uscite diventano sviluppo. Un successivo tentativo richiede nuovo protocollo, namespace non usato, budget Monte Carlo fra tentativi e autorizzazioni pertinenti. Qui è previsto **un solo tentativo confermativo** con γ=1%, ancora proposta del DGS.

Anche in caso di conferma, riportare potenza e falsa bocciatura: l'esito non attribuisce al metodo una potenza minima sostanziale. Se la potenza è troppo bassa per gli obiettivi del titolare, il metodo può risultare statisticamente prudente ma praticamente inutilizzabile. La decisione di usarlo resta distinta dal passaggio di questo collaudo.

### 2a.7 Perché 12.000, costi e limiti

M₂ è scelto prima dei risultati come compromesso proposto. Con soglia k≤248:

| Tasso avverso vero ipotetico | Probabilità di passare un controllo |
|---:|---:|
| 0,0125 = a/2 | circa 100% |
| 0,0166667 = a/1,5 | **99,9588%** |
| 0,0200 | **71,2758%** |
| 0,0250 = a | **0,0993062%** |

Se **tutti e dieci** i tassi fossero al più a/1,5, la probabilità di superare tutti i controlli sarebbe almeno **99,5876%** per unione, senza assumere indipendenza fra controlli. Questo calcolo non include i requisiti di completezza, flussi e potenza. Non dimostra che il candidato raggiunga davvero quei tassi. Rispetto a DGS-06 non impongo p*=a/2: la tabella espone il compromesso di precisione anche per margini meno conservativi.

Una validazione del bootstrap su tutte le 12 celle richiederebbe 144.000 repliche esterne e **575.856.000** ricampionamenti interni. Al costo riferito di 0,13 s per replica, l'ordine di grandezza è **18.720 secondi CPU, circa 5 ore e 12 minuti**. Il costo di 0,13 s riguardava il pilota e va inteso come proiezione, non promessa. Se vince HAC, va applicato il suo costo misurato, non quello del bootstrap. M₁ e M₂ non sono sommati per il verdetto confermativo.

La scelta del metodo sui dati della fase 1 non richiede moltiplicare per otto i controlli della fase 2 se il candidato viene congelato prima di esaminare repliche nuove valide. Se invece si provano più candidati in fase 2 o si ritenta finché qualcuno passa, questa giustificazione non vale più.

### 2a.8 Tabella necessaria per un verdetto replicabile

Una riga per fase, versione, metodo, Δ e cella, con almeno: M previsto, M registrato, E, P, B, I, k^+, k^−, U_CP pertinente, esito del controllo, potenza P/M. In fase 1 sono richiesti tutti gli otto candidati; in fase 2 soltanto il vincitore. Aggiungere tabella della selezione con minimo e somma dei quattro conteggi di potenza, e stato dei controlli di flusso.

Per la sola descrizione riportare anche intervalli Clopper–Pearson bilaterali al 95% sulla potenza. Non usarli come criterio ulteriore nascosto e non confonderli con i limiti unilaterali decisionali.

Un errore di formula o implementazione accertato invalida il risultato della versione coinvolta: non lo si considera automaticamente risolto perché E è stato conteggiato. E serve a impedire che fallimenti individuali spariscano dai tassi, non a legittimare un algoritmo diverso da quello dichiarato.

## 2b. PCG64 sostituito da Mersenne Twister con seme SHA-256

### Parere

**Accettabile in linea di principio per questo pilota, con condizioni documentate.** La sostituzione dichiarata non è motivo sufficiente per scartare la corsa. Non considero PCG64 un requisito sostanziale di IA-02 e non attribuisco a SHA-256 una prova di indipendenza dei flussi. Python documenta `Random` come generatore Mersenne Twister e consente istanze con stato separato [S2]. Il meccanismo di NumPy/SeedSequence è diverso e la sua documentazione non certifica una derivazione personalizzata SHA-256→`Random` [S3].

Le sequenze sono pseudocasuali e deterministiche. Stessa master con fase diversa può essere una separazione adeguata per simulazioni, se la fase entra realmente nella derivazione e gli stati non vengono condivisi. Cambiare soltanto il nome della fase nel log non basta.

### Controlli strutturali, soglia zero

Prima della lettura confermativa, il responsabile tecnico deve attestare:

1. **Serializzazione univoca** della tupla ordinata (master, fase, cella, replica, componente), formato esatto dei byte e conversione del digest nel seme. Vietate concatenazioni ambigue, `hash()` dipendente dal processo, troncamenti non dichiarati e seed tratto dall'orologio. Usare il digest completo secondo la conversione congelata. Non prescrivo ora una conversione diversa da quella già usata: va documentata e mantenuta.
2. **Zero duplicati non intenzionali** di chiave e seme nell'inventario dei flussi delle fasi 1 e 2. I due metodi condividono intenzionalmente i dati della stessa replica; questa condivisione è un unico flusso logico, non due repliche indipendenti. Componenti diverse o fasi diverse non devono collidere.
3. Istanze separate per chiave, nessuno stato globale condiviso o ereditato da worker senza corretta inizializzazione; nessun riavvio dello stesso seme dentro una replica quando servono estrazioni nuove. Il medesimo lavoro, assegnato in ordine diverso ai worker, deve produrre lo stesso risultato per identificativo.
4. Versione Python e funzioni di trasformazione dichiarate, inclusa la generazione normale e la gestione delle sue eventuali cache. Riproducibilità verificata nell'ambiente congelato. La documentazione Python non promette identità di tutte le funzioni di distribuzione fra versioni: non sommare copie della stessa replica su Python 3.9 e 3.13 come nuove osservazioni.

Un difetto strutturale accertato significa **corsa non valida** finché non viene risolto con versione e trattamento dei risultati documentati. Zero collisioni osservate non prova che tutte le forme di dipendenza siano assenti.

### Diagnostica limitata fra flussi, proposta con soglia esplicita

Non esiste un test finito che certifichi l'indipendenza di tutti i flussi. Propongo un controllo leggero mirato a riusi, allineamenti e dipendenze grossolane, distinto dalla validazione del metodo. Non è una batteria universale per generatori.

Usare **copie appena inizializzate** delle istanze corrispondenti alle chiavi sotto, senza consumare gli stati del pilota. Per ogni istanza estrarre i primi 10.002 valori di `random()`, indicizzati 0…10.001, e trasformarli in bit con 1 se u≥0,5, altrimenti 0.

Per ciascuna delle 12 celle confrontare le seguenti coppie di flussi:

| Gruppo | Primo flusso (fase, replica, componente) | Secondo flusso | Coppie totali |
|---|---|---|---:|
| A, separazione delle fasi | (1,1,0) | (2,1,0) | 12 |
| B, repliche adiacenti | (f,1,0), per f=1 e f=2 | (f,2,0) | 24 |
| C, componenti | (1,1,0) | (1,1,g), per g=1,2,3 | 36 |

Totale 72 coppie. È lecito inizializzare a scopo diagnostico anche una componente non utilizzata in una particolare cella. Per ciascuna coppia valutare h∈{−1,0,+1}: per t=1…10.000 contare X_h, numero di uguaglianze fra il bit del primo flusso all'indice t e quello del secondo all'indice t+h.

Sotto il riferimento di bit iid indipendenti, X_h∼Bin(10.000,0,5). Utilizzare il p-value bilaterale **p= min[1; 2 min{P(X≤X_h), P(X≥X_h)}]**. Sono **216 confronti**. Segnalazione se **p≤0,01/216 ≈ 0,0000462963**.

Equivalenza intera ricalcolata: nessuna segnalazione per **4.796≤X_h≤5.204**; segnalazione se X_h≤4.795 oppure X_h≥5.205. È una soglia di allarme preregistrata, con rischio familiare al più 1% sotto quel riferimento, non un certificato d'indipendenza. La correzione non richiede indipendenza fra i 216 confronti.

**Esito meccanico:** se tutti i controlli strutturali sono soddisfatti e nessuno dei 216 confronti segnala, la diagnostica è «senza anomalie rilevate nel perimetro». Se almeno uno segnala, il verdetto di ammissione della fase 2 secondo questo protocollo è **NON CONFERMATO**. Non si cambia master, seme, coppia o soglia per cancellare l'allarme. Un allarme può essere casuale: non dimostra da solo un difetto del Mersenne Twister. Una sua eventuale risoluzione richiede un nuovo parere e, se pertinente, un nuovo protocollo; non consente di trasformare retroattivamente in passaggio l'esito della tabella corrente.

Questa diagnostica non controlla tutte le componenti, tutte le repliche, tutti i ritardi o dipendenze non lineari. Non fonda da sola l'ipotesi binomiale del collaudo. Serve insieme alla corretta costruzione dei flussi e all'uso di un generatore noto. Non raccomando testare milioni di correlazioni scegliendo poi quali ignorare.

## 2c. Cella 11: perdite rare

**Regola proposta prima dei risultati: cella obbligatoria con diritto di veto, senza pesi o compensazioni.** Con q=0,01 e 1.000 osservazioni il numero atteso di perdite è 10, ma la singola replica non deve contenerne esattamente 10. Non si rigenerano campioni con poche perdite per normalizzare il conteggio. Il generatore discreto e asimmetrico può mettere in difficoltà il metodo: è precisamente ciò che la cella deve verificare.

Applicazione deterministica:

| Situazione | Conseguenza |
|---|---|
| Fase 1, un candidato ha k_11^+>60 oppure k_11^−>60 | Quel candidato è escluso dalla selezione, anche se passa tutte le altre celle. |
| Fase 1, margine zero fallisce solo in 11 | Si valutano comunque gli altri margini **già presenti nella griglia**, per entrambi i metodi e su tutte le celle. Nessun punto aggiunto e nessun margine specifico per la cella 11. |
| Fase 1, tutti gli otto candidati falliscono almeno un controllo, anche solo in 11 | STOP; nessun candidato per la fase 2. |
| Fase 2, il candidato scelto ha k_11^+>248 oppure k_11^−>248 | **NON CONFERMATO**, anche se le altre celle passano. Nessun cambio di margine o metodo sulla fase 2. |
| Cella 11 mancante, interrotta o generatore riconosciuto errato | Corsa non valutabile per il dominio dichiarato; non si procede omettendola. |

La frequenza del 1% non è una stima verificata delle perdite rare nella futura strategia. Tuttavia non abbiamo una giustificazione preventiva per escludere l'asimmetria dal dominio. Se si volesse in futuro un metodo valido soltanto in un dominio che esclude questo caso, occorrerebbero condizioni sostanziali riconoscibili prima della prova reale e una nuova validazione. «La strategia osservata sembra gaussiana» o «nello sviluppo non si sono viste perdite rare» non bastano da soli a giustificarlo.

Non si decide il peso della cella osservando quanto penalizza il candidato preferito. La cella 12 conserva inoltre la misura del costo in potenza del metodo prudente scelto per questa famiglia.

## 2d. Ordine delle finestre, spiegato al titolare

La scelta riguarda quale parte della storia usare prima e quale conservare intatta. Nessuna delle due opzioni elimina la necessità di una successiva verifica prospettica.

| Opzione | Che cosa ottieni | Che cosa spendi o rischi |
|---|---|---|
| **Recenti prima** | La prima prova usa la parte della riserva temporalmente più vicina allo sviluppo e a oggi. | Consumi subito quei dati. La parte rimasta per la seconda prova è più antica e potrebbe rispondere soprattutto alla domanda «funzionava anche in un contesto più lontano?». Vicinanza temporale non prova somiglianza del mercato. |
| **Vecchi prima, recenti protetti** | Conservi i dati storici più recenti per una seconda prova. | La prima prova si svolge in un contesto più lontano e può consumare la quota maggiore su una domanda meno vicina all'uso futuro. Per la seconda prova servono più dati se la quota scende. |

Con la formula di spesa discussa, non ancora qui ratificata, la seconda quota per una variante scende da 2,5% a circa 0,8333%. Nell'esempio normale con potenza 80% ciò richiede circa **un terzo di trade in più**, a parità delle altre ipotesi. Non è un costo fisso valido per ogni strategia.

Prima della scelta servono soltanto copertura annuale BID, ASK e intersezione, denominatori del calendario e idoneità sotto criteri già motivati. La sola verifica BID non basta. Dal rendiconto di copertura non si possono ricavare liquidità, frequenza dei segnali o rendimento della candidata. Per il dimensionamento si usano ipotesi dichiarate derivate dallo sviluppo consentito, senza prezzi della riserva.

La domanda per il titolare è: **preferisci che la prima prova usi la storia più vicina a oggi, oppure conservare quella storia per un secondo tentativo?** La scelta ha senso solo se la porzione lasciata da parte può davvero sostenere la seconda prova. Se non c'è spazio per entrambe, occorre valutare una sola verifica storica e/o nuovi dati prospettici. Nessuna raccomandazione vincolante e nessuna assegnazione di finestre in questo documento.

## 2e. Parere sulla lettura stretta di D-24 e su R15

**Il mantenimento a 0/2 mi sembra coerente come applicazione prudente del principio descritto, ma non ne certifico l'obbligatorietà normativa.** Il modello di minaccia riportato include gli errori in buona fede. Un errore in un test può indebolire l'evidenza che dovrebbe individuare difetti, anche se non altera direttamente il codice eseguito sul mercato. Non è automaticamente irrilevante perché è «solo nel test».

Il motivo metodologico è l'effetto sulla qualità della verifica. Il fatto che considerarlo innocuo favorirebbe Claude spiega il suo atteggiamento prudente, ma non è da solo un criterio tecnico sufficiente. L'origine dell'errore, l'onestà dell'autore e il conflitto d'interesse non sostituiscono la valutazione del suo effetto.

Non ho letto il rapporto R15, #106 o il testo normativo integrale di D-24 in questa revisione. Non posso stabilire se la lettera della regola obblighi a scartare il giro, né se ogni correzione minore richieda un azzeramento. Il cambio a `303890b` richiede comunque che il giro successivo dichiari chiaramente candidato, ambiente e perimetro. Questo resta nel lavoro di Claude e Gemini.

Distinguere nel registro: **«R15 non conteggiata secondo l'interpretazione prudente adottata da Claude»** da **«D-24 impone senza possibilità interpretativa questo esito»**. La prima è sostenuta dal messaggio; la seconda non è dimostrata qui. Il contatore resta quello dichiarato, 0/2. Non propongo di ribaltarlo e non riapro D-24. L'eventuale decisione diversa resta del titolare, con motivazione registrata.

## 3. Controllo finale del DGS, letture e consegna

### Seconda lettura interna

Ho controllato la separazione fra scelta e validazione, i conteggi delle celle, le code dei limiti, le uguaglianze alle soglie e le condizioni di arresto. I limiti CP sono **superiori unilaterali** anche quando l'evento conteggiato è la falsa bocciatura: si sta sempre limitando dall'alto un tasso di errore. Non sono limiti sulla media R.

Il protocollo non cambia regole dopo il risultato della cella 11, non recupera quota Monte Carlo con tentativi successivi e non spaccia un test di correlazione per prova d'indipendenza. Il margine è uniforme e simmetrico, la graduatoria è totale e la fase 2 riguarda un solo candidato. Nessun risultato reale è stato usato per scegliere griglia o soglie. Nella seconda lettura ho eliminato un'ambiguità: un allarme sui flussi produce NON CONFERMATO per questo protocollo, senza una clausola discrezionale che permetta di ribaltare il risultato della stessa tabella.

Controlli logici con esempi inventati: P=59 ed E=2 danno k=61 e non passano la fase 1; P=247 ed E=1 danno k=248 e passano quel singolo controllo della fase 2; P=248 ed E=1 danno k=249 e non lo passano. Il passaggio di un singolo controllo non sostituisce i restanti requisiti. Questi esempi non sono risultati del pilota.

**Limiti da mantenere visibili:** le scelte γ=1%, griglia, M₂=12.000, spareggio e diagnostica dei flussi sono proposte. Il controllo di errore è condizionato alla correttezza dei generatori e delle repliche. La conferma non garantisce sufficiente potenza né trasportabilità al mercato. Un singolo revisore che rilegge il proprio lavoro non costituisce una revisione indipendente.

### Letture

- **Integrale:** MESSAGGIO 5 ricevuto in chat.
- **Parziale:** DGS-06, sezioni del pilota, finestre e relativi limiti; documentazione pubblica Python 3.13 sul generatore, seed e riproducibilità; documentazione NIST sui limiti binomiali; documentazione NumPy sulla generazione parallela. Non letti gli interi articoli scientifici collegati.
- **Non letti:** risultati della fase 1 o 2, codice del pilota o del banco, worktree, repository, registri correnti, R15/R16, documenti sigillati e dati di mercato. Nessun incarico inviato a Claude o Gemini.
- **Ricalcolati:** soglie CP 60/3.000 e 248/12.000 con i limiti adiacenti, probabilità illustrative di superamento, soglie binomiali della diagnostica dei flussi e costi. Nessuna simulazione della strategia o del pilota.

### Fonti pubbliche

- [S1 — NIST, Exact binomial confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm). Formula dell'inversione binomiale. Non stabilisce i livelli o le regole di governance proposti qui.
- [S2 — Python 3.13, random](https://docs.python.org/3.13/library/random.html). Generatore, istanze, seeding e limiti della riproducibilità. Non certifica l'implementazione di Claude.
- [S3 — NumPy, Parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html). Utile per distinguere separazione degli stream e hashing dei seed. Le garanzie specifiche di SeedSequence non si trasferiscono automaticamente a SHA-256 con `random.Random`.

**Consegna:** un protocollo candidato unico e applicabile ai conteggi, con proposte numeriche esplicite e nessuna autorizzazione implicita alla sua adozione. Le regole, se adottate, vanno impegnate prima della lettura e poi applicate senza eccezioni opportunistiche.
