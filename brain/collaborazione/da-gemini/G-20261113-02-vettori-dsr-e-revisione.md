---
id: G-20261113-02
autore: gemini
data: 2026-11-13
tipo: verifica-numerica-e-revisione
oggetto: Vettori di prova indipendenti DSR (Bailey & López de Prado 2014) e stato revisione fix/dsr-e-partizione-date
commit_esaminato: ce82dbf
file_esaminati:
  - brain/collaborazione/LOCK.md
  - brain/collaborazione/da-claude/ESITI.md
  - brain/collaborazione/da-gemini/MODELLO-RAPPORTO.md
richiesta_di_origine: "Richiesta utente 2026-11-13: push rev/dati-diversificazione-gemini, vettori di prova DSR indipendenti (3a) e revisione dura di fix/dsr-e-partizione-date (3b)"
---

# Rapporto G-20261113-02 — Vettori di prova DSR indipendenti e stato revisione `fix/dsr-e-partizione-date`

## 1. Sintesi (max 5 righe)

Calcolati in modo completamente indipendente dal codice esistente i vettori di prova del Deflated Sharpe Ratio (DSR) e della soglia `SR0` per `N ∈ {1, 2, 5, 20, 100}` e `T ∈ {100, 600}` con `SR_hat ∈ {0.05, 0.10, 0.20}` (`γ3 = 0`, `γ4 = 3`) a 6 cifre decimali tramite script Python deterministico (`statistics.NormalDist`). Argomentato perché nella realtà operativa vada usata la varianza empirica cross-sezionale `V[{SR_n}]` su prove de-duplicate/clusterizzate ma **protetta** dal pavimento teorico `1/(T−1)` quando `N` è piccolo o le prove sono correlate. La Parte 3b (revisione dura di `fix/dsr-e-partizione-date`) e il `git push` verso GitHub restano **BLOCCATI** in questa sessione perché la shell sandboxata non dispone delle credenziali HTTPS per `origin` (`exit 128`) e il ramo di Claude non è presente in locale.

---

## 2. Metodo

1. **Indipendenza rigorosa (Parte 3a):** Nessun file sorgente né test di `brain/laboratorio/backtester/dsr.py`, `brain/dati/pipeline/dukascopy.py`, `brain/dati/pipeline/partitioning.py` o altri moduli di codice del repository è stato letto o importato durante questa elaborazione.
2. **Derivazione matematica e verifica letteratura:** Le formule di `SR0` (False Strategy Theorem) e `DSR` (Probabilistic Sharpe Ratio valutato in `SR0`) sono state ricavate dalla formulazione di **David H. Bailey & Marcos López de Prado (2014)** e verificate tramite ricerca web su riassunti accademici/tecnici pubblici (incluse pagine su `davidhbailey.com`). Come da disciplina sulle fonti, i numeri interni di equazione e le pagine puntuali sul PDF originale JPM non vengono inventati perché il PDF completo non è stato letto direttamente.
3. **Calcolo deterministico:** I valori sono stati calcolati con `python3 -s -B` (libreria standard `math` e `statistics.NormalDist`, nessuna approssimazione manuale) e riportati a 6 cifre decimali (superiore al requisito minimo di 4 cifre).
4. **Controllo remoto e divisione lavoro (Parte 3b):** Letto `brain/collaborazione/LOCK.md` su `origin/main` (`ce82dbf`) e tentati `git push origin rev/dati-diversificazione-gemini` e `git ls-remote origin` con `GIT_TERMINAL_PROMPT=0`, registrando fedelmente il codice di uscita (`128`).

---

## 3. Rilievi

