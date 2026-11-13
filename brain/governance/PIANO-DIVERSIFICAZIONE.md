# Piano di diversificazione su più mercati (proposta, 13/11/2026)

**Stato:** proposta di Claude, chiesta dall'utente («deve essere centrale la diversificazione»). Va confermata con DA-27 e DA-28. La versione per la lettura è nel documento «Trading Brain — Progetto generale», sezione «Diversificazione su più mercati».

**Premessa.** La diversificazione moltiplica un vantaggio statistico solo se il vantaggio c'è già. Ogni mercato in più è anche un'occasione in più di trovare qualcosa per caso. Prima vengono i dati e il conteggio delle prove, poi le strategie. Si va un mercato alla volta, con la procedura dell'oro.

## Cosa cambia rispetto all'oro (verificato nel codice il 13/11/2026)
- **Scala e prezzi dell'oro.** `dati/pipeline/dukascopy.py` conosce solo XAUUSD: `SCALA = {"XAUUSD": 3}`, e `PREZZO_MIN`/`PREZZO_MAX` valgono 1.000–10.000. Ogni strumento ha i suoi valori, da ricavare e proteggere con controlli.
- **Regola dei buchi.** `classifica_buco` (fine settimana solo se contiene un sabato intero) va bene per oro e cambi. Indici ed energia hanno pause ogni giorno e festività: servono orari per ogni strumento.
- **Un solo strumento.** `laboratorio/backtester` (engine e portfolio) segue un solo `strumento`. Per il portafoglio serve un'estensione, prima nei test.
- **Prove contate per strumento.** Il registro delle prove è separato per strumento (`dati/operativo/trial_registry_xauusd.json`), ma il conteggio deve essere unico (DA-28).

## Regole proposte
1. **Stesso calendario** di sviluppo e di verifica per tutti i mercati. Mercati legati, per esempio dal dollaro, rendono visibile il periodo chiuso degli altri.
2. **Un mercato alla volta:** controlli, buchi, metadati, sigillo.
3. **Mercati dichiarati prima.** Un'ipotesi scrive in anticipo su quali mercati vale e con quali parametri, e deve reggere senza ritocchi. Scegliere dopo i mercati dove funziona è autoinganno.
4. **Ogni coppia ipotesi–mercato è una prova.** Il totale di tutte le prove entra nel DSR.
5. **Correlazioni misurate** solo sul periodo di sviluppo, anche nei periodi di crisi.
6. **P-06 resta 1 posizione:** per ora la diversificazione è in sequenza. Più posizioni insieme solo con DA-23, dopo l'incubazione.

## Mercati candidati e ordine
Per ognuno vanno verificati il codice su Dukascopy, l'anno di inizio e la disponibilità su FTMO e sui broker demo. Ordine proposto:
1. EURUSD;
2. S&P 500;
3. XAGUSD, come prova di robustezza delle idee sull'oro, non come diversificazione;
4. GBPUSD e USDJPY;
5. DAX e petrolio WTI o Brent;
6. BTCUSD solo alla fine, se ha senso.

## Tempi (stime)
- **Oro:** 3 anni sono circa 1.100 richieste, più di 12 ore sul Mac.
- **Tutti i mercati:** 10 mercati per 15 anni sono circa 55.000 richieste, cioè almeno 23 ore di sole pause e realisticamente settimane di notti. Un mercato a settimana basta.

## Oltre ai prezzi
- seconda fonte per ogni mercato (storico MT5 dei broker demo);
- costi reali per mercato e per ora (spread, commissione, swap);
- calendario storico delle notizie (fonte da trovare e verificare);
- orari, festività e ora legale;
- definizioni scritte di Fibonacci e order block, prima di guardare i dati;
- effetti noti nella letteratura come fonte di ipotesi. Gli effetti pubblicati tendono a ridursi dopo la pubblicazione (McLean e Pontiff, 2016);
- journal dei conti demo.

## Fasi
- **D0:** oro, con DA-26 decisa e sigillo definitivo.
- **D1:** scaricatore per più strumenti (TDD, Python 3.13 e 3.9, una richiesta di prova per strumento).
- **D2:** download un mercato alla volta, con lo stesso calendario.
- **D3:** seconda fonte e costi reali.
- **D4:** registro unico e backtester su più strumenti, **solo dopo la prima ipotesi testata sull'oro** (contromisura 8: niente nuova infrastruttura prima). Scaricare altri mercati (D1–D2) è raccolta dati del Gate 2 e può procedere; il portafoglio no.
- **D5:** ipotesi con i mercati dichiarati prima, replica indipendente di Gemini, criteri DA-20.
- **D6:** portafoglio entro l'1,5% al giorno, durante l'incubazione.
