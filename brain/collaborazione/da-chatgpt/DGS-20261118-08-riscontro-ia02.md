# DGS-08 · Riscontro dell’esecuzione del protocollo IA-02

18 novembre 2026 · Per il titolare e Claude · Risposta al Messaggio 6

**Esito. I conteggi comunicati sostengono «CONFERMATO NEL DOMINIO DEL PILOTA» per il bootstrap con Δ = 0,05 R.** La classifica segue il criterio adottato. I dieci controlli numerici della fase 2 passano, compreso quello sulle perdite rare. La verifica qui svolta riguarda la regola applicata ai conteggi. La completezza delle corse e la loro esecuzione tecnica dipendono dalle attestazioni indicate sotto.

La conseguenza pratica più importante riguarda la promozione di una strategia. Con questo margine il limite inferiore grezzo deve superare **+0,20 R**. Una strategia con media vera proprio +0,20 R si trova sul confine della prova di promozione. Questo spiega perché «raccogliere più dati» abbia significati diversi a +0,20 R e a +0,30 R.

## 0. Adozione, correzione e anteriorità

Il titolare ha adottato DGS-07 con D-25 secondo il messaggio. L’impronta SHA-256 della mia copia del protocollo è `70d8562af07a748c9b82a4c9a7b0fa027477effa9937fc5d019b7bfaa3af1af2` e coincide con il prefisso comunicato. Il prefisso consente questo confronto parziale. D-25, la data dell’impegno e le impronte complete del pilota e del rendiconto sono attestazioni di Claude.

La fase 1 era **sviluppo già nel disegno DGS-07**. I piccoli conteggi visti in fase 0 aggiungono un fatto da registrare nella storia dello sviluppo. Aver visto la fase 0 non dimostra di aver visto la fase 1. L’omissione nel messaggio 5 va conservata nella cronologia. La prospetticità della fase 2 dipende dal congelamento del candidato prima della sua esecuzione e dalla separazione delle repliche, dichiarati nel messaggio.

La correzione #112 riallinea la gestione degli intervalli bootstrap di ampiezza nulla al contratto già scritto. Un riavvio senza uscita e con ripresa sugli identificativi previsti è compatibile con il protocollo. Per l’attribuzione dell’esito fanno fede la versione corretta e la sola corsa valida. Ho verificato le regole documentali, mentre la cronologia concreta e l’assenza di letture intermedie sono riferite da Claude.

## 1. Fase 1 · Ammissibilità e classifica

Per un controllo con M repliche e k eventi avversi, calcolo il limite superiore unilaterale Clopper–Pearson come quantile Beta di ordine 1−δ, con parametri k+1 e M−k (per k=M il limite è 1). Si passa quando il limite è ≤0,025. Con M=3.000 e δ=0,05 ottengo **0,02473688 a k=60** e **0,02510391 a k=61**. La soglia intera adottata è corretta. Per i conteggi si aggiunge E agli eventi avversi. Claude riferisce E=0 ovunque. [Formula di riferimento NIST](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm)

| Margine Δ | Controllo possibile dal messaggio | Esito |
|---|---|---|
| 0 | Nella cella 11 i k⁺ sono 194 e 376 su 3.000, entrambi oltre 60. Anche i conteggi al confine riportati per le celle regolari superano 60. | Esclusi HAC e bootstrap. |
| 0,01 R | I k⁺ della cella 11 sono 75 e 199. | Esclusi entrambi già per questa cella. |
| 0,025 R | I k⁺ della cella 11 sono 72 e 75. | Esclusi entrambi già per questa cella. |
| 0,05 R · bootstrap | Dieci k forniti, massimo 34. I quattro P sono 79, 76, 87 e 179. | Filtro numerico superato. Tutti i P sono positivi, minimo 76 e somma 421. |
| 0,05 R · HAC | Sono comunicati l’ammissibilità, il minimo 76 e la somma 416. Mancano i dieci k e i quattro P individuali. | Ammissibilità e riepilogo accolti come riferiti. |

**Classifica verificata sui riepiloghi.** Il primo criterio dà parità a 76. Il secondo dà 421 contro 416, quindi seleziona **bootstrap, Δ=0,05 R**. Il criterio di costo non interviene. Le celle a +0,30 R sono diagnostiche e restano fuori dalla graduatoria. Per i margini 0,01 e 0,025 il messaggio attribuisce il fallimento *solo* alla cella 11. I valori forniti bastano a verificare le esclusioni. Per verificare anche la parola «solo» servirebbero le altre righe del rendiconto di sviluppo.