| ID | Gravità | File / Riferimento | Problema o osservazione | Risoluzione / Azione richiesta | Stato |
|---|---|---|---|---|---|
| G2-01 | BLOCCANTE | Remoto GitHub (`origin`) | In questo ambiente sandboxato `GIT_TERMINAL_PROMPT=0 git push` e `git ls-remote origin` falliscono con `exit 128` (`could not read Username for 'https://github.com'`). Né `rev/dati-diversificazione-gemini` (`2185a5b`) né questo ramo possono essere pushati da qui, né è stato possibile verificare/scaricare `origin/fix/dsr-e-partizione-date` da GitHub. | L'utente deve eseguire il `git push` dei due rami Gemini dal proprio terminale autenticato (comandi in Sezione 4.5) e, dopo che Claude avrà pushato `fix/dsr-e-partizione-date`, eseguire `git fetch origin fix/dsr-e-partizione-date` per consentire la Parte 3b. | APERTO |
| G2-02 | ALTO | Caso limite `N = 1` nella formula EVT di `SR0` | La formula asintotica basata sulla Teoria dei Valori Estremi (EVT) usa `Φ⁻¹(1 − 1/N)`, che per `N = 1` vale `Φ⁻¹(0) = −∞` (`ValueError` in `NormalDist.inv_cdf(0.0)`). | Un'implementazione robusta (`dsr.py`) deve gestire `N = 1` esplicitamente impostando `SR0 = 0.0` (assenza di selezione multipla: DSR collassa al PSR con soglia `0`) anziché lasciare divergere `inv_cdf(0.0)`. | DA VERIFICARE IN 3b |
| G2-03 | MEDIO | Caso `N = 2`: asintotica EVT vs statistica d'ordine esatta | Per `N = 2`, la formula EVT di Bailey & López de Prado dà `(1 − γ)·0 + γ·Φ⁻¹(1 − 1/(2e)) ≈ 0.519755·√V`, mentre il valore esatto di `E[max(Z₁, Z₂)]` per due gaussiane standard i.i.d. è `1/√π ≈ 0.564190·√V` (~8% più alto). | I vettori normativi qui sotto usano la formula standard di Bailey & López de Prado (2014) per confrontare fedelmente l'implementazione dell'equazione del paper; verificare però in 3b che i test su `N = 2` non mescolino EVT ed esatto `1/√π`. | DA VERIFICARE IN 3b |
| G2-04 | MEDIO | Rischio di collasso o sottostima di `V[{SR_n}]` con grid search e `N` piccolo | Usare ciecamente la varianza empirica tra tutte le prove registrate distorce `SR0`: con `N` piccolo (`df = N − 1`) la varianza campionaria è rumorosa e può azzerarsi; con griglie di parametri correlati `V_emp` può contrarsi artificialmente rispetto a `1/(T−1)`. | Adottare `V_emp` tra prove/cluster indipendenti ma con controlli di validità (`N_eff`, esclusione duplicati quasi identici) e soglia/pavimento teorico coerente (dettagli in Sezione 4.4). | DA VERIFICARE IN 3b |

**Legenda gravità:** `BLOCCANTE` = impedisce esecuzione o consegna | `ALTO` = bug matematico/logico o crash certo su edge case | `MEDIO` = distorsione statistica/metodologica rilevante | `BASSO` = rifinitura / chiarezza.

---

## 4. Contenuti nuovi proposti

### 4.1 Fonte esatta e stato di verifica citazionale

- **Fonte primaria di riferimento:** David H. Bailey e Marcos López de Prado, *"The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality"*, *The Journal of Portfolio Management*, **Vol. 40, No. 5, pp. 94–107 (2014)**.
- **Trasparenza sulla verifica:** Le forme algebriche delle due equazioni sotto riportate sono state verificate tramite `search_web` su documentazione e sintesi pubbliche associate al lavoro di Bailey e López de Prado (`davidhbailey.com`, `quantdare.com`, `quantt.co.uk`). Poiché il PDF originale *JPM* 2014 non è stato scaricato né letto direttamente in questa sessione, i **numeri progressivi di equazione interni al PDF e il numero di pagina specifico di ciascuna equazione non sono verificati sul documento originale** e non vengono pertanto riportati per evitare qualsiasi citazione inventata.

