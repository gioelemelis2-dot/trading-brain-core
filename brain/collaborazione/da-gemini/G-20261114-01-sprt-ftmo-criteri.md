---
id: G-20261114-01
autore: gemini
data: 2026-11-13
tipo: revisione-e-proposte
oggetto: Revisione critica SPRT/DA-29, verifica FTMO Standard vs Swing su fonti primarie e proposte D3 (Dukascopy-MT5) e demo->FTMO
commit_esaminato: 408ba3f
file_esaminati:
  - brain/laboratorio/studi/simulazione_sprt.py
  - brain/governance/DECISIONI-APERTE.md
  - brain/governance/PIANO-DIVERSIFICAZIONE.md
  - brain/guardian/regole/prop_firm_ftmo.toml
  - brain/guardian/regole/fonti/FTMO_REGOLE_ESTRATTO_20261112.txt
  - brain/guardian/regole/regole_personali.toml
richiesta_di_origine: "Richiesta utente 2026-11-13 (rapporto G-20261114-01): 1) revisione simulazione_sprt.py e DA-29; 2) regole FTMO primarie vs prop_firm_ftmo.toml; 3) proposte Dukascopy-MT5 e passaggio demo->FTMO"
---

# Rapporto G-20261114-01 — Revisione SPRT (`DA-29`), verifica fonti primarie FTMO e proposte operative

## 1. Sintesi (max 5 righe)

In `simulazione_sprt.py` formule di Wald e formula browniana FTMO sono matematicamente esatte (`A=2.7726`, `B=-1.5581`, FTMO `88.1%/98.2%/73.1%` verificati), ma emergono tre limiti critici: (1) a `N_MAX=600` la potenza reale è `64.3%` (`β_eff = 35.7%` con `18.6%` indecisi); (2) con `σ > 1R` (`N_MAX` fisso) gli indecisi esplodono all'`84%` a `σ=2R`, mentre con perdite a grappoli i falsi arresti saltano al `41.2%`; (3) la simulazione FTMO ignora il limite giornaliero del `5%`. Sulle pagine ufficiali `ftmo.com` (13/11/2026) tutte le regole `2-Step` coincidono con `prop_firm_ftmo.toml`, ma mancano dettagli chiave di **Standard vs Swing** (break `> 2h`, news `±2 min` inclusi SL/TP su `XAUUSD`, leva `1:100` vs `1:30`, applicazione a 1-Step/Instant). Chiudono il rapporto due proposte numerate pronte per D3 e per il passaggio demo → FTMO.

---

## 2. Metodo

1. Operato esclusivamente sul worktree separato `../tb-gemini` (ramo `rev/gemini-20261114` da `origin/main` `408ba3f`), senza toccare `/Users/gioele/Downloads/trading-brain-core` né fare alcuna richiesta a Dukascopy né leggere dati storici/nonce.
2. Eseguito `simulazione_sprt.py` e condotto un ricalcolo indipendente in Python (formule ASN di Wald, equazione delle barriere browniane, simulazione con `σ ∈ {1.0, 1.5, 2.0}R` e processo Markov a 2 stati per il clustering delle perdite).
3. Consultate direttamente le pagine ufficiali `ftmo.com` (2-Step, Trading Objectives, e 4 pagine FAQ ufficiali), confrontando riga per riga con `brain/guardian/regole/prop_firm_ftmo.toml` e segnalando esplicitamente ciò che non è leggibile in HTML statico (`ftmo.com/en/symbols/` renderizzato via JS).
4. Redatte proposte operative numerate per discordanza Dukascopy–MT5 e criteri minimi demo → FTMO coerenti con `P-01..P-14` e `DA-26..DA-29`.

---

## 3. Rilievi

