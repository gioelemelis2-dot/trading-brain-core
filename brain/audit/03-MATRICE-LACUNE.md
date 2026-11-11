# 3 · Matrice delle lacune

Legenda: **P** presente e adeguato al livello introduttivo · **S** presente ma superficiale · **A** assente · **V** presente ma da verificare/correggere (vedi `02-VERIFICA-AFFERMAZIONI.md`).
"Dove" indica la lezione v1 (es. 0.18 = Modulo 0, lezione 18). Priorità: ★★★ blocca altri moduli · ★★ importante · ★ approfondimento.

## Riepilogo per area

| Area | P | S | A | V | Copertura stimata | Priorità |
|---|---|---|---|---|---|---|
| A Economia e macro | 0 | 5 | 22 | 0 | ~5% | ★★★ |
| B Architettura dei mercati | 1 | 4 | 17 | 0 | ~10% | ★★ |
| C Microstruttura e order flow | 1 | 5 | 27 | 0 | ~8% | ★★ |
| D Analisi tecnica e price action | 0 | 2 | 34 | 0 | ~3% | ★★ |
| E Prezzo e flussi avanzati | 0 | 0 | 26 | 0 | 0% | ★ |
| F Finanza quantitativa e matematica | 6 | 8 | 23 | 0 | ~20% | ★★★ |
| G Fondamentale e valutazione | 0 | 1 | 34 | 0 | ~2% | ★★ |
| H Derivati e volatilità | 3 | 8 | 30 | 2 | ~15% | ★★ |
| I Strategie ed edge | 1 | 6 | 16 | 1 | ~15% | ★★ |
| L Rischio e portafoglio | 4 | 5 | 26 | 1 | ~15% | ★★★ |
| M Backtesting e ricerca | 4 | 10 | 19 | 0 | ~25% | ★★★ |
| N Programmazione e infrastruttura | 0 | 0 | 32 | 0 | 0% | ★★ |
| O Machine learning | 0 | 0 | 25 | 0 | 0% | ★ |
| P Psicologia e decisione | 9 | 10 | 11 | 3 | ~45% | ★ |
| Q Regolamentazione e fiscalità | 0 | 5 | 14 | 1 | ~10% | ★★ |
| R Processi e performance | 4 | 6 | 11 | 0 | ~25% | ★★ |
| S Epistemologia | 6 | 6 | 7 | 0 | ~35% | ★★★ (trasversale) |

La copertura è il rapporto tra voci P+S (pesate 1 e 0,4) e voci totali della mappa richiesta: è un indicatore d'ordine, non una misura precisa.

## Dettaglio

### A · Economia e macroeconomia
| Voce | Stato | Dove |
|---|---|---|
| Tassi e banche centrali come driver valutari | S | 1.1 |
| Curva dei rendimenti, inversione e recessioni | S | 1.3 |
| Spread di credito, BTP-Bund | S | 1.3 |
| Petrolio, rame, oro come barometri | S | 1.4 |
| Risk-on / risk-off | S | 1.1, 1.6 |
| Micro e macroeconomia di base, cicli, crescita, produttività | A | — |
| Inflazione/disinflazione, mercato del lavoro | A | — |
| Politica monetaria: mandati, strumenti, corridoio/floor, QE/QT, forward guidance | A → **in sviluppo** (M2 L2.1) | — |
| Fed, BCE, BoJ, BoE: differenze istituzionali | A → **parziale** (Fed, BCE in L2.1) | — |
| Tassi nominali e reali, breakeven, Fisher | A | — |
| Aspettative incorporate nei prezzi, sorprese | A → **in sviluppo** (L2.2) | — |
| Canali di trasmissione ai mercati | A → **in sviluppo** (L2.3) | — |
| Politica fiscale, debito pubblico e privato, credito | A | — |
| Liquidità globale, condizioni finanziarie, dollaro e sistema monetario internazionale | A | — |
| Bilancia dei pagamenti, flussi di capitale, commercio | A | — |
| Geopolitica ed energia, ciclo delle materie prime | A | — |
| Indicatori anticipatori / coincidenti / ritardati, calendario macro, revisioni dei dati | A | — |

### B · Architettura dei mercati
| Voce | Stato | Dove |
|---|---|---|
| OTC vs regolamentato (Forex, CFD) | S | 1.1, 1.10 |
| Cassa di compensazione (CCP) | S | 1.8 |
| Broker market maker e conflitto d'interesse | S | 1.10 |
| Regolamento T+1/T+2 | S | 1.7 |
| Tipi di ETF/ETC/ETN e controparte | P | 1.7 |
| Exchange, dealer, banche d'investimento, hedge fund, fondi pensione/sovrani/comuni, retail, arbitraggisti, HFT: incentivi e vincoli | A | — |
| Dark pool, MTF/OTF, internalizzatori sistematici, PFOF | A | — |
| Clearing, settlement, custodia (CSD), infrastrutture (Target2, CLS) | A | — |
| Regolamentazione delle sedi (MiFID II, Reg NMS) | A | — |

