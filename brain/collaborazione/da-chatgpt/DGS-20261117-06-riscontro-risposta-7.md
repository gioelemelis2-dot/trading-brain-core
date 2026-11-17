# DGS-06 · Seconda revisione e bozze metodologiche

17 novembre 2026 · Per il titolare e Claude · **Proposte, nessuna ratifica e nessun mandato di esecuzione.**

## Perimetro ed esito

Letta integralmente `7-RISPOSTA-AL-DOSSIER-DGS-05.md`. Il confronto riguarda il testo ricevuto e i precedenti documenti del DGS. Non sono stati aperti codice di progetto, worktree, archivio del progetto, documenti sigillati o dati di mercato. Sono stati eseguiti soltanto ricalcoli matematici isolati. Nessun pilota è stato eseguito e H-002 non viene modificata né riesaminata.

La risposta di Claude recepisce correttamente molte rettifiche. Restano da correggere due campioni arrotondati per difetto, una conclusione troppo forte sulla verificabilità dei vantaggi, il «non passa mai» del collaudo e la stima troppo ottimistica dei tempi. **I nove budget Monte Carlo di Claude sono sufficienti per il requisito dichiarato. Non sono errori solo perché esistono budget minori.**

Questo documento contiene il controllo di tutte le undici righe del §2, i ricalcoli, quattro bozze e una seconda revisione interna finale. Non certifica il candidato `8e51ce9`, i mutanti, i 366 test o lo stato della riserva. Questi rimangono risultati riferiti da Claude.

## 1. Controllo riga per riga del §2

| Riga | Giudizio DGS | Motivo e correzione richiesta |
|---|---|---|
| 1. P1, stima nello screening e limite inferiore in verifica | **Concordo sul principio, in disaccordo con parte della motivazione** | 4.906 e 6.544 sono corretti nel modello dichiarato. 545 e 1.226 sono arrotondamenti per difetto. I valori dipendenti sono approssimazioni con F troncato. «Solo vantaggi veri di +0,25 R o più sono verificabili» non segue dai calcoli. Servono durata effettivamente assegnata, frequenza, dispersione, dipendenza, quota e potenza obiettivo. Il principio non ratifica questi parametri. Vedi §1.1. |
| 2. P2, α totale e spesa α_j/m | **Concordo con condizioni** | 5% resta proposta. Le quote sommano al budget per telescopaggio, ma occorrono test validi per il disegno adattivo effettivo. Il +33% è corretto nell'approssimazione normale con potenza 80%, m=1, medesima dispersione ed effetto. Non è un moltiplicatore universale per altri m, potenze o dipendenze. Presenza della formula nel codice riferita, non verificata qui. |
| 3. P2, ordine delle finestre e parte protetta | **Concordo che sia da decidere** | Nessun ordine è dimostrato migliore per ogni obiettivo. «Durata minima» deve essere una durata pianificata prima, non fermarsi quando compare il risultato favorevole. La parte protetta va dimensionata con la quota della prova a cui è destinata. Vedi §2d. |
| 4. P2, custodia prima della verifica | **Concordo sul vincolo temporale, con riserva sulla prova** | Il collegamento al caricatore deve essere dimostrato prima di qualsiasi lettura della riserva, incluse letture indirette per segnali o riscaldamento. Un commit spinto dà un impegno esterno, ma da solo non prova che ogni percorso di accesso sia vincolato. La verifica tecnica resta nel mandato di Claude/Antigravity e nel modello D-24 già deciso. Non impongo questo requisito come nuovo blocco del sigillo, salvo che quel passaggio legga già la riserva. |
| 5. P3, quattro integrazioni | **Concordo sull'integrazione, non sulla riduzione a mera redazione** | Esplicitare R e casi ambigui può documentare convenzioni esistenti. Estenderle a nuove strategie o fissare trattamento dei dati mancanti e verdetti è anche una scelta di metodo. «Stop prima del target» non risolve da solo ordini d'ingresso intrabar, gap o prezzi BID/ASK. La sintesi di Claude omette parte della mia seconda integrazione: benchmark, varianti, veti, N, m e vie di promozione. Testi completi al §2b. |
| 6. P4, DA-31 a tre stati | **Concordo nel principio** | Servono anche livello del limite superiore, priorità dei controlli, significato dei due minimi e regole di riesame. Un limite inferiore che non supera la soglia non basta a bocciare. Bozza al §2a. |
| 7. P5, ritiro 99/98/95% e cinque minuti | **Concordo** | È ritirata la raccomandazione di ratificarli immediatamente. I numeri non diventano vietati, ma restano privi di giustificazione sufficiente. Neppure 50% e 25% sono validati da questo ritiro. Il rendiconto di intersezione e buchi resta utile. |
| 8. P6, commit, ambiente, perimetro | **Concordo sul requisito** | L'applicazione a R15 è riferita da Claude. Non ho letto il mandato attivo e non certifico che sia applicato. La separazione dei perimetri aiuta, purché siano dichiarate le dipendenze dagli strumenti di contorno che incidono sull'evidenza. Nessuna riapertura di D-24. |
| 9. Addendum §4, buchi selettivi | **Concordo, con un confine essenziale** | Il controesempio dimostra una distorsione possibile, non la sua frequenza sul feed. Lo studio degli effetti deve usare dati sintetici o sviluppo consentito. Nessuna scelta di soglia guardando segnali, prezzi o risultati della riserva. L'esclusione a posteriori delle sedute peggiori può selezionare il campione. |
| 10. Collaudo, Clopper–Pearson e U≤a | **Concordo sulla matematica, non sulla fattibilità già conclusa** | La regola è corretta per repliche indipendenti del generatore fissato. I costi di repliche si possono calcolare, quelli di tempo vanno misurati. Non è dimostrato che tutto l'intervallo sia economico o che tutta la procedura sia sproporzionata. I bootstrap interni incidono molto. Vedi §1.2. |
| 11. γ=1%, p*=a/2, 90% per cella | **Concordo che vadano discussi, preciso il significato** | p* è un obiettivo di pianificazione, non il tasso vero già dimostrato né un obbligo matematico di dimezzare il nominale. Il pilota può informare margine, costi e potenza. Il protocollo finale deve poi essere congelato e verificato su repliche nuove. Non si allenta l'accettazione dopo aver visto la verifica finale. |

