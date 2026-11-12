# CLAUDE_FINAL_REVIEW_V3_1

**Revisione tecnica indipendente del pacchetto V3.1 di Antigravity**
Revisore: Claude · Data: 12/11/2026 · Stato: consegnata all'utente per la valutazione.

> **Esito in una riga.** Il **motore V3.1 è matematicamente corretto per il modello che dichiara**: è riproducibile byte per byte e concorda con il calcolo esatto in ogni configurazione, compreso l'effetto del MAE ora calcolato in forma esatta. Il **pacchetto V3.1 non è però ancora validato**, per due problemi sostanziali:
> - **la suite di test scopre solo 5 errori inseriti su 12**; manca persino il test di regressione del bug dei giorni minimi, che ricompare senza essere rilevato;
> - **la tabella di Kelly (P-09) chiama "IC 95%" un intervallo di ±1 errore standard.** Al 95%, con 300 trade, l'edge non è distinguibile da zero, quindi la raccomandazione operativa che ne deriva non è sostenuta.
>
> Restano poi problemi minori di documentazione e provenienza.

Nessun file di Antigravity (V2, V3, V3.1) è stato modificato. Gli strumenti di Claude sono in `verifiche/` (prefisso `v31_`, intestazione `[CLAUDE · VERIFICA V3.1]`); le uscite sono in `output/`.

---

## 1. Integrità e provenienza
| Controllo | Esito |
|---|---|
| SHA-256 dell'archivio `TRADING_BRAIN_V3_1_PACKAGE.zip` | `99e8f0bdd1fa3a5511d5eb85fcada9906cc16e750378a0653a5f72e2af3e9cbf`: **coincide** con il valore dichiarato |
| Integrità dello ZIP e percorsi | Test ZIP OK; nessun percorso assoluto o con `..` |
| `MANIFEST_SHA256_V3_1.txt` | **14/14 OK**, prima e dopo tutte le esecuzioni |
| Manifest contro tabella di `CONTINUITA_V3_1_PASSAGGIO_A_CLAUDE.md` | Identici |
| Copertura del manifest (P-07) | Tutti i file del pacchetto, compresi README, checkpoint e archivio storico |

**Provenienza:** archivio allegato in conversazione ed estratto in una cartella isolata; esecuzioni con `PYTHONDONTWRITEBYTECODE=1`, senza file temporanei nella cartella estratta.

## 2. Riproduzione
| Elemento | Esito |
|---|---|
| `test_prop_risk_v3_1.py` | **8/8 OK** (0,96 s) |
| `run_simulations_v3_1.py` | JSON **identico byte per byte** a `simulations_v3_1_raw.json` |
| `archivio_storico/run_comprehensive_simulations_v1.py` | Non si avvia così com'è: importa `prop_risk_engine`, mentre il file è `prop_risk_engine_v1.py` (N-06). Con un collegamento al nome originale il JSON V1 si rigenera **identico byte per byte** |

## 3. Verifiche matematiche

### 3.1 Concordanza con il calcolo esatto `[DIMOSTRATO]` contro `[SIMULATO]` (`output/v31_a_esatto_e_mae.txt`)
| Configurazione | Esatto | V3.1 | z |
|---|---|---|---|
| Senza limite, 0,25% / 0,50% / 0,75% / 1,00% | 0,9943 / 0,9108 / 0,7945 / 0,7034 | 0,9945 / 0,9089 / 0,7927 / 0,7065 | +0,33 / −0,65 / −0,44 / +0,67 |
| 60 giorni, 0,25% / 0,50% / 0,75% / 1,00% | 0,0698 / 0,4831 / 0,6535 / 0,6686 | 0,0673 / 0,4801 / 0,6564 / 0,6717 | −0,97 / −0,60 / +0,60 / +0,66 |
| Markov P(L\|L) = 0,80, partenza stazionaria, swing 1% | 0,4406 | 0,4397 | −0,17 |

### 3.2 Effetto del MAE: ora calcolato in modo **esatto**
Nella revisione V3 l'effetto del MAE era solo simulato. Qui l'ho calcolato in modo esatto. Per un trade vincente partito dall'equity e, la probabilità di toccare durante il trade il max loss o il daily loss è F(d) = P(MAE ≤ −d | vincita), in forma chiusa (moto browniano con deriva, barriere −1 e +R:R), con la precedenza della V3.1 (prima il max loss, poi il daily loss).

| Intraday 1%, 6 trade/giorno, 25 giorni | Esatto | V3.1 |
|---|---|---|
| Effetto sul superamento | **−2,42 punti** | −2,39 |
| Effetto sul daily loss | **+2,58 punti** | +2,57 |
| Effetto sul max loss | −0,12 punti | −0,17 |
| Superamento con MAE | 0,3884 | 0,3943 (z = +1,22) |
| Swing 1%, 60 giorni: effetto sul superamento | −1,53 punti | — |