| ID | Gravità | Ambito | Problema o osservazione | Risoluzione / Azione richiesta | Stato |
|---|---|---|---|---|---|
| G5-01 | **ALTO** | `simulazione_sprt.py`, `DA-29` | Con `σ > 1R` (es. setup R:R 1:3) ricalcolando solo le soglie (`∝ σ²`) e lasciando `N_MAX = 600`, lo SPRT paralizza: con `σ = 1.5R` gli indecisi salgono al **`60.1%`** (`26.9%` promozioni); con `σ = 2.0R` gli indecisi raggiungono l'**`84.0%`** (`7.8%` promozioni). | Normalizzare la somma `S_n` rispetto a un target in Sharpe per trade (`θ₁ = μ₁/σ_OOS`) oppure scalare `N_MAX` proporzionalmente a `σ²` entro un tetto dichiarato, fissando `σ_OOS` dal backtest (mai sui primi 20–30 trade demo). | PROPOSTO |
| G5-02 | **ALTO** | `simulazione_sprt.py`, `DA-29` | Perdite a grappoli violano l'ipotesi i.i.d. di Wald: in un processo a 2 regimi con `μ = +0.10R` e varianza non condizionata `1R²` (`p_stay = 0.85`), i falsi arresti salgono al **`41.2%`** (vs `17.1%` i.i.d.). | Sostituire `σ²` nell'LLR con la **Long-Run Variance** (`VIF × σ²`, via Newey–West o varianza su blocchi OOS) e introdurre un **burn-in di 30–50 trade** prima dell'arresto SPRT (lasciando a `P-05` la protezione del rischio iniziale). | PROPOSTO |
| G5-03 | **MEDIO** | `DA-29#L320-L329` | Il troncamento a `600` trade porta la mancata promozione sotto `H₁` (`+0.10R`) dal `20%` nominale al **`35.7%`** (`17.1%` fermata + `18.6%` indecisa), anche se 600 trade resta un tetto temporale sensato (`~4` anni a 3 trade/sett.). | Dichiarare esplicitamente in `DA-29` che `β = 20%` vale asintoticamente (`ASN₁ ≈ 381`), mentre a 600 trade la potenza effettiva è `~64%`. | PROPOSTO |
| G5-04 | **MEDIO** | `simulazione_sprt.py#L9, L46-L59` | La stima FTMO Fase 1 (`88.1%`, `98.2%`, `73.1%`) è un **limite superiore ottimistico**: ignora la regola più restrittiva (`Max Daily Loss 5%` su equity), ignora i toccamenti **intrabarra** dell'equity e assume trade gaussiani i.i.d. | Integrare una simulazione con calendario giornaliero, `Max Daily Loss 5%` e asimmetria `R` prima di stimare la probabilità reale di superare FTMO. | PROPOSTO |
| G5-05 | **MEDIO** | `DA-29#L319` | Il controllo di fedeltà nei primi 20–30 trade cita "segnali, prezzi di ingresso, spread, slippage", ma non vieta esplicitamente di giudicare il PnL/win-rate in quella finestra (`±0.45R` di errore standard in 20 trade). | Specificare per iscritto in `DA-29` che i primi 20–30 trade valutano **esclusivamente la fedeltà meccanica e dei costi**, mai il PnL o la qualità statistica dell'edge. | PROPOSTO |
| G5-06 | **MEDIO** | `prop_firm_ftmo.toml#L62-L66, L69-L106` | Rispetto alle FAQ ufficiali `ftmo.com` lette il 13/11/2026: in `prop_firm_ftmo.toml` mancano (1) regola dei **market break > 2h** e finestra news **±2 min** (inclusi **SL/TP/pending**, `XAUUSD` incluso negli eventi USD!), (2) leva **`1:100` vs `1:30`** e **irreversibilità Standard → Swing**, (3) applicazione di entrambe le restrizioni a **`ftmo_1step` e `ftmo_instant`** (dove Swing non esiste). | Aggiornare `prop_firm_ftmo.toml` da `V-parziale` a `V` con i campi estratti dalle 4 pagine FAQ ufficiali (Sezione 4.2) e verificare su MT5/cTrader gli orari di `XAUUSD` non leggibili su `symbols/` JS. | APERTO |