### 1.1 Ricalcolo indipendente di P1

Modello illustrativo: test normale unilaterale, soglia c=0,15, deviazione marginale σ=1,25 R nota, potenza 1−β=0,80. Per osservazioni indipendenti:

**n_cont = [(z_(1−a)+z_0,80) σ /(μ−c)]²; n = ceil(n_cont).**

| Quota a | μ vera | n continuo | Minimo intero iid | Numero di Claude |
|---:|---:|---:|---:|---:|
| 0,025 | 0,30 | 545,061093 | **546** | 545 |
| 0,025 | 0,25 | 1.226,387458 | **1.227** | 1.226 |
| 0,025 | 0,20 | 4.905,549834 | **4.906** | 4.906 |
| 0,05/6 | 0,20 | 6.543,196280 | **6.544** | 6.544 |

Le prime due differenze sono piccole, ma quando si dichiara un minimo vanno arrotondate per eccesso. Non cambiano la conclusione generale sulla scarsità d'informazione.

Per AR(1) stazionario gaussiano con correlazione ρ=0,25 e σ marginale fissata:

**F(n)=1+2 Σ_(k=1…n−1)(1−k/n)ρ^k**, Var(media)=σ²F(n)/n.

Il minimo si ottiene cercando il primo intero con n/F(n) ≥ n_cont, non moltiplicando un intero già arrotondato per 1,66. Per ρ=0,25, F(n) tende a 5/3, non a 1,66 esatto.

| Quota 2,5%, μ vera | Claude, con F≈1,66 | Minimo con F(n) finito e varianza nota |
|---:|---:|---:|
| 0,30 | 905 | **908** |
| 0,25 | 2.036 | **2.044** |
| 0,20 | 8.143 | **8.176** |

Non attribuisco a Claude un errore di modello per avere usato un'approssimazione dichiarata. Chiedo di non presentare quei valori come minimi esatti. Anche i miei valori sono esatti soltanto entro il modello gaussiano con varianza e dipendenza note. Non dimensionano automaticamente HAC o bootstrap stimati.

Il rapporto continuo fra n a quota 0,05/6 e n a quota 0,025 è **1,33383545**, cioè **+33,3835%**, a effetto e potenza invariati. La frase «circa 33%» è corretta in queste condizioni.

**La soglia pratica +0,25 R non è deducibile.** Trattando 4.700 trade soltanto come ipotesi, con quota 2,5%, ρ=0,25 e σ nota, la media che dà potenza 80% è circa **0,21594 R**. Con 2.500 trade diventa **0,24041 R**. Non ho verificato che la riserva offra 4.700 sedute idonee, un trade per seduta o questi campioni dopo la protezione. La precedente proiezione di circa 2.500 trade e questa di 4.700 sono scenari di frequenza diversi.

Con μ=0,20 e n=4.700 la potenza del riferimento è circa **56,53%**, non zero. Non raggiungere l'80% pianificato non significa impossibilità di promozione. Nemmeno «esito atteso non decidibile» è automatico: dipende dai minimi e dalla regola a tre stati. Il dimensionamento va rifatto nella scheda con ipotesi conservative motivate, senza trasformare una media selezionata nello sviluppo in un vantaggio vero noto.

### 1.2 Ricalcolo indipendente dei costi del §4

Ho usato le quote esatte 0,025, 0,05/6 e 0,05/12, non le etichette arrotondate 0,833% e 0,417%. Ho mantenuto **δ=0,01/(2K)**, perché è la convenzione della specifica discussa.

Per un conteggio X∼Bin(M,p*), definire:

- U(k,M)=BetaQuantile(1−δ;k+1,M−k), con U(M,M)=1.
- k_max(M)=massimo intero k con U(k,M)≤a, oppure −1 se nessuno.
- Probabilità di superamento **q(M)=P_(p*)[X≤k_max(M)]**.

Ho cercato tutti gli M interi da 1 a 100.000 e preso il primo con q(M)≥0,90. La condizione su U è stata calcolata mediante inversione della CDF binomiale e ricontrollata con i quantili Beta ai nove risultati e ai nove budget di Claude. Ricalcoli con SciPy 1.17.0, senza script di Claude e senza simulazioni di strategie.

| a | K | p* | M di Claude | q(M di Claude) | Primo M che raggiunge 90% | q al primo M |
|---:|---:|---:|---:|---:|---:|---:|
| 0,025 | 20 | a/2 | 3.068 | 92,7734% | **2.770** | 90,7826% |
| 0,025 | 60 | a/2 | 3.529 | 93,8457% | **3.077** | 90,1197% |
| 0,025 | 20 | a/1,5 | 7.102 | 91,7650% | **6.823** | 90,2121% |
| 0,05/6 | 20 | a/2 | 9.394 | 94,7250% | **8.338** | 90,3439% |
| 0,05/6 | 60 | a/2 | 10.804 | 95,2841% | **9.413** | 90,4505% |
| 0,05/6 | 20 | a/1,5 | 21.733 | 90,9207% | **20.790** | 90,2582% |
| 0,05/12 | 20 | a/2 | 18.898 | 94,2816% | **16.689** | 90,2390% |
| 0,05/12 | 60 | a/2 | 21.733 | 94,8542% | **18.841** | 90,3395% |
| 0,05/12 | 20 | a/1,5 | 43.715 | 91,2661% | **41.602** | 90,1267% |

**Tutti i budget di Claude soddisfano il requisito.** Non dichiara esplicitamente che siano i minimi interi, quindi la differenza non dimostra un errore. I primi M trovati non sono raccomandazioni di risparmio automatico. q(M) ha un andamento a denti di sega, perché k_max cambia a scatti. Aumentare leggermente M può riportare q sotto 90%: ogni M finale va valutato direttamente. Il 90% per cella non è 90% di superamento congiunto.

