# Trading Guardian G0 (consultivo)

**Che cosa fa (D-16):** calcola, avvisa, registra. **Non** blocca ordini, **non** li intercetta, **non** accede al conto in scrittura.

**Stato nel ciclo di vita** (modello in `governance/MODELLO-EPISTEMICO.md`):

| Componente | Stato | Che cosa manca |
|---|---|---|
| Regole della prop firm FTMO (`regole/prop_firm_ftmo.toml`) | verificate sulla fonte ufficiale il 12/11/2026 | dettagli dei tipi di conto Standard e Swing (FAQ); prossima verifica 12/02/2027 |
| Regole personali (`regole/regole_personali.toml`) | **proposta** | conferma dell'utente, regola per regola |
| Calcoli G0 (`g0/`) | implementati e testati (44 test unitari) | **validazione**: riconciliazione con un estratto conto reale e con le specifiche del broker |
| Journal (`journal/`) | implementato e testato (32 test: trade sovrapposti esclusi da R1, riferimenti fantasma rifiutati, lock anche in verifica e recupero sicuro dei lock orfani, formato orari unico su ogni versione, probabilità Decimal, lock esclusivo, catena di hash, ancora e impronta esterna, validazione all'ingresso, coerenza di correzioni ed esiti, Brier con correzioni, sigilli, R1, Decimal e orari ISO-8601) | scelta di dove conservare i dati (`journal/LEGGIMI.md`, alternative A/B/C) |
| Uso per decidere | **NON AUTORIZZATO** | la scheda lo dichiara in prima riga finché `riconciliato = false` |

## Componenti
- `g0/valori.py`: schema dei valori. Un numero senza tipo, fonte e stato di verifica non si può costruire. Propaga tipo, condizioni, verifica e NON STIMABILE. Una stima non può allargare un limite.
- `g0/strumenti.py`: perdita allo stop per FX, futures e CFD, con conversione nella valuta del conto. I futures si descrivono **solo** con passo e valore del tick (nessuna dimensione del contratto fittizia); FX e CFD richiedono la dimensione del contratto. Simbolo, fonte e valuta del profitto devono essere testi non vuoti. Prezzi, quantità, cambi, specifiche e capitale iniziale devono essere positivi; uno stop uguale al prezzo di partenza è rifiutato; le commissioni devono essere finite e non negative (0 per i conti solo spread), perché una commissione negativa ridurrebbe la perdita allo stop. Futures: la distanza deve essere un multiplo del tick; una tolleranza di 1e-9 tick assorbe solo il rumore di un `Decimal` costruito da un float.
- **Dati NON STIMABILI:** margini, stop residui e scenario di stress li propagano come NON STIMABILI. Ogni confronto con un dato NON STIMABILE diventa un avviso «controllo non verificabile», mai un errore né un controllo dato per superato; con un avviso la raccomandazione è «non entrare». È un DERIVATO condizionato a H_esec: gap, slippage e lato del trigger sono esclusi e vanno in una riserva separata.
- `g0/limiti.py`: limiti FTMO (2-Step, 1-Step, Instant) esattamente come nelle regole ufficiali; margini; stop residui; scenario di stress (tutte le posizioni allo stop).
- `g0/scheda.py`: scheda consultiva in ordine fisso (misure → regole → limiti → trade previsto → stress → riserve → avvisi → regole personali → raccomandazione → decisione).
  - Lo stress è confrontato con il limite **giornaliero e con quello totale**.
  - Le regole personali si leggono da `regole/regole_personali.toml`: si applicano **solo** quelle con `confermata = true`. P-01 (rischio del trade e size dopo una perdita), P-05 (limite personale giornaliero, segnalato se non è più stretto di quello della prop firm), P-11, P-14 e P-15 hanno un controllo automatico; le altre restano domande della checklist; i dati di sessione mancanti sono dichiarati. Soglie e dati di sessione non validi (booleani, negativi, NaN, infiniti, ore di sonno oltre 24, perdite consecutive non intere) producono un avviso «non valido» e la regola resta non verificata. P-05 segnala trade e stress anche quando il limite personale è già superato.
  - I dati di sessione facoltativi stanno nella sezione `[sessione]`: `minuti_da_ultima_perdita`, `ore_sonno`, `perdite_consecutive_oggi`, `ultima_operazione_in_perdita` (vero/falso), `size_precedente`.

## Uso
Dalla cartella `guardian/`:
```bash
python3 -s -B -m g0.scheda esempi/situazione_esempio.toml
```
```bash
python3 -s -B -m unittest discover -s test -v
```
Risultato: **77 test, tutti superati** con `-W error`, su Python 3.9, 3.11, 3.12 e 3.13:
- 18 G0 e 6 journal originari;
- 17 in `test/test_fix_g0_journal.py`: 5 del mandato «Binario A», 7 del contro-audit e 5 del mandato notturno;
- 11 in `test/test_mutanti_g0_journal.py`, aggiunti per uccidere i mutanti sopravvissuti;
- 9 in `test/test_compatibilita_e_concorrenza.py`: Python 3.9, probabilità `Decimal`, lock concorrente;
- 16 in `test/test_red_team_guardian.py` (compresa la visualizzazione delle frazioni con 3 decimali): rilievi dell'audit esterno «Red Team», il rilievo MEDIO dell'audit di verifica e ALTO-8 (race nel recupero del lock orfano).

Mutation testing (dalla cartella `guardian/test/`, con una cartella temporanea per le copie):
```bash
python3 -s -B mutazioni_g0_journal.py /tmp/mutanti_g0
```
Risultato, su tutti e 7 i file operativi (compreso `g0/_toml.py`):
- con Python 3.13: **80/80 mutanti non equivalenti uccisi**;
- con Python 3.9: **79/79**. V48 lì è equivalente: prima di 3.11 `date.fromisoformat` accetta già solo `AAAA-MM-GG`; lo script lo dichiara con la versione minima.

In più c'è 1 mutante equivalente su ogni versione (E01), dichiarato con la motivazione.

Storia:
- 30/44 con 41 test;
- 44/44 con 52;
- dopo la rifinitura per Python 3.9: 58/58 su 3.13, ma 55/58 su 3.9;
- il parser TOML minimale era controllato solo contro `tomllib`, assente proprio su 3.9: con un risultato atteso scritto nel test, 57/57.
- bonifica Red Team: 19 mutanti nuovi, tutti uccisi al primo giro (77/77 su 3.13, 76/76 su 3.9);
- correzione MEDIO di `versioni_finali`: 1 mutante nuovo (78/78 su 3.13, 77/77 su 3.9);
- correzione ALTO-8 (recupero del lock orfano): 1 mutante nuovo (79/79 su 3.13, 78/78 su 3.9);
- frazioni con 3 decimali nella scheda: 1 mutante nuovo (80/80 su 3.13, 79/79 su 3.9). Dettaglio in `collaborazione/da-claude/CONSEGNA_FIX_G0/`.
Requisiti: Python 3.9 o successivo, sola libreria standard.
- Il TOML si legge con `tomllib` (3.11+), altrimenti con `tomli` se installato, altrimenti con il parser minimale di `g0/_toml.py`.
- Il parser minimale copre solo il sottoinsieme usato dai file del Guardian; ogni altro costrutto è un errore esplicito con il numero di riga.
- Un test confronta il suo risultato con `tomllib` su tutti i file TOML del Guardian.

## Limiti dichiarati
- Le posizioni aperte vanno descritte con il **prezzo attuale**: la perdita ulteriore si misura da lì allo stop, perché l'equity include già il P/L flottante.
- La conversione al prezzo dello stop (conto nella valuta base della coppia) è esatta solo se il broker converte all'uscita: da verificare nella riconciliazione.
- Swap, finanziamento, spread al trigger e regole di arrotondamento del broker non sono modellati.
- L'esempio in `esempi/` è inventato ed etichettato `[ESEMPIO]`.