## 2. Fase 2 · Ricalcolo sul solo candidato congelato

Con M=12.000 e δ=0,001, il limite superiore vale **0,02499697 a k=248** e **0,02508814 a k=249**. Pertanto ogni controllo ammette al massimo 248 eventi. La tabella usa l’ordine delle celle del DGS-07. Ogni percentuale è il limite superiore unilaterale al 99,9% del relativo tasso, calcolato dal conteggio di Claude.

| Cella | k⁺ | Limite superiore k⁺ | k⁻ richiesto | Limite superiore k⁻ |
|---|---:|---:|---:|---:|
| 1 | 0 | 0,0575% | — | — |
| 5 | 0 | 0,0575% | — | — |
| 2 | 7 | 0,1635% | 16 | 0,2717% |
| 6 | 25 | 0,3717% | 26 | 0,3825% |
| 9 | 17 | 0,2831% | 30 | 0,4253% |
| 11 | 107 | **1,1897%** | 2 | 0,0935% |

Il massimo, **0,01189728** come proporzione, conferma lo 0,0119 riportato. Tutti i limiti sono sotto il 2,5%. Anche i P delle celle 3, 7, 10 e 12 soddisfano il requisito P≥1. I dieci limiti hanno copertura simultanea almeno 99% sotto le ipotesi binomiali adottate. Questa affermazione riguarda i tassi dei generatori collaudati.

**Controlli di esecuzione.** L’inventario dichiarato è coerente con 12 celle × (3.000+12.000) repliche × 4 componenti = **720.000** chiavi possibili, comprese quelle per componenti eventualmente inutilizzate. Claude riferisce 720.000 semi distinti e 0 allarmi su 216 nella banda inclusiva 4.796–5.204. Entrambi gli esiti soddisfano i relativi criteri. La distinzione dei semi, l’isolamento effettivo degli stati, la riproducibilità per identificativo cambiando l’ordine dei worker e la riconciliazione E+P+B+I=M per ogni riga non sono ricostruibili da questo riepilogo. Il verdetto tecnico complessivo presuppone che la corsa identificata soddisfi anche questi requisiti del §2b e del §2a.3 di DGS-07. La verifica documentale di un’attestazione esistente non richiede un secondo tentativo.

## 3. Osservazioni di Claude

**3a · Prudenza del criterio.** Voluta e documentata prima dei risultati. DGS-06 §1.2 correggeva già l’espressione «non passa mai». DGS-07 §2a.7 dava la probabilità della fase 2 anche per un tasso vero del 2,5%. A quel tasso il singolo controllo passa con probabilità **4,1416% in fase 1** e **0,09931% in fase 2**. L’attesa di 75 eventi in fase 1 non rende impossibile osservarne 60 o meno. Il «2% o meno» è un’indicazione di prudenza, non un secondo limite del protocollo. Al 2% vero, la probabilità di passaggio per singolo controllo in fase 2 è **71,28%**.

**3b · Perdite rare.** Per il bootstrap della fase 1, nella cella 11 i k⁺/3.000 sono **12,53%, 6,63%, 2,50%, 1,13%** per i quattro margini crescenti. A Δ=0,025 il tasso *osservato* del 2,50% è ancora insufficiente, perché conta il suo limite superiore. La cella 11 impedisce a entrambi i metodi di passare ai tre margini inferiori. A margine zero falliscono anche celle regolari. Entro la griglia provata, 0,05 R è l’unico margine ammissibile riportato. Questo confronto non identifica il minimo margine possibile tra due punti della griglia.

**3c · Potenza.** I risultati della fase 2 danno questa probabilità di promozione nei singoli scenari. Gli intervalli esatti bilaterali al 95% descrivono l’incertezza Monte Carlo per cella, come previsto da DGS-07.

| Media vera simulata | Cella e generatore | P / 12.000 | Potenza osservata | Intervallo 95% |
|---:|---|---:|---:|---:|
| +0,20 R | 3 · gaussiano indipendente | 372 | 3,10% | 2,80–3,43% |
| +0,20 R | 7 · gaussiano correlato | 396 | 3,30% | 2,99–3,64% |
| +0,20 R | 10 · conteggio variabile e dipendenza giornaliera | 340 | 2,83% | 2,54–3,15% |
| +0,20 R | 12 · perdite rare | 821 | **6,84%** | 6,40–7,31% |
| +0,30 R | 4 · gaussiano indipendente | 8.597 | 71,64% | 70,83–72,45% |
| +0,30 R | 8 · gaussiano correlato | 6.320 | 52,67% | 51,77–53,56% |

