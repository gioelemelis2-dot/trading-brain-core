# Journal del Trading Brain

Creato da Claude (D-23) e affidato all'utente per la compilazione, con l'aiuto di Claude in sessione.

## Che cosa registra
| Registro | Contenuto | Natura |
|---|---|---|
| `trade` | simbolo, direzione, orari, ingresso, stop, uscita, quantità, P/L, setup, checklist, voto di aderenza (1–5), deviazioni | MISURE (dalla piattaforma o dichiarate, con `fonte`) |
| `decisione` | raccomandazione del G0, decisione dell'utente, deroga sì/no e **motivo** | MISURA dell'atto di decidere |
| `stato` | ore di sonno, stato emotivo, note | **dati personali sensibili**, facoltativi |
| `previsione` | previsioni probabilistiche di utente, Claude e Gemini, con scadenza e poi esito | per il Brier score e la calibrazione |

## Garanzie
- **Sola aggiunta.** Una correzione è un nuovo record con `corregge` = id del record corretto.
- **Catena di hash.** Ogni riga contiene l'hash della precedente; `verifica` scopre modifiche e cancellazioni.
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