---

## 4. Contenuti nuovi proposti

### 4.1 Compito 1 — Revisione critica di `simulazione_sprt.py` e di `DA-29`

#### A. Verifica indipendente di formule, soglie e simulazione

Eseguendo `python3 -s -B brain/laboratorio/studi/simulazione_sprt.py` e un calcolo indipendente con script Python separato (`seed=42`, formule chiuse):

1. **Soglie di Wald (`simulazione_sprt.py:21, 28, 64-65`):**
   - $A = \ln\frac{1-\beta}{\alpha} = \ln\frac{0.80}{0.05} = \ln(16) = 2.772589$
   - $B = \ln\frac{\beta}{1-\alpha} = \ln\frac{0.20}{0.95} = \ln(4/19) = -1.558145$
   - Per $X_i \stackrel{iid}{\sim}\mathcal{N}(\mu, \sigma^2)$, $H_0:\mu=0$ vs $H_1:\mu=\mu_1=0.10$, con $S_n=\sum_{i=1}^n X_i$:
     $$\Lambda_n = \frac{\mu_1}{\sigma^2}\left(S_n - \frac{n\mu_1}{2}\right)$$
     che con $\sigma = 1R$ dà esattamente le due rette:
     - arresto se $S_n \le \frac{\sigma^2}{\mu_1}B + \frac{\mu_1}{2}n = -15.581446 + 0.050\,n$ (`-15.58 + 0.050 n` nel codice, `-15,6 + 0,05 × n` in `DA-29`);
     - promozione se $S_n \ge \frac{\sigma^2}{\mu_1}A + \frac{\mu_1}{2}n = +27.725887 + 0.050\,n$ (`27.73 + 0.050 n` nel codice, `+27,7 + 0,05 × n` in `DA-29`).
   - **Verdetto formule SPRT:** **ESATTE**.
2. **ASN teorico e troncamento a 600 trade:**
   - Formula teorica di Wald (senza troncamento né overshoot): $KL_1 = +0.005$, $KL_0 = -0.005$; quindi $\mathbb{E}_0[N] \approx \frac{0.95(-1.558145)+0.05(2.772589)}{-0.005} = 268.32$ trade; $\mathbb{E}_1[N] \approx \frac{0.80(2.772589)+0.20(-1.558145)}{+0.005} = 381.29$ trade.
   - Con troncamento a `600`: `simulazione_sprt.py` (`6000` seq.) ottiene sotto $\mu=0.10R$: `64.3%` promossa, `17.1%` fermata, `18.6%` indecisa, `348` trade medi (il nostro controllo indipendente con `seed=42`, `4000` seq.: `63.7%`, `17.8%`, `18.5%`, `349` trade medi).
   - **Critica sul troncamento (`G5-03`):** `600` trade ha senso pratico per non attendere oltre ~4 anni a 3 trade/settimana, **ma** taglia la potenza effettiva al `64.3%` (`β_eff = 35.7%` includendo le indecise). Va chiarito in `DA-29` che `β = 20%` non è raggiunto entro 600 trade.
3. **Formula FTMO Fase 1 (`simulazione_sprt.py:46-49`):**
   - Ricalcolo indipendente dall'equazione del moto browniano con deriva $\mu$ fra barriere assorbenti $\pm a$: $P(+a \text{ prima di } -a) = \frac{1}{1 + e^{-2\mu a/\sigma^2}}$.
   - Per `rischio = 0.5%` ($a = 20R$): $\mu=0 \to 50.0000\%$, $\mu=0.05R \to 88.0797\%$, $\mu=0.10R \to 98.2014\%$. Per `rischio = 1.0%` ($a = 10R$): $50.0000\%$, $73.1059\%$, $88.0797\%$.
   - **Coincide esattamente** con i valori stampati da `simulazione_sprt.py` (`50.0% / 88.1% / 98.2%` e `50.0% / 73.1% / 88.1%`), **ma** è un limite superiore ottimistico (`G5-04`) perché ignora il limite giornaliero del `5%` sull'equity, gli overshoot intratrade dell'equity e code/grappoli.

