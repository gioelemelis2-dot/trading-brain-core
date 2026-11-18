# Messaggio 8 al DGS: revisione del modello di scheda H-003 (18/11/2026)

MESSAGGIO 8 AL DGS — solo metodo; nessuna decisione riservata al titolare.

CONTESTO
- Banco di prova: R16 primo giro pulito (contatore 1 su 2, D-26); R17 in corso sul candidato e476a9a.
- Decisioni recenti del titolare:
  - D-31: verifica col metro collaudato, cioè bootstrap con Δ = 0,05 R; promozione se il limite inferiore grezzo
    supera +0,20 R;
  - D-29: partizione: sviluppo dal 15/11/2023, riserva 2005 → circa 31/10/2023.
- Da DGS-09: istituiti il registro della provenienza delle idee e il censimento di GBPJPY.
- Costi del broker: specifiche di XAUUSD lette (commissione 6 USD per lotto, da confermare). Lo spread per ora
  verrà dai tick dello sviluppo.
- Il titolare sta studiando idee esterne (un corso video) in un progetto ChatGPT separato. La prima scheda H-003
  verrà da lì o da idee sue.

RICHIESTA
In allegato, sotto, due documenti:
(A) il modello di scheda H-003 IN VIGORE;
(B) la BOZZA di aggiornamento NON APPLICATA (sezioni A–F del 17/11 e G–J del 18/11).
Per ogni sezione della bozza (A–J) indicate:
1. se è corretta e coerente con D-24, D-29, D-31, DGS-07, DGS-08, DGS-09;
2. se è [DOC], un aggiornamento che non cambia il metodo, o [METODO], che richiede una decisione: confermate o
   correggete la classificazione;
3. che cosa manca o è ambiguo e lascerebbe gradi di libertà dopo aver visto i dati. Formulate le correzioni come
   testo pronto da sostituire;
4. per la sezione E (esiti a tre stati, dipende da DA-31): le opzioni per il titolare, senza sceglierne una.
In più:
5. l'ordine consigliato per approvare le parti, considerando che la prima scheda può arrivare presto;
6. eventuali requisiti che la prima scheda dovrà soddisfare per poter usare D-31 sul suo disegno reale
   (corrispondenza al dominio collaudato), senza aprire la riserva.

FORMATO: DGS-10, sezioni numerate come sopra. L'approvazione spetta al titolare.

---

## (A) MODELLO IN VIGORE: MODELLO-SCHEDA-H-003.md

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
4. due revisioni di fila senza rilievi critici o importanti; contano i rilievi di tipo E (errori in buona fede) e M a costo basso (D-24, 17/11/2026); prima della verifica sulla riserva serve in più un giro su TUTTE le manomissioni, senza rilievi critici o importanti, e la decisione sulla protezione del ramo su GitHub;
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


---

## (B) BOZZA NON APPLICATA: MODELLO-SCHEDA-H-003-BOZZA-P3.md

# Bozza di aggiornamento del modello di scheda H-003 (integrazioni P3 del DGS e DA-31)

**Stato: BOZZA, NON APPLICATA.** Preparata da Claude il 17/11/2026 pomeriggio su richiesta del titolare (decisione 5 della risposta 7). Il modello in vigore resta `MODELLO-SCHEDA-H-003.md`. Si applica solo con il via del titolare, e la parte sugli esiti solo dopo la ratifica di DA-31.

Per ogni punto: **[DOC]** è un aggiornamento documentale, cioè rende esplicito ciò che H-002 già fa; **[METODO]** è un cambio di metodo, che serve una decisione.

---

## A. Nuovo §5-bis «Unità e misura del risultato» [DOC]

