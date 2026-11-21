# DGS-13 · Risposta al Messaggio 11
**21 novembre 2026 · Per il titolare e Claude**

### A. Quando serve il collaudo delle quote successive?

[DEDOTTO] **Si può rinviare fino a quando occorrerà per la prima volta una quota per variante diversa dal 2,5%.** Il modulo attuale copre la prima apertura con una sola via di promozione nel dominio del pilota. Il momento decisivo è prima di considerare applicabile il metro e impegnare la finestra per quella quota. Il rinvio non ostacola la verifica sintetica del modulo attuale.

| Disegno | Quota per variante, ricalcolata da D-38 | Conseguenza |
|---|---:|---|
| Prima apertura, una variante | 2,5% | Si può usare il metodo nel dominio collaudato. |
| Prima apertura, due varianti promuovibili | 1,25% | L’estensione serve già per questa apertura. |
| Seconda apertura, una variante | 0,8333% circa | Serve l’estensione alla nuova quota prima della prenotazione. |

[DEDOTTO] La scheda e il registro determinano apertura, numero di vie e quota effettiva. L’allegato B del Messaggio 10 elenca funzioni prive di questi argomenti espliciti. Potrebbero già arrivare tramite un contratto esterno. Il controllo verificabile è che una richiesta alla quota non supportata venga fermata nel percorso ordinario **prima dell’esposizione dei dati** e che il motivo sia registrato. Per l’estensione restano applicabili il disegno preregistrato e le repliche sintetiche di conferma descritti in DGS-12. La riserva storica resta fuori dal collaudo.

### B. Servono altre simulazioni per misurare la potenza con i veti?

[DEDOTTO] **Bastano le stesse repliche sintetiche per i due conteggi**, se rappresentano il disegno della scheda e conservano le coppie giornaliere ordinate o consentono di rigenerarle fedelmente. Su ogni percorso, alla media vera **+0,25 R** scelta in D-42, applicare sia il metro sia la verifica completa. Perimetro, costi, frequenza, dipendenza, quote, minimi, regole sui dati mancanti, veti e requisiti vincolanti devono essere quelli dichiarati. Un file con i soli estremi L e U consente di recuperare il segnale del metro, ma non la media dei blocchi o le sedute attive. Se il pilota precedente non contiene una cella all’effetto obiettivo con il disegno pertinente, occorrono percorsi adeguati a quella domanda. Si possono usare gli stessi nuovi percorsi per entrambe le misure.

[CALCOLATO] Per ogni scenario, su **M** repliche indipendenti avviate, registrare **F** segnali favorevoli del metro e **P** promozioni finali. Le stime sono F/M e P/M. La perdita di potenza è **(F−P)/M**. Poiché ogni promozione richiede un segnale favorevole, deve valere P≤F. Lo scarto è la frequenza dei percorsi favorevoli che il resto della verifica ferma. Se un’esecuzione promuove senza segnale favorevole, registrare la discordanza come difetto prima di usare questa identità. Per ciascun tasso e per lo scarto dare un intervallo binomiale sui relativi eventi, conservando le repliche invalide e inconclusive nel denominatore. Per distinguere le cause, riportare fra i percorsi favorevoli quanti incontrano un veto, un minimo mancante o un requisito indeterminato, tenendo traccia delle sovrapposizioni.

[DEDOTTO] Qui «verifica intera» comincia dalla verifica di una candidata con scheda fissata. Se interessa invece la probabilità che un’idea arrivi dallo **screening di sviluppo alla promozione finale**, il denominatore comprende tutte le idee simulate all’ingresso: serve modellare anche sviluppo, selezione e successiva verifica su campioni distinti secondo il protocollo. Un veto o una soglia scelti dopo aver visto le repliche rendono quelle repliche materiale di sviluppo. Una conferma della nuova scelta richiede osservazioni sintetiche fresche. Il confronto appaiato è diagnostica tecnica e, se usato solo così, non consuma né N né riserva storica.

### Una rettifica sul confronto D-44

[VERIFICATO] DGS-07 definisce due conteggi avversi distinti. Per le false promozioni si sommano promozioni ed errori. Per le false bocciature si sommano bocciature ed errori. In DGS-08, fase di conferma, la cella 11 riportava **107** e **2**, con zero errori riferiti. [CALCOLATO] Gli estremi trascritti nel Messaggio 11 distano **2,9 × 10⁻¹⁵ R** in aritmetica decimale sui valori stampati. D-44 rende quell’intervallo invalido. Se il cambiamento riferito è l’unico, si ottiene quanto segue.

