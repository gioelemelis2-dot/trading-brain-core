# H-002 v2 · Rottura del range di apertura di Londra su XAUUSD

**Stato:** versione 2, **da sigillare** dopo l'ultima rilettura.
- Sostituisce la bozza `H-002-ORB-BOZZA.md` (commit `417094c`).
- Le correzioni vengono dalle revisioni di DeepSeek (R1) e Gemini (R2), verificate da Claude in `H-002-REVISIONI.md`.
- Decisioni dell'utente del 14/11/2026: solo Londra, due varianti di uscita, esclusi i range molto grandi.
- **Contaminazione dichiarata (DA-17):**
  - lo Studio 1 (E-001) e lo Studio 2 (E-002) sono stati letti prima di questa versione. Non hanno trovato strutture direzionali né sulle sessioni né sui micro-range;
  - l'utente ha visto i grafici del periodo di sviluppo;
  - nessun test di questa strategia è stato fatto.

## 1. Ipotesi
Dopo i primi 30 minuti di Londra, la prima chiusura a 15 minuti fuori dal range di apertura indica la direzione del resto della sessione più spesso di quanto serva a pagare i costi.

## 2. Dati
- **Prezzi:** XAUUSD di Dukascopy, candele da 1 minuto **BID e ASK**. Lo spread è quello vero, minuto per minuto (ASK − BID). Le candele da 15 minuti si costruiscono dai minuti BID, allineate in UTC.
- **Sviluppo:** dal 15/11/2023 al 12/11/2026 (DA-26).
- **Verifica sigillata:** dal 2005 a circa il 31/10/2023, con date esatte in DA-26, una sola volta. Con gli ASK storici, quando saranno scaricati.
- **Minuto mancante:** in Dukascopy è un minuto senza scambi; non si inventano prezzi.

## 3. Definizioni (ora di Londra, Europe/London: l'ora legale la gestisce il fuso)
- **Sessione:** dalle 08:00 alle 16:30.
- **Range di apertura (RA):** i minuti dalle 08:00 incluse alle 08:30 escluse, cioè 30 minuti. RA alto e RA basso sono massimo e minimo **BID** di quei minuti; A = RA alto − RA basso.
- **Giorno valido:**
  - dal lunedì al venerdì;
  - almeno 24 dei 30 minuti del range presenti (80%);
  - non è un giorno di chiusura anticipata o festivo noto in anticipo (24 e 31 dicembre, 25 e 26 dicembre, 1° gennaio, Venerdì Santo, lunedì di Pasqua);
  - l'ampiezza è nella fascia ammessa (sotto).