**Correzione di «p=a non passa mai».** Può passare con probabilità piccola, al più δ nella convenzione esatta utilizzata. Per esempio, a=0,025, K=20, M=2.770, k_max=42: sotto p=a la probabilità di passaggio è circa **0,000249508**, cioè **0,0249508%**. È raro, non impossibile. Aumentare M non rende probabile la certificazione di un metodo esattamente al nominale con questa regola.

**Una coda o due.** Per la sola conclusione positiva U≤a, δ=γ/K può bastare per K conclusioni preregistrate. Se si vuole proteggere anche la conclusione negativa L>a, occorre una ripartizione fra code, per esempio γ/(2K). K deve contare tutte le conclusioni interessate, inclusi più metodi se certificati insieme. Non cambio la convenzione a posteriori per ottenere un passaggio.

**Tempo.** 60×10.000 = 600.000 valutazioni per un metodo. In esecuzione seriale:

| Tempo per valutazione | Tempo totale |
|---:|---:|
| 1 millisecondo | 10 minuti |
| 10 millisecondi | 1 ora e 40 minuti |
| 1 secondo | 166 ore e 40 minuti, circa 6,94 giorni |
| 60 secondi | 10.000 ore |

Quindi «da millisecondi a un secondo, si fanno in ore» non è una stima sufficiente. Servono benchmark separati HAC/bootstrap, B ricampionamenti interni, hardware, parallelismo reale e memoria. «Mezza giornata di lavoro» è una stima dell'autore, non verificabile qui. La procedura completa può essere costosa, ma la sproporzione non è dimostrata senza dimensionare almeno un prototipo.

### 1.3 Precisazioni sui §§1 e 3, senza allargare l'audit tecnico

- La distinzione tra l'arresto BID al 2020 e il vecchio episodio dei venti giorni è recepita. Il mio DGS-05 affiancava i due eventi in modo poco utile. La riga «Last login» e un log incompleto, descritti da Claude, non provano da soli la causa riavvio. Non ho letto quei log e non trasformo la spiegazione in verifica indipendente.
- «Mai aperta» va inteso con i limiti del censimento, non come prova assoluta su accessi manuali o fuori log.
- Un collaudo completo della selezione può aspettare mentre si prepara il metodo. **Non può aspettare oltre una verifica che pretenda una garanzia globale non altrimenti giustificata.** Una dimostrazione valida del disegno può evitare una simulazione integrale enorme, ma va esplicitata. Analogamente, uno stress esteso sui regimi può essere differito, mentre le ipotesi di stabilità e l'estimando devono essere definiti prima dell'uso.
- Il compito B di R15 e il nuovo collaudo sono descritti come distinti. Non ho letto il mandato R15 e non aggiungo incarichi a Gemini.

## 2a. Bozza DA-31 completa a tre stati

**Testo proposto per nuove ipotesi. Non applicare retroattivamente a H-002. I parametri del disegno devono essere compilati e ratificati nella scheda prima dell'accesso.**

### Oggetto e livelli d'errore

L'estimando μ è la media netta per operazione della politica congelata, nel periodo e nell'universo dichiarati. La soglia c è +0,15 R secondo IA-02. Fissare il metodo per entrambi i limiti:

- L_a, limite inferiore unilaterale con copertura almeno 1−a, dove a è la quota della variante.
- U_b, limite superiore unilaterale con copertura almeno 1−b, dove b è la tolleranza di falsa bocciatura statistica.

**Proposta concreta da ratificare: b=a.** Con un metodo simmetrico normale ciò dà L=μ_hat−z_(1−a)SE e U=μ_hat+z_(1−a)SE. È un esempio, non l'approvazione di una SE iid. Un bootstrap richiede entrambe le code esplicitate e collaudate. Se b=a, la copertura congiunta dei due limiti è almeno 1−2a per unione, non 1−a. Il budget α di P2 riguarda le false promozioni. Non diventa per questo un budget globale di ogni possibile errore di decisione. Se si vuole controllare globalmente anche le false bocciature, va registrato un budget distinto.

### Due minimi e condizioni d'idoneità

**Minimo tecnico.** Fissare nella scheda numero minimo di operazioni, sedute osservate e sedute con operazioni, requisiti sul denominatore, sul numero di blocchi e sulla stimabilità della varianza. I numeri derivano dal metodo e dal suo dominio collaudato. Trenta trade non è una convenzione universale. Una routine che restituisce un numero non dimostra di avere raggiunto il minimo tecnico.

**Minimo informativo.** Fissare prima dell'apertura campione e durata che raggiungano la potenza obiettivo scelta a un'alternativa μ_+>c, con dispersione, dipendenza e frequenza motivate dallo sviluppo consentito. Registrare anche la sensibilità a ipotesi meno favorevoli. Per la capacità di bocciare, dichiarare una μ_-<c e la relativa potenza, oppure dichiarare espressamente che non è stata garantita. Il minimo informativo è una condizione del disegno, non una potenza ricalcolata usando la media favorevole osservata nella riserva.

**Proposta conservativa per questa bozza:** richiedere entrambi i minimi per entrambi i verdetti statistici. Ciò può produrre un non decidibile anche quando un limite apparentemente favorevole attraversa la soglia su un campione troppo piccolo. È un costo esplicito della regola, non una necessità matematica universale. I veti terminali hanno invece propri requisiti di validità, definiti prima.

### Regola di decisione e priorità

1. Accertare integrità, identificabilità degli esiti e validità delle misure pertinenti. Un errore di strumenti o dati non costituisce da solo una bocciatura economica dell'ipotesi.
2. Se un **veto terminale preregistrato** è accertato con le sue misure valide e il suo campione richiesto, l'esito è **bocciata per veto**, anche se la media resta non stimabile. Un requisito non valutabile non è un veto fallito. Un veto probabilistico richiede la propria incertezza e non eredita una garanzia automatica dal test di μ.
3. In assenza di veto terminale accertato, se dati o metodo non sono idonei, un minimo manca o l'intervallo non è stimabile, l'esito è **non decidibile**, con causa registrata.
4. Con prova idonea e minimi raggiunti, **promossa** solo se L_a>c e tutti gli altri requisiti vincolanti sono valutabili e superati.
5. Con prova idonea e minimi raggiunti, **bocciata statisticamente** se U_b<c.
6. Negli altri casi, **non decidibile**. L_a=c o U_b=c non bastano per i rispettivi verdetti. L>U o risultati numerici incoerenti invalidano il calcolo.