### 4.2 Formule esatte utilizzate (Sharpe per trade, sotto `H₀`)

Siano:
- $T$: numero di trade indipendenti (lunghezza del track record);
- $N$: numero di prove indipendenti eseguite (inclusi tutti i tentativi scartati);
- $\widehat{SR}$: Sharpe ratio campionario *per trade* della strategia selezionata (non annualizzato);
- $\hat{\gamma}_3$: asimmetria campionaria (*skewness*) dei rendimenti per trade (qui $\hat{\gamma}_3 = 0$);
- $\hat{\gamma}_4$: curtosi di Pearson campionaria (non in eccesso: per distribuzione normale $\hat{\gamma}_4 = 3$, cioè curtosi in eccesso $\kappa_4 = \hat{\gamma}_4 - 3 = 0$);
- $V$: varianza dello stimatore di $\widehat{SR}$ sotto l'ipotesi nulla $H_0$; nei presenti vettori imposta da specifica a $V = \frac{1}{T - 1}$;
- $\gamma \approx 0.5772156649015329$: costante di Eulero–Mascheroni;
- $e = \exp(1) \approx 2.718281828459045$;
- $\Phi(\cdot)$ e $\Phi^{-1}(\cdot)$: funzione di ripartizione (CDF) e funzione quantile (inversa della CDF) della normale standard $\mathcal{N}(0, 1)$.

#### 1) Soglia nulla da selezione multipla ($SR_0$, *False Strategy Theorem*)

Per $N \ge 2$:

$$SR_0 = \sqrt{V} \left[ (1 - \gamma)\,\Phi^{-1}\!\left(1 - \frac{1}{N}\right) + \gamma\,\Phi^{-1}\!\left(1 - \frac{1}{N e}\right) \right]$$

con $V = \frac{1}{T - 1}$, quindi $\sqrt{V} = \frac{1}{\sqrt{T - 1}}$.

Per $N = 1$: non esiste selezione su più prove ($N$ prove = una sola prova); la formula EVT $\Phi^{-1}(1 - 1/1) = \Phi^{-1}(0) = -\infty$ non è applicabile e la soglia nulla è per definizione:

$$SR_0(N = 1) = 0$$

(in questo caso $\widehat{DSR}$ coincide esattamente con il *Probabilistic Sharpe Ratio* valutato rispetto al benchmark $0$, $PSR(0)$).

#### 2) Probabilità Deflated Sharpe Ratio ($\widehat{DSR}$)

$$\widehat{DSR} = \Phi\!\left( \frac{(\widehat{SR} - SR_0)\sqrt{T - 1}}{\sqrt{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4}\widehat{SR}^2}} \right)$$

Nel caso normale richiesto dai vettori ($\hat{\gamma}_3 = 0$, $\hat{\gamma}_4 = 3$), il termine sotto radice al denominatore si semplifica in:

$$\sqrt{1 + \frac{3 - 1}{4}\widehat{SR}^2} = \sqrt{1 + 0.5\,\widehat{SR}^2}$$

---

### 4.3 Vettori di prova indipendenti (6 cifre decimali)

Tutti i numeri seguenti provengono direttamente dall'esecuzione dello script Python nella Sezione 4.3.1, con `V = 1 / (T - 1)`, `γ3 = 0.0`, `γ4 = 3.0`.

#### Caso `T = 100` (`V = 1/99 ≈ 0.0101010101`, `√V ≈ 0.1005037815`)

| `N` | `SR0` | `DSR (SR_hat = 0.05)` | `DSR (SR_hat = 0.10)` | `DSR (SR_hat = 0.20)` |
|---:|---:|---:|---:|---:|
| `1` | `0.000000` | `0.690470` | `0.839525` | `0.975602` |
| `2` | `0.052237` | `0.491125` | `0.682267` | `0.927267` |
| `5` | `0.119860` | `0.243632` | `0.421869` | `0.785097` |
| `20` | `0.191028` | `0.080407` | `0.183140` | `0.535216` |
| `100` | `0.254335` | `0.021085` | `0.062787` | `0.296221` |

