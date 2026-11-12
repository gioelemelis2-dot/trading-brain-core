# Proposte di correzione per la V3.2 (eventuale V3.3, da eseguire da Antigravity dopo l'approvazione dell'utente)

Riferimento: [`CLAUDE_FINAL_REVIEW_V3_2.md`](CLAUDE_FINAL_REVIEW_V3_2.md), 12/11/2026. **Nessuna proposta è stata applicata**; la V3.2 resta congelata.
Nessuna proposta è bloccante: l'esito VALIDATA CON RISERVE non dipende da esse. Si possono applicare tutte insieme in una V3.3 minore, oppure l'utente può accettare la V3.2 così com'è e registrare le riserve.

I test di accettazione marcati ✔ sono già scritti ed eseguiti in `verifiche/test_proposti_claude_v32.py`; i risultati sono in `output/test_proposti_claude_v32.txt`. Passano sul motore V3.2 (il test Wilson passa sul motore con Wilson corretto) e falliscono sui mutanti indicati.

---

## S-01 · Benchmark della fase 2 etichettato come analitico · Media
- **Dove:** `test_prop_risk_v3_2.py`, docstring riga 332 («~0.860 contro ~0.776») e assert riga 349 (`0.8596`); risposta, riga 65 («coincida con il benchmark analitico … ≈85,96% contro ≈77,60%»).
- **Evidenza:** calcolo esatto (`v32_a_esatto.py` (A)): fase 1 isolata **0,7800**, fase 2 isolata **0,8572**, prodotto 0,6686 (pari al valore del Gruppo A). I valori 0,8596 e 0,776 sono stime Monte Carlo.
- **Modifica:**
  - sostituire 0,8596 con 0,8572 e 0,776 con 0,7800;
  - etichettarli «esatti (programmazione dinamica sul reticolo, `c1_esatto_challenge.fase`)»;
  - usare una tolleranza in errori standard invece di ±0,025;
  - correggere la frase della risposta.
- **Test di accettazione ✔:** `test_fase2_esatta_e_prodotto_due_fasi` (fase 2 contro 0,8572 entro 4 SE; sfida intera attraverso `run_full_challenge_v3_2` contro 0,6686 entro 4 SE).

## S-02 · Corrispondenza test → mutanti dichiarata errata · Bassa
- **Dove:**
  - test riga 298 («Uccisione mutanti V03 e V10») e riga 328 («Uccisione mutante V07»);
  - risposta righe 59–65;
  - checkpoint righe 28–31.
- **Evidenza:**
  - Nel test R:R 1 (rischio 10%, pavimento al 5%) la violazione scatta per MAE ≤ −0,5R. Troncare il MAE a 0,5R (V10) lascia la probabilità **identica** (1/6), quindi il test non può rilevare V10.
  - Con 40 semi alternativi V10 non è mai rilevato né da questo test né dal Gruppo A (`v32_b` (3)): l'effetto esatto di V10 è +2,52 SE contro una soglia di 4.
  - V10 è ucciso solo da `test_q02_barrier_priority_during_trade_mae`, che usa un MAE fissato a −0,999.
  - Il test della fase 2 chiama `simulate_phase_v3_2` e non passa da `run_full_challenge_v3_2`: V07 è ucciso solo dal Gruppo A.
- **Modifica:**
  - correggere la tabella di corrispondenza nei documenti;
  - aggiungere un test del MAE profondo attraverso il motore;
  - far passare il test della fase 2 da `run_full_challenge_v3_2`.
- **Test di accettazione ✔:**
  - `test_mae_profondo_attraverso_motore_rr1`: pavimento al 7,5%, quindi violazione per MAE ≤ −0,75R; P esatta = 0,5·F(0,75) = 1/14. Uccide V10 (P = 0) e V03;
  - `test_fase2_esatta_e_prodotto_due_fasi`: uccide V07.

