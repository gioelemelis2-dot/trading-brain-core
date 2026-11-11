# Generatori di dati SIMULATI

Nessuna serie qui descritta rappresenta un mercato reale. Servono solo a testare il codice o a illustrare un concetto.

| Nome | Generatore | Parametri | Uso | Script |
|---|---|---|---|---|
| GBM-017 | Moto geometrico browniano, 8 passi intragiornalieri + rumore d'apertura | n = 2600 giorni, seme 17, deriva 0,02%/giorno, σ ≈ 1,1%/giorno, σ apertura 0,3% | Test del codice di `riproduci_017.py` (una serie gaussiana **non** deve mostrare code grasse) | `strumenti/riproduci_017.py`, funzione `serie_simulata()` |
