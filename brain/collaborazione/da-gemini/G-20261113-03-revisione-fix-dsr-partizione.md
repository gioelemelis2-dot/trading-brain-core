---
id: G-20261113-03
autore: gemini
data: 2026-11-13
tipo: revisione
oggetto: Revisione dura di fix/dsr-e-partizione-date (commit 2d16a46) — Parte 3b e verifica ESITI.md
commit_esaminato: 2d16a46
file_esaminati:
  - brain/laboratorio/backtester/dsr.py
  - brain/laboratorio/tests/test_dsr_scala.py
  - brain/dati/pipeline/dukascopy.py
  - brain/dati/pipeline/partizione_date.py
  - brain/dati/pipeline/partitioning.py
  - brain/dati/tests/test_dukascopy.py
  - brain/dati/tests/test_partizione_date.py
  - brain/dati/tests/mutazioni_dsr_partizione.py
  - brain/collaborazione/da-claude/ESITI.md
  - brain/CONTINUITA.md
  - brain/governance/DECISIONI-APERTE.md
  - brain/governance/PIANO-DIVERSIFICAZIONE.md
  - brain/governance/REGISTRO-MODIFICHE.md
richiesta_di_origine: "Richiesta utente 2026-11-13: Parte 3b revisione dura del ramo fix/dsr-e-partizione-date (2d16a46)"
---

# Rapporto G-20261113-03 — Revisione dura di `fix/dsr-e-partizione-date` (`2d16a46`)

## 1. Sintesi (max 5 righe)

Sul worktree di `origin/fix/dsr-e-partizione-date` (`2d16a46`), la correzione principale del DSR coincide con tutti i **30/30 vettori indipendenti** di `G-20261113-02` entro `1.11e-16`, e superano in locale **63/63** test `dati+laboratorio`, **77/77** test `guardian` e **26/26** mutanti su Python `3.9.6`. Tuttavia la revisione ha scoperto **2 bug di gravità ALTA** (riprodotti empiricamente: `calculate_dsr_analytical(float('nan'), ...)` restituisce `DSR = 1.0`; `partizione_date.verifica()` restituisce `valido = True` se si cambia `"ruolo"` in `"sviluppo"` in `commitment.json` usando un nonce falso) e **3 bug/lacune MEDI** su `dukascopy.py` e `dsr.py`. Si sconsiglia il merge su `main` finché almeno i due rilievi `ALTO` non saranno corretti.

---

## 2. Metodo

1. Eseguito `git fetch origin` e montato il worktree separato `../tb-revisione-claude` su `origin/fix/dsr-e-partizione-date` (`2d16a46`), senza modificare alcun file del ramo di Claude né leggere file di dati reali o nonce.
2. Letto per intero il diff `ce82dbf..2d16a46` su codice sorgente, test, mutation testing e documenti di governance (`ESITI.md`, `CONTINUITA.md`, `DECISIONI-APERTE.md`, `PIANO-DIVERSIFICAZIONE.md`, `REGISTRO-MODIFICHE.md`).
3. Confrontati tutti i 30 valori DSR di `G-20261113-02` contro `DSRCalculator.calculate_dsr_analytical` (`max_diff = 1.110e-16`, `0` discrepanze).
4. Eseguite localmente (Python `3.9.6`) le suite `unittest` con `-s -B -W error` e `mutazioni_dsr_partizione.py`, più test riproduttivi mirati su casi limite non coperti dai test esistenti (`NaN`, manomissione di `commitment.json`, buchi > 2h in orario di mercato, spike intra-candela).

---

## 3. Rilievi

