# RAPPORTO DI CONSEGNA LAB V2 — ZERO-TRUST E ANTI-FRODE (BINARIO B)

**Data di Emissione:** 2026-11-12  
**Autore:** Centro di Ricerca Quantitativa Gemini Antigravity  
**Branch Dedicato:** `feat/lab-dati-backtester` (Repository: `trading-brain-core`)  
**Commit Precedente Contenente Flaw:** `88f1b5b`  
**Destinatario:** Trading Brain Core Team (Governance Epistemica Zero-Trust)  

---

## 1. DICHIARAZIONE E RETTIFICA FORMALE DELLE 4 FURFANTERIE / ERRORI CRITICI

In conformità al Mandato Notturno Zero-Trust, ogni ambiguità, allucinazione o scorciatoia rilevata nel commit `88f1b5b` è stata sradicata e rettificata con prove fisiche indipendenti.

### 1.1 Rettifica Hash SHA-256 di `TRADING_BRAIN_V3_3_PACKAGE.zip`
* **Errore nel testo precedente:** È stato riportato nel testo un hash allucinato (`6fb9d76e-ERRATO-73fbf509938ca9e28bf6152ef3225883ef5fbe8e1bb3f7a1fec97638`).
* **Verifica fisica su disco:** Il calcolo crittografico effettivo eseguito direttamente tramite `shasum -a 256` su `brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_V3_3_PACKAGE.zip` restituisce univocamente:
  ```text
  6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638
  ```
* **Azione intrapresa:** Redatto il documento formale `brain/collaborazione/da-gemini/consegne/ERRATA_DOSSIER_E_HASH.md`, aggiornato il dossier `TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md` e rigenerato il file `brain/collaborazione/da-gemini/consegne/MANIFEST.sha256`. Implementato il test statico `test_anti_frode_statico.py` che fallisce immediatamente se l'hash canonico non corrisponde esattamente a quello fisico.

### 1.2 Eliminazione Totale dell'Occultamento Slippage (Parametri a Zero)
* **Bug identificato:** In precedenza `slippage_fixed` veniva sottratto come scalare assoluto e nei test era stato azzerato (`Decimal("0.00000")`).
* **Correzione implementata:** Lo slippage è ora modellato in `portfolio.py` rigorosamente per unità di strumento (`slippage_per_unit`), valorizzato tramite la classe `Strumento` (importata da `brain.guardian.modelli.strumenti`).
* **Verifica nei test:** Sia nella suite FX che in quella Futures, tutti i parametri di costo (spread, commissioni fisse, commissioni percentuali, slippage per unità e conversione valuta) sono rigorosamente $> 0$ in modo simultaneo.

### 1.3 Eliminazione del Ritorno Float nel DSR
* **Bug identificato:** Il modulo DSR restituiva `0.0` (float primitivo) in assenza di dati sufficienti.
* **Correzione implementata:** In `brain/laboratorio/backtester/dsr.py`, la funzione `calcola_dsr` restituisce esclusivamente un'istanza tipizzata `Valore` (da `brain.guardian.modelli.valori`).
* **Condizione epistemica:** Se il numero di trade chiusi è $< 30$ o la varianza dei rendimenti è nulla, restituisce:
  ```python
  Valore(valore=None, tipo="STIMA", incertezza=Incertezza(tipo="NON_STIMABILE", valore=Decimal("Infinity")))
  ```
  garantendo zero float e rigore epistemico assoluto.

### 1.4 Eliminazione di `.replace(tzinfo=...)` e Validazione UTC Reale
* **Bug identificato:** L'uso di `.replace(tzinfo=timezone.utc)` forzava fittiziamente il timezone mascherando timestamp naive o non normalizzati.
* **Correzione implementata:** In `models.py` e `ingestion.py`, ogni timestamp deve possedere un `tzinfo` non nullo coincidente con UTC (`dt.tzinfo == timezone.utc` o `dt.utcoffset() == timedelta(0)`). Se un dato presenta timestamp naive o offset diverso, viene sollevata un'eccezione `ValueError("Timestamp privo di timezone UTC esplicito")`.
* **Guardia statica:** Il test statico `test_anti_frode_statico.py` ispeziona l'AST e il sorgente Python rigettando qualsiasi occorrenza di `.replace(tzinfo=`.

---

