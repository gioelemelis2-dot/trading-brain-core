# H-002 · Revisioni della bozza (commit 417094c) e verifica di Claude

## R1 · DeepSeek, 14/11/2026 (revisore esterno)
**Nota di attribuzione:** per un errore di invio, DeepSeek ha ricevuto il prompt destinato a Gemini e si è firmato «Gemini». La revisione è di **DeepSeek**, non di Gemini, quindi non va salvata in `da-gemini/`.
- DeepSeek ha dichiarato correttamente di non avere accesso al repository e non ha inventato commit.
- Ha lavorato sul testo della bozza incollato dall'utente.
- Testo originale: nella conversazione dell'utente con DeepSeek.

**Giudizio complessivo di Claude:** revisione seria e utile. Molte ambiguità vere, sei proposte sbagliate o da ridimensionare (sotto, con il motivo).

| Rilievo di DeepSeek | Esito | Verifica e motivo di Claude |
|---|---|---|
| A1: quali minuti compongono il range di apertura | **accolto** | Va scritto come intervallo [08:00, 08:30): 30 minuti, dal minuto delle 08:00 a quello delle 08:29 |
| A2: nei giorni di cambio dell'ora la sessione dura 7,5 o 9,5 ore | **respinto** | Le sessioni sono definite nell'ora locale della borsa e il cambio d'ora avviene di notte: la sessione dura sempre 8,5 ore (Londra) e 6,5 ore (New York). Lo sfasamento USA–Europa cambia solo la relazione fra le due in UTC, ed è già gestito dai fusi |
| A3: minuti mancanti nel range | **accolto** | In Dukascopy un minuto mancante è un minuto senza scambi. Il range usa i minuti presenti; giorno valido solo con almeno l'80% dei minuti |
| A4: 20 giorni di calendario o di trading | **accolto** | Si usano le 20 sessioni valide precedenti della stessa sessione |
| A6, A8: prezzi per acquisti e vendite, e scatto degli stop | **accolto** | Convenzione da scrivere:<br>• acquisto: entra all'ASK, esce al BID, stop quando il BID tocca RA basso;<br>• vendita: entra al BID, esce all'ASK, stop quando l'ASK (BID + spread) tocca RA alto |
| A7: salto di prezzo all'apertura della candela d'ingresso | **accolto** | Se il prezzo d'ingresso è già oltre lo stop, o il rischio è minore del 25% dell'ampiezza del range, il trade non si fa |
| A9: prezzo dell'uscita a fine sessione | **accolto** | Uscita all'apertura del primo minuto dopo la fine della sessione, dal lato giusto (BID o ASK), con slittamento |
| A10: lo spread contato due volte nella dimensione | **accolto come chiarimento** | Distanza = prezzo d'ingresso eseguito meno prezzo d'uscita allo stop, dai lati giusti (lo spread è già dentro); poi si aggiungono commissione e slittamento, una volta sola |
| A11: slittamento sulle uscite | **accolto** | Target come ordine limite: nessuno slittamento. Uscita a fine sessione e stop: slittamento |
| Costi: spread 0,35 troppo ottimistico «all'apertura» | **accolto in parte** | Gli ingressi NON avvengono all'apertura della sessione: il primo possibile è alle 08:45 di Londra e alle 10:15 di New York, a 45 minuti dall'apertura. Senza spread misurati, però, la scelta prudente è giusta: **riferimento 0,50** finché non avremo gli spread di FP Markets per ora del giorno |
| Slittamento 0,10 troppo basso sugli stop | **accolto** | 0,20 USD sugli stop e sulle uscite a mercato; 0,10 sugli ingressi a mercato |
| Esempio numerico con stop di 2,50 USD | **respinto come esempio** | Lo stop di H-002 è il lato opposto del range di apertura. Con candele mediane da circa 2 USD a 1 minuto (Studio 1), un range di 30 minuti è largo molti dollari, quindi i costi pesano molto meno in R. Il principio (contare tutti i costi) resta valido |
| N = 32: contare nel DSR anche le 24 prove di robustezza | **respinto in parte** | Il DSR corregge la scelta della migliore fra N alternative. Le prove di robustezza non possono essere scelte, possono solo bocciare: non aumentano i falsi positivi, li riducono. Contarle anche in N punirebbe due volte.<br>Si registrano tutte nel registro, con ruolo «robustezza», ma restano fuori da N (da confermare in DA-19 e DA-28).<br>Per riferimento, con 600 trade la soglia di Sharpe per trade sale da 0,043 (N = 4) a 0,086 (N = 32) |
| Contare il filtro notizie come prove | **accolto** | Diventerà una variante selezionabile: si pre-registrano 4 prove in più (N = 8 quando ci sarà) |
| Scenari di spread e slittamento come prove | **respinto** | Il riferimento è unico e fissato prima; gli altri scenari si riportano soltanto. Nessuna scelta, quindi nessuna prova in più |
| «Crolla» non definito | **accolto** | Una variante è bocciata se in una qualsiasi prova di robustezza l'aspettativa diventa ≤ 0 o perde più del 50% rispetto alla base |
| Robustezza decisa dopo aver visto il risultato (sguardo al futuro di secondo livello) | **accolto** | Le 6 prove di robustezza per variante si eseguono sempre, comunque vada la base; la soglia è quella sopra |
| Benchmark direzionale contro la tendenza 2023–2026 | **accolto** | La strategia deve battere «sempre acquisto» e «sempre vendita» negli stessi orari di ingresso e con le stesse uscite. Acquisti e vendite si riportano separati, e il confronto entra fra i criteri |
| Criterio di drawdown | **accolto** | Il drawdown massimo in sviluppo deve stare sotto 12R (60% del limite totale FTMO di 20R a rischio 0,5%) |
| Mediana R > −0,1R e asimmetria < 3 | **respinto** | Sbagliato per questa strategia: con target a 1,5R e meno del 50% di vincite, la mediana è per costruzione −1R anche se la strategia guadagna. Un'asimmetria positiva è normale per chi taglia le perdite e lascia correre |
| Dichiarare che i giorni con meno dell'80% dei minuti sono esclusi anche dal vivo | **accolto in parte** | Dal vivo un minuto mancante è un minuto senza scambi, lo stesso fenomeno; va scritto che la regola si applica allo stesso modo |
| Contare in anticipo i trade possibili per verificare il minimo di 300 | **respinto** | Contarli vuol dire far girare i segnali sui dati di sviluppo prima del sigillo. Stima senza dati: circa 750 giorni in 3 anni, quasi sempre con rottura, quindi ben sopra 300 per sessione |
| Saltare i giorni del cambio d'ora | **respinto** | Non serve (vedi A2) |

