# H-002 · Rottura del range di apertura di Londra e New York su XAUUSD (BOZZA per la revisione, NON sigillata)

**Stato:** bozza di Claude del 14/11/2026, scritta su richiesta dell'utente per una revisione critica prima del sigillo.
- **Valori di partenza:** dove l'utente non ha ancora scelto, i valori sono **proposte di Claude** (segnate [P]).
- **Uso:** nessun test è stato fatto. Nessuno guarda risultati prima del sigillo.

## 1. Ipotesi in una frase
Dopo i primi 30 minuti di Londra o di New York, la prima chiusura a 15 minuti fuori dal range di apertura indica la direzione del resto della sessione più spesso di quanto basti a pagare i costi.

**Perché potrebbe esistere:** all'apertura entrano i flussi della sessione (banche europee, poi USA e mercato dei future). La rottura del range iniziale indicherebbe quale lato prevale.
**Perché potrebbe NON esistere:**
- è una strategia nota e pubblicata da decenni (Crabel 1990; Zarattini e Aziz 2023 sulle azioni USA), quindi un eventuale vantaggio può essersi esaurito (McLean e Pontiff 2016);
- sull'oro a 15 minuti non conosciamo prove pubblicate;
- lo Studio 1 (E-001) non ha trovato nessuna struttura direzionale chiaramente diversa dal caso.