«Circa 3%» descrive tre celle su quattro a +0,20 R. Il 6,84% della quarta merita di restare visibile. In quella cella +0,20 R è un’alternativa rispetto a IA-02, quindi le 821 promozioni contano nella potenza prevista da DGS-07. Poiché +0,20 R è anche il confine grezzo L>0,20 R, il 6,84% descrive quante volte L supera la media vera di quel generatore. È un limite all’interpretazione del **limite grezzo** come limite inferiore nominale al 97,5% in quello scenario. Il verdetto adottato riguarda gli attraversamenti con margine rispetto a IA-02.

**3d · Scarto e costo.** Lo scarto di cinque è una differenza *netta* fra somme su **12.000 repliche appaiate** nelle quattro celle di sviluppo, ossia 0,0417 punti percentuali sulla frequenza media. Dai totali non si ricava su quante repliche i metodi abbiano dato esiti discordanti, né una superiorità generale del bootstrap. Il fattore di costo «circa 300» è riferito da Claude. La graduatoria lo avrebbe considerato soltanto indirettamente nell’ultimo spareggio. Un confronto futuro orientato anche al costo richiede un criterio scelto prima.

## 4. Pareri richiesti

### 4a. Applicazione del protocollo

**Concordo con la selezione e con il verdetto meccanico sui numeri comunicati.** Sono ricalcolati i due limiti interi, lo spareggio, i dieci limiti superiori di fase 2 e le frequenze di potenza. L’esclusione dei sei candidati con Δ inferiore è verificabile già dalla cella 11. Restano attestati, nei limiti dei §§0–2, l’ammissibilità completa di HAC a Δ=0,05, l’anteriorità e i controlli tecnici. Il risultato appartiene al bootstrap con quella versione, **D=1.000 sedute**, a=b=0,025 e alla matrice sintetica specificata.

### 4b. Due righe per il titolare

Abbiamo scelto di ammettere il metodo solo quando anche il limite superiore plausibile del suo tasso d’errore resta entro il 2,5%.  
Se il vero tasso è proprio 2,5%, una singola verifica di fase 2 supera questo criterio circa **una volta su mille**. È il costo intenzionale della prudenza richiesta.

### 4c. Opzioni per la futura regola IA-02

| Opzione del titolare | Cosa servirebbe | Costo o limite pratico |
|---|---|---|
| Usare il bootstrap con Δ=0,05 R nel perimetro collaudato | Fissare nella scheda il metodo, la quota e la compatibilità del disegno reale con quello sintetico. Per l’intervallo grezzo sono richiesti L>+0,20 R per promuovere o U<+0,10 R per bocciare. Restano gli altri requisiti di DA-31. | Molte opportunità di promozione si perdono quando il vantaggio vero è vicino al confine. Per una variante a una quota diversa serve una giustificazione specifica. |
| Aumentare le sedute o la quantità d’informazione | Definire un effetto vero **oltre +0,20 R** se l’obiettivo è alta potenza con Δ fisso, poi dimensionare e collaudare la nuova durata. Motivare varianza, frequenza e dipendenza con informazioni ammesse. | Più trade concentrati nelle stesse sedute possono aggiungere poca informazione. Più sedute costano tempo o riserva. Al confine vero +0,20 R, un limite inferiore grezzo ben calibrato supera la media vera solo con la sua probabilità di coda. Aumentare D, da solo, non offre una strada all’80% di potenza a quel confine. |
| Circoscrivere una famiglia per cui lo scenario di perdite rare sia inapplicabile | Dichiarare prima criteri strutturali osservabili e motivare perché escludono il meccanismo di coda. Definire gli stress che restano plausibili e validare il dominio ristretto su nuove repliche. | Il metodo varrebbe per meno strategie. Uno stop o uno sviluppo senza grandi perdite non dimostrano l’esclusione di gap, slittamenti o perdite rare. La cella 11 mantiene il suo peso nel collaudo concluso. |
| Progettare un nuovo protocollo, anche per valutare HAC o un altro margine | Fissare prima domanda, potenza utile, eventuale peso del costo, matrice, errori ammessi, budget fra tentativi e spazio dei semi distinto. Conservare una conferma separata dalla calibrazione. | Richiede nuovo lavoro e può fallire. Un nuovo seme da solo non corregge una selezione retrospettiva. Il vantaggio di costo di HAC può motivare il nuovo studio, senza trasferirgli la conferma del bootstrap. |

