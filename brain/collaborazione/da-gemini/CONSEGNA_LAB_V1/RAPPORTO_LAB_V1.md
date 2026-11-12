# RAPPORTO DI CONSEGNA — BINARIO B: DATI REALI & BACKTESTER EVENT-DRIVEN (V1)

**Data:** 12 Novembre 2026  
**Autore:** Gemini Antigravity (Quantitative Research Lab)  
**Destinatario:** Gioele Melis / Claude Code  
**Repository:** `https://github.com/gioelemelis2-dot/trading-brain-core.git`  
**Branch:** `feat/lab-dati-backtester`  
**Perimetro di Intervento Esclusivo:** `brain/collaborazione/da-gemini/`, `brain/dati/`, `brain/laboratorio/`  
**Vincoli Rispettati:** Zero live trading, V3.3 baseline congelata, `brain/guardian/` non modificato (competenza Claude), governance epistemica rigorosa (nessun float, tipi invarianti, condizioni `{H}`).

---

## 1. SINTESI DELL'INTERVENTO E OBIETTIVI RAGGIUNTI

In conformità con il mandato operativo ricevuto per il **Binario B (Fasi 4 e 5 della Roadmap)**, sono state realizzate e verificate al 100% tutte le componenti richieste:

1. **Sincronizzazione e Archiviazione Baseline Gemini:**  
   Archiviato in `brain/collaborazione/da-gemini/consegne/` il pacchetto storico `TRADING_BRAIN_V3_3_PACKAGE.zip` (SHA-256: `6fb9d76e...7638`), il manuale `TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md` e il dossier `TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md` con il rispettivo `MANIFEST.sha256`.
2. **Pipeline Ingestione & Validazione Dati Reali (`brain/dati/pipeline/`):**  
   - Modello dati `Candle` ad alta precisione monetaria (`Decimal`, zero float), classificato epistemologicamente come `MISURA` con condizione `{H_feed_integro}`.
   - Validazione della stretta monotonia cronologica UTC ($t_i \ge t_{i-1}$) e distinzione esplicita tra `open_time` e `close_time` per impedire strutturalmente il look-ahead bias.
   - Rilevamento automatico di buchi anomali (`AnomalyGapError`) e blocco dati futuri rispetto al cutoff (`LookAheadDataError`).
   - Partizionatore fisico `IN-SAMPLE` e `OUT-OF-SAMPLE` con protocollo crittografico `Sealed OOS Commitment`: generazione di un nonce CSPRNG a 256 bit e calcolo di $\text{SHA256}(\text{OOS\_bytes} \parallel \text{Nonce\_bytes})$ in `commitment.json` per garantire la non-contaminazione e il rilevamento immediato di manomissioni.
3. **Motore di Backtest Strictly Event-Driven (`brain/laboratorio/backtester/`):**  
   - **Regola Esecutiva Ferrea:** Un segnale generato al `Close(t)` viene accodato ed eseguito ESCLUSIVAMENTE all'`Open(t+1)` della barra successiva. Divieto assoluto di same-bar execution.
   - **Gestione Realistica del Gap:** Se la barra $t+1$ apre oltre il livello dello Stop Loss (gap down su long o gap up su short), l'ordine viene eseguito all'`Open(t+1)` assorbendo l'intero slippage da gap negativo, e NON all'illusorio prezzo nominale dello stop.
   - **Accounting Istituzionale Esplicito:** Commissioni fisse, metà spread per leg e slippage contabilizzati separatamente come `DERIVATO | H_esec` in `Decimal`.
   - **Deflated Sharpe Ratio (DSR) & Trial Registry:** Implementazione dell'algoritmo di Bailey & López de Prado (2014) collegato al contatore globale persistente in `brain/laboratorio/trial_registry.json`. Ogni simulazione incrementa il trial counter $N$, provocando la deflazione progressiva del DSR a parità di Sharpe ratio stimato per neutralizzare il data snooping.
4. **Verifica Sperimentale al Centesimo (2 Strategie Giocattolo):**  
   - *Strategia 1 (Reversal deterministico):* PnL lordo \$33.00, costi round-trip \$5.00, PnL netto +\$28.00 $\to$ Cash finale \$100,028.00 esatto al centesimo.
   - *Strategia 2 (Gap Down oltre Stop Loss):* Posizione Long da 1.10250 con SL a 1.09500. Apertura barra successiva a 1.09200 (gap di 30 pips oltre lo stop). Esecuzione confermata a 1.09200. PnL lordo -\$105.00, costi \$8.00, PnL netto -\$113.00 $\to$ Cash finale \$99,887.00 esatto al centesimo.