## 2. Dati
- **Fonte:** XAUUSD, candele BID da 1 minuto di Dukascopy, aggregate a 15 minuti in UTC. Il minuto per minuto serve per stabilire se arriva prima lo stop o il target (§4).
- **Sviluppo:** dal 15/11/2023 al 12/11/2026 (DA-26, già visto dall'utente).
- **Verifica sigillata:** dal 2005 a circa il 31/10/2023 (date esatte in DA-26); una sola prova per ogni variante promossa.
- **Prezzi di acquisto:** ASK = BID + spread dello scenario di costo (§5). Non abbiamo l'ASK storico.

## 3. Definizioni (orari nei fusi delle borse, ora legale inclusa)
| | Londra | New York |
|---|---|---|
| Sessione | 08:00–16:30 Europe/London | 09:30–16:00 America/New_York |
| Range di apertura (RA) | 08:00–08:30 | 09:30–10:00 |
| Ultimo ingresso possibile [P] | candela che apre alle 15:15 | candela che apre alle 14:45 |
| Ora italiana (indicativa) | sessione 09:00–17:30, RA 09:00–09:30 | sessione 15:30–22:00, RA 15:30–16:00 |

- **RA alto / RA basso:** massimo e minimo delle candele da 1 minuto del range di apertura. **Ampiezza** A = alto − basso.
- **Ampiezza normale [P]:** A fra 0,5 e 2 volte la mediana delle ampiezze del range di apertura della **stessa sessione** nei 20 giorni precedenti. Fuori da questi limiti, quel giorno non si opera.
- **Giorni validi:** dal lunedì al venerdì, con almeno l'80% dei minuti del range di apertura presenti nei dati.

## 4. Regole di trading
1. **Segnale:** la prima candela da 15 minuti, completa e aperta dopo la fine del range di apertura ed entro l'ultimo ingresso possibile, che **chiude** sopra RA alto (acquisto) o sotto RA basso (vendita).
2. **Ingresso:** a mercato, all'apertura della candela da 15 minuti successiva, con spread e slittamento (§5).
3. **Stop:** il lato opposto del range di apertura (RA basso per l'acquisto, RA alto per la vendita). Rischio = distanza ingresso–stop.
4. **Uscita:** due varianti dichiarate (§7):
   - **V-T:** target a +1,5 × rischio, altrimenti chiusura a fine sessione;
   - **V-S:** nessun target, chiusura a fine sessione.
5. **Un solo trade per sessione e per giorno.** Niente rientri dopo uno stop.
6. **Ordine degli eventi:** si scorre minuto per minuto. Se nello stesso minuto si toccano sia lo stop sia il target, conta lo stop (scelta prudente).
7. **Niente posizioni oltre la fine della sessione,** quindi mai oltre la notte né il weekend.
8. **Notizie:** il filtro P-08 (15 minuti prima e dopo i dati ad alto impatto) richiede un calendario storico che non abbiamo.
   - Il **primo test è senza filtro notizie, ed è dichiarato.**
   - Il filtro verrà aggiunto come variante separata, contata, quando avremo il calendario.
   - Limite noto: la riunione della Fed (FOMC, 14:00 New York) cade dentro la sessione di New York.

## 5. Costi e dimensione della posizione
- **Spread:** tre scenari (0,20 / 0,35 / 0,50 USD per oncia). **Lo scenario di riferimento è 0,35** finché non avremo gli spread misurati su FP Markets.
- **Commissione [P]:** 7 USD per lotto di 100 once andata e ritorno, cioè 0,07 USD per oncia. Da sostituire con quella reale.
- **Slittamento:** 0,10 USD sugli stop e sugli ingressi a mercato. È una stima.
- **Dimensione:** rischio dello 0,5% del conto (P-01) diviso per (distanza dallo stop + costi), arrotondato per difetto a 0,01 lotti.
- **Stop giornaliero 1,5% (P-05):** con 2 trade al giorno al massimo non si raggiunge; si controlla comunque.

## 6. Metriche, tutte in R (1R = rischio del trade)
- Numero di trade, percentuale di vincite, R medio netto (aspettativa), Sharpe per trade, DSR con tutte le prove contate (DA-28).
- Drawdown massimo in R, serie peggiore di perdite consecutive.
- **Stabilità:** risultato per trimestre e per anno; acquisti e vendite separati, perché il periodo di sviluppo è stato quasi tutto in salita e gli acquisti potrebbero vincere solo per la tendenza.
- Simulazione della fase 1 FTMO con il limite giornaliero del 5%.
- **Confronto casuale:** stessi orari di ingresso e stesse regole di uscita, ma direzione estratta a caso (1.000 ripetizioni). La strategia deve stare sopra il 95° percentile.

## 7. Conteggio delle prove (DA-19)
**Prove dichiarate:** Londra V-T, Londra V-S, New York V-T, New York V-S, cioè **4 prove**. Entrano tutte nel registro e nel DSR, anche quelle che falliscono.

**Robustezza, che non sceglie niente:** si rifà il test cambiando un parametro alla volta del ±20–30%:
- range di apertura di 20 e 45 minuti;
- target 1,2 e 2,0;
- filtro dell'ampiezza 0,4–2,5.

Queste prove possono solo **bocciare** una variante (se il risultato crolla), **mai** sostituire i parametri.

## 8. Criteri scritti prima
**Sviluppo (per ogni variante):**
- aspettativa netta ≥ +0,05R nello scenario a 0,35;
- e DSR ≥ 0,95 con N = 4 più le prove già registrate;
- e almeno 300 trade;
- e sopra il 95° percentile del confronto casuale;
- e risultato non negativo in almeno 2 anni su 3;
- e non crolla nella robustezza.

Altrimenti la variante è bocciata.

**Verifica sigillata (una sola volta, solo per le varianti promosse):**
- aspettativa netta > 0 nello scenario a 0,35;
- e risultato positivo in almeno il 60% degli anni;
- e DSR ≥ 0,95 sul periodo di verifica.

Limite noto: gli spread del 2005–2012 erano più larghi. Si riporta anche lo scenario a 0,50.

**Se nessuna variante passa:** H-002 è chiusa. Non si ritoccano i parametri per farla passare.

## 9. Punti deboli già noti (autocritica di Claude)
1. **Un solo tipo di mercato nello sviluppo** (2023–2026, oro in forte salita): gli acquisti possono sembrare buoni solo per la tendenza.
2. **Apertura di New York alle 09:30:** è l'apertura della borsa azionaria. Per l'oro conta anche quella dei future (08:20 New York) e i dati USA delle 08:30. La scelta è discutibile, ed è fissata prima per evitare di sceglierla dopo.
3. **Spread all'apertura delle sessioni:** può essere più largo della media proprio quando si entra.
4. **Senza filtro notizie** il test non rispetta P-08.
5. **Dati Dukascopy:** l'utente guarda i grafici di FXCM e opererà con altri broker. Servirà il confronto con lo storico MT5 (criterio di discordanza ancora da decidere).
6. **Il filtro sull'ampiezza (0,5–2)** è una stima senza base: è il primo candidato all'eccesso di adattamento.
7. **Un solo trade per sessione:** pochi trade per decidere in demo, circa 2 al giorno.

## 10. Domande per i revisori
1. Le regole sono **eseguibili senza ambiguità** da un programma? Dove no?
2. C'è qualche **sguardo al futuro** (dati non disponibili al momento della decisione)?
3. I **costi** sono realistici per XAUUSD con un broker con spread bassi (Raw)? Cosa manca?
4. Le **4 varianti** sono quelle giuste? Ne togliereste o cambiereste qualcuna?
5. I **criteri del §8** sono troppo deboli o troppo severi?
6. Cosa può far sembrare buona la strategia nello sviluppo e poi farla fallire nella verifica o in demo?