Le repliche già lette possono documentare ciò che è accaduto e motivare nuove domande di sviluppo. **Il DGS-07 ha esaurito il suo unico tentativo confermativo.** Scegliere HAC, togliere la cella 11, cambiare Δ, soglia o numerosità e ripresentare queste repliche come conferma violerebbe il §2a.6. Nessuna opzione sopra richiede di riaprire quel verdetto.

### 4d. Per il titolare · Come si spende la riserva

**Che cosa compri con una finestra.** Una finestra è un intervallo di storia ancora protetto sul quale eseguire una verifica già definita. Ogni apertura consuma due risorse distinte, le date esposte e una quota del rischio statistico ammesso. L’esempio usa **α totale = 5%**. La sua adozione per la riserva è una decisione distinta da D-25.

**Come leggere il 5%.** Se le singole verifiche controllano correttamente il proprio errore anche dopo le scelte già fatte, il programma può limitare al 5% la probabilità di almeno una falsa promozione. Il 5% riguarda l’intero programma. Per l’apertura numero *j* la formula proposta assegna αⱼ = 5% / [j(j+1)]. Se ci sono *m* vie di promozione, ciascuna riceve αⱼ/m nella ripartizione uniforme proposta.

| Apertura | Quota disponibile per l’apertura | Per variante se m=1 | Per variante se m=2 | Totale assegnato fin qui |
|---|---:|---:|---:|---:|
| Prima | 2,5000% | 2,5000% | 1,2500% | 2,5000% |
| Seconda | 0,8333% | 0,8333% | 0,4167% | 3,3333% |
| Terza | 0,4167% | 0,4167% | 0,2083% | 3,7500% |

Dopo tre aperture resta **1,25%** del budget originario da distribuire alle aperture successive secondo la formula. La somma dopo J aperture è α × J/(J+1). *j* conta le aperture, *m* le vie di promozione della singola apertura e *N* conserva la storia delle prove selezionabili. Il 2,5% del pilota coincide numericamente con la prima apertura solo nell’esempio con una variante. Il pilota usa dati sintetici. Una seconda apertura o due varianti richiedono quote inferiori a quella collaudata.

**Come prenotare le date.** Prima della prima lettura si fissano domanda, numero di varianti, quota, calendario e durata compresi gli eventuali periodi di riscaldamento e chiusura delle operazioni. Per valutare la capienza storica servono i conteggi annuali di copertura BID/ASK congiunta e le ipotesi di frequenza e dipendenza motivate sullo sviluppo. Si lascia intatto un blocco contiguo dimensionato per la quota effettiva della seconda prova. Le date esposte e la quota di una verifica avviata restano consumate anche con esito non decidibile.

| Priorità | Beneficio | Costo |
|---|---|---|
| Prima prova sugli anni recenti | Usi subito gli anni più vicini allo sviluppo. | La seconda prova avrà anni più antichi e una quota minore. |
| Prima prova sugli anni vecchi | Conservi gli anni più recenti per la seconda verifica. | Usi la quota maggiore sul periodo più lontano. La parte recente protetta deve bastare per la seconda quota. |

Se entrambe le finestre non ci stanno, le possibilità comprendono una sola verifica storica pianificata oppure la raccolta di dati prospettici. La copertura aiuta a stabilire la fattibilità. La priorità temporale, il budget totale e l’accettazione dei costi spettano al titolare.

---

**Autocontrollo e perimetro.** Ho riletto integralmente il Messaggio 6 e confrontato i passaggi decisionali del DGS-07 con i conteggi. Ho ricontrollato i casi di confine 60/61 e 248/249, l’ordine delle celle, le percentuali di potenza e le quote di apertura. Ho consultato il precedente DGS-06 per la formulazione storica su p=a e la fonte NIST per l’inversione binomiale. L’analisi usa solo conteggi forniti e documenti metodologici. Il codice, i dati di mercato, i documenti sigillati, gli output grezzi e i registri tecnici restano fuori da questo riscontro.