#### B. Come trattare `σ ≠ 1R` e perdite a grappoli (verificato con simulazione indipendente)

| Scenario | Risultato osservato (`N=4000`, `μ=+0.10R`, `N_MAX=600`) | Conseguenza critica |
|---|---|---|
| Base i.i.d. `σ = 1.0R` | Promossa `63.7%` · Fermata `17.8%` · Indecisa `18.5%` (`349` trade medi) | Coerente con `simulazione_sprt.py` (`64.3%`) |
| `σ = 1.5R`, soglie ricalcolate `[-35.1, +62.4]` | Promossa **`26.9%`** · Fermata `13.0%` · Indecisa **`60.1%`** (`509` trade medi) | Soglie ×2.25 → quasi inutile in 600 trade |
| `σ = 2.0R`, soglie ricalcolate `[-62.3, +110.9]` | Promossa **`7.8%`** · Fermata `8.2%` · Indecisa **`84.0%`** (`569` trade medi) | Soglie ×4 → paralisi totale dello SPRT |
| Perdite a grappoli (`σ = 1R`, 2 regimi `p_stay = 0.85`) | Promossa `56.7%` · Fermata **`41.2%`** · Indecisa `2.1%` | Falsi arresti più che raddoppiati (`17.1% → 41.2%`) |

**Proposte operative:**
1. **Per `σ ≠ 1R`:** non lasciare fisso sia `μ₁ = 0.10R` sia `N_MAX = 600`. Due alternative pulite:
   - *Opzione raccomandata:* fissare l'ipotesi alternativa sullo **Sharpe per trade standardizzato** $\theta_1 = \mu_1 / \sigma_{\text{OOS}} \approx 0.10$ (così una strategia con $\sigma = 2R$ punta a $\mu_1 = +0.20R$ mantenendo lo stesso orizzonte `~350–600` trade); se invece il target resta fisso a `+0.10R`, scalare `N_MAX(σ) = min(1500, ceil(600 · σ²))`.
   - Stimare $\sigma_{\text{OOS}}$ **dal backtest prima di aprire la demo** (mai stimarla sui primi trade live). Se la strategia ha asimmetria marcata (`R:R >= 1:2`), valutare LLR su rendimenti winsorizzati o per blocchi invece del modello gaussiano puro.
2. **Per perdite a grappoli:**
   - Calcolare nel backtest OOS la **Long-Run Variance** $\sigma_{\text{LR}}^2 = \text{VIF} \cdot \sigma^2$ (stimatore Newey–West oppure varianza di somme su blocchi disgiunti di $k = 5\text{--}10$ trade divisa per $k$) e usare $\sigma_{\text{LR}}^2$ al posto di $\sigma^2$ in $\Lambda_n$, oppure eseguire lo SPRT direttamente sulle **somme settimanali/a blocchi**;
   - Introdurre un **burn-in minimo di 30–50 trade** prima di applicare l'arresto statistico SPRT (mentre il solo limite di rischio `P-05` resta sempre attivo).
3. **Controllo fedeltà 20–30 trade (`G5-05`):** limitarlo rigorosamente a **segnali, timing, spread, slippage e costi**, escludendo per scritto qualsiasi valutazione di PnL medio o win-rate nei primi 30 trade.

---

### 4.2 Compito 2 — Fonti primarie FTMO vs `brain/guardian/regole/prop_firm_ftmo.toml`

