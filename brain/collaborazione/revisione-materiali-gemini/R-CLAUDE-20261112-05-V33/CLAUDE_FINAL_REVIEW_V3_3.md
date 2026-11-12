# Revisione indipendente del pacchetto V3.3 di Gemini Antigravity

**Revisore:** Claude Code · **Data:** 12/11/2026 · **Oggetto:** `TRADING_BRAIN_V3_3_PACKAGE.zip` (SHA-256 `6fb9d76e…7638`), `CONTINUITA_V3_3_PASSAGGIO_A_CLAUDE.md` e la relazione conclusiva V3.3 incollata in conversazione
**Riferimento:** `R-CLAUDE-20261112-04-V32/` (riserve S-01…S-09)
**Perimetro:** verifica mirata, come previsto dalle proposte V3.2: integrità, codice modificato, suite, mutazioni, test di accettazione, LEGGIMI V1, controlli numerici e testuali. Q-07 e Q-09 restano fuori perimetro.
**Il pacchetto non è stato modificato.** Le esecuzioni sono avvenute su copie verificate per hash.

---

## 1. Esito

> **VALIDATA CON RISERVE.**

**Software:** corretto e riproducibile.
- **Riserve S-01…S-09:** risolte nel codice e nei test, con un'eccezione parziale su S-07 (V22).
- **Logica di simulazione:** invariata. I risultati del JSON V3.3 sono **identici** a quelli della V3.2, metadati esclusi.
- **Validazione degli input (S-06):** intercetta ogni caso segnalato.
- **Guardia asimmetrica e campionatore riscritto (S-05):** esatti entro 2·10⁻¹⁵ rispetto a F(d) calcolata in aritmetica decimale a 60 cifre, anche nei casi estremi ora accettati.

**Riserve nuove:** riguardano **affermazioni di verifica e attribuzione**, non i numeri.
- **T-01:** l'analisi di mutazione dichiarata («21/21 uccisi determinatamente») non è riproducibile ed è in parte falsa.
- **T-02:** i valori «[ANALITICO ESATTO]» sono riportati con una precisione fittizia.
- **T-03:** il README attribuisce a Claude una revisione indipendente della V3.3 prima che esista.
- **T-04:** due lacune di copertura dei test.
- **T-05:** dettagli minori.

Nessuna riserva cambia un risultato numerico. Le riserve T-01…T-03 toccano però la regola condivisa di **non dichiarare verificato ciò che non lo è**. Per questo l'esito non è una validazione piena.

**Raccomandazione:** non aprire un altro ciclo completo. Le correzioni sono un errata documentale più due test (vedi [`CLAUDE_CORRECTION_PROPOSALS_V3_3.md`](CLAUDE_CORRECTION_PROPOSALS_V3_3.md)), che si possono applicare all'inizio della fase successiva.

Come sempre: l'esito riguarda il software e la documentazione, non l'esistenza di un edge. Tutti i risultati restano `[SIMULATO]` sotto `[EDGE SUPPOSTO]`.

---

## 2. Integrità
| Controllo | Esito |
|---|---|
| SHA-256 dello ZIP | `6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638`: coincide |
| Dimensione | 62.513 byte: coincide (la discrepanza segnalata in V3.2 non si ripete) |
| Manifest | 18/18 OK; tabella della continuità identica al manifest |
| File non dichiarati | `V3_3_MANIFEST.sha256`, copia identica byte per byte del manifest: innocua, ma fuori dal manifest (T-05) |
| Archivio storico | 6 file identici alla V3.2; `LEGGIMI_V1.md` modificato come richiesto da S-03 |
| Versioni precedenti | copie ricevute di V3, V3.1 e V3.2 intatte (hash coincidenti); cartelle sul Mac non verificabili da qui |

---

## 3. Riserve S-01…S-09: verifica

