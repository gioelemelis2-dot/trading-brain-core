# Registro delle modifiche

Formato: data · versione della base · cosa · perché · file.

## 2026-11-11 · v1.0 della base modulare (sprint S1)

**Aggiunto**
- Copia integrale del Manuale del Brain v1 (artifact del 23/09/2026) in `originale/` + estrazione testuale. Nessuna modifica al contenuto originale.
- Governance: `STANDARD.md` (fonti F1–F7, evidenze E1–E7, stati V/V-sec/C/X, modello di lezione a 20 sezioni, livelli L1–L5, regole di sicurezza), questo registro, `REGISTRO-CONOSCENZE.md`.
- Audit: diagnosi, verifica di 18 citazioni + 11 calcoli + 6 affermazioni da qualificare, matrice delle lacune per 17 aree.
- Mappa delle competenze (A–S + nuove aree T–Z) e mappa delle dipendenze con due catene causali con livelli di evidenza.
- Architettura (opzione C: spina 0–9 + Modulo 10 a tracce), corrispondenza vecchio → nuovo.
- Bibliografia strategica (185 voci; 25 confermate in sessione come V o V-sec, il resto marcato C).
- Piano di espansione con punteggio di priorità e sprint.
- Modulo 2, unità 2.1: lezioni L2.1, L2.2, L2.3 (bozze), protocollo di analisi di un movimento, README con cancello.
- Strumenti: `verifica_m0.py`, `sorpresa_monetaria.py`.
- Glossario (26 voci) e domande aperte (Q1–Q7).
- `CONTINUITA.md`.

**Corretto (nella nuova base, non nell'artifact originale)**
- Individuati 2 errori nel v1 (McLean-Pontiff A7; Novy-Marx/RMW A9) e 8 imprecisioni: elencati in `audit/02-VERIFICA-AFFERMAZIONI.md`, da applicare nello sprint S5.
- L2.1, esercizio 1: soluzione corretta in fase di stesura (3,5–4,5%).

**Non fatto (dichiarato)**
- Nessuna fonte con stato C è stata letta in questa sessione.
- Due siti (gwern.net, counterpointfunds.com) non raggiungibili dalla rete dell'ambiente: il testo di McLean-Pontiff è stato verificato tramite fonti secondarie.
- I valori correnti dei tassi Fed/BCE non sono stati inseriti nelle lezioni (dati letti solo da snippet; vedi Q4).

## 2026-11-11 · v1.1 (sprint S2)

**Decisioni dell'utente recepite** (registrate in `governance/DECISIONI.md`): D-02 progetto autonomo (solo piano, nessuno spostamento), D-03 Markdown fonte primaria e HTML generato, D-04 nessun dato inventato o simulato non dichiarato, D-05 classi di contenuto separate, D-06 collaborazione con Gemini, D-07 approvazione per modifiche strutturali. Proposta D-08 (da confermare).

**Aggiunto**
- `governance/STANDARD.md` §8 classi di contenuto, §9 ciclo di vita delle lezioni, §10 sorgente vs versione generata.
- `governance/DECISIONI.md`.
- `piano/PIANO-MIGRAZIONE.md` (proposta, **non eseguita**).
- `dati/` con regole reali/simulati, `RICHIESTA-DATI-0.17.md`, `simulati/README.md`, `reali/README.md`.
- `strumenti/riproduci_017.py` (testato solo su casi a mano e su serie `[SIMULATO]`), `strumenti/tassi_reali.py`.
- Lezioni **L2.4** Tassi reali e inflazione attesa, **L2.5** Bilancio della banca centrale, **L2.6** Fed/BCE/BoJ/BoE (stato `in_verifica`).
- `collaborazione/`: consegna per Gemini, protocollo operativo, LOCK, disaccordi, modello di rapporto, richieste R-001–R-006, esiti, cartella per i documenti fondativi.
- Bibliografia: 6 nuove fonti V-sec (Gagnon et al. 2011; D'Amico-Kim-Wei; Erb-Harvey 2013; Fed bilancio 2025; BoJ; BoE).
- Glossario +13 voci; domande aperte Q8–Q12.

**Modificato**
- L2.1–L2.3: stato da `bozza` a `in_verifica` (complete, fonti con stato dichiarato; etichette §8 da allineare alla prima revisione).
- `moduli/m02-macro/README.md`: elenco lezioni, cancello dell'unità esteso a L2.4–L2.6.
- `architettura/ARCHITETTURA.md`, `piano/PIANO-ESPANSIONE.md` (S2 concluso, S3 bloccato, nuovo S3-bis generatore HTML), `audit/02-VERIFICA-AFFERMAZIONI.md` (C5), `README.md`.

**Non fatto (dichiarato)**
- Nessun file spostato o rinominato; nessuna modifica all'artifact originale.
- Nessun dato reale scaricato: FRED, Yahoo Finance e Stooq sono rifiutati dalla rete dell'ambiente.
- Master Mission e Protocollo comune dell'utente non trovati (né in conversazione, né su Drive, né tra gli artifact): il protocollo operativo è provvisorio.
- Le fonti V-sec non sono state lette nel testo integrale.
