---
id: G-20261113-01
autore: Gemini
data: 2026-11-13
tipo: revisione
oggetto: "Revisione critica indipendente di DA-26, DA-27, DA-28, del Piano di diversificazione e delle contromisure contro l'autoinganno"
commit_esaminato: "43fff60"
file_esaminati:
  - brain/CONTINUITA.md
  - brain/collaborazione/LOCK.md
  - brain/governance/DECISIONI-APERTE.md (voci DA-19..DA-28)
  - brain/governance/PIANO-DIVERSIFICAZIONE.md
  - brain/governance/REGISTRO-MODIFICHE.md (voci v1.18..v1.22)
  - brain/dati/pipeline/dukascopy.py
  - brain/laboratorio/backtester/dsr.py (righe 160-260)
  - brain/dati/reali/demo_broker_mt5_50k_xauusd.toml
richiesta_di_origine: "Richiesta utente 2026-11-13 (DA-26, DA-27, DA-28, PIANO-DIVERSIFICAZIONE.md)"
---

# Revisione critica indipendente su DA-26, Piano di diversificazione e contromisure contro l'autoinganno

## 1. Sintesi (max 5 righe)
Il passaggio al sigillo provvisorio (`DA-26`) è corretto ma incompleto: «tenere un periodo vecchio come verifica» **non rende il test cieco per gli LLM** e rischia di confrontare costi/volatilità incomparabili senza normalizzazione e senza dati `ASK`. Il `PIANO-DIVERSIFICAZIONE.md` (`DA-27`, `DA-28`) contiene una contraddizione diretta tra *stesso calendario comune* e inclusione di asset giovani (`BTCUSD`/indici), sovraespone al fattore `USD` e trascura che l'attuale `dukascopy.py` blocca `XAUUSD < 1000` e partiziona in percentuale (`0.7`), mentre `dsr.py` omette $\sqrt{V[\widehat{SR}_n]}$ in `sr_star`. Le contromisure contro l'autoinganno elencate in `CONTINUITA.md`/`REGISTRO-MODIFICHE.md` **non bastano** senza chiusura dei gradi di libertà di Fibonacci/order block e prevenzione dei test esplorativi non registrati.

---

## 2. Metodo
Revisione critica in sola lettura sui documenti di governance e sul codice sorgente della pipeline e del backtester al commit `43fff60` (`origin/main`), condotta su ramo separato `rev/dati-diversificazione-gemini`.
- **Vincoli rispettati:** nessuna esecuzione di `dukascopy.py`, nessuna lettura di file storici/CSV/cache/partizioni, nessuna ricerca del nonce esterno, nessuna modifica al codice o alle regole personali.
- **Verifiche bibliografiche e tecniche:** controllo mirato di fonti secondarie/abstract su data di inizio storica di Dukascopy per XAUUSD/EURUSD, su McLean & Pontiff (2016) e sulla formula di Bailey & López de Prado (2014) per il Deflated Sharpe Ratio.
- **Cosa non è stato possibile consultare:** il documento esterno *«Trading Brain — Progetto generale»* (su `claude.ai`, fuori dal repository), i testi integrali dietro paywall di McLean & Pontiff (2016) e Bailey & López de Prado (2014), le serie storiche effettive sui server Dukascopy (non interpellati) e le specifiche/disponibilità reali di tutti gli strumenti presso i broker demo/FTMO.

---

## 3. Rilievi