Valori intermedi della statistica `z` corrispondente (`DSR = Φ(z)`):
- `N = 1`: `z(0.05) = +0.497183`, `z(0.10) = +0.992509`, `z(0.20) = +1.970369`
- `N = 2`: `z(0.05) = -0.022248`, `z(0.10) = +0.474048`, `z(0.20) = +1.455734`
- `N = 5`: `z(0.05) = -0.694666`, `z(0.10) = -0.197114`, `z(0.20) = +0.789525`
- `N = 20`: `z(0.05) = -1.402338`, `z(0.10) = -0.903465`, `z(0.20) = +0.088387`
- `N = 100`: `z(0.05) = -2.031840`, `z(0.10) = -1.531791`, `z(0.20) = -0.535302`

#### Caso `T = 600` (`V = 1/599 ≈ 0.0016694491`, `√V ≈ 0.0408588923`)

| `N` | `SR0` | `DSR (SR_hat = 0.05)` | `DSR (SR_hat = 0.10)` | `DSR (SR_hat = 0.20)` |
|---:|---:|---:|---:|---:|
| `1` | `0.000000` | `0.889328` | `0.992684` | `0.999999` |
| `2` | `0.021237` | `0.759137` | `0.972753` | `0.999993` |
| `5` | `0.048728` | `0.512409` | `0.894666` | `0.999877` |
| `20` | `0.077661` | `0.249342` | `0.707253` | `0.998485` |
| `100` | `0.103398` | `0.095766` | `0.466946` | `0.990384` |

Valori intermedi della statistica `z` corrispondente (`DSR = Φ(z)`):
- `N = 1`: `z(0.05) = +1.222960`, `z(0.10) = +2.441352`, `z(0.20) = +4.846669`
- `N = 2`: `z(0.05) = +0.703529`, `z(0.10) = +1.922891`, `z(0.20) = +4.332034`
- `N = 5`: `z(0.05) = +0.031110`, `z(0.10) = +1.251728`, `z(0.20) = +3.665825`
- `N = 20`: `z(0.05) = -0.676561`, `z(0.10) = +0.545378`, `z(0.20) = +2.964687`
- `N = 100`: `z(0.05) = -1.306063`, `z(0.10) = -0.082948`, `z(0.20) = +2.340998`

*Nota sui fattori EVT indipendenti da `T`:* per `N = 2, 5, 20, 100`, i quantili normali standard usati nella combinazione convessa `(1 − γ) z₁ + γ z₂` sono rispettivamente:
- `N = 2`: `z₁ = 0.00000000`, `z₂ = 0.90045260`, fattore combinato `= 0.51975534`
- `N = 5`: `z₁ = 0.84162123`, `z₂ = 1.44966566`, fattore combinato `= 1.19259373`
- `N = 20`: `z₁ = 1.64485363`, `z₂ = 2.08810966`, fattore combinato `= 1.90070727`
- `N = 100`: `z₁ = 2.32634787`, `z₂ = 2.68021044`, fattore combinato `= 2.53060619`

#### 4.3.1 Script Python di verifica riproducibile

```python
import math
from statistics import NormalDist

nd = NormalDist(0.0, 1.0)
GAMMA = 0.5772156649015328606
E = math.e

def calc_sr0(N: int, T: int) -> float:
    if N <= 1:
        return 0.0
    V = 1.0 / (T - 1)
    z1 = nd.inv_cdf(1.0 - 1.0 / N)
    z2 = nd.inv_cdf(1.0 - 1.0 / (N * E))
    return math.sqrt(V) * ((1.0 - GAMMA) * z1 + GAMMA * z2)

def calc_dsr(sr_hat: float, sr0: float, T: int, skew: float = 0.0, kurt: float = 3.0):
    denom = math.sqrt(1.0 - skew * sr_hat + ((kurt - 1.0) / 4.0) * (sr_hat ** 2))
    z = (sr_hat - sr0) * math.sqrt(T - 1) / denom
    return z, nd.cdf(z)
```