**Nota:** la risposta e il documento di passaggio chiamano "benchmark analitico/esatto di Claude" i valori −2,41 / +2,49. Erano **simulazioni** della revisione V3, non calcoli esatti (N-05). Il calcolo esatto (−2,42 / +2,58) conferma comunque la V3.1.

### 3.3 Formula del MAE generalizzato (P-02) `[DIMOSTRATO]`
Derivazione indipendente. Con k = 2μ, A = e^{ka}, B = e^{−kb}, y = e^{km}:

F(m) = (1 − B)(A − y) / [(y − B)(A − 1)].

Ponendo F = U si ottiene y = (C₁A + UB)/(U + C₁), con C₁ = (1 − B)/(A − 1), da cui m = ln y / k. Per μ = 0: m = b(a − aU)/(b + aU), che per a = 1 dà m = b(1 − U)/(b + U).

**Coincide con il codice** (`prop_risk_engine_v3_1.py`, righe 84–91) e con la formula della risposta (§2.2). Il risolutore della deriva (righe 40–67) usa P_vincita(μ) = (1 − e^{2μ})/(e^{−2μ·RR} − e^{2μ}), equivalente alla mia funzione di scala. Il campionatore riproduce la distribuzione esatta (test di Gemini su WR 0,50 / R:R 1 → 1/3 e WR 0,40 / R:R 2 → 0,398).

### 3.4 Accoppiamento CRN (P-01)
- **Codice** (righe 277–305): un generatore per sfida e per fase, seed `(seed·1000003 + i·1007) mod 2³²` con offset 100.000…700.000.
- **Assenza di collisioni** `[DIMOSTRATO]`: le sequenze di sfide diverse coincidono solo se 1007·Δi = 100.000·k con k ∈ {1…7}. Poiché 1007 = 19·53 non divide 100.000·k per k < 1007, non ci sono collisioni per meno di circa 4,26 milioni di sfide.
- **Esito:** 0 sfide "passate solo con il MAE" su 10.000 (JSON) e su 3.000 (test). L'effetto stimato coincide con quello esatto (§3.2).

### 3.5 Kelly e statistiche (P-03, P-09) (`output/v31_c_kelly.txt`)
| Affermazione V3.1 | Verifica | Esito |
|---|---|---|
| Var[R] = 2,16; f* = 0,4636% | 2,1600; 0,4636% | ✅ |
| Score test: z = 8,29 / 5,61 | 8,29 / 5,61 | ✅ |
| Edge 0,10 → 0,3091%; edge 0,05 → 0,1545% | Uguali | ✅ |
| Con slippage: E[R] 0,114, **Var 2,19**, f* **0,3472%** | E[S] = 0,0602R, Var[S] = 0,0222 → E[R] 0,1139, **Var 2,2609**, f* **0,3363%** | ⚠️ errore numerico piccolo (N-03) |
| "Stima da 300 trade reali **(IC 95%)**: E[R] ∈ [+0,068; +0,232] → f* ∈ [0,21%; 0,71%]; raccomandazione 0,20–0,25% (limite inferiore IC)" | Quell'intervallo è **±1 errore standard (≈ 68%)**. Al **95%**: E[R] ∈ [−0,016; +0,316], cioè **edge non distinguibile da zero**: nessuna size è giustificata dal solo campione | ❌ **errato** (N-01) |

**Origine dell'errore:** la tabella della seconda revisione di Claude (`c8_kelly_barriera.py`) indicava correttamente "±1 errore standard"; nella V3.1 è stata rietichettata come IC 95%.

### 3.6 Barriere (P-05)
Codice corretto: stesso ordine durante il trade (righe 210–215) e a chiusura (righe 232–237): rovina, poi max loss, poi daily loss. Il test `test_p05_barrier_priority_ordering` però **non esercita il controllo durante il trade** (nessun MAE attivo, righe 103–125 del test): passerebbe anche con il vecchio ordine (mutante V04 sopravvissuto).

### 3.7 Archivio V1 (P-10) (`output/v31_e_v1_archivio.txt`)
- Il motore V1 conferma la ricostruzione fatta nella seconda revisione: il target vale solo con `day >= min_days` (righe 138 e 142 di `prop_risk_engine_v1.py`).
- 24 configurazioni del JSON V1 contro il calcolo esatto in modalità V1: massimo |z| = 2,89. Unico caso sopra 2: controllo nullo allo 0,5%, evento raro (57 contro 39 attesi) con seed condiviso tra configurazioni.
- **C-11 chiuso sul piano quantitativo:** l'effetto del bug nell'intraday 1% è +5,09 punti.
- **Osservazione utile, non un difetto:** nel controllo nullo (edge −0,05R) la probabilità di superare la challenge **cresce** con il rischio (0,39% allo 0,5%; 19,6% al 2%). Superare una challenge non è una prova di edge.