Consultate direttamente il `2026-11-13` (nessuna fonte secondaria):
- [U1] `https://ftmo.com/en/trading-objectives/`
- [U2] `https://ftmo.com/en/2-step-challenge/`
- [U3] `https://ftmo.com/en/faq/what-is-the-swing-account-type-and-how-does-it-work/`
- [U4] `https://ftmo.com/en/faq/can-i-hold-positions-overnight-or-over-the-weekend/`
- [U5] `https://ftmo.com/en/faq/can-i-trade-news/`
- [U6] `https://ftmo.com/en/faq/what-are-the-account-specifications/`

#### Citazioni testuali chiave dalle fonti primarie
- **Standard vs Swing (`U3`, `U6`):**
  - `U3`: *"Account type changes the account’s leverage, the rule for holding trades during market close, and the rule for news trading."*
  - `U3`: *"Compared to the Standard account type, the FTMO Swing account type have: No restrictions on trading during restricted news releases or holding positions past market close for more than 2 hours (e.g., over the weekend or overnight for equities), provided you avoid Forbidden Trading Practices. However, the account’s base leverage is reduced from 1:100 to 1:30."*
  - `U3`: *"The FTMO Swing account type is available exclusively within the 2-Step FTMO Challenge product. It is not offered for the 1-Step FTMO Challenge or the FTMO Instant Account."*
  - `U3`: *"You can request a change from a Swing account type to a Standard account type. We can process this change only for accounts with no trades... You may not change from the Standard account type to the Swing account type."*
  - `U6`: *"The leverage we offer for the Standard type account is up to 1:100 and cannot be increased. The Swing account type has leverage set to up to 1:30."*
- **Overnight & Weekend (`U4`):**
  - `U4`: *"FTMO restricts holding positions through market breaks longer than 2 hours for all accounts, excluding the exceptions mentioned below. You must close all open positions before the break begins. Violating this rule may result in termination of an FTMO Account / FTMO Instant Account."*
  - `U4`: *"This restriction does not apply to: any Swing type accounts / any accounts in the FTMO Challenge or Verification"*
- **News Trading (`U5`):**
  - `U5`: *"FTMO restricts order execution for 2 minutes before and 2 minutes after selected news releases for all accounts, excluding the exceptions mentioned below. You are allowed to hold open positions on the targeted instruments if they were opened more than 2 minutes before the restricted event. This restriction applies to any order execution, including your Stop Loss, Take Profit or any other pending orders. Violating this rule may result in termination of an FTMO Account / FTMO Instant Account."*
  - `U5`: *"This restriction does not apply to: any Swing type accounts / any accounts in the FTMO Challenge or Verification phase."*
  - `U5` tabella strumenti mirati **USD**: *"Forex pairs with the USD currency involved / Gold (XAUUSD) / US Indices (US2000.cash, US500.cash, US100.cash, US30.cash) / DXY"* su *"Federal Funds Rate & Statement, Non-Farm Employment Change, Unemployment Rate & Wages, Advance GDP q/q, FOMC Meeting Minutes, CPI y/y"* (e analoghe tabelle per EUR, GBP, CAD, AUD, NZD, CHF, Crude Oil).

#### Tabella di confronto con `prop_firm_ftmo.toml`