I tre stati sono mutuamente esclusivi dopo l'applicazione di questa priorità. «Bocciata» significa mancato superamento di questa domanda e prova, non dimostrazione di inutilità universale. «Promossa» non attesta stabilità futura o autorizzazione all'impiego reale.

### Esiti incompleti, orizzonte e riesame

La finestra è fissata prima. Non si prolunga perché il risultato è vicino alla soglia e non si chiude prima perché è favorevole. Operazioni aperte o non ricostruibili restano nel rendiconto. Il trattamento di fine finestra e l'eventuale periodo di liquidazione devono essere prenotati. Se l'incertezza non può essere delimitata con un metodo valido e può cambiare il giudizio, l'esito non può essere promosso.

Una prova non decidibile viene archiviata con identità, causa, dati consumati, metodo, quota e condizione di eventuale riesame. Il riesame ordinario usa **solo nuove osservazioni non esposte**, calendario prenotato e stesso estimando e regola congelata. Per stesso estimando si intende la stessa definizione della quantità bersaglio; non si presume che la media vera resti uguale in periodi diversi. Il vecchio risultato rimane visibile nel registro, ma non viene sommato al nuovo campione per un test ordinario come se il riesame fosse stato pianificato dall'inizio. Un disegno cumulativo/sequenziale richiede un protocollo distinto e controllo dell'errore prima della prima lettura.

La scheda stabilisce ex ante un limite di riesami, proposto qui pari a **uno** per la stessa versione, da ratificare. È una proposta di contenimento del consumo della riserva, non una costante statistica necessaria. Al secondo non decidibile la versione resta non promossa e parcheggiata. L'eventuale lavoro successivo richiederebbe una nuova decisione esplicita, senza cancellare la storia o azzerare i contatori. Una bocciatura terminale chiude la versione per quella domanda. Una revisione motivata deve dichiarare cosa cambia e costituisce una nuova versione/ipotesi, non un tentativo nascosto.

### N, j, m, quota e consumo

| Oggetto | Regola proposta |
|---|---|
| **N** | Mantiene la storia delle prove selezionabili secondo il registro e DA-19. Ogni nuova prova selezionabile di riesame viene registrata, anche se il risultato è non decidibile. Cambi di regola, filtro, variante o analisi usati per selezionare richiedono voci ulteriori coerenti con la convenzione di N. Non si deduce N da j. Una replica identica di controllo tecnico non crea una nuova strategia selezionabile, purché non introduca scelte. |
| **j** | Indice globale delle coorti/aperture confermative. Il riesame su una nuova finestra richiede la successiva apertura disponibile, non un reset e non necessariamente j+1 della sola ipotesi se altre coorti sono passate nel frattempo. Più varianti realmente prenotate insieme condividono la coorte con m dichiarato. |
| **m e a** | Tutte le vie di promozione della coorte entrano nella ripartizione, proposta a=α_j/m. Un riesame non riusa la vecchia quota. Nessuna riduzione di m dopo l'esclusione sfavorevole di una variante. |
| **Consumo** | Registrazione dell'impegno e consumo prima della prima lettura. L'apertura avviata consuma perimetro e quota a prescindere dal verdetto o da un guasto successivo. Non decidibile non dà rimborso. Una cancellazione prima di ogni esposizione non deve produrre un numero fittizio di prova eseguita, ma le regole per liberare una prenotazione vanno deliberate in P2 e dimostrate dalla custodia. In questa bozza non autorizzo alcun rimborso. |
| **Parti esposte** | Dati già letti, riscaldamento, segnali ed esiti non tornano vergini cambiando nome o mercato della scheda. Il perimetro di consumo e le eventuali sovrapposizioni sono dichiarati prima. |

Un nuovo tratto cronologico non garantisce indipendenza dal precedente. Prima di attribuire alla spesa α una garanzia globale occorre giustificare la validità dei test rispetto alla selezione e alla dipendenza fra finestre. Un embargo arbitrario non è una dimostrazione.

## 2b. Quattro integrazioni P3 pronte per il modello H-003

**Mappatura dichiarata.** Le quattro integrazioni sono quelle numerate in DGS-05 §P3. Il §8 del modello è identificato nei documenti letti come sezione degli esiti. L'allegato di Claude non fornisce i numeri delle altre sezioni di destinazione. Non li invento e non riapro altri file del progetto per recuperarli. Indico la destinazione per titolo/funzione; Claude può confermare i riferimenti nella propria copia prima dell'eventuale inserimento autorizzato. I testi seguenti non sono ancora applicati.

### P3.1 · Nella sezione di regole operative, esecuzione e casi ambigui

> Per ciascun segnale e ordine indicare timestamp dell'informazione, primo istante in cui è conoscibile, lato eseguibile BID/ASK e primo istante d'esecuzione consentito. Una decisione fondata sulla chiusura della barra non può usare quella chiusura per un'esecuzione anteriore alla sua disponibilità.
>
> Preregistrare la gestione dei percorsi intrabar non distinguibili, inclusi ingresso e uscita nella stessa barra, stop e target entrambi compatibili, gap, ordini pendenti e dati mancanti. Quando pertinente, applicare una convenzione conservativa motivata rispetto ai percorsi compatibili e contarne gli utilizzi. La precedenza dello stop sul target non risolve automaticamente gli altri casi. Se non è possibile identificare un esito o un limite attendibile, dichiarare l'incertezza senza eliminare l'operazione.
>
> Elencare i casi di riferimento e il risultato atteso. Il criterio principale di gestione dell'ambiguità viene fissato prima delle prove. Le analisi alternative restano diagnostiche, salvo essere dichiarate e conteggiate come vie di selezione.

### P3.2 · Nella sezione di metriche, confronti, varianti e conteggio delle prove

