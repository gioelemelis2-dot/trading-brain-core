# H-002 v3.1 · Rottura del range di apertura di Londra su XAUUSD

**Stato:** versione 3, **da sigillare** dopo la revisione esterna.
- Sostituisce la v2 (commit `9780d71`).
- Applica:
  - i rilievi della rilettura di Gemini G-20261114-03 (verdetto sulla v2: non ancora sigillabile), verificati da Claude;
  - le 2 correzioni trovate da Claude scrivendo il simulatore.
- **v3.1:** chiarimenti dalla revisione esterna di DeepSeek (esiti in `H-002-REVISIONI.md`, R4).
- **Cosa è già codice e cosa no** (la v3 diceva «ogni regola», ed era falso: rilievo di DeepSeek):
  - §2–§5, i benchmark direzionali e le metriche del §6 sono eseguiti da `laboratorio/simulatori/orb_londra.py`, con test e mutation testing. I numeri aggiornati non sono scritti qui, perché cambiano a ogni revisione e la scheda sigillata non deve contenere dati che invecchiano: sono in `H-002-REVISIONI.md`. Rilievo di ChatGPT: qui era rimasto «39 test» mentre erano già 43;
  - il confronto casuale (§6), la robustezza e il veto (§7) e i criteri del §8, DSR compreso, saranno eseguiti da un programma a parte. **Va scritto, testato e rivisto PRIMA del sigillo.**

**Contaminazione dichiarata (DA-17):**
- gli Studi E-001 (sessioni) ed E-002 (micro-range) sono stati letti prima: nessuna struttura direzionale trovata;
- l'utente ha visto i grafici del periodo di sviluppo;
- nessun test di questa strategia è stato fatto.

## 1. Ipotesi
Dopo i primi 30 minuti di Londra, la prima chiusura a 15 minuti fuori dal range di apertura indica la direzione del resto della sessione più spesso di quanto serva a pagare i costi.

## 2. Dati
- **Prezzi:** XAUUSD di Dukascopy, candele da 1 minuto **BID e ASK**.
- **Segnali e range:** sui minuti BID.
- **Esecuzioni:** solo sui minuti **eseguibili**, cioè quelli con BID e ASK e con ASK ≥ BID sia in apertura sia in chiusura.
  - Un minuto con ASK sotto il BID è un dato errato: non si usa (come se mancasse) e si conta.
  - Il giorno NON si esclude: sarebbe uno sguardo al futuro.
- **Minuto mancante** = minuto senza scambi; non si inventano prezzi.
  - Senza scambi il prezzo non si muove, quindi non può toccare lo stop.
  - Se invece mancano dati per un'interruzione del flusso e il prezzo è andato oltre lo stop, lo stop scatta all'apertura del primo minuto dopo il buco, al prezzo peggiore (§4.3).
  - Limite residuo dichiarato: un prezzo andato oltre lo stop e tornato indietro DENTRO un buco di dati non si vede.
- **Sviluppo:** dal 15/11/2023 al 12/11/2026.
- **Verifica sigillata:** dal 2005 a circa il 31/10/2023, con date esatte in DA-26; una sola volta, con gli ASK storici.

## 3. Definizioni (ora di Londra, Europe/London: l'ora legale la gestisce il fuso)
- **Sessione:** dalle 08:00 alle 16:30.
- **Range di apertura (RA):** minuti BID nell'intervallo [08:00, 08:30).
  - RA alto = massimo dei massimi; RA basso = minimo dei minimi; A = RA alto − RA basso.
  - Nella robustezza con 20 o 45 minuti l'intervallo cambia di conseguenza, e il minimo di minuti presenti resta l'80% (16 su 20, 36 su 45).
- **Sessione di base:** dal lunedì al venerdì, non esclusa (sotto), con almeno l'80% dei minuti del range presenti. Solo le sessioni di base entrano nelle mediane.
- **Giorni esclusi, noti in anticipo:**
  - i bank holiday di Inghilterra e Galles: Capodanno, Venerdì Santo, lunedì di Pasqua, primo e ultimo lunedì di maggio, ultimo lunedì di agosto, Natale, Santo Stefano;
  - i giorni sostitutivi quando un festivo cade nel fine settimana;
  - gli spostamenti e le aggiunte straordinarie: 2011-04-29; 2012-06-04 al posto del 2012-05-28; 2012-06-05; 2020-05-08 al posto del 2020-05-04; 2022-06-02 al posto del 2022-05-30; 2022-06-03; 2022-09-19; 2023-05-08.
    - **Verificato:** per il 2019–2028 l'elenco del codice coincide esattamente con il file ufficiale di gov.uk (`dati/riferimenti/uk_bank_holidays.json`, commit `ac17502`); un test lo controlla.
    - Per il 2005–2018 il file ufficiale non c'è: le date straordinarie del 2011 e del 2012 vengono dalla conoscenza di Claude (limite dichiarato);
  - in più: 24, 25, 26 e 31 dicembre, 1° gennaio.
  - Le chiusure anticipate USA (13:00–13:30 di New York) cadono dopo la fine della sessione di Londra e non la toccano.