| Voce / Regola | Fonti primarie `ftmo.com` (13/11/2026) | `prop_firm_ftmo.toml` | Esito confronto |
|---|---|---|---|
| **2-Step Profit Target** | `10%` Challenge, `5%` Verification, assente su FTMO Account (`U1`, `U2`) | `0.10`, `0.05`, `"assente"` | **Coincide** |
| **2-Step Max Daily Loss** | `5%` del capitale iniziale, ricalcolato `00:00 CE(S)T` su `balance`, controllo su `equity` (`U1`) | `0.05`, stessa formula e `CE(S)T` | **Coincide** |
| **2-Step Max Loss** | `10%` statico su capitale iniziale, controllo su `equity` (`U1`) | `0.10`, `"statico"` | **Coincide** |
| **2-Step Min Trading Days & Periodo** | `4` giorni (`00:00:00–23:59:59 CE(S)T`, almeno 1 posizione aperta), assente su FTMO Account; periodo `Unlimited` (`U1`, `U2`) | `4`, `"illimitato"` | **Coincide** |
| **Overnight / Weekend (Standard vs Swing)** | Divieto di posizioni attraverso **market break > 2 ore** su `FTMO Account` / `Instant` Standard; **nessun divieto** su Swing e durante Challenge/Verification (`U4`). Su FX/XAUUSD il rollover ordinario feriale non è vietato *in quanto tale* se < 2h, ma lo diventano weekend, festività/chiusure anticipate e azioni/indici > 2h. | Solo nota generica `V-parziale`: *"dettagli da verificare: pagine FAQ non lette"* (`L62-66`) | **Lacuna in TOML** |
| **News trading** | Finestra **`±2 minuti`** su **qualsiasi esecuzione ordini (inclusi SL, TP e pending)** sugli strumenti target (incluso **`XAUUSD`** per news USD!) su FTMO Account / Instant Standard; consentito tenere posizioni aperte `> 2 min` prima se non chiudono nella finestra; **nessun divieto** su Swing e Challenge/Verification (`U5`). | Solo nota `V-parziale`, dettagli assenti (`L62-66`); in `regole_personali.toml` P-08 impone `15 min` sugli ingressi. | **Lacuna in TOML** (e attenzione su **SL/TP** su conto Standard!) |
| **Leva e cambio tipo conto** | Standard `up to 1:100`, Swing `up to 1:30` (solo 2-Step); `Swing → Standard` solo con 0 trade, **`Standard → Swing` impossibile** (`U3`, `U6`). | **Assente** in `prop_firm_ftmo.toml` | **Manca in TOML** |
| **Applicazione a 1-Step / Instant** | Sia market break > 2h sia news ±2 min si applicano anche ad FTMO Account (1-Step) e FTMO Instant (`U4`, `U5`), dove Swing **non esiste** (`U3`). | Presente solo sotto `[prodotti.ftmo_2step.tipo_conto]` | **Manca in 1-Step/Instant** |
| **Fuso server vs FTMO + Forbidden Practices** | MT4/MT5 server `GMT+2 +DST` vs reset giornalieri `00:00 CE(S)T` (`U6`, `U1`); richiamo a *Forbidden Trading Practices* (`U3-U5`). | Fuso server MT4/MT5 non annotato; *Forbidden Practices* assente. | **Integrazione utile** |
| **Orari e leva puntuale di `XAUUSD`** | `https://ftmo.com/en/symbols/` ha tabella **caricata via JavaScript** non leggibile via HTML statico (`U6` rinvia al terminale MT5 o pagina `Symbols`). | In `demo_broker` va verificata sul broker | **Non verificato nelle fonti statiche — da leggere in MT5/browser** |

---

### 4.3 Compito 3 — Due proposte scritte prima di guardare i dati

#### 3(a) Criterio scritto di discordanza Dukascopy vs storico MT5 del broker (Fase D3)

*Principio:* confrontare solo barre sovrapposte sullo stesso intervallo temporale UTC (escludendo finestre di manutenzione note e i minuti intorno al rollover giornaliero `21:00–23:00 UTC`), dopo avere allineato il fuso `GMT+2 +DST` di MT5 a UTC e controllato che entrambe le serie rappresentino il lato **BID**.