- **Fascia dell'ampiezza:**
  - limite alto: A ≤ 2 × la mediana di A nelle **20 sessioni valide precedenti** (protezione dai giorni di notizie finché manca P-08; decisione dell'utente);
  - limite basso: A ≥ 6 × il costo per trade di riferimento (§5), cioè almeno 6 × 0,50 = 3,00 USD (rilievo di Gemini M-04, scelta unica prima del test).
  - Se le sessioni precedenti sono meno di 20 (inizio dei dati), il giorno non è valido.
- **Candela di segnale:** le candele BID da 15 minuti che **aprono** fra le 08:30 e le 15:15 incluse e sono **complete**, cioè con i 15 minuti trascorsi; la chiusura è il BID dell'ultimo minuto scambiato.

## 4. Regole
1. **Segnale:** la prima candela di segnale che chiude **sopra RA alto** (acquisto) o **sotto RA basso** (vendita). Una sola, la prima.
2. **Ingresso a mercato** all'apertura della candela successiva, cioè il primo minuto scambiato dopo la fine della candela di segnale:
   - acquisto all'**ASK** di apertura di quel minuto + slittamento;
   - vendita al **BID** di apertura − slittamento.

   L'ultimo ingresso possibile è quindi alle 15:30.
3. **Stop:**
   - acquisto: chiusura quando il **BID** tocca RA basso;
   - vendita: chiusura quando l'**ASK** tocca RA alto.
   - Esecuzione al livello ± slittamento sugli stop.
   - **Se all'ingresso il prezzo è già oltre lo stop,** o il rischio (distanza ingresso–stop) è minore di 0,25 × A, il trade non si fa.
4. **Uscita, due varianti:**
   - **V-T:** target a ingresso ± 1,5 × rischio, con ordine limite, senza slittamento; scatta quando il BID (acquisto) o l'ASK (vendita) tocca il livello. Se non scatta, uscita a fine sessione;
   - **V-S:** nessun target, uscita a fine sessione.
   - **Fine sessione:** apertura del primo minuto scambiato dalle 16:30 in poi, al BID (acquisto) o all'ASK (vendita), ± slittamento. Mai posizioni oltre.
5. **Ordine degli eventi:** si scorre minuto per minuto dal minuto d'ingresso.
   - Nel minuto d'ingresso conta solo lo stop.
   - Se in un minuto si toccano stop e target, conta lo stop.
6. **Un solo trade al giorno.**
7. **Notizie:** il primo test è **senza** il filtro P-08, ed è dichiarato. Il filtro, quando ci sarà un calendario affidabile, sarà una variante in più e conterà come prova.

## 5. Costi e dimensione
- **Spread:** quello vero dai dati ASK e BID, già dentro i prezzi d'ingresso e d'uscita.
- **Commissione:** 0,07 USD per oncia andata e ritorno (7 USD per lotto; FP Markets dichiara 6, quindi stima prudente).
- **Slittamento:** 0,10 USD sugli ingressi; 0,20 USD sugli stop e sulle uscite a mercato; 0 sul target limite.
- **Costo di riferimento per il filtro dell'ampiezza:** 0,50 USD a trade, stima prudente di spread più commissione più slittamenti.
- **Scenario di stress (solo riportato):** spread + 0,20 USD su ingresso e uscita.
- **Dimensione:** capitale **fisso** di 100.000 USD (niente interesse composto), rischio 0,5% (P-01) = 500 USD.
  - Once = 500 / (rischio in USD per oncia + commissione + slittamento d'ingresso e di stop), arrotondato per difetto a 1 oncia (0,01 lotti).
  - **Il rischio in USD per oncia contiene già lo spread:** è misurato fra prezzi eseguiti, dai lati giusti.
- **Metrica principale in R** = risultato netto del trade / 500 USD.

## 6. Metriche
- Trade, percentuale di vincite, R medio netto, Sharpe per trade, drawdown massimo in R, serie peggiore di perdite.
- **Separati:** acquisti e vendite, e ogni anno del periodo.
- **Benchmark direzionali:** «compro sempre» e «vendo sempre», con gli stessi giorni, gli stessi orari d'ingresso e le stesse uscite (stop e target a distanza R uguale, dalla parte giusta).
- **Confronto casuale:** stessi giorni e orari d'ingresso, direzione estratta a caso, stop e target a distanza R uguale dalla parte giusta; 1.000 ripetizioni con seme fisso.
- **Scenario di stress sullo spread:** solo riportato.

## 7. Prove (DA-19, DA-28)
- **Prove dichiarate: V-T e V-S, quindi N = 2.** Si registrano insieme, prima del calcolo, e si valutano entrambe con lo stesso N (rilievo di Gemini).
- **Robustezza:** registrata con ruolo «robustezza», fuori da N, eseguita **sempre**, qualunque sia il risultato base. Un parametro alla volta:
  - range di apertura di 20 e di 45 minuti;
  - target 1,2 e 2,0 (solo V-T);
  - limite alto del filtro 1,6 e 2,5 × la mediana.
- **Veto di robustezza:** una variante è bocciata se in una qualunque prova di robustezza l'R medio diventa ≤ 0 o scende di oltre il 50% rispetto alla base.

## 8. Criteri scritti prima
**Screening sullo sviluppo (per variante, tutti insieme):**
1. R medio netto ≥ +0,05R;
2. Sharpe per trade ≥ 0,06;
3. almeno 300 trade;
4. sopra il 95° percentile del confronto casuale;
5. R medio netto **maggiore** di quello di «compro sempre» e di «vendo sempre»;
6. R medio delle vendite ≥ −0,05R (il risultato non deve dipendere solo dalla tendenza al rialzo);
7. drawdown massimo < 12R;
8. nessun veto di robustezza;
9. R medio netto > 0 anche nello scenario di stress.

Se una variante non passa, è bocciata. Se nessuna passa, **H-002 è chiusa** e non si ritocca.

**Verifica sigillata (una volta, per le varianti promosse, con N = 2 più le prove già registrate):**
1. DSR ≥ 0,95;
2. R medio netto > 0;
3. almeno il 60% degli anni positivi;
4. risultato positivo anche negli ultimi 5 anni della verifica;
5. drawdown massimo < 15R.

## 9. Limiti noti
- **Un solo tipo di mercato nello sviluppo** (2023–2026): soprattutto salita, poi la discesa del 2026.
- **Spread Dukascopy ≠ spread del broker:** il confronto con lo storico MT5 è ancora da fare (criterio di discordanza da decidere).
- **Senza filtro notizie:** i dati UK e USA cadono dentro la sessione di Londra.
- **Il tetto di 2 × la mediana** è una stima: per questo è nella robustezza.
- **Pochi trade per la demo:** al massimo uno al giorno.

## 10. Sigillo
- Quando l'utente approva: questa scheda viene pubblicata su GitHub e la sua impronta SHA-256 viene registrata nel registro delle prove, con N = 2, **prima** di qualunque esecuzione.
- **Nessuna modifica dopo il sigillo.** Ogni cambiamento è un'ipotesi nuova.