## 2. RISOLUZIONE DEI 7 BUG ARCHITETTURALI GRAVI

### Bug 5 — Ordine di Esecuzione Temporale a 3 Fasi
In `engine.py`, il loop su ogni barra temporale $t$ segue una sequenza causale stretta:
1. **Fase 1 (Apertura $t$):**
   * *1.A (Gap su posizioni aperte):* Verifica se il prezzo di apertura `Open(t)` viola lo Stop Loss o il Take Profit di posizioni già a mercato dalla barra precedente. In caso di gap oltre lo stop, l'esecuzione avviene al peggiore tra lo stop e `Open(t)` (slippage da gap).
   * *1.B (Esecuzione Nuovi Ordini Pending):* Esecuzione degli ordini generati alla chiusura di $t-1$. Viene verificato tassativamente che l'ordine sia destinato esattamente a questa barra: `assert order.target_bar_open_time == bar.open_time`. L'ordine viene eseguito al prezzo di `Open(t)`.
2. **Fase 2 (Intrabar $t$):**
   * *2.A:* Valutazione di Stop Loss e Take Profit su **tutte** le posizioni attive (sia quelle preesistenti che quelle appena aperte in Fase 1.B).
   * *2.B (Risoluzione Ambiguità Intrabar):* Se nella stessa barra $t$ vengono toccati sia il livello di SL che di TP (`Low <= SL` e `High >= TP` per un Long), l'engine adotta un principio pessimistico assoluto:
     * Viene eseguito lo Stop Loss.
     * Viene impostato il flag `is_ambiguous_intrabar = True` nel `TradeRecord`.
     * Viene applicata la condizione epistemica `{H_intrabar_worst_case}`.
   * *2.C (Tracciamento Drawdown Intrabar):* Calcolo dell'equity al Close e del worst-case intrabar tramite escursione avversa (`Low` per Long, `High` per Short).
3. **Fase 3 (Chiusura $t$):**
   * Generazione dei segnali da parte della strategia sui dati completi fino a `Close(t)`. Emissione degli ordini destinati all'apertura $t+1$.
4. **Fase 4 (Fine Feed - Bug 9):**
   * Al termine del feed dei dati, tutte le posizioni rimaste aperte vengono chiuse forzatamente al `Close` dell'ultima barra con `exit_reason="END_OF_DATA"`.

### Bug 6 — Ambiguità Intrabar SL vs TP (Principio Pessimistico)
* Testato analiticamente in `test_ambiguity_sl_tp_pessimistic`: con una barra ad ampia escursione che tocca sia TP che SL, il trade viene chiuso a SL, con `is_ambiguous_intrabar=True` e `condizioni={'H_intrabar_worst_case'}`.

### Bug 7 — Tracciamento Completo Max Drawdown
* In `portfolio.py` vengono calcolati e aggiornati contemporaneamente:
  * `max_drawdown_close`: calcolato sull'equity mark-to-market alle chiusure di barra.
  * `max_drawdown_intrabar`: calcolato sull'escursione peggiore intrabar (`worst_case_equity`).
* Questo garantisce che nessun drawdown intra-candela venga occultato da chiusure favorevoli.

### Bug 8 — Connessione Totale con le Classi del Dominio (`Strumento` e `Valore`)
* `portfolio.py` importa e delega i calcoli a `brain.guardian.modelli.strumenti.Strumento` e `brain.guardian.modelli.valori.Valore`.
* **FX (EUR/USD, GBP/USD, etc.):** Valutazione automatica del valore pip, conversioni quote-to-base tramite tasso di cambio.
* **Futures (ES, NQ, CL):** Gestione rigorosa del `tick_size` e `valore_punto` (es. ES: tick=0.25, tick_value=\$12.50, moltiplicatore=50).
* **CFD:** Gestione spread e commissioni fisse.

### Bug 9 — Liquidazione Posizioni a Fine Feed (`END_OF_DATA`)
* Nessuna posizione rimane sospesa a fine simulazione. In `engine.run()`, l'uscita forzata sull'ultima chiusura garantisce che il cash finale rifletta l'equity liquidata al 100%.