### C · Microstruttura e order flow
| Voce | Stato | Dove |
|---|---|---|
| Spread effettivo/realizzato, selezione avversa | P | 1.18 |
| Tipi di ordine | S | 1.12 |
| Liquidità a tre dimensioni | S | 1.18 |
| Kyle λ (solo formula) | S | 1.18 |
| Market maker, inventario | S | 1.18 |
| Limit order book, profondità, coda, cancellazioni, replenishment | A | — |
| Order flow imbalance, aggressione, market impact (legge della radice quadrata) | A | — |
| Glosten-Milgrom, Roll, modelli di LOB | A | — |
| Aste di apertura e chiusura, dealer vs order-driven, frammentazione, SOR | A | — |
| Algoritmi di esecuzione (TWAP, VWAP, IS, Almgren-Chriss), TCA, latenza, HFT | A | — |

### D · Analisi tecnica e price action
| Voce | Stato | Dove |
|---|---|---|
| Multi-timeframe | S (E5, non testato) | 1.17 |
| Gap: statistica di chiusura | S | 0.17 |
| Trend, range, swing structure, S/R, breakout, false rotture, pullback, retest | A | — |
| Compressione/espansione, candele e pattern, livelli e sessioni, stagionalità | A | — |
| Indicatori (MA, RSI, MACD, ATR, Bollinger, VWAP) con regola misurabile e test | A | — |
| Volume/Market profile, Fibonacci | A | — |
| Dow, Wyckoff, Elliott, auction market theory: rilevanza storica vs prova empirica | A | — |
| Letteratura empirica (Brock-Lakonishok-LeBaron, Lo-Mamaysky-Wang, Park-Irwin) | A | — |

### E · Prezzo e flussi avanzati
Tutte le voci (value area, POC, initial balance, single prints, excess, cumulative delta, footprint, liquidity pools, sweep, FVG, opening range, VWAP bands…) **A**. Nota: richiedono prima C (microstruttura) e N (dati tick/book), altrimenti il rischio è di imparare gergo e non mercato.

### F · Finanza quantitativa e matematica
| Voce | Stato | Dove |
|---|---|---|
| Valore atteso, varianza, deviazione standard (in R) | P | 0.10, 0.13, 0.14 |
| Legge dei grandi numeri, errore standard | P | 0.14 |
| Media geometrica, variance drag, ergodicità | P | 0.15 |
| Monte Carlo e bootstrap delle equity | P | 0.16 |
| Statistica descrittiva, code grasse, curtosi | P | 0.17 |
| Test d'ipotesi e p-value, test multipli | P | 0.18 |
| Correlazione | S | 1.6 |
| Autocorrelazione, stazionarietà (ADF/KPSS) | S | 0.18 |
| GARCH(1,1) | S (solo formula) | 0.18 |
| Cointegrazione (Engle-Granger, Johansen) | S (solo nome) | 0.18 |
| Variance ratio | S | 0.18 |
| Permutation test | S | 0.18 |
| Kelly (citato, non sviluppato) | S | 0.15 |
| Rischio di rovina | S | 0.13 |
| Algebra, calcolo, algebra lineare | A | — |
| Distribuzioni, inferenza, intervalli di confidenza (formale) | A | — |
| Regressione lineare/multipla/logistica, PCA, clustering | A | — |
| AR/MA/ARMA/ARIMA, VAR, ECM, HMM | A | — |
| Inferenza bayesiana | A | — |
| EVT, copule, processi stocastici, martingale, moto browniano | A | — |
| Teoria dell'informazione | A | — |

### G · Fondamentale e valutazione
| Voce | Stato | Dove |
|---|---|---|
| Valore = flussi scontati (esempio di duration azionaria) | S | 1.2 |
| Bilancio, conto economico, rendiconto, margini, FCF, ROE/ROIC/ROA, multipli, DCF, WACC, CAPM, DDM, qualità degli utili, revisioni, guidance, buyback, M&A, banche, cicliche | A | — |

### H · Derivati e volatilità
| Voce | Stato | Dove |
|---|---|---|
| Futures: margini, mark-to-market, roll | P | 1.8 |
| Contango/backwardation | P | 1.4 |
| Payoff call, greche base | P | 1.9 |
| Perpetual e funding rate | S | 1.10 |
| CFD | S | 1.10 |
| VIX, struttura a termine, variance risk premium | S | 1.5 |
| Volmageddon | V | 1.5 |
| Regola IV alta/bassa | V | 1.9 |
| Forward, swap, basis, hedging, arbitraggio, put-call parity | A | — |
| Volatilità implicita/realizzata/forward/locale/stocastica, smile, skew, superficie | A | — |
| Delta hedging, gamma scalping, vanna, charm | A | — |
| Fixed income: duration, convessità, curva, swap di tasso | S (una riga) | 1.3 |
| Mercati specialistici (energia, metalli, agricoli, tassi) | S | 1.4 |

