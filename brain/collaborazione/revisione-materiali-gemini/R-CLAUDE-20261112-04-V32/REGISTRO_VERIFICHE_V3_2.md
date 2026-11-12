# Registro delle verifiche effettivamente eseguite (revisione V3.2)

Ambiente: contenitore Linux, Python 3.13.18, sola libreria standard. Data: 12/11/2026.
- Ogni esecuzione è avvenuta su **copie** dei file di Gemini, verificate per hash, in cartelle di lavoro separate.
- Opzioni `-s -B` e `PYTHONDONTWRITEBYTECODE=1` (nessun file `.pyc`).
- L'estratto originale era in sola lettura.

Le uscite in `output/` sono quelle prodotte in questa sessione. Nei file di testo i percorsi della cartella di lavoro sono abbreviati in `<cartella di lavoro>`.

| # | Verifica | Metodo, strumento | Risultato | Uscita |
|---|---|---|---|---|
| V-01 | SHA-256 e dimensione dello ZIP | `sha256sum`, `stat` | hash coincide; dimensione 47.977 byte (dichiarati 41.696) | `hash_v32_ricevuti.txt` |
| V-02 | Estrazione sicura | `zipfile.testzip`, controllo di percorsi assoluti e `..`; estrazione in una cartella vuota, poi in sola lettura | OK | idem |
| V-03 | Manifest | `sha256sum -c MANIFEST_SHA256_V3_2.txt` | 15/15 OK | idem |
| V-04 | File non dichiarati | confronto tra l'elenco dei file e il manifest | nessuno | idem |
| V-05 | Tabella della continuità contro il manifest | `diff` | identiche | — |
| V-06 | Archivio storico contro V3.1 | `cmp` sui 6 file | identici | idem |
| V-07 | Copie ricevute di V2, V3 e V3.1 | hash degli ZIP; `sha256sum -c` dei manifest V3 e V3.1; confronto V2 con `MANIFEST_SHA256.txt` | tutte intatte (le cartelle sul Mac non sono verificabili) | idem |
| V-08 | Suite di Gemini | `python3 -s -B test_prop_risk_v3_2.py -v` | 14/14 OK | `v32_test_suite.txt` |
| V-09 | Runner e JSON | `run_simulations_v3_2.py` su copia; `cmp` con il JSON consegnato | identico byte per byte (`5260c4f0…`) | `v32_runner.txt`, `simulations_v3_2_raw_RIPRODOTTO.sha256` |
| V-10 | LEGGIMI V1, modalità A e B | entrambe su copie separate | A: `a6781b7e…` OK; B: `AttributeError`; B con `run_suite()`: `a6781b7e…` OK | `v32_e_v1_leggimi.txt` |
| V-11 | Valori di riferimento dei test | `v32_a_esatto.py` (A): calcolo esatto sul reticolo (`c1`, `c4b` della revisione V2) e F(d) in forma chiusa | Gruppo A coincide; fase 2 0,8572 (non 0,8596); fase 1 0,7800 (non 0,776); 1/3, 1/6, μ e F(0,5) coincidono | `v32_a_esatto.txt` |
| V-12 | Effetto esatto del mutante V10 | `v32_a` (B) | identico nel test R:R 1; +2,52 SE nel Gruppo A (soglia 4) | idem |
| V-13 | MAE con R:R ≠ 2 sull'intera sfida | `v32_a` (C): 4 configurazioni, esatto contro motore, n = 20.000 | tutti i \|z\| < 1,7 | idem |
| V-14 | Analisi di mutazione | `v32_d_mutazioni.py`: 12 mutanti della V3.1 adattati più 10 nuovi; caricamento del mutante verificato | V02–V12 11/11; totale 17/22 | `v32_d_mutazioni.txt` |
| V-15 | Robustezza dei test stocastici | `v32_b_robustezza_test.py`: seme 42 e 40 semi alternativi; V10 con 40 semi | 0 falsi allarmi; \|z\| massimo con il seme 42 1,67; V10 mai rilevato dal Gruppo A né dal test R:R 1 | `v32_b_robustezza_test.txt` |
| V-16 | Q-01 | `v32_c` con `NormalDist` | IC e f* coincidono | `v32_c_kelly_q08_crn.txt` |
| V-17 | Quantili per altri livelli | `v32_c` | Wilson errato a livelli ≠ 0,95; Kelly: banda attorno a 0,6827 | idem |
| V-18 | Q-03 | `v32_c`: momenti troncati in forma chiusa più Monte Carlo (2·10⁶) della formula del motore | coincidono | idem |
| V-19 | Q-08, casi estremi | `v32_c`: 15 combinazioni (WR, R:R); errore di P_win; campionatore contro F(d) | nessun overflow; accettati corretti; rifiuti conservativi | idem |
| V-20 | Soglia μ ≈ 0 | `v32_c`: WR a 10⁻⁸, 2·10⁻⁷ e −3·10⁻⁷ dalla soglia; continuità di F(0,5) | coerente | idem |
| V-21 | Input non validi | `v32_c`: `nan`, `inf`, rischio negativo, alpha 0, `max_days` < `min_days` | non intercettati | idem |
| V-22 | Semi CRN | `v32_c`: collisioni per il seme 42 fino a 20.000 sfide; distanza minima di collisione per qualsiasi seme | 0 collisioni; distanza minima 439.306.784 | idem |
| V-23 | Q-05, attribuzioni | ricerca di «Claude» in tutti i file, JSON compreso; confronto con `git log` | coerenti; V01 descritto in modo errato; commit errato | — |
| V-24 | Etichette epistemiche | ricerca di «analitic», «forma chiusa», «ufficiale», «V-SEC» e dei valori citati | S-01, S-08 | — |
| V-25 | Ipotesi del modello | lettura di `simulate_phase_v3_2`; ricerca testuale nei documenti | S-09 | — |
| V-26 | Test di accettazione proposti | `test_proposti_claude_v32.py` su motore originale, mutanti V03, V07, V10, V19, V20 e V21, e su una copia con Wilson corretto (con e senza V21) | discriminano come atteso | `test_proposti_claude_v32.txt` |

**Non eseguito:**
- verifica delle cartelle di Antigravity sul Mac (inaccessibili);
- verifica delle regole FTMO sulla fonte ufficiale;
- Q-07 e Q-09 (fuori perimetro);
- analisi delle schede STR e del rulebook.
