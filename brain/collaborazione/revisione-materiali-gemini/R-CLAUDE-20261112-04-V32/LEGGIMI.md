# Revisione V3.2: come rieseguire le verifiche

Contenuto:
- `CLAUDE_FINAL_REVIEW_V3_2.md`: revisione ed esito;
- `CLAUDE_CORRECTION_PROPOSALS_V3_2.md`: proposte S-01…S-09;
- `REGISTRO_VERIFICHE_V3_2.md`: verifiche eseguite;
- `CONFRONTO_AFFERMAZIONI_V3_2.md`: affermazioni di Gemini a confronto con i risultati;
- `verifiche/`: strumenti;
- `output/`: uscite;
- `MANIFEST_REVISIONE_CLAUDE.sha256`: impronte.

## Preparazione
- Estrarre `TRADING_BRAIN_V3_2_PACKAGE.zip` in una cartella vuota, che qui chiamiamo `<V32>`.
- Copiare `prop_risk_engine_v3_2.py`, `test_prop_risk_v3_2.py` e `run_simulations_v3_2.py` in una cartella di lavoro, che qui chiamiamo `<LAV>`: il runner scrive il JSON accanto a sé.
- Usare `PYTHONDONTWRITEBYTECODE=1`.
- `<V2>` è `../R-CLAUDE-20261111-01-V2/verifiche` e contiene `c1_esatto_challenge.py` e `c4b_markov_esatto.py`.

## Comandi
```bash
cd <V32> && sha256sum -c MANIFEST_SHA256_V3_2.txt
```
```bash
cd <LAV> && python3 -s -B test_prop_risk_v3_2.py -v
```
```bash
cd <LAV> && python3 -s -B run_simulations_v3_2.py && sha256sum simulations_v3_2_raw.json
```
```bash
python3 -s -B verifiche/v32_a_esatto.py <V2> <LAV>
```
```bash
python3 -s -B verifiche/v32_d_mutazioni.py <V32>/prop_risk_engine_v3_2.py <V32>/test_prop_risk_v3_2.py <cartella vuota per i mutanti>
```
```bash
python3 -s -B verifiche/v32_b_robustezza_test.py <LAV> <cartella mutanti>/V10
```
```bash
python3 -s -B verifiche/v32_c_kelly_q08_crn.py <LAV>
```
```bash
PYTHONPATH=<LAV> python3 -s -B verifiche/test_proposti_claude_v32.py
```

Il runner V1 va eseguito secondo `archivio_storico/LEGGIMI_V1.md`, su una copia dei due file. La modalità B funziona solo con `r.run_suite()` (S-03).

## Tempi indicativi (contenitore della sessione)
- suite: 1,4 s;
- runner: 8 s;
- `v32_a`: 5 s;
- `v32_d`: 33 s;
- `v32_b`: 75 s;
- `v32_c`: 1 s.
