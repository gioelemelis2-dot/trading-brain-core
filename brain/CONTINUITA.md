# Documento di continuità

Ultimo aggiornamento: **2026-11-11**, fine sprint **S2**. Leggere questo file per primo all'inizio di ogni sessione (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Dove siamo
- Fasi 1–3 completate; fase 4 (sviluppo) in corso: **Modulo 2, unità 2.1 scritta (L2.1–L2.6), tutte `in_verifica`**. Nessuna lezione è `verificata`; nessuna padronanza registrata.
- Il manuale v1 è intatto (artifact `https://claude.ai/artifact/T4xESphh3BmonZPoprQBtb` e copia in `originale/`). Le correzioni al v1 sono elencate in `audit/02-VERIFICA-AFFERMAZIONI.md` e non ancora applicate (sprint S5).
- Collaborazione con Gemini predisposta in `collaborazione/`; nessun rapporto ricevuto.

## In attesa dell'utente (non procedere senza)
1. **Approvazione del piano di migrazione** (`piano/PIANO-MIGRAZIONE.md`): nome e visibilità del nuovo repository, creazione del repository vuoto, scelta per l-Altro (6a/6b/6c). Fino ad allora: **nessuno spostamento**.
2. **Dati del vault** per la lezione 0.17 (`dati/RICHIESTA-DATI-0.17.md`).
3. **Testi del Master Mission e del Protocollo comune** da copiare in `collaborazione/fondamenti/`.
4. Conferma o modifica di **D-08** (aggiunte non distruttive ≠ modifiche strutturali).
5. Eventuale abilitazione di rete per i siti di dati (es. `fred.stlouisfed.org`) per il lab S3.

## Prossima azione esatta (sprint S4, traccia 10.1 · probabilità e statistica, parte 1)
1. Controllare `collaborazione/LOCK.md` e `collaborazione/da-gemini/` (rapporti nuovi → controllo di qualità prima di tutto).
2. Creare `moduli/m10-tracce/10.1-statistica/` con README e le prime lezioni: variabili casuali e distribuzioni; stima e intervalli di confidenza; test d'ipotesi (ripresa critica di 0.18); regressione lineare; bootstrap. Collegare a 0.10–0.18 senza duplicarle.
3. Ogni lezione: 20 sezioni, etichette di classe (STANDARD §8), fonti con stato, esempi riprodotti da uno script in `strumenti/`, stato `in_verifica`.
4. Poi S3-bis: generatore HTML (`strumenti/genera_manuale.py`) dai Markdown, stile v1.
5. Aggiornare registri, glossario, `LOCK.md` e questo file.

## Convenzioni da mantenere
- Lingua: italiano. Riquadri del v1: Definizione · Esempio · Errori tipici · Sintesi · Oltre il vault.
- File lezione: `moduli/mXX-nome/L<m>.<n>-titolo.md`, intestazione YAML (id, versione, data, stato, revisione_entro).
- Mai segnare una fonte come V senza averla letta. Mai segnare una padronanza senza cancello superato dichiarato dall'utente. Mai presentare dati simulati come reali.
- Branch di lavoro attuale: `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/` (cambierà con la migrazione).
- Gemini scrive solo in `collaborazione/da-gemini/` su branch `gemini/<argomento>`.