| Misura (su 15m in orario attivo comune) | Soglia PASS | Soglia WARN (indagine prima di decidere) | Soglia FAIL (blocco) |
|---|---|---|---|
| **Copertura candele valide** | Scarto conteggio `<= 0.5%`, `0` buchi `> 1h` su una sola fonte | Scarto `0.5%–1.5%` o 1–2 micro-buchi spiegabili da manutenzione | Scarto `> 1.5%` o buco `> 1h` in sessione su una sola fonte |
| **Differenza livelli `\|close_MT5 - close_Duka\|`** | Mediana `<= 0.5 × spread_med_MT5`; p99 `<= 2.0 × spread_med_MT5 + 0.05%` | Mediana `0.5–1.0 × spread_med_MT5` | Mediana `> 1.0 × spread_med_MT5` o p99 `> 0.15%` fuori rollover |
| **Bias direzionale `media(close_MT5 - close_Duka)`** | `\|media\| <= 0.3 × spread_med_MT5` | `0.3–0.6 × spread_med_MT5` | `\|media\| > 0.6 × spread_med_MT5` (sospetto BID vs MID) |
| **Correlazione rendimenti 15m (`r = close/open - 1`)** | Pearson `>= 0.98` | `0.95 <= r < 0.98` | **`r < 0.95`** (sospetto fuso orario, DST o scala) |
| **Scarto ATR(14) mediano 15m** | `\|ATR_MT5 / ATR_Duka - 1\| <= 5%` | `5%–10%` | **`> 10%`** |

**Cosa succede se non torna:**
1. **FAIL su copertura, correlazione `< 0.95`, bias sistematico o ATR `> 10%`:** blocco automatico del pipeline (`ErroreDiscordanza`). Non si esegue alcun backtest su nessuna strategia finché non è identificata la causa tecnica (DST/fuso, unità `SCALA`, feed BID vs MID, festività locale).
2. **WARN persistente o discordanza legittima di micro-liquidità:** Dukascopy resta utilizzabile solo per test strutturali su timeframe `>= 15m` con stop larghi (`>= 10 × spread_med`), ma **non è fonte unica valida**: parametri, filtri di ingresso e costi vanno ri-eseguiti e superati integralmente sullo **storico MT5 del broker** prima di qualsiasi promozione in demo.

#### 3(b) Condizioni minime per passare da demo a FTMO (con `+0.10R` ≈ 350 trade medi in SPRT)

Poiché un singolo setup a `3` trade/settimana richiederebbe `> 2` anni per raggiungere 350 trade in demo da solo, il passaggio non può basarsi né su 20 trade in demo (rumore puro) né sull'attesa paralizzante di 600 trade per ogni singola strategia. Proposta a **Due Chiavi**:

1. **Chiave 1 — Prova statistica nel backtest (obbligatoria prima della demo):**
   - `DSR >= 0.95` sul blocco di sviluppo con **tutte le prove contate** (DA-28) e verifica OOS coerente sui blocchi sigillati (`DA-26`);
   - Superamento di permutation test, ablation e stabilità parametri `±20–30%` (`DA-29`);
   - Simulazione FTMO completa (includendo **`Max Daily Loss 5%`**, weekend chiuso e asimmetria R reale) con probabilità di superamento Fase 1 `>= 80%` al rischio `P-01 = 0.5%`.
2. **Chiave 2 — Semaforo verde in conto demo MT5 (Gate operativo prima di FTMO):**
   - **Fedeltà meccanica e dei costi (obbligatoria per OGNI strategia: `>= 30` trade live e `>= 4` settimane):**
     - corrispondenza segnali demo vs replay del backtest sugli stessi dati MT5 `>= 95%`;
     - costo medio reale `(spread + commissione + slippage)_demo <= 1.25 × costo_assunto_backtest`, e il backtest ri-eseguito con i costi effettivi misurati in demo mantiene `expectancy >= +0.05R` netti e `DSR >= 0.95`;
     - **0 violazioni non spiegate** di `P-01..P-14` (`regole_personali.toml`).
   - **Conferma statistica sequenziale (senza falsi arresti):**
     - nessuna strategia deve essere stata **fermata** dallo SPRT;
     - **Via principale (portafoglio `K >= 3` strategie indipendenti, come previsto in `DA-29`):** ciascuna strategia ha completato la fedeltà (`>= 30` trade ciascuna, `>= 90–150` trade live complessivi su `>= 8–12` settimane), lo SPRT aggregato di portafoglio è in territorio positivo (`LLR > 0`, mai sotto zero netto su `>= 100` trade aggregati) e il CUSUM non segnala degrado;
     - **Via alternativa (strategia singola, se si vuole partire prima di avere 3 strategie):** almeno `>= 100` trade live con fedeltà approvata e `LLR > 0` (oppure promozione piena `LLR >= A`), **con size ridotta a `0.25%` per trade su FTMO** finché il cumulato forward non supera `LLR >= A`.
