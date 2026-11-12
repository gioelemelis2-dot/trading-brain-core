# Journal del Trading Brain

Creato da Claude (D-23) e affidato all'utente per la compilazione, con l'aiuto di Claude in sessione.

## Che cosa registra
| Registro | Contenuto | Natura |
|---|---|---|
| `trade` | simbolo, direzione, orari, ingresso, stop, uscita, quantità, P/L, setup, checklist, voto di aderenza (1–5), deviazioni | MISURE (dalla piattaforma o dichiarate, con `fonte`) |
| `decisione` | raccomandazione del G0, decisione dell'utente, deroga sì/no e **motivo** | MISURA dell'atto di decidere |
| `stato` | ore di sonno, stato emotivo, note | **dati personali sensibili**, facoltativi |
| `previsione` | previsioni probabilistiche di utente, Claude e Gemini, con scadenza e poi esito | per il Brier score e la calibrazione |

Validazione **all'ingresso** (`valida`, chiamata da `aggiungi`): un record malformato, una volta nella catena, non si può più togliere.
- Orari: formato unico `AAAA-MM-GGTHH:MM:SS[.frazione da 1 a 6 cifre]` seguito da `Z` o `+00:00`, identico su ogni versione di Python dalla 3.9 (Python 3.11+ di suo accetterebbe anche forme che 3.9 rifiuta: un journal valido su una macchina lo è così anche sulle altre); `chiuso_utc` non precede `aperto_utc`. Date (`stato.data`): `AAAA-MM-GG`.
- `probabilita`: numero finito tra 0 e 1, come `int`, `float`, `Decimal` o testo numerico. I `Decimal` sono registrati come testo, per conservarne la precisione esatta.
- Numeri: finiti (niente testo, NaN o infiniti). `ingresso`, `stop`, `quantita`, `uscita` e `target` maggiori di zero; `ore_sonno` tra 0 e 24; `data` come data ISO-8601.
- Riferimenti: `corregge` e `chiude` devono puntare a un record esistente dello stesso registro.
- Previsioni ed esiti (`controlla_riferimenti`, applicato da `aggiungi` e ripetuto da `verifica`):
  - `corregge` collega record della stessa natura (previsione → previsione, esito → esito);
  - `chiude` punta all'id **radice** di una previsione, non a una sua correzione né a un esito;
  - una previsione ha un solo esito originale: per cambiarlo si scrive una correzione (`corregge`), che chiude la stessa previsione.
- Booleani: `true`/`false` non valgono come numeri (`probabilita`, `esito`, `aderenza`, prezzi e quantità), anche se in Python `True == 1`.
- Gli indicatori calcolano con `Decimal`, mai con `float` (il Brier score, una statistica, è in `float`).

Concorrenza: `aggiungi` lavora sotto un lock esclusivo (`.journal.lock` nella cartella dei dati).
- Su Unix si usa `fcntl.flock`, che il sistema rilascia anche se il processo termina.
- Altrimenti un file di lock creato in modo esclusivo, rimosso alla fine.
- Dopo 30 secondi di attesa: errore esplicito, mai una scrittura non protetta. Se un'interruzione lascia il file di lock (solo nel ripiego), l'errore dice di rimuoverlo a mano.
- `verifica` non prende il lock (non scrive nulla): eseguita **durante** una scrittura può segnalare una differenza transitoria fra l'ultima riga e l'ancora, che sparisce rieseguendola.

Correzioni: `versioni_finali` applica `corregge`, anche a catena (una correzione di una correzione). Brier score e indicatori usano sempre l'ultima versione.

## Garanzie
- **Sola aggiunta.** Una correzione è un nuovo record con `corregge` = id del record corretto.
- **Catena di hash.** Ogni riga contiene l'hash della precedente: scopre modifiche e cancellazioni delle righe che hanno un successore. Da sola **non** scopre la modifica dell'ultima riga, il troncamento della coda né una riscrittura completa.
- **Ancora di integrità** (`ancora_integrita.json`): numero di righe e SHA-256 dell'ultima riga di ogni registro, aggiornata da `aggiungi` e controllata da `verifica`. Scopre anche i tre casi precedenti.
  - **Limite:** se l'ancora sta nella stessa cartella dei dati, chi riscrive deliberatamente i dati può riscrivere anche l'ancora.
  - Per questo l'ancora può stare in un percorso separato (`TRADING_JOURNAL_ANCHOR`), e `python3 -m journal.journal ancora` stampa un'impronta da annotare fuori dal journal (commit, messaggio, nota).
  - `python3 -m journal.journal verifica --impronta <sha256>` confronta l'ancora con l'impronta annotata: rileva anche la **cancellazione totale** di dati e ancora, che senza impronta passerebbe per un journal vuoto e integro.
  - L'impronta cambia a ogni `aggiungi`: va annotata di nuovo dopo ogni registrazione, o almeno a fine sessione.
  - Se un'interruzione avviene tra la scrittura della riga e quella dell'ancora, `verifica` segnala la discrepanza: si controlla l'ultima riga e si riallinea l'ancora solo dopo averla verificata.
- **Impegni sigillati** (DA-07): `sigilla` produce un impegno SHA-256 con nonce segreto di 256 bit. Non è una firma e non prova chi l'ha creato.
- **Indicatori comportamentali** (`indicatori.py`): metriche oggettive come DERIVATI. Il pattern R1 è un'IPOTESI («compatibile con un rientro impulsivo») ed è **spento** finché l'utente non fissa i parametri.

## Dove stanno i dati: decisione dell'utente
- Predefinito: `journal/dati/`, **esclusa da git** (contiene un `.gitignore`), oppure la cartella indicata da `TRADING_JOURNAL_DIR`.
- L'ambiente cloud di Claude è **temporaneo**: senza una scelta, i dati inseriti qui andrebbero persi alla chiusura della sessione. Le alternative:
  - **A.** il journal vive sul **tuo computer**: lo compili tu, e in sessione mi incolli gli estratti da analizzare;
  - **B.** il journal vive nel **repository privato** (D-19): io registro le voci che mi detti in chat e le committo. Comodo, ma i dati personali (soprattutto `stato`) finiscono su GitHub;
  - **C.** misto: `trade`, `decisione` e `previsione` nel repository privato; `stato` solo sul tuo computer.

## Uso
Dalla cartella `guardian/`:
```bash
python3 -s -B -m journal.journal aggiungi trade '{"simbolo":"EURUSD","direzione":"long","aperto_utc":"2026-11-13T09:00:00Z","ingresso":"1.08500","stop":"1.08300","quantita":"1","fonte":"MT5"}'
```
```bash
python3 -s -B -m journal.journal verifica
```
```bash
python3 -s -B -m journal.journal brier
```
