# Modello epistemico: schema dei valori e mappatura verso `STANDARD.md`

**Stato:** proposta (DA-06), applicata come schema interno del **G0 minimo** (D-20). L'adozione per tutto il Brain resta una decisione dell'utente (DA-06).
**Origine:**
- principio dell'utente (tipi MISURA, DERIVATO DETERMINISTICO, STIMA, IPOTESI, REGOLA; propagazione del tipo più debole);
- audit dell'architettura V2 (§3);
- controverifica di Gemini (A.1–A.4);
- revisione esterna di ChatGPT (§6.3).

## 1. Il principio dell'utente resta intatto
**Regola di propagazione:** il **tipo epistemico** di un risultato è il **più debole** fra i tipi dei suoi input, nell'ordine
`MISURA > DERIVATO > STIMA > IPOTESI`.
Una stima calcolata da ipotesi non diventa mai una misura.

Per non perdere informazione, ogni valore porta altri due campi, distinti dal tipo:
- **operazione**: la natura del calcolo che l'ha prodotto (osservazione, calcolo deterministico, inferenza statistica, assunzione, norma);
- **condizioni**: l'**insieme delle ipotesi** {H₁…Hₖ} da cui dipende, ereditato da tutti gli input (unione).

**Esempio.** P(violazione) calcolata in modo esatto dal reticolo con edge supposto 0,15R:
- `tipo = IPOTESI` (l'input più debole è un'ipotesi);
- `operazione = calcolo deterministico`;
- `condizioni = {H_edge = 0,15R, H_iid, H_esec}`.

Il lettore sa che il numero non è un fatto (tipo), che non c'è rumore di simulazione (operazione) e su che cosa poggia (condizioni). Questo risolve la divergenza D-02 senza sostituire la regola dell'utente.

## 2. La REGOLA è fuori dall'ordine dei tipi
Una regola non è vera o falsa: vale o non vale. Combinata con misure (per esempio margine = equity − limite giornaliero), dà un **DERIVATO**. La regola però trasmette il proprio **stato di verifica**: se la regola è V-sec, anche il derivato porta «regola V-sec».

## 3. Campi di un valore

| Campo | Contenuto | Obbligatorio | Raccordo con `STANDARD.md` |
|---|---|---|---|
| `valore`, `unita` | numero e unità (valuta del conto, frazione, R, minuti…) | sempre | — |
| `tipo` | MISURA, DERIVATO, STIMA, IPOTESI, REGOLA | sempre | nuovo |
| `operazione` | osservazione, calcolo deterministico, inferenza, assunzione, norma | sempre | nuovo |
| `condizioni` | insieme di identificativi di ipotesi (registro delle ipotesi) | se non vuoto | §7 «distinguere ciò che si sa da ciò che si deduce» |
| `incertezza` | «esatto», intervallo con livello e N, oppure **NON STIMABILE** | sempre per STIMA; «esatto» per MISURA e DERIVATO se la precisione è trascurabile | nuovo |
| `fonte` | origine (piattaforma, file, URL), timestamp UTC, versione del codice o della regola | sempre | §1 (rango F1–F7 per le fonti documentali) |
| `qualita` | per MISURA: risoluzione o precisione, flag (dato mancante, ritardato, stimato dal broker) | per MISURA | nuovo |
| `stato_verifica` | fonte: V / V-sec / C / X; ipotesi: aperta / corroborata / falsificata; stima: calibrata / non calibrata | sempre | §3 (V/V-sec/C/X) esteso |
| `evidenza` | E1–E7, solo per affermazioni tratte dalla letteratura | se pertinente | §2 |
| `validazione` | TEORIA, SIMULATO, IN-SAMPLE, OOS, WALK-FORWARD, FORWARD-PAPER, LIVE-REAL | per risultati di ricerca | nuovo (dall'architettura V2 §11.2) |
| `classe` | VERIFICATO, IN VERIFICA, IPOTESI, ESERCIZIO, SIMULATO, REALE | per testi e lezioni | §8 |

Il **ciclo di vita** (progettato → documentato → implementato → testato → validato → validato empiricamente → in uso) riguarda gli **artefatti** (codice, regole, strumenti), non i singoli valori. Si registra nel LEGGIMI di ogni componente.

## 4. Regole di combinazione (applicate nel codice del G0)
1. **Tipo:** il più debole fra gli input (§1). REGOLA non entra nell'ordine.
2. **Condizioni:** unione delle condizioni degli input.
3. **Stato di verifica:** il più debole fra quelli degli input, nell'ordine V > V-sec > C > X.
4. **Incertezza:**
   - se tutti gli input sono «esatti», il risultato è esatto (condizionato);
   - se un input ha un intervallo, il risultato porta un intervallo propagato e dichiarato;
   - se un input è NON STIMABILE, lo è anche il risultato.
5. **NON STIMABILE:** una STIMA è NON STIMABILE *per una decisione* quando il suo intervallo contiene valori che porterebbero a decisioni diverse. Richiede quindi una soglia decisionale dichiarata. Non si usa una soglia fissa di N (D-05).
6. **Limiti:**
   - i limiti calcolati da MISURA e REGOLA si mostrano **prima** di qualsiasi stima;
   - una stima può solo **restringere** un limite, mai allargarlo.
7. **Rischio aggregato:** si chiama **scenario di stress** («tutte le posizioni raggiungono lo stop ed eseguono secondo H_esec»), non «correlazione 1» né «co-monotonicità». Va sempre affiancato da scenari separati di gap, slippage e mancata esecuzione.

## 5. Raccomandazione e decisione
- Il G0 produce **raccomandazioni** (avvisi), che sono derivati dalle regole.
- La **decisione** è dell'utente e si registra nel journal come **MISURA** dell'atto: che cosa è stato deciso, quando, con quali valori visibili, se c'è una deroga e perché.
- La decisione registrata non modifica i valori che l'hanno preceduta.