### I · Strategie ed edge
| Voce | Stato | Dove |
|---|---|---|
| Fattori che sopravvivono (trend, momentum, value, quality, low-vol, carry) | P (con 1 errore) | 0.3 |
| Le 5 domande su ogni edge | S | 0.3 |
| Fonti dell'edge per il retail | S | 0.9 |
| Tassonomia con i 12 attributi per famiglia | A | — |
| Pairs/stat arb, dispersion, relative value, calendar, intermarket, stagionali, event-driven, market making | A | — |

### L · Rischio e portafoglio
| Voce | Stato | Dove |
|---|---|---|
| Rischio fisso per trade, size da stop | P | 0.8, 1.1 |
| Drawdown e recupero | P | 0.13 |
| Correlazioni nelle crisi | P | 1.6 |
| Kill switch | P | 0.8 |
| Kelly / frazione di Kelly | S | 0.15 |
| Rischio di rovina | V | 0.13 |
| Leva e margine | S | 1.8, 1.10 |
| Controparte | S | 1.11 |
| Diversificazione | S | 1.6 |
| VaR, ES, stress test, scenari, risk parity, ottimizzazione, frontiera efficiente, beta, tracking error, attribution, asset allocation, ribilanciamento, rischio di liquidità/modello/operativo/sistemico | A | — |

### M · Backtesting e ricerca
| Voce | Stato | Dove |
|---|---|---|
| Pre-registrazione, IS/OOS, test multipli, revisione avversariale, criteri di abbandono | P | 0.4 |
| p-hacking, HARKing | P | 0.3 |
| Monte Carlo/bootstrap | P | 0.16 |
| Replication crisis | P | 0.3 |
| DSR, PBO (solo nome) | S | 0.18 |
| Costi realistici | S | 1.13 |
| Survivorship, look-ahead, selection bias, data leakage | A | — |
| Walk-forward, rolling/expanding, CPCV | A | — |
| Robustezza dei parametri, regime analysis | S | 0.9 |
| Paper/forward testing, monitoraggio live, decay | S | 0.2, 0.9 |
| White's Reality Check, SPA di Hansen, Romano-Wolf | A | — |

### N · Programmazione e infrastruttura
Tutte le voci **A** (Python, SQL, pandas, statsmodels, API, WebSocket, database, ETL, OHLCV/tick/book, validazione dati, Git, logging, test, architetture, monitoraggio). Primo seme: `strumenti/` (2 script).

### O · Machine learning
Tutte le voci **A**.

### P · Psicologia e decisione
| Voce | Stato | Dove |
|---|---|---|
| Prospect theory, loss aversion | V (λ attribuito al 1979) | 0.19 |
| Sistema 1 / Sistema 2 | P | 0.19 |
| Catalogo dei bias (11) con contromisure | P | 0.20 |
| Disposition effect con esempio | P | 0.20 |
| Tilt e protocollo | P | 0.21 |
| Sonno | V | 0.22 |
| Pratica deliberata, recupero attivo, spaziatura | P | 0.24 |
| Resulting (Duke) | P | 0.7 |
| Neurobiologia del rischio | V | 0.19 |
| Stress, arousal, carico cognitivo, attenzione, memoria di lavoro | S | 0.19, 0.22 |
| Psicologia dei mercati: gregge, panico, bolle, contagio | S | 0.20 |
| Metacognizione, calibrazione, abitudini | A | — |
| Evidenze vs divulgazione nelle neuroscienze | A | — |

### Q · Regolamentazione, fiscalità, etica
| Voce | Stato | Dove |
|---|---|---|
| Redditi di capitale vs diversi, minus, 26/12,5% | S | 1.13 |
| Amministrato vs dichiarativo, RT/RW, IVAFE, bollo | S | 1.13 |
| Cripto 33% | V | 1.13 |
| Leva retail e protezione saldo negativo UE | S | 1.10 |
| MiFID II, ESMA, CONSOB, best execution, market abuse (MAR), insider, front running, manipolazione, conflitti, MiCAR | A | — |

### R · Processi
| Voce | Stato | Dove |
|---|---|---|
| Journal, voto di aderenza, review settimanale | P | 0.7, 0.8 |
| Kill switch, limiti | P | 0.8, 0.21 |
| Checklist | S | 0.8 |
| Diario emotivo | P | 0.19 |
| Trading plan, playbook, pre-market, review mensile, screenshot, error tracking, decision log, procedure di emergenza | S/A | — |

### S · Epistemologia
| Voce | Stato | Dove |
|---|---|---|
| Metodo scientifico, falsificabilità | P | 0.4 |
| Replication crisis | P | 0.3 |
| Base rate | P | 0.1, 0.17 |
| Processo vs esito | P | 0.7 |
| Pareidolia, scetticismo | P | 0.5 |
| Correlazione/causalità | S | 1.6 |
| Inferenza bayesiana | A | — |
| Teoria della decisione, razionalità limitata | S | 0.19 |
| Qualità delle fonti, conflitti d'interesse | S | 0.3 |
| Causal inference (event study, diff-in-diff, IV) | A | — |
| Forecasting e calibrazione (Brier score) | A | — |
| Pensiero controfattuale, analisi avversariale strutturata | S | 0.4 |