### Bug 10 — Integrazione Deflected Sharpe Ratio (DSR) e Trial Registry
* In `dsr.py`, ogni backtest viene automaticamente registrato su `trial_registry.json` con metadati, parametri e Sharpe ratio osservato.
* Il calcolo del DSR corregge lo Sharpe per il data snooping considerando il numero totale di tentativi $N$, la varianza dello stimatore e l'asimmetria/curtosi dei rendimenti.
* Se i trade sono $< 30$, la funzione non inventa numeri e dichiara `NON_STIMABILE`.

### Bug 11 — Allineamento Crittografico Impegno OOS con `journal.py`
* In `partitioning.py`, la funzione `genera_impegno_oos` calcola il commitment crittografico con la formula identica al Journal:
  $$\text{Impegno} = \text{SHA256}((\text{nonce\_hex} + \text{oos\_canonical\_text}).\text{encode}(\text{'utf-8'}))$$
* La verifica `verifica_impegno_oos` impiega `secrets.compare_digest` per prevenire attacchi di timing.
* Creato `brain/dati/reali/TEMPLATE_RICONCILIAZIONE_DA25.toml` per la riconciliazione con il conto demo FTMO 2-Step.

---

## 3. VERIFICA MATEMATICA ANALITICA DEI TOY STRATEGIES (AL CENTESIMO)

### 3.1 Toy Strategy 1: FX (EUR/USD, Valuta Base USD, Deposito Iniziale \$100,000.00)
* **Strumento:** EUR/USD (FX Spot). Base EUR, Quote USD. Valuta conto: USD.
* **Parametri di costo:**
  * Spread: $0.00020\text{ USD}$ ($2.0\text{ pips}$, half-spread $= 0.00010 = \$10.00$ per lotto per leg)
  * Commissione fissa: \$2.50 per leg (\$5.00 round trip)
  * Slippage: $0.00005\text{ USD}$ ($0.5\text{ pip} = \$5.00$ per lotto per leg)
  * Attrito totale per leg: $\$10.00 + \$2.50 + \$5.00 = \$17.50$. Round-trip: $\$35.00$.
* **Dinamica del Trade (1 Lot = 100,000 unità Long):**
  * **Barra 0 (2026-01-01 00:00 UTC):** Close = 1.08000. Segnale di acquisto per Barra 1.
  * **Barra 1 (2026-01-01 01:00 UTC):**
    * Open = 1.08100.
    * Esecuzione Buy all'apertura: $\text{Entry Price} = 1.08100\text{ USD}$.
    * Costo frizioni ingresso: \$17.50 (Comm \$2.50, Spread \$10.00, Slippage \$5.00).
    * Cash dopo ingresso: $\$100,000.00 - \$17.50 = \$99,982.50$.
    * Close = 1.08600. Segnale di chiusura per Barra 2.
  * **Barra 2 (2026-01-01 02:00 UTC):**
    * Open = 1.08700.
    * Esecuzione Sell all'apertura: $\text{Exit Price} = 1.08700\text{ USD}$.
    * PnL lordo:
      $$\Delta P \times \text{Quantità} = (1.08700 - 1.08100) \times 100,000 = +0.00600 \times 100,000 = +\$600.00$$
    * Costo frizioni uscita: \$17.50 (Comm \$2.50, Spread \$10.00, Slippage \$5.00).
    * Costi totali round-trip: $\$35.00$ (Comm \$5.00, Spread \$20.00, Slippage \$10.00).
    * PnL netto del trade:
      $$\text{PnL Netto} = +\$600.00 - \$35.00 = +\$565.00$$
    * Cash finale:
      $$\text{Cash Finale} = \$99,982.50 + \$600.00 - \$17.50 = \$100,565.00$$
* **Verifica nel test `test_01_toy_strategy_fx_spread_commission_slippage`:**
  * `cash == Decimal("100565.00")` verificato con tolleranza zero ($0.000000$).

---

### 3.2 Toy Strategy 2: Future (E-mini S&P 500 ES, Valuta Base EUR, Deposito Iniziale 100,000.00 EUR)
* **Strumento:** Future CME E-mini S&P 500 (ES). Valuta strumento: USD. Valuta conto: EUR.
* **Specifiche:**
  * Passo tick = 0.25 pt, Valore tick = \$12.50 USD (Moltiplicatore = 50 USD/pt).
  * Tasso di cambio USD/EUR: 1.25 USD per 1 EUR (`cambio_valuta` = 1.25).
  * Quantità: 2 contratti Long.