## R2 · Gemini (Antigravity), 14/11/2026: `da-gemini/G-20261114-02-revisione-H-002.md`, ramo `rev/gemini-h002`, commit `f12b8b9`
Verificato su GitHub: il ramo esiste e tocca solo quel file. Revisione di alta qualità: legge anche il codice (engine, portfolio, dsr) e trova problemi che né Claude né DeepSeek avevano visto.

| Rilievo di Gemini | Esito | Verifica e motivo di Claude |
|---|---|---|
| Londra e New York si sovrappongono (Londra apre fino alle 16:30 di Londra), quindi il conflitto con P-06 (una posizione) e con `Portfolio.on_fill()` | **accolto** | Vero. Le 4 varianti si testano come portafogli separati. Se in demo girassero insieme: un segnale di New York con una posizione di Londra aperta viene saltato (regola scritta prima) |
| Il motore controlla stop e target alla risoluzione dei dati (15 minuti); a 1 minuto i buchi senza scambi spostano le aperture | **accolto** | Vero. Per H-002 serve un simulatore minuto per minuto con convenzioni esplicite, scritto in TDD, non `engine.py` com'è |
| Gli stop delle vendite non scattano sull'ASK in `engine.py`; slittamento applicato anche al target limite | **accolto** | Verificato nel codice: per la vendita lo stop scatta su `bar.high >= stop` (BID) e lo slittamento viene applicato a ogni uscita. Nel simulatore di H-002: lo stop di una vendita scatta quando l'ASK tocca il livello, e il target limite non ha slittamento |
| Ultimo ingresso: l'ingresso reale è alle 15:30 di Londra e alle 15:00 di New York, non alle 15:15 e 14:45 | **accolto (chiarimento)** | La tabella indicava la candela del segnale: va scritto in modo esplicito |
| Le 22 chiusure anticipate dei festivi USA farebbero restare aperta la posizione oltre la chiusura (overnight) | **accolto, importante** | Vero. Quei giorni si escludono usando il calendario dei festivi, che è noto in anticipo, quindi non è uno sguardo al futuro |
| Confronto casuale impossibile: una direzione opposta alla rottura con lo stop su RA alto o RA basso | **accolto** | Vero: lo stop starebbe dalla parte sbagliata. Il confronto usa lo stesso orario e lo stesso rischio R, con stop e target simmetrici rispetto all'ingresso |
| Il filtro dei giorni pieni (`MINUTI_GIORNO_PIENO`) va controllato solo fino al segnale | **accolto (cautela)** | La scheda usa il controllo solo sui minuti del range di apertura, noti alla fine del range. Nessun filtro sulla giornata intera |
| Contaminazione dallo Studio 1 (E-001): le scelte [P] fatte dopo averne letto i risultati | **accolto** | Va dichiarato nella scheda. E-001 non ha trovato strutture direzionali, ma la trasparenza è dovuta |
| Chiusura della candela da 15 minuti forzata a t + 15 quando mancano gli ultimi minuti | **respinto** | Il segnale si legge comunque alla fine nominale della candela: nessuna informazione futura. Effetto trascurabile |
| Commissione FP Markets Raw: 3 USD per lato (6 andata e ritorno) secondo il sito; FTMO senza commissione sui metalli | **da verificare** | Plausibile. Si userà la commissione misurata sul conto demo; quella FTMO va controllata alla fonte prima di FTMO |
| Costi fissi in USD su 20 anni: nel 2005–2012 l'oro valeva 400–1.000 USD, quindi gli stessi dollari pesano molto di più | **accolto, importante** | Vero, e nemmeno la proporzione al prezzo è corretta (gli spread relativi si sono ristretti molto). Soluzione: scaricare anche le candele **ASK** di Dukascopy per avere lo spread storico vero minuto per minuto (era già un rilievo di G-20261113-01) |
| DSR ≥ 0,95 nello sviluppo è troppo severo (3 anni, circa 300–500 trade) | **accolto, importante** | Ricalcolato da Claude: con N = 4 e T = 500 la soglia è circa 0,047 di Sharpe per trade. Una strategia da +0,10R con target 1,5R ha Sharpe ≈ 0,08, quindi DSR ≈ 0,77, e verrebbe bocciata anche se è buona. Lo sviluppo diventa uno **screening** (soglie su aspettativa e Sharpe); DSR ≥ 0,95 solo sulla verifica sigillata (circa 2.500 trade) |
| La verifica con il 60% degli anni positivi tollera molti anni negativi recenti | **accolto** | Si aggiunge: risultato positivo anche negli ultimi 5 anni della verifica (2018–2023) |
| Manca un vincolo sulle vendite | **accolto in parte** | Il benchmark «sempre acquisto / sempre vendita» lo copre in gran parte. Proposta: aspettativa delle vendite non sotto −0,05R |
| Tetto di 2 × la mediana arbitrario; filtro di economicità A ≥ 6 × costi | **accolto in parte** | Si usa A ≥ 6 × costi come limite inferiore, una sola scelta prima del test, senza prove in più. Il tetto di 2 × la mediana resta come protezione rozza dai giorni di notizie finché non c'è P-08: la scelta spetta all'utente |
| Dimensione calcolata sul capitale iniziale fisso | **accolto** | Comunque le metriche sono in R |
| Tutte e 4 le varianti valutate con lo stesso N finale (prove precedenti + 4), non con N = 1, 2, 3, 4 in sequenza come farebbe `dsr.py` | **accolto, importante** | Vero: con `evaluate_portfolio` la prima variante verrebbe valutata con N = 1. Le 4 varianti si registrano insieme e si valutano con lo stesso N |
| Robustezza con `dry_run=True` e veto binario scritto prima, fuori da N | **accolto** | È la stessa posizione di Claude, contro la proposta di DeepSeek di N = 32 |
| Annotare 09:30 New York contro 08:20/08:30 e il fixing LBMA delle 15:00 di Londra; non aggiungere varianti ora | **accolto** | Annotato fra le idee future |

