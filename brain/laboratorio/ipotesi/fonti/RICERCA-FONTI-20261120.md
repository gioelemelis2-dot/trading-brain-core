# Ricerca di fonti di idee oltre Brad Goh (Claude, 20/11/2026)

**Su richiesta del titolare** («fai la ricerca completa adesso»). Ricerca sul web: 11 interrogazioni.

**Questo documento non registra idee.** Ogni riga del registro della provenienza la decide il titolare.

**Provenienza da annotare:**
- Claude ha letto queste fonti il 20/11/2026.
- Se un'idea ne deriva, la scheda dovrà dichiararlo (D-32, testo G).
- Poiché la scelta delle fonti è di Claude, la revisione indipendente spetta ad altri.

**Limite:** quasi sempre ho letto **riassunti e abstract**, non i testi integrali. Le cifre citate sono quelle delle fonti, non verificate da me.

## Criteri di valutazione (gli stessi del dossier P-001)

| Criterio | Domanda |
|---|---|
| **Regole** | Sono abbastanza precise da tradurle in un programma senza inventare? |
| **Evidenza** | Peer review, revisione certificata, verifica fuori campione, replica da terzi, oppure solo dichiarazioni? |
| **Adattabilità** | Funziona su oro o forex, intraday, nelle nostre sessioni? Produce abbastanza trade (circa 300 in 1.000 sedute)? |
| **Incentivi** | Chi la propone vende qualcosa? |
| **Periodo** | Su quali anni è stata provata? Se si sovrappone alla nostra riserva (2005–2023), quell'informazione è «già vista» |

## 1. Fonti accademiche (regole chiare, dati pubblici)

| Fonte | Che cosa dice | Valutazione |
|---|---|---|
| **Gao, Han, Li, Zhou (2018)**, «Market intraday momentum», *Journal of Financial Economics* | Sulle azioni USA, il rendimento della prima mezz'ora predice quello dell'ultima | Regola chiarissima. Peer review. Non sull'oro |
| **«Intraday Time Series Momentum: International Evidence»** (Li e coll., Reading/Lancaster) | Lo stesso effetto in **12 mercati su 16** | Replica indipendente su più mercati |
| **Working paper MPRA 97134** | Lo stesso effetto su **4 futures su materie prime** | Da leggere per capire quali materie prime |
| **«The night effect of intraday trading: Chinese gold and silver futures»** (2025, ScienceDirect) | **Momentum e inversione intraday esistono sull'oro (futures cinesi)**, ma dipendono dalla sessione e dall'apertura notturna | La fonte più vicina all'oro intraday. Mercato diverso dal nostro |
| **Caminschi e Heaney (2014)**, «Fixing a Leaky Fixing», *Journal of Futures Markets* 34(11) | Intorno al fixing PM di Londra (fino al 2015) le informazioni trapelavano: i primi minuti predicevano la direzione del fixing | Meccanismo strutturale. **Attenzione:** a marzo 2015 il fixing è stato sostituito dall'asta LBMA/ICE, quindi è un **cambio di regime dentro la nostra riserva** |
| **Abrantes-Metz e Metz** (2001–2013) | Movimenti anomali, soprattutto al ribasso, intorno al fixing delle 15:00 | Stesso cambio di regime del 2015 |
| **Studio sugli annunci FOMC e l'oro ad alta frequenza** (Manchester Metropolitan / KFUPM) | La reazione dell'oro continua **oltre i 5 minuti** dopo l'annuncio: possibile inefficienza di breve durata | Interessante, ma **pochi eventi** (circa 8 all'anno, circa 150 nella riserva): potenza bassa |
| **Hauptfleisch, Putniņš e Lucey** (1997–2014) | La scoperta del prezzo dell'oro si sposta fra Londra (spot) e New York (futures) durante il giorno | Contesto utile per scegliere le finestre orarie |

## 2. Trader con risultati certificati

| Fonte | Che cosa dice | Valutazione |
|---|---|---|
| **Andrea Unger** (italiano; World Cup Trading Championship 2008, 2009, 2010, 2012) | Sistemi automatici, da 4 nel 2008 a 30–80 al mese. Dichiara un rendimento reale del 20–30% annuo | Risultati certificati dal campionato. **Regole non pubbliche:** vende corsi e un libro. Utile per il **metodo** (robustezza, portafoglio di sistemi, costi rispetto al trade medio), non per una strategia pronta |
| **Kevin Davey** (WCTC; 148%, 107%, 112% in tre anni) | Libro «Building Winning Algorithmic Trading Systems»: obiettivi fissati prima, dati dentro e fuori campione, **test una sola volta senza ritocchi** | **Lo stesso spirito della nostra macchina.** Utile per migliorare il processo, non come fonte di una strategia |
| **Larry Williams** (WCTC 1987, rendimento dichiarato 11.376%) | Rottura di volatilità: ingresso all'apertura più o meno una frazione del range del giorno prima | Regola semplice e pubblicata nei suoi libri. Giornaliera, quindi meno trade. Va verificata sui testi originali |
| **Toby Crabel** (1990) | Rottura del range d'apertura, giorni a range stretto | Antenato di H-002. Regole pubbliche |

## 3. Test indipendenti (i più utili per evitare errori)