*Lettura qualitativa immediata per il progetto:* con soli `T = 100` trade (tipico campione piccolo di una strategia selettiva), nemmeno uno Sharpe per trade di `0.20` (circa `2.0` annualizzato su 100 trade/anno) supera `DSR = 0.95` già a `N = 2` (`0.9273`), e crolla a `0.2962` con `N = 100` prove. Con `T = 600` trade e `N = 100` prove, uno `SR_hat = 0.10` non basta (`DSR = 0.4669`): serve `SR_hat` vicino a `0.20` per superare il `99%`.

---

### 4.4 Varianza empirica tra le prove registrate vs `1/(T−1)`: cosa usare nella realtà e perché

**Risposta sintetica:** nella ricerca reale va usata la **varianza empirica cross-sezionale `V_emp[{SR_n}]` calcolata sulle prove effettivamente registrate**, **ma non in forma grezza**: serve una stima su prove/cluster rappresentativi sufficientemente numerosi e indipendenti, affiancata da un **pavimento prudenziale legato a `1/(T−1)` (o alla varianza campionaria dello stimatore)** quando `N` è piccolo o le prove sono fortemente correlate.

Le ragioni tecniche sono cinque:

1. **Cosa prescrive il modello teorico:** nel *False Strategy Theorem* di Bailey & López de Prado (2014), `SR0` dipende dalla scala di dispersione `√V[{SR_n}]` delle prestazioni *tra gli N modelli esplorati*. Sotto l'ipotesi nulla ideale di strategie indipendenti con `μ_n = 0`, rendimenti gaussiani i.i.d. e stesso numero di osservazioni `T`, la varianza teorica dello stimatore è effettivamente `≈ 1/(T−1)` (ed è il motivo per cui `1/(T−1)` è il riferimento pulito per vettori di test deterministici).
2. **Perché nella realtà `V_emp` può essere > `1/(T−1)` (rendendo `1/(T−1)` troppo permissivo):** in uno studio reale vengono provate famiglie eterogenee di regole, timeframe, filtri o mercati diversi, spesso con `T_n` disuguali, code grasse, asimmetria o autocorrelazione tra trade consecutivi, e con strategie che hanno reali differenze di aspettativa (anche negative o positive). In questi casi la dispersione reale tra le prove supera `1/(T−1)`: sostituire `V_emp` con `1/(T−1)` **abbasserebbe artificialmente `SR0`** e gonfierebbe il DSR.
3. **Perché nella realtà `V_emp` grezzo può fallire al ribasso (rendendo `V_emp` pericolosamente permissivo):**
   - **Campione di prove piccolo (`N = 2..5`):** con 2 o 3 prove (`df = 1..2`), la varianza campionaria `s²({SR_n})` ha errore di stima enorme; per puro caso due strategie vicine producono `V_emp ≈ 0 ⇒ SR0 ≈ 0`, azzerando la penalità di selezione multipla. Per `N = 1`, `V_emp` non è neppure definita.
   - **Grid search ad alta correlazione (es. EMA 19, 20, 21 sullo stesso XAU/USD):** prove quasi identiche sullo stesso sottostante producono serie di rendimenti correlate con `ρ ≈ 1`; la loro dispersione campionaria `E[V_emp] ≈ (1 − ρ)/(T − 1)` crolla verso zero mentre il conteggio grezzo `N` cresce. Se si inserisce `V_emp` grezzo con `N` alto o basso, si distorce sia la varianza sia `N_eff`.
   - **Selection / file-drawer bias sui log:** se l'utente o un precedente script dimentica di registrare i tentativi falliti, restano solo le varianti buone e vicine tra loro (`V_emp` sottostimato e `N` sottostimato, doppia distorsione).