- **Mediane** sulle **20 sessioni di base precedenti**; meno di 20 → giorno non valido. La sessione corrente non entra mai.
- **Tetto dell'ampiezza:** A ≤ 2 × la mediana di A.
- **Costo di riferimento:**
  - mediana dello spread (ASK − BID in apertura) del primo minuto eseguibile dalle 08:30 in poi, calcolata sulle **ultime 20 sessioni di base**: fra queste **almeno 15 devono avere lo spread**, altrimenti il giorno non è valido. Non si va più indietro per cercarne altre;
  - lo stress NON entra nel costo di riferimento, così lo scenario di stress si misura sugli stessi giorni;
  - più commissione (0,07), slittamento d'ingresso (0,10) e slittamento d'uscita (0,20).
  - Così il minimo segue i costi veri di ogni epoca, dal 2005 a oggi.
- **Minimo dell'ampiezza:** A ≥ 6 × il costo di riferimento.
- **Candele di segnale:** candele BID da 15 minuti allineate in UTC, che **aprono** dalla prima quarta d'ora non anteriore alla fine del range fino alle 15:15 incluse. Con il range di 20 minuti la prima candela è quella delle 08:30.
  - Chiusura = BID di chiusura dell'ultimo minuto presente nella candela; una candela senza minuti non esiste.

## 4. Regole
1. **Segnale:** la prima candela di segnale che chiude **sopra RA alto** (acquisto) o **sotto RA basso** (vendita). Una sola, la prima.
2. **Ingresso:** all'apertura del primo minuto eseguibile dopo la fine della candela di segnale, **nei 15 minuti successivi** (fine esclusa: un minuto esattamente 15 minuti dopo non vale); altrimenti niente trade.
   - acquisto: ASK di apertura + 0,10 (+ stress);
   - vendita: BID di apertura − 0,10 (− stress).
   - L'ultimo ingresso possibile è quindi entro le 15:45.
3. **Stop:**
   - livello: acquisto RA basso; vendita RA alto.
   - **Niente trade se il prezzo all'ingresso è già oltre lo stop:** acquisto se BID di apertura ≤ RA basso; vendita se ASK di apertura ≥ RA alto.
   - **Rischio** = distanza fra il prezzo d'ingresso eseguito e il **livello** dello stop. Niente trade se il rischio < 0,25 × A.
   - **Scatto:**
     - acquisto: quando il BID minimo del minuto ≤ livello; uscita = min(livello, BID di apertura del minuto) − 0,20 (− stress);
     - vendita: quando l'ASK massimo ≥ livello; uscita = max(livello, ASK di apertura) + 0,20 (+ stress).
     - Se il prezzo salta oltre lo stop, si esce al prezzo di apertura, peggiore.
4. **Uscita, due varianti:**
   - **V-T:** target = ingresso ± 1,5 × rischio, con ordine limite.
     - Acquisto: si chiude quando il BID massimo ≥ target; vendita: quando l'ASK minimo ≤ target.
     - Il prezzo d'uscita è il livello esatto del target: nessun miglioramento e nessuno slittamento.
     - Se non scatta, uscita a fine sessione.
   - **V-S:** nessun target, uscita a fine sessione.
   - **Fine sessione:** all'apertura del primo minuto eseguibile nell'intervallo [16:30, 16:45): acquisto al BID − 0,20, vendita all'ASK + 0,20 (± stress). In quel minuto l'uscita all'apertura viene prima di stop e target.
     - Se non c'è nessun minuto eseguibile in quell'intervallo: alla chiusura dell'ultimo minuto eseguibile prima delle 16:30, con lo stesso slittamento.
     - Mai posizioni oltre.
5. **Ordine degli eventi:**
   - si scorre minuto per minuto dal minuto d'ingresso;
   - nel minuto d'ingresso conta solo lo stop;
   - se in un minuto si toccano stop e target, conta lo stop.
6. **Un solo trade al giorno.**
7. **Notizie:** nessun filtro P-08 in questo test, ed è dichiarato. Il filtro sarà una variante futura, contata come prova.