## S-03 · LEGGIMI del runner V1 · Bassa
- **Dove:** `archivio_storico/LEGGIMI_V1.md`, riga 12 (import citato) e riga 29 (modalità B).
- **Evidenza:** la modalità B termina con `AttributeError: module 'run_comprehensive_simulations_v1' has no attribute 'main'`. La riga 13 del runner importa `PropSimulationScenario, run_full_challenge_experiment, wilson_confidence_interval`.
- **Modifica:**
  - nella modalità B sostituire `r.main()` con `r.run_suite()`;
  - citare l'import esatto;
  - indicare che il JSON prodotto si chiama `prop_simulations_raw.json` e viene scritto nella cartella corrente, quindi va eseguito su una copia e non nella cartella d'archivio.
- **Test di accettazione (eseguito da Claude):** le due modalità, su copie separate, producono un JSON con SHA-256 `a6781b7e…`. La modalità B corretta lo produce (`output/v32_e_v1_leggimi.txt`).

## S-04 · Quantili di Wilson e dell'intervallo di Kelly · Bassa (difetto latente)
- **Dove:**
  - `prop_risk_engine_v3_2.py:46`: `z = 1.96 if |confidence − 0,95| < 1e-4 else 2.5758`;
  - righe 84–97: banda ±0,01 attorno a 0,6827 con z = 1.
- **Evidenza (`v32_c`):** `wilson_confidence_interval(50, 100, 0.90)` restituisce [0,3753; 0,6247], cioè l'IC al 99%; il corretto è [0,4188; 0,5812]. Kelly al livello 0,69 usa z = 1,000 invece di 1,0152. Il pacchetto usa solo 0,95, 0,6827 e 0,99, quindi nessuna uscita è errata. Il difetto di Wilson esiste dalla V3.
- **Modifica:**
  - `z = statistics.NormalDist().inv_cdf(0.5 + confidence/2)` in entrambe le funzioni;
  - eliminare l'approssimazione di Hastings;
  - `ValueError` se il livello non è in (0, 1).
- **Test di accettazione ✔:** `test_wilson_valori_noti` (k = 50, n = 100, livelli 0,90, 0,95 e 0,99). Fallisce sulla V3.2 (lo dimostra) e passa con la correzione. Per Kelly: livello 0,69 contro z = 1,0152.

## S-05 · Guardia del MAE più restrittiva del necessario · Bassa (suggerimento)
- **Dove:** `prop_risk_engine_v3_2.py:121–154, 174–177, 260–264`.
- **Evidenza:**
  - per μ > 0, `exp(-2μ·R:R)` va in underflow a 0 senza errore. WR 0,99 / R:R 500 (μ ≈ 2,30) è quindi calcolabile ma viene rifiutato; lo stesso vale per WR 0,40 / R:R 0,001 (μ molto negativo, `exp(2μ)` va in underflow);
  - il messaggio parla di «overflow» anche quando il limite è il tetto ±15 dell'intervallo di bisezione, e stampa «WR=1.0000» per 0,9999995.
  - **La guardia simmetrica viene dalla mia proposta Q-08**: la correzione riguarda un mio eccesso di prudenza.
- **Modifica, opzionale:**
  - guardia sul solo esponente positivo: 2μ < 700 se μ > 0; 2|μ|·R:R < 700 se μ < 0;
  - `math.expm1` per i termini 1 − e^x;
  - messaggi che distinguono «fuori dall'intervallo di ricerca» da «overflow»;
  - WR stampato con 8 cifre.
  - In alternativa, lasciare la guardia e documentare il dominio accettato nei documenti, dove oggi si legge «per qualsiasi (WR, R:R)».
- **Test di accettazione:** WR 0,99 / R:R 500 accettato con |P_win(μ) − WR| < 1e-12 e campionatore entro 4 SE da F(d) su 8 quantili; nessun `OverflowError` sulla griglia di `v32_c`.

## S-06 · Input non validati fuori dal MAE · Bassa (rischio potenziale)
- **Dove:** costruttore, righe 225–228; slippage, riga 344; `simulate_phase_v3_2`, righe 370–371.
- **Evidenza (`v32_c`, input):**
  - R:R `nan` → `timeout`; costo `nan` → `timeout`; R:R `inf` → `pass`;
  - rischio −1% accettato, con esiti incoerenti;
  - alpha 0 → `ZeroDivisionError`;
  - `max_days` 3 < `min_days` 4 → `('pass', 4, 0.1)`, cioè un superamento oltre il limite di tempo.