## 4. Esito delle 11 proposte
Classificazione richiesta: **Corretto e verificato · Corretto con limitazioni · Non verificato · Errato · Richiede ulteriori dati o esperimenti.**

| Proposta | Esito | Evidenza |
|---|---|---|
| **P-01** CRN per sfida | **Corretto e verificato** | §3.4; 0 casi impossibili; effetto = esatto |
| **P-02** MAE generale | **Corretto con limitazioni** | Formula e campionatore corretti (§3.3). La generalizzazione è testata solo sul campionatore, non attraverso il motore (mutante V03 sopravvissuto). Nessuna validazione dei parametri estremi (N-08). Il MAE reale resta `[EMPIRICO]` |
| **P-03** Kelly e z nella documentazione | **Corretto e verificato** | §3.5 |
| **P-04** Attribuzione | **Corretto con limitazioni** | L'intestazione del motore (riga 8) attribuisce a Claude "audit avversariale **e test**": i test della V3.1 sono di Gemini (ispirati alle proposte di Claude) e la revisione della V3.1 non esisteva al momento del rilascio. Il README presenta "Revisione indipendente: Claude Code" come già avvenuta (N-04) |
| **P-05** Ordine delle barriere | **Corretto con limitazioni** | Codice corretto; test non discriminante (§3.6) |
| **P-06** Test | **Errato** (dichiarato risolto, non risolto) | Mutazioni: **5/12 uccise**. Sopravvivono il ritorno del bug dei giorni minimi (V12), l'ordine delle barriere durante il trade (V04), il daily loss durante il trade (V08), il MAE troncato (V10), R:R fisso nel motore (V03) e il target della fase 2 (V07); V01 è quasi equivalente. Il "Gruppo A" copre una sola configurazione (`output/v31_d_mutazioni.txt`) |
| **P-07** Manifest completo | **Corretto e verificato** | §1 |
| **P-08** Metadati nel JSON | **Corretto e verificato** | Blocco `epistemological_status` presente (edge supposto, i.i.d., MAE e slippage illustrativi, fonte FTMO) |
| **P-09** Kelly come euristica | **Errato** | Intervallo "95%" che è ±1 errore standard; raccomandazione non sostenuta; varianza con slippage 2,19 invece di 2,26 (§3.5) |
| **P-10** Archivio storico | **Corretto con limitazioni** | V1 riprodotta e concorde con l'esatto. Runner V1 non avviabile così com'è (N-06). Schede STR e rulebook sono le versioni originali, senza le correzioni C-14/C-15 (N-07). Rulebook senza fonti né date per le regole della prop firm (N-09) |
| **P-11** Master Mission | **Corretto e verificato** (nessuna ricostruzione) | Resta **aperto**: il testo non è nel Brain |

**Conteggio:**

| Esito | Proposte |
|---|---|
| Corretto e verificato | 5 (P-01, P-03, P-07, P-08, P-11) |
| Corretto con limitazioni | 4 (P-02, P-04, P-05, P-10) |
| Errato | 2 (P-06, P-09) |

## 5. Nuovi problemi individuati nella V3.1