3. **Coerenza operativa FTMO prima dell'acquisto:**
   - Se le strategie rispettano `weekend chiuso` e non toccano finestre news `±2 min` (garantito da `P-08 = 15 min` sugli ingressi **e** verificando se posizioni aperte con SL/TP possano scattare nei `±2 min` sulle news USD di `XAUUSD`!), è idoneo il conto **Standard (1:100)**; se un'ipotesi prevede posizioni con SL/TP attivi durante news target USD o possibili break `> 2h` (es. festività/indici), è obbligatorio scegliere **FTMO Swing (1:30)** all'acquisto (`Standard → Swing` è irreversibile).

---

## 5. Lacune, duplicazioni, contraddizioni trovate

1. **Contraddizione parziale fra `P-08` (`regole_personali.toml:90-93`) e regola news FTMO:** `P-08` vieta l'*ingresso* entro `15` minuti attorno alle news ad alto impatto, ma sul conto **FTMO Account Standard** FTMO sanziona **qualsiasi esecuzione ordini — inclusi SL e TP — nei `±2 minuti`**, anche per posizioni aperte `> 2` minuti prima! Se una strategia su `XAUUSD` tiene posizioni intraday aperte attraverso l'uscita di NFP/CPI/FOMC e tocca lo SL in quei 4 minuti, rischia la chiusura del conto Standard (non in Challenge/Verification, ma sull'FTMO Account finanziato sì!).
2. **Stato `V-parziale` superato:** `prop_firm_ftmo.toml` può essere aggiornato a `V` sulle regole Standard/Swing grazie alle pagine FAQ ufficiali lette il `2026-11-13`, lasciando solo i dettagli per simbolo (`XAUUSD` trading hours / margin specs via JS su `ftmo.com/en/symbols/`) da leggere in MT5/browser.

---

## 6. Fonti consultate

1. Repository `origin/main` (`408ba3f`) su worktree `../tb-gemini`: `simulazione_sprt.py`, `DECISIONI-APERTE.md`, `PIANO-DIVERSIFICAZIONE.md`, `prop_firm_ftmo.toml`, `FTMO_REGOLE_ESTRATTO_20261112.txt`, `regole_personali.toml`.
2. Fonti primarie `ftmo.com` lette direttamente il `2026-11-13`:
   - `https://ftmo.com/en/trading-objectives/`
   - `https://ftmo.com/en/2-step-challenge/`
   - `https://ftmo.com/en/faq/what-is-the-swing-account-type-and-how-does-it-work/`
   - `https://ftmo.com/en/faq/can-i-hold-positions-overnight-or-over-the-weekend/`
   - `https://ftmo.com/en/faq/can-i-trade-news/`
   - `https://ftmo.com/en/faq/what-are-the-account-specifications/`
3. Output diretti di `python3 -s -B brain/laboratorio/studi/simulazione_sprt.py` e script di verifica indipendente Python.

---

## 7. Limiti del rapporto

- Le specifiche puntuali per simbolo su `https://ftmo.com/en/symbols/` (es. orari esatti di negoziazione e leva effettiva specifica su `XAUUSD`, se diversa dal massimo `1:100` / `1:30` dichiarato per categoria) sono renderizzate via JavaScript e **non erano estraibili da HTML statico**: vanno verificate direttamente nel terminale MT5/cTrader FTMO o via browser prima della fase demo/challenge.
- Nessun file fuori da `brain/collaborazione/da-gemini/` modificato; nessuna richiesta effettuata a Dukascopy; nessun dato storico o nonce letto.