> Definire R_i=P/L netto_i/B_i, con budget positivo B_i impegnato prima dell'ingresso, valuta, regola di dimensionamento e arrotondamenti dichiarati. Riportare separatamente il rischio pianificato effettivamente impiegato. Ingresso e relative uscite parziali compongono una sola operazione. Definire prima come aggregare incrementi, reingressi e posizioni sovrapposte. Non cambiare il denominatore dopo aver osservato il risultato.
>
> Il netto include costi pertinenti con formule e fonti. Lo spread già incorporato nei prezzi eseguibili non viene sottratto due volte. Il trattamento di slittamento, gap, finanziamento e cambio valuta è esplicito. Lo stop non garantisce una perdita massima di −1 R.
>
> Dichiarare l'estimando per operazione, il calendario eleggibile e la politica congelata. I giorni osservati senza trade non sono operazioni da zero R. Dati mancanti e giorni senza trade restano distinti.
>
> Per ogni benchmark motivare comparabilità di date eleggibili, rischio, costi ed esecuzione. Elencare variante primaria, alternative, tagli ereditati, veti e tutte le vie che possono portare a promozione. Registrare separatamente N, m, j e quota. Una diagnostica che influenza la scelta viene registrata come selezionabile secondo la convenzione di progetto. Le varianti non vengono ridotte a posteriori per recuperare quota.

### P3.3 · Nella sezione di campione, inferenza, potenza e finestre

> Fissare metodo e livelli di entrambi i limiti, trattamento della dipendenza entro e fra sedute, metodo di aggregazione e parametri dell'intervallo. Per coppie giornaliere (S_d,K_d), la media per trade è ΣS_d/ΣK_d, non la media non pesata dei rendimenti medi giornalieri. Conservare i giorni osservati senza operazioni come (0,0) ove previsto dal metodo.
>
> Dichiarare minimo tecnico e minimo informativo, unità temporali richieste, alternativa di pianificazione, potenza e sensibilità. Motivare il passaggio da frequenza nello sviluppo a durata della verifica. Non stimare la durata necessaria dai risultati della riserva.
>
> Definire prima anni parziali, sedute valide, denominatori dei criteri annuali e significato di «ultimi cinque anni». La finestra deve consentire tutti i requisiti previsti. Un criterio non valutabile non è considerato superato. Calendario, riscaldamento, embargo e periodo di liquidazione sono parte del disegno prenotato. Esclusioni per dati mancanti non devono occultare segnali o operazioni già maturati.

### P3.4 · Nel §8, esiti e condizione d'uscita

> Applicare la versione ratificata di DA-31, identificata con data e versione. Per ogni variante registrare separatamente promossa, bocciata oppure non decidibile e la causa. «Nessuna variante promossa» non implica che tutte siano bocciate: se almeno una è non decidibile, la sua incertezza resta esplicita. Nessun esito non decidibile autorizza l'avanzamento.
>
> Per l'eventuale riesame indicare dati nuovi ammessi, regola congelata, limite di riesami, nuova prenotazione, quota e registrazione in N e j. Non riutilizzare gratuitamente dati o quota consumati. Una modifica per recuperare un esito sfavorevole crea una versione/ipotesi distinta con la storia precedente preservata. Fino alla ratifica della DA-31 completa, questa clausola è una bozza senza effetto normativo.

## 2c. Pilota del collaudo, proposta prima dell'esecuzione

### Obiettivo e critica al pilota di Claude

Concordo con un pilota di sviluppo del metodo, senza valore di certificazione. I quattro casi proposti verificano due riferimenti gaussiani e un'alternativa relativamente facile. Con σ=1,25, n=1.000, a=2,5%, il test con varianza vera ha potenza circa **96,67%** a μ=0,30 iid e **83,65%** con ρ=0,25. A μ=0,20 scende rispettivamente a **24,35%** e **16,36%**. Limitarsi a +0,30 rende poco visibile il costo che interessa P1.

Inoltre, con un trade per seduta non si mette alla prova il rapporto ΣS/ΣK, e una distribuzione gaussiana non verifica le perdite rare. Propongo **12 celle, due metodi**, mantenendo 3.000 repliche esterne per cella. È un ampliamento motivato del pilota, da approvare. Se il costo non è sostenibile, il titolare può autorizzare solo le prime otto celle come confronto gaussiano, esplicitando che frequenza variabile e asimmetria non sono state verificate. Non si riduce la matrice dopo aver visto gli esiti.

### Matrice proposta

Tutti i parametri seguenti sono valori sintetici proposti, non stime del mercato. D=1.000 sedute; a=b=0,025; σ marginale=1,25 R. Non si applicano screening o veti di H-002. Si valuta l'intervallo isolato e i suoi attraversamenti di soglia, senza presentarli come promozioni operative.

| Celle | Generatore | μ | Conteggio e scopo |
|---|---|---|---|
| 1–4 | Gaussiano iid | 0,10; 0,15; 0,20; 0,30 | K_d=1, n=1.000. Null sotto/al confine, alternativa vicina/lontana. |
| 5–8 | Gaussiano AR(1), ρ=0,25 | 0,10; 0,15; 0,20; 0,30 | K_d=1. Stesse domande con dipendenza. |
| 9–10 | Conteggio casuale e componente giornaliera correlata | 0,15; 0,20 | K_d∈{0,1,3} con probabilità {0,25;0,50;0,25}, indipendente dai rendimenti. E[K_d]=1,25, n casuale, D fisso. Verifica pesi e clustering. |
| 11–12 | Perdite rare iid, q=0,01 | 0,15; 0,20 | K_d=1. R=μ+1,25(q−I)/sqrt[q(1−q)], I∼Bernoulli(q). Media e varianza teoriche note, asimmetria negativa. |

Per AR(1), generare Z_1∼N(0,1), poi Z_d=ρZ_(d−1)+sqrt(1−ρ²)ε_d e R_d=μ+1,25 Z_d. Le innovazioni ε sono gaussiane standard indipendenti tra loro e dall'inizializzazione. L'inizializzazione è stazionaria. Non ricentrare il campione per forzare la media realizzata a μ.

