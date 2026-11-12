# Trading Guardian G0 (consultivo)

**Che cosa fa (D-16):** calcola, avvisa, registra. **Non** blocca ordini, **non** li intercetta, **non** accede al conto in scrittura.

**Stato nel ciclo di vita** (modello in `governance/MODELLO-EPISTEMICO.md`):

| Componente | Stato | Che cosa manca |
|---|---|---|
| Regole della prop firm FTMO (`regole/prop_firm_ftmo.toml`) | verificate sulla fonte ufficiale il 12/11/2026 | dettagli dei tipi di conto Standard e Swing (FAQ); prossima verifica 12/02/2027 |
| Regole personali (`regole/regole_personali.toml`) | **proposta** | conferma dell'utente, regola per regola |
| Calcoli G0 (`g0/`) | implementati e testati (18 test unitari) | **validazione**: riconciliazione con un estratto conto reale e con le specifiche del broker |
| Journal (`journal/`) | implementato e testato (6 test: catena di hash, validazione, Brier, sigilli, R1) | scelta di dove conservare i dati (`journal/LEGGIMI.md`, alternative A/B/C) |
| Uso per decidere | **NON AUTORIZZATO** | la scheda lo dichiara in prima riga finché `riconciliato = false` |

## Componenti
- `g0/valori.py`: schema dei valori. Un numero senza tipo, fonte e stato di verifica non si può costruire. Propaga tipo, condizioni, verifica e NON STIMABILE. Una stima non può allargare un limite.
- `g0/strumenti.py`: perdita allo stop per FX, futures e CFD, con conversione nella valuta del conto. È un DERIVATO condizionato a H_esec: gap, slippage e lato del trigger sono esclusi e vanno in una riserva separata.
- `g0/limiti.py`: limiti FTMO (2-Step, 1-Step, Instant) esattamente come nelle regole ufficiali; margini; stop residui; scenario di stress (tutte le posizioni allo stop).
- `g0/scheda.py`: scheda consultiva in ordine fisso (misure → regole → limiti → trade previsto → stress → riserve → avvisi → raccomandazione → decisione).

## Uso
Dalla cartella `guardian/`:
```bash
python3 -s -B -m g0.scheda esempi/situazione_esempio.toml
```
```bash
python3 -s -B -m unittest discover -s test -v
```
Risultato al 12/11/2026: **24 test, tutti superati** (18 G0, 6 journal).
Requisiti: Python 3.11 o successivo, sola libreria standard.

## Limiti dichiarati
- Le posizioni aperte vanno descritte con il **prezzo attuale**: la perdita ulteriore si misura da lì allo stop, perché l'equity include già il P/L flottante.
- La conversione al prezzo dello stop (conto nella valuta base della coppia) è esatta solo se il broker converte all'uscita: da verificare nella riconciliazione.
- Swap, finanziamento, spread al trigger e regole di arrotondamento del broker non sono modellati.
- L'esempio in `esempi/` è inventato ed etichettato `[ESEMPIO]`.
