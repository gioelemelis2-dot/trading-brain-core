# Documento di continuità

Ultimo aggiornamento: **2026-11-11**. Leggere questo file per primo (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Stato: SVILUPPO SOSPESO, in attesa della revisione di Gemini (decisione D-12)
Fino a nuova indicazione dell'utente Claude **non**:
- avvia nuovi moduli didattici;
- sviluppa il motore quantitativo o altri strumenti;
- modifica le lezioni L2.4–L2.6 né altri propri materiali originali;
- esegue migrazioni o riorganizzazioni;
- modifica i materiali di Gemini;
- avvia autonomamente altre attività.

## Versione di riferimento della revisione
- **Commit `1b051df`** sul branch `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/`.
- Le impronte `collaborazione/pacchetto-per-gemini/MANIFEST.sha256` corrispondono a quel commit (verificato il 2026-11-11: tutte corrette).
- I commit successivi toccano solo continuità e registri; nessun contenuto sotto revisione è cambiato.

## Che cosa riceve Gemini
`collaborazione/pacchetto-per-gemini/`: registro delle 32 affermazioni, formule ed esempi di L2.4–L2.6; domande su architettura e governance (AR-01…AR-14); confronto quantitativo con i quattro scenari S1–S4; materiale sulla verifica delle regole FTMO (checklist sezione C in `revisione-materiali-gemini/`); impronte SHA-256.

## Seconda fase: quando arriva `GEMINI_PEER_REVIEW_CLAUDE.md`
Il dossier sarà depositato da Gemini in `collaborazione/da-gemini/` e **non verrà modificato** da Claude. Procedura prevista:
1. Verificare su quale commit Gemini ha lavorato e che le impronte coincidano.
2. Per ogni contestazione (citata con i codici `L2.x-Axx/Fxx/Exx`, `AR-xx`, `X0x`):
   - riprodurre calcoli ed esempi (script in `strumenti/` e `riferimento_rovina.py`);
   - leggere le fonti citate da Gemini, dichiarando lo stato effettivo (V / V-sec / C / X);
   - classificare: **errore dimostrato di Claude** · **errore di Gemini** · **divergenza metodologica** · **non decidibile con le evidenze disponibili**.
3. Riconoscere esplicitamente gli errori propri; contestare con evidenze le conclusioni non supportate; registrare le divergenze in `collaborazione/DISACCORDI.md`.
4. Scenari S1–S4: pubblicare solo allora i propri risultati e confrontarli con quelli di Gemini entro l'errore Monte Carlo (S1 ha la soluzione in forma chiusa 0,5).
5. Scrivere il **rapporto conclusivo di confronto** (rilievi accolti, respinti con motivazione, divergenze, correzioni proposte con priorità) e presentarlo all'utente.
6. **Nessuna correzione** ai materiali di Claude prima dell'autorizzazione dell'utente dopo la valutazione complessiva.

## Documenti fondativi
Master Mission e Protocollo comune **non ancora ricevuti**. `collaborazione/PROTOCOLLO-OPERATIVO.md` resta **provvisorio** e non li sostituisce (D-09). Alla ricezione: inserimento integrale in `collaborazione/fondamenti/`, poi verifica di coerenza del protocollo operativo e elenco delle differenze all'utente, senza riallineare prima della sua approvazione.

## Altre questioni aperte (ferme)
- Piano di migrazione: sospeso (D-02, D-10).
- Dati del vault per la lezione 0.17: richiesti (`dati/RICHIESTA-DATI-0.17.md`).
- D-08 da confermare.
- Materiali di Gemini (studio FTMO, motore, test, rulebook, Discovery Lab): non ancora ricevuti.

## Dove eravamo nel lavoro (per la ripresa futura)
Modulo 2, unità 2.1: L2.1–L2.6 `in_verifica`; nessuna lezione `verificata`; nessuna padronanza registrata. Roadmap sospesa: `piano/PIANO-ESPANSIONE.md` §6.3-bis.

## Convenzioni da mantenere
- Lingua: italiano. Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Gemini scrive solo in `collaborazione/da-gemini/`; Claude non modifica mai quella cartella.
