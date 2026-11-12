# Documento di continuità

Ultimo aggiornamento: **2026-11-11**, dopo l'audit architetturale. Leggere questo file per primo (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Stato
- **Sviluppo sospeso** (D-12): nessun nuovo modulo, nessuno sviluppo del motore quantitativo, nessuna modifica a L2.1–L2.6 né ai materiali di Antigravity, nessuna migrazione o riorganizzazione.
- **Audit architetturale concluso** (D-13): `audit/AUDIT-ARCH-20261111/`, sintesi in `RELAZIONE-AUDIT.md`, con 7 decisioni richieste all'utente (§5) e un piano a tre mesi **proposto, non approvato** (`07-PRIORITA-TRE-MESI.md`).
- **Ciclo di revisione V2/V3 di Antigravity:**
  - seconda revisione V2 (`collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/`, commit `3bbe137`) con errata (`a764e61`); contestazione C-01…C-17 in `collaborazione/da-claude/`;
  - risposta di Antigravity e pacchetto V3 ricevuti come archivio ZIP in conversazione (SHA-256 `6c64a3a4…`), **non archiviati nel Brain**;
  - **revisione conclusiva V3** in `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/`: validazione **non conclusa**. Punti: 9 risolti, 2 risolti con limitazione, 5 non risolti, 1 non verificabile; nuovi problemi N-01…N-09 (i più gravi: CRN non accoppiati tra sfide, MAE con parametri fissi, attribuzione a Claude nell'intestazione del motore, documentazione incoerente su Kelly). Proposte P-01…P-11 **non applicate**;
  - revisione V3: in attesa della valutazione dell'utente; V3.1 ricevuta (ZIP `99e8f0bd…`) e revisionata il 12/11/2026 (vedi sotto).
- Lezioni: L2.1–L2.6 `in_verifica`; nessuna `verificata`; nessun cancello superato.
- Master Mission e Protocollo comune: non ancora ricevuti; protocollo operativo provvisorio (D-09).

## Prossima azione esatta
**Parte A (revisione V3.1): completata il 12/11/2026.** `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/`: motore corretto e riproducibile; pacchetto **non validato** (N-01 intervallo di Kelly etichettato 95% ma ±1 errore standard; N-02 test 5/12 mutanti). Proposte Q-01…Q-09 **non applicate**, da sottoporre ad Antigravity dopo l'approvazione dell'utente.
**Parte B: completata il 12/11/2026.** `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` (proposta, **non implementata**; 5 decisioni richieste all'utente, §10).
**Ora: fermo in attesa dell'utente** (valutazione della revisione V3.1, proposte Q-01…Q-09, decisioni della proposta).

## Correzioni note ancora da applicare (dopo il via libera)
- Contestazione, punto C-04: il rimando "(§3, C-05)" va corretto in "(§3, C-06)".
- Registri: seconda revisione e stato dello Studio 01 nel `REGISTRO-CONOSCENZE.md`; Q-01…Q-07 in `DOMANDE-APERTE.md`; conteggio della bibliografia (audit I-02, I-03, I-06).

## Ripresa dopo interruzioni
Prompt pronto in [`PROMPT-RIPRESA.md`](PROMPT-RIPRESA.md). Regola: prima di un lavoro lungo, Claude programma un messaggio di ripresa con quel prompt; senza lavoro in corso non programma nulla.

## Convenzioni da mantenere
- Lingua: italiano. Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Branch di lavoro: `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/` (migrazione sospesa).
- Gemini scrive solo in `collaborazione/da-gemini/`; Claude non modifica mai i materiali di Gemini.
