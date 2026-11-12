# Revisione V3.3: come rieseguire le verifiche

Contenuto:
- `CLAUDE_FINAL_REVIEW_V3_3.md`: esito, stato di S-01…S-09, rilievi T-01…T-05, confronto delle affermazioni e registro delle verifiche;
- `CLAUDE_CORRECTION_PROPOSALS_V3_3.md`: errata proposto;
- `verifiche/`: strumenti;
- `output/`: uscite;
- `MANIFEST_REVISIONE_CLAUDE.sha256`: impronte.

Gli strumenti `v33_a`, `v33_c` e `test_proposti_claude_v33` sono gli strumenti della revisione V3.2 (`../R-CLAUDE-20261112-04-V32/verifiche/`) con i nomi della V3.3. Nei test proposti, `min_days=1` nelle due chiamate con `max_days=1`, richiesto dalla validazione S-06. `v33_d_mutazioni.py` aggiunge V23–V25 ai mutanti della V3.2.

## Preparazione
- Estrarre lo ZIP in `<V33>`.
- Copiare motore, test e runner in `<LAV>`.
- Usare `PYTHONDONTWRITEBYTECODE=1`.
- `<V2>` è `../R-CLAUDE-20261111-01-V2/verifiche`.

## Comandi
```bash
cd <V33> && sha256sum -c MANIFEST_SHA256_V3_3.txt
```
```bash
cd <LAV> && python3 -s -B test_prop_risk_v3_3.py -v && python3 -s -B run_simulations_v3_3.py
```
```bash
python3 -s -B verifiche/v33_d_mutazioni.py <V33>/prop_risk_engine_v3_3.py <V33>/test_prop_risk_v3_3.py <cartella vuota>
```
```bash
python3 -s -B verifiche/v33_a_esatto.py <V2> <LAV>
```
```bash
python3 -s -B verifiche/v33_c_kelly_q08_crn.py <LAV>
```
```bash
python3 -s -B verifiche/v33_f_precisione.py <V2> <LAV>
```
```bash
PYTHONPATH=<LAV> python3 -s -B verifiche/test_proposti_claude_v33.py
```