Per celle 9–10, usare Z_d AR(1) stazionario con ρ=0,25 e R_di=μ+1,25[√0,5 Z_d+√0,5 ε_di], con ε_di gaussiane standard iid indipendenti da Z e K. Anche i conteggi K sono iid nel tempo. Formare S_d=Σ_i R_di e mantenere (0,0) quando K_d=0. L'estimando di lungo periodo E[S_d]/E[K_d] è μ. Questa versione non collauda conteggi dipendenti dai rendimenti: è un limite esplicito da coprire nella matrice finale se pertinente.

### Due candidati definiti per il solo pilota

**HAC candidato.** μ_hat=ΣS/ΣK, K_bar=ΣK/D, e_d=S_d−μ_hat K_d. Covarianze γ_hat_h=D^−1 Σ_(d=h+1…D)e_d e_(d−h). Kernel Bartlett con ritardo L=floor[4(D/100)^(2/9)]=6 a D=1.000. V_hat=γ_hat_0+2Σ_(h=1…L)(1−h/(L+1))γ_hat_h. SE=sqrt[V_hat/(D K_bar²)]. Limiti μ_hat±z_0,975 SE. Nessuna scelta del ritardo guardando quale passa. Denominatore nullo, V_hat non positivo o risultato non finito sono errori/non stimabilità da rendicontare, non promozioni. Formula e convenzione numerica devono essere controllate da Claude prima di implementarla. La regola dei ritardi è un candidato convenzionale, non una validazione.

**Bootstrap candidato.** Bootstrap circolare a blocchi sulle coppie giornaliere, blocchi di lunghezza ℓ=10, 100 blocchi estratti con rimpiazzo per ottenere D=1.000 coppie. Stessi pesi temporali per S e K. B=3.999 ricampionamenti interni per replica. Ricalcolare μ_hat* come rapporto delle somme. Usare intervallo basic: [2μ_hat−Q_0,975(μ_hat*), 2μ_hat−Q_0,025(μ_hat*)]. Quantile definito dall'inversa della distribuzione empirica, rango ceil(pB) nella sequenza ordinata, senza interpolazione. Non passare a percentile o studentizzato dopo l'esito. Un ricampionamento con denominatore nullo viene contato come fallimento della replica esterna, senza sostituirlo di nascosto. Per questa proposta, limiti non finiti, invertiti o intervalli di ampiezza nulla sono non stimabilità da rendicontare, non promozioni.

Sono due procedure candidate, non le uniche possibili. Il bootstrap basic può avere problemi con asimmetria e campioni finiti. B=3.999 dà circa 100 osservazioni per coda al 2,5%, ma non prova stabilità dei quantili. La sua casualità interna è parte del tasso misurato; la validazione finale deve collaudare la versione e B effettivamente impiegati. Quote più piccole richiedono un nuovo dimensionamento di B.

### Repliche, semi, versioni e tempi

Proposta: **M=3.000 repliche indipendenti per ciascuna delle 12 celle**, con stessi dati fra i due metodi per confronti appaiati. La motivazione è una precisione esplorativa vicina a ±0,6 punti percentuali al 95% per un tasso attorno al 2,5%, non la certificazione di quel tasso. Per una potenza attorno al 50%, la semilarghezza normale indicativa è circa 1,79 punti percentuali. Gli intervalli effettivi restano quelli esatti sotto indicati. Totale 36.000 serie esterne e 72.000 valutazioni di intervallo. Il bootstrap comporta **143.964.000** ricampionamenti interni. Questo costo non può essere nascosto nel termine «una replica».

Proposta riproducibile di semi: master seed intero **2026111706**, generatore PCG64 con implementazione e versione fissate. Derivare flussi con SeedSequence dalla tupla intera [master, fase, cella, replica, componente]. Indici cella 1…12 e replica 1…3.000, fase 1 per pilota. Componenti 0 per i dati iid/AR o la componente comune Z, 1 per i conteggi K, 2 per le innovazioni individuali nelle celle 9–10, 3 per il bootstrap. I flussi non pertinenti alla cella restano inutilizzati. I due metodi ricevono la medesima serie già generata; soltanto il bootstrap usa il suo flusso interno. Registrare lo schema esatto e l'ambiente. La riproducibilità non dimostra da sola indipendenza statistica, ma evita riusi accidentali dei flussi.

Prima della corsa, Claude deve fissare impronte di protocollo, implementazione, generatori e ambiente. Per benchmark di tempo usare fase 0, 30 repliche per cella e metodo, nessun riuso nel pilota, nessuna scelta del metodo dai risultati del benchmark. Misurare tempo mediano e coda, memoria e parallelismo. Se il preventivo è incompatibile col budget, riportarlo al titolare prima di lanciare il pilota. Non assumere «qualche ora» senza misura.

Il pilota non assegna semi alla futura validazione finale. Quelli saranno impegnati dopo il congelamento del metodo e prima della prima replica finale, con namespace distinto, senza recuperare semi del pilota. Modifiche durante il pilota sono versioni di sviluppo documentate. Errori non giustificano selezionare solo i semi favorevoli.

### Misure e lettura, fissate prima

Per ogni cella e metodo riportare M richiesto/eseguito, L>0,15, U<0,15, attraversamenti della soglia, copertura di μ vera, ampiezza mediana e quantili dell'intervallo, errori/non stimabilità, bias di μ_hat, n e sedute con trade, tempi. Conservare le osservazioni appaiate per confrontare i due metodi e rendicontare i casi discordanti.

Al confine μ=0,15, misurare separatamente falsa promozione e falsa bocciatura. Sotto soglia, promozioni restano false; sopra soglia, il loro tasso è potenza dell'intervallo. Il residuo fra i due attraversamenti è inconclusività statistica. Gli errori sono una categoria distinta. Non chiamare queste frequenze verdetti completi di DA-31, perché qui mancano minimi informativi operativi e veti della strategia.

Per ogni tasso fornire **Clopper–Pearson bilaterale descrittivo al 95%**, senza rivendicare copertura simultanea su tutti i confronti. A M=3.000 e p=0,025 l'errore standard è circa **0,285 punti percentuali**. Se si osservano 75 eventi, l'intervallo esatto è circa **[1,9714%; 3,1238%]**. Un 2,5% osservato non certifica p≤2,5%. Gli intervalli esatti derivano dall'inversione binomiale [S1].

