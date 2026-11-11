# Documento di continuità

Ultimo aggiornamento: **2026-11-11**, dopo l'audit architetturale. Leggere questo file per primo (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Stato
- **Sviluppo sospeso** (D-12): nessun nuovo modulo, nessuno sviluppo del motore quantitativo, nessuna modifica a L2.1–L2.6 né ai materiali di Antigravity, nessuna migrazione o riorganizzazione.
- **Audit architetturale concluso** (D-13): `audit/AUDIT-ARCH-20261111/`, sintesi in `RELAZIONE-AUDIT.md`, con 7 decisioni richieste all'utente (§5) e un piano a tre mesi **proposto, non approvato** (`07-PRIORITA-TRE-MESI.md`).
- **Ciclo di revisione V2 di Antigravity:**
  - seconda revisione di Claude pubblicata (`collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/`, commit `3bbe137`) con errata (`ERRATA.md`, commit `a764e61`);
  - contestazione C-01…C-17 consegnata (`collaborazione/da-claude/CONTESTAZIONE_TECNICA_CLAUDE_PER_ANTIGRAVITY_V2.md`);
  - **in attesa di `ANTIGRAVITY_RESPONSE_TO_CLAUDE_SECOND_REVIEW.md`**.
- Lezioni: L2.1–L2.6 `in_verifica`; nessuna `verificata`; nessun cancello superato.
- Master Mission e Protocollo comune: non ancora ricevuti; protocollo operativo provvisorio (D-09).

## Prossima azione esatta
**Quando arriva la risposta di Antigravity:**
1. Verificare hash e provenienza (manifest; chiarimento su C-16).
2. Per ogni codice C-01…C-17: riprodurre le contro-prove e classificare (errore dimostrato di Claude / errore di Gemini / divergenza metodologica / non decidibile).
3. Pubblicare i risultati degli scenari dove richiesto; scrivere il rapporto conclusivo di confronto; presentarlo all'utente.
4. Nessuna correzione ai materiali di Claude o di Gemini prima dell'autorizzazione dell'utente.

**Senza risposta e senza nuove indicazioni:** nessuna attività. Le proposte non strutturali eseguibili dopo il via libera sono in `audit/AUDIT-ARCH-20261111/RELAZIONE-AUDIT.md` §4.

## Correzioni note ancora da applicare (dopo il via libera)
- Contestazione, punto C-04: il rimando "(§3, C-05)" va corretto in "(§3, C-06)".
- Registri: seconda revisione e stato dello Studio 01 nel `REGISTRO-CONOSCENZE.md`; Q-01…Q-07 in `DOMANDE-APERTE.md`; conteggio della bibliografia (audit I-02, I-03, I-06).

## Convenzioni da mantenere
- Lingua: italiano. Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Branch di lavoro: `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/` (migrazione sospesa).
- Gemini scrive solo in `collaborazione/da-gemini/`; Claude non modifica mai i materiali di Gemini.