- **Modifica:** `ValueError` per:
  - valori non finiti;
  - `cost_r` < 0;
  - `slippage_tail_alpha` ≤ 0;
  - `slippage_scale` ≤ 0 o `slippage_cap_r` ≤ 0;
  - `risk_pct` ∉ (0, 1);
  - `trades_per_day` < 1;
  - `max_days` < `min_days`.
- **Test di accettazione:** ognuno dei casi sopra solleva `ValueError`; la suite esistente resta 14/14.

## S-07 · Copertura dei test su slippage, Wilson e soglia μ≈0 · Bassa (suggerimento)
- **Evidenza (`v32_d`):**
  - sopravvivono V19 (esponente −α invece di −1/α), V20 (tetto ignorato) e V21 (Wilson con z = 1);
  - V22 (soglia μ≈0 del campionatore a 0,1) sopravvive anch'essa: l'effetto è piccolo per μ = 0,0975, ma rompe l'allineamento richiesto da Q-08;
  - `test_c03_slippage_execution` controlla solo che lo slippage riduca il superamento.
- **Modifica:**
  - un test deterministico dello slippage;
  - un test dei momenti contro la forma chiusa;
  - il test di Wilson (S-04);
  - un test del campionatore con μ = 2·10⁻⁷ contro F(d) con deriva.
- **Test di accettazione ✔:**
  - `test_slippage_deterministico`: uccide V19 e V20;
  - `test_momenti_slippage_forma_chiusa`: E[S] = 0,060169;
  - `test_wilson_valori_noti`: uccide V21.
  - Rieseguendo `v32_d_mutazioni.py` con questi test aggiunti, devono restare vivi solo V01 e, al più, V22.

## S-08 · Inesattezze documentali · Minima
Correggere:
- **Dimensione dello ZIP:** 47.977 byte, non 41.696 (continuità, riga 16).
- **Gruppo A:** «tutti \|z\| ≤ 1,46» → con il seme 42 il massimo è 1,67, nella configurazione Markov (checkpoint, riga 33).
- **«Forma chiusa»:** le variazioni del MAE sono un calcolo esatto numerico che usa la F(d) in forma chiusa (risposta, riga 87; checkpoint, riga 39).
- **V01:** è «la fase 2 riusa i generatori della fase 1», quasi equivalente; non «tolleranza bisezione» (risposta, riga 69).
- **Commit:** la revisione V3.1 è nel commit `9ff4514`; `8544a15` è la revisione V3 (risposta, riga 7).
- **«per qualsiasi (WR, R:R)» `[DIMOSTRATO]`:** limitare al dominio accettato dalla guardia (risposta, riga 155).
- **«Regolamento ufficiale FTMO»:** allineare allo stato V-SEC dichiarato nel JSON, oppure verificarlo sulla fonte ufficiale con data (risposta, riga 160).
- **Test di accettazione:** ricerca testuale dei termini corretti; nessuna affermazione numerica senza una fonte riproducibile.

## S-09 · Ipotesi del modello non dichiarate · Bassa (limite metodologico)
- **Ipotesi da dichiarare** nel README e nel JSON (`epistemological_status`):
  1. nessuna posizione aperta a mezzanotte: il pavimento giornaliero è calcolato sul capitale chiuso;
  2. trade sequenziali, mai sovrapposti;
  3. stato della catena di Markov ricampionato dalla distribuzione stazionaria all'inizio di ogni fase;
  4. dopo il target, operatività a rischio zero fino ai giorni minimi.
- Non sono errori: sono scelte del modello, che il Trading Guardian dovrà confrontare con le regole reali (Q-09).
- **Test di accettazione:** presenza delle quattro ipotesi nei metadati.

---

## Ordine consigliato
```
S-01, S-02, S-07 (test)  ──►  rieseguire v32_d_mutazioni.py
S-03, S-08, S-09 (documenti)
S-04, S-06 (validazione)  ──►  la suite esistente deve restare 14/14
S-05 (opzionale)
```
Dopo la V3.3, la mia verifica si limiterebbe a: suite, mutazioni, `test_proposti_claude_v32.py`, LEGGIMI e ricerca testuale. Non servirebbe una nuova revisione completa.
