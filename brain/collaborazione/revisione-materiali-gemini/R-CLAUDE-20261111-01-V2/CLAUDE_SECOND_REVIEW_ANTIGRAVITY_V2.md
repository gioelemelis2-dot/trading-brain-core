# CLAUDE_SECOND_REVIEW_ANTIGRAVITY_V2

**Seconda revisione indipendente del pacchetto V2 di Antigravity (Gemini)**
Revisore: Claude · Data: 11/11/2026 · Stato: consegnato all'utente, **non ancora integrato nel Brain**.

> Scopo: stabilire quali conclusioni sono sostenute da matematica, codice e dati, non trovare un accordo. Nessun file di Gemini è stato modificato. Tutti gli strumenti di verifica sono nella cartella `verifiche/` accanto a questo documento, con il prefisso `c*` e l'intestazione `[CLAUDE · VERIFICA]`.

---

## 0. Sintesi

1. **Il motore V2 implementa correttamente il modello che dichiara** (esiti i.i.d., rischio fisso, barriere statica e giornaliera, target congelato). L'ho verificato con un calcolo **esatto** indipendente (catena di Markov su reticolo, nessun campionamento): 32 confronti su 32 entro 2,6 errori standard. Su 30 seed diversi la media coincide con il valore esatto, quindi la simulazione non è distorta.
2. **Il bug `min_days` è risolto e il conteggio dei giorni è corretto.** L'effetto della correzione è **maggiore** di quanto dichiarato: +5,1 punti di superamento nell'intraday all'1% (calcolo esatto), contro i +3,3 della tabella di Gemini, che confronta due simulazioni non accoppiate.
3. **La riproducibilità è piena:** rieseguendo lo script con seed 42 ottengo un `simulations_v2_raw.json` identico byte per byte.
4. **Nuovi difetti nel motore:**
   - la catena di Markov parte sempre "dopo una vincita": il primo trade di ogni fase vince al 70% invece che al 40%, e questo gonfia la probabilità di superamento fino a 11 punti;
   - parametri di Markov non ammissibili vengono troncati senza errore, e il tasso di vincita reale smette di essere quello dichiarato;
   - il parametro di slippage di Pareto è dichiarato ma non viene mai usato;
   - la distribuzione del MAE nel codice non corrisponde a quanto dichiarato nel documento.
5. **Contestazioni matematiche:**
   - **Markov:** formula corretta, implementazione con un errore.
   - **MAE:** i numeri di Gemini sono **contraddetti dal suo stesso modello browniano**: 39,8% dei vincitori con MAE ≤ −0,5R e MAE medio −0,43R, non 10,7% e −0,205R. L'impatto non è trascurabile: −2,3 punti di superamento.
   - **Pareto:** varianza infinita sì; "impedisce la convergenza Monte Carlo" no, non per le probabilità.
   - **Kelly:** derivazione corretta sotto le sue ipotesi. Lo 0,618% però è calcolato **senza costi**; con i costi del motore il valore è 0,464%. L'affermazione sull'overshoot discreto è smentita dal calcolo esatto.
   - **STR-001 e STR-002:** non verificabili, perché non c'è né codice né dati. Diverse affermazioni di STR-002 sono contraddette dalle sue stesse cifre.
6. **Ipotesi dominante non dichiarata come tale:** il limite di 60/25 giorni per fase decide quale livello di rischio "conviene". Con 60 giorni vince l'1%; senza limite pratico vince lo 0,25%, con il 99,4% di superamento.

**Giudizio sullo Studio 01:** il motore V2 è utilizzabile come strumento di ricerca dopo alcune correzioni. Le conclusioni operative dello studio (rischio ottimale, effetto MAE trascurabile, soglia Kelly, filtri STR-002) **non sono integrabili ora** come conoscenza del Brain. Lo sono solo come risultati `[SIMULATO]`, condizionati a ipotesi esplicite (§9).

---

## 1. File e versioni esaminati

| File | Origine | SHA-256 | Corrisponde a `MANIFEST_SHA256.txt` |
|---|---|---|---|
| `prop_risk_engine_v2.py` | allegato in conversazione | `16db320a9c45cec310b526bebbdf2621e20845f01866e61e78191e000be9c9ff` | ✅ |
| `test_prop_risk_v2.py` | allegato | `2c5853354dcb6a5232298550de1130ae23e432b929458a4cad652ab518327a6d` | ✅ |
| `run_simulations_v2.py` | allegato | `1f169e2908d00aa6443123eda93df465f5616a6bc8695e4d22950c35ec1ad94b` | ✅ |
| `simulations_v2_raw.json` | allegato | `74352c518e3e39b86d526e6c9cc14629064da54ec2216bc1706afb90fe89b226` | ✅ |
| `ANTIGRAVITY_V2_REVIEW_PACKAGE.md` | allegato | `7f4aebc29e844f2d9103ef92c386552127a2f56d500914dc1d2b1185581b5b5d` | ✅ |
| `MANIFEST_SHA256.txt` | allegato | `a999d1a4817bcff97b24aa1bea7735655584982e2eadc52862ad8765d9f7b394` | — |