5. **Auto-Revisione Avversariale Anti-Lookahead:**  
   Iniezione di segnali malevoli anticipati o incoerenti bloccata con sollevamento immediato di `LookAheadViolationError`.

---

## 2. STRUTTURA DEI FILE CREATI

```
brain/
├── collaborazione/
│   └── da-gemini/
│       ├── consegne/
│       │   ├── TRADING_BRAIN_V3_3_PACKAGE.zip          [Baseline V3.3 congelata]
│       │   ├── TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md
│       │   ├── TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md
│       │   └── MANIFEST.sha256
│       └── CONSEGNA_LAB_V1/
│           ├── RAPPORTO_LAB_V1.md                      [Questo documento]
│           ├── diff_lab_v1.patch                       [Diff completo vs main]
│           ├── log_test_lab.txt                        [Verbale esecuzione 12/12 test OK]
│           └── MANIFEST.sha256                         [Manifest integrità consegna]
├── dati/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── models.py       [Candle dataclass, Decimal puro, EpistemicType.MISURA]
│   │   ├── ingestion.py    [DataIngestionPipeline, controlli temporali e gap]
│   │   └── partitioning.py [DatasetPartitioner, nonce 256-bit, commitment.json]
│   └── tests/
│       └── test_pipeline.py [8 test unitari: float reject, inverted time, gaps, OOS seal]
└── laboratorio/
    ├── backtester/
    │   ├── __init__.py
    │   ├── events.py       [SignalEvent, OrderEvent, FillEvent, Position, TradeRecord]
    │   ├── portfolio.py    [Portfolio, accounting cash/equity rigoroso in Decimal]
    │   ├── engine.py       [EventDrivenBacktester, bar-by-bar, gap slippage, anti-lookahead]
    │   └── dsr.py          [DSRCalculator, Bailey & Lopez de Prado 2014, trial counter]
    ├── tests/
    │   └── test_backtester.py [4 test unitari: 2 toy strategy al centesimo, stress-test, DSR]
    └── trial_registry.json    [Registro globale persistente delle prove N]
```

---

## 3. RISULTATI DEI TEST E VERIFICHE RIPRODUCIBILI

Tutti i test sono stati eseguiti con Python standard 3.9+ (zero dipendenze esterne):

```
=== PIPELINE DATI REALI (brain/dati/tests/test_pipeline.py) ===
test_01_valid_candle_creation ................................ OK
test_02_reject_float_strictly ................................ OK (Type safety Decimal)
test_03_reject_inverted_bar_timestamps ....................... OK (Rifiuto open >= close)
test_04_reject_corrupted_prices .............................. OK (Rifiuto Low > High / fuori range)
test_05_reject_non_monotonic_sequence ........................ OK (Rifiuto overlap / inversioni)
test_06_reject_lookahead_future_candles ....................... OK (Rifiuto dati oltre cutoff)
test_07_reject_anomaly_data_gaps ............................. OK (Rilevamento buchi anomali)
test_08_partitioning_and_sealed_commitment ................... OK (Sigillo crittografico OOS)

=== BACKTESTER EVENT-DRIVEN (brain/laboratorio/tests/test_backtester.py) ===
test_01_toy_strategy_1_reversal_exact_to_the_cent ............ OK ($100,028.00 esatto)
test_02_toy_strategy_2_gap_down_stop_loss_exact_to_the_cent .. OK ($99,887.00 slippage gap reale)
test_03_adversarial_lookahead_detection ...................... OK (Blocco look-ahead bias)
test_04_trial_registry_and_deflated_sharpe_ratio ............. OK (DSR deflates as N grows)

ESITO COMPLESSIVO: 12/12 TEST SUPERATI (100% PASS)
```

---

## 4. GOVERNANCE EPISTEMICA RISPETTATA

- **Prezzi e Volumi:** Classificati come `MISURA`, condition `{H_feed_integro}`.
- **Metriche e PnL:** Classificati come `DERIVATO DETERMINISTICO`, condition `{H_esec}`.
- **DSR e Sharpe:** Classificati come `STIMA` con parametri espliciti di non-normalità ($T$, $N$, $\gamma_3$, $\gamma_4$).
- **Regole di Esecuzione e Sigilli:** Classificati come `REGOLA`, condition `{H_oos_sigillato}` e `{H_trial_counter_integro}`.
- **Assenza di Float:** Nessun tipo `float` è ammesso nei bilanci di cassa, prezzi di fill, margini o PnL monetario.

---

## 5. STATO DELLA CONSEGNA

Il lavoro è interamente committato sul branch `feat/lab-dati-backtester` e pronto per essere sincronizzato con il repository remoto `trading-brain-core`.
Nessun file di `brain/guardian/` è stato toccato, garantendo l'assenza totale di conflitti Git con le consegne parallele di Claude.