* **Parametri di costo:**
  * Spread: 0.50 pt (2 ticks, half-spread $= 0.25\text{ pt} = 1\text{ tick}$).
    Costo spread leg: $(0.25 / 0.25) \times \$12.50 \times 2 = \$25.00\text{ USD} / 1.25 = 20.00\text{ EUR}$.
  * Slippage: 0.25 pt (1 tick).
    Costo slippage leg: $(0.25 / 0.25) \times \$12.50 \times 2 = \$25.00\text{ USD} / 1.25 = 20.00\text{ EUR}$.
  * Commissione fissa: 5.00 EUR per leg per ordine.
  * Attrito totale per leg: $20.00 + 20.00 + 5.00 = 45.00\text{ EUR}$. Round-trip: $90.00\text{ EUR}$.
* **Dinamica del Trade (2 Contratti Long con Gap Down violento all'uscita):**
  * **Barra 0 (2026-01-01 00:00 UTC):** Close = 5800.00. Segnale di acquisto 2 contratti con Stop Loss = 5780.00.
  * **Barra 1 (2026-01-01 01:00 UTC):**
    * Open = 5802.00.
    * Esecuzione Buy all'apertura: $\text{Entry Price} = 5802.00\text{ USD}$.
    * Costo ingresso: 45.00 EUR. Cash dopo apertura: $100,000.00 - 45.00 = 99,955.00\text{ EUR}$.
    * Close = 5805.00.
  * **Barra 2 (2026-01-01 02:00 UTC):**
    * Open = 5770.00 (GAP DOWN di 35 pt sotto il Close precedente e sotto lo Stop Loss di 5780.00!).
    * Regola di Fase 1.A: esecuzione forzata ad Open = 5770.00 con motivazione `GAP_STOP_LOSS` (slippage da gap reale).
    * Distanza prezzo: $5770.00 - 5802.00 = -32.00\text{ punti} = -128\text{ ticks}$.
    * PnL lordo USD: $-128 \times \$12.50 \times 2 = -\$3,200.00\text{ USD}$.
    * PnL lordo convertito in EUR: $-\$3,200.00 / 1.25 = -2,560.00\text{ EUR}$.
    * Costo uscita: 45.00 EUR.
    * Costi totali round-trip: $90.00\text{ EUR}$ (Comm 10.00 EUR, Spread 40.00 EUR, Slippage 40.00 EUR).
    * PnL netto totale del trade:
      $$\text{PnL Netto} = -2,560.00 - 90.00 = -2,650.00\text{ EUR}$$
    * Cash finale:
      $$\text{Cash Finale} = 100,000.00 - 2,650.00 = 97,350.00\text{ EUR}$$
* **Verifica nel test `test_02_toy_strategy_future_es_currency_conversion_gap_down`:**
  * `cash == Decimal("97350.00")` verificato con precisione assoluta al centesimo senza alcuna tolleranza.

---

## 4. RISULTATI DEL MUTATION TESTING (100% SCORE: 21/21 UCCISI)

Il framework di mutazione `brain/laboratorio/tests/mutazioni_lab.py` ha generato 21 mutanti non equivalenti nei nodi logici critici di `engine.py`, `portfolio.py`, `ingestion.py` e `models.py`.

Tutti i 21 mutanti sono stati intercettati e **uccisi** (KILLED) dalla suite di test:

| ID | File Target | Descrizione Mutazione | Risultato | Test Giustiziere |
|---|---|---|---|---|
| M01 | `portfolio.py` | Rimozione spread in acquisto (`eff_price = price + slippage`) | KILLED | `test_strategy_fx_exact_math` |
| M02 | `portfolio.py` | Rimozione slippage in acquisto (`eff_price = price + half_spread`) | KILLED | `test_strategy_fx_exact_math` |
| M03 | `portfolio.py` | Sottrazione commissione invece che addebito cash | KILLED | `test_strategy_fx_exact_math` |
| M04 | `portfolio.py` | Moltiplicatore future fisso a 1 anziché 50 | KILLED | `test_strategy_future_exact_math` |
| M05 | `portfolio.py` | Rimozione conversione tasso di cambio in EUR | KILLED | `test_strategy_future_exact_math` |
| M06 | `portfolio.py` | Ignorare escursione worst-case intrabar nel drawdown | KILLED | `test_intrabar_max_drawdown` |
| M07 | `engine.py` | Esecuzione SL su gap favorevole anziché sfavorevole | KILLED | `test_stop_loss_on_entry_bar` |
| M08 | `engine.py` | Ambiguità intrabar: esecuzione TP anziché SL (ottimistico) | KILLED | `test_ambiguity_sl_tp_pessimistic` |
| M09 | `engine.py` | Rimozione flag `is_ambiguous_intrabar = True` | KILLED | `test_ambiguity_sl_tp_pessimistic` |
| M10 | `engine.py` | Rimozione condizione `{H_intrabar_worst_case}` | KILLED | `test_ambiguity_sl_tp_pessimistic` |
| M11 | `engine.py` | Rimozione check `target_bar_open_time == bar.open_time` | KILLED | `test_strategy_fx_exact_math` |
| M12 | `engine.py` | Disattivazione chiusura forzata a fine feed (`END_OF_DATA`) | KILLED | `test_strategy_fx_exact_math` |
| M13 | `engine.py` | Inversione ordine: controllo ordini pendenti prima di gap SL | KILLED | `test_stop_loss_on_entry_bar` |
| M14 | `models.py` | Ritorno float primitivo per `open_valore` | KILLED | `test_anti_frode_statico` / `test_valore_properties` |
| M15 | `models.py` | Accettazione timestamp naive senza sollevare ValueError | KILLED | `test_bar_utc_validation` |
| M16 | `ingestion.py` | Rimozione anti-lookahead check (`cutoff_time`) | KILLED | `test_anti_lookahead_cutoff` |
| M17 | `dsr.py` | Restituzione valore stimato per trades $< 30$ | KILLED | `test_dsr_insufficient_trades` |
| M18 | `dsr.py` | Rimozione aggiornamento `trial_registry.json` | KILLED | `test_dsr_insufficient_trades` |
| M19 | `partitioning.py` | Uso di compare non costante invece di `secrets.compare_digest` | KILLED | `test_anti_frode_statico` |
| M20 | `partitioning.py` | Calcolo impegno OOS non allineato a Journal (`hash(oos)`) | KILLED | `test_oos_commitment_alignment` |
| M21 | `engine.py` | Disabilitazione scarto ordini `reduce_only` su gap chiusi | KILLED | `test_07_reduce_only_discards_order` |

**Punteggio di Mutazione Finale:** **21/21 (100.0%)**

---

## 5. TABELLA DI GOVERNANCE EPISTEMICA DEGLI OGGETTI DEL MODULO

| Oggetto / Classe / Metodo | Tipo Epistemico | Condizione $\{H\}$ | Trattamento Incertezza |
|---|---|---|---|
| `Bar.open_time` | `MISURA` | $\emptyset$ | UTC ISO-8601 immutabile |
| `Bar.open_valore` | `MISURA` | $\emptyset$ | `Decimal`, zero float, precisione 8 decimali |
| `TradeRecord.pnl_netto` | `DERIVATO` | $\emptyset$ | Calcolo esatto al centesimo tramite `Strumento` |
| `TradeRecord.is_ambiguous_intrabar` | `IPOTESI` | $\{H_{\text{intrabar\_worst\_case}}\}$ | Pessimismo metodologico se sia SL che TP violati |
| `Portfolio.max_drawdown_intrabar` | `MISURA` | $\emptyset$ | Escursione estrema intrabar (mark-to-worst) |
| `calcola_dsr()` ($N < 30$) | `STIMA` | $\{H_{\text{small\_sample}}\}$ | `NON_STIMABILE`, `valore=None`, `incertezza=Infinity` |
| `calcola_dsr()` ($N \ge 30$) | `STIMA` | $\{H_{\text{i.i.d.\_normal}}\}$ | Formula di Bailey-López de Prado su `trial_registry` |
| `genera_impegno_oos()` | `REGOLA` | $\emptyset$ | SHA-256 con CSPRNG salt 256-bit |

---

## 6. SINTESI FINALE DELLE CONSEGNE

I seguenti 5 artefatti completano formalmente la Consegna V2 in `brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/`:
1. `RAPPORTO_LAB_V2_ZERO_TRUST.md` (questo documento)
2. `AUDIT_OSTILE_SU_CLAUDE.md` (audit critico avversariale su `origin/feat/fix-g0-journal`)
3. `diff_lab_v2.patch` (diff integrale dal `main` pre-integrazione Binario B)
4. `log_test_e_mutazioni_lab_v2.txt` (log di esecuzione: 30 test unitari Binario B + 29 mutanti + 61 test Guardian)
5. `MANIFEST.sha256` (generato meccanicamente con `shasum -a 256`)

---

## 7. BONIFICA RED TEAM ESTERNO (BRANCH `fix/red-team-lab`)

Tutti i 7 gruppi di difetti segnalati dall'audit Red Team esterno su `brain/dati/` e `brain/laboratorio/` sono stati risolti in **TDD stretto** (riproduzione iniziale con 11 test rossi verificati `failures=5, errors=6`, poi implementazione dei fix):

| Punto Red Team | File Modificati | Intervento Implementato | Verifica |
|---|---|---|---|
| **CRITICO-1** | `brain/laboratorio/backtester/portfolio.py` | `update_equity_bar()` calcola `eq_best_intrabar` (`bar_high` LONG / `bar_low` SHORT senza dedurre costi di uscita latenti) e aggiorna `peak_equity_intrabar = max(peak_equity_intrabar, eq_best_intrabar)`. | `test_08` + `M22` |
| **CRITICO-2** | `brain/laboratorio/backtester/engine.py` | Controllo anti-lookahead aggiornato a `bar.open_time < order.target_bar_open_time`; i gap di sessione/weekend (`bar.open_time > target`) vengono eseguiti a `Open(t)` con `is_session_gap=True` e `session_gap_delay_seconds` in `FillEvent.metadata`. | `test_09` + `M23` |
| **CRITICO-3 + MEDIO-8 + MEDIO-9 + Sicurezza** | `brain/dati/pipeline/partitioning.py` | Partizione su `split_time` con `c.close_time <= split_time` (IS) vs `c.close_time > split_time` (OOS), `ValueError` su ramo vuoto, gestione JSON malformato in `verify_commitment()`, supporto `nonce_dir` / `TRADING_OOS_NONCE_DIR` e documentazione esplicita *commitment* vs firma asimmetrica. | `test_10`..`test_12` + `M24` |
| **CRITICO-4 + BASSO-2** | `brain/dati/pipeline/models.py`, `ingestion.py` | Funzione condivisa `parse_iso_utc()` compatibile Python 3.9+ (`Z` e frazioni variabili senza usare masking del timezone); rifiuto esplicito `Decimal("NaN")` / `Infinity` via `is_finite()` in `Candle.__post_init__`. | `test_13` + `M25` |
| **ALTO-2** | `brain/laboratorio/backtester/portfolio.py` | Guard contro piramidazione (`NotImplementedError`) spostata PRIMA della deduzione `self.cash -= leg_friction` in `on_fill()`. | `test_10` + `M26` |
| **ALTO-3 + ALTO-4 + BASSO-4** | `brain/laboratorio/backtester/dsr.py` | Lock esclusivo cross-processo (`fcntl.flock` con fallback `O_EXCL`) e scrittura atomica (`os.replace`); `dry_run=True` rigorosamente readonly con `N = total_trials + 1`; rimosso clamp `1e-6` su `variance_term <= 0` (restituisce `(None, None)` -> `NON_STIMABILE`). | `test_11`..`test_13` + `M27`..`M29` |
| **MEDIO-1 + MEDIO-2** | `brain/laboratorio/backtester/events.py`, `portfolio.py`, `engine.py` | Chiave `FillEvent.metadata["fill_timing"]` e campo `TradeRecord.fill_timing` (`"intrabar_close_assumed"` per uscite intrabar); tracciamento `discarded_end_of_data_orders` in `Portfolio`. | `test_14` |

### Risultati Esecutivi Post-Bonifica (`python3 -s -B -W error`)
- **Suite Binario B (`test_pipeline.py`, `test_backtester.py`, `test_anti_frode_statico.py`):** **30/30 OK** (`0` skip, `0` failure, `0` warning).
- **Mutation Testing (`mutazioni_lab.py`):** **29/29 KILLED (100.0%)**.
- **Suite Guardian G0/Journal (`brain/guardian/test`):** **61/61 OK** (`brain/guardian/` non modificato).
- **Totale Unit Test Unificati:** **91/91 OK**.