| ID | Gravità | File / Righe | Problema o osservazione | Risoluzione / Azione richiesta | Stato |
|---|---|---|---|---|---|
| G3-01 | **ALTO** | `brain/laboratorio/backtester/dsr.py#L186-L213` | `calculate_dsr_analytical(float("nan"), 20, 600)` restituisce **`(1.0, nan)`**. `math.isfinite` è controllato solo su `varianza_sr_prove` (riga 186), non su `sharpe_estimated`, `skewness`, `kurtosis`, `benchmark_sharpe`; inoltre in Python `min(1.0, float("nan")) == 1.0`, quindi `max(0.0, min(1.0, nan))` trasforma un `NaN` in `DSR = 1.0` (100%). Inoltre `num_trials <= 0` (`0`, `-5`) viene silenziato dal ramo `num_trials <= 1` invece di sollevare `ValueError`. | Validare `math.isfinite` su tutti i parametri float (incluso `z_stat`/`dsr_prob`), sollevare `ValueError` per `num_trials < 1`, e aggiungere test TDD dedicati per `NaN`/`±inf` e `num_trials <= 0`. | APERTO |
| G3-02 | **ALTO** | `brain/dati/pipeline/partizione_date.py#L161-L176` | Bypass crittografico di `verifica()`: modificando una riga di `verifica.jsonl`, cambiando `"ruolo": "verifica"` in `"sviluppo"` dentro `commitment.json` e aggiornando il solo `sha256` (senza conoscere `sealed_nonce.secret`), `verifica(d, fake_nonce)` restituisce **`{'valido': True, ...}`** perché non verifica la presenza di almeno un blocco `"verifica"` né il `commitment_hash`, fidandosi del campo mutabile `d["ruolo"]` dentro `commitment.json`. | Richiedere in `verifica()` che ci sia almeno un blocco `"verifica"` con `commitment_hash` valido verificato tramite nonce, verificare `protocol`/`schema` e preferibilmente accettare/confrontare il file TOML di partizione (`partizione_sha256` e ruoli attesi dei blocchi) in modo che i ruoli non possano essere declassati a `"sviluppo"` in `commitment.json`. | APERTO |
| G3-03 | **MEDIO-ALTO** | `brain/dati/pipeline/dukascopy.py#L154-L209` | Due buchi nei controlli dati di `dukascopy.py`: (1) `classifica_buco()` etichetta un buco infrasettimanale di **2h15m alle 10:00 UTC di mercoledì** come `"festività o chiusura lunga (da verificare)"` anziché `"ANOMALO (in orario di mercato)"`, quindi `controlla()` dà `anomali = 0` e `esegui()` prosegue e scrive il CSV senza fermarsi né chiedere `--accetta-buchi`; (2) `controlla()` verifica `SALTO_MAX` solo fra `c["open"]` e `p["close"]`, lasciando passare con `anomali = 0` uno **spike intra-candela `×3.7`** (`open=2650, high=9999, low=2650, close=2650`, dentro `[1200, 10000]`) o una candela anomala in chiusura seguita da riallineamento. | (1) Classificare `> 2h` in giorni feriali diurne senza copertura festiva dichiarata (o almeno segnalare/bloccare salvo `--accetta-buchi` i buchi `> 2h` che non toccano weekend/chiusure note, o documentare che `--accetta-buchi` serve per festività); (2) controllare anche l'ampiezza intra-candela `c["high"] / c["low"] > SALTO_MAX` (o `max/min` OHLC della singola candela). | APERTO |
| G3-04 | **MEDIO** | `brain/dati/pipeline/dukascopy.py#L248-L285` | In `esegui()`, `scrivi_csv(candele, csv_path)` (riga 273) sovrascrive `XAUUSD_15m.csv` **prima** che `partizione_date.partiziona()` (riga 284) controlli `open(cartella_nonce / NONCE, "x")`. Se un nonce esiste già, `esegui()` solleva `FileExistsError` **dopo** aver già sovrascritto il CSV su disco, lasciando `CSV` e `meta.json`/`partizioni/` disallineati. | Eseguire un pre-check `(Path(cartella_nonce) / partizione_date.NONCE).exists()` all'inizio di `esegui()` (quando `partizione is not None`) prima di scrivere qualsiasi file su disco, mantenendo `open(..., "x")` in `partiziona()` come difesa atomica finale. | APERTO |
| G3-05 | **MEDIO** | `brain/laboratorio/backtester/dsr.py#L142-L153, L296-L307` | La scelta di Claude `V = max(1/(t_len - 1), statistics.variance(campione))` protegge bene dal collasso sotto `1/(T-1)` con prove concentrate, ma `_sharpe_registrati()` raccoglie tutti gli `sharpe_ratio` storici di `trial_registry.json` senza controllare che abbiano lo stesso `total_trades` (`T_n`), senza clusterizzare varianti fortemente correlate (`N_eff`) e usando `statistics.variance` anche con `df = 1` (una sola prova passata valida). Inoltre con `num_trials == 1`, la `nota` di `dsr_v` (riga 343-345) cita una varianza degli Sharpe non usata per `SR0 = 0`. | Accettabile come argine transitorio finché DA-19 / DA-28 non introducono il registro unico con clusterizzazione `N_eff` e `T_med`; aggiungere almeno controllo/avviso su `T_n` eterogenei e pulire la `nota` quando `num_trials == 1`. | APERTO (DA-19/DA-28) |
| G3-06 | **BASSO** | `brain/dati/pipeline/dukascopy.py#L127-L134` | `decodifica()` non controlla `0 <= sec < 86400`, né `lo > 0`, né `math.isfinite(vol)`. Con `vol` pari a `NaN` o `+inf` nel record binario float32, `vol <= 0` è `False` e `round(vol, 6)` solleva `ValueError`/`OverflowError` non incapsulato in `ErroreDati`. | Aggiungere guardie esplicite `0 <= sec < 86400`, `lo > 0`, `math.isfinite(vol)` con sollevamento di `ErroreDati`. | APERTO |
| G3-07 | **INFO / VERIFICATO** | `brain/laboratorio/backtester/dsr.py#L191-L213`, `ESITI.md#L18-L20` | I **30/30 vettori DSR** di `G-20261113-02` coincidono con `calculate_dsr_analytical` (`max_diff = 1.110e-16`), incluso `N = 1` (`SR0 = 0`). La proposta di Claude in `ESITI.md` (riga 20) di calcolare `E[max]` per piccoli `N` via integrazione numerica esatta (o `max(esatto, EVT)`) dopo la revisione 3b è matematicamente fondata (corregge il −8.5% a `N = 2`), purché i vettori di test vengano aggiornati esplicitamente al momento del cambio. | Approvata come evoluzione post-fix; non mescolare finché restano attivi i test sulla formula EVT di Bailey & López de Prado (2014). | CHIUSO / PROPOSTO |