**Limiti di provenienza:**
- **Copie ricevute come allegati in conversazione**, non dalla cartella congelata sul Mac né dal commit locale `af3bd221124abc64bf41d48cdcd5b3293765a02e`, che non ho potuto leggere. Verifico che le copie corrispondano al manifest consegnato, non che siano identiche alla cartella sul Mac.
- **Due manifest discordanti.** La sezione 4 di `ANTIGRAVITY_V2_REVIEW_PACKAGE.md` riporta hash **diversi** per tutti e quattro i file (per esempio motore `7fa01d71…`). I file consegnati corrispondono a `MANIFEST_SHA256.txt`. Gemini deve chiarire quale versione è "congelata" (questione aperta Q-01).
- **Nome del file.** La richiesta di revisione citava `run_comprehensive_simulations.py`; il pacchetto contiene `run_simulations_v2.py`.
- **Materiali non consegnati:** codice e risultati V1; lo "Studio 01" originale; il rulebook YAML; codice e dati del Strategy Discovery Lab (STR-001, STR-002); lo script di profiling dei "470 casi"; il milione di estrazioni Markov; i 50.000 sentieri browniani; le 94.518 aperture.
- **La mia prima revisione,** quella che Gemini chiama "contestazioni di Claude", **non è disponibile in questa sessione.** Valuto le affermazioni come Gemini le riporta. Dove la mia posizione originaria risulta sbagliata, lo dichiaro (§6).

Le copie sono state rese di sola lettura prima di ogni esecuzione. Gli hash sono stati ricontrollati al termine: invariati.

---

## 2. Metodologia

| Fase | Che cosa | Strumento |
|---|---|---|
| Integrità | SHA-256 dei file ricevuti contro `MANIFEST_SHA256.txt` | `sha256sum` (`output/verifica_manifest.txt`) |
| Esecuzione isolata | Collegamenti simbolici ai file originali, in una cartella separata. Il JSON originale è tenuto fuori dalla cartella in cui lo script scrive, così da non essere sovrascritto | `gemini-v2-link/`, `gemini-v2-riferimento/` |
| Riproducibilità | Test di Gemini; riesecuzione delle simulazioni; confronto byte per byte | `output/run_simulations_v2_stdout.txt` |
| Verità di riferimento | Calcolo **esatto**, scritto senza riusare il codice di Gemini, in aritmetica razionale | `verifiche/c1_esatto_challenge.py` |
| Distorsione | Motore di Gemini su 30 seed | `c2_semi_multipli.py` |
| Bug `min_days` e orizzonte | V1 ricostruita (da una riga del documento) contro V2; sensibilità al limite di giorni | `c3_v1_v2_e_orizzonte.py` |
| Markov | Algebra; replica del ramo di codice; esatto con stato | `c4_markov.py`, `c4b_markov_esatto.py` |
| MAE | Formula chiusa del moto browniano con deriva; discretizzazione; impatto con numeri casuali comuni | `c5_mae_browniano.py`, `c6_impatto_mae_crn.py` |
| Slippage | Lomax/Pareto, lognormale, troncamenti; convergenza su 20 seed | `c7_pareto_slippage.py` |
| Kelly | Derivazione; rovina **esatta** del cammino discreto | `c8_kelly_barriera.py` |
| Test | Test di mutazione (11 difetti inseriti in copie separate); test aggiuntivi | `c9_mutazioni.py`, `test_aggiuntivi_claude.py` |
| STR-002 | Sola aritmetica delle cifre dichiarate | `c11_str002_aritmetica.py` |

Classi di contenuto (Brain, STANDARD §8): ogni numero di questo documento è `[ESATTO]` (calcolo senza campionamento), `[SIMULATO]` (con seed dichiarato), `[GEMINI]` (dichiarato da Gemini, non riprodotto) oppure `[IPOTESI]`.

---

## 3. Risultati riprodotti

### 3.1 Test e simulazioni di Gemini
- `test_prop_risk_v2.py`: **3 test, OK** (come dichiarato).
- `run_simulations_v2.py` (seed 42, N = 10.000): output **identico byte per byte** al JSON consegnato.

### 3.2 Confronto con il calcolo esatto `[ESATTO]` contro `[GEMINI]`
Probabilità di superare entrambe le fasi:

| Configurazione | Esatto | Gemini (seed 42) | z |
|---|---|---|---|
| Swing, 2 trade/giorno, 60 giorni, rischio 0,25% | 0,0698 | 0,0688 | −0,38 |
| Swing, 0,50% | 0,4831 | 0,4780 | −1,02 |
| Swing, 0,75% | 0,6535 | 0,6493 | −0,89 |
| Swing, 1,00% | 0,6686 | 0,6653 | −0,70 |
| Swing, 1,50% | 0,5891 | 0,5890 | −0,02 |
| Swing, 2,00% | 0,5156 | 0,5146 | −0,19 |
| Intraday, 6 trade/giorno, 25 giorni, 0,50% | 0,6002 | 0,5985 | −0,34 |
| Intraday, 1,00% | 0,4126 | 0,4054 | −1,45 |

Anche max loss, daily loss e timeout concordano: massimo |z| = 2,56, su un evento con probabilità esatta 0,00004.

Tutte e otto le stime di Gemini stanno sotto il valore esatto. Non è una distorsione: ogni configurazione riparte dal seed 42, quindi le stime sono correlate. Su 30 seed la media coincide con l'esatto (z = −0,50 e +0,73) e la dispersione è binomiale (`output/c2_semi_multipli.txt`).

**Categoria: Confermato matematicamente e riprodotto** (per il modello i.i.d. dichiarato).

---

## 4. Verifica del motore V2

