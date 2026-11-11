# 4 · Nuova architettura didattica

Versione 1.0 · 11/11/2026

## 4.1 Decisione: conservare la numerazione 0–10, cambiare la forma

Ho valutato tre opzioni:

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| A. Tenere 0–10 lineari come nel v1 | Continuità totale | La matematica (Area F) arriverebbe al Modulo 10, cioè dopo i moduli che la usano (4, 6, 7, 8) | Scartata |
| B. Riorganizzare per discipline (A–Z) | Coerenza accademica | Rompe la progressione "dalle fondamenta alla pratica" e i cancelli del v1 | Scartata |
| **C. Tenere 0–9 come spina dorsale + Modulo 10 come insieme di tracce parallele con cancelli di prerequisito** | Conserva numerazione, ordine e cancelli del v1; la matematica entra quando serve | Richiede un grafo di prerequisiti esplicito | **Scelta** |

Il Modulo 10 non è più "formazione di supporto" generica: è **formazione specialistica trasversale**, divisa in tracce. Alcune tracce sono **obbligatorie prima di un certo modulo** (es. 10.1 prima del 6; 10.2 prima dell'8).

Ogni lezione è un file Markdown autonomo (`moduli/mXX-nome/L<modulo>.<n>-titolo.md`), con versione e stato. Il manuale HTML può essere rigenerato dai file quando serve una versione da leggere.

## 4.2 Struttura

Legenda profondità: **I** introduttiva · **II** intermedia · **III** avanzata/professionale. Cancello: livello di padronanza minimo (L1–L5).

### Modulo 0 · Fondamenta mentali e statistiche (v1 conservato, 24 lezioni)
- 0.1 Onestà sull'obiettivo (L1–4) · 0.2 Modello mentale (L5–8) · 0.3 Ancora statistica (L9–18) · 0.4 Fattore umano (L19–24)
- **Nuove lezioni previste**: 0.25 Livelli di evidenza e qualità delle fonti (S) · 0.26 Pensiero bayesiano operativo (S, F) · 0.27 Calibrazione delle proprie previsioni (T)
- Correzioni: vedi `audit/02-VERIFICA-AFFERMAZIONI.md`
- Cancello: L2 → **L3** (si aggiunge un esercizio su dati reali)

### Modulo 1 · Come funzionano i mercati (v1 conservato, 18 lezioni)
- 1.1 Mercati e motori · 1.2 Strumenti · 1.3 Cripto · 1.4 Orizzonti · 1.5 Microstruttura essenziale
- **Nuova unità 1.6 · Chi partecipa al mercato** (Area B): exchange, broker, dealer, market maker, banche, hedge fund, fondi pensione e sovrani, fondi comuni ed ETF, retail, HFT, arbitraggisti; incentivi e vincoli · **1.7 Infrastrutture**: sedi (RM, MTF, OTF, SI), dark pool, clearing, settlement, custodia
- Cancello: L3

### Modulo 2 · Macro, politica monetaria e flussi (nuovo · **in sviluppo**: unità 2.1 scritta, in verifica)
| Unità | Lezioni | Profondità |
|---|---|---|
| 2.1 Politica monetaria e mercati | **L2.1** Banche centrali · **L2.2** Aspettative e sorprese · **L2.3** Trasmissione ai mercati · **L2.4** Tassi reali e inflazione attesa · **L2.5** Bilancio: QE, QT, riserve · **L2.6** Fed, BCE, BoJ, BoE — tutte `in_verifica` (11/11/2026) | I–II |
| 2.2 Il ciclo economico | Crescita, produttività, output gap · Inflazione e disinflazione · Mercato del lavoro · Indicatori anticipatori/coincidenti/ritardati · Come si costruiscono e si rivedono i dati (vintages) | I–II |
| 2.3 Dati macro come eventi | Calendario macro, consensus e sorprese · Reazioni condizionate al regime · Event study su dati macro (lab) | II |
| 2.4 Credito, debito e politica fiscale | Debito pubblico e privato, ciclo del credito, spread · Politica fiscale e interazione con la monetaria | II |
| 2.5 Sistema monetario internazionale | Dollaro, eurodollaro, swap lines · Bilancia dei pagamenti e flussi di capitale · Ciclo finanziario globale | II–III |
| 2.6 Condizioni finanziarie e liquidità (plumbing, Area U) | Riserve, repo, collaterale · Indici di condizioni finanziarie · Casi: repo 2019, marzo 2020, UK LDI 2022 | II–III |
| 2.7 Energia, materie prime e geopolitica | Shock di offerta e domanda di petrolio · Ciclo delle commodity · Rischio geopolitico misurato | II |
- Cancello: **L4** — dato un evento macro reale, costruire il quadro (attese, sorpresa, catena di trasmissione con livelli di evidenza, spiegazioni alternative) e dire cosa lo confuterebbe.

### Modulo 3 · Analisi tecnica e struttura del mercato
- 3.1 Struttura: trend, range, swing, massimi/minimi definiti in modo algoritmico
- 3.2 Livelli: supporti/resistenze, livelli di sessione, giornalieri, settimanali; gap
- 3.3 Eventi di prezzo: breakout, falsa rottura, pullback, retest, compressione/espansione
- 3.4 Indicatori come trasformazioni dei dati (MA, RSI, MACD, ATR, Bollinger, VWAP): definizione, regola misurabile, test
- 3.5 Candele e pattern: cosa dice (poco) l'evidenza
- 3.6 Scuole storiche: Dow, Wyckoff, Elliott, auction theory, Fibonacci — rilevanza storica vs prova empirica
- 3.7 Letteratura empirica sull'analisi tecnica (Brock-Lakonishok-LeBaron 1992; Sullivan-Timmermann-White 1999; Lo-Mamaysky-Wang 2000; Park-Irwin 2007)
- Cancello: L4 — tradurre un concetto tecnico in regola codificabile e progettarne il test

### Modulo 4 · Lettura avanzata del prezzo e order flow
- 4.1 Microstruttura II: limit order book, coda, cancellazioni, replenishment, impatto, modelli (Kyle, Glosten-Milgrom, Roll)
- 4.2 Esecuzione: algoritmi (TWAP, VWAP, IS, Almgren-Chriss), TCA, latenza, HFT, frammentazione
- 4.3 Auction market theory, market/volume profile (value area, POC, initial balance)
- 4.4 Order flow: delta, footprint, imbalance — **dati osservabili vs interpretazioni**; dipendenza da piattaforma e dati
- 4.5 Concetti delle community (liquidity pools, sweep, FVG): definizioni, ciò che è testabile, ciò che non lo è
- Cancello: L4

### Modulo 5 · Analisi fondamentale, dati e valutazione
- 5.1 I tre prospetti e i loro legami · 5.2 Redditività e qualità degli utili · 5.3 Struttura finanziaria · 5.4 Valutazione: DCF, multipli, DDM, WACC · 5.5 Aspettative: consensus, revisioni, guidance, earnings surprise · 5.6 Corporate actions, buyback, diluizione, M&A · 5.7 Settori speciali: banche, assicurazioni, cicliche
- Cancello: L4

### Modulo 6 · Sistema operativo, rischio e portafoglio
- 6.1 Sizing: fixed fractional, fixed risk, volatilità-target, Kelly e frazione di Kelly · 6.2 Rischio di rovina con edge incerto · 6.3 Leva, margine, controparte, liquidità · 6.4 VaR, Expected Shortfall, stress test, scenari · 6.5 Portafoglio: diversificazione, correlazioni instabili, risk parity, ottimizzazione e i suoi limiti · 6.6 Fattori, beta, tracking error, attribution · 6.7 Trading plan, limiti, kill switch, procedure di emergenza (Area R)
- Prerequisito: traccia 10.1
- Cancello: L4

### Modulo 7 · Strategie, famiglie di edge e playbook
- 7.1 Tassonomia e scheda standard a 12 attributi
- 7.2 Premi persistenti: trend/momentum, value, quality, low-vol, carry
- 7.3 Relative value: pairs, stat arb, calendar, intermarket, dispersion
- 7.4 Intraday: breakout, mean reversion, opening range, stagionalità intraday
- 7.5 Volatilità: vendita di premio, coperture, eventi
- 7.6 Event-driven, market making, arbitraggio (perché il retail di solito non può)
- 7.7 Discrezionale, sistematico, ibrido
- Cancello: L4 — revisione avversariale scritta di una famiglia

### Modulo 8 · Validazione, ricerca quantitativa, programmazione e automazione
- 8.1 Protocollo di ricerca (pre-registrazione, dati, bias) · 8.2 Bias dei dati: survivorship, look-ahead, point-in-time, leakage · 8.3 Validazione: walk-forward, CPCV, PBO, DSR, Reality Check/SPA · 8.4 Costi e esecuzione realistica · 8.5 Robustezza e regimi · 8.6 Paper e forward testing, monitoraggio, decay · 8.7 Infrastruttura (traccia N): Python, dati, test, logging, architettura
- Prerequisito: tracce 10.1–10.2
- Cancello: **L5** — una ricerca pre-registrata completa, anche con esito negativo

### Modulo 9 · Operatività reale, intermediari, esecuzione, fiscalità e controllo
- 9.1 Scelta dell'intermediario e tutele (MiFID II, best execution, separazione patrimoniale, fondi di garanzia) · 9.2 Regole UE/IT: ESMA, CONSOB, MAR, MiCAR · 9.3 Fiscalità italiana (con data e fonti ufficiali) · 9.4 Prop firm: modello economico e regole · 9.5 Dal paper al reale: cancello con rischi e autorizzazioni esplicite · 9.6 Controllo e revisione periodica
- Cancello: L5 + autorizzazione scritta

### Modulo 10 · Formazione specialistica trasversale (tracce)
| Traccia | Contenuti | Prerequisito di |
|---|---|---|
| **10.1 Matematica, probabilità e statistica** | Algebra, funzioni, calcolo, algebra lineare; probabilità, distribuzioni, inferenza, IC, test, regressione, bayes, bootstrap | 6, 8 |
| **10.2 Econometria delle serie storiche** | Stazionarietà, AR/MA/ARIMA, VAR, cointegrazione, ECM, ARCH/GARCH, HMM e regime switching | 8 |
| 10.3 Probabilità avanzata e rischio di coda | Processi stocastici, martingale, moto browniano, EVT, copule, teoria dell'informazione | 10.5, 6.4 |
| 10.4 Machine learning per la finanza | Supervisionato/non supervisionato, validazione su serie temporali, drift, explainability, limiti | — |
| 10.5 Derivati e volatilità avanzati | Pricing, greche di ordine superiore, superficie di volatilità, VRP, delta hedging | 7.5 |
| 10.6 Fixed income avanzato (Area X) | Curve, duration/convessità, swap, credito, inflation-linked | 2.4 |
| 10.7 Asset pricing e storia finanziaria (W, V) | Efficienza, SDF, fattori, limiti all'arbitraggio; storia delle crisi | 7 |
| 10.8 Psicologia, neuroscienze e mercati (P) | Evidenze vs divulgazione; bolle, gregge, contagio | — |
| 10.9 Inferenza causale e forecasting (T) | Event study, identificazione, calibrazione | 2.3, 8 |
| 10.10 Sistemi complessi e stabilità finanziaria (Y, U) | Leva, prociclicità, cascate, reti | 6 |

## 4.3 Corrispondenza vecchio → nuovo

| v1 | Nuova posizione | Azione |
|---|---|---|
| 0.1–0.17, 0.19–0.24 | Invariati | Conservati; correzioni puntuali con nota (A7, A9, A12–A14) |
| 0.18 Test e serie storiche | 0.18 (panoramica) + 10.1, 10.2 (sviluppo) | Conservata come mappa; i contenuti si sviluppano nelle tracce |
| 1.1–1.4 | Invariati, con rimandi a 2.x | 1.3 → collegata a L2.3 e 10.6 |
| 1.5 Volatilità come asset | 1.5 + 10.5 | Correzione A15 |
| 1.6 Correlazioni | 1.6 + 6.5 | — |
| 1.7–1.12 | Invariati | 1.9 → nota C2 |
| 1.13 Costi e fiscalità | 1.13 (mappa) + 9.3 (con fonti e data) | Correzioni A16–A17 |
| 1.14–1.17 | Invariati | 1.17 → nota C3 |
| 1.18 Microstruttura | 1.18 (essenziale) + 4.1–4.2 | — |
| "Modulo 10 · Formazione di supporto (magistrale e libri)" | Modulo 10 tracce | Ridefinito: da contenitore a tracce con prerequisiti |

## 4.4 Ordine didattico consigliato

```
0 → 1 → [10.1 in parallelo] → 2 → 3 → [10.2 in parallelo] → 4 → 5 → 6 → 7 → 8 → 9
           10.8 (psicologia) e 10.7 (storia) in parallelo continuo, senza cancello
```