| # | File e sezione | Affermazione esaminata | Esito | Evidenza | Stato fonte | Proposta concreta |
|---|---|---|---|---|---|---|
| 1 | `DECISIONI-APERTE.md` `DA-26`; `CONTINUITA.md` §Gate 2 | "Più anni di storico; un periodo vecchio tenuto come verifica" | ⚠️ | Un periodo storico vecchio (es. 2003–2015) è già noto ai pesi di addestramento di Claude e Gemini quanto o più dell'ultimo anno: mitiga solo la vista visiva recente dell'utente su MT5/TV, non elimina il leakage dei modelli. | [RAGIONAMENTO + STIMA] su `DA-26` righe 255–260 | Riclassificare il periodo vecchio come **Holdout multi-regime non cieco** e riservare l'etichetta di test cieco autentico solo all'incubazione forward post-sigillo. |
| 2 | `dati/pipeline/dukascopy.py` riga 44 (`PREZZO_MIN`) | Scaricamento XAUUSD su più anni (`DA-26`) | ❌ | Nel codice attuale `PREZZO_MIN = Decimal("1000")`: qualsiasi candela storica `XAUUSD < 1000` USD/oz (pre-2009/2010) solleva `ErroreDati` bloccando `DA-26`. | `V` (codice `dukascopy.py:44,166-168`) | Prima di estendere `DA-26` a prima del 2010, verificare sul feed `.bi5` scala e prezzi reali pre-2010 e parametrizzare `PREZZO_MIN` per data/strumento. |
| 3 | `dati/pipeline/dukascopy.py` riga 237 vs `PIANO-DIVERSIFICAZIONE.md` Regola 1 | "Stesso calendario di sviluppo e di verifica per tutti i mercati" | ❌ | `dukascopy.py:237` invoca `DatasetPartitioner(0.7).split(...)` per frazione di righe, **non** per `split_time` in date UTC. Asset con orari diversi (es. DAX vs FX vs BTC 24/7) o anni di inizio diversi avranno date di taglio incompatibili. | `V` (`dukascopy.py:237`; `PIANO-DIVERSIFICAZIONE.md:14`) | Imporre `split_time` esplicito in date UTC (con fascia di embargo) anziché `in_sample_ratio = 0.7`, separando il calendario lungo (FX/Oro) dai mercati giovani. |
| 4 | `PIANO-DIVERSIFICAZIONE.md` §Regola 1 e §Mercati candidati | "Stesso calendario" applicato a `EURUSD`, `S&P 500`, `DAX`, `WTI/Brent`, `BTCUSD` | ❌ | `DA-27` Regola 1 obbliga lo stesso calendario per tutti; includere `BTCUSD` (storia recente sui feed retail/CFD) o asset che partono molto più tardi di `XAUUSD`/`EURUSD` (il cui feed tick è indicato da fonti terze dal 4–5 maggio 2003, non verificato per `.bi5` né per indici/petrolio) costringerebbe a troncare oro e cambi. | `V-sec` (`tickstory.com` per inizio tick 2003) + [NON VERIFICATO per `.bi5` e indici/WTI/BTC] | Ammettere esplicitamente **coorti temporali stratificate** (o escludere asset senza ≥10 anni comuni omogenei dalla prima ondata D1–D5). |
| 5 | `PIANO-DIVERSIFICAZIONE.md` §Mercati candidati (ordine 1–6) | Ordine: `XAUUSD`, `EURUSD`, `S&P 500`, `XAGUSD`, `GBPUSD`, `USDJPY`, `DAX`, `WTI/Brent`, `BTCUSD` | ⚠️ | Concentrazione eccessiva su uno stesso fattore macro (**USD + tassi reali USA / risk-on**): oro, argento, EURUSD, GBPUSD, USDJPY (inverso), WTI e BTCUSD reagiscono insieme a CPI/NFP/FOMC. Manca un **cross non-USD** (es. `EURJPY`/`EURGBP`) e un tasso/indice asiatico decorrelato prima di replicare major USD. | [STIMA Gemini] + `PIANO-DIVERSIFICAZIONE.md:21-28` | Riorganizzare l'ordine per **ortogonalità di fattore**, inserendo al massimo un cambio USD principale e introducendo un cross non-USD prima di aggiungere `GBPUSD`/`USDJPY`. |
| 6 | `dati/pipeline/dukascopy.py` riga 40 e `PIANO-DIVERSIFICAZIONE.md` riga 36 | Storico solo `BID` con spread/costi aggiunti dopo (`D3`) | ⚠️ | `dukascopy.py:40` scarica solo `BID_candles_min_1.bi5`: per SHORT su `XAUUSD`/FX/CFD l'entrata è su `BID` ma SL/TP chiudono su `ASK`. Applicare spread fisso sottostima sistematicamente l'allargamento a rollover (21:00–22:00 UTC) e su news. Inoltre `engine.py`/`portfolio.py` (stato osservato precedente, da riverificare se esteso in D4) non modellano swap overnight né roll dei CFD su materie prime (`WTI`). | `V` (`dukascopy.py:40`); [NON VERIFICATO su `engine.py` al `43fff60`] | Scaricare anche `ASK_candles_min_1.bi5` (o quantili orari reali `ASK-BID`) e censire swap tripli/rollover prima del backtest multigiornaliero. |
| 7 | `laboratorio/backtester/dsr.py` righe 171–174 e 248–251 vs `DA-28` | "Ogni coppia ipotesi–mercato entra nel DSR (`DSRCalculator`)" | ❌ | Nella formula implementata in `dsr.py:173`, `sr_star` **omette il fattore $\sqrt{V[\widehat{SR}_n]}$** (assumendo implicitamente varianza unitaria degli Sharpe tra le prove), e `evaluate_portfolio` (`dsr.py:248`) calcola lo Sharpe **per trade in PnL**, non su serie temporale allineata; inoltre `DSRCalculator` assume prove indipendenti ($N$ nominale anziché $N_{\text{eff}}$). | `V` (`dsr.py:171-174,248-251`) + `V-sec` (`Bailey & López de Prado 2014`) | Far rivedere e correggere a Claude `dsr.py` (includendo stima di $\sqrt{V[\widehat{SR}_n]}$ dai trial, ritorni su calendario uniforme e stima di $N_{\text{eff}}$) prima della fase D4–D5. |
| 8 | `PIANO-DIVERSIFICAZIONE.md` §Oltre ai prezzi riga 39 & `CONTINUITA.md` | Regole su `Fibonacci` e `order block` prima di guardare i dati | ⚠️ | Definire concetti grafici discrezionali con 4–6 scelte arbitrarie (finestra swing, tolleranza di tocco, body vs wick dell'order block, conferma FVG/struttura) genera decine di micro-iterazioni informali *prima* della registrazione, eludendo il conteggio `N`. | [STIMA Gemini] + `PIANO-DIVERSIFICAZIONE.md:39` | Bloccare **una sola definizione matematica minimale** con al massimo 2 gradi di libertà e senza soglie numeriche ottimizzate ex-post, prima di eseguire il primo run. |

Legenda esito: ✅ confermato · ⚠️ impreciso o da qualificare · ❌ errato · ❓ non verificabile.

---

## 4. Contenuti nuovi proposti (Risposta ai quesiti a, b, c)

### a) DA-26: come dividere i dati (anni totali, sviluppo, verifica) e perché

**Premessa fattuale (cosa sappiamo e cosa NON sappiamo):**
- **Sappiamo dal codice (`dukascopy.py:40-46`)** che il modulo attuale scarica solo candele M1 `BID`, aggrega a 15m UTC, accetta solo `XAUUSD` con `PREZZO_MIN = Decimal("1000")`, e usa `DatasetPartitioner(0.7)` (taglio al 70% delle barre).
- **Non sappiamo da fonte primaria ufficiale Dukascopy** in quale data esatta inizi il feed `BID_candles_min_1.bi5` con copertura affidabile per `XAUUSD` e per gli altri strumenti candidati. Fonti secondarie di tool terzi (`tickstory.com`, `dukascopy-node.app` — stato `V-sec`) riportano l'avvio del feed tick FX e `XAUUSD` intorno al **4–5 maggio 2003**; questo **non garantisce** né la qualità dei volumi/buchi del 2003–2009 sui `.bi5` M1 né la presenza degli indici, petrolio e cripto in quegli anni. Finché la fase D1 non effettuerà un sondaggio reale di testa/coda sul server Dukascopy, le date storiche di copertura per ciascuno strumento restano **non verificate**.

**Perché la divisione «3 anni 70/30 + periodo vecchio come OOS» va corretta:**
1. **3 anni coprono quasi un solo macro-regime sull'oro** (`2023–2026`: tassi alti/tagli e forte rialzo strutturale oltre \$2.000–\$2.700/oz — noto in generale fino al cutoff dell'addestramento, da misurare solo dopo il sigillo sul dataset effettivo). Un campionamento di 3 anni espone al rischio che il bias rialzista o la volatilità di un ciclo dominino ogni test.
2. **Un periodo vecchio (es. 2008–2013) NON è davvero "cieco" né per l'uomo né per gli AI.** Nella memoria pre-addestramento di Claude e Gemini, i grandi movimenti storici dell'oro (picco 2011, crollo aprile 2013, crisi 2008) sono noti **almeno quanto** gli ultimi mesi. Serve a impedire il *visual overfitting* recente dell'utente su M15, ma resta un **holdout di robustezza multi-regime**, non un vero test cieco.
3. **Problema dell'invarianza di scala sul lungo periodo:** tra il 2004 (~350–450 USD/oz, ordine di grandezza storico) e il 2025 (>2.500 USD/oz), il prezzo nominale dell'oro è cambiato di ~5×–7×. Qualsiasi strategia con stop/target in USD fissi fallirà o esploderà per pura non-stazionarietà nominale: ogni regola su serie >5 anni va espressa in **unità adimensionali** (multipli di ATR, percentuale del prezzo o deviazione standard locale), mai in dollari o pip fissi.
4. **Blocco tecnico già nel codice:** `PREZZO_MIN = 1000` (`dukascopy.py:44`) impedirà lo scaricamento automatico di qualunque dato `XAUUSD` anteriore al ~2009–2010.

