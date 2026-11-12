# Revisione indipendente del pacchetto V3.2 di Gemini Antigravity

**Revisore:** Claude Code · **Data:** 12/11/2026 · **Oggetto:** `TRADING_BRAIN_V3_2_PACKAGE.zip` (SHA-256 `989dd288…3d18`) e `CONTINUITA_V3_2_PASSAGGIO_A_CLAUDE.md`
**Riferimenti:** `R-CLAUDE-20261112-03-V31/CLAUDE_FINAL_REVIEW_V3_1.md` e `PROPOSTE-CORREZIONE-V3_1.md` (Q-01…Q-09)
**Perimetro:** Q-01, Q-02, Q-03, Q-04, Q-05, Q-06, Q-08 e passata avversariale. Q-07 e Q-09 sono fuori perimetro: non verificati, solo dipendenze segnalate (§6).
**Il pacchetto non è stato modificato.** Tutte le esecuzioni sono avvenute su copie verificate per hash, in cartelle separate.

Documenti collegati:
- [`CLAUDE_CORRECTION_PROPOSALS_V3_2.md`](CLAUDE_CORRECTION_PROPOSALS_V3_2.md): correzioni proposte, con i test di accettazione;
- [`REGISTRO_VERIFICHE_V3_2.md`](REGISTRO_VERIFICHE_V3_2.md): le verifiche effettivamente eseguite;
- [`CONFRONTO_AFFERMAZIONI_V3_2.md`](CONFRONTO_AFFERMAZIONI_V3_2.md): le affermazioni di Gemini a confronto con i miei risultati.

---

## 1. Esito

> **VALIDATA CON RISERVE.**