## 5. Costi e dimensione
- **Spread:** quello vero, già dentro i prezzi d'ingresso e d'uscita.
- **Commissione:** 0,07 USD per oncia andata e ritorno (FP Markets dichiara 6 USD per lotto: stima prudente).
- **Slittamento:** 0,10 sugli ingressi; 0,20 sugli stop e sulle uscite a fine sessione; 0 sul target limite.
- **Scenario di stress:** 0,20 USD in più contro, sia sull'ingresso sia sull'uscita (stop e fine sessione). Entra anche nella dimensione della posizione. **È un criterio eliminatorio (§8).**
- **Dimensione:** capitale fisso di 100.000 USD, rischio dello 0,5% = 500 USD.
  - **once** = floor(500 / (perdita per oncia allo stop + commissione));
  - **perdita per oncia allo stop** = differenza fra il prezzo d'ingresso eseguito e il prezzo d'uscita eseguito allo **livello** dello stop, con slittamento e stress, senza salto;
  - se le once sono meno di 1, niente trade.
- **R del trade** = (once × (differenza fra uscita e ingresso a favore − commissione)) / 500.

## 6. Metriche
- Trade, percentuale di vincite, R medio netto, Sharpe per trade.
- **Drawdown massimo** sulla curva cumulata dei trade chiusi, in R.
- Serie peggiore di perdite consecutive.
- **Separati:** acquisti e vendite, e ogni **anno solare**.
- **Benchmark direzionali:** «compro sempre» e «vendo sempre», negli stessi giorni e con gli stessi minuti d'ingresso della strategia. Il confronto si fa sui giorni in cui entrano sia la strategia sia il benchmark.
  - Nei giorni in cui la direzione è opposta al segnale, lo stop è alla **stessa distanza** dall'ingresso, dalla parte giusta.
  - V-T: target a 1,5 × quella distanza; V-S: uscita a fine sessione.
- **Confronto casuale:** stessi giorni e minuti d'ingresso, direzione estratta a caso, stop alla stessa distanza dalla parte giusta, stesse uscite della variante. 1.000 ripetizioni con seme fisso.
- **Dati scartati e giorni** (funzione `resoconto`):
  - numero di minuti con spread negativo nelle sessioni di base, dalle 08:00 alle 16:45;
  - numero di giorni per motivo di esclusione, un motivo per giorno, con questa priorità: fine settimana o festivo; minuti del range insufficienti; poi il motivo del §3.
  - Il campo `minuti_scartati` del singolo giorno conta solo i minuti dopo il segnale e serve solo a ispezionare quel giorno.
- **Sharpe** con la deviazione standard campionaria (n − 1). **Per anno:** numero di trade, media e somma.

## 7. Prove (DA-19, DA-28)
- **Prove dichiarate: V-T e V-S.** Si registrano **al sigillo**, insieme, nel registro delle prove: N di H-002 = 2. Tutte e due si valutano con lo stesso N.
- **Robustezza:** registrata con ruolo «robustezza», fuori da N, eseguita **sempre**. Un parametro alla volta:
  - range di 20 e di 45 minuti;
  - target 1,2 e 2,0 (solo V-T);
  - tetto 1,6 e 2,5 × la mediana.
- **Veto:** una variante è bocciata se in una qualunque prova di robustezza l'R medio è ≤ 0 o scende di oltre il 50% rispetto alla base.

## 8. Criteri scritti prima
**Screening sullo sviluppo (per variante, tutti insieme):**
1. R medio netto ≥ +0,05R;
2. Sharpe per trade ≥ 0,06;
3. almeno 300 trade;
4. R medio sopra il 95° percentile del confronto casuale;
5. R medio maggiore di quello di «compro sempre» e di «vendo sempre»;
6. R medio delle vendite ≥ −0,05R;
7. drawdown massimo < 12R;
8. nessun veto di robustezza;
9. R medio netto > 0 nello scenario di stress.

Se nessuna variante passa, **H-002 è chiusa** e non si ritocca.

**Verifica sigillata (una volta, solo per le varianti promosse):**
1. DSR ≥ 0,95, con N = **numero totale di prove nel registro in quel momento**. Le 2 di H-002 sono già dentro dal sigillo: non si aggiungono di nuovo;
2. R medio netto > 0;
3. almeno il 60% degli **anni solari** positivi;
4. **risultato cumulato** degli ultimi 5 anni solari della verifica > 0;
5. drawdown massimo < 15R.

## 9. Limiti noti
- **Un solo tipo di mercato nello sviluppo** (2023–2026).
- **Spread Dukascopy ≠ spread del broker:** il confronto con lo storico MT5 è ancora da fare.
- **Senza filtro notizie.**
- **Il tetto di 2 × la mediana** è una stima: per questo è nella robustezza.
- **Al massimo un trade al giorno.**
- **Varianti escluse in questo giro, annotate per il futuro:**
  - aperture legate agli USA: 08:20 e 08:30 di New York, cioè l'apertura dei future sull'oro e i dati macro;
  - il fixing LBMA delle 15:00 di Londra.

## 10. Sigillo
- Dopo la revisione esterna e l'approvazione dell'utente: commit della scheda, impronta SHA-256 registrata nel registro delle prove con N = 2, **prima** di qualunque esecuzione.
- **Nessuna modifica dopo il sigillo.**
