# Journal operativo — conto demo broker ECN MT5 50.000 USD (XAU/USD)

Cartella dei dati del journal del Guardian (`brain/guardian/journal/`) per il conto demo del Gate 1.

- I file del journal (`trade.jsonl`, `decisione.jsonl`, `stato.jsonl`, `previsione.jsonl`, `ancora_integrita.json`, `.journal.lock`) sono **dati personali**: il `.gitignore` di questa cartella li esclude da git (DA-16). Restano solo in locale.
- Uso, dalla cartella `brain/guardian/`:
  ```bash
  TRADING_JOURNAL_DIR=../dati/operativo/journal_broker_mt5_50k python3 -s -B -m journal.journal verifica
  ```
- **Protezione dell'integrità:** tenere l'ancora fuori da questa cartella (`TRADING_JOURNAL_ANCHOR=<percorso separato>`). Dopo ogni sessione annotare altrove l'impronta stampata da `python3 -m journal.journal ancora`, e verificare con `verifica --impronta <sha256>`. Dettagli in `brain/guardian/journal/LEGGIMI.md`.
- Scheda del conto: `brain/dati/reali/demo_broker_mt5_50k_xauusd.toml`.
- Inizializzata il 12/11/2026, vuota: nessun dato registrato.
