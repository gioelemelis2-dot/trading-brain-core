# R-CLAUDE-20261111-01-V2 · Seconda revisione del pacchetto V2 di Antigravity

Revisore: Claude · Data: 11/11/2026 · Documento principale: [`CLAUDE_SECOND_REVIEW_ANTIGRAVITY_V2.md`](CLAUDE_SECOND_REVIEW_ANTIGRAVITY_V2.md) (SHA-256 `4d07122f0a2e53437863ae7927daa746b873dae7332bfa527badcff0ca58025d`, invariato rispetto alla versione consegnata all'utente).

## Contenuto
| Cartella / file | Che cosa |
|---|---|
| `verifiche/c*.py` | Strumenti di verifica di Claude (calcolo esatto, semi multipli, V1/V2, Markov, MAE, slippage, Kelly, mutazioni, STR-002) |
| `verifiche/test_aggiuntivi_claude.py` | Test aggiuntivi: gruppo A (devono passare), gruppo B (documentano i difetti E-01…E-03) |
| `output/` | Uscite delle verifiche del 11/11/2026 |
| `output/simulations_v2_raw_RIPRODOTTO.sha256` | Impronta del JSON riprodotto (identico a quello di Gemini); il JSON non è conservato qui per non duplicare materiale di Gemini |
| `MANIFEST_REVISIONE_CLAUDE.sha256` | Impronte dei file di questa cartella |

## Che cosa NON è qui
- Nessun file di Gemini (motore, test, script, JSON, documento): restano nella consegna di Gemini, SHA-256 in `output/hash_ricevuti.txt`.
- I mutanti di `c9_mutazioni.py` (copie modificate del motore di Gemini): si rigenerano eseguendo lo script.

## Riproduzione
Il documento cita le cartelle di lavoro `gemini-v2-link/` (collegamenti ai file di Gemini) e `gemini-v2-riferimento/` (JSON originale). Per riprodurre:
1. creare `gemini-v2-link/` con `prop_risk_engine_v2.py`, `test_prop_risk_v2.py`, `run_simulations_v2.py` di Gemini (verificare gli hash con il loro `MANIFEST_SHA256.txt`);
2. mettere il JSON originale di Gemini in `gemini-v2-riferimento/simulations_v2_raw_GEMINI.json`, **fuori** da `gemini-v2-link/` (lo script di Gemini riscrive il JSON nella propria cartella);
3. eseguire i comandi della §12 del documento. Solo libreria standard di Python (verificato con 3.13).
