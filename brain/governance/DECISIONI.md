# Registro delle decisioni

Ogni decisione: id · data · chi · decisione · motivazione · conseguenze · stato.

| Id | Data | Chi | Decisione | Motivazione | Conseguenze | Stato |
|---|---|---|---|---|---|---|
| D-01 | 2026-11-11 | Claude, approvata dall'utente | Architettura "opzione C": spina 0–9 + Modulo 10 a tracce con prerequisiti | Conserva numerazione e cancelli del v1; la matematica arriva quando serve | `architettura/ARCHITETTURA.md` | attiva |
| D-02 | 2026-11-11 | Utente | Il Trading Brain diventerà un **progetto autonomo**, separato da l-Altro | Il Brain non ha legami con l-Altro | Piano in `piano/PIANO-MIGRAZIONE.md`; **nessuno spostamento senza approvazione esplicita** | **sospesa** (D-10): prima si coordinano i materiali dei due sistemi |
| D-03 | 2026-11-11 | Utente | I Markdown sono la fonte primaria; l'HTML è una versione **generata e aggiornabile**, in stile v1 | La conoscenza deve stare in file versionabili e verificabili | Generatore da costruire (sprint dedicato); vietato modificare l'HTML generato a mano | attiva |
| D-04 | 2026-11-11 | Utente | Dati mancanti del vault **non** si sostituiscono con dati inventati o simulati non dichiarati | Rigore | `dati/RICHIESTA-DATI-0.17.md`; dati simulati solo per test, etichettati | attiva |
| D-05 | 2026-11-11 | Utente | Separare sempre verificato / in verifica / ipotesi / esercitazioni / dati simulati / dati reali | Rigore e tracciabilità | `governance/STANDARD.md` §8–9 | attiva |
| D-06 | 2026-11-11 | Utente | Collaborazione strutturata Claude–Gemini sullo **stesso** Brain; integrazione solo dopo controllo di qualità; mai modifiche simultanee agli stessi file | Migliorare la qualità con verifica indipendente, senza creare due progetti | `collaborazione/` | attiva |
| D-07 | 2026-11-11 | Utente | Ogni migrazione o modifica strutturale importante richiede un piano e l'approvazione dell'utente | Controllo del progetto | Vale per Claude e Gemini | attiva |
| D-08 | 2026-11-11 | Claude | Le aggiunte non distruttive (nuovi file, nuove cartelle di supporto come `dati/`, `collaborazione/`) non sono considerate modifiche strutturali importanti | Permettono di proseguire la roadmap senza bloccarsi | Spostamenti, rinomine, cancellazioni e cambi di architettura restano soggetti a D-07 | **da confermare dall'utente** |
| D-09 | 2026-11-11 | Utente | Master Mission e Protocollo comune vanno **inseriti esplicitamente** nel progetto; il protocollo operativo di Claude **non li sostituisce** | I testi originali non erano reperibili | `collaborazione/fondamenti/`; protocollo operativo marcato PROVVISORIO | attiva, in attesa dei testi |
| D-10 | 2026-11-11 | Utente | Prima fase di collaborazione: **nessuna migrazione**, **nessuna nuova struttura definitiva**, **sospesi i nuovi cantieri non urgenti** (traccia 10.1, generatore HTML, unità 2.2–2.3); priorità a collaborazione, continuità, verificabilità | Coordinare prima il materiale prodotto dai due sistemi | Le cartelle di collaborazione create in questa fase sono provvisorie | attiva |
| D-11 | 2026-11-11 | Utente | I materiali di Gemini non si sovrascrivono; nessuna modifica simultanea agli stessi file; ogni integrazione è una proposta documentata sottoposta a controllo | Proteggere il lavoro di entrambi | `collaborazione/da-gemini/consegne/` intoccabile per Claude; L2.4–L2.6 congelate durante la revisione di Gemini | attiva |