> **R di un'operazione.** R_i = P/L netto dell'operazione i ÷ B_i, dove B_i è il budget di rischio in USD fissato **prima** dell'ingresso (in H-002: 500 USD, §5). Il denominatore non cambia dopo il risultato.
> - **Operazione** = un ingresso con tutte le sue uscite, parziali comprese, fino alla chiusura completa. Reingressi e aumenti di posizione: [DA COMPILARE] (vietati, oppure regola scritta).
> - **Numeratore:** comprende spread (già nei prezzi del lato eseguibile, da non sottrarre due volte), commissione [fonte], slittamento [modello dichiarato], eventuali costi di finanziamento. Uno stop con salto può costare più di 1 R.
> - **Estimando:** media di R per operazione della regola congelata, sulle opportunità del calendario. I giorni senza operazioni non sono trade a zero R; si contano a parte (frequenza, esposizione).
> - **Unità statistica:** la seduta. Per ogni seduta d si registrano S_d (somma degli R delle operazioni attribuite alla seduta d'ingresso) e K_d (numero di operazioni). Media per trade = ΣS_d / ΣK_d.

## B. §4 «Regole», nuova voce obbligatoria «Ambiguità sulla barra al minuto» [DOC]

> Il primo istante in cui ogni informazione è disponibile: [DA COMPILARE per ingresso, stop, target, uscita a orario].
> - Se nella stessa barra al minuto sono compatibili più percorsi (per esempio stop e target toccati), vale la regola **conservativa**, cioè lo stop prima del target, come in H-002 (`H-002-ORB-v3.md` riga 85; `orb_londra.py` righe 231–239, dove nel minuto d'ingresso conta solo lo stop). I casi si **contano** e si riportano.
> - Stessa regola scritta per ingressi e uscite vicini a un buco nei dati.
> - Ogni regola di ambiguità ha almeno un caso d'oro (§10).

## C. §6 «Metriche» e §7 «Prove e N»: confronti e gradi di libertà [DOC]

> - **Primario:** media di R netto per trade (A). Benchmark («compro sempre», «vendo sempre», confronto casuale) **sulle stesse date eleggibili**, con la stessa esecuzione e lo stesso rischio.
> - **Elenco chiuso** di ogni via di promozione: varianti, tagli ereditati (§0), veti, N e m (promozioni possibili nella stessa apertura). Una diagnostica usata per scegliere diventa una prova selezionabile e entra in N.

## D. §8 «Criteri»: coerenza del campione [METODO]

> - **Metodo dell'intervallo** per IA-02 in verifica: [DA SCEGLIERE dopo il pilota del collaudo: HAC con regola dei ritardi fissata, oppure bootstrap a blocchi delle coppie giornaliere (S_d, K_d)]. Quota unilaterale = quota della variante (P2).
> - **Minimo tecnico** (per calcolare le statistiche) e **minimo informativo** (trade necessari per la potenza dichiarata, con la dipendenza stimata nello sviluppo), entrambi scritti prima. Il minimo informativo si calcola dalla frequenza osservata nello sviluppo e dall'effetto minimo plausibile **motivato prima**.
> - **Anni:** definire gli anni parziali e gli «ultimi cinque anni». Una finestra senza cinque anni valutabili non può soddisfare il criterio 4 della verifica: va dichiarato prima se il criterio cade o se la finestra va allungata.

## E. §8 «Esiti» a tre stati (sostituisce il blocco «Esiti») [METODO, dipende da DA-31]

> | Esito | Regola scritta prima |
> |---|---|
> | **Promossa** | dati idonei; minimi raggiunti; **limite inferiore > +0,15 R**; tutti i requisiti vincolanti passati |
> | **Bocciata** | su una prova valida, **limite superiore < +0,15 R** (metodo: [DA SCEGLIERE]), oppure un veto terminale accertato su misure valide |
> | **Non decidibile** | dati insufficienti, statistica non stimabile, o intervallo che contiene +0,15 R, senza veto terminale |
>
> - Solo «promossa» fa avanzare.
> - «Non decidibile» **consuma le date e la quota della riserva** (non le restituisce).
> - **Riesame:** solo con dati **nuovi**, successivi all'ultima data vista, con la regola **congelata**, una prenotazione nuova e una prova in più in N.
> - Se cambia la regola o il disegno per recuperare l'esito, è un'**ipotesi nuova**.
> - **Conflitto da risolvere** (rilevato dal DGS): l'attuale frase «se nessuna variante passa, H-003 è chiusa» vale per «bocciata». Per «non decidibile» l'ipotesi resta **sospesa** fino al riesame preregistrato, oppure chiusa per scelta del titolare.

## F. §11 «Sigillo», tracciabilità dei giri di revisione [DOC, già in vigore per R15]

> Ogni giro di revisione che conta per la regola d'uscita dichiara: commit esatto, ambiente (sistema, versione e opzioni di Python), perimetro verificato e prove eseguite. Se tra due giri cambia il codice del perimetro, le prove toccate si rifanno sul candidato finale prima di contare entrambi i giri (D-24, parere P6 del DGS).

---

**Cosa NON cambia:** IA-02 (+0,15 R), il §0 sulla contaminazione, il divieto di eseguire prima del sigillo, la verifica una volta sola.

---

## Aggiornamento del 18/11/2026: decisioni D-31, DGS-07, DGS-08 e DGS-09

Anche queste voci sono **BOZZA, NON APPLICATA**: si applicano con il via del titolare, come il resto.

## G. Nuovo §0 «Provenienza dell'idea» [METODO, DGS-09 §1]
> - **Riga di provenienza** in `laboratorio/ipotesi/PROVENIENZA-IDEE.md`, compilata **prima** di questa scheda: fonte e versione, regola disponibile a quella data, informazioni dell'autore, selezione da parte nostra, destinazione.
> - **Che cosa viene dalla fonte e che cosa aggiungiamo noi**: due elenchi separati.
> - **Chi ha contribuito al disegno**: persone e chat, compresa la chat delle strategie. Serve a scegliere un revisore indipendente (DGS-09 §3).

## H. §9 «Verifica»: stato della finestra candidata [METODO, DGS-09 §1b e §2b]
> Per ogni finestra candidata della riserva: **vista per questa domanda / esposizione incerta / ammissibile in linea di principio**, con la motivazione e il rimando al censimento del mercato (per esempio `governance/censimento/CENSIMENTO-GBPJPY.md`). Si prenota solo una finestra ammissibile.

## I. §8 «Criteri»: regola di verifica di D-31 e dominio collaudato [METODO, DGS-08 §4c, DGS-09 §2c]
> - **Verifica:** bootstrap circolare a blocchi (ℓ = 10, B = 3.999, intervallo basic) con Δ = 0,05 R. Promozione se il limite inferiore grezzo supera **+0,20 R**, bocciatura se il limite superiore è sotto **+0,10 R** (D-31).
> - **Corrispondenza al dominio collaudato**, da motivare con le sole informazioni ammesse dello sviluppo:
>   - numero di sedute vicino a 1.000;
>   - quota del 2,5% per coda;
>   - operazioni per seduta, dipendenza, dispersione e perdite rare comparabili con le 12 celle del pilota.
>   Se una condizione materiale cambia (per esempio la quota scende all'1,25% per una seconda variante o una seconda apertura), serve una giustificazione specifica o un collaudo preregistrato su repliche nuove **prima** dell'uso.
> - **Pareggi alle soglie** (#116): limiti a meno di 1e-9 dalla soglia vanno contati e dichiarati nel rendiconto, con la regola di pareggio fissata prima.
> - **Screening sullo sviluppo:** regola da decidere (orientamento del titolare: sulla stima).

## J. §5 «Costi» [DOC, Gate 1]
> Commissione e spread **fissati prima dei dati** da `dati/costi/` (specifiche del broker rilevate e spread per ora UTC misurato con `dati/pipeline/costi_tick.py` sullo sviluppo). Il costo in R dipende dalla distanza dello stop: va riportato per la distanza tipica della regola.
