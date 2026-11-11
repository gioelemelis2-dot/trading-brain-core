# 03 · Dal trading discrezionale alla ricerca quantitativa sistematica: competenze mancanti

Audit AUDIT-ARCH-20261111.

**Legenda copertura nel Brain:** ✅ presente e verificata · 🟡 presente ma parziale o non verificata · ❌ assente.
**Livello obiettivo** (STANDARD §5): L3 applicazione · L4 analisi critica · L5 progettazione di test.
La colonna "Chi" indica chi potrebbe svilupparla senza duplicare: C = Claude, G = Gemini, U = decisione o dati dell'utente.

## 1. Che cosa cambia nel passaggio
| Discrezionale | Sistematico |
|---|---|
| Il giudizio sceglie il trade | Una regola scritta sceglie il trade; il giudizio sceglie e mette in discussione le regole |
| Il journal registra i trade | Un registro delle ipotesi registra **tutte** le prove, anche quelle fallite |
| Il risultato si valuta sul conto | Il risultato si valuta fuori campione, dopo i costi, contando quante varianti sono state provate |
| Il rischio è una regola personale | Il rischio è un modello con parametri incerti, testato e monitorato |
| Gli errori si correggono con l'esperienza | Gli errori si prevengono con dati puliti, codice testato e revisione indipendente |

## 2. Mappa delle competenze

### A. Fondamenti matematici e statistici
| Competenza | Copertura | Dove oggi | Obiettivo | Chi |
|---|---|---|---|---|
| Aspettativa, varianza, R, legge dei grandi numeri | ✅ | v1 0.10–0.14 (numeri verificati) | L3 | — |
| Ergodicità, crescita geometrica, Kelly | 🟡 | v1 0.15; seconda revisione §5.D | L4 | C |
| Monte Carlo e bootstrap | 🟡 | v1 0.16; strumenti di revisione | L4 | C |
| Inferenza: intervalli, test, potenza, errore standard dello Sharpe | 🟡 | v1 0.14, 0.18 (compressa) | L4 | C (traccia 10.1) |
| Regressione lineare e logistica, multicollinearità | ❌ | — | L3 | C |
| Serie storiche: stazionarietà, autocorrelazione, ARMA, GARCH, cointegrazione | ❌ (solo nominate in 0.18) | — | L3/L4 | C (traccia 10.2) |
| Processi stocastici, moto browniano, tempi di primo passaggio | 🟡 | seconda revisione (MAE, Kelly) | L3 | C |
| Test multipli: Bonferroni, BH, Reality Check, SPA, DSR, PBO | 🟡 (solo nominati) | v1 0.18 | L5 | C |
| Inferenza bayesiana e incertezza sui parametri | ❌ | — | L3 | C |

### B. Metodo di ricerca
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Pre-registrazione, criteri di abbandono | 🟡 | v1 0.4 (principi), nessun registro operativo | L5 | C |
| Separazione esplorazione / validazione | 🟡 | v1 0.4 | L5 | C |
| Validazione temporale: walk-forward, finestre mobili ed espanse, CPCV, purging ed embargo | ❌ | solo citata in architettura | L5 | C (Modulo 8.3) |
| Inferenza causale, event study | 🟡 | L2.2 (identificazione ad alta frequenza) | L4 | C |
| Previsione probabilistica e calibrazione | ❌ | — | L3 | C/G |
| Revisione avversariale e test di mutazione | ✅ | procedure della seconda revisione | L4 | C+G |

### C. Ingegneria dei dati
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Provenienza, licenze, hash, metadati | 🟡 | `dati/README.md` (regole, nessun dato) | L3 | C |
| Dati point-in-time, revisioni macro (vintage) | ❌ | citato in mappa | L4 | C |
| Bias: sopravvivenza, look-ahead, selezione | 🟡 | v1 0.3 (principi) | L5 | C |
| Contratti futures continui, roll, rettifiche | ❌ | — | L3 | G (dati) / C (lezione) |
| Sessioni, fusi orari, ora legale, festività | 🟡 | richiesta dati 0.17; checklist FTMO C3 | L3 | C |
| Validazione dei dati (OHLC coerente, buchi, outlier) | 🟡 | `riproduci_017.py` (controllo minimo) | L3 | C |
| Dati tick, order book, M1 | ❌ | — | L3 | G |