| Fonte | Esito | Che cosa ci insegna |
|---|---|---|
| **«Silver Bullet [GBB]»**: test meccanico delle ore «Silver Bullet» di ICT su futures ES, NQ, YM e **GC (oro)**, 2011–2026, a 1 minuto, con costi e anni tenuti da parte | **Le ore «Silver Bullet» non hanno niente di speciale**. Il modello da solo non è profittevole. Lo stop migliora un po' i risultati senza renderli positivi | **Prova contraria, pertinente, sulla scuola ICT**, che è anche quella di Brad. Abbassa le aspettative su P-001. Non lo chiude: è la traduzione di un altro autore |
| **Replica fuori campione dello studio Zarattini, Aziz e Barbon su SPY** (Sheimy Paz, SSRN) | Sharpe **da 1,33 a 0,39** fuori campione | Anche gli studi seri **perdono gran parte del vantaggio** dopo la pubblicazione. Dobbiamo aspettarcelo |
| **Deriva notturna dell'oro** (Quantpedia; Quantified Strategies) | L'effetto esiste ma è piccolo. Il «+30% annuo» era un artefatto dei dati giornalieri (OHLC); **dopo i costi probabilmente non è sfruttabile** | Esempio di risultato gonfiato dal tipo di dati: con i prezzi d'apertura e chiusura reali sparisce |

## 4. Fonti pratiche non verificate (solo spunti)

- **Trade That Swing: «Initial Balance Breakout» sull'oro.** Un trade al giorno, regole complete, «+445% nell'ultimo anno» dichiarato dall'autore. È della famiglia della rottura del range (H-002, Crabel).
- **«Successful Traders Stories» di FTMO.** Singoli conti, alcuni con scalping sull'oro e profitti concentrati in certe ore. Sono aneddoti, non statistiche.
- **Pagine dei broker sulla rottura all'apertura di Londra** (per esempio «range 7:30–8:00 GMT, ±10 pip»). Spunti senza prove.

## 5. Che cosa ne ricavo (IPOTESI di Claude, per la scelta del titolare)

**Le famiglie più promettenti da provare sull'oro**, dopo la macchina:
1. **Momentum intraday per sessioni** (Gao e repliche, studio cinese sull'oro del 2025). Regola semplice, molti trade, prove accademiche su altri mercati.
2. **Rottura del range di sessione** (Crabel, H-002, initial balance). Abbiamo già metà dell'infrastruttura. Famiglia unica: ogni variante conta in N.
3. **Il piano meccanico pubblico di Brad (P-001)**, con i filtri di calendario. Da provare, ma con **aspettative ridotte**: il test indipendente sulla scuola ICT è negativo.

**Da evitare o da trattare con cautela:**
- strategie legate al fixing di Londra: il regime è cambiato nel 2015, a metà della riserva;
- la deriva notturna: i costi la annullano;
- gli eventi FOMC: troppo pochi per la nostra potenza.

**Per il processo, più che per le strategie:** Davey e Unger confermano l'impostazione della nostra macchina (regole prima, una sola verifica, costi). Unger aggiunge l'idea di un **portafoglio di molti sistemi semplici**, invece di uno solo perfetto.

**La lezione generale:**
- chi ha risultati certificati non pubblica le regole; chi pubblica le regole non ha risultati certificati;
- gli studi accademici sono il compromesso migliore, ma quasi nessuno riguarda l'oro intraday;
- quindi **le nostre prove sull'oro sarebbero davvero originali**, e possiamo aspettarci un decadimento rispetto ai risultati pubblicati.

## Fonti

- [Gao e coll., Intraday Momentum (PDF)](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf) · [Alpha Architect](https://alphaarchitect.com/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- [Intraday Time Series Momentum: International Evidence](https://centaur.reading.ac.uk/95566/1/Accepted-Version.pdf) · [MPRA 97134](https://mpra.ub.uni-muenchen.de/97134/1/MPRA_paper_97134.pdf)
- [Night effect, futures cinesi su oro e argento (2025)](https://www.sciencedirect.com/science/article/abs/pii/S1044028325000110)
- [Caminschi e Heaney 2014, RePEc](https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html) · [LBMA Alchemist, manipolazione del fixing PM](https://www.lbma.org.uk/alchemist/issue-73/has-there-been-a-decade-of-london-pm-gold-fixing-manipulation) · [Hauptfleisch, Putniņš e Lucey (PDF)](https://opus.lib.uts.edu.au/bitstream/10453/41414/4/GoldILS%20JFutMkt%20Forthcoming.pdf)
- [Oro e annunci FOMC, MMU](https://e-space.mmu.ac.uk/635429) · [KFUPM](https://pure.kfupm.edu.sa/en/publications/how-do-the-gold-intra-day-returns-and-volatility-react-to-monetar/)
- [Unger Academy](https://ungeracademy.com/blog/interview-andrea-unger-world-cup-trading-champion) · [Algorithmic Advantage, Unger](https://thealgorithmicadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- [Kevin Davey, IBKR Campus](https://www.interactivebrokers.com/campus/ibkr-quant-news/algo-advantage-036-kevin-davey-part-i-its-all-about-process-in-algo-trading/)
- [Larry Williams, Kagels Trading](https://www.kagels-trading.de/?p=25277)
- [Silver Bullet [GBB], TradingView](https://jp.tradingview.com/script/teL2dDvS-Silver-Bullet-GBB/) · [Riassunto: 25.000 varianti del Silver Bullet](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)
- [Replica fuori campione di Zarattini, Aziz e Barbon (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7290621) · [GitHub della replica](https://github.com/PazSheimy/spy-intraday-momentum-oos)
- [Quantpedia, deriva notturna su GDX](https://quantpedia.com/dangers-of-relying-on-ohlc-prices-the-case-of-overnight-drift-in-gdx-etf/) · [Quantified Strategies, oro di notte](https://quantifiedstrategies.substack.com/p/a-quantitative-look-at-the-gold-overnight)
- [Trade That Swing, Initial Balance sull'oro](https://tradethatswing.com/one-trade-a-day-gold-strategy-411-in-last-year-fully-automatable/)
- [FTMO, Successful Traders Stories](https://ftmo.com/en/blog/ftmo-traders-analysis-less-is-sometimes-more/)
