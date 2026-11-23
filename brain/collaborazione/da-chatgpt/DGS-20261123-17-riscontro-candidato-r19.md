# DGS-17 · Riscontro al Messaggio 16 e parere sul candidato R19

23 novembre 2026 · Per il titolare e Claude · Seconda lettura con il Messaggio 16 integrale

**[DEDOTTO] Parere per il titolare.** La consegna è sufficiente per proporre a Gemini il giro indipendente su `1431190`, se il titolare ne autorizza l'avvio. Il materiale distingue il collaudo dell'esecutore sintetico, il calcolo della potenza per una futura scheda reale e il giro di revisione. Il primo è documentato da Claude, il secondo resta da implementare e il terzo attende la decisione del titolare. Per il punto 5 di D-34 il mio giudizio è favorevole alla descrizione del percorso esercitato. Per confermare in autonomia la riconciliazione mancano ancora gli originali indicati sotto.

**Metodo.** [CALCOLATO] Ricalcolo indipendente in Python sui numeri trascritti. [NON VERIFICATO] Identificativi, ambienti, stati del software, conteggi di esecuzione e nomi di casi sono letti nei documenti. [DEDOTTO] indica conclusioni metodologiche e proposte. Ho confrontato i tre allegati, la ricevuta precedente, DGS-14 e il passaggio su V10. Ho poi letto il Messaggio 16 originale. Q9 termina con «ricalcolare e confrontare?». La domanda è completa. Ho controllato sia il confronto con la dichiarazione sia quello con la soglia.

## Attribuzione e riconciliazione

| Evidenza | Riscontro |
|---|---|
| Prova ordinaria A–G | [NON VERIFICATO] L'aggiornamento dettagliato è su `4659dc8`. Il collaudo prepara sigillo e prenotazione e fornisce la potenza 0,6. Claude riferisce che l'esecutore produce screening, autorizzazione, coppie, verdetto, record e rapporto. Questo risponde alla domanda sulla provenienza della stima. |
| Calendario | [CALCOLATO] Fra l'8 febbraio 2010 e il 31 gennaio 2014 inclusi ci sono 1.040 feriali. Sottraendo i 40 riferiti si ottengono 1.000 sedute. [NON VERIFICATO] Festività e chiusure sono attribuite al calendario sintetico di H-002. La corrispondenza ordinata fra elenco impegnato prima della lettura e date delle coppie è riferita. I JSON sono nominati, senza essere allegati. [DEDOTTO] Per un riscontro indipendente confrontare direttamente gli elenchi, verificare unicità e, per i giorni senza operazioni, distinguere una seduta osservata con K=0 da una seduta con dati mancanti. La corsa A storica era descritta con un trade per seduta, quindi da sola non esercita il caso K=0. |
| Rapporti | [NON VERIFICATO] Claude riferisce uguaglianza in byte fra rapporto originale e rigenerato nello stesso ambiente. I prefissi delle impronte e i comandi permettono di localizzare la prova. Per controllarla servono record e rapporti originali, o accesso alla relativa cartella. | [DEDOTTO] La coincidenza di due stampe può riprodurre anche un errore comune. Per chiudere il confronto verificare dal record almeno identità dell'esecuzione, numero e ordine delle sedute, somma degli S divisa per somma dei K, segnale, veti e causa del verdetto riportati. La sola media delle medie giornaliere può differire quando il numero di trade varia.
| Mutanti | [CALCOLATO] 96+71+62+70 = 299 e 314−15 = 299. [NON VERIFICATO] La ricevuta di `1431190` dichiara campagne complete 299/299, 131/132 e 57/58 su ciascun ambiente. Sul candidato precedente 131/132 era un conteggio composto. [DEDOTTO] Sul nuovo candidato si cita la sua campagna completa. Se Gemini verifica la copertura, confronti anche gli identificativi dei gruppi con l'inventario e controlli le due equivalenze nel dominio degli input ammessi, incluso il comportamento osservabile in caso di errore. |
| Stato di D-51 | [NON VERIFICATO] La chiusura di PIANO-D51 parla ancora di corse in corso su `1080da8`. La ricevuta successiva identifica `1431190`. [DEDOTTO] Collegare la ricevuta finale dalla riga storica. Per attribuire anche A–G al candidato proposto, indicare la corrispondente esecuzione dopo le modifiche al lanciatore e ai registri, oppure includerla nel giro già previsto. |
| V10 | [DEDOTTO] Ritiro la richiesta a Claude di correggere una sua sintesi. ATTRIBUZIONE §5 usa correttamente «sostituito». DGS-14 lasciava aperta la domanda «sostituito o riclassificato». Nella mia successiva comunicazione al titolare ho parlato di «riclassificazione di V10». La formulazione da correggere è mia. |