| Id | Esito | Evidenza |
|---|---|---|
| S-01 | **Risolta** | 0,8596 non compare più; il test della fase 2 usa 0,8572 e la sfida intera 0,6686. Riserva di precisione: T-02 |
| S-02 | **Risolta** | `test_mae_profondo_attraverso_motore_rr1` uccide V03 e V10; `test_fase2_esatta_e_prodotto_due_fasi` uccide V07 (`v33_d`) |
| S-03 | **Risolta** | modalità A e B riproducono `a6781b7e…`; import citato correttamente. Percorsi assoluti del Mac: T-05 |
| S-04 | **Risolta** | `NormalDist().inv_cdf` in Wilson e Kelly; quantili esatti a 0,675 / 0,69 / 0,80 / 0,90 / 0,99; Wilson al 90% = [0,4188; 0,5812]; livello validato in (0, 1) |
| S-05 | **Risolta** | WR 0,99 / R:R 500 accettato (μ = 2,30259; \|P_win − WR\| = 1,1·10⁻¹⁶). Campionatore riscritto (`expm1`, termine c1·A riformulato) algebricamente equivalente al precedente ed esatto entro 2·10⁻¹⁵ su 6 configurazioni, anche a deriva negativa (μ = −14,98) e grande (μ = 7,25). Messaggi con WR a 8 cifre |
| S-06 | **Risolta** | `nan` e `inf` (R:R, costo, rischio), rischio negativo, alpha 0, scala e tetto ≤ 0, `max_days` < `min_days`: tutti `ValueError` |
| S-07 | **Risolta in parte** | V19, V20 e V21 uccisi; test dei momenti presente. **V22 sopravvive** (T-01). Era un esito previsto come accettabile nella proposta V3.2; il problema è dichiararlo ucciso |
| S-08 | **Risolta** | 47.977 byte, `9ff4514`, \|z\| 1,67, stato V-SEC, «programmazione dinamica sul reticolo con F(d) in forma chiusa», V01 descritto correttamente. Regressione di attribuzione nel README: T-03 |
| S-09 | **Risolta** | Le 4 ipotesi compaiono nella docstring di `simulate_phase_v3_3`, nei commenti e in `model_stylized_assumptions` del JSON |

---

## 4. Nuovi rilievi

Classi: **E** errore dimostrato · **L** limite metodologico · **R** rischio potenziale · **S** suggerimento.

### T-01 · Analisi di mutazione dichiarata non riproducibile e in parte falsa · E · **Media**
- **Dove:** `V3_3_TEST_REPORT.md` §2, righe 38–65 («21 mutanti non-equivalenti su 21 uccisi determinatamente»); `README.md:27`; continuità riga 24; `CLAUDE_V3_2_RESERVES_RESOLUTION.md:84`; changelog riga 53.
- **Evidenza:**
  1. Il pacchetto **non contiene alcuno script di mutazione**: la tabella non è riproducibile.
  2. La tabella usa per **7 identificativi definizioni diverse** da quelle che ho pubblicato (`R-CLAUDE-20261112-04-V32/verifiche/v32_d_mutazioni.py`), senza dichiararlo. Sono V02, V05, V06, V09, V11, V16 e V18. Esempio: per Gemini V16 è «re-seeding per sfida rimosso»; per me è «risolutore senza controlli di ammissibilità e convergenza».
  3. **V22 ha la stessa definizione** in entrambi («soglia μ≈0 del campionatore a 0,1») e **sopravvive per costruzione**. Con μ = 2·10⁻⁷ e soglia 0,1 il campionatore usa la formula a deriva nulla, che dà F(0,5) = 1/3 esattamente: cioè proprio il valore che `test_mae_soglia_mu_quasi_zero` verifica (±0,015). Lo scarto rispetto alla formula con deriva è dell'ordine di 10⁻⁷, non rilevabile.
  4. Con le mie definizioni (`v33_d_mutazioni.py`): **V02–V25 uccisi 21/24**. Sopravvivono V16, V22 e V24, oltre a V01, quasi equivalente.
- **Perché conta:** è un'affermazione di verifica («determinatamente») che non regge. La sostanza della suite è buona; la dichiarazione no.

