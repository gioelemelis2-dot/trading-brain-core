# Procedura prima e dopo l'assistenza del Mac

**Scritta il 18/11/2026 su richiesta del titolare.** Il Mac si spegne anche con la batteria carica e andrà in assistenza.
**Promemoria per Claude:** quando il titolare dice che porta il Mac in assistenza, si riprende da qui, passo per passo.

## Che cosa c'è dove

| Che cosa | Dove sta | Rischio se il Mac si rompe |
|---|---|---|
| Codice, test, registri, decisioni, rapporti di Gemini e del DGS, roadmap | **GitHub**, ramo `feat/esecutore-h002` (ogni passo è pubblicato) | nessuno |
| Chat di ChatGPT | cloud di OpenAI | nessuno |
| **Dati veri** (`brain/dati/reali/`: cache Dukascopy BID e ASK, registri dello scaricamento con le impronte) | **solo sul Mac**, fuori da GitHub per scelta | **alto**: riscaricarli richiede giorni |
| Log dello scaricamento (`~/scarica_storico.log`, `~/scarica_ask.log`) | solo sul Mac | basso |
| Lavoro di Gemini in corso (cartelle `~/Downloads/tb-r16`, `tb-r17`) | sul Mac finché Gemini non fa push | medio |

## Copie di sicurezza registrate

| Data | File | Dimensione | SHA-256 | Contenuto |
|---|---|---|---|---|
| 18/11/2026 13:42 | `~/Desktop/dati_reali_20261118.zip` | 136 MB | `0aec0b91f6a6f1633b301572261ebef534f626c4af488acc8f41f19e10d14113` | `brain/dati/reali/` completo: BID 2005–2023 controllato, sviluppo, ASK parziale (fino al 02/02/2013 circa), registri dello scaricamento |

**Regola:** lo zip contiene la riserva sigillata. Si copia, non si apre e non si guarda.

## PRIMA dell'assistenza

1. **Fine dell'ASK**, se il Mac regge: si aspetta la riga `FINITO ASK` in `~/scarica_ask.log`. Se il Mac peggiora, si porta comunque: lo scaricamento riprende dal primo giorno mancante.
2. **Controllo della cache ASK** (solo conteggi; il comando lo prepara Claude).
3. **Copia finale** di `brain/dati/reali/` con i log:
   ```bash
   cd ~/Downloads/trading-brain-core/brain/dati && cp ~/scarica_*.log reali/ && zip -rq ~/Desktop/dati_reali_FINALE.zip reali && shasum -a 256 ~/Desktop/dati_reali_FINALE.zip
   ```
   L'impronta si comunica a Claude, che la registra qui.
4. **Due copie fuori dal Mac:** chiavetta USB o disco esterno, più iCloud Drive o Google Drive. Su ogni copia si controlla `shasum -a 256 <file>`: deve dare la stessa impronta.
5. **Niente lavoro non pubblicato.** Nel Terminale:
   ```bash
   cd ~/Downloads/trading-brain-core && git status --short | head; git fetch -q origin && git log --oneline origin/feat/esecutore-h002..HEAD
   ```
   Se compaiono righe, si avvisa Claude prima di consegnare il Mac. Lo stesso controllo vale per le cartelle di Gemini (`~/Downloads/tb-r17`): Gemini deve aver fatto push.
6. Se c'è un disco esterno: un backup completo con **Time Machine**, come garanzia in più.

## DOPO l'assistenza (o su un altro computer)

1. Si scarica il repository da GitHub, ramo `feat/esecutore-h002`.
2. Si controlla l'impronta dello zip (`shasum -a 256`), che deve coincidere con quella registrata qui, e lo si estrae in `brain/dati/` senza aprire i file.
3. Claude prepara i comandi di controllo: `controlla_cache` su BID e ASK (solo conteggi), confrontati con quelli registrati, e il riavvio dello scaricamento se l'ASK non era finito.
4. Si registra l'evento nel REGISTRO-MODIFICHE. Copiare ed estrarre file non è una lettura dei dati: il censimento della riserva non cambia.