## Q1 · Quale ambiente produce il risultato ufficiale

[DEDOTTO] Fissare **un singolo ambiente di riferimento** prima della verifica. Preferire l'ambiente Linux del collaudo IA-02 se dai suoi artefatti si ricostruiscono interprete esatto, architettura, dipendenze numeriche, codice, semi e configurazione e vi si riproducono i riferimenti congelati. «Linux» da solo lascia aperta la versione. Se l'ambiente storico non è ricostruibile, scegliere una singola immagine CI riproducibile, rieseguire i controlli di riferimento e documentare la qualificazione e le differenze prima dell'uso. Conservare l'altra versione CI e il Mac come riscontri di portabilità. Il Mac può avviare il lavoro e leggere il rapporto. Registrare l'identità dell'ambiente che calcola, separatamente dalla macchina da cui il titolare lancia la richiesta.

[CALCOLATO] Decodificando le quattro stringhe esadecimali della ricevuta, per L e per U la differenza assoluta è **5,662137425588298 × 10⁻¹⁵ R**, esattamente **102** passi binari alla loro scala. Entrambi i limiti inferiori, circa +0,3085695 R, superano +0,20 R. [NON VERIFICATO] Il verdetto completo concorde è riferito da Claude. [CALCOLATO] La stringa pubblicata per la media decodifica a **0,3836564999999758 R**. Scrivere «≈ 0,3836565 R». [DEDOTTO] L'uguaglianza dei bit tra ambienti e l'arrotondamento decimale descrivono confronti diversi.

## Q2 · Alternative per D-49