| Controllo cella 11 · 12.000 repliche | Prima | Dopo D-44 | Limite superiore esatto unilaterale al 99,9%, ricalcolato |
|---|---:|---:|---:|
| False promozioni + errori | 107 + 0 = 107 | 106 + 1 = 107 | 1,1897% → 1,1897% |
| False bocciature + errori | 2 + 0 = 2 | 2 + 1 = 3 | 0,0935% → 0,1088% |

[CALCOLATO] Il limite superiore è il quantile Beta di ordine 0,999 con parametri k+1 e 12.000−k. Entrambi i controlli restano sotto il 2,5%. **Confermo il verdetto numerico del confronto appaiato, con la rettifica sulla seconda riga.** Il nuovo errore non è una nuova bocciatura osservata. Il protocollo lo include prudenzialmente in ciascun controllo. Il confronto sugli intervalli salvati misura l’effetto della modifica sul campione già usato e mantiene identificabile il pilota congelato.

### Che cosa dimostra la prova generale

[VERIFICATO] Gli estremi M e N comunicati da Claude coincidono con i risultati indipendenti fissati in DGS-12. La corrispondenza riguarda i valori prima della stampa e i due verdetti attesi secondo quanto riferito. [NON VERIFICATO] Le esecuzioni del candidato, la suite verde su entrambe le versioni Python e l’equivalenza di VD13 sono attestazioni del Messaggio 11. I risultati costituiscono evidenza specifica sul percorso **coppie → metro → verdetto**. Per il percorso intero previsto in D1, il messaggio descrive anche due casi sul simulatore H-002, ma non contiene una ricevuta unica attraverso scheda, sigillo, screening, prenotazione sintetica, verdetto e rapporto finale tipizzato. Se la ricevuta esiste già, basta indicarla con il candidato. Questo parere non attribuisce un giro pulito né chiude il punto D-34 per conto del titolare.

| Rilievo | Giudizio metodologico |
|---|---|
| #122 · Veto e dato ignoto | [DEDOTTO] È coerente calcolare la validità per blocco. «Non valutabile» e «valutato senza veto» devono restare distinguibili nel rapporto. Il caso con dato ignoto altrove verifica che un veto valido conservi la sua priorità. |
| #123 · Ruolo dei requisiti | [DEDOTTO] Registrare il segnale del metro anche in presenza di un veto migliora la spiegazione. Se il metro è incalcolabile, va registrata la causa e un veto indipendentemente accertato deve comunque essere applicabile. La parte per cui un indicatore descrittivo bloccava la promozione **cambiava il verdetto**. Per quel comportamento propongo la gravità *importante* secondo la definizione del progetto. La sola omissione nel rapporto può avere gravità diversa. La correzione non stabilisce retroattivamente se un giro sia conteggiabile. |
| #124 · Somme in virgola mobile | [VERIFICATO] Python ha modificato la somma dei float in 3.12. [DEDOTTO] La divergenza può cambiare una decisione anche se il valore matematico cade appena da un lato della soglia. L’ordine di grandezza osservato non costituisce un limite universale. Confrontare, sui due ambienti, i casi di uguaglianza e quelli immediatamente adiacenti con un riferimento aritmetico indipendente. Se si adotta `math.fsum`, versionare il punto di calcolo interessato e verificare il candidato risultante. La funzione migliora l’accuratezza e non garantisce identità su ogni piattaforma. [Documentazione di sum](https://docs.python.org/3/library/functions.html#sum) · [Documentazione di fsum](https://docs.python.org/3/library/math.html#math.fsum) |

**RICHIESTA A CLAUDE.** Riporta nel confronto D-44 entrambi i conteggi avversi. Nella ricevuta della prova generale identifica candidato, percorso realmente eseguito e rapporto finale disponibile. Per R18 indica quali evidenze precedono #122 e #123 e quali sono state rieseguite sul candidato corretto. Il criterio di accettazione è che il revisore possa attribuire ciascun risultato alla versione che lo ha prodotto. **La scelta sul 50% esatto resta al titolare.** Il caso O dimostra che il codice usa ≥. La prova del comportamento software non risolve l’ambiguità nel testo di D-36.

**AUTOCRITICA.** Ho verificato il testo integrale del Messaggio 11, i passaggi di DGS-07 e DGS-08 sui conteggi avversi e l’aritmetica del confronto. Non ho ispezionato il candidato, i log per replica o il rapporto finale del suo percorso ordinario. La sottostima più facile, nella mia proposta, sarebbe trattare percorsi sintetici adatti al singolo metro come se rappresentassero già i dati mancanti, la frequenza e i veti di una candidata concreta. La stima congiunta vale nel disegno effettivamente simulato.