Ogni replica resta nel denominatore. Per gli errori dare sia eventi/M sia (eventi+errori)/M, come estremi descrittivi se ogni errore potesse nascondere un evento. Riportare separatamente il tasso fra repliche valide. Non validare un metodo perché gli errori abbassano la frequenza di promozione.

**Regola d'uso del pilota:** nessuna accettazione definitiva. Una cella con limite descrittivo inferiore del tasso di falsa promozione sopra a è un segnale da investigare, non una certificazione simultanea di fallimento. Un limite superiore sotto a è evidenza preliminare, non autorizzazione all'uso. Confrontare anche potenza a +0,20, falsa bocciatura al confine, errori e costo. Un metodo che non promuove mai non vince il confronto. Se entrambi appaiono plausibili, presentare il compromesso al titolare senza selezionare automaticamente il più favorevole. Se un metodo viene modificato, registrare versione e motivazione.

Dopo il pilota, il titolare potrà fissare dominio, γ, p*, probabilità di superamento desiderata, budget fra tentativi, K effettivo e M della validazione indipendente. Per una sola conclusione positiva si può proporre un piano a una coda; per conclusioni positive e negative simultanee si mantiene una ripartizione dichiarata. I risultati del pilota non possono diventare la validazione dello stesso metodo selezionato su di essi.

**Limiti residui:** questo pilota non copre dipendenza negativa o molto persistente, code a varianza infinita, regimi, buchi, selezione fra strategie o quote successive. Non dimostra il controllo globale del programma. HAC è asintotico e la scelta automatica dei ritardi può mostrare distorsioni in campioni finiti [S2]. La matrice finale dovrà coprire il dominio realmente rivendicato o dichiarare ciò che esclude.

## 2d. «Vecchi prima» contro «recenti prima»

Entrambe sono proposte. La cronologia è una proprietà nota, la somiglianza effettiva dei mercati non è dimostrata dalla distanza temporale. Non si possono dedurre liquidità, volatilità, costi o vantaggio dai soli metadati di copertura.

| Tema | Vecchi prima, recenti protetti | Recenti prima, vecchi protetti |
|---|---|---|
| Domanda della prima prova | Trasferibilità indietro rispetto allo sviluppo recente. Può essere severa, ma una bocciatura in un vecchio contesto non dimostra assenza di vantaggio oggi. | Prova temporalmente più vicina allo sviluppo. La maggiore vicinanza non dimostra identico regime o replicabilità. |
| Impiego della quota maggiore | Viene usata sul periodo più lontano dall'uso futuro. Potrebbe consumare risorse su una domanda meno pertinente. | Viene usata sul periodo più recente della riserva, se l'obiettivo è la pertinenza temporale della prima prova. |
| Valore della parte protetta | Conserva l'evidenza storica più recente per una prova successiva, con quota inferiore e fabbisogno maggiore. | Conserva evidenza più antica, utile soprattutto alla trasportabilità storica. Non equivale a una conferma prospettica dopo la prima prova. |
| Copertura | Gli anni antichi potrebbero avere copertura peggiore, ma qui non è verificato. Esclusioni possono rendere impossibile la prima finestra. | Possibile maggiore capienza iniziale se il rendiconto la dimostra. Rischio di lasciare alla seconda quota una parte antica insufficiente. |
| Adattamento dopo il primo esito | Le scelte per il secondo tentativo possono essere influenzate dalla prima lettura. Serve un disegno valido per l'adattamento. | Stesso rischio. Spostarsi indietro non rende i dati indipendenti dalla selezione effettuata. |
| Trasferimento al futuro | Nessuna garanzia automatica. | Nessuna garanzia automatica. |

L'indicazione «2005–2010» come seconda finestra è un esempio di Claude, non un confine già dimensionato. Nessuna parte viene qui assegnata.

### Informazioni ammesse per la scelta

Richiedere soltanto un **rendiconto annuale di copertura**, prodotto dal custode nel mandato tecnico già previsto, con:

- anno e frazione di anno coperta, calendario/sessione/versione e denominatore di sedute e minuti attesi;
- sedute e minuti presenti BID, ASK e nell'intersezione, mancanti, non leggibili o in quarantena, senza valori delle quotazioni;
- distribuzioni annuali aggregate della completezza e dei buchi, con definizione degli intervalli e conteggio dei buchi ai bordi, senza date intraday o segnali;
- quota di sedute valutabili sotto la regola di idoneità **già giustificata e congelata**, oppure stato «idoneità non ancora definita»;
- conferma del custode se i blocchi annuali candidati possono formare una finestra contigua utilizzabile e con quale capacità, senza rilasciare contenuti di prezzo. Un totale annuale da solo non localizza i buchi e non dimostra continuità;
- versione e impronta del rendiconto e limiti delle verifiche.

Questi sono metadati di copertura, non spread, volatilità, distribuzioni dei rendimenti, conteggi dei trade della candidata o profitti. Non chiedo ora la loro produzione o accesso ai dati. L'inventario di presenza può precedere la scelta delle soglie. La soglia non deve essere ottimizzata per far entrare l'anno desiderato. Se l'idoneità richiede controlli di valori eseguiti dal custode, al DGS arriva solo lo stato aggregato autorizzato, senza prezzi.

Per tradurre capacità in potenza si possono usare solo le stime già autorizzate dello sviluppo e ipotesi sintetiche motivate. La copertura annuale non stima frequenza dei segnali, varianza o dipendenza della strategia nella riserva. Senza un'ipotesi giustificata di trasferibilità, quella traduzione resta uno scenario.

### Procedura di scelta proposta