**Proposta di partizione raccomandata (`[STIMA Gemini]`):**
1. **Lunghezza totale richiesta per XAUUSD (da verificare sul feed reale prima di fissare le date):** almeno **14–16 anni completi** (es. **`2010-01-01` → ieri** se la copertura M1 Dukascopy pre-2010 presenta buchi/spread anomali o finché `PREZZO_MIN = 1000`; oppure **`2007-01-01` → ieri** (~19 anni) previa verifica che la scala $\times 10^{-3}$ e la continuità M1 dal 2007 siano integre e adattando `PREZZO_MIN`).
2. **Divisione obbligatoria per DATE UTC fisse (non per `%` di candele) in 3 partizioni + embargo:**
   - **Blocco A — Holdout Storico Pre-Regime («periodo vecchio», ~4–5 anni):** e.g. **`2007-01-01` → `2012-12-31`** (oppure `2010-01-01` → `2013-12-31` se si parte dal 2010). Contiene il boom 2009–2011 e/o l'inversione 2013. Resta **sigillato con nonce** (`Holdout_Vecchio`).
   - **Embargo A↔B:** **14 giorni di calendario** (scartati in ogni statistica al confine) per annullare la dipendenza seriale di indicatori o posizioni multi-giorno a cavallo del taglio.
   - **Blocco B — Sviluppo & Walk-Forward interno («In-Sample», ~10 anni):** e.g. **`2013-01-15` → `2023-12-15`**. Comprende lateralità post-crollo (2013–2018), pre-COVID (2019), shock liquidità (marzo 2020), inflazione e rialzo tassi (2021–2023). Dentro questo blocco si usano solo fold Walk-Forward o *Purged Cross-Validation* per validare le varianti.
   - **Embargo B↔C:** **14 giorni di calendario**.
   - **Blocco C — Holdout Recente Sigillato (`2024-01-01` → ieri, ~2,8 anni):** già visto sui grafici dall'utente e in addestramento dai modelli. Va declassato esplicitamente da «conferma OOS» a **Filtro Falsificatore Recente dei Costi**: se la strategia fallisce in Blocco C con i costi attuali va scartata; se passa in Blocco C **non aumenta la confidenza**, perché non è cieco.
   - **Blocco D — Test Cieco Autentico:** **solo il futuro** (dati generati *dopo* la data di sigillo dell'ipotesi, in incubazione su conto demo).
3. **Ordine di apertura dei sigilli (regola di condanna irreversibile):**
   - Una variante promossa internamente su Blocco B viene congelata e testata **una sola volta** sul Blocco A (`Holdout_Vecchio`) **e** sul Blocco C (`Recente`). Ogni apertura consuma 1 prova di verifica definitiva su quel sigillo; se fallisce su Blocco A o Blocco C, l'ipotesi muore (non si "ritocca" per ri-testarla sullo stesso holdout).

---

### b) Piano di diversificazione (`PIANO-DIVERSIFICAZIONE.md`, `DA-27`, `DA-28`): errori, rischi, ordine e regole mancanti

**1. Errori e contraddizioni del piano attuale:**
- **Contraddizione tra "stesso calendario" (Regola 1) e paniere eterogeneo (`BTCUSD`, `WTI`, indici):** se Dukascopy non ha `BTCUSD` o `USA500`/`DEU40`/`WTI` dal 2007–2010 (cosa molto probabile — **non verificata**, da appurare in D1), applicare letteralmente "lo stesso calendario per tutti i mercati" obbligherebbe a ridurre anche `XAUUSD` ed `EURUSD` alla finestra breve dell'ultimo arrivato (es. 2017–2026 = 9 anni). Soluzione: mantenere un **calendario di riferimento unico** per il blocco FX+Metalli (14–16+ anni) e trattare eventuali mercati più giovani in una **Coorte 2** separata con identiche date di split recente e incubazione comune, oppure escludere i mercati senza storia sufficiente.
- **Disallineamento `dukascopy.py` vs Regola 1:** `dukascopy.py:237` divide ancora al `0.7` del numero di candele. Asset con sessioni da 14 ore (DAX cassa/estesa), 23 ore (XAUUSD) o 24/7 (`BTCUSD`) producono date `split_time` diverse anche sullo stesso periodo!
- **Sottostima sistematica dei costi e gap da singolo feed `BID` e assenza `swap`/rollover:**
  - `dukascopy.py` scarica solo `BID`. Su indici, argento (`XAGUSD`) e petrolio (`WTI`), lo spread varia enormemente tra sessione principale e apertura asiatica/rollover/news.
  - Nei CFD multiday mancano nel backtester corrente lo **swap overnight** (e triplo swap) e i **salti di rollover dei contratti CFD/futures** su materie prime come `WTI`/`Brent` (richiesto anche da `DA-21`). Una strategia intraday che talvolta tiene overnight può passare da positiva a negativa solo per gli swap.
- **Falla matematica nel `DSRCalculator` prima di `DA-28`:** in `dsr.py:173`, `sr_star` è calcolato senza moltiplicare per $\sqrt{V[\widehat{SR}_n]}$ (la deviazione standard campionaria degli Sharpe osservati tra le $N$ prove, Bailey & López de Prado 2014) e `evaluate_portfolio` usa PnL per trade (`dsr.py:248`), rendendo i confronti di DSR tra mercati a diversa frequenza/ampiezza trade statisticamente distorti prima ancora di introdurre il registro unico (`DA-28`). Inoltre, su 8 mercati testati in sequenza, le prove sugli stessi pattern *non sono indipendenti*: usare $N$ come se fossero indipendenti senza stimare $N_{\text{eff}}$ altera il valore del DSR.

**2. Rischi non visti:**
- **Concentrazione nascosta sul fattore `USD` e crisi di liquidità:** su 9 mercati totali considerati (`XAUUSD`, `EURUSD`, `S&P 500`, `XAGUSD`, `GBPUSD`, `USDJPY`, `DAX`, `WTI/Brent`, `BTCUSD`), 7 dipendono direttamente dal dollaro USA o dal premio al rischio USA. La correlazione media sull'intero decennio (`Regola 5`) nasconde che nei giorni di shock macro (CPI, FOMC, marzo 2020) le correlazioni collassano verso $+1$/$-1$ contemporaneamente (*tail dependence*).
- **Rischio di sfasamento orario e festività (`classifica_buco`):** `dukascopy.py:140-154` classifica i buchi solo per ore `20–23 UTC` e sabato intero. Con `S&P 500`, `DAX` e `WTI` entrano: festività nazionali asincrone, chiusure giornaliere diverse (`21:00–22:00 UTC` vs `22:00–23:00 UTC`), settimane di sfasamento tra ora legale US e EU (marzo e fine ottobre/inizio novembre) dove gli orari di apertura/chiusura cambiano di un'ora in UTC. Applicare una strategia basata su orari UTC fissi senza gestire fusi locali di Borsa (New York / Francoforte / Londra) rompe i backtest su indici e FX.
- **Sovraccarico operativo / paralisi da download ("tempi settimane di notti"):** raccogliere 10 mercati × 15 anni rischia di spostare l'attenzione dall'ipotesi all'infrastruttura di download (contraddicendo il principio *«niente nuova infrastruttura»*!).

**3. Mercati candidati e ordine alternativo proposto (`[STIMA Gemini]`):**
Invece di scaricare 8–10 mercati "a pioggia" subito, proporre **un paniere essenziale a 4–5 fattori ortogonali**, in quest'ordine dopo `XAUUSD` (`D0`):
1. **`EURUSD`:** benchmark liquido FX contro USD, verifica meccanismi di costi e sessione Londra/NY con spread minimo.
2. **`EURJPY` (o `EURGBP`) PRIMA di `GBPUSD`/`USDJPY`:** introduce un cross **privo di gamba diretta USD**, necessario per verificare se un'ipotesi regge fuori dalla dinamica esclusiva del biglietto verde.
3. **`S&P 500` (o altro indice liquido primario, solo dopo verifica orari di sessione + ora legale NY + costi CFD/swap):** secondo fattore strutturale (azionario USA).
4. **`XAGUSD` come puro *test di stress/falsificazione* dell'oro** (dichiarato fin da subito come controllo di robustezza su metallo più sottile/costoso, **non** aggiunto al portafoglio per diversificare).
5. **`DAX` / `GBPUSD` / `USDJPY`:** solo se il nucleo `{XAUUSD, EURUSD, EURJPY, S&P 500}` mostra segnali di robustezza.
6. **`WTI/Brent` e `BTCUSD`: rimossi dal perimetro di prima fase (`[PROPOSTA]`).** Il petrolio richiede gestione rigorosa dei roll mensili/contango (`DA-21`) che il backtester non ha; `BTCUSD` ha regime 24/7, costi/swap molto alti sui CFD MT5 e storia troppo breve per allinearlo agli altri senza accorciare il dataset comune.

**4. Regole mancanti da aggiungere a `PIANO-DIVERSIFICAZIONE.md`:**
- **Regola 7 — Segretezza preventiva cross-asset:** vietato ispezionare statistiche o grafici dei mercati `D2–D5` durante lo sviluppo della prima ipotesi su `XAUUSD`, per non progettare regole "su misura" sapendo già dove funzionano altrove.
- **Regola 8 — Invarianza dimensionale obbligatoria:** ogni parametro di distanza (stop, target, filtro range, tolleranza swing) tra mercati diversi deve essere espresso in unità adimensionali (es. multipli di ATR o deviazione standard locale), mai in punti/pip/USD assoluti.
- **Regola 9 — Correlazione condizionata alle code (non solo media):** in Regola 5 aggiungere la misura della correlazione sui peggiori giorni (`bottom 5%` per rendimento o `top 5%` per ATR) e durante finestre macro ad alto impatto, imponendo che `P-05 = 1,5%` copra in futuro il **rischio di coda congiunto**, non solo la somma lineare dei margini di giornata normale.
- **Regola 10 — Pre-filtro di economicità dei costi (prima del backtest):** prima di consumare prove nel DSR su un mercato nuovo, verificare che `(spread medio + commissione + swap atteso) / ATR(15m o H1)` rientri in una soglia fissata; se i costi mangiano una frazione eccessiva della volatilità media per quel timeframe, il mercato viene scartato *prima* del test strategico.

---

### c) Contromisure contro l'autoinganno (`CONTINUITA.md`, `DA-26`, `REGISTRO-MODIFICHE.md` v1.21): bastano? Cosa manca?

*(Nota di trasparenza: la valutazione riguarda le contromisure esplicitamente riportate nel repository in `DECISIONI-APERTE.md` righe 256–263 e `REGISTRO-MODIFICHE.md` righe 297–305; il testo completo del documento esterno su `claude.ai` non è presente nel repository).*

**Giudizio: NO, non bastano.** Tutte le misure attuali agiscono bene sulla *disciplina formale dei dati* e sul *registro*, ma lasciano aperti **6 canali concreti attraverso cui il *false discovery* e il *data snooping* passano comunque**:

1. **La "replica indipendente Claude/Gemini" controlla il software, NON previene l'overfitting di ipotesi condivise.**
   Se entrambi i modelli implementano una variante proposta dall'utente (es. su Fibonacci + order block) sugli stessi dati già noti nei pesi fino al 2026, ottenere lo stesso output conferma l'assenza di bug (`cross-implementation parity`), ma non aggiunge un solo grado di libertà statistica indipendente. Servono invece **test di permutazione/placebo** (es. randomizzare gli orari di ingresso mantenendo identica la frequenza/durata dei trade, oppure testare sull'inverso/dati sintetici *bootstrap* a blocchi) per misurare se l'effetto è superiore al caso a parità di struttura del segnale.

2. **L'incubazione in conto demo ha bassa potenza statistica e rischia abbandono prematuro o falso negativo.**
   Con rischio per trade `P-01 = 0,5%` (250 USD) e strategie selettive intraday/swing (stima indicativa 1–4 trade/settimana), in 3–6 mesi si raccolgono circa 15–80 trade: un campione insufficiente per dimostrare statistical significance dello Sharpe (come mostrato già dal calcolo di potenza di 594 trade richiamato in `REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md` §4.1). **Cosa manca:** un protocollo pre-registrato a due livelli in incubazione:
   - *livello operativo rapido (primi 20–30 trade):* verifica di **fedeltà esecutiva** (slippage, spread reali al momento del fill, frequenza segnali rispetto al simulato), che invalida subito un backtest irrealistico;
   - *livello statistico di arresto (Sequential Stopping / CUSUM predefinito):* soglie di invalidazione scritte prima per decidere quando fermare una strategia senza aspettare l'esaurimento casuale.

3. **"Fibonacci e Order Block" sono ad altissimo rischio di overfitting silenzioso da ambiguità definitoria (`PIANO-DIVERSIFICAZIONE.md:39`).**
   Prima di toccare i dati, bisogna chiudere l'ambiguità algoritmica completa: regola esatta dei pivot, tolleranza di tocco (`%` ATR), definizione deterministica dell'order block, gestione del multiplo tocco, invalidazione. Lasciare anche solo una regola "a buon senso" mentre si osservano i primi risultati parziali introduce un numero occulto di prove implicite che invalida il DSR.

4. **"Seconda fonte di dati" senza criterio pre-registrato di discordanza.**
   Dukascopy (`BID` ECN) e il feed del broker MT5 demo hanno fusi candela, filtri tick e quote `BID`/`ASK` differenti. Cosa succede se su Blocco B una strategia fa `+1.2R` su Dukascopy e `+0.3R` sul broker MT5? Senza una regola *scritta prima* ("differenza massima tollerata su tasso di segnale, win rate o costo implicito"), il confronto con la seconda fonte rischia di produrre razionalizzazioni a posteriori invece che un vero rifiuto.

5. **File-drawer effect e corse esplorative pre-registro (`DA-19` e `DA-22` ancora aperti).**
   Se l'utente guarda TradingView «a occhio» o un modello fa verifiche rapide «per vedere se ha senso registrare l'ipotesi», quelle prove scartate **non entrano in `trial_registry`**, falsando al ribasso il valore di $N$ nel DSR. Manca una regola operativa dura: **divieto di eseguire qualsiasi script esplorativo o conteggio statistico su dati reali fuori da una `run` che auto-incrementa `trial_registry` prima del calcolo.**

6. **Mancanza del controllo sull'instabilità dei parametri (sensibilità / *plateau check*) e sull'ablation test:**
   Nel pacchetto attuale si passa da un singolo backtest al DSR (`N` prove), ma manca l'obbligo sistematico di:
   - **Ablation study predefinito:** se una strategia usa "Fibonacci + Order Block + Filtro sessione", va testato se ciascun componente migliora effettivamente o se è solo rumore decorativo che aggiunge parametri liberi;
   - **Test di vicinato dei parametri (±20–30%):** un punto isolato profittevole circondato da parametri perdenti è quasi certamente overfitting, anche se supera per caso un singolo check.

---

## 5. Lacune, duplicazioni, contraddizioni trovate

1. **Contraddizione `DA-26` ↔ `DA-27` / `dukascopy.py`:** `DA-26` chiede più anni di storia sull'oro e `DA-27` chiede un calendario unico per tutti i mercati; ma `dukascopy.py:44` blocca sotto `1000` (`XAUUSD` pre-2010), `dukascopy.py:237` divide al `70%` di righe invece che per data fissa `split_time`, e gli asset candidati in `DA-27` (`WTI`, `DAX`, `BTCUSD`) quasi certamente non condividono lo stesso anno di avvio di `EURUSD`/`XAUUSD`.
2. **Contraddizione interna sul `DSR` (`DA-28` vs `dsr.py`):** si affida al `DSRCalculator` il ruolo di gate anti-overfitting multistrumento, mentre `dsr.py:173` omette $\sqrt{V[\widehat{SR}_n]}$ in `sr_star`, calcola Sharpe su singolo trade in USD (`dsr.py:248`) anziché su serie temporale uniforme, e non calcola $N_{\text{eff}}$ per prove correlate.
3. **Duplicazione/slittamento di stato su `Gate 1` vs `DA-25`:** `CONTINUITA.md:109-118` dichiara `Gate 1, chiuso` pur annotando subito dopo «Scheda non riconciliata con la piattaforma (`DA-25`): finché non lo è, la scheda dichiara di non usarne i numeri per decidere». Operativamente conviene distinguere chiaramente `Gate 1 configurato (template demo)` da `Gate 1 riconciliato (pronto per paper trading)` così da non dare per concluso un prerequisito ancora non usabile.
4. **Assenza di riferimento operativo a costi `ASK`, `swap` e festività locali nel `PIANO-DIVERSIFICAZIONE.md`:** elencati come titoli in `§Oltre ai prezzi` (`D3`), ma assenti nei criteri bloccanti delle fasi `D1–D2` e nel motore di backtest (`D4`).

---

## 6. Fonti consultate

### Documenti e codice nel repository (`trading-brain-core`, commit `43fff60`)
- `brain/CONTINUITA.md` — letto integralmente (righe 1–157).
- `brain/collaborazione/LOCK.md` — letto integralmente (righe 1–43).
- `brain/governance/DECISIONI-APERTE.md` — lette righe 200–286 (voci `DA-18`–`DA-28` e fonti).
- `brain/governance/PIANO-DIVERSIFICAZIONE.md` — letto integralmente (righe 1–50).
- `brain/governance/REGISTRO-MODIFICHE.md` — lette righe 200–318 (voci `v1.15`–`v1.22`).
- `brain/dati/pipeline/dukascopy.py` — letto integralmente (righe 1–301).
- `brain/laboratorio/backtester/dsr.py` — lette righe 160–260.
- `brain/dati/reali/demo_broker_mt5_50k_xauusd.toml` — letto integralmente (righe 1–54).

### Fonti esterne consultate (solo riassunti/pagine secondarie via ricerca web — nessuna lettura del paper PDF completo né interrogazione dei server Dukascopy)
- **Bailey, D. H. e López de Prado, M. (2014)**, *"The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality"*, *The Journal of Portfolio Management*, Vol. 40, No. 5, pp. 94–107. Verificata la formula di $\mathbb{E}[\max \widehat{SR}_n]$ con il fattore $\sqrt{V[\widehat{SR}_n]}$ tramite riassunti tecnici consultati (`marti.ai`, `semanticscholar.org`, `davidhbailey.com`, stato `V-sec`).
- **McLean, R. D. e Pontiff, J. (2016)**, *"Does Academic Research Destroy Stock Return Predictability?"*, *The Journal of Finance*. Verificati i numeri principali tramite summary accademico (`abfer.org`, `repec.org`: calo medio post-pubblicazione del 58%, calo out-of-sample pre-pubblicazione del 26%, stato `V-sec`).
- **Copertura storica Dukascopy:** consultato riassunto di tool terzi (`tickstory.com`, `dukascopy-node.app`: avvio feed tick per `EURUSD` e `XAUUSD` indicato al 4–5 maggio 2003, stato `V-sec`; **non verificato** né sul feed binario `.bi5` M1 BID né per indici, petrolio e cripto).

---

## 7. Limiti del rapporto
1. **Nessun accesso al documento esterno *«Trading Brain — Progetto generale»*** su `claude.ai`: le valutazioni sul punto (c) si basano esclusivamente sulle contromisure sintetizzate nel repository (`CONTINUITA.md`, `DECISIONI-APERTE.md`, `REGISTRO-MODIFICHE.md`). Eventuali protocolli aggiuntivi presenti solo in quel documento non sono stati esaminati.
2. **Nessuna verifica diretta sul feed Dukascopy né sui dati reali:** per vincolo operativo esplicito non è stato lanciato `dukascopy.py` né letto alcun dato storico; tutte le osservazioni su date di inizio, scala storica pre-2010, qualità dei buchi e disponibilità per indici/materie prime/cripto vanno verificate empiricamente con richieste di prova in fase `D1`.
3. **Ispezione parziale al commit `43fff60`:** del modulo `engine.py`/`portfolio.py` è stata esaminata l'assenza storica di modelli di swap/rollover nello stato precedente del Binario B; tali file non sono stati riletti integralmente dopo la presa in carico di Claude (`43fff60`), e lo stesso vale per `test_dukascopy.py`.
4. **Fonti accademiche in stato `V-sec`:** le formule ed evidenze di Bailey & López de Prado (2014) e McLean & Pontiff (2016) sono state verificate tramite abstract/summary web, non sul testo integrale dei PDF originali.