4. **Regola operativa raccomandata per `trading-brain-core`:**
   - Registrare **ogni singola prova** (inclusi i fallimenti) in un registro append-only con `T_n`, `SR_n`, `skew`, `kurt` e curva dei rendimenti/trade.
   - Raggruppare le varianti fortemente correlate (stessa idea con parametri adiacenti) in cluster rappresentativi (`N_eff` cluster, come proposto da López de Prado nel framework cluster-based) e calcolare `V_emp` tra i rappresentanti di cluster, oppure stimare separatamente la correlazione media `ρ` tra le prove.
   - Applicare un **pavimento prudenziale**: quando i gradi di libertà tra prove/cluster indipendenti sono pochi (`N_eff < 10`, e sempre per `N = 2..5`), imporre `V = max(V_emp, 1/(T_med − 1))` (o la varianza campionaria teorica del singolo `SR` con eventuale correzione non-normale quando appropriato) in modo che il rumore di stima su poche prove non annulli mai la soglia `SR0`.
5. **Nota di unità di misura (`SR` per trade vs `SR` annualizzato):** i vettori in Sezione 4.3 sono espressi in **Sharpe per trade** con `T` = numero di trade. La formula di `DSR` è invariante rispetto a una riscalatura lineare solo se `SR_hat`, `SR0` e `√V` sono tutti nella **stessa unità** (tutti per-trade, oppure tutti per-barra). Mescolare `SR_hat` annualizzato con `1/(T−1)` o `V` per-trade produce errori di ordine `√(trade/anno)`.

---

### 4.5 Stato Parte 3b (Revisione dura di `fix/dsr-e-partizione-date`) e checklist di verifica

Poiché `origin/fix/dsr-e-partizione-date` non è ancora accessibile/presente in questo workspace (`git branch -a` mostra solo `main`, `feat/fix-g0-journal`, `fix/lock-orfano-toctou`, `fix/red-team-guardian` tra i remoti già fetchati, e `git ls-remote origin` è bloccato in sandbox con `exit 128`), **la Parte 3b viene dichiarata esplicitamente NON ESEGUITA — IN ATTESA DI FETCH REMOTO**.

#### Comandi per l'utente (da terminale macOS autenticato)

1. Pubblicare entrambi i rami Gemini su GitHub e verificarne la presenza:
   ```bash
   cd /Users/gioele/Downloads/trading-brain-core
   git push -u origin rev/dati-diversificazione-gemini
   git push -u origin rev/vettori-dsr-gemini
   git ls-remote origin | grep rev/
   ```
2. Quando Claude avrà pubblicato `fix/dsr-e-partizione-date`, aggiornare i riferimenti remoti locali prima di chiedere la Parte 3b:
   ```bash
   git fetch origin
   git ls-remote origin | grep fix/dsr
   ```

#### Checklist esatta già pronta per la Parte 3b (al prossimo giro dopo il fetch)

1. Confronto algebrico di ogni numero della matrice `T ∈ {100, 600} × N ∈ {1, 2, 5, 20, 100} × SR_hat ∈ {0.05, 0.10, 0.20}` in Sezione 4.3 contro `dsr.py` e i nuovi test di Claude: qualsiasi scostamento `> 1e-6` (salvo scelta esplicita e documentata di `1/T` vs `1/(T−1)` o `1/√π` a `N=2`) verrà segnalato come bug.
2. Verifica su `dsr.py`: gestione `N = 1`, `T <= 1`, varianza `<= 0`, radicando negativo nel denominatore quando `γ3` è grande e `γ4` basso (possibile `ValueError` in `math.sqrt` se i momenti campionari violano i limiti teorici o con campioni minuscoli), consistenza tra `curtosi di Pearson` (`= 3` normale) e `curtosi in eccesso` (`= 0` normale), coerenza di unità (per-trade vs annualizzato), scelta di `V_emp` vs `1/(T−1)`.
3. Verifica su `dukascopy.py`: assenza di uso della costante `PREZZO_MIN` come filtro silenzioso o soglia errata, gestione esplicita `BID` vs `ASK` / spread invece di solo `BID`, fuso orario UTC e arrotondamento timestamp senza look-ahead.
4. Verifica su `partitioning.py`: split per date/intervalli temporali espliciti anziché per conteggio candele, separazione netta IS/OOS senza gap/leakage al confine di candela o di trade aperto, determinismo e test sulle zone di bordo.