**Legenda gravità:** `BLOCCANTE` = blocco strutturale | `ALTO` = bug grave di correttezza/integrità riprodotto | `MEDIO` = difetto di validazione o robustezza operativa | `BASSO` = difesa sui bordi di decodifica | `INFO` = verifica positiva / allineamento.

---

## 4. Contenuti nuovi proposti

### 4.1 Esito dettagliato delle verifiche eseguite su `2d16a46`

| Verifica | Comando / Metodo (su worktree `../tb-revisione-claude`, Python `3.9.6`) | Risultato osservato |
|---|---|---|
| Confronto 30 vettori DSR `G-20261113-02` vs `DSRCalculator.calculate_dsr_analytical` | Script Python su `T∈{100,600} × N∈{1,2,5,20,100} × SR∈{0.05,0.10,0.20}` (`skew=0, kurt=3`) | **30/30 coincidenti**, `max_diff = 1.110e-16` |
| Suite `dati` + `laboratorio` | `python3 -s -B -W error -m unittest brain.dati.tests.test_pipeline brain.dati.tests.test_dukascopy brain.dati.tests.test_partizione_date brain.laboratorio.tests.test_backtester brain.laboratorio.tests.test_anti_frode_statico brain.laboratorio.tests.test_dsr_scala` | **63/63 OK** (`0.659s`) |
| Suite `guardian` | `python3 -s -B -W error -m unittest discover -s brain/guardian/test -p "test_*.py"` | **77/77 OK** (`6.178s`) |
| Mutation testing nuovo | `python3 -s -B brain/dati/tests/mutazioni_dsr_partizione.py <tmp>` | **26/26 mutanti uccisi** (`exit 0`) |
| Probe `G3-01` (`NaN`, `N=0`) | `DSRCalculator.calculate_dsr_analytical(float("nan"), 20, 600)` e `(0.10, 0, 600)` | Restituisce `(1.0, nan)` su `NaN`; accetta `N=0` |
| Probe `G3-02` (`verifica()` su role tampering) | Modifica `verifica.jsonl` + cambio `"ruolo": "sviluppo"` + aggiornamento `sha256` in `commitment.json` + nonce falso `"deadbeef"` | `PD.verifica(...)` restituisce `valido: True` |
| Probe `G3-03` (`dukascopy` 2h15m e spike) | `classifica_buco(mer 10:00, mer 12:15)` e `controlla` su `high=9999` da `open=close=2650` | Entrambi passano con `anomali = 0` |

