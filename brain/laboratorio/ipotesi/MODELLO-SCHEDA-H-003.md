# Modello di scheda per H-003 (e ipotesi successive)

**Stato del modello:** bozza di Claude, 16/11/2026, **da approvare dall'utente**. Non contiene nessuna idea: la parte «Ipotesi» la scrive l'utente.
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

## 1. Ipotesi
[DA COMPILARE: una frase che possa risultare falsa.] Esempio di forma: «Dopo X, il prezzo fa Y più spesso di quanto serva a pagare i costi.»
- **Perché dovrebbe funzionare (meccanismo):** [DA COMPILARE]. Senza un meccanismo plausibile, un risultato positivo è più probabilmente un caso.
- **Cosa la renderebbe falsa:** [DA COMPILARE].

## 2. Dati
- **Prezzi:** XAUUSD di Dukascopy, candele da 1 minuto BID e ASK; esecuzioni solo su minuti eseguibili (BID e ASK presenti, ASK ≥ BID), come H-002 v3.1 §2. [DA COMPILARE se diverso.]
- **Sviluppo:** dal 15/11/2023 al 12/11/2026. **Dati già visti** (contaminazione al §0).
- **Verifica:** una sola finestra della riserva 2005 → 31/10/2023, assegnata dal registro della riserva (`esecuzione/riserva.py`, una volta ratificato). **Una sola volta:** se fallisce, non si ripete sugli stessi dati.
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

## 6. Metriche
Come H-002 v3.1 §6: trade, vincite, R medio netto, Sharpe per trade, drawdown in R, serie di perdite, acquisti e vendite separati, anni solari, benchmark «compro sempre» e «vendo sempre», confronto casuale con 1.000 ripetizioni e seme fisso, resoconto dei giorni scartati. [DA COMPILARE se si aggiunge altro.]

## 7. Prove e N (OBBLIGATORIO)
- **Varianti dichiarate:** [DA COMPILARE, al massimo 2 o 3]. Si registrano tutte **al sigillo**.
- **N** = tutte le prove selezionabili del registro (H-002 compresa) **più** i tagli esplorativi usati dall'ipotesi (§0).
- **Robustezza:** [DA COMPILARE: un parametro alla volta]. Resta fuori da N **solo** come veto fisso. Se orienta una scelta, entra in N (emendamento dell'utente).
- **Nessun taglio nuovo dopo il sigillo:** niente anni, direzioni o fasce scelti guardando i risultati.

## 8. Criteri scritti prima (OBBLIGATORIO)
**Screening sullo sviluppo (per variante, tutti insieme):**
1. **R medio netto ≥ +0,15 R (IA-02)**, regola: [DA SCEGLIERE: «sulla stima» (proposta di Claude) / «sul limite inferiore al 95%»];
2. Sharpe per trade ≥ [DA COMPILARE; coerente con 0,15 R: circa 0,15 / deviazione standard per trade];
3. almeno [DA COMPILARE] trade (vedi `potenza_IA-02.md`);
4. R medio sopra il 95° percentile del confronto casuale;
5. R medio maggiore di «compro sempre» e di «vendo sempre»;
6. [DA COMPILARE: vincolo sul lato debole, es. vendite ≥ −0,05 R];
7. drawdown massimo < [DA COMPILARE] R;
8. nessun veto di robustezza;
9. R medio netto > 0 nello scenario di stress.

**Verifica sulla riserva (una volta, solo varianti promosse):**
1. DSR ≥ 0,95 con N = registro intero in quel momento;
2. **R medio netto ≥ +0,15 R (IA-02)**, regola: [DA SCEGLIERE: «sul limite inferiore al 95%» (proposta di Claude) / «sulla stima»];
3. almeno il 60% degli anni solari positivi;
4. risultato cumulato degli ultimi 5 anni solari della finestra > 0;
5. drawdown massimo < [DA COMPILARE] R.

**Esiti:** [DA SCEGLIERE prima dei dati: due esiti (promossa / bocciata), oppure tre esiti con «non decidibile»]. Se tre esiti:
- «non decidibile» va **definito qui** in numeri, ad esempio «l'intervallo contiene la soglia»;
- **si risolve solo con dati nuovi** (successivi all'ultima data già vista), mai rieseguendo sugli stessi dati;
- non dà accesso alla riserva. La lezione è la patch di `tb-proposte`, archiviata e non applicata.

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
4. due revisioni di fila senza rilievi critici o importanti;
5. al sigillo si registrano le impronte SHA-256 della scheda e del codice che la esegue. Dopo il sigillo nulla cambia: un errore trovato dopo vuol dire un'ipotesi nuova.

**Prima del sigillo nessuno esegue la strategia sui dati veri**, né lo sviluppo né la riserva: è la lezione dell'incidente del 14/11 (#41). Le prove si fanno solo su dati inventati.

## 12. Controlli prima del sigillo (OBBLIGATORIO)
- [ ] §0 compilato, con il periodo esatto guardato e chi ha guardato
- [ ] meccanismo e falsificazione scritti (§1)
- [ ] nessuna regola guarda il futuro, nemmeno l'assenza di quotazioni (§4)
- [ ] scelte «stima» / «limite» e due / tre esiti fatte e motivate (§8)
- [ ] numero minimo di trade coerente con `potenza_IA-02.md`
- [ ] N calcolato, con i tagli esplorativi usati
- [ ] casi d'oro scritti e calcolati a mano (§10)
- [ ] condizioni del §11 tutte vere, con le prove nel registro delle revisioni