1. Prima di vedere esiti della riserva, il titolare chiarisce la domanda prioritaria: prima prova temporalmente vicina all'uso, oppure mantenere la parte storica più recente intatta per una seconda prova.
2. Con quote, m, criteri annuali e ipotesi di frequenza dichiarati, dimensionare **entrambe** le finestre, incluso il maggior fabbisogno della seconda quota. Non definire «protetta» una porzione incapace di sostenere la domanda prevista.
3. Con il solo rendiconto di copertura, valutare se ciascun ordine è fattibile. Se entrambi lo sono, scegliere in base alla domanda del punto 1, non a presunte opportunità di mercato. Se nessuno consente due prove, esplicitare la scelta fra una sola verifica storica e raccolta prospettica, senza ridurre requisiti per ottenere artificialmente due finestre.
4. Congelare ordine, confini, esclusioni, riscaldamento, consumo, quota e regole per esiti inconclusivi prima di ogni lettura di prezzo o risultato. Se servono confini subannuali precisi, il custode li determina secondo la regola già fissata; un totale annuale non basta per sceglierli al giorno.

**Parere del DGS:** non raccomando oggi un ordine definitivo. «Vecchi prima» protegge un'opzione temporalmente più recente, ma non è metodologicamente superiore in assoluto. «Recenti prima» può essere coerente con la pertinenza della prima prova, ma lascia una seconda prova con significato diverso e potenzialmente meno capacità. Il prossimo elemento necessario è il rendiconto ammesso e la domanda del titolare, non i prezzi della riserva.

## 3. Seconda revisione interna, dopo la stesura

Ho riletto la bozza rispetto alla consegna, ricontrollato i risultati numerici e cercato contraddizioni fra le sezioni. Questo è un autocontrollo dello stesso revisore, non una seconda revisione indipendente.

| Controllo | Esito e limite |
|---|---|
| Errori reali contro differenze innocue | Correzioni di ceil mantenute. F≈1,66 trattato come approssimazione dichiarata. I nove M di Claude sono riconosciuti sufficienti, non denunciati come errori. |
| Binomiale e quantili Beta | Doppio calcolo delle soglie di passaggio ai valori riportati, con la stessa libreria numerica. Concordanza riscontrata. Non è una replica con implementazione indipendente della libreria. |
| Significato dei minimi Monte Carlo | Precisato che il primo M non garantisce q≥90% per ogni M maggiore e che 90% per cella non è congiunto. Nessun risparmio imposto. |
| Due incertezze distinte | Separati a/b del test della strategia da δ/γ del collaudo del tasso. Il pilota usa intervalli descrittivi, non la certificazione simultanea della specifica finale. |
| Decisioni del titolare | b=a, un riesame, 12 celle, L=6, ℓ=10, B=3.999, M=3.000 e semi sono tutti proposti. Nessuna modifica normativa applicata. |
| DA-31 | Chiarita la precedenza del veto valido, la richiesta dei minimi per i verdetti statistici e l'uguaglianza alla soglia. Esplicitato il costo conservativo della regola. |
| Contatori e dati nuovi | N, j e m separati. Nessun azzeramento, rimborso o pooling automatico. Nuove date non equiparate a indipendenza. |
| Pilota | D distinto da n nelle celle con conteggi casuali. Controllate le scale marginali dei generatori. Nella seconda lettura precisati distribuzione delle innovazioni, componenti dei semi, trattamento degli intervalli degeneri e motivazione di M=3.000. Distinti repliche esterne e bootstrap interni. Nessuna simulazione eseguita. |
| Destinazioni P3 | Non inventati numeri di sezioni assenti dai testi autorizzati. §8 identificato dal dossier; gli altri inserimenti hanno destinazione funzionale da confermare da Claude. |
| Confini operativi | Nessun codice o dato di progetto letto/modificato. Nessun incarico a Gemini, nessuna riapertura di H-002 o D-24. |

**Autocritica residua.** I metodi e il pilota proposti sono più definiti, ma non validati. I parametri sintetici hanno valore diagnostico, non rappresentatività dimostrata del mercato. I requisiti sul controllo globale, sulla selezione e sulla dipendenza restano da soddisfare prima di rivendicare quella garanzia. Il costo effettivo attende un benchmark autorizzato. Il titolare può respingere o ridimensionare le proposte prima dell'esecuzione.

## 4. Letture ed evidenze

**Letto per intero in questa revisione:** `7-RISPOSTA-AL-DOSSIER-DGS-05.md`; `DGS-05.md`; `DGS-05-addendum-metodo.md`; `DGS-specifica-collaudo-IA02.md`. I precedenti documenti del DGS sono fonti delle mie proposte storiche, non prove dello stato attuale del progetto.

**Letto in parte:** `PASSAGGIO-A-CLAUDE-DGS-20261117.md`, introduzione di coordinamento e inizio dell'allegato A; fonti statistiche pubbliche S1–S2 nei passaggi sulle formule e sui limiti metodologici, senza lettura integrale degli articoli scientifici collegati.

**Non letto in questa revisione:** pacchetto ZIP, codice del progetto, repository, worktree, documenti sigillati, attuale modello H-003, registri correnti, mandato e risultati R15, log del Mac, cache o dati di sviluppo/riserva. Nessun risultato tecnico di Claude è stato replicato. L'integrità 369/369 resta una verifica storica del DGS-05, non ripetuta qui.

**Ricalcolato:** campioni normali e AR(1), rapporto delle quote, soglie di potenza illustrative, tutti i nove budget di repliche, nove primi M esatti secondo la convenzione dichiarata, probabilità di passaggio al nominale, precisione illustrativa del pilota e conversioni dei tempi. Nessuna quotazione utilizzata.

### Fonti pubbliche di metodo

- **[S1] NIST**, [Exact binomial confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm) e [Confidence intervals](https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm). Supportano l'inversione binomiale e la distinzione delle code, non i budget di governance proposti. I numeri delle tabelle sono ricalcoli del DGS.
- **[S2] Newey e West**, [Automatic Lag Selection in Covariance Matrix Estimation](https://www.nber.org/papers/t0144). Supporta il limite della sola giustificazione asintotica e segnala distorsioni nelle simulazioni. Non valida la specifica candidata di questo documento.

**Consegna al titolare:** questo testo è pronto per il confronto con Claude. Richiede decisioni esplicite sui parametri metodologici prima di diventare norma o mandato di esecuzione. Non modifica il lavoro tecnico già in corso.