[NON VERIFICATO sul conto] il titolare risulta su Free con repository privato personale. [DEDOTTO dalla documentazione GitHub] Su questa configurazione la protezione server del ramo richiede un piano che la supporti. Un ramo dedicato identifica chi lavora a cosa. Per impedire materialmente l'unione prima della visione del titolare occorre che l'identità dell'agente non possa né aggiornare direttamente il ramo di destinazione né unire da sola né cambiare le regole. Verificare anche che la shell dell'agente non disponga delle credenziali del titolare. [Documentazione GitHub sui rami protetti](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

| Alternativa | Beneficio | Limite per l'obiettivo «il titolare vede la modifica» |
|---|---|---|
| A · identità dell'agente separata, il titolare approva | [DEDOTTO] Offre la separazione diretta fra autore e approvatore, se il server richiede l'approvazione umana sulla revisione ancora corrente e l'agente non possiede privilegi alternativi. | Gestione di identità e credenziali. Sul piano attuale una seconda identità con scrittura nello stesso repository non introduce da sola l'obbligo di approvazione. |
| B · richiesta di unione e test, zero approvazioni | [DEDOTTO] Traccia modifiche e controlli con poco lavoro umano. | Test verdi consentono comunque l'unione a chi ne ha il permesso. Una modifica congiunta a codice, test o workflow può rispettare i controlli configurati. La visione del titolare richiede che sia effettivamente l'unico a poter unire. |
| C · approvazione richiesta e deroga del titolare abituale | [DEDOTTO] Può mantenere un atto umano per ogni unione se solo il titolare dispone della deroga. | L'atto di deroga non attesta la lettura del contenuto e perde valore come segnale di eccezione se è sistematico. |

[DEDOTTO] Per tutte le alternative fare una prova su modifiche innocue al ramo o tag di test con i permessi effettivi, incluso un aggiornamento dopo l'approvazione. Se l'identità agente non ha scrittura sul repository autorevole e consegna una patch da esaminare, la separazione può essere ottenuta anche con più lavoro manuale. Se si usa un account macchina, verificare i termini applicabili. La scelta fra costo, attrito e protezione resta del titolare. [Termini GitHub per gli account](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)

## Q4 · Ricalcoli

[CALCOLATO] Ho sommato i float nell'ordine scritto con un accumulatore che esegue un'addizione alla volta, poi diviso per il numero di elementi. Ho confrontato questo risultato con `math.fsum(xs)/len(xs)` e con la media esatta delle `Fraction.from_float(x)`, usando la frazione della soglia float. L'accumulatore esplicito rende indipendente il significato di «sequenziale» dalla versione del built-in `sum`.

| Caso | Media sequenziale | Media con fsum | Media esatta e confronto |
|---|---:|---:|---|
| S1 | 0,25000000000000144 | 0,25 | 1/4, uguaglianza. Il sequenziale passa erroneamente il confronto stretto sulla media dello screening. |
| B1 | 0,2999999999999986 | 0,3 | 5404319552844595 / 18014398509481984, esattamente la soglia float 0,3. Il sequenziale farebbe scattare un veto con confronto stretto inferiore. |
| B3 | −0,25000000000000144 | −0,25 | −1/4, uguaglianza. Il sequenziale farebbe scattare il veto. |

[DEDOTTO] In questi tre esempi fsum dà il confronto atteso. L'esito della media da solo non determina l'intero screening. La rappresentazione della soglia deve essere coerente con quella degli input.

[CALCOLATO] Tabella DGS-14 del solo metro, per una variante, 1.000 sedute indipendenti con una operazione ciascuna, media vera +0,25 R, soglia +0,20 R e σ = 1,25 R. Con quota a = 0,05/[j(j+1)] e z = Φ⁻¹(1−a), SE massimo = 0,05/z e potenza = Φ(0,05√1000/1,25 − z).

| Apertura | Quota | SE massimo per potenza 50% | Potenza |
|---|---:|---:|---:|
| Prima | 2,5000% | 0,02551 R | 24,35% |
| Seconda | 0,8333% | 0,02089 R | 12,94% |
| Terza | 0,4167% | 0,01895 R | 8,48% |
| Quarta | 0,2500% | 0,01781 R | 6,15% |

[CALCOLATO] Limiti superiori esatti unilaterali al 99,9%, quantile Beta(0,999, k+1, 12.000−k): **1,189728%** per k=107, **0,093538%** per k=2 e **0,108806%** per k=3. I conteggi rettificati 107 e 3 restano entrambi sotto il 2,5%.

## Q8 · Copertura di D-51 e identità dello sviluppo

[DEDOTTO] La migrazione copre nel disegno le famiglie principali elencate. Una semplice impronta della directory sarebbe insufficiente. Il meccanismo descritto è più forte se consente di risalire dall'esito registrato ai byte effettivamente decodificati, all'insieme atteso di mercato, lato, date, esclusioni e riscaldamento, a uno snapshot di provenienza identificabile e alla stessa scheda, codice, ambiente e regola di screening. Verificare che una variazione fra screening e autorizzazione causi il rifiuto prima della lettura della riserva, anche al riuso di una registrazione precedente. Questo controlla l'identità. La qualità originaria dei dati richiede il consuntivo separato.

[DEDOTTO] Per valutare la completezza chiederei a Gemini di mappare le seguenti proprietà sui test già presenti, approfondendo soltanto quelle prive di un esito specifico.

- **Due richieste per la stessa ipotesi e variante.** Dopo il controllo preventivo, due processi con prenotazioni distinte possono trovarsi entrambi ammissibili. Dimostrare l'unicità al momento del consumo, anche se un domani la seconda quota fosse supportata. Cercare prima una prova esistente con due richieste della stessa ipotesi e variante che arrivano al passaggio di autorizzazione. Il caso D già descritto coinvolge ipotesi diverse e il secondo accesso si ferma per quota. Se serve isolare l'unicità a quota ammissibile, usare una prova sintetica mirata e dichiarare l'eventuale parametro simulato. Gli esiti attesi sono al massimo un'autorizzazione e un consumo, con causa di rifiuto attribuibile all'unicità. Questo controllo non richiede di estendere le quote operative. Distinguere la ripresa tecnica identica da una nuova verifica. Verificare anche che due ipotesi diverse nello stesso registro non siano bloccate per errore.
- **Due registri, un'interruzione.** Seguire la caduta fra scrittura dell'autorizzazione, registrazione della verifica, esito e rapporto. Controllare che le riprese riconcilino gli identificativi, conservino il consumo e producano al massimo un esito, anche se il primo rapporto non è scrivibile. Il paragrafo di completamento del piano cita soprattutto l'unicità per variante. Chiedere i riferimenti anche per esito unico e due ipotesi.
- **Percorso effettivo e custodia.** Identificare un caso positivo avviato dal lanciatore previsto sul candidato nuovo. [NON VERIFICATO] La storia è stata provata con un remoto finto e rete bloccata. [DEDOTTO] Questo esercita la logica Git. I permessi effettivi, l'autorità dello snapshot remoto e la protezione dei riferimenti in GitHub restano verifiche distinte. Un reflog locale offre evidenza limitata alla storia disponibile. Una nuova copia del repository deve poter riconoscere il riferimento autorevole o fermarsi quando manca.

[DEDOTTO] Per B distinguere rilascio esplicito tramite la funzione del registro e rilascio automatico al rifiuto del comando. La ricevuta cita un test di prenotazione abbandonata. Per G, conservare la traccia della correzione del catalogo che consente il nuovo tentativo prima dell'autorizzazione.

## Q9 · Contratto minimo per ricalcolare la potenza

[DEDOTTO] Sigillare **la ricetta riproducibile e la provenienza dei suoi input**. La procedura può essere implementata una volta nel codice versionato. La scheda ne porta identificativo, impronta e parametri. All'esecutore bastano i seguenti elementi, o riferimenti immutabili agli stessi.

| Campo del contratto | Contenuto minimo |
|---|---|
| Quantità e decisione | Definizione dell'evento stimato (segnale favorevole del metro oppure promozione completa), alternativa vera congelata, unità, verso del confronto, trattamento dell'uguaglianza e degli indeterminati. Se si riportano entrambe le potenze, identificare prima quale alimenta D-36 secondo la decisione vigente. |
| Dati ammessi e modello | Snapshot verificato del solo sviluppo ammesso, calendario e regola deterministica che ne stima frequenza, dispersione, dipendenza, costi e mancanze. Specificare come si impone l'effetto obiettivo conservando la struttura delle sedute. Ogni parametro fornito per ipotesi ha fonte e dominio dichiarati. |
| Disegno applicabile | Variante, finestra, quota prevista e sua applicabilità, minimi, veti, metro e versione. L'ingresso usa il vero effetto obiettivo fissato da D-42, non la media vincente ricavata dalla selezione sullo sviluppo. |
| Riproduzione | Versioni di generatore ed estimatore, ambiente di riferimento, semi e gestione dei flussi casuali, numero di repliche esterne e ricampionamenti interni, denominatore e regola per esiti invalidi. Se ci sono più scenari, fissare prima come concorrono alla decisione. |
| Ricevuta e confronto | Registrare input e impronte, eventi favorevoli F, promozioni P quando previste, repliche avviate M, incertezza e causa degli arresti. L'esecutore ricalcola prima dell'autorizzazione. Con un metodo Monte Carlo deterministico e semi fissati confronta gli interi attesi e ricalcolati, se dichiarati, e usa il tasso ricalcolato. |

[DEDOTTO] Per una soglia pari alla metà e M positivo, il confronto esatto si può fare come 2 × successi ≥ M usando l'evento previsto. L'intervallo d'incertezza accompagna il tasso. Usarlo come ulteriore soglia cambierebbe la regola e richiederebbe una decisione. Tenere separati il confronto di riproduzione (stessi input e conteggi) e l'ammissibilità al momento dell'autorizzazione. Se durante l'attesa cambia la quota per effetto di un'altra richiesta, ricontrollare sotto il blocco che la ricevuta della potenza sia riferita alla quota attuale e collaudata. Una stima riferita a una quota precedente non giustifica il consumo. Se il calcolo manca, è irriproducibile o il valore dichiarato è incoerente, registrare la causa e fermarsi prima del consumo. Prova di accettazione sintetica: stesso contratto e dati riproducono i conteggi, un valore dichiarato alterato viene rilevato, una quota incompatibile viene fermata e i casi al confine rispettano la regola.

[CALCOLATO] Nel controllo deterministico dei veti, con blocchi di uguale peso in trade, (−0,35 + 3 × 0,70)/4 = **+0,4375 R** per i livelli nominali. [DEDOTTO] È un buon modo per lasciare al metro un segnale favorevole mentre si esercita il veto. Il controllo omogeneo va confrontato alla stessa media effettiva. La prova documenta la logica del veto e non stima la probabilità di promozione all'alternativa di +0,25 R. Con blocchi di numerosità differente il riferimento va pesato per trade.

**Consegna minima.** Per la riconciliazione D-34 bastano i JSON originali già nominati con calendario, record e rapporti sintetici pertinenti, oppure un unico archivio con quei file e l'indice delle impronte. Per R19, se autorizzato, Gemini riceve separatamente requisito, candidato e materiali consentiti secondo la procedura cieca. Il riscontro completo del DGS è destinato al titolare e Claude.

**Autocritica.** I calcoli controllano l'aritmetica dei valori pubblicati. Non ho eseguito il candidato né confrontato i byte dei rapporti o gli elenchi originali delle sedute. Le possibili lacune di Q8 sono domande discriminanti per il revisore. Nessuna è qui classificata come difetto riprodotto. Nella seconda lettura ho ricontrollato i confronti in frazioni, i passi binari con la distanza fra rappresentazioni intere, le probabilità normali e i limiti Beta con inversione della distribuzione binomiale. I risultati pubblicati coincidono agli arrotondamenti indicati.