*Nota d'ambiente:* in questa macchina è disponibile solo Python `3.9.6`; Python `3.13` non è installato (`which python3.13` assente), quindi i test sono stati verificati personalmente solo su `3.9.6`.

### 4.2 Verdetto sul merge di `fix/dsr-e-partizione-date`

**Raccomandazione: NON ancora pronto per `main`; richieste 2 correzioni mirate (`G3-01` e `G3-02`) + auspicabili `G3-03` e `G3-04` prima del merge.**
Le correzioni richieste sono piccole e isolate (nessuna modifica architetturale):
1. In `dsr.py`: rifiutare `NaN`/`inf` su tutti gli input float (e prima di `max(0.0, min(1.0, ...))`) e `num_trials < 1` con `ValueError`.
2. In `partizione_date.py`: impedire che `verifica()` restituisca `valido = True` quando nessun blocco `"verifica"` è stato verificato col nonce o se i ruoli/schema in `commitment.json` sono stati alterati rispetto al file TOML di partizione.
3. In `dukascopy.py`: segnalare come anomali i buchi infrasettimanali `> 2h` in orario diurno di mercato (o almeno richiedere `--accetta-buchi` anche su `festività o chiusura lunga` non dichiarate), controllare lo spike intra-candela `high / low > SALTO_MAX`, e verificare l'assenza del nonce prima di sovrascrivere `XAUUSD_15m.csv`.

---

## 5. Lacune, duplicazioni, contraddizioni trovate

1. **Gap di verifica fra `partitioning.py` e `partizione_date.py`:** `DatasetPartitioner.verify_commitment` controllava esplicitamente `commitment_hash` di OOS in radice al JSON, rendendo impossibile declassare OOS a in-sample dentro `commitment.json`. `partizione_date.verifica()` delega invece il ruolo (`"verifica"` vs `"sviluppo"`) a un attributo modificabile dentro `commitment.json` senza controllo minimo di cardinalità (`>= 1` verifica verificata) né riscontro sul file TOML di partizione.
2. **Contraddizione interna in `dukascopy.py` sulle "festività o chiusure lunghe":** il docstring di `dukascopy.py` (riga 12) recita *"si ferma sui buchi anomali in orario di mercato, salvo `--accetta-buchi`"*, ma un'interruzione del feed di 2h15m alle 10:00 UTC di mercoledì non viene mai classificata come `"ANOMALO"`, bensì come `"festività o chiusura lunga (da verificare)"`, aggirando silenziosamente il fermo automatico.
3. **Asimmetria tra validazione `varianza_sr_prove` e altri input in `calculate_dsr_analytical`:** mentre `varianza_sr_prove` è protetto rigidamente contro `NaN`/`inf`/`<= 0` (ucciso dal mutante `D05`), `sharpe_estimated`, `skewness`, `kurtosis` e `num_trials` non hanno controlli analoghi.

---

## 6. Fonti consultate

1. Worktree `origin/fix/dsr-e-partizione-date` al commit `2d16a46` (`/Users/gioele/Downloads/tb-revisione-claude`), lettura diretta di tutti i file elencati in `file_esaminati`.
2. Risposte di Claude in `brain/collaborazione/da-claude/ESITI.md` (`2d16a46`).
3. Output diretti di `unittest`, `mutazioni_dsr_partizione.py` e script di probe riproduttivi eseguiti il 2026-11-13 su Python `3.9.6`.

---

## 7. Limiti del rapporto

- Verificato su Python `3.9.6` soltanto (`python3.13` non installato in questa macchina).
- Nessuna esecuzione di rete verso Dukascopy, nessuna lettura di CSV storici, partizioni reali o nonce segreti, nessun file di Claude modificato.
- Nota operativa precedente sui tempi: `brain/laboratorio/tests/mutazioni_lab.py` (31/31 citato in `CONTINUITA.md`) non è stato rilanciato in questa revisione perché fuori dai 12 file modificati nel diff `ce82dbf..2d16a46`.
