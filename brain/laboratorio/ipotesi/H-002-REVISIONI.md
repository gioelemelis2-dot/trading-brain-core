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

## Prossimo passo
Quando arriva R2: versione 2 della scheda con le correzioni accolte, e l'elenco delle scelte che restano all'utente (sessione, uscita, stop, numero di prove). Solo dopo, il sigillo.