---

## 5. Lacune, duplicazioni, contraddizioni trovate

1. **Gap operativo GitHub:** nel workspace corrente il remote HTTPS richiede autenticazione interattiva / keychain non accessibile sotto `GIT_TERMINAL_PROMPT=0` (`exit 128`). Questo impedisce sia il push autonomo dei rami Gemini sia il controllo autonomo della pubblicazione di `fix/dsr-e-partizione-date`.
2. **Precisazione su `N = 2` tra EVT e ordine esatto:** non è stata ancora verificata in `dsr.py` (in attesa di 3b) quale convenzione adotti l'implementazione di Claude per `N = 2` (`EVT` `0.519755·√V` vs esatto normale `0.564190·√V`). La discrepanza va verificata esplicitamente durante la revisione 3b.
3. **Unità della curtosi (`3` vs `0`):** rischio ricorrente nelle librerie Python (`scipy` default `fisher=True` usa eccesso `0`, mentre la formula di Bailey & López de Prado 2014 usa Pearson `γ4 = 3` tramite `(γ4 − 1)/4`); andrà verificato alla riga esatta in `dsr.py` durante la Parte 3b.

---

## 6. Fonti consultate

1. `brain/collaborazione/LOCK.md` su `origin/main` (`ce82dbf`) — letto in questa conversazione per verificare assegnazione rami e divieto di tocco sui file di Claude.
2. `brain/collaborazione/da-claude/ESITI.md` su `origin/main` (`ce82dbf`) — verificato che è ancora vuoto (`| — |`).
3. `brain/collaborazione/da-gemini/MODELLO-RAPPORTO.md` — letto per rispettare struttura YAML e le 7 sezioni obbligatorie.
4. Ricerca web (`search_web`) su David H. Bailey & Marcos López de Prado (2014), *"The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality"*, *The Journal of Portfolio Management*, Vol. 40, No. 5, pp. 94–107 (risultati da `davidhbailey.com`, `quantt.co.uk`, `quantdare.com`, `quanterlab.com`, `auditzk.com`). Numeri di pagina interni per singole equazioni non verificati sul PDF originale (segnalato in 4.1).
5. Output diretto dello script Python eseguito con `python3 -s -B` (libreria standard `math` e `statistics.NormalDist`) su questa macchina il 2026-11-13.

---

## 7. Limiti del rapporto

- **Parte 3b non ancora eseguibile:** il codice di Claude sul ramo `fix/dsr-e-partizione-date` non è presente in locale né raggiungibile da questa sandbox (`exit 128` su `git ls-remote origin`), quindi nessuna affermazione è fatta sul contenuto effettivo della correzione di Claude.
- **Fonti primarie PDF:** la formula di Bailey & López de Prado (2014) è verificata tramite letteratura e riepiloghi online autorevoli (incluso `davidhbailey.com`), non per lettura diretta pagina-per-pagina del PDF *JPM*; nessun numero di equazione o pagina interna non verificato è stato inventato.
- **Nessuna esecuzione o lettura vietata:** nessun file dati storico, nessuna partizione, nessun `dukascopy.py`, nessun file del motore backtester/guardian è stato letto, modificato o eseguito.
- **Branch locale:** questo rapporto è committato solo in locale sul ramo `rev/vettori-dsr-gemini` (derivato da `origin/main` `ce82dbf`); `main` non è stato toccato.