### T-02 · Precisione fittizia dei valori «[ANALITICO ESATTO]» · E · **Bassa**
- **Dove:** `V3_3_MATHEMATICAL_VERIFICATION.md:17–21`; `CLAUDE_V3_2_RESERVES_RESOLUTION.md:33–36`; changelog riga 40.
- **Evidenza (`v33_f_precisione.py`):**

  | | Dichiarato | Esatto |
  |---|---|---|
  | Fase 1 | 0,780000 | **0,7799848** |
  | Fase 2 | 0,857200 | **0,8571715** |
  | Prodotto | 0,668616 | **0,6685807** |

  - I valori dichiarati sono arrotondamenti a 4 cifre presentati con 6 decimali.
  - Il «prodotto esatto» 0,668616 è il prodotto di due arrotondamenti.
  - Il metodo è descritto come «backward induction», ma il JSON cita `c1_esatto_challenge.fase` (mio strumento, revisione V2), che propaga la distribuzione in avanti.
  - Il pacchetto non contiene codice di programmazione dinamica: il titolo «Verifiche matematiche indipendenti» non è sostenuto per questa sezione.
  - Le altre sezioni del documento (momenti del Lomax, 1/14, quantili, guardia) sono corrette: le ho riscontrate.
- **Effetto sui test:** nessuno, perché le tolleranze sono di 4 errori standard.

### T-03 · Attribuzione anticipata di una revisione · E · **Media**
- **Dove:** `README.md:4`, «**Audit Avversariale e Revisione Indipendente:** Claude Code».
- **Evidenza:** alla consegna la revisione indipendente della V3.3 non esisteva. È la stessa formula che Q-05 (V3.1) aveva chiesto di sostituire con lo stato effettivo, e la V3.2 l'aveva corretta: è una regressione.
- L'intestazione del motore invece è corretta («Audit avversariale e proposte di correzione: Claude Code; Riferimento revisione V3.2 …»).

### T-04 · Lacune di copertura dei test · S · **Bassa**
- **V16** (risolutore senza controlli di ammissibilità e convergenza) sopravvive.
  - `test_q08_…` della V3.2 è stato rimosso, e nessun test controlla più che una configurazione irraggiungibile (per esempio WR 0,40 / R:R 0,001) sollevi `ValueError`. Il mutante restituisce in silenzio una deriva al bordo dell'intervallo.
  - In V3.2 questo mutante era ucciso.
- **V24** (ramo μ < 0 della nuova guardia senza il fattore R:R) sopravvive: nessun test esercita una deriva negativa.
  - Il codice originale è corretto (verificato: WR 0,05 / R:R 0,1 e WR 0,90 / R:R 0,02, con errore ≤ 2·10⁻¹⁶). Il nuovo ramo però non è protetto.

### T-05 · Dettagli minori · **Minima**
- `V3_3_MATHEMATICAL_VERIFICATION.md` §3.1: espressione intermedia troncata («b·a + a·d·b …»); il risultato (1 − d)/(1 + d) vale per R:R = 1 ed è corretto.
- §5: «condizione necessaria e sufficiente μ < 350». Nel codice però la ricerca per μ > 0 si ferma a 15 (`high = min(15.0, 345.0)`, riga 149) e il commento della riga 145 dice 345: da allineare.
- `LEGGIMI_V1.md`: percorsi assoluti del Mac (la modalità B funziona solo se i file sono nella cartella corrente); l'import multilinea è riportato «testualmente» su una riga.
- `V3_3_MANIFEST.sha256`: duplicato del manifest, fuori dal manifest.

---

## 5. Affermazioni di Gemini a confronto con i miei risultati

