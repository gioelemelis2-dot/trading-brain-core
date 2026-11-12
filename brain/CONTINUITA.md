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
**Revisione V3.1: completata il 12/11/2026.**
- Cartella: `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/`.
- Esito: motore corretto, pacchetto non validato (N-01, N-02).
- Antigravity ha risposto con la V3.2.

**Parte B: completata il 12/11/2026.** `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` (proposta, **non implementata**; 5 decisioni richieste all'utente, §10).

**Revisione V3.2: completata il 12/11/2026.**
- Cartella: `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/`.
- Pacchetto ricevuto: ZIP `989dd288…`, manifest 15/15. Non archiviato nel Brain.
- Esito: **VALIDATA CON RISERVE**.
  - Q-01, Q-02 (V02–V12 11/11), Q-03, Q-04, Q-05 e Q-08 risolti; Q-06 in parte.
  - Riserve non bloccanti S-01…S-09; la più rilevante è S-01: il valore simulato 0,8596 chiamato «benchmark analitico» (l'esatto è 0,8572).
  - Proposte **non applicate** (eventuale V3.3 minore).
- Q-07 e Q-09 fuori perimetro.

**Revisione V3.3: completata il 12/11/2026.**
- Cartella: `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/`.
- Pacchetto ricevuto: ZIP `6fb9d76e…`, manifest 18/18. Non archiviato nel Brain.
- Esito: **VALIDATA CON RISERVE**.
  - S-01…S-09 risolte (S-07 in parte); software corretto; risultati identici alla V3.2.
  - Riserve nuove T-01…T-05, documentali e di copertura:
    - T-01: mutazioni dichiarate «21/21» non riproducibili; V22 sopravvive; con le definizioni di Claude 21/24;
    - T-02: precisione fittizia dei valori esatti;
    - T-03: README attribuisce a Claude la revisione V3.3 prima che esista.
  - Proposto un errata, non un nuovo ciclo.

**Decisioni dell'utente recepite (12/11/2026):**
- V3.3 congelata con riserve; T-01…T-05 requisiti di ingresso della successiva fase tecnica;
- Trading Guardian iniziale G0 consultivo.

**Audit architetturale della revisione V2 di Gemini: completato il 12/11/2026.**
- Cartella: `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/`.
- Contenuto: audit, affermazioni e fonti, registro delle divergenze D-01…D-28, pacchetto per una revisione esterna.
- Esito: buona base di principi, non ancora base esecutiva. Rilievi principali:
  - modello a 5 tipi non progettato;
  - errori bibliografici;
  - stato della roadmap dichiarato in modo prematuro;
  - memoria condivisa inesistente nei fatti;
  - contaminazione delle ipotesi da addestramento.

**Valutazione della controverifica di Gemini: completata il 12/11/2026** (`R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/`): utile come riconoscimento degli errori, insufficiente come verifica indipendente (Area G e autocritica assenti, nessun disaccordo, proposte trasformate in decisioni). Decisioni consolidate in §7.

**Registro unico delle decisioni aperte: creato il 12/11/2026** (`governance/DECISIONI-APERTE.md`, DA-01…DA-18; bloccanti DA-01, DA-03, DA-15). Decisioni dell'utente del 12/11 registrate in `governance/DECISIONI.md` (D-14…D-18). Pacchetto per la revisione esterna consegnato in chat (istruzioni in `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/`).

**Lavoro del 12/11/2026 dopo le decisioni D-19…D-23:**
- errata V3.3 chiusa come addendum (`collaborazione/da-claude/ERRATA-V3_3/`, 24/24 mutanti non equivalenti uccisi);
- revisione esterna di ChatGPT archiviata, con risposta;
- regole FTMO verificate sulla fonte ufficiale e rulebook separato (`guardian/regole/`);
- modello epistemico (`governance/MODELLO-EPISTEMICO.md`);
- **G0 minimo** e **journal** (`guardian/`, 24 test superati).

Il G0 **non** è ancora utilizzabile per decidere: serve la riconciliazione con un estratto conto (DA-25). Il repository nuovo e privato (D-19) va creato dall'utente; poi va spostato il Brain e archiviate le consegne di Gemini.

**Ora: fermo in attesa dell'utente**, per:
- rispondere alle decisioni di `governance/DECISIONI-APERTE.md`, a partire da quelle bloccanti;
- valutare la revisione V3.3 e decidere se applicare l'errata (T-01…T-05) all'inizio della fase successiva;
- prendere le decisioni elencate nell'audit architetturale (§10) e nella valutazione della controverifica (§7);
- avviare Q-09 (Trading Guardian) e Q-07;
- prendere le decisioni della proposta della Parte B.

## Correzioni note ancora da applicare (dopo il via libera)
- Contestazione, punto C-04: il rimando "(§3, C-05)" va corretto in "(§3, C-06)".
- Registri: seconda revisione e stato dello Studio 01 nel `REGISTRO-CONOSCENZE.md`; Q-01…Q-07 in `DOMANDE-APERTE.md`; conteggio della bibliografia (audit I-02, I-03, I-06).

## Ripresa dopo interruzioni
Prompt pronto in [`PROMPT-RIPRESA.md`](PROMPT-RIPRESA.md). Regola: prima di un lavoro lungo, Claude programma un messaggio di ripresa con quel prompt; senza lavoro in corso non programma nulla.

## Convenzioni da mantenere
- Lingua: italiano. Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Branch di lavoro: `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/` (migrazione sospesa).
- Gemini scrive solo in `collaborazione/da-gemini/`; Claude non modifica mai i materiali di Gemini.
