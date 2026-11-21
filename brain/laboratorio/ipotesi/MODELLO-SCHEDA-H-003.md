# Modello di scheda per H-003 (e ipotesi successive)

**Stato del modello:** bozza di Claude, 16/11/2026. **Non ancora approvato nel suo insieme.** Il 19/11/2026 il titolare ha approvato e fatto applicare tre parti, nel testo di DGS-10 §3 (D-32): §0 «Provenienza» (G), §2 «Stato della finestra» (H) e §11 «Tracciabilità dei giri» (F). Le altre modifiche proposte (A–E, I, J) restano in `MODELLO-SCHEDA-H-003-BOZZA-P3.md` e in DGS-10. Il 19–20/11 il titolare ha preso le decisioni che le riguardano (D-35 esiti, D-36 screening, D-37 minimi e anni, D-42 obiettivo, D-43 code). **Il 20/11 è stata applicata solo la clausola sulle code (D-43, §5);** il testo delle altre si integra dopo la risposta del DGS al messaggio 10. Non contiene nessuna idea: la parte «Ipotesi» la scrive l'utente.
**Da dove viene:** struttura di H-002 v3.1, più le lezioni pagate con H-002:
- la soglia IA-02 (`governance/IMPEGNI-ANTICIPATI.md`);
- il difetto DGS-03 (uscita scelta guardando il futuro, #42);
- l'incidente del 14/11 (#41);
- la regola d'uscita per il sigillo (proposta v3.2 §C);
- il calcolo di potenza (`studi/risultati/potenza_IA-02.md`).

**Come si usa:**
1. Si copia in `H-003-<nome>-v1.md`.
2. Si compila ogni campo `[DA COMPILARE]`.
3. Le parti marcate **OBBLIGATORIO** non si tolgono e non si ammorbidiscono: per cambiarle serve una decisione scritta dell'utente, presa **prima** di guardare i dati di H-003.

---

# H-003 v1 · [DA COMPILARE: titolo in una riga]

**Stato:** bozza; **da sigillare** solo alle condizioni del §11.

## 0. Origine e contaminazione (OBBLIGATORIO, prima di tutto il resto)
- **Chi ha avuto l'idea, quando, guardando cosa:** [DA COMPILARE: persona, data, strumento (es. TradingView), mercato, **periodo esatto guardato**].
  - Guardare solo dal 15/11/2023 in avanti. Uno sguardo a grafici dal 2005 al 31/10/2023 va dichiarato qui. Se riguarda l'idea, la riserva per questa ipotesi è compromessa.
- **Chi ha scritto la scheda:** [DA COMPILARE]. Il revisore che giudica l'idea (il DGS, Gemini) **non** può esserne anche l'autore.
- **Esplorazioni già fatte sugli stessi dati** (`studi/REGISTRO-ESPLORAZIONI.md`):
  - E-001 sessioni;
  - E-002 micro-range;
  - **E-003**, i tagli di Gemini su H-002 del 14/11: apertura di Londra, ampiezza e durata del range, direzione, anno, regimi senza costi.
  - [DA COMPILARE: quali usa questa ipotesi]. Ogni taglio usato **conta in N** (§7).
- **Risultati di H-002 visti da chi scrive:** [DA COMPILARE]. Se l'ipotesi nasce da come è andata H-002, è dipendente da H-002: va detto.
- **Provenienza (approvata il 19/11, D-32; testo di DGS-10 §3 G).** Prima della scheda registrare, nel registro `laboratorio/ipotesi/PROVENIENZA-IDEE.md`:
  - ID di provenienza, autore originario, fonte e versione databile, data di pubblicazione;
  - regola e parametri allora disponibili, versioni precedenti, mercati e periodi usati dall'autore, con fonte oppure «ignoto»;
  - chi ha scelto l'idea, quali alternative o risultati hanno orientato la scelta, quali periodi sono già stati osservati da persone o chat.

  Separare gli elementi ereditati dalle aggiunte del titolare. Collegare esplorazioni pregresse, eventuale dipendenza da H-002, voci di N e censimento del mercato.
- **Revisore (DGS-10 §3 G).** Per il revisore dichiarare i contributi alla progettazione e le informazioni ricevute prima del fascicolo congelato. Chi ha scelto la variante non firma il giudizio indipendente su quella scheda. In caso di esposizione passiva a dettagli rilevanti, dichiarare quali giudizi restano indipendenti e affidare gli altri a un revisore idoneo.

## 1. Ipotesi
[DA COMPILARE: una frase che possa risultare falsa.] Esempio di forma: «Dopo X, il prezzo fa Y più spesso di quanto serva a pagare i costi.»
- **Perché dovrebbe funzionare (meccanismo):** [DA COMPILARE]. Senza un meccanismo plausibile, un risultato positivo è più probabilmente un caso.
- **Cosa la renderebbe falsa:** [DA COMPILARE].

## 2. Dati
- **Prezzi:** XAUUSD di Dukascopy, candele da 1 minuto BID e ASK; esecuzioni solo su minuti eseguibili (BID e ASK presenti, ASK ≥ BID), come H-002 v3.1 §2. [DA COMPILARE se diverso.]
- **Sviluppo:** dal 15/11/2023 al 12/11/2026. **Dati già visti** (contaminazione al §0).
- **Verifica:** una sola finestra della riserva 2005 → 31/10/2023, assegnata dal registro della riserva (`esecuzione/riserva.py`, una volta ratificato). **Una sola volta:** se fallisce, non si ripete sugli stessi dati.
- **Stato della finestra (approvato il 19/11, D-32; testo di DGS-10 §3 H; si collega ai §§0 e 9).** Per ogni coppia domanda–finestra registrare: mercato, date esatte comprese le date accessorie, esposizioni dirette o tramite fonte esterna o mercato correlato, motivazione, stato e prove. Gli stati sono tre:
  - **vista**: l'informazione del periodo ha influenzato questa domanda;
  - **esposizione incerta**: un'influenza pertinente resta plausibile e irrisolta;
  - **ammissibile in linea di principio**: censimento e provenienza sostengono questa classificazione.

  Si prenota solo nell'ultimo stato, dopo i controlli indipendenti di calendario, copertura congiunta BID/ASK e quota.
  - Si usano censimenti e conteggi consentiti, senza consultare prezzi della riserva.
  - Si applicano le date di D-29 e si indica esplicitamente l'intervallo eventualmente non assegnato fra riserva e sviluppo.
  - Una finestra compromessa per provenienza e un'apertura contabilizzata sono due eventi distinti da registrare.
  - Le finestre dei mercati correlati seguono le disposizioni adottate sul calendario comune.
- **ASK storico:** [DA COMPILARE dopo lo scaricamento]. Senza ASK la verifica non misura gli stessi costi dello sviluppo, e va deciso **prima** come trattarla.

## 3. Definizioni
[DA COMPILARE: orari (fuso Europe/London o altro), sessioni, range, livelli, ogni termine usato nelle regole. Niente termini vaghi: «forte», «chiaro», «vicino» vanno tradotti in numeri.]

## 4. Regole
[DA COMPILARE: ingresso, direzione, stop, target o uscita, dimensione, quanti trade al giorno.]

**OBBLIGATORIO, per tutte le regole:**
1. **Solo informazioni già disponibili** nel momento della decisione. Nessuna regola può dipendere da quotazioni successive, nemmeno dalla loro *assenza*. Lezione DGS-03: l'uscita di H-002 sceglieva un prezzo prima delle 16:30 perché dopo non c'erano quotazioni.
2. **Uscite solo in avanti:** se manca la quotazione all'ora d'uscita, si esce alla **prima quotazione successiva**, mai a una precedente. Se non arriva entro [DA COMPILARE] minuti, la regola lo dice prima.
3. **Dati mancanti:** non si inventano prezzi. Stop scavalcato in un buco: uscita all'apertura del primo minuto dopo il buco, al prezzo peggiore (come H-002 §4.3).
4. **Stop sul lato giusto:** acquisti escono sul BID, vendite sull'ASK.

## 5. Costi e dimensione
- Spread dai dati BID/ASK; commissione [DA COMPILARE]; slittamento [DA COMPILARE].
- **Scenario di stress:** [DA COMPILARE, almeno costi +50%].
- Rischio per trade: [DA COMPILARE]. Calcolo delle once con interi esatti (correzione D2 di H-002).
- **Esposizione alle code (OBBLIGATORIO, D-43, applicata il 20/11/2026).** Prima del sigillo la scheda dichiara, in modo verificabile:
  1. **la distanza di stop prevista:** statistica (per esempio la mediana) e periodo, calcolati con una procedura congelata prima del sigillo;
  2. **il salto di prezzo peggiore plausibile** all'esecuzione dello stop, con fonte e periodo: per esempio il salto massimo alla riapertura o sulle notizie nello sviluppo autorizzato. Se non è misurabile, una stima dichiarata come IPOTESI;
  3. **l'esposizione massima per trade in R** = 1 R + (salto peggiore plausibile ÷ distanza di stop): [DA COMPILARE].
  - Uno stop **non garantisce** il prezzo d'esecuzione in un salto (DGS-11 §2): non si dichiara un tetto alla perdita che lo stop non può assicurare.
  - **Confronto con il dominio collaudato:** il collaudo IA-02 contiene perdite rare di circa **−12,3 R con probabilità 1%** (celle 11 e 12 di `pilota_ia02.genera`, due soli valori). Se l'esposizione dichiarata o la frequenza delle perdite estreme escono da questo dominio, serve un **collaudo mirato** prima della verifica. Altrimenti si registra «applicazione motivata nel perimetro provato» (DGS-10 §6).
  - Il riscontro a DGS-11 §2 mostra perché conta: con stop molto stretti un salto di prezzo vale molti R.
  - **Precisazioni di DGS-12 §2 (21/11/2026):**
    - il salto peggiore plausibile descrive uno **scenario di stress**, non una perdita massima garantita: una garanzia richiede un vincolo dimostrabile;
    - distinguere il salto misurato **dall'ingresso** e il salto **oltre lo stop**;
    - per una posizione **senza stop**: esposizione = perdita monetaria di scenario ÷ budget monetario di rischio fissato all'ingresso, esplicitando lato eseguibile, costi, salto e slittamento;
    - senza un'esposizione stimabile, o senza prove su frequenza, gravità e dipendenza delle code, il trasferimento del collaudo resta **indimostrato**.

## 6. Metriche
Come H-002 v3.1 §6: trade, vincite, R medio netto, Sharpe per trade, drawdown in R, serie di perdite, acquisti e vendite separati, anni solari, benchmark «compro sempre» e «vendo sempre», confronto casuale con 1.000 ripetizioni e seme fisso, resoconto dei giorni scartati. [DA COMPILARE se si aggiunge altro.]

## 7. Prove e N (OBBLIGATORIO)
- **Varianti dichiarate:** [DA COMPILARE, al massimo 2 o 3]. Si registrano tutte **al sigillo**.
- **N** = tutte le prove selezionabili del registro (H-002 compresa) **più** i tagli esplorativi usati dall'ipotesi (§0).
- **Robustezza:** [DA COMPILARE: un parametro alla volta]. Resta fuori da N **solo** come veto fisso. Se orienta una scelta, entra in N (emendamento dell'utente).
- **Nessun taglio nuovo dopo il sigillo:** niente anni, direzioni o fasce scelti guardando i risultati.

## 8. Criteri scritti prima (OBBLIGATORIO; riallineato il 21/11/2026 a D-31, D-35, D-36, D-37, D-42 e DGS-12)
Il verdetto lo calcola il modulo `laboratorio/verdetto/verdetto_d31.py`. La scheda fissa solo quello che il modulo lascia alla scheda. La versione precedente di questa sezione (15/11: +0,15 R, DSR, anni positivi, «stima» o «limite», due o tre esiti) è superata dalle decisioni citate.

**Screening sullo sviluppo (D-36), per variante, tutte le condizioni insieme:**
1. R medio netto **> +0,25 R**;
2. limite inferiore dello stesso bootstrap **> 0**;
3. potenza stimata della verifica **≥ 50%** (la lettura dell'uguaglianza esatta al 50% è da confermare dal titolare: DGS-12 §2). La potenza si calcola:
   - alla **media vera obiettivo +0,25 R** (D-42), **mai** alla media osservata sullo sviluppo, che è gonfiata dalla selezione (DGS-12 §2);
   - alla quota della candidata (prima apertura con una variante: 2,5% per coda);
   - con una procedura congelata qui prima del sigillo, che tenga conto di concentrazione dei trade, dipendenza fra sedute e incertezza sulla dispersione: [DA COMPILARE];
   - dichiarando se riguarda il solo segnale del metro o la verifica intera con i veti, e misurandole entrambe sugli stessi percorsi.
4. **Controllo di fattibilità (DGS-12 §2, ricalcolato da Claude):** con un trade indipendente per seduta e 1.000 sedute, il 50% di potenza a +0,25 R richiede una deviazione standard per trade **σ ≤ 0,807 R** (errore standard ≤ 0,0255 R). Con σ = 1,25 R la potenza è circa il 24%. Dichiarare σ stimata e trade per seduta: [DA COMPILARE].
5. L'ammissione allo screening non è un verdetto: decide solo se spendere la riserva.

**Verifica sulla riserva (D-31, D-35, D-37):**
- **Metro:** bootstrap circolare a blocchi da 10 sedute, B = 3.999, intervallo basic, quota 2,5% per coda. Vale solo alla prima apertura con una variante; un'altra quota richiede un collaudo preregistrato (D-31, DGS-12 §1).
- **Esiti:** promossa se L > +0,20 R e requisiti vincolanti superati; bocciata se U < +0,10 R o per veto accertato; altrimenti non decidibile. Uguaglianza: non attraversa la soglia.
- **Minimi:** D = 1.000 sedute scelte per calendario prima dell'apertura, almeno 300 trade, almeno 200 sedute con trade.
- **Veto per blocchi da 250 sedute:** soglia [DA COMPILARE; proposta −0,25 R]; minimo di trade con esito noto per blocco [DA COMPILARE]. Un blocco con un esito ignoto non dà veto; un blocco completo sì, anche se manca un esito altrove (DGS-12 §3).
- **Requisiti con ruolo dichiarato (DGS-12 §3):** per ciascuno «veto», «vincolante per promuovere» o «descrittivo» (riportato, non cambia l'esito): [DA COMPILARE]. Gli anni civili sono descrittivi (D-37).
- **Non decidibile:** si riprova solo con dati nuovi (la demo futura), come prova nuova contata in N; la verifica avviata consuma comunque date e quota (D-35).

Se nessuna variante passa, **H-003 è chiusa** e non si ritocca. Un'idea simile è un'ipotesi nuova, con N che cresce.

## 9. Limiti noti
[DA COMPILARE: cosa questa prova non può dire.]

## 10. Casi d'oro (OBBLIGATORIO)
Almeno [DA COMPILARE, minimo 10] giornate inventate con il risultato calcolato a mano, una per ogni regola e per ogni bordo:
- ingresso;
- stop;
- target;
- stop in salto;
- dati mancanti;
- ora legale;
- arrotondamenti delle once;
- uscita senza quotazioni (solo in avanti).

Ognuna diventa un test che il simulatore e la replica indipendente devono riprodurre (modello: proposta v3.2 §B).

## 11. Sigillo e regola d'uscita (OBBLIGATORIO, proposta v3.2 §C)
Il sigillo si fa solo quando **tutte** queste condizioni sono vere, ognuna con una prova scritta:
1. ogni `[DA COMPILARE]` e `[DA SCEGLIERE]` è deciso dall'utente;
2. la replica indipendente (Gemini) è uguale al simulatore e al programma dei criteri su dati inventati, casi d'oro compresi;
3. test verdi e mutanti al 100% su Python 3.13 e 3.9;
4. due revisioni di fila senza rilievi critici o importanti; contano i rilievi di tipo E (errori in buona fede) e M a costo basso (D-24, 17/11/2026); prima della verifica sulla riserva serve in più un giro su TUTTE le manomissioni, senza rilievi critici o importanti, e la decisione sulla protezione del ramo su GitHub;
5. al sigillo si registrano le impronte SHA-256 della scheda e del codice che la esegue. Dopo il sigillo nulla cambia: un errore trovato dopo vuol dire un'ipotesi nuova.

**Tracciabilità dei giri (approvata il 19/11, D-32; testo di DGS-10 §3 F).** Per ogni giro che si intende contare registrare commit, ambiente, versione e opzioni di Python, perimetro, evidenze e rilievi per gravità e classe D-24.
- Tra commit diversi, documentare le modifiche, quali evidenze restano applicabili al candidato finale e le riesecuzioni delle prove interessate.
- Un giro si conta quando ne è documentata l'idoneità secondo la regola vigente.
- Prima della verifica si aggiungono il giro su tutte le manomissioni e la decisione sulla protezione del ramo.
- Registrare separatamente il contatore corrente e l'autorizzazione all'apertura.

**Prima del sigillo nessuno esegue la strategia sui dati veri**, né lo sviluppo né la riserva: è la lezione dell'incidente del 14/11 (#41). Le prove si fanno solo su dati inventati.

## 12. Controlli prima del sigillo (OBBLIGATORIO)
- [ ] §0 compilato, con il periodo esatto guardato e chi ha guardato
- [ ] meccanismo e falsificazione scritti (§1)
- [ ] nessuna regola guarda il futuro, nemmeno l'assenza di quotazioni (§4)
- [ ] potenza stimata a +0,25 R con procedura congelata e controllo di fattibilità su σ (§8)
- [ ] ruoli dei requisiti e parametri del veto per blocchi fissati (§8)
- [ ] N calcolato, con i tagli esplorativi usati
- [ ] casi d'oro scritti e calcolati a mano (§10)
- [ ] condizioni del §11 tutte vere, con le prove nel registro delle revisioni