## Decisioni dell'utente (14/11/2026)
- **Sessione:** solo **Londra**, per ora.
- **Uscita:** **entrambe** le varianti, V-T (target 1,5R) e V-S (fine sessione). Quindi **N = 2** prove dichiarate.
- **Range di apertura molto grandi:** si escludono, con il tetto di 2 × la mediana, finché non c'è il calendario delle notizie (P-08).
- **Prezzi ASK:** da scaricare per avere lo spread storico vero (scaricatore esteso in TDD, opzione `--lato ASK`).
- **Rapporto di Gemini:** unito su main.

## Prossimo passo
Quando arriva R2: versione 2 della scheda con le correzioni accolte, e l'elenco delle scelte che restano all'utente (sessione, uscita, stop, numero di prove). Solo dopo, il sigillo.

## Correzioni di testo da applicare alla v2 PRIMA del sigillo (trovate da Claude scrivendo il simulatore)
1. **§5, dimensione.** La formula «500 / (rischio + commissione + slittamento d'ingresso e di stop)», con un rischio misurato fra prezzi eseguiti, conterebbe due volte lo slittamento d'ingresso. Testo corretto:
   - **once** = floor(500 / (perdita per oncia allo stop + commissione));
   - **perdita per oncia allo stop** = differenza fra il prezzo d'ingresso eseguito (spread e slittamento compresi) e il prezzo d'uscita eseguito allo stop (livello ± slittamento ± stress).
2. **§4.3, rischio per il filtro dei 0,25 × A e per il target.** Rischio = distanza fra il prezzo d'ingresso eseguito e il **livello** dello stop, senza lo slittamento dello stop.

## R3 · Rilettura di Gemini sulla v2: `da-gemini/G-20261114-03-rilettura-H-002-v2.md`, ramo `rev/gemini-h002-v2`, commit `807cda0`
**Verdetto di Gemini sulla v2: non ancora sigillabile.** Tutti i rilievi sono stati verificati da Claude; quelli sul simulatore sono coperti da test scritti PRIMA della correzione (commit `c1f0163`) e da mutanti nuovi (29/29).

| Rilievo | Esito | Applicazione |
|---|---|---|
| Doppio conteggio dello slittamento nella dimensione; manca la regola «once < 1, niente trade»; segni espliciti | **accolto** (Claude l'aveva trovato in parallelo) | v3 §5 |
| Stop in salto eseguito al livello invece che all'apertura del minuto (vantaggio irreale) | **accolto, grave** | v3 §4.3; simulatore e test |
| Uscita di fine sessione che con un buco di dati poteva scivolare molto in là | **accolto** | finestra [16:30, 16:45), altrimenti l'ultima chiusura prima delle 16:30 |
| Ingresso ritardato da buchi di dati | **accolto** | ingresso solo entro 15 minuti dalla fine della candela di segnale |
| «Oltre lo stop all'ingresso» dal lato giusto (BID per l'acquisto, ASK per la vendita) | **accolto** | v3 §4.3 (era già così nel simulatore) |
| BID senza ASK, ASK sotto il BID | **accolto, con una correzione di Claude** | Minuto non eseguibile, contato. NON si esclude il giorno: sarebbe uno sguardo al futuro (errore di Claude nella prima stesura del test, corretto) |
| Robustezza con range di 20 minuti e soglia dell'80% proporzionale | **accolto (chiarimento)** | v3 §3 |
| Pavimento fisso di 3 USD inadatto al 2005–2012 | **accolto** | minimo = 6 × costo di riferimento dagli spread veri delle 20 sessioni precedenti |
| Festivi: mancano i bank holiday inglesi | **accolto** | elenco completo con sostituti e date straordinarie (da verificare su gov.uk) |
| Chiusure anticipate USA | **respinto per Londra** | cadono dopo le 16:30 di Londra |
| Scenario di stress «solo riportato» in §5/§6 ma criterio in §8 | **accolto** | è un criterio; entra anche nella dimensione |
| N di H-002 contato due volte (sigillo e verifica) | **accolto** | in verifica N = totale del registro in quel momento |
| Drawdown, ultimi 5 anni, anni solari da precisare | **accolto** | trade chiusi; risultato cumulato del quinquennio; anni solari |
| Confronto casuale: testo sul target di V-S e sulla «distanza R» | **accolto** | v3 §6 |
| Nota sulle alternative USA e sul fixing LBMA | **accolto** | v3 §9 |

## R4 · Revisione esterna di DeepSeek sulla v3 (14/11/2026)
DeepSeek ha ricevuto per errore la bozza v1 al posto dei test, quindi non ha valutato `test_orb_londra.py`. Alcuni rilievi (spread di riferimento 0,35, spread all'apertura) vengono dalla bozza v1, non dalla v3. Correzioni in TDD (commit `8e2f61c` rosso, poi verde): 39 test e mutanti 33/33.

| Rilievo | Esito | Motivo e applicazione |
|---|---|---|
| B3: la scheda dichiarava che ogni regola era nel simulatore, ma il confronto casuale, il DSR, la robustezza, il veto e il cumulato dei 5 anni non c'erano | **accolto, alto** | Vero. La v3.1 dice cosa è codice e cosa no; il programma che esegue §6–§8 si scrive, si testa e si rivede prima del sigillo |
| Spread disponibile in meno di 20 sessioni; «manca lo spread» ambiguo | **accolto** | Servono almeno 15 spread fra le 20 sessioni precedenti; codice e test |
| Stress nel costo di riferimento | **accolto (chiarimento)** | Escluso, dichiarato: lo stress si misura sugli stessi giorni |
| Limite dei 15 minuti per l'ingresso | **accolto (chiarimento)** | Fine esclusa |
| Minuti mancanti che nascondono uno stop | **accolto in parte** | Un minuto senza scambi non muove il prezzo. Un buco del flusso è coperto dallo stop in salto all'apertura successiva. Limite residuo dichiarato |
| Sharpe con la deviazione di popolazione | **accolto** | Deviazione campionaria; nella prima stesura del test Claude ha sbagliato una somma (4,6 invece di 7,2), corretto |
| Somma per anno e cumulato degli ultimi 5 anni | **accolto** | `per_anno` con la somma; `somma_ultimi_anni` |
| Minuti con spread negativo solo nei giorni con segnale; giorni esclusi senza traccia | **accolto** | `resoconto()` per tutti i giorni |
| `specchio` senza direzione: KeyError | **accolto** | Errore esplicito |
| Benchmark su campioni diversi | **accolto** | Confronto sui giorni in cui entrano entrambi |
| Docstring «v2» | **accolto** | Aggiornato |
| Festivi straordinari 2024–2026 | **accolto** | Da confrontare con il file ufficiale gov.uk (dal Mac) prima del sigillo |
| Spread di riferimento 0,35 «ottimistico all'apertura» | **respinto** | Viene dalla bozza v1. La v3 usa lo spread vero minuto per minuto (dati ASK), e gli ingressi sono almeno 45 minuti dopo l'apertura |
| DSR anche nello screening | **respinto, con il motivo** | Con 3 anni di sviluppo una strategia da +0,10R a trade avrebbe DSR circa 0,77 (calcolo di Gemini G-20261114-02, ricontrollato da Claude): il DSR nello screening boccerebbe anche le strategie buone. Il DSR resta sulla verifica sigillata. È un disaccordo fra i due revisori, deciso con il calcolo |
| Il confronto casuale 50/50 sarebbe «positivo» in un mercato in tendenza | **respinto** | Con direzione casuale metà dei trade va contro la tendenza: la media è circa zero meno i costi. La tendenza la controllano i benchmark «compro sempre» e «vendo sempre», già fra i criteri |
| Casi della sezione C non coperti dai test | **accolto** | Aggiunti: ora legale, target della vendita sull'ASK, minuto delle 16:30, due rotture e un solo trade, once < 1, rischio al limite. Erano già corretti nel codice: mancava la copertura |

## R5 · DeepSeek, secondo giro (14/11/2026)
Non ha ricevuto di nuovo `test_orb_londra.py` (allegata ancora la bozza v1), quindi la sezione C manca ancora. Ha ricontrollato le correzioni: giudicate in gran parte giuste.

| Rilievo | Esito | Motivo e applicazione |
|---|---|---|
| Il simulatore citava ancora `H-002-ORB-v2.md` | **accolto** | Corretto |
| «20 sessioni che ce l'hanno» ambiguo; il codice è più severo | **accolto (chiarimento)** | La scheda ora dice: ultime 20 sessioni di base, di cui almeno 15 con lo spread, senza andare più indietro (come fa il codice) |
| Priorità dei motivi di esclusione in `resoconto` | **accolto (chiarimento)** | Priorità scritta nella scheda |
| `minuti_scartati` parziale | **accolto (chiarimento)** | Dichiarato a cosa serve |
| Prezzo all'ingresso già oltre il target | **respinto** | Impossibile: il target si calcola dal prezzo d'ingresso eseguito (ingresso ± 1,5 × rischio), quindi è sempre dalla parte giusta |
| Festivi 2024–2026 | **già risolto** | DeepSeek aveva la versione precedente: dal commit `9af64db` i festivi coincidono con il file ufficiale gov.uk per il 2019–2028 |
| Sigillo bloccato finché non c'è il programma dei criteri | **d'accordo** | È il piano |
| Casi della sua lista senza test | **accolto** | Aggiunti 3 test: stress che non cambia i giorni ammessi, fine sessione al primo minuto disponibile, minuto senza ASK non contato come spread negativo |

## Stato di test e mutanti (aggiornato a ogni modifica)
- **14/11/2026, commit `a79a342`:** 43 test verdi su Python 3.13 e 3.9; mutation testing 33/33 su entrambe le versioni.

## R6 · ChatGPT, prima revisione (parziale, 14/11/2026)
Eseguiti i 43 test nel suo ambiente: verdi, codice di uscita 0. Non ha potuto completare il mutation testing: un errore di permessi su `/tmp/mutanti_h002`, poi il limite di tempo di esecuzione. L'esecuzione di Python sarà di nuovo disponibile più avanti. Giudizio sul sigillo sospeso, correttamente: ha scritto che senza prove non attribuisce esiti positivi.

| Rilievo | Esito | Applicazione |
|---|---|---|
| La scheda dichiarava 39 test, ma i test sono 43 | **accolto** | I numeri non stanno più nella scheda (invecchiano), ma qui |


## Programma dei criteri e sigillo (notte del 14–15/11/2026, ramo `feat/esecutore-h002`, NON unito a main)
- **Codice nuovo** in `laboratorio/esecuzione/`:
  - `sigillo.py`: registro delle prove `registro-prove/1`, impronta SHA-256, niente doppio sigillo, verifica una volta sola;
  - `criteri.py`: generico, riusabile per le ipotesi future;
  - `caricatore.py`: modalità «sviluppo» e «verifica»;
  - `esegui_h002.py`: esecutore e riga di comando;
  - `sintetico.py`: mercati inventati, solo per le prove.
- **Il sigillo NON è stato eseguito:** il registro vero `laboratorio/registro_prove.json` non esiste. La scheda v3.1 non è stata toccata: `git diff main -- H-002-ORB-v3.md` è vuoto.
- **Prove su mercati inventati** (seme 3, 800 giorni di calendario, circa 433 trade per variante):

  | mercato | V-T | V-S | esito |
  |---|---|---|---|
  | casuale | R medio −0,028 | R medio −0,029 | entrambe bocciate |
  | vantaggio noto nella rottura (+0,01 USD al minuto) | R medio 0,250 | R medio 0,336 | entrambe promosse, tutti i 9 criteri |
  | sola tendenza al rialzo | vendite −0,255 | vendite −0,437 | entrambe bocciate, anche dai benchmark |

  Taratura del generatore: su 10 mercati casuali (semi 1–10) l'R medio è −0,046 (V-T) e −0,053 (V-S), cioè i costi.

### Ambiguità della scheda v3.1 trovate scrivendo il programma (NON corrette: proposte per l'utente)
| # | Punto | Cosa fa oggi il programma | Proposta |
|---|---|---|---|
| A1 | Criterio 6 senza vendite | Boccia: un valore mancante non passa | Tenere: senza vendite non si può mostrare l'indipendenza dalla tendenza |
| A2 | Confronto casuale: quale percentile, quali giorni | Percentile a rango più vicino (ceil 0,95·n), «sopra» = strettamente maggiore. Giorni = quelli in cui esistono sia l'acquisto sia la vendita speculari (≥ 95% dei giorni della strategia nelle prove). L'R della strategia è quello di tutti i suoi trade | Scrivere nella v3.2 che strategia e confronto casuale si misurano sugli **stessi** giorni, come per i benchmark |
| A3 | «60% degli anni solari positivi»: anni senza trade | Contati solo gli anni con trade (la funzione accetta anche l'elenco completo degli anni) | Contare tutti gli anni del periodo, con gli anni senza trade come non positivi (più severo) |
| A4 | Veto con la base ≤ 0 | Veto. Non cambia nulla: il criterio 1 boccia già | Scriverlo |
| A5 | DSR: asimmetria, curtosi e V | Momenti degli R per trade; V = max(1/(T−1), varianza empirica degli Sharpe delle altre varianti promosse sullo stesso periodo), come in `backtester/dsr.py` | Scrivere V nella scheda. Le non promosse non girano in verifica, quindi non entrano in V |
| A6 | Sigillo prima anche dello sviluppo (§10) | La riga di comando rifiuta **qualunque** esecuzione senza sigillo; il caricatore in sviluppo non lo controlla (come chiesto dal mandato) | Tenere la versione più severa |
| A7 | Due registri | Esiste ancora `laboratorio/trial_registry.json` del vecchio backtester (0 prove). N conta solo il registro nuovo | Congelare il vecchio (è vuoto) e dichiarare unico il nuovo (DA-19) |
| A8 | Fine esatta della verifica | Il caricatore rifiuta solo le date dal 15/11/2023; DA-26 dice «circa il 31/10/2023» con embargo | Fissare la data esatta in DA-26 **prima** del sigillo; il caricatore rifiuterà l'embargo |
| A9 | Riscaldamento | Le prime 20 sessioni di ogni periodo servono solo da storico (nessun trade possibile) | Scriverlo |
| A10 | Verifica registrata prima del calcolo | Sì: se il programma cade a metà, la verifica conta comunque come eseguita | Tenere |
| A11 | Ultimi 5 anni con il 2023 parziale | Il 2023 (gennaio–ottobre) conta come anno solare | Scriverlo, o usare gli ultimi 60 mesi |

### Stato di test e mutanti del programma
- 49 test nuovi (`test_esecuzione`: 31; `test_esegui_h002`: 18), verdi su Python 3.13 e 3.9.
- Mutation testing: `tests/mutazioni_esecuzione.py`, 56 mutanti.
  - Primo giro: 55/56 su entrambe le versioni. Sopravvissuto E12: senza `--varianti` la verifica si fermava solo dopo aver letto i dati sigillati.
  - Aggiunto il test (`fdf4afe`). **Secondo giro, intero: 56/56 su Python 3.13.18 e 56/56 su 3.9.25.**
- Regressioni: suite di `dati/tests` e `laboratorio/tests` (11 moduli, 183 test) e Guardian (77 test) verdi.

## R7 · Revisioni del programma dei criteri (in attesa)
- Gemini (Antigravity): replica indipendente e revisione del ramo.
- DeepSeek: revisione del codice e delle ambiguità.
- ChatGPT: doppia revisione con il pacchetto eseguibile.