### D. Backtesting
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Motore a eventi vs vettoriale; confronto tra i due | ❌ | — | L4 | G (codice) + C (revisione) |
| Modello di esecuzione: riempimenti, gap oltre lo stop, tocco intraday, slippage, costi, finanziamento | 🟡 | contestazione C-15; v1 1.12–1.13 | L5 | G + C |
| Dimensionamento e regole di rischio nel backtest | 🟡 | motore V2 (solo challenge) | L4 | G |
| Metriche e loro errore: Sharpe, drawdown, R medio, errore standard | 🟡 | v1 0.13–0.14 | L4 | C |
| Controllo dei bias nel codice (test contro look-ahead) | ❌ | — | L5 | C |

### E. Sviluppo di strategie
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Fonti dell'edge e ragione economica | ✅ | v1 0.3, 0.9 | L4 | — |
| Tassonomia delle famiglie (trend, carry, mean reversion…) | 🟡 | v1 0.3 (fattori); Modulo 7 pianificato | L4 | C |
| Tradurre un concetto discrezionale in regola testabile | ❌ | Modulo 3 pianificato | L5 | C |
| Registro delle ipotesi e ciclo di vita di una strategia | ❌ | — | L5 | C (proposta in documento 05) |

### F. Gestione del rischio
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Rischio per trade, strisce, drawdown, rovina | ✅ | v1 0.13; strumenti esatti verificati | L4 | — |
| Regole di prop firm (daily loss, max loss, target, tempi) | 🟡 | motore V2 (verificato sul modello); regole FTMO non verificate | L4 | G (rulebook) + U (fonti ufficiali) |
| MAE, slippage, code pesanti | 🟡 | seconda revisione §5.B–C | L4 | C+G |
| Incertezza sull'edge nel dimensionamento | 🟡 | seconda revisione §5.D | L4 | C |
| Rischio di portafoglio: correlazioni, VaR/ES, stress | ❌ | Modulo 6 pianificato | L4 | C |
| Rischio di modello e monitoraggio del decadimento dell'edge | ❌ | — | L4 | C |

### G. Automazione e ingegneria del software
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Python riproducibile, solo libreria standard o dipendenze bloccate | ✅ | tutti gli strumenti | L3 | — |
| Test automatici, test di mutazione | 🟡 | strumenti; seconda revisione | L4 | C |
| Esecutore unico dei test, integrazione continua | ❌ | — | L3 | C |
| API dei broker, gestione degli ordini, paper trading | ❌ | — | L3 | G (+ autorizzazione U) |
| Registrazione, monitoraggio, allarmi | ❌ | — | L3 | G |
| Sicurezza: credenziali, separazione tra ambiente di ricerca e reale | ❌ | STANDARD §6 (principio) | L4 | C+G |

### H. Trading Guardian (funzione da definire, vedi documento 05)
| Competenza | Copertura | Dove | Obiettivo | Chi |
|---|---|---|---|---|
| Regole personali non negoziabili, kill switch, tilt | ✅ (come regole umane) | v1 0.8, 0.21 | — | — |
| Rulebook versionato con fonti | ❌ (quello di Gemini non è stato consegnato) | — | L4 | G + C |
| Calcolo dello stato di rischio in tempo reale | 🟡 | motore V2 + calcolo esatto | L4 | G + C |
| Journal strutturato e voto di aderenza | 🟡 | v1 0.7 (concetto) | L3 | C |

## 3. Lettura d'insieme
1. **Il Brain sa ragionare sul rischio meglio di quanto sappia fare ricerca.** Le aree D (backtesting) e C (dati) sono quasi vuote, e sono quelle che separano un'idea da un risultato verificabile.
2. **Il collo di bottiglia non è teorico ma pratico:** nessun dato reale, nessun registro delle ipotesi, nessun modello di esecuzione verificato.
3. **La statistica del Modulo 0 basta per iniziare** il Modulo 8 (protocollo e validazione), ma non per le serie storiche e la validazione temporale avanzata: la traccia 10.1–10.2 va riaperta in parallelo.
4. **Il Guardian è la componente con il valore più immediato** per un operatore discrezionale: protegge il processo già oggi e non richiede backtest. Dipende però da un rulebook verificato e da una definizione condivisa.