Il criterio fissato nella revisione V3.1 era: «il pacchetto si può considerare validato quando Q-01, Q-02 e Q-05 sono chiusi e la revisione di Claude li conferma». È soddisfatto.
- **Q-01 (intervallo dell'edge):** chiuso; ricalcolato in modo indipendente.
- **Q-02 (suite di test):** chiuso; la suite uccide 11/11 dei mutanti non equivalenti V02–V12.
- **Q-05 (attribuzione):** chiuso.
- **Q-03, Q-04 e Q-08:** chiusi.
- **Q-06:** chiuso solo in parte; una delle due procedure documentate non funziona (S-03).
- **Motore:** nessun errore numerico. È stato confrontato con il calcolo esatto anche in configurazioni nuove: MAE con R:R ≠ 2 sull'intera sfida a due fasi, sempre |z| < 1,7.

**Le riserve (S-01…S-09) non invalidano alcun risultato numerico del pacchetto.** Riguardano:
- etichette epistemiche;
- la corrispondenza dichiarata tra test e mutanti;
- una procedura del LEGGIMI;
- difetti latenti in funzioni non usate a livelli diversi da 0,95;
- copertura dei test sullo slippage;
- validazione degli input;
- ipotesi del modello non dichiarate.

La più rilevante è **S-01**: un valore simulato (0,8596) viene presentato come «benchmark analitico» nel test e nella risposta. È la stessa categoria di problema che Q-04 doveva eliminare. Il valore esatto è 0,8572.

**Cosa NON significa questo esito:** non valida alcuna strategia, né l'esistenza di un edge.
- Tutti i risultati restano `[SIMULATO]` sotto l'ipotesi `[EDGE SUPPOSTO]` di +0,15R netto per trade.
- Q-01 ora dimostra correttamente che con 300 trade un edge di questa entità non è distinguibile da zero al 95%.
- Nessun dimensionamento della posizione è giustificato dal solo campione. Senza un edge dimostrato su dati reali, la scelta razionale resta **non operare**.

---

## 2. Integrità (eseguita prima di ogni altra verifica)

| Controllo | Esito |
|---|---|
| SHA-256 dello ZIP | `989dd288e04cb5601af0012442707b833054001ba48cdc6392bcdd5423643d18`: **coincide** con il dichiarato |
| Dimensione dello ZIP | **47.977 byte**, non 41.696 come dichiarato (continuità, riga 16). L'hash coincide, quindi il file è quello certificato: l'errore riguarda solo la dimensione dichiarata (S-08) |
| Struttura dell'archivio | `testzip` OK; nessun percorso assoluto o con `..` |
| Manifest (15 file) | `sha256sum -c`: **15/15 OK**. Tabella del documento di continuità identica al manifest |
| File non dichiarati | **nessuno** |
| Archivio storico (6 file) | identico byte per byte all'archivio della V3.1 (STR-001, STR-002, motore V1, JSON V1, rulebook, runner V1) |
| Versioni precedenti | Le copie ricevute in conversazione sono intatte: ZIP V3 `6c64a3a4…` (manifest V3 tutto OK), ZIP V3.1 `99e8f0bd…` (manifest V3.1 tutto OK), V2 (5/5 file conformi a `MANIFEST_SHA256.txt`). **Le cartelle `consegne/`, `consegne-v3/` e `consegne-v3.1/` sul Mac non sono verificabili da questo ambiente** |

Nessun fallimento di integrità. Uscita: `output/hash_v32_ricevuti.txt`.

---

## 3. Verifica delle correzioni

### Q-01 · Intervallo dell'edge: **RISOLTO**
- **Ricalcolo indipendente** (`v32_c`, quantile da `statistics.NormalDist`). Con N = 300, WR 0,40, R:R 2 e costo 0,05:
  - E[R] = 0,150, SE = 0,084853, pari a √(Var[R]/N) con Var[R] = 2,16;
  - **±1 SE:** [+0,0651; +0,2349], quindi f* in [0,201%; 0,726%];
  - **IC 95%:** [−0,0163; +0,3163];
  - al limite inferiore del 95% f* è negativo (−0,050%).
- **Riscontro con il motore:** `calculate_kelly_confidence_interval` restituisce esattamente questi valori.
- **Conclusioni:** sono corrette e senza dimensionamento ingiustificato.
  - Risposta §2.1: «nessuna size operativa o dimensionamento frazionario di Kelly è giustificato dal solo campione»;
  - JSON: `statistical_conclusion`.
  - Nel pacchetto non restano raccomandazioni di rischio basate sul campione.
- **Test:** `test_q01_…` uccide i mutanti V13 (z = 1 al 95%, cioè N-01 reintrodotto), V14 (SE senza il fattore R:R+1) e V15 (costo ignorato).
- **Difetto latente (S-04).** Per livelli non standard il quantile è approssimato:
  - qualsiasi livello entro ±0,01 da 0,6827 riceve z = 1 (0,69 → 1,000 invece di 1,015);
  - il livello non è validato in (0, 1).
  - Nessun risultato del pacchetto ne è toccato.

### Q-02 · Suite di test: **RISOLTO (criterio di accettazione soddisfatto), con riserve S-01, S-02, S-07**
- **Esecuzione:** 14/14 test OK (Python 3.13.18). Il runner riproduce il JSON identico byte per byte (`5260c4f0…`).
- **Mutazioni.** I 12 mutanti della V3.1 sono stati adattati ai nomi della V3.2 e affiancati da 10 nuovi (`v32_d`). Ogni mutante è verificato come effettivamente caricato.
  - **V02–V12: 11/11 uccisi** (in V3.1 erano 5/12).
  - V01 sopravvive: è quasi equivalente, come già documentato.
  - Totale 17/22. Sopravvivono V19 e V20 (slippage), V21 (Wilson) e V22 (soglia μ≈0 nel campionatore): vedi S-07.
- **Controlli richiesti:**

| Controllo | Esito | Test che lo garantisce davvero |
|---|---|---|
| Regressione `min_days` | OK | `test_q02_min_days_regression…` uccide V12 e V17 (giorni minimi ignorati) |
| Precedenza delle barriere durante il trade | OK | `test_q02_barrier_priority_during_trade_mae` uccide V04 e V08, e **anche V10** |
| MAE con R:R ≠ 2 attraverso il motore | OK per V03 | `test_q02_mae_through_engine_rr_diff_2` uccide V03, ma **non può uccidere V10 per costruzione** (S-02) |
| Target della fase 2 | OK | V07 è ucciso **solo** dal test del Gruppo A. `test_q02_phase2_target_concordance` chiama `simulate_phase_v3_2` e non passa da `run_full_challenge_v3_2`, dove vive il target della fase 2 (S-02) |
| Concordanza Gruppo A | OK | i 5 valori di riferimento coincidono con il mio calcolo esatto (0,9108 / 0,7034 / 0,6686 / 0,4406 / 0,3884): il test non è circolare |

- **I test non passano artificialmente.** Sul motore originale, con 40 semi alternativi (`v32_b`):
  - 0 falsi allarmi nel Gruppo A (|z| massimo 2,86 contro la soglia 4);
  - 0 nel test R:R 1;
  - 0 nel test della fase 2.
- **Riserva.** Il test della fase 2 usa come «benchmark analitico» 0,8596, che è un valore **simulato**: l'esatto è 0,8572 (S-01). Il test passa per la tolleranza ±0,025, non perché il riferimento sia esatto.

### Q-03 · Varianza con slippage: **RISOLTO**
- **Metodo.** Momenti troncati del Lomax in **forma chiusa**, un metodo diverso dall'integrazione numerica della V3.1:
  - E[min(S, c)] = λ/(α−1)·[1 − (1 + c/λ)^(1−α)];
  - E[min(S, c)²] = 2λ²·[(T^(2−α) − 1)/(2−α) − (T^(1−α) − 1)/(1−α)], con T = 1 + c/λ = 61.
- **Valori.** E[S] = 0,060169; Var[S] = 0,022249; E[R netto] = 0,113899; Var[R] = 2,260861; **f\* = 0,3363%**. Coincidono alla quarta cifra con i dichiarati.
- **Controllo Monte Carlo** della formula del motore (2·10⁶ estrazioni): E[S] 0,06017, Var[S] 0,02216.
- **Metodo dichiarato:** «integrazione di P(S > s)». È equivalente; la forma chiusa lo conferma.

### Q-04 · Valori di riferimento del MAE: **RISOLTO per il MAE, con riserva S-01**
- I valori −2,42 / +2,58 / −0,12 (intraday) e −1,53 (swing) sono quelli **esatti** della revisione V3.1. Sono attribuiti correttamente (`v31_a`) e distinti dai simulati −2,39 / +2,57 / −0,17, nel codice, nel JSON e nei documenti.
- **F(d) ricavata di nuovo in modo indipendente.**
  - Ingredienti: funzione di scala s(x) = 1 − e^(−2μx); probabilità d'uscita P_x(+b prima di −1); proprietà di Markov forte nel primo passaggio a −d. Ne segue F(d) = [1 − P_0(+b prima di −d)]·P_(−d)(+b prima di −1)/P_0(+b prima di −1).
  - Caso μ = 0, R:R 1: F(0,5) = 1/3, quindi P(daily loss al primo trade) = 1/6.
  - Caso R:R 2: μ = 0,097475 e F(0,5) = 0,398109, come nei test.
- **Precisazione (S-08).** «Analitici esatti in forma chiusa» non è esatto: le variazioni dei tassi di superamento sono un **calcolo esatto numerico** (programmazione dinamica sul reticolo) che *usa* la F(d) in forma chiusa.
- **Riserva S-01.** Nella stessa consegna un nuovo valore simulato (0,8596, e 77,60% per la fase 1) è chiamato «benchmark analitico».

### Q-05 · Attribuzione: **RISOLTO**
- Intestazione del motore, README, risposta e registro: riportano le stesse attribuzioni, nella forma proposta («Proposte di correzione: Claude … Revisione indipendente della V3.1: Claude … esito: non validata»). Nel JSON non ci sono attribuzioni a Claude.
- **Inesattezze minori (S-08):**
  - la risposta, riga 69, descrive V01 come «tolleranza bisezione», attribuendo l'osservazione a Claude. Nella mia analisi V01 è «la fase 2 riusa i generatori della fase 1»;
  - la riga 7 indica il commit `8544a15` per la revisione V3.1: è il commit della revisione **V3**; quella V3.1 è `9ff4514`.

### Q-06 · Runner V1 d'archivio: **RISOLTO IN PARTE**
- **Modalità A (collegamento simbolico):** riproduce `a6781b7e…`, identico all'atteso.
- **Modalità B (alias in `sys.modules`):** **fallisce** con `AttributeError: … has no attribute 'main'`, perché il runner V1 definisce `run_suite()`. Con `r.run_suite()` riproduce l'hash atteso (verificato).
- **Citazione dell'import errata:** la riga 13 del runner importa `PropSimulationScenario, run_full_challenge_experiment, wilson_confidence_interval`, non `run_comprehensive_simulations` (S-03).

### Q-08 · Validazione dei parametri del MAE: **RISOLTO, con suggerimenti S-05 e S-06**
- **Casi estremi (`v32_c`):**
  - R:R 50 (WR 0,40 e 0,99), R:R 24, 100 e 500 (WR 0,40), WR 0,99 e 0,999 (R:R 2), R:R 0,1 e 0,02: accettati;
  - in tutti questi casi la deriva riproduce il WR con errore ≤ 2·10⁻¹⁶ e il campionatore coincide con F(d) esatta (8 quantili, n = 20.000, |z| massimo 2,60);
  - WR 0,99 con R:R 500, WR 0,9999995 con R:R 50 e WR 0,40 con R:R 0,001: rifiutati con `ValueError`;
  - nessun `OverflowError`.
- **Soglia μ ≈ 0:** coerente tra risolutore e campionatore. A WR = 1/3 + 10⁻⁸ restituisce μ = 0 con errore 10⁻⁸; appena sopra la soglia l'errore è ≤ 2·10⁻¹¹; F(0,5) è continua (0,400000000 con μ = 0, 1,01·10⁻⁷ e 10⁻⁶).
- **La guardia è più restrittiva del necessario (S-05).** Per μ > 0 il termine e^(−2μ·R:R) va in underflow a 0 senza errore, quindi WR 0,99 / R:R 500 sarebbe calcolabile. La guardia simmetrica 2|μ|·max(1, R:R) < 700 viene dalla **mia** proposta Q-08: il difetto è mio, non di Gemini.
- **Messaggio fuorviante.** Il messaggio parla di overflow anche quando il limite è il tetto ±15 dell'intervallo di bisezione, e arrotonda WR a 4 decimali («WR=1.0000»).
- **Input fuori dal MAE non validati (S-06):** R:R o costo `nan` danno un esito `timeout` silenzioso; R:R `inf` dà `pass`; un rischio negativo viene accettato; `slippage_tail_alpha = 0` produce `ZeroDivisionError`; con `max_days` < `min_days` il motore dichiara un superamento al giorno 4 con un limite di 3 giorni.

---

## 4. Passata avversariale

| Area | Verifica | Esito |
|---|---|---|
| Errori matematici non rilevati | Motore contro calcolo esatto su 4 configurazioni nuove con R:R 1 e 3, intraday e swing, sfida a due fasi con MAE | nessuno: tutti i \|z\| < 1,7 |
| Formule fuori dominio | Risolutore e campionatore del MAE agli estremi; momenti troncati | nessun uso fuori dominio. Dominio ristretto più del necessario (S-05) |
| Simulatore e motore | Runner e test usano lo stesso motore; JSON riprodotto byte per byte; valori uguali alla V3.1 (logica invariata) | coerenti |
| Confini temporali | Congelamento al target, giorni minimi, pavimento giornaliero a mezzanotte, fine del periodo | corretti. Un caso limite incoerente: `max_days` < `min_days` (S-06) |
| Casualità e riproducibilità | Semi CRN per seme 42 fino a 20.000 sfide: 0 collisioni tra i 6 flussi; due flussi coincidono solo tra sfide distanti almeno 439.306.784 indici, per qualsiasi seme | nessun problema |
| Test mancanti | Mutanti nuovi | slippage (V19, V20), Wilson (V21) e soglia μ≈0 (V22) non coperti (S-07) |
| Ipotesi non dichiarate | Lettura del codice e ricerca testuale nei documenti | 3 ipotesi del modello non dichiarate (S-09) |
| Affermazioni eccessive | Confronto sistematico (`CONFRONTO_AFFERMAZIONI_V3_2.md`) | «benchmark analitico» per un valore simulato (S-01); «\|z\| ≤ 1,46» (reale 1,67); «MAE … per qualsiasi (WR, RR) `[DIMOSTRATO]`» malgrado il dominio ristretto; «Regolamento ufficiale FTMO» contro lo stato V-SEC del JSON (S-08) |

---

## 5. Rilievi

Classificazione: **E** errore dimostrato · **L** limite metodologico · **R** rischio potenziale · **S** suggerimento.
Gravità: **Alta** invalida risultati · **Media** etichetta o affermazione fuorviante in un deliverable · **Bassa** documentazione o difetto latente che non tocca le uscite · **Minima**.

| Id | Classe | Gravità | File e posizione | Sintesi | Evidenza |
|---|---|---|---|---|---|
| S-01 | E | Media | `test_prop_risk_v3_2.py:332, 349`; risposta riga 65 | Fase 2 «benchmark analitico» 0,8596 e fase 1 0,776 / 77,60% sono simulati: gli esatti sono **0,8572** e **0,7800** | `output/v32_a_esatto.txt` (A) |
| S-02 | E | Bassa | test righe 296–322 e 327–349; risposta righe 54–65; checkpoint righe 28–31 | Corrispondenza test → mutanti dichiarata errata: il test R:R 1 non può rilevare V10 (identico per costruzione); il test della fase 2 non attraversa `run_full_challenge_v3_2` e non rileva V07. Entrambi sono uccisi da altri test | `v32_a_esatto.txt` (B); `v32_d_mutazioni.txt`; `v32_b_robustezza_test.txt` (3) |
| S-03 | E | Bassa | `archivio_storico/LEGGIMI_V1.md:12, 29` | Modalità B non funziona (`main` inesistente); import citato in modo errato | `output/v32_e_v1_leggimi.txt` |
| S-04 | E (latente) | Bassa | `prop_risk_engine_v3_2.py:46`; righe 84–97 | Wilson: ogni livello diverso da 0,95 riceve z = 2,5758 (a 0,90 restituisce l'IC al 99%); preesistente dalla V3. Kelly: banda ±0,01 attorno a 0,6827 con z = 1; livello non validato | `v32_c_kelly_q08_crn.txt` (Q-01) |
| S-05 | S | Bassa | `prop_risk_engine_v3_2.py:121–154` | Guardia simmetrica più restrittiva del necessario; messaggio d'errore fuorviante. Origine: mia proposta Q-08 | `v32_c_kelly_q08_crn.txt` (Q-08) |
| S-06 | R | Bassa | `prop_risk_engine_v3_2.py:225–228, 344, 370–371` | Input non validati: `nan`/`inf`, rischio negativo, alpha ≤ 0, `max_days` < `min_days` | `v32_c_kelly_q08_crn.txt` (input) |
| S-07 | S | Bassa | test righe 167–175 | Slippage verificato solo nella direzione (riduce il superamento); Wilson non testato; soglia μ≈0 non testata | `v32_d_mutazioni.txt` (V19–V22) |
| S-08 | E (documentale) | Minima | continuità riga 16; checkpoint righe 33, 39; risposta righe 7, 69, 87, 155, 160 | Dimensione dello ZIP; \|z\| ≤ 1,46; «forma chiusa»; V01; commit; «per qualsiasi (WR, RR)»; «Regolamento ufficiale» | §2, §3, `CONFRONTO_AFFERMAZIONI_V3_2.md` |
| S-09 | L | Bassa | motore righe 300–368; documenti | Non dichiarate: nessuna posizione aperta a mezzanotte (il pavimento giornaliero usa il capitale chiuso); trade sequenziali, mai sovrapposti; la catena di Markov riparte dalla distribuzione stazionaria all'inizio della fase 2. Dichiarato solo il commento sui micro-lotti (riga 309) | lettura del codice; ricerca testuale |

Correzioni e test di accettazione: [`CLAUDE_CORRECTION_PROPOSALS_V3_2.md`](CLAUDE_CORRECTION_PROPOSALS_V3_2.md).

---

## 6. Fuori perimetro e dipendenze
- **Q-07 (schede STR) e Q-09 (rulebook):** non verificati, rinviati per mandato dell'utente. File d'archivio intatti.
- **Dipendenza da Q-01.** Ogni soglia di rischio nel rulebook o nelle schede (per esempio il rischio massimo 0,75%) va giustificata senza presupporre un edge: con 300 trade l'edge di riferimento non è dimostrabile al 95%. Da affrontare con Q-09, prima del Trading Guardian.
- **Dipendenza da S-09.** Il Guardian dovrà dichiarare come tratta le posizioni aperte a mezzanotte e le posizioni simultanee: il motore oggi non le modella.

## 7. Limiti di questa revisione
- Le cartelle di Antigravity sul Mac non sono accessibili: la conservazione di V2, V3 e V3.1 è verificata solo sulle copie ricevute.
- Le regole FTMO non sono state riverificate in questa sessione.
- I calcoli «esatti» usano un reticolo razionale e `float` per F(d): l'errore di arrotondamento è trascurabile rispetto alle tolleranze.
- I casi estremi del MAE sono una griglia di 15 punti, non una dimostrazione su tutto il dominio.