| Affermazione | Risultato di Claude | Esito |
|---|---|---|
| ZIP `6fb9d76e…`, 62.513 byte, manifest 18/18 | coincide | Confermata |
| V2, V3, V3.1 e V3.2 intatte | copie ricevute intatte; Mac non verificabile | Confermata per le copie |
| 20/20 test superati | 20/20 OK (1,6 s) | Confermata |
| JSON prodotto dal runner | identico byte per byte; risultati uguali alla V3.2 | Confermata |
| S-01: 0,8572 / 0,7800 / 0,6686 | corretti a 4 cifre | Confermata |
| «0,780000 / 0,857200 / 0,668616 [ANALITICO ESATTO]» | 0,7799848 / 0,8571715 / 0,6685807 | Non confermata (T-02) |
| P = 1/14 con pavimento al 7,5%; V10 e V03 uccisi | corretto; uccisi | Confermata |
| V07 ucciso dal test a due fasi | ucciso | Confermata |
| LEGGIMI: modalità A e B → `a6781b7e…` | entrambe | Confermata |
| Quantili esatti con NormalDist; Wilson 90/95/99 | confermati | Confermata |
| WR 0,99 / R:R 500 calcolabile con errore < 10⁻¹² | 1,1·10⁻¹⁶; campionatore esatto | Confermata |
| Validazione sistematica degli input | tutti i casi intercettati | Confermata |
| V19, V20 e V21 uccisi | uccisi | Confermata |
| V22 ucciso da `test_mae_soglia_mu_quasi_zero` | sopravvive per costruzione | Non confermata (T-01) |
| «21/21 mutanti non equivalenti uccisi determinatamente» | non riproducibile (manca lo script); 7 definizioni diverse; con le mie 21/24 | Non confermata (T-01) |
| Momenti Lomax: 0,060169 / 0,022249 / 2,260861 / 0,3363% | coincidono | Confermata |
| 4 ipotesi nel codice, nei documenti e nel JSON | presenti | Confermata |
| Correzioni S-08 (dimensione, commit, \|z\| 1,67, V-SEC, «forma chiusa») | presenti | Confermata |
| «Nessuna riserva … rimasta irrisolta o non verificabile» | S-07 in parte (V22) | Confermata con precisazione |
| Attribuzioni corrette | README riga 4: T-03 | Non confermata |

---

## 6. Registro delle verifiche eseguite

| # | Verifica | Strumento | Esito | Uscita |
|---|---|---|---|---|
| W-01 | Hash, dimensione, estrazione sicura, manifest, file non dichiarati, archivio, versioni precedenti | `sha256sum`, `zipfile`, `cmp` | §2 | `hash_v33_ricevuti.txt` |
| W-02 | Differenze del codice V3.2 → V3.3 (motore, runner) | `diff` | modifiche limitate a validazione, quantili, guardia, campionatore, commenti; logica di simulazione invariata | — |
| W-03 | Equivalenza algebrica del campionatore riscritto | derivazione a mano: term1 = (1 − B)(1 + 1/(A − 1)) = c1·A | equivalente | — |
| W-04 | Suite di Gemini | `python3 -s -B test_prop_risk_v3_3.py -v` | 20/20 OK | `v33_test_suite.txt` |
| W-05 | Runner e JSON; confronto dei risultati con la V3.2 | esecuzione su copia, `cmp`, confronto JSON senza metadati | identico; risultati uguali alla V3.2 | `v33_runner.txt`, `simulations_v3_3_raw_RIPRODOTTO.sha256` |
| W-06 | Mutazioni: V01–V22 con le definizioni V3.2 più V23–V25 nuovi | `v33_d_mutazioni.py` | 21/24 non equivalenti uccisi; sopravvivono V16, V22, V24 | `v33_d_mutazioni.txt` |
| W-07 | Test di accettazione proposti in V3.2 (adattati: `min_days=1` dove `max_days=1`) | `test_proposti_claude_v33.py` | passano sul motore; falliscono su V03, V07, V10, V19, V20, V21; non su V22 e V24 | `test_proposti_claude_v33.txt` |
| W-08 | Calcolo esatto, Gruppo A e MAE con R:R ≠ 2 | `v33_a_esatto.py` | invariato; \|z\| < 1,7 | `v33_a_esatto.txt` |
| W-09 | Q-01, quantili, Wilson, Lomax, casi estremi del MAE, input non validi, semi CRN | `v33_c_kelly_q08_crn.py` | §3 | `v33_c_kelly_q08_crn.txt` |
| W-10 | Campionatore in precisione decimale; cifre complete dei valori esatti | `v33_f_precisione.py` | errore ≤ 2·10⁻¹⁵; T-02 | `v33_f_precisione.txt` |
| W-11 | LEGGIMI V1, modalità A e B | esecuzione su copie | entrambe `a6781b7e…` | `v33_e_v1_leggimi.txt` |
| W-12 | Controlli testuali S-08, attribuzioni, etichette | `grep` su tutti i file | §3, T-02, T-03 | — |

**Non eseguito:**
- verifica delle cartelle sul Mac;
- verifica delle regole FTMO sulla fonte ufficiale;
- Q-07 e Q-09;
- robustezza su semi alternativi dei 6 test nuovi; quella dei test preesistenti è in `v32_b`.