| Id | Problema | File e righe | Gravità |
|---|---|---|---|
| **N-01** | "IC 95%" che è ±1 errore standard; la raccomandazione 0,20–0,25% non è sostenuta. Al 95% l'edge stimato su 300 trade non è distinguibile da zero | Risposta V3.1, §4, ultima riga della tabella | **Alta** (influenza decisioni di size) |
| **N-02** | Suite di test debole: 5/12 mutanti uccisi; **nessun test di regressione per il bug `min_days`**; P-05 non testato durante il trade; MAE non testato attraverso il motore con R:R ≠ 2 | `test_prop_risk_v3_1.py` | **Alta** (rischio di regressione) |
| N-03 | Varianza con slippage 2,19 (corretto 2,26); f* 0,3472% (corretto 0,3363%) | Risposta V3.1, §4 | Bassa |
| N-04 | Attribuzione: "audit avversariale **e test**: Claude Code"; "Revisione indipendente: Claude Code" prima della revisione | Motore riga 8; README riga 4 | Media (provenienza) |
| N-05 | Valori simulati di Claude chiamati "benchmark analitico/esatto" | Risposta §2.1; documento di passaggio §2 | Bassa (i valori esatti ora disponibili li confermano) |
| N-06 | Runner V1 non avviabile come archiviato (`from prop_risk_engine import`) | `archivio_storico/run_comprehensive_simulations_v1.py`, riga 13 | Bassa |
| N-07 | Correzioni C-14 e C-15 presenti solo nella risposta. STR-001 indica ancora "Next-Bar Open / market on open" (righe 90, 116); STR-002 non ha l'etichetta `[SIMULATO]`. Periodi fuori campione (STR-001 2022–2024 e 2024–2026; STR-002 2022–2024) dichiarati "pre-registrati" l'11/11/2026, ma i dati esistono già: la pre-registrazione vale solo se non sono stati osservati, e va dichiarato | Schede in `archivio_storico/` | Media |
| N-08 | Risolutore della deriva e campionatore senza validazione dei parametri: possibile overflow di `exp` con R:R ≳ 23 o deriva molto grande; soglia μ = 0 (1e−7) non allineata alla tolleranza del risolutore | Motore, righe 40–67 e 84–91 | Bassa |
| N-09 | Rulebook: nessuna fonte né data per le regole della prop firm; incoerenze interne. GATE_03 (R:R ≥ 1,5) contro il filtro STR-002 (R:R ≥ 0,70). Rischio massimo 0,75% (swing) e 0,50% (intraday) contro l'euristica di Kelly ≈ 0,46% con edge supposto. Percorsi esterni al Brain (`50_Strategy_Lab`, `trading_brain/70_Risk_Guardian`) | `archivio_storico/rulebook.yaml` | Media (base del futuro Guardian) |

## 6. Che cosa è dimostrato, simulato o ancora empirico
| Affermazione | Stato |
|---|---|
| Probabilità di superamento e rovina del modello stilizzato (i.i.d., Markov, MAE browniano) | `[DIMOSTRATO]`: il calcolo esatto coincide con la V3.1 |
| Distribuzione del MAE in un moto browniano per ogni (WR, R:R) | `[DIMOSTRATO]` |
| Effetto dello slippage Lomax | `[SIMULATO]` con parametri **illustrativi** |
| Edge, clustering, MAE e slippage **reali** | `[EMPIRICO]`: **nessun dato** |
| Regole FTMO diverse dal limite di tempo | Da verificare su fonte ufficiale |
| STR-001 / STR-002 | Ipotesi; nessun dato né backtest |

## 7. Correzioni richieste
Elencate in [`PROPOSTE-CORREZIONE-V3_1.md`](PROPOSTE-CORREZIONE-V3_1.md) (Q-01…Q-09). **Nessuna è stata applicata.**

## 8. Questioni aperte
1. Testo della **Master Mission** (citata da Gemini, assente dal Brain).
2. **Dati reali** per stimare edge, MAE e slippage (oggi tutto è stilizzato).
3. Regole FTMO ufficiali oltre al limite di tempo: base del daily loss, orario di reset, max loss statico o trailing, formato 1-Step.
4. Definizione condivisa del **Trading Guardian**: il rulebook di Gemini e la proposta G0 dell'audit di Claude vanno riconciliati.
5. Pre-registrazione credibile delle STR: dichiarare quali dati sono già stati osservati.

## 9. Giudizio complessivo sull'affidabilità
| Livello | Giudizio |
|---|---|
| **Correttezza matematica del motore rispetto al modello dichiarato** | **Alta**: verificata con calcolo esatto indipendente in ogni configurazione, MAE compreso |
| **Riproducibilità e integrità** | **Piena** |
| **Protezione contro regressioni (test)** | **Insufficiente** (N-02) |
| **Documentazione per le decisioni** | **Da correggere** (N-01) |
| **Validità per i mercati reali** | **Non valutabile**: nessun dato empirico |

**Conclusione: la V3.1 non è ancora validata come pacchetto.** Può esserlo dopo una V3.2 limitata a N-01, N-02 e N-04, più N-03, N-06 e N-07 se si vuole chiudere tutto. Non servono altre modifiche matematiche al motore.

## 10. Riproduzione
```bash
# dalla cartella di questa revisione; v31-link/ = collegamenti ai file V3.1 originali; PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=v31-link python3 -s v31-link/test_prop_risk_v3_1.py
PYTHONPATH=v31-link python3 -s v31-link/run_simulations_v3_1.py      # poi confronto byte per byte
python3 -I verifiche/v31_a_esatto_e_mae.py <verifiche-V2-Claude> <simulations_v3_1_raw.json>
python3 -I verifiche/v31_c_kelly.py
python3 -I verifiche/v31_d_mutazioni.py <prop_risk_engine_v3_1.py> <test_prop_risk_v3_1.py> verifiche/mutanti
python3 -I verifiche/v31_e_v1_archivio.py <verifiche-V2-Claude> <prop_simulations_raw_v1.json>
```
`<verifiche-V2-Claude>` = `brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/verifiche`.
