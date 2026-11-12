# Proposte di correzione per la V3.1 (da eseguire da Antigravity in una V3.2, dopo l'approvazione dell'utente)

Riferimento: `CLAUDE_FINAL_REVIEW_V3_1.md` (12/11/2026). **Nessuna proposta è stata applicata.** La V3.1 resta congelata.
Ogni proposta riporta: problema, motivazione con evidenza, modifica richiesta, test di accettazione, dipendenze.

---

## Q-01 · Intervallo di Kelly etichettato "IC 95%" (N-01) · priorità ALTA
- **Problema:** nella risposta V3.1, §4, ultima riga, l'intervallo "Stima da 300 trade reali (IC 95%)", E[R] ∈ [+0,068; +0,232] → f* ∈ [0,21%; 0,71%], è in realtà ±1 errore standard (≈ 68%). Ne deriva la raccomandazione "0,20–0,25% (limite inferiore IC)".
- **Evidenza** (`output/v31_c_kelly.txt`): con N = 300, WR = 0,40, R:R 2, costo 0,05: SE[WR] = √(0,24/300) = 0,0283 e SE[E[R]] = 3 × 0,0283 = 0,0849.
  - ±1 SE: [+0,065; +0,235] (f* 0,20%–0,73%).
  - **IC 95%: [−0,016; +0,316]**: l'edge non è distinguibile da zero.
- **Modifica:**
  - etichettare l'intervallo come "±1 errore standard (≈ 68%)", oppure sostituirlo con l'IC 95%;
  - riscrivere la conclusione: "con 300 trade non si può affermare un edge positivo al 95%; il dimensionamento basato sull'edge stimato non è giustificato dal solo campione".
- **Test di accettazione:** una funzione che calcola l'IC a un livello dato e un test che, per N = 300, restituisce un limite inferiore < 0 al 95%.
- **Dipendenze:** nessuna.

## Q-02 · Suite di test (N-02) · priorità ALTA
- **Problema:** la suite V3.1 uccide 5 mutanti su 12 (`output/v31_d_mutazioni.txt`).
- **Modifica, test da aggiungere:**
  1. **Regressione del bug dei giorni minimi:** target raggiunto prima del giorno 4 → nessun trade a rischio successivo; esito "pass" con equity uguale al target (come `test_min_days_freezes_risk_after_target` della V2, assente nella V3.1).
  2. **Ordine delle barriere durante il trade:** generatore controllato (come il test A4 di Claude) in cui un MAE profondo viola insieme max loss e daily loss → esito atteso `max_loss`; e un caso in cui viola solo il daily loss → `daily_loss`.
  3. **MAE attraverso il motore con R:R ≠ 2:** scenario WR 0,50 / R:R 1 con `use_brownian_mae=True`, confronto della frequenza di violazione durante il trade con il calcolo esatto (`F(d)`, formula della revisione §3.2).
  4. **Target della fase 2:** concordanza della probabilità della sola fase 2 con il calcolo esatto.
  5. **Concordanza con l'esatto su più configurazioni** (gruppo A completo): swing 1% con 60 giorni, intraday 1% senza e con MAE, Markov stazionario; tolleranza 4 errori standard.
- **Test di accettazione:** rieseguire `v31_d_mutazioni.py`; tutti i mutanti non equivalenti (V02–V12) devono essere uccisi. V01 è quasi equivalente: va documentato.
- **Dipendenze:** Q-04 (usa le formule esatte del MAE).

## Q-03 · Varianza con slippage (N-03) · priorità BASSA
- **Problema:** risposta §4, riga "Con Slippage Pareto": Var 2,19 e f* 0,3472%.
- **Evidenza:** con tetto 3R, E[S] = 0,0602R e Var[S] = 0,0222, quindi Var[R] = 2,2609 e f* = 0,3363% (`v31_c_kelly.py`, integrazione numerica di P(S > s) sui momenti troncati).
- **Modifica:** correggere i valori, o mostrare il metodo se diverso.
- **Dipendenze:** nessuna.

