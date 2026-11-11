# Documento di continuità

Ultimo aggiornamento: **2026-11-11**, dopo la **preparazione della prima revisione reciproca Claude–Gemini**. Leggere questo file per primo (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Fase attuale: prima revisione reciproca (decisione D-10)
- **Nessuna migrazione** (D-02 sospesa), **nessuna nuova struttura definitiva**, **nuovi cantieri sospesi** (traccia 10.1, generatore HTML, unità 2.2–2.3, correzioni v1, lab).
- Priorità: collaborazione, continuità, verificabilità del materiale già prodotto.

## Dove siamo
- Modulo 2, unità 2.1: L2.1–L2.6 `in_verifica`. Nessuna lezione `verificata`; nessuna padronanza registrata.
- **L2.4, L2.5, L2.6 congelate** per la revisione di Gemini (`collaborazione/LOCK.md`): Claude non le modifica.
- Manuale v1 intatto (artifact `https://claude.ai/artifact/T4xESphh3BmonZPoprQBtb` e `originale/`).
- Materiale pronto per Gemini: `collaborazione/pacchetto-per-gemini/` (registro delle verifiche, domande su architettura e registri, confronto quantitativo, impronte SHA-256).
- Materiale pronto per la revisione dei lavori di Gemini: `collaborazione/revisione-materiali-gemini/` (checklist, modello di rapporto, `strumenti/riferimento_rovina.py` testato contro la formula chiusa della rovina classica).
- Dove Gemini consegna: `collaborazione/da-gemini/consegne/` (con MANIFEST obbligatorio). **Claude non modifica mai quella cartella** (D-11).
- Nessun materiale di Gemini ricevuto finora.

## In attesa dell'utente
1. **Master Mission e Protocollo comune** (testi originali) da inserire in `collaborazione/fondamenti/` (D-09). Il protocollo operativo è provvisorio e non li sostituisce.
2. Avviare Gemini sulla consegna dei suoi materiali (R-007), sugli scenari di confronto (R-008) e sulla revisione di L2.4–L2.6 (R-001).
3. Dati del vault per la lezione 0.17 (`dati/RICHIESTA-DATI-0.17.md`).
4. Conferma o modifica di D-08.

## Prossima azione esatta (quando arrivano i materiali di Gemini)
1. Leggere `collaborazione/LOCK.md` e `collaborazione/da-gemini/` (rapporti e consegne nuove).
2. Per una **consegna**: verificare il MANIFEST (hash), eseguire i test in ambiente pulito, compilare `revisione-materiali-gemini/CHECKLIST-REVISIONE.md`, eseguire `riferimento_rovina.py` sugli scenari S1–S4 e confrontare; scrivere `revisione-materiali-gemini/R-CLAUDE-AAAAMMGG-NN-*.md` dal modello. Non toccare i file di Gemini.
3. Per un **rapporto di revisione** su L2.4–L2.6: controllo di qualità (protocollo §6), esito per ogni codice in `da-claude/ESITI.md`; modifiche alle lezioni solo dopo, sbloccando il congelamento in `LOCK.md`.
4. Aggiornare registri, `LOCK.md` e questo file. Non riprendere i cantieri sospesi senza via libera dell'utente.

## Convenzioni da mantenere
- Lingua: italiano. Riquadri del v1: Definizione · Esempio · Errori tipici · Sintesi · Oltre il vault.
- File lezione: `moduli/mXX-nome/L<m>.<n>-titolo.md`, intestazione YAML (id, versione, data, stato, revisione_entro).
- Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Branch di lavoro: `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/`.
- Gemini scrive solo in `collaborazione/da-gemini/` su branch `gemini/<argomento>`.
