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
## R8 · Gemini, replica indipendente alla cieca del simulatore (`da-gemini/G-20261115-01-replica-H-002.md`, ramo `rev/gemini-replica-h002`)
- **Metodo:** replica scritta dalla sola scheda e committata prima di leggere il codice di Claude (`619a6a4`), poi confronto trade per trade (`106bcc3`). 3 semi, 10 configurazioni, 8.010 giorni-configurazione.
- **Risultato:** coincidenza ≤ 1e-9 su 25 configurazioni su 30.
- **Ramo controllato da Claude:** tocca solo `da-gemini/`.
- **Rilievi riprodotti da Claude con prove proprie prima di correggere** (sonde indipendenti dal codice di Gemini):

| Rilievo | Esito | Applicazione |
|---|---|---|
| D1: spread di riferimento cercato dalla fine del range invece che dalle 08:30; con il range di 20 minuti entrano gli ASK delle 08:20–08:29, con quello di 45 si saltano quelli delle 08:30–08:44. Tocca solo la robustezza (con 30 minuti la fine del range è proprio le 08:30) | **accolto, errore di Claude** | Corretto in TDD: lo spread si cerca dalle 08:30 qualunque sia il range. 2 test, mutante O34 |
| D1 bis: nessun limite superiore (uno spread alle 17:00 viene accettato) | **ambiguità (A12)** | La scheda dice «dalle 08:30 in poi», quindi il codice la rispetta alla lettera. Capita solo in una sessione senza alcun minuto eseguibile. **Proposta per la v3.2:** «fino alle 16:45», come le sessioni di base del `resoconto` |
| D2: once in virgola mobile; 500 / 10,00 diventa 49,99999999999968 e le once 49 invece di 50 (riprodotto: 1 caso ogni ~200 prezzi a 3 decimali, in acquisto e in vendita) | **accolto, errore di Claude** | Corretto in TDD: divisione intera esatta ai milionesimi di USD. Test con un acquisto e una vendita, mutante O35 |
| D3: i giorni con ingresso oltre i 15 minuti restano «validi» con motivo «ingresso oltre la candela successiva» nel `resoconto` | **ambiguità (A13), solo diagnostica** | Nessun effetto sui trade. **Proposta per la v3.2:** scrivere che è una categoria del `resoconto` (mancato ingresso, §4.2) |
| D4: `minuti_scartati` conta anche dopo le 16:45 | **ambiguità (A14), solo diagnostica** | **Proposta per la v3.2:** «fino alle 16:45» |
| Casi non coperti dai 43 test (robustezza, ora legale di ottobre, 24/30 minuti, ingresso ritardato entro i 15 minuti, vendita senza quotazioni alle 16:30, doppio tocco al minuto d'ingresso, e altri) | **accolto** | Sulla replica coincidono già. Da trasformare in test prima del sigillo |
| AMB-01, AMB-03…AMB-08 | **d'accordo** | Scelte identiche nelle due implementazioni indipendenti |

- **Correzioni:** ramo `fix/orb-replica-gemini` da main, commit rosso `b26be54`, poi verde. Test di H-002: 46 su Python 3.13 e 3.9. Mutanti: 35/35 su entrambe (O15 aggiornato, O34 e O35 nuovi).
- **Effetto sul ramo `feat/esecutore-h002`:** cambiano solo le prove di robustezza con range 20 e 45. Dopo il merge di questa correzione va riallineato e i suoi test vanno rieseguiti.
- **Da chiedere a Gemini:** rieseguire `confronto.py` sul ramo corretto e confermare 30 configurazioni su 30.

### Dopo R8 (15/11/2026, ramo `fix/orb-replica-gemini`)
- **Test strutturali** (`TestStrutturali`):
  - taglio dei dati contro lo sguardo al futuro;
  - simmetria acquisti/vendite a spread zero.
- **8 casi** segnalati da Gemini come non coperti (`TestCasiScopertiGemini`).
- **Mutanti nuovi** O36–O40, tutti uccisi. O36 (segnale dalla chiusura della giornata) lo prende solo il test del taglio; O37 lo prende il test di simmetria.
- **Stato:** 56 test di H-002; mutanti 40/40 su Python 3.13 e 3.9.
- **Registro dei difetti:** `laboratorio/REGISTRO-DIFETTI.md`.
- **Proposta v3.2:** `H-002-v3.2-PROPOSTA.md`. Contiene A1–A14 da decidere, 16 casi d'oro e la regola d'uscita per il sigillo.

## R9 · ChatGPT, revisione incrociata (15/11/2026): verdetto «non sigillabile»
**Cosa ha visto:** la scheda v3.1 e le revisioni R1–R5, cioè lo stato **prima** del mandato notturno. Non ha visto il programma dei criteri, R7–R8, le correzioni D1 e D2, i test strutturali e la proposta v3.2.

**Giudizio di Claude sui suoi punti:**

| ID | Suo stato | Giudizio di Claude | Applicazione |
|---|---|---|---|
| F-01 minuti senza dati o senza scambi | aperto, alta | **Accolto.** «Minuto mancante = senza scambi» era un'affermazione troppo forte senza un controllo | Proposta A15: definizione di buco, conteggio, scenario pessimistico eliminatorio |
| F-02 programma dei criteri §6–§8 | aperto, alta | **Già fatto dopo la sua revisione:** `laboratorio/esecuzione/` (49 test, mutanti 56/56) | Da rivedere: pacchetto R9-bis |
| F-03 ASK storici | aperto, alta | **D'accordo che servono prima della verifica, non prima del sigillo.** Il sigillo fissa le regole; la verifica non può partire senza gli ASK storici scaricati e controllati (stesso controllo dei buchi del BID) | Scritto nella regola d'uscita: la verifica parte solo con gli ASK storici controllati |
| F-04 lo 0,5% non è la perdita massima | da dichiarare | **Accolto** | Proposta A16 |
| F-05 spread di riferimento dalle 08:30 | da giustificare | **Accolto:** è un riferimento poco rappresentativo. Nota: Gemini (D1) chiedeva di rispettare le 08:30 scritte nella scheda, e il codice ora lo fa; la scelta dell'orario è dell'utente | Proposta A17 |
| F-06 N e robustezza | aperto | **Già applicato:** la robustezza si registra con ruolo «robustezza», fuori da N, solo veto, sempre eseguita (`esegui_h002.py`, mutanti E01, E07) | — |
| F-07 39 contro 43 test | correzione documentale | **Già corretto il 14/11** (R6, commit `3063b98`): i numeri non stanno più nella scheda. Ha rivisto un file precedente | — |
| F-08 33/33 non riprodotto | non verificato | **Giusto non attribuirlo.** Il pacchetto nuovo fa girare i mutanti a blocchi | Pacchetto R9-bis |
| F-09 tetto 2× euristico | accettabile | **D'accordo**, è dichiarato come euristica | — |
| F-10 qualità degli ASK | dati mancanti | **D'accordo** (come F-03) | — |
| Respingimento «stima di 750 trade» | motivazione debole | **Accolto in parte.** La stima era una stima. Il motivo giusto per non contare i trade prima non è lo «sguardo al futuro», ma il §10: nessuna esecuzione delle regole sui dati prima del sigillo. Il minimo di 300 è un criterio dello screening, verificato dopo | — |
| Respingimento «confronto casuale con aspettativa zero» | troppo in fretta | **Accolto:** con stop, target e percorsi il payoff non è lineare, e va simulato, non argomentato. Ora il programma lo simula (1.000 ripetizioni). Su un mercato inventato con sola tendenza il 95° percentile del casuale è 0,004 (V-T) e 0,020 (V-S): vicino a zero, ma è un dato su quel mercato, non una prova generale | — |
| Mediana e asimmetria | motivazione incompleta | **Accolto:** né veto né criterio, ma vanno riportate | Proposta A18 |

**Stato del ramo `feat/esecutore-h002` dopo l'unione con `fix/orb-replica-gemini` (`4e2835a`):** tutte le suite di dati e laboratorio verdi, Guardian 77/77; mutanti del simulatore 40/40 e del programma dei criteri 56/56, su Python 3.13 e 3.9. Pacchetto per ChatGPT: prompt in `collaborazione/da-claude/PROMPT-CHATGPT-R9-BIS.md`.

## R10 · Gemini, revisione R7 del programma dei criteri (`da-gemini/G-20261115-R7-esecutore-h002.md`, ramo `rev/gemini-esecutore-h002`)
- **Conferma sul simulatore** (`G-20261115-02`, ramo `rev/gemini-replica-h002`, `84dd2a3`): dopo la correzione di D1 e D2, **30 configurazioni su 30 identiche** (6.432 trade e 3.858 benchmark uguali).
- **Replica alla cieca del programma dei criteri:**
  - commit della replica `80aab37` prima di leggere `esecuzione/`; rapporto `c97a2e6`;
  - differenza 0 su tutte le metriche deterministiche dei tre mercati inventati;
  - 95° percentile del casuale entro 0,0062 (generatore casuale diverso);
  - test 49/49 e mutanti 56/56 su Python 3.9.6.
- **Verdetto di Gemini:** «pronto con correzioni obbligatorie prima del sigillo».
- **Ramo controllato da Claude:** tocca solo `da-gemini/`.

| Rilievo | Gravità (registro dei difetti) | Esito | Correzione (TDD: `6a29aa2` rosso, poi verde) |
|---|---|---|---|
| P1: la verifica accettava varianti bocciate o mai provate in sviluppo | critica | **accolto** | Verifica solo delle varianti con screening registrato e **mai bocciate**: uno screening ripetuto non cancella una bocciatura. Mutante E13 |
| P2: chiamate separate per V-T e V-S svuotavano V nel DSR | critica | **accolto** | Una sola verifica con **tutte e sole** le promosse. Mutante E14 |
| P3: il programma girava con un sigillo da N = 1 | critica | **accolto** | Le varianti del sigillo devono coincidere con quelle dell'esecutore. Mutante E15 |
| P4: anni senza trade ignorati; ultimi 5 anni contati dall'ultimo trade | critica | **accolto** (A3 e A11 in via prudenziale) | La riga di comando passa tutti gli anni del periodo; gli ultimi 5 anni partono dalla fine del periodo. Mutanti E16, K28 |
| P5: R della strategia su tutti i giorni, casuale solo su quelli comuni | critica | **accolto** (A2 in via prudenziale) | Stessi giorni; il rapporto riporta la copertura. Mutante E17 |
| P6: cache vuota o sbagliata bruciava la verifica | importante | **accolto** | Dati incompleti (giorni senza file o zero minuti): fermo prima di registrare, in sviluppo e in verifica. Mutante E18 |
| P7: embargo 1–14/11/2023 leggibile in verifica | importante | **accolto** (A8 in via prudenziale) | Fine **provvisoria** della verifica al 31/10/2023, finché DA-26 non fissa la data. Mutanti C03, C09 |
| P8: registro senza blocco | importante | **accolto, ed era più grave del previsto** | Il test con 4 fili e 60 scritture **perdeva esecuzioni**. Blocco esclusivo (`fcntl`) e file temporaneo per filo. Mutante S10 |
| P8 bis: simulatore sul ramo precedente alla correzione D1/D2 | — | già risolto | Unione `4e2835a` |
| MG01, MG03, MG04, MG06, MG07 sopravvissuti | test | **accolto** | Test di confine; i 5 mutanti sono nello script e muoiono |
| A1–A11 | — | **posizioni registrate** | D'accordo con le proposte. A2, A3 e A8 da applicare subito (fatto, in via prudenziale). A11: preferisce gli ultimi 60 mesi, oppure il 2023 dichiarato |

- **Errore di Claude nei test nuovi:** la prima stesura del test P4 dalla riga di comando usava un mercato con il 2010 negativo, e accettava 0 o 1/3. Non distingueva i due casi e il mutante E16 sopravviveva. Corretto: mercato con il 2010 positivo, valore esatto 1/3.

**Stato dopo R10:**
- test di H-002 (simulatore e programma dei criteri): 119;
- tutte le suite di dati e laboratorio: 210 test verdi; Guardian: 77/77;
- mutanti: simulatore 40/40, programma dei criteri 70/70, su Python 3.13 e 3.9.

Prossimo giro: R11, a Gemini e a ChatGPT sullo stesso commit (`collaborazione/da-claude/PROMPT-R11-GEMINI-E-CHATGPT.md`).

## R11 · Gemini, secondo attacco al programma dei criteri (`da-gemini/G-20261115-R11.md`, ramo `rev/gemini-r11`, `f8fbc7b`)
- **Sul commit `83c8956`:**
  - le sonde R7 P1–P7 risultano tutte bloccate;
  - la replica (adeguata solo ad A2 e A3) coincide entro 3,3e-16;
  - test 119/119; mutanti 40/40 e 70/70 su Python 3.9.6.
- **Secondo attacco:** 3 critici, 4 importanti e 1 minore. Tutti nei **collegamenti** (riga di comando, registro, caricatore), di nuovo.
- **Ramo controllato da Claude:** tocca solo `da-gemini/`.
- **Diagnosi di Claude:** il difetto comune è che la riga di comando lasciava **scelte libere** (periodi, ripetizioni, seme, cartella dei dati). **Correzione di classe:**
  - periodi, ripetizioni e seme diventano costanti del codice;
  - **il sigillo registra le impronte SHA-256 del codice che esegue la scheda**, e ogni esecuzione le controlla;
  - la riga di comando sceglie solo la modalità.

| Rilievo | Gravità | Esito | Correzione (TDD: `d4a5dc9` rosso, poi verde) | Mutanti |
|---|---|---|---|---|
| S1: verifica promossa con 2 trade (DSR = 1,0); finestra di verifica scelta a mano | critica | **accolto** | Periodo di verifica fisso nel codice (2005-01-01 → 2023-10-31, provvisorio); DSR solo con almeno 30 trade (come `dsr.py`) | R01 |
| S2: file vuoti nei giorni feriali aggiravano il controllo dei dati | critica | **accolto** | Un giorno feriale senza minuti, BID o ASK, ferma tutto e viene elencato. Tollerati solo il 1° gennaio, il 25 dicembre e il Venerdì Santo | R02, R03, R04 |
| S3: `--ripetizioni 1 --seme 1` accettati e non registrati | critica | **accolto** | Opzioni tolte: 1.000 ripetizioni e seme fisso, scritti nel registro | R12 |
| S4: rapporto non scrivibile bruciava la verifica; esito non registrato | importante | **accolto** | Controllo del rapporto prima di registrare; esito (promossa, DSR, R, quota, impronta del rapporto) registrato | R05, R06 |
| S5: copertura dei confronti non vincolante (5,7% promossa) | importante | **accolto** (A23 in via prudenziale) | Criteri 4 e 5 richiedono copertura ≥ 90% | R07, R08 |
| S6: cache diversa fra sviluppo e verifica; `anni=None` nell'API | importante | **accolto** | La verifica usa la stessa cache dello sviluppo; impronta SHA-256 dei dati letti nel registro; `anni` obbligatorio | R09, R13 |
| S7: varianti inventate nel registro | minore | **accolto** | Si registrano solo varianti del sigillo (anche robustezza ed esito) | R10 |
| MR01–MR07 sopravvissuti | importante (test) | **accolto** | Test nuovi. MR05 (seme della riga di comando) non esiste più: l'opzione è tolta | MR01–MR04, MR06, MR07 |
| — | — | **aggiunta di Claude** | Impronta del codice nel sigillo: con il codice cambiato, nessuna esecuzione | R11 |

- **Test rivisti dopo il commit rosso:** il test P4 (anni senza trade) usava anni **senza dati**, che dopo S2 sono un buco dei dati e vengono rifiutati, giustamente. Ora usa anni con i dati ma senza trade (mercato piatto).
- **Posizioni di Gemini su A12–A21:** registrate nella proposta v3.2.

**Stato dopo R11:**
- test di H-002: 138; tutte le suite di dati e laboratorio: 229 verdi; Guardian 77/77; su Python 3.13 e 3.9.
- Mutanti:
  - simulatore 40/40;
  - programma dei criteri 89/89, su Python 3.13 e 3.9. Al giro completo erano 87/89: S06 era coperto dal nuovo controllo sulle varianti, MR02 da quello sui feriali vuoti, tranne che in un periodo di soli giorni non feriali. Aggiunti 2 test; rieseguiti i due mutanti, morti su entrambe le versioni. Un test in più non può far sopravvivere un mutante già ucciso.
- Prossimo giro: R12 (Gemini) e messaggio 2 del DGS (ChatGPT), sullo stesso commit.

## INCIDENTE del 14/11/2026: H-002 eseguita sui dati veri dello sviluppo PRIMA del sigillo
**Cosa è successo** (verificato da Claude il 15/11 solo sui nomi dei file, sul codice e sulle intestazioni, senza leggere i risultati):
- Il 14/11 Gemini ha pubblicato tre rami nuovi non richiesti da Claude: `rev/gemini-dgs03` (`cfa4a3b`, `1e0c73f`), `rev/gemini-analisi-h002` (`d5103a8`) e `rev/gemini-proposte-tester-dgs03` (`a0e1b7b`…`1fec51c`).
- `misura_dgs03.py` e `analisi_h002_esplorativa.py` caricano **la cache vera del Mac** (`brain/dati/reali/cache_dukascopy`) sul periodo di sviluppo 15/11/2023 → 12/11/2026 ed eseguono il simulatore di H-002. Ci sono anche analisi «esplorative» per ampiezza, direzione e anno.
- Gemini dichiara di non aver letto il periodo di verifica (fino al 31/10/2023). Claude non l'ha ancora controllato riga per riga.
- Le misure rispondono a un punto «DGS-03», a quanto pare della prima relazione di ChatGPT (DGS). Claude non ha ancora ricevuto quella relazione.
- `rev/gemini-proposte-tester-dgs03` **modifica file di Claude** (simulatore, criteri, esecutore, test, registro dei difetti) e una regola della scheda (uscita di fine sessione). È contro il protocollo (Gemini scrive solo in `da-gemini/`). Non è unito.

**Regole violate:**
- scheda v3.1 §10: il sigillo viene prima di qualunque esecuzione;
- mandati R7, R11 e R12: niente dati reali.

**Contaminazione dichiarata:**
- **Chi conosce i risultati:** Gemini; chi ha letto i rapporti (da verificare: utente, ChatGPT).
- **Claude:** cercando chi avesse chiesto le misure, ha visto involontariamente **una riga di sintesi del risultato statistico** sullo sviluppo. Il contenuto resta nel rapporto di Gemini e non viene ripetuto qui. Da ora le proposte di Claude sulle regole che cambiano i trade di H-002 (A12, A15, A17 e simili) **non sono cieche**.
- **Il periodo di verifica resta intatto**, se la dichiarazione di Gemini è vera. È lui la vera prova (DA-26).

**Conseguenze proposte da Claude (decide l'utente):** vedi CONTINUITA, «Incidente del 14/11».

### Revisione esterna del nucleo statistico (15/11), archiviata in `collaborazione/da-revisori-esterni/2026-11-15-nucleo-statistico-e-incidente.md`
- **Contiene i risultati di H-002 sullo sviluppo,** con l'autorizzazione dell'utente. **Claude l'ha letta per intero il 15/11: da ora è non cieco sullo sviluppo**, cieco sulla verifica.
- **Punti accolti da Claude:**
  - N va contato, non dichiarato. V-T e V-S condividono il 100% degli ingressi; il moltiplicatore 6 del filtro è una superficie di selezione mai giustificata;
  - **il veto di robustezza relativo («−50% rispetto alla base») è mal tarato:** respinge una strategia valida molto spesso (stima del revisore: 24–81% secondo la correlazione fra le prove). La funzione di perdita non è mai stata scritta;
  - **la verifica 2005–2023 non è lo stesso test senza gli ASK storici:** il costo entra nel filtro d'ammissione;
  - **lo stato dei dati è da verificare,** non «pronto»: computer spento durante lo scaricamento; copertura storica solo dichiarata.
- **Controllo di Claude sul rischio di file troncati:**
  - lo scaricatore scrive in un `.tmp` e poi rinomina (`dati/pipeline/dukascopy.py:115-117`), ma senza forzare la scrittura su disco: dopo uno spegnimento brusco non si può escludere un file vuoto o parziale;
  - un file parziale fa fallire la decompressione (righe 130-132); un file vuoto in un giorno feriale lo ferma il controllo R11-S2. Restano da cercare i `.tmp` residui.
- **Da chiarire con l'utente:**
  - la «soglia r = 0,15 R sigillata il 14/11», che non è nel repository;
  - il «documento autoportante sul nucleo statistico», consegnato al revisore il 14/11: chi l'ha prodotto, e su quali esecuzioni dei dati veri.

### Revisione di Claude sul proprio lavoro (15/11, su richiesta dell'utente)
- **Correzione di un'affermazione di Claude all'utente:** «dai numeri del rapporto il criterio 1 boccia H-002» era troppo forte.
  - L'intervallo citato dal revisore (IC netto da −0,158 a +0,056) non dice a quale variante si riferisce: dai conteggi delle uscite è quasi certamente V-T.
  - Per V-S il rapporto non dà la media.
  - L'esito lo decide solo lo screening ufficiale.
- **Limite del blocco tecnico `7d2fc71`, da non sopravvalutare:** ferma un uso **per errore** (gli script di Gemini sarebbero stati fermati). Non ferma un uso **voluto**: chiunque può creare un sigillo in un registro di prova, oppure leggere i file `.bi5` senza passare dal caricatore.
  - La protezione vera è di processo: il registro vero e il sigillo stanno nel repository, le impronte del codice sono nel sigillo, e gli agenti che fanno revisione lavorano senza accesso alla cache dei dati.
- **Istruzioni per il controllo della cache:** la prima versione non indicava il periodo atteso, quindi un archivio finito prima del previsto non sarebbe risultato. Corretto nelle istruzioni per il Mac: lo sviluppo si controlla con il periodo esplicito, lo storico mostra l'ultima data per anno.
- **Stato dopo il blocco:** 139 test di H-002; tutte le suite di dati e laboratorio 238 verdi; Guardian 77/77; su Python 3.13 e 3.9. **Riesecuzione completa dei mutanti: simulatore 40/40, programma dei criteri 89/89, controllo della cache 11/11, su Python 3.13 e 3.9.**

### Chiarimento dell'utente sulla «soglia r = 0,15» (15/11)
- **Non è una soglia operativa** né un sigillo: è un **impegno anticipato**. Il 14/11, prima di vedere il «banco di taratura del motore», l'utente ha scritto che il vantaggio minimo che sceglierebbe oggi è 0,15 R per trade. Va confrontato con il numero che sceglierà dopo il banco.
- **Registrato** in `governance/IMPEGNI-ANTICIPATI.md`, voce IA-01.
- **Il criterio della scheda v3.1 non cambia:** R medio netto ≥ +0,05 R.
- **Da documentare:** il «banco di taratura del motore».

## Rapporti del DGS 01–04 (ChatGPT, 14/11; archiviati in `collaborazione/da-chatgpt/`), lettura di Claude del 15/11
**Cronologia ricostruita dai rapporti (dichiarazioni dell'utente riportate dal DGS, non verificate da Claude):**
1. **DGS-01:** insediamento su `83c8956`. Rilievi DGS-01…DGS-12. Il più rilevante per la scheda è **DGS-03**.
2. **Misure di Gemini sui dati veri dello sviluppo:** riguardano DGS-03. Gemini ha comunicato all'utente gli R medi di V-T e V-S su 456 trade (T1 di DGS-03).
3. **DGS-03:** con quei numeri, **H-002 «respinta»** sul criterio 1 dello screening.
4. **Disposizione successiva dell'utente («Una correzione»):** **H-002 = «NON DECIDIBILE · PARCHEGGIATA»**, registrata dal DGS in DGS-04 §1.

**Posizione di Claude (decide l'utente):**

| Punto | Giudizio | Motivo |
|---|---|---|
| DGS-03: l'uscita di fine sessione senza quotazioni usa un prezzo **precedente** alle 16:30, scelto in base all'assenza di quotazioni **successive** | **accolto, critico (difetto della scheda, ripetuto fedelmente dal simulatore)** | È uno sguardo al futuro nella regola: alle 16:29 non si sa ancora se arriveranno quotazioni. Va corretto **prima** di qualunque sigillo, con una regola eseguibile solo in avanti. La misura sullo sviluppo (0 casi su 456) dice che lì non ha pesato. Nel periodo vecchio può pesare di più |
| DGS-10: dati personali nel pacchetto per i revisori | **accolto: errore di Claude** | Claude aveva scritto «nessun dato personale» controllando solo email e stipendio. Nel pacchetto c'erano nome, utente GitHub e percorsi del Mac (20 file e 45 righe secondo il conteggio dell'utente). Il prossimo pacchetto per revisori va redatto con una scansione per classi, compresi gli archivi interni |
| DGS-01 §4.1: SR₀ (soglia di riferimento del DSR) confuso con lo Sharpe osservato necessario | **accolto: errore di Claude** | In R2/R4 «circa 0,047» era SR₀, non lo Sharpe osservato da superare (circa 0,121 nell'esempio con N = 4 e T = 500) |
| DGS-04 (N con la robustezza), poi ritirato con l'emendamento dell'utente | **d'accordo con l'emendamento** | La robustezza resta fuori da N solo come veto fisso; se orienta una scelta, l'esclusione decade |
| **Riclassificazione di H-002 da «respinta» a «non decidibile · parcheggiata»** | **contraria alla regola scritta prima, segnalata come scelta da rivedere** | La scheda v3.1 §8, scritta prima dei risultati, dice: un criterio non passato boccia la variante; «se nessuna variante passa, H-002 è chiusa e non si ritocca». Le due stime puntuali stanno sotto la soglia di +0,05 R di circa 0,10 e 0,12 R. Cambiare la **categoria** del verdetto dopo aver visto i numeri è il tipo di scelta che il metodo vuole impedire, anche se lo screening non era ancora sigillato. È vero che statisticamente l'esito è inconclusivo (l'intervallo arriva poco sopra la soglia). **Proposta:** registrare entrambe le cose. Esito per la regola: BOCCIATA su questo campione. Nota statistica: incertezza alta. Se l'idea si vuole riprovare, è un'**ipotesi nuova** (H-002b), sigillata e contata in N, su dati **futuri**. Lo schema a tre esiti (promossa / bocciata / non decidibile) è sensato, ma solo per le ipotesi **future**, adottato prima dei loro dati |
| Il DGS ha accolto la riclassificazione senza contestarla | **rilievo sul processo** | In DGS-03 aveva scritto «respinta». In DGS-04 ha registrato la disposizione dell'utente senza confrontarla con il §8 della scheda. È proprio il caso in cui il suo ruolo (la parte scomoda) dovrebbe opporsi o almeno nominare il conflitto |
| Richieste del DGS a Gemini di lavorare ancora sui dati dello sviluppo (DGS-04 §8) | **sospese** | Sono il canale da cui è nato l'incidente del 14/11. Prima serve un registro delle esecuzioni sui dati veri e l'autorizzazione scritta dell'utente per ciascuna |
| Richieste del DGS a Claude (Gate 4 e riserve, registro di consumo, 404 contro risposta vuota, tre esiti, scheda di stato, pacchetto redatto, emendamento nel mandato e in DA-19) | **da pianificare** | In ordine di priorità, dopo la decisione dell'utente su H-002 e il censimento delle esecuzioni (vedi CONTINUITA) |

**Decisione dell'utente (15/11/2026, dopo la posizione di Claude qui sopra):** H-002 resta **«non decidibile · parcheggiata» per ora**. Claude ha esposto le due opzioni (A bocciata su questo campione; B parcheggiata) e raccomandato A; l'utente ha scelto B, con «per ora». Conseguenze, uguali nei due casi: H-002 **non va in verifica**, la riserva 2005–2023 resta intatta, le esecuzioni del 14/11 entrano nel censimento di N. Resta aperto: con quale condizione, scritta prima, H-002 esce dal parcheggio. Senza una condizione fissata ora, il parcheggio non deve diventare una porta per riprovarla sugli stessi dati.

**Condizione d'uscita dal parcheggio (approvata dall'utente il 15/11/2026):** H-002 esce dal parcheggio **solo** con una prova su dati **successivi al 12/11/2026**, con scheda sigillata **prima** di vederli e contata in N. **Mai** rieseguita sui dati dello sviluppo (15/11/2023 → 12/11/2026). La patch di `tb-proposte` (riprova sugli stessi dati finché esce «promossa») è quindi esclusa anche per regola.

**Censimento di N:** le trascrizioni delle conversazioni di Gemini sono sul Mac, in formato JSONL (`~/.gemini/antigravity/brain/`, indicazione dell'utente del 15/11). Il censimento va fatto da lì, estraendo **solo** i comandi eseguiti sui dati veri, con data, senza gli output.

## R12-bis · Terzo attacco di Gemini (16/11/2026)

Rapporto: `collaborazione/da-gemini/G-20261116-R12bis.md` (commit `3ad6d77`, identità di Gemini, base `ccdac1f`, solo file in `da-gemini/`). **Regole del mandato rispettate**, con una violazione accidentale dichiarata da Gemini: al passo 13 una richiesta vera a Dukascopy (2/1/2024, sviluppo) per un mock che non arrivava, causa un difetto di Claude (#58).

**Riproduzione di Claude:** tutte le sonde A3, B e C rieseguite sul ramo di Gemini con la rete bloccata: risultati identici. A1 (14/14 difetti storici bloccati), A2 (replica uguale, differenza ≤ 3,3e-16) e i mutatori ufficiali (40/40, 89/89, 20/20) confermano lo stato precedente.

| Rilievo | Giudizio di Claude | Motivo |
|---|---|---|
| A3-01 codice fuori da `FILE_CODICE` | **accolto, importante** (#48) | Le impronte devono coprire tutto il codice `brain` eseguito, non un elenco scritto a mano |
| A3-02 un tick basta | **accolto, importante** (#49) | Dati quasi vuoti brucerebbero la verifica unica |
| A3-03 festività spostate | accolto, minore (#50) | Sbaglia dalla parte sicura (blocca senza bruciare) |
| A3-04 registro manomissibile | **accolto, importante** (#51) | Serve un'impronta a catena confrontabile con la versione su GitHub |
| A3-05 uscita all'indietro | già noto (#42) | H-002 parcheggiata; regola obbligatoria nel modello H-003 |
| B-01 Retry-After data | accolto, importante (#52) | |
| B-02 cache e registro dopo un'interruzione | **accolto, importante** (#53) | È il caso dello spegnimento del 16/11 |
| B-03, B-05 | accolti, minori (#54, #55) | |
| B-04 un 404 azzera gli errori di fila | **respinto** | Un 404 è una risposta valida del server: non è un blocco. Il fermo dopo 20 errori di fila serve a riconoscere un blocco vero, non a contare gli errori sparsi; questi restano nel registro e danno codice 5 |
| C-01/C-02 punti ciechi del riconteggio | accolti, importanti (#56) | |
| C-03 stampa di contenuti | **accolto, importante** (#57) | |

**Esito per la regola d'uscita (proposta v3.2 §C):** R12-bis ha trovato difetti importanti: il contatore dei giri puliti di fila resta a zero.

**Correzioni (16/11):** #48–#58 corretti in TDD (eccetto A3-05, già noto, e B-04, respinto); trovato e corretto #59 (mutanti non validi). Commit `b0525a9`, `b8c211e`, `774573d`. Dettaglio in `governance/REGISTRO-MODIFICHE.md` v1.40–v1.41.

## R13 · Quarto attacco di Gemini (16/11/2026)

Rapporto: `collaborazione/da-gemini/G-20261116-R13.md` (commit `6e17782`, identità di Gemini, base `fd879ed`, solo file in `da-gemini/`, rete bloccata in tutte le prove). Sonde A, B e C1 rieseguite da Claude con la rete bloccata: risultati coincidenti.

**Verifica delle correzioni R12-bis (compito A):** chiusi #50, #52, #53, #54, #55, #57, #58; chiusi in parte #48, #49, #51, #56, #59; A3-05 (#42) noto.

| Rilievo | Giudizio di Claude | Motivo |
|---|---|---|
| R13-A-01 controprova di B-04 | **accolto: Claude aveva torto** (#67) | Con un blocco su tutti i feriali, i 404 del fine settimana azzerano il conteggio ogni 5 giorni: il fermo non scatta mai. Il conteggio va azzerato solo da un giorno con dati |
| R13-B-01 ambiente | **accolto, importante** (#61) | Si controllerà l'origine di ogni modulo caricato (libreria standard o file sigillati, con impronta del file davvero caricato) all'avvio e prima di scrivere i risultati |
| R13-B-02 ancora git | **accolto, importante** (#62) | Registro identico alla HEAD prima di ogni esecuzione, HEAD su un ramo, discendente della versione su GitHub (ramo remoto), niente collegamenti simbolici |
| R13-B-03 completezza | **accolto, importante** (#63) | Ogni terzo della sessione deve avere minuti; nelle vigilie almeno il mattino |
| R13-B-04 vol = 0 e mezze giornate | **respinto in parte** | Un giorno con soli minuti a volume 0 è un giorno senza scambi: vuoto è corretto. Il 3 luglio la sessione di Londra è piena (chiude prima solo New York): l'esempio non corrisponde a una giornata vera |
| R13-B-05 38 festività tollerate | **respinto, rischio annotato** | La tolleranza vale solo se il giorno è VUOTO: se Dukascopy ha dati non cambia nulla. Il rischio residuo (un buco del feed proprio in un festivo britannico passa inosservato) è basso e dichiarato |
| R13-B-06 robustezza | accolto, minore (#69) | I nomi delle prove di robustezza si registrano al sigillo |
| R13-C1-01, C1-02 riserva | **accolti, importanti** (#64, #65) | Ancora a git come per il registro delle prove, più controlli dei valori |
| R13-C2-01 potenza | accolto, minore (#70) | Controlli del dominio; varianza campionaria isolata e provata |
| R13-D-01 test in rete | **accolto, importante** (#66) | Test con risposte finte; gli script di mutanti bloccano la rete da soli e segnalano il tempo scaduto |
| R13-A-02 date compatte | accolto, minore (#68) | |
| R13-A-03 DGS-03 | già noto (#42) | |

**Per la regola d'uscita:** R13 ha trovato difetti importanti: contatore dei giri puliti a zero.

## R14 di Gemini (17/11/2026)

- **Consegna:** `brain/collaborazione/da-gemini/G-20261117-R14.md`, commit `e305e4a` su `rev/gemini-r14`, partito da `6b1b136`. Rilievi classificati per tipo (E o M) e costo, come chiesto (D-24).
- **Verificate chiuse da Gemini:** #86 (secondo registro, ramo nuovo, etichette), #89, #90 (salvo il limite dichiarato), #91, #93, #94 a/c/d, #73–#85, riconteggio 51/51, controllo della cache 20/20, scaricatore 50/50.
- **Rilievi:**
  - **R14-01, critico, M a costo basso:** conta per D-24.
  - **R14-02, R14-03, R14-04, R14-05, importanti:** R14-02 era un difetto dei miei test.
  - **R14-06…R14-09, minori.**
- **Riproduzione:** Claude ha riprodotto R14-01 e R14-02 prima di correggere. Tutti sono corretti in TDD come #96–#104 (`79e6b4e`, poi rosso, `b6a2c3e`).
- **Per la regola d'uscita:** R14 ha trovato un difetto critico che conta (M a costo basso, D-24) e quattro importanti. **Il contatore dei giri puliti resta a zero.**

## R15 di Gemini (17/11/2026)

- **Consegna:** `collaborazione/da-gemini/G-20261117-R15.md` (commit `6509a00`).
  - Candidato `8e51ce9` dichiarato.
  - Ambiente dichiarato: Apple Python 3.9.6, macOS 14.5 arm64, opzioni con e senza `-I` (parere P6).
- **A:** tutte le correzioni #86–#104 verificate come chiuse. #104 è chiuso in parte (vedi #106). Gli script BANCO-02 e R14 rilanciati sul registro canonico: tutti «ATTACCO RESPINTO».
- **B, taratura su 80 mercati inventati** (20 semi × 4 livelli di spinta, `sintetico.mercato`, `esegui_sviluppo`). È il primo dato sul comportamento dell'intera procedura di screening:

  | Spinta | Promozioni | R medio V-T |
  |---|---|---|
  | **0** (nessun vantaggio) | **0 / 20** | −0,06 |
  | 0,005 | 2 / 20 | +0,11 |
  | 0,01 | 16 / 20 | +0,27 |
  | 0,02 | 17 / 20 | +0,57 |

  A spinta 0,02 i 3 mancati sono solo per il minimo di 300 trade. Con vantaggio debole il segnale si perde soprattutto sul veto di robustezza e sul drawdown.

  **Limite:** sono mercati del generatore del progetto (lo stesso autore del codice), con 20 semi. L'intervallo del caso nullo arriva al 16%.
- **C:** 6 sonde, 6 mutanti nuovi uccisi; rilievi minori #107–#111.
- **D sul Mac:** riconteggio 53/53, controllo della cache 20/20, scaricatore 50/50. Mutanti dell'esecuzione fermi per #106; 1/353 test fallito (#106).
- **Per la regola d'uscita (D-24):** Gemini segnala due casi «dubbio» per il titolare: #106 (difetto di un test, non del codice sigillato) e #108. Se il titolare li esclude, R15 è il **primo giro pulito**. Nel frattempo il contatore resta a **0 su 2**.