## Q-04 · Valori di riferimento del MAE (N-05) · priorità BASSA
- **Problema:** −2,41 / +2,49 chiamati "benchmark analitico/esatto di Claude", mentre erano simulati.
- **Modifica:** citare i valori **esatti** ora disponibili (intraday 1%: −2,42 / +2,58 / −0,12 punti; swing 1%: −1,53) con il metodo (`v31_a_esatto_e_mae.py`).
- **Dipendenze:** nessuna.

## Q-05 · Attribuzione (N-04) · priorità MEDIA
- **Modifica:**
  - intestazione del motore: "Sviluppo e test: Gemini Antigravity. Proposte di correzione: Claude (CLAUDE_FINAL_REVIEW_V3.md). Revisione indipendente della V3.1: Claude (CLAUDE_FINAL_REVIEW_V3_1.md, esito: non validata)";
  - nel README sostituire "Revisione Indipendente: Claude Code" con lo stato effettivo.
- **Dipendenze:** nessuna.

## Q-06 · Runner V1 d'archivio (N-06) · priorità BASSA
- **Modifica:** lasciare intatto il file storico e aggiungere un `LEGGIMI` con l'istruzione per eseguirlo (collegamento `prop_risk_engine.py` → `prop_risk_engine_v1.py`) e l'hash del JSON atteso.
- **Dipendenze:** nessuna.

## Q-07 · Schede STR (N-07) · priorità MEDIA
- **Modifica:** nuove versioni, separate da quelle d'archivio, di STR-001 e STR-002 con:
  - STR-001: ingresso con resting stop su H₂₀, riempimento all'apertura in caso di gap, sessione coerente, attribuzione Dennis/Eckhardt;
  - STR-002: etichetta `[SIMULATO]` sul campione da 94.518 aperture e z con il test score;
  - per entrambe, una **dichiarazione su quali dati sono già stati osservati** prima della registrazione dei periodi fuori campione.
- **Dipendenze:** Q-09 per la coerenza con il rulebook.

## Q-08 · Validazione dei parametri del MAE (N-08) · priorità BASSA
- **Modifica:** nel costruttore, se `use_brownian_mae`: controllare che la deriva risolta riproduca il win rate entro 1e−9 e che `2·|μ|·max(1, R:R) < 700`, altrimenti `ValueError`. Allineare la soglia μ ≈ 0 alla tolleranza del risolutore.
- **Test:** scenari estremi (R:R 50; WR 0,99) sollevano un errore chiaro invece di un overflow.
- **Dipendenze:** nessuna.

## Q-09 · Rulebook (N-09) · priorità MEDIA, prima del Trading Guardian
- **Modifica:** separare in due file:
  1. **regole della prop firm:** ogni regola con fonte ufficiale, data e tipo di conto (base del daily loss, orario di reset, max loss statico o trailing, target, limite di tempo, formato 1-Step);
  2. **regole personali:** buffer, controlli pre-trade, condizioni proibite.

  Risolvere le incoerenze: GATE_03 (R:R ≥ 1,5) contro STR-002 (0,70); rischio massimo 0,75% contro l'euristica di Kelly, da dichiarare. Sostituire i percorsi esterni al Brain.
- **Dipendenze:** definizione condivisa del Trading Guardian (decisione dell'utente).

---

## Dipendenze e ordine consigliato
```
Q-01  (indipendente, priorità alta)
Q-04 ──► Q-02  (i test del MAE usano le formule esatte)
Q-03, Q-05, Q-06, Q-08  (indipendenti, minori)
Decisione utente sul Guardian ──► Q-09 ──► Q-07
```
Il pacchetto si può considerare **validato** quando Q-01, Q-02 e Q-05 sono chiusi e la revisione di Claude li conferma.