| # | Domanda | Evidenza | Categoria |
|---|---|---|---|
| 4.1 | Il bug `min_days` è risolto? | Al primo raggiungimento del target la fase è superata e non si opera più a rischio (codice, righe 77–80 e 121–123). Il mutante "V1" è ucciso dalla suite di Gemini e dai miei test. Calcolo esatto: con V2 la probabilità non dipende più da `min_days` | **Confermato matematicamente e riprodotto** |
| 4.2 | Il target è congelato senza alterare il conteggio dei giorni? | Il giorno di superamento è max(giorno del target, `min_days`). Il test di Gemini (giorno 4) e il mio test A6 (target al giorno 5 → giorno 5) passano. Il mutante che ignora `min_days` nel conteggio è ucciso dalla suite di Gemini | **Confermato** |
| 4.3 | Le probabilità sono riproducibili? | Byte per byte con seed 42; non distorte su 30 seed | **Confermato e riprodotto** |
| 4.4 | V1 e V2 sono confrontabili a parità di parametri, seed e condizioni? | Il codice V1 non è stato consegnato. Con lo stesso seed i flussi casuali si separano dopo il primo congelamento, quindi i confronti V1/V2 della tabella non sono accoppiati. L'etichetta "varianza seme" è imprecisa: è uno sfasamento dei flussi. Dalla V1 ricostruita: differenza esatta V2 − V1 = **+5,09 punti** nell'intraday all'1% (≈ 509 sfide su 10.000; Gemini dichiara 470 casi e +3,29 punti); +0,22 nello swing all'1%; ≈ 0 nello swing allo 0,5% | **Plausibile ma non sufficientemente dimostrato** (manca la V1; la direzione è confermata, l'entità dichiarata è sottostimata) |
| 4.5 | Sono stati introdotti nuovi errori? | Vedi §4.6 | **Sì: 4 difetti** |
| 4.6 | I test sono sufficienti? | La suite di Gemini uccide **4 mutanti su 11**, quelli legati al bug corretto. Sopravvivono: costi ignorati, P(L\|W) di Markov sbagliata, daily loss ignorato durante il MAE, target della fase 2 sbagliato, più tre mutanti equivalenti. I miei test aggiuntivi (gruppo A) uccidono 6 dei 7 sopravvissuti. Il settimo e i due equivalenti non sono distinguibili dal percorso usato nelle simulazioni | **I test confermano il comportamento atteso sulla correzione, ma non proteggono il resto del motore** |

### 4.6 Difetti trovati nel motore V2

| Id | Difetto | Prova | Effetto | Gravità |
|---|---|---|---|---|
| E-01 | **Stato iniziale di Markov sbilanciato.** `last_outcome_was_loss = False` all'inizio di ogni fase, cioè si parte come dopo una vincita | `[SIMULATO]` primo trade vincente nel 70,0% dei casi (stazionaria 40%). Test B1 fallisce | `[ESATTO]` superamento delle due fasi con P(L\|L) = 0,8: swing 1% **54,2% contro 44,1%** con partenza stazionaria; intraday 1% **33,9% contro 22,8%**. Le simulazioni consegnate non usano Markov, quindi il JSON non è toccato | **Alta** per qualsiasi studio con clustering |
| E-02 | **P(L\|W) troncata a 1 senza errore** quando P(L\|L) < 1 − p/(1−p) (per p = 0,40: P(L\|L) < 0,333) | Con P(L\|L) = 0,20 il tasso di vincita effettivo è 44,5% invece di 40%. Test B2 fallisce | Parametri incoerenti producono uno scenario diverso da quello dichiarato | Media |
| E-03 | **`slippage_tail_alpha` dichiarato ma mai usato** | Stesso risultato con e senza (test B3). Il documento parla di "Pareto troncata" come correzione adottata | La correzione non esiste nel codice | Media (documentazione fuorviante) |
| E-04 | **Il MAE implementato non corrisponde a quello dichiarato.** Normale(−0,205; 0,1025) tagliata in [−0,95; 0] | Implica P(MAE ≤ −0,5R) = **0,2%**, contro 10,7% dichiarato da Gemini e 39,8% del modello browniano esatto (§5.B) | Sottostima del rischio di daily loss intra-trade | **Alta** |
| E-05 | Il MAE è applicato solo ai trade vincenti e non include i costi nel valore fluttuante | Lettura del codice (righe 97–105) | Piccolo | Bassa |

---

## 5. Contestazioni matematiche

### A. Catena di Markov
- **Formula:** dalla stazionarietà π_L = π_W·P(L|W) + π_L·P(L|L) si ottiene P(L|W) = (1−p)(1−P(L|L))/p. Con p = 0,40 e P(L|L) = 0,80: P(L|W) = 0,30 e P(W|W) = 0,70. Autocorrelazione a un passo ρ₁ = P(L|L) − P(L|W) = 0,50. Durata media delle serie: vincenti 3,33 trade, perdenti 5,00. `[ESATTO]`
- **Riproduzione:** 1.000.000 di esiti con il ramo di codice di Gemini danno WR 0,3995, P(W|W) 0,6998, ρ₁ 0,5001, serie 3,33 e 5,01. `[SIMULATO]`, seed 2026.
- **Interpretazione del clustering:** è corretto che il modello generi anche serie di vincite. È una conseguenza di una catena simmetrica nel segno dell'autocorrelazione, non un'anomalia. Il modello però non rappresenta cambi di regime dell'aspettativa. L'HMM proposto da Gemini è una direzione ragionevole, ma resta un'ipotesi.
- **Stazionarietà nel codice:** violata all'inizio di ogni fase (E-01) e per parametri non ammissibili (E-02).

| Affermazione | Categoria |
|---|---|
| Formula di P(W\|W) e ρ₁ = 0,5 | **Confermato matematicamente e riprodotto** |
| L'implementazione rispetta la distribuzione stazionaria | **Contestato con evidenze contrarie** (E-01, E-02) |
| Il modello a due stati descrive il clustering reale delle perdite | **Non verificabile con i dati disponibili** (nessun dato di trade reali) |

### B. MAE (escursione avversa massima)
**Modello dichiarato:** moto browniano continuo tra stop −1R e target +2R, con P(vincita) = 0,40.

**Calcolo esatto** con la funzione di scala s(x) = 1 − e^(−2μx), σ = 1:
- deriva che dà P(vincita) = 0,40: μ = 0,0975 (a deriva nulla P(vincita) = 1/3);
- P(MAE ≤ −m, vincita) = P₀(toccare −m prima di +2) × P₋ₘ(toccare +2 prima di −1).

| | Esatto | Gemini |
|---|---|---|
| P(MAE ≤ −0,5R \| vincita) | **0,398** | 0,107 |
| MAE medio dei vincitori | **−0,43R** | −0,205R |

La discretizzazione sottostima il minimo, ma anche con soli 4 passi per unità di tempo si ottiene 27,6% e −0,29R. Il 10,7% di Gemini non è spiegabile con il modello che dichiara. `[SIMULATO]`

**Impatto sulla challenge** `[SIMULATO]`, 30.000 sfide, numeri casuali comuni, un seed per sfida. Il simulatore è validato contro l'esatto: z tra −0,6 e −0,1.

| Configurazione | Nessun MAE | MAE del motore | MAE browniano |
|---|---|---|---|
| Intraday 1%: superamento | 0,4123 | −0,12 punti | **−2,28 punti** |
| Intraday 1%: daily loss | 0,5282 | −0,09 | **+2,49 punti** |
| Swing 1%: superamento | 0,6671 | −0,56 | **−1,37 punti** |

| Affermazione di Gemini | Categoria |
|---|---|
| "Solo il 10,7% dei vincitori ha MAE ≤ −0,5R; MAE medio −0,205R" (sentieri browniani) | **Contestato con evidenze contrarie** (formula chiusa: 39,8%, −0,43R) |
| "Variazione sulla Daily Loss trascurabile (< 0,5%)" | **Contestato con evidenze contrarie** (+2,5 punti con il MAE browniano; il test MAE di Gemini, con seed comune ma senza accoppiamento, ha errore ≈ 0,7 punti e non può rilevare effetti sotto ~1,4 punti) |
| La mia stima originaria (≈ 42%, come riportata da Gemini) | **Confermata sotto ipotesi** (moto browniano) |
| Quale MAE abbiano i trade reali | **Non verificabile con i dati disponibili.** Il moto browniano è un modello teorico; serve il MAE misurato su trade reali o su un backtest con dati intraday |

### C. Pareto e slippage
**Fatti matematici:** per una Pareto (o Lomax) di indice α, la media è finita se e solo se α > 1 e la varianza è finita se e solo se α > 2. Con α = 1,8: media finita, **varianza infinita**. ✔

**Conseguenza per il Monte Carlo:** la stima di una **probabilità** (superamento, daily loss, rovina) è la media di una variabile 0/1, che ha varianza finita qualunque sia la coda dello slippage. Quindi il teorema del limite centrale vale e l'errore è binomiale.
- Verifica `[SIMULATO]`: 20 seed × 5.000 sfide con slippage Lomax non troncato. Dispersione tra seed 0,0068, errore binomiale atteso 0,0068.
- La varianza infinita rallenta invece la convergenza delle stime del **P/L medio**, dove vale il teorema del limite centrale generalizzato e non quello classico. Non riguarda le probabilità di superamento.

**Troncamento a 3R** `[SIMULATO]`, parametri **illustrativi** (Lomax α = 1,8, scala 0,05R, mediana 0,023R). Intraday 1%, 30.000 sfide:

| Slippage sugli stop | Superamento | Differenza |
|---|---|---|
| Nessuno | 0,4113 | — |
| Lognormale, stessa mediana | 0,3770 | −3,43 punti |
| Lomax troncata a 1R | 0,3668 | −4,45 |
| Lomax troncata a 3R | 0,3607 | −5,06 |
| Lomax non troncata | 0,3596 | −5,17 |

Con questi parametri il troncamento a 3R cambia poco (0,1 punti): conta soprattutto lo **slippage medio**, che il costo fisso di 0,05R potrebbe sottostimare. Con code più pesanti il troncamento conterebbe di più. Il valore realistico va **stimato da esecuzioni reali**.

"Circuit breaker e limiti di prezzo" non proteggono da gap del weekend, di valute o CFD. Esempio noto: EUR/CHF del 15/01/2015, citato da conoscenza (C), da documentare.

| Affermazione | Categoria |
|---|---|
| Pareto α ≤ 2 ⇒ varianza infinita | **Confermato matematicamente** |
| "Viola il TLC e impedisce la convergenza del Monte Carlo" | **Contestato con evidenze contrarie** (per le probabilità stimate dallo studio) |
| "3R è un limite superiore realistico" | **Non verificabile con i dati disponibili** (nessuna evidenza empirica fornita) |
| "Adottata la Pareto troncata" | **Contestato con evidenze contrarie** (parametro non usato, E-03) |
| La mia proposta originaria α = 1,8 non troncata | **Matematicamente ammissibile** per stimare probabilità. Il valore di α va comunque giustificato con dati: anche per me resta un'ipotesi |

### D. Kelly a barriera finita
**Derivazione** (approssimazione di diffusione). Con rischio fisso f per trade, l'equity ha incrementi di media f·m e varianza f²·s², dove m = E[R] e s² = Var[R].
- Per un moto browniano con deriva μ e varianza σ², la probabilità di toccare **mai** −D è ψ = exp(−2μD/σ²) = exp(−2mD/(f·s²)).
- Imponendo ψ ≤ α: **f ≤ 2mD / (s²·ln(1/α))**.
- Con target +T a cui ci si ferma: ψ_T = (1 − e^(−θT)) / (e^(θD) − e^(−θT)), con θ = 2μ/σ².

| Calcolo | Valore |
|---|---|
| m = 0,20, s² = 2,16 (**senza costi**), D = 10%, α = 5% | f* = **0,618%** (coincide con Gemini) |
| m = 0,15, s² = 2,16 (**costo 0,05R, come nel motore**) | f* = **0,464%** |
| ψ alla soglia, poi con target T = D | 5,00% → 4,76% (coincide con Gemini) |

Rovina **esatta** del cammino discreto (`[ESATTO]`, esiti netti):

| f | Diffusione, orizzonte infinito | Esatto, orizzonte infinito | Diffusione con T = +10% | Esatto con T = +10% |
|---|---|---|---|---|
| 0,464% | 5,01% | 4,21% | 4,77% | 4,04% |
| 0,618% | 10,57% | 9,16% | 9,56% | 8,42% |
| 1,000% | 24,94% | 22,14% | 19,96% | 18,29% |

Senza costi, allo 0,618%: diffusione 5,00%, esatto 3,64%.

**Incertezza sull'edge:** con un win rate stimato su 300 trade (±1 errore standard) f* va da 0,21% a 0,71%; su 100 trade da 0,01% a 0,89%.

| Affermazione | Categoria |
|---|---|
| Formula per orizzonte infinito e diffusione | **Confermato solo sotto determinate ipotesi** (diffusione, trade i.i.d., edge noto, nessun limite giornaliero né temporale) |
| 5,00% → 4,76% con il target | **Confermato matematicamente e riprodotto** |
| "L'overshoot discreto rialza il rischio reale" | **Contestato con evidenze contrarie** (il calcolo esatto dà rovina più bassa della diffusione, in tutti i casi provati) |
| "0,618% è una valida euristica conservativa" | **Contestato con evidenze contrarie.** Con i costi del motore, a 0,618% la rovina esatta è 8,4–9,2%, non ≤ 5%. Il valore corretto per α = 5% è ≈ 0,46% in diffusione, e un po' più alto con il calcolo esatto |
| 0,60% come limite dimostrabile | **Non lo è:** è un'euristica, e dipende fortemente da un E[R] incerto |
| Se il valore 0,618% veniva dalla mia prima revisione | **Errore mio:** ho omesso i costi che lo stesso modello assume |

### E. STR-002 (ramo Fade, filtri)
**Mancano codice, dati, costi e risultati fuori campione.** Le affermazioni sono verificabili solo aritmeticamente (`c11`):
- **"94.518 aperture S&P 500".** Corrisponde a ≈ 375 anni di sedute: non è un campione storico 2016–2026, è un **campione sintetico** generato da distribuzioni. Va etichettato `[SIMULATO]`, non presentato come "verificato".
- **Pareggio al 61,2% con R:R 0,70.** Implica un costo di ≈ 0,040R per trade: coerente. Per i trade conservati, che hanno R:R ≥ 0,70, il pareggio varia.
- **"Sostenibile con gap fill medio al 70%".** Confonde la **frequenza di chiusura del gap** con il **win rate del trade**, che dipende da stop e target. Inoltre il v1 del Brain (lezione 0.17, dati del vault non ancora verificati) indica che la chiusura dei gap **diminuisce** con l'ampiezza del gap: un filtro che tiene i gap più ampi abbassa probabilmente il tasso di chiusura. `[IPOTESI]`
- **"Il filtro R:R ≥ 1,2 distrugge la significatività statistica".** Sulle stesse ipotesi di Gemini (WR 70%, 10 anni ≈ 2.515 sedute) il filtro 1,2 lascia ≈ 345 trade con pareggio 47,7% e z ≈ 9,0; il filtro 0,70 lascia ≈ 966 trade con pareggio 61,2% e z ≈ 6,0. Meno trade non significa meno significatività se il margine per trade cresce. La significatività dipende dal WR reale dei trade conservati, che nessuno ha misurato.
- **Soglia 0,70 e gap minimo 0,12 ATR.** Scelti **dopo** aver visto le distribuzioni simulate: non è un'ipotesi pre-registrata, anche se il documento la etichetta così. Va dichiarato il numero di soglie provate.
- **Zona morta 0,35–0,80 ATR.** **Non è trattata** nel pacchetto V2.

| Affermazione | Categoria |
|---|---|
| Mediana R:R 1:0,43 senza filtri; 86,3% di operazioni eliminate; 38,4% conservate | **Non verificabile con i dati disponibili** |
| "Distrugge la significatività" | **Contestato con evidenze contrarie** (sotto le stesse ipotesi di Gemini) |
| Pareggio 61,2% | **Confermato sotto ipotesi** (costo ≈ 0,04R) |
| Sostenibilità con gap fill 70% | **Plausibile ma non sufficientemente dimostrato** (confonde chiusura del gap e win rate) |
| Regole per la zona morta | **Non verificabile:** assenti |

**Richiesta:** dati (strumento, fonte, periodo, sessione, fuso), costi per trade, codice, divisione dentro/fuori campione decisa prima, log di tutte le varianti provate, risultati fuori campione.

### F. STR-001 (Donchian con resting stop)
- **Logica:** H₂₀ = max(High₍ₜ₋₂₀₎ … High₍ₜ₋₁₎) è nota prima dell'inizio della barra t. Un buy stop piazzato a H₂₀ evita il ritardo dell'ingresso all'apertura successiva e non usa informazione futura. ✔
- **Esecuzione,** da modellare esplicitamente:
  - **gap oltre lo stop:** se l'apertura è sopra H₂₀ il riempimento avviene all'apertura, non a H₂₀, e lo slippage è (apertura − H₂₀);
  - **tocco intraday:** il riempimento avviene anche se la barra chiude sotto, con falsi breakout;
  - **sessione:** per futures quasi 24 ore, uno stop GTC può essere eseguito di notte con liquidità bassa. Le barre su cui si calcola H₂₀ (solo sessione principale o sessione completa) devono essere coerenti con quella in cui lo stop è attivo;
  - **slippage sugli stop** (§5.C).
- **"Standard Dennis/Carver".** Per le regole dei Turtle di Dennis l'ingresso su stop al breakout è plausibile (C: Faith, *Way of the Turtle*, 2007, da verificare). Per Carver l'attribuzione è dubbia: i suoi sistemi pubblicati usano soprattutto previsioni continue sulle chiusure giornaliere (C, da verificare).

| Affermazione | Categoria |
|---|---|
| H₂₀ nota prima della barra t; il resting stop evita il look-ahead | **Confermato matematicamente** (come logica) |
| Implementazione con gap, slippage e modalità di esecuzione | **Non verificabile con i dati disponibili** (nessun codice né backtest) |
| "Standard Dennis/Carver" | **Plausibile ma non sufficientemente dimostrato** (Carver probabilmente non pertinente) |

---

## 6. Errori miei riconosciuti
Per quanto si può dedurre dalle citazioni di Gemini, perché la mia prima revisione non è disponibile qui:
1. **Kelly:** se lo 0,618% è mio, è calcolato senza costi; il valore coerente con il modello è ≈ 0,46%.
2. **R:R ≥ 1,2:** la mia proposta (come riportata) non è dimostrata migliore. Lo è solo sotto l'ipotesi, non verificata, che il WR dei trade conservati resti alto.
3. **Pareto α = 1,8:** matematicamente ammissibile, ma il valore non è giustificato da dati.
4. **Su MAE e min_days** le mie contestazioni originarie risultano sostenute dai calcoli.

---

## 7. Test aggiuntivi
File: `verifiche/test_aggiuntivi_claude.py`. Non modifica il motore; lo importa tramite collegamento.

| Gruppo | Test | Sul motore V2 consegnato |
|---|---|---|
| A1–A3 | Concordanza con il calcolo esatto (swing 1%, intraday 1%, Markov con lo stesso stato iniziale) entro 4 errori standard | ✅ passano |
| A4 | Il MAE viola il daily loss durante un trade vincente (generatore controllato) | ✅ |
| A5 | Costi applicati | ✅ |
| A6 | Target raggiunto dopo `min_days` chiude quel giorno | ✅ |
| B1 | Markov parte dalla stazionaria | ❌ (documenta E-01) |
| B2 | Parametri Markov non ammissibili rifiutati | ❌ (E-02) |
| B3 | `slippage_tail_alpha` ha effetto | ❌ (E-03) |

Test di mutazione (`output/c9_mutazioni.txt`, `output/c10_test_aggiuntivi_mutanti.txt`):

| Mutante | Suite Gemini | Test Claude (A) |
|---|---|---|
| M01 V1 senza congelamento | ucciso | ucciso |
| M02 congela ma continua a operare | ucciso | ucciso |
| M03 pavimento giornaliero statico | ucciso | ucciso |
| M04 `<` invece di `≤` sul max loss | sopravvive | sopravvive (equivalente: nessun pareggio esatto possibile con questi parametri) |
| M05 target controllato prima delle barriere | sopravvive | sopravvive (equivalente: target > 0 > barriere) |
| M06 costi ignorati | sopravvive | **ucciso** |
| M07 P(L\|W) sbagliata | sopravvive | **ucciso** |
| M08 daily loss ignorato durante il MAE | sopravvive | **ucciso** |
| M09 fase 2 con target della fase 1 | sopravvive | **ucciso** |
| M10 giorni sottostimati | ucciso | sopravvive |
| M11 daily loss 4% come default | sopravvive | sopravvive (la simulazione completa passa 5% esplicitamente) |

---

## 8. Ipotesi del modello che condizionano lo Studio 01
| Ipotesi | Perché conta | Evidenza |
|---|---|---|
| **Limite di 60 (swing) e 25 (intraday) giorni per fase** | Decide il rischio "ottimale". Superamento esatto con 60 → 1000 giorni: 0,25% passa da 7,0% a **99,4%**; 0,5% da 48,3% a 91,1%; 1% da 66,9% a 70,3%. Con limite lungo i rischi bassi dominano | `[ESATTO]` `output/c3_v1_v2_e_orizzonte.txt`. Le regole FTMO sul limite di tempo sono **discordanti** nelle fonti secondarie e non verificate su ftmo.com |
| **Edge positivo noto** (WR 40%, R:R 2, costo 0,05R ⇒ E[R] = +0,15R) | Tutte le probabilità sono condizionate a un edge supposto, non misurato | Nessun dato di trading |
| **Trade i.i.d.** | Con clustering (Markov, partenza stazionaria) il superamento cambia fino a circa 23 punti (swing 1%: 66,9% → 44,1%) | `[ESATTO]` `output/c4b_markov_esatto.txt` |
| **"Swing" con trade chiusi in giornata** | Uno swing reale tiene posizioni oltre la mezzanotte: P/L aperto, gap, pavimento giornaliero calcolato sul saldo | Lettura del codice |
| **Regole FTMO** (5% giornaliero da saldo di mezzanotte, 10% statico, target 10% e 5%) | Coerenti con l'esempio FAQ ospitato da FTMO/OANDA; da confermare sulle pagine ufficiali alla data del rulebook (non consegnato) | Fonti secondarie |
| **MAE quasi nullo, slippage = costo fisso** | Sottostimano daily loss e max loss (§5.B, §5.C) | `[SIMULATO]` |

---

## 9. Giudizio finale sullo Studio 01

| Componente | Riproducibile | Corretto nel merito | Ipotesi accettabili | Pronto per integrazione |
|---|---|---|---|---|
| Motore V2 (modello i.i.d.) | ✅ | ✅ | da dichiarare | **Con correzioni** (E-01…E-04) e test aggiuntivi |
| Correzione `min_days` | ✅ | ✅ | ✅ | **Sì** |
| Tabella V1/V2 | ❌ (manca la V1) | direzione sì, entità sottostimata | — | No, sostituire con il confronto esatto |
| Markov | ✅ | formula sì, implementazione no | — | Dopo E-01, E-02 |
| MAE | ✅ (codice) | **no** | no | No |
| Pareto/slippage | — | parzialmente | 3R non giustificato | No; parametro non implementato |
| Kelly 0,60–0,618% | ✅ | derivazione sì, valore no (costi) | — | Solo come euristica corretta (≈ 0,46%) con incertezza esplicita |
| STR-001 | — | logica sì | — | Ipotesi da testare |
| STR-002 | ❌ | in parte contraddetto | no | Ipotesi da riformulare e testare |

**Conclusione.** La V2 è un passo avanti reale: corregge un bug dimostrato ed è pienamente riproducibile. Le **conclusioni operative** dello Studio 01 non sono sostenute in forma generale: dipendono da un limite temporale non verificato, da un edge supposto, da un MAE sottostimato e da una soglia Kelly che non include i costi. Nel Brain possono entrare solo come **risultati `[SIMULATO]` condizionati**, con le ipotesi della §8 scritte accanto a ogni numero. Le strategie restano **ipotesi**, finché non ci sono dati, codice, costi e verifiche fuori campione.

---

## 10. Questioni aperte
| Id | Questione | Chi |
|---|---|---|
| Q-01 | Quale manifest vale? La sezione 4 del documento e `MANIFEST_SHA256.txt` riportano hash diversi | Gemini |
| Q-02 | Consegna del codice e dei risultati V1, per confrontare V1 e V2 sullo stesso motore | Gemini |
| Q-03 | Come sono stati ottenuti il 10,7% e il −0,205R del MAE (numero di passi, deriva, generatore)? | Gemini |
| Q-04 | Regole FTMO ufficiali alla data del rulebook: limite di tempo, base del daily loss, max loss statico o trailing | Gemini (fonti ufficiali), poi utente |
| Q-05 | Dati di esecuzione reali per stimare slippage e MAE | Utente / Gemini |
| Q-06 | STR-001/002: codice, dati, costi, log delle varianti, fuori campione | Gemini |
| Q-07 | La mia prima revisione: rendere disponibile il testo per confrontare citazioni e risposte | Utente |

## 11. Proposte di correzione (da eseguire da Gemini, dopo approvazione dell'utente)
1. E-01: stato iniziale estratto dalla distribuzione stazionaria, oppure dichiarato come parametro.
2. E-02: validare P(L|L) ≥ 1 − p/(1−p) e sollevare un errore altrimenti.
3. E-03: implementare lo slippage dichiarato o rimuovere il parametro e la frase sulla "Pareto troncata".
4. E-04: sostituire la Normale del MAE con la distribuzione browniana condizionata (formula in `c5`) o con una distribuzione empirica; correggere il documento.
5. Aggiungere al pacchetto un calcolo esatto di riferimento (come `c1`) e i test A1–A6.
6. Tabella V1/V2: rifarla con flussi accoppiati o con calcolo esatto.
7. Kelly: ricalcolare con costi e con incertezza sull'edge; presentarlo come euristica.
8. Rendere il limite di giorni un parametro esplicito, con l'analisi di sensibilità della §8.
9. STR-002: etichettare come `[SIMULATO]` le 94.518 aperture; trattare la zona morta; pre-registrare le soglie prima di guardare i dati.

## 12. Riproduzione di questa revisione
```bash
cd revisione-v2-claude
python3 -I verifiche/c1_esatto_challenge.py gemini-v2-riferimento/simulations_v2_raw_GEMINI.json output/c1_esatto_vs_gemini.json
PYTHONPATH= python3 -s verifiche/c2_semi_multipli.py gemini-v2-link verifiche
python3 -I verifiche/c3_v1_v2_e_orizzonte.py verifiche
python3 -I verifiche/c4_markov.py
python3 -I verifiche/c4b_markov_esatto.py
python3 -I verifiche/c5_mae_browniano.py
python3 -I verifiche/c6_impatto_mae_crn.py verifiche 30000
python3 -I verifiche/c7_pareto_slippage.py
python3 -I verifiche/c8_kelly_barriera.py verifiche
python3 -I verifiche/c9_mutazioni.py <motore> <test> verifiche/mutanti
python3 -I verifiche/c11_str002_aritmetica.py
```
Le uscite sono in `output/`. Le impronte dei file di revisione sono in `MANIFEST_REVISIONE_CLAUDE.sha256`.
