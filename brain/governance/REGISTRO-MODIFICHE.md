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

## 2026-11-11 · v1.2 (preparazione della prima revisione reciproca)

**Decisioni dell'utente recepite**: D-02 sospesa; D-09 (documenti fondativi da inserire, il protocollo provvisorio non li sostituisce); D-10 (nessuna migrazione, nessuna struttura definitiva, cantieri sospesi); D-11 (materiali di Gemini intoccabili, nessuna modifica simultanea, integrazione solo con proposta documentata e controllo).

**Aggiunto (cartelle provvisorie, solo in `collaborazione/`)**
- `pacchetto-per-gemini/`: registro delle verifiche per L2.4–L2.6 (affermazioni, formule, esempi con risultati attesi, domande), domande guida su architettura/registri/governance (AR-01…AR-14), confronto quantitativo con esperimento a 4 scenari, `MANIFEST.sha256`.
- `revisione-materiali-gemini/`: README, checklist (sezioni A–I: integrità, riproducibilità, rulebook e regole FTMO, motore, Monte Carlo, test, Discovery Lab, interpretazione, esito), modello di rapporto (confermati, errori, ipotesi discutibili, dati mancanti, differenze metodologiche, proposte), `strumenti/riferimento_rovina.py` (calcolo esatto + Monte Carlo; test: rovina classica in forma chiusa, monotonia rispetto al limite giornaliero, Monte Carlo entro 4 errori standard).
- `da-gemini/consegne/README.md`: struttura delle consegne e MANIFEST obbligatorio.
- Decisioni D-09–D-11; richieste R-007–R-009.

**Modificato**
- `PROTOCOLLO-OPERATIVO.md` marcato PROVVISORIO (non sostituisce i documenti fondativi); ruoli di scrittura per le nuove cartelle.
- `fondamenti/README.md`: procedura per inserire i testi originali.
- `HANDOFF-GEMINI.md` v1.1: fase attuale, attività 0 (consegna materiali e confronto).
- `LOCK.md`: L2.4–L2.6 congelate; attività sospese.
- `PIANO-ESPANSIONE.md` (§6.3-bis sospensione), `PIANO-MIGRAZIONE.md` (proposta sospesa), `CONTINUITA.md`.

**Non fatto (dichiarato)**
- Nessuna migrazione, nessuna modifica alle lezioni, nessun nuovo cantiere.
- Materiali di Gemini non ancora ricevuti: nessuna revisione eseguita.
- Regole FTMO consultate solo su fonti secondarie (divergenti su punti chiave): non verificate su ftmo.com.

## 2026-11-11 · v1.2.1 (sospensione per la revisione di Gemini)

- Recepita la decisione D-12: sviluppo sospeso; attesa del dossier `GEMINI_PEER_REVIEW_CLAUDE.md`.
- Fissata la **versione di riferimento della revisione: commit `1b051df`**; verificate tutte le impronte di `MANIFEST.sha256`.
- Aggiornati solo `CONTINUITA.md` (procedura della seconda fase), `collaborazione/LOCK.md`, `governance/DECISIONI.md`, questo registro.
- Nessuna modifica a lezioni, strumenti, pacchetto per Gemini, documenti provvisori o materiali di Gemini.

## 2026-11-11 · v1.3 (seconda revisione V2, errata, contestazione, audit architetturale)

- `3bbe137`: seconda revisione indipendente del pacchetto V2 di Antigravity con 11 strumenti di verifica, test aggiuntivi, uscite e impronte (`collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2/`).
- `a764e61`: `ERRATA.md` (4 dei 7, non 6 dei 7) e contestazione tecnica C-01…C-17 in `collaborazione/da-claude/`.
- Audit architetturale (D-13): `audit/AUDIT-ARCH-20261111/` con inventario e qualità, incoerenze e duplicazioni, competenze quantitative mancanti, dipendenze, proposta di architettura per Strategy Discovery Lab e Trading Guardian, fonti e validazione, piano a tre mesi, relazione e strumento di misura.
- Aggiornati solo `CONTINUITA.md`, `collaborazione/LOCK.md`, `governance/DECISIONI.md` (D-13) e questo registro. Nessuna lezione, nessun materiale di Antigravity, nessuna struttura modificati.

## 2026-11-11 · v1.4 (revisione conclusiva V3)

- Ricevuto il pacchetto V3 di Antigravity (archivio ZIP in conversazione, SHA-256 `6c64a3a4…`; manifest V3 6/6 OK). Non archiviato nel Brain: decisione dell'utente pendente (audit, decisione 3).
- Aggiunta `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-02-V3/`: `CLAUDE_FINAL_REVIEW_V3.md`, `PROPOSTE-CORREZIONE-V3.md`, 4 strumenti `v3_*.py`, uscite, impronte.
- Esito: validazione V3 **non conclusa**. Riconosciuta come più appropriata la convenzione dello z usata da Gemini (test score) in C-14.
- Rimossa una cartella `__pycache__` generata localmente (non tracciata). Aggiornati `CONTINUITA.md`, `collaborazione/LOCK.md` e questo registro. Nessun file di Antigravity e nessuna lezione modificati.

## 2026-11-12 · v1.5 (revisione V3.1)

- Ricevuto il pacchetto V3.1 (ZIP `99e8f0bd…`, coincide con il dichiarato; manifest 14/14 OK) e `CONTINUITA_V3_1_PASSAGGIO_A_CLAUDE.md`. Non archiviati nel Brain (decisione pendente).
- Aggiunta `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-03-V31/`: revisione, proposte Q-01…Q-09 (non applicate), 4 strumenti `v31_*`, uscite, impronte. Novità metodologica: **effetto esatto del MAE** (prima solo simulato).
- Esito: motore corretto; pacchetto non validato (N-01, N-02).
- Rimossa una cartella `__pycache__` locale. Aggiornati `CONTINUITA.md`, `collaborazione/LOCK.md` e questo registro. Nessun file di Antigravity e nessuna lezione modificati.
- Aggiunta `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` (proposta, non implementata). Nessuna modifica al Brain principale, al Master Mission o al protocollo.

## 2026-11-12 · v1.6 (revisione V3.2)

- Ricevuti il pacchetto V3.2 (ZIP `989dd288…`, coincide con il dichiarato; dimensione reale 47.977 byte contro 41.696 dichiarati; manifest 15/15 OK) e `CONTINUITA_V3_2_PASSAGGIO_A_CLAUDE.md`. Non archiviati nel Brain (decisione pendente).
- Aggiunta `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-04-V32/`:
  - revisione, proposte S-01…S-09 (non applicate), registro delle verifiche, confronto delle affermazioni;
  - 4 strumenti `v32_*` e i test di accettazione proposti;
  - uscite e impronte.
- Esito: **VALIDATA CON RISERVE**. Mutazioni V02–V12: 11/11 uccise.
- Riconosciuto che la guardia simmetrica del MAE (S-05) deriva dalla proposta Q-08 di Claude ed è più restrittiva del necessario.
- Aggiornati `CONTINUITA.md`, `collaborazione/LOCK.md` e questo registro. Nessun file di Antigravity e nessuna lezione modificati.

## 2026-11-12 · v1.7 (revisione V3.3)

- Ricevuti il pacchetto V3.3 (ZIP `6fb9d76e…`, 62.513 byte, entrambi coincidenti; manifest 18/18 OK) e `CONTINUITA_V3_3_PASSAGGIO_A_CLAUDE.md`. Non archiviati nel Brain.
- Aggiunta `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-05-V33/`:
  - revisione con registro e confronto;
  - errata T-01…T-05 (non applicato);
  - strumenti `v33_*` (adattati dalla V3.2, più `v33_f_precisione.py`), uscite e impronte.
- Esito: **VALIDATA CON RISERVE**.
  - Riserve S-01…S-09 risolte (S-07 in parte).
  - Mutazioni dichiarate non riproducibili; con le definizioni di Claude 21/24.
  - Precisione fittizia dei valori esatti; attribuzione anticipata nel README.
- Aggiornati `CONTINUITA.md`, `collaborazione/LOCK.md` e questo registro. Nessun file di Antigravity e nessuna lezione modificati.

## 2026-11-12 · v1.8 (audit dell'architettura V2 di Gemini)

- Ricevuto il pacchetto `TRADING_BRAIN_ARCHITECTURE_REVISION_V2_PACKAGE.zip` (SHA-256 `f4794a55…`, diverso dal dichiarato `64470738…`; i tre documenti coincidono con gli hash dichiarati; manifest 4/4 OK). Non archiviato nel Brain.
- Aggiunta `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/`:
  - audit indipendente;
  - revisione delle affermazioni (CLM-01…16, A-01…18) e delle fonti (6 verificate al web, stato V-sec);
  - registro delle divergenze D-01…D-28;
  - calcolo di potenza (`verifiche/potenza_campione.py`);
  - pacchetto per una revisione esterna (`PACCHETTO_AUDIT_ARCHITETTURA_V2_PER_CHAT.md` e `.zip`).
- Riconosciuti due errori di Claude (D-03 ρ = 1; D-04 limiti «deterministici» senza H_esec).
- Commit autorizzato dall'utente il 12/11/2026. Aggiornati `CONTINUITA.md`, `collaborazione/LOCK.md` e questo registro. Nessun file di Gemini, nessuna lezione e nessun codice modificati.

## 2026-11-12 · v1.9 (controverifica di Gemini, registro delle decisioni, revisione esterna)

- Ricevuto il pacchetto di controverifica di Gemini (ZIP `c0bb94a5…`, manifest 4/4 OK). Non archiviato nel Brain (DA-01).
- `R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/`: valutazione critica (G-01…G-17), con 10 correzioni dopo una verifica fattuale (§9).
- `governance/DECISIONI.md`: aggiunte D-14…D-18, decisioni dell'utente del 12/11 (ecosistema e autonomia bounded; simmetria e indipendenza dai fornitori; Guardian G0 consultivo; V3.3 congelata; TradingView e motore indipendente).
- Nuovo `governance/DECISIONI-APERTE.md`: registro unico delle decisioni aperte DA-01…DA-18, raccolte da cinque documenti.
- `R-CLAUDE-20261112-08-REVISIONE-ESTERNA/`: istruzioni per un revisore esterno, indice e manifest. Lo ZIP con le copie dei documenti di Gemini è stato consegnato in chat e non è archiviato nel repository.
- Aggiornato `CONTINUITA.md`. Nessun file di Gemini, nessuna lezione e nessun codice modificati.

## 2026-11-12 · v1.10 (decisioni dell'utente e revisione esterna)

- `DECISIONI.md`: D-19…D-23 (repository nuovo e privato creato dall'utente; revoca mirata della sospensione; dati a costo zero; errata prima del G0; sistema creato da Claude).
- `DECISIONI-APERTE.md`: DA-01, DA-03, DA-11 e DA-15 segnate come decise; aggiunte DA-19…DA-23, dalla revisione esterna.
- Archiviata la revisione esterna di ChatGPT (`R-CLAUDE-20261112-08-REVISIONE-ESTERNA/REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md`, senza modifiche) e la risposta di Claude.
- Errori di Claude riconosciuti: etichetta «co-monotonicità» per lo scenario di stress; conteggio delle prove «mentali»; caso Wilson n = 0 e aritmetica di STR-002 non rilevati nelle revisioni V3.x.

## 2026-11-12 · v1.11 (errata V3.3, Q-09, G0 minimo, journal)

- `collaborazione/da-claude/ERRATA-V3_3/`: errata T-01…T-05 come addendum. Test V16, V22, V24 e R-16 (fallimento atteso); script di mutazione: 24/24 mutanti non equivalenti uccisi. V3.3 intatta.
- Ambiente: aggiunto l'host `ftmo.com` (approvato dall'utente) per leggere le regole ufficiali.
- `guardian/regole/`: regole FTMO (2-Step, 1-Step, Instant) verificate sulla fonte ufficiale (estratto e hash, 12/11/2026); regole personali come proposta, con provenienza.
- `governance/MODELLO-EPISTEMICO.md`: schema dei valori e mappatura verso `STANDARD.md` (proposta DA-06, usata dal G0).
- `guardian/g0/`: G0 minimo consultivo (schema dei valori, perdita allo stop per FX/futures/CFD, limiti FTMO, scenario di stress, scheda); `guardian/journal/`: journal di sola aggiunta con catena di hash, Brier score, impegni sigillati, indicatore R1 spento finché i parametri non sono definiti. 24 test superati.
- `DECISIONI-APERTE.md`: aggiunte DA-24 (conservazione dei dati del journal) e DA-25 (dati del conto per la riconciliazione).

## 2026-11-12 · v1.12 (repository canonico, correzioni G0 e journal)

- **Migrazione (D-19)** a `gioelemelis2-dot/trading-brain-core` (privato). Storia della sola `brain/` dal ramo `claude/vibrant-cannon-5uunho` di `l-Altro` (commit `f6a2824`), filtrata con `git filter-branch`: 23 commit, albero `brain/` identico (`7422e1fc…`). Su `main` anche il commit di configurazione (`README.md` e `.gitignore` alla radice).
- **Ramo `feat/fix-g0-journal`**, in TDD:
  - mandato «Binario A»: stress contro il limite totale; futures senza dimensione fittizia; regole personali confermate applicate; ancora di integrità del journal; Decimal e orari ISO-8601 negli indicatori;
  - contro-audit: P-05 confrontato con il limite giornaliero della prop firm e avvisi non soppressi; seconda parte di P-01 (size dopo una perdita); validazione di numeri e orari all'ingresso del journal e riferimenti `corregge`/`chiude` esistenti; correzioni applicate in `brier()` e negli indicatori (`versioni_finali`); `verifica --impronta`; positività in G0;
  - 36/36 test verdi.
- Aggiornati `CONTINUITA.md`, `DECISIONI-APERTE.md` (DA-01 eseguita) e questo registro (autorizzazione del contro-audit, punto 7).
- Nessuna modifica a V3.3, lezioni o materiali di Gemini.

## 2026-11-12 · v1.13 (mandato notturno: blindatura di G0 e journal, mutation testing, audit su Gemini)

- **Ramo `feat/fix-g0-journal`**, in TDD:
  - 5 correzioni: commissioni finite e non negative; avvisi P-05 su trade e stress anche a limite personale superato; `controlla_riferimenti` nel journal (stessa natura per `corregge`, `chiude` solo sulla radice di una previsione, nessuna doppia chiusura), applicato anche da `verifica`; soglie e dati di sessione validati; booleani rifiutati come numeri;
  - `guardian/test/mutazioni_g0_journal.py`: 44 mutanti non equivalenti sui 6 file operativi, più 1 equivalente dichiarato. Erano 30/44 uccisi con 41 test; con 11 test aggiunti sono 44/44;
  - 52/52 test verdi.
- **Merge su `main`** (commit `138daf3`), autorizzato dall'utente dopo l'audit (52/52 test, 44/44 mutanti).
- **Audit su Gemini** (`CONSEGNA_FIX_G0/AUDIT_OSTILE_SU_GEMINI.md`): nessun ramo del Binario B su GitHub; 138/138 hash dichiarati coincidono; l'hash falso del V3.3 non compare nei materiali disponibili ed è quasi certamente ricostruito dall'abbreviazione `6fb9d76e…7638`.
- Nessuna modifica a V3.3, lezioni o materiali di Gemini.

## 2026-11-12 · v1.14 (compatibilità Python 3.9, probabilità Decimal, lock concorrente)

- Dall'audit incrociato con Gemini (macOS, Python 3.9.6 di sistema), in TDD sul ramo `feat/fix-g0-journal`:
  - 9 test rossi (commit `6e9aca8`), poi le correzioni;
  - TOML portabile (`g0/_toml.py`: `tomllib`, poi `tomli`, poi un parser minimale identico a `tomllib` sui file del Guardian, con errore esplicito su ogni altro costrutto);
  - orari in un formato unico su ogni versione (`Z` convertita in `+00:00` e frazione portata a 6 cifre prima di `fromisoformat`; senza formato unico un journal scritto con 3.13 sarebbe invalido su 3.9);
  - `probabilita` anche come `Decimal` finito, registrato come testo;
  - lock esclusivo in `aggiungi()` (`fcntl.flock`, altrimenti un file di lock esclusivo, con attesa massima); la fase rossa ha mostrato una collisione reale fra scrittori concorrenti sul file temporaneo dell'ancora.
- Esito: 61/61 test su Python 3.9.25, 3.11, 3.12 e 3.13, con `-W error`. Mutation testing con 14 mutanti nuovi: 58/58 non equivalenti uccisi su 3.13.
  - Su 3.9 il primo giro dava 55/58: V54 e V58 sopravvivevano perché il parser TOML minimale era controllato solo contro `tomllib`, assente proprio su 3.9; ora un risultato atteso scritto nel test lo controlla anche lì.
  - V48 è equivalente prima di 3.11. Risultato finale su 3.9: 57/57.
- Nessuna modifica a V3.3, lezioni o materiali di Gemini.

## 2026-11-12 · v1.15 (bonifica dei rilievi del Red Team esterno su `brain/guardian/`)

- Ramo `fix/red-team-guardian` da `main`, solo `brain/guardian/`, in TDD.
  - 13 test rossi (commit `e78cc00`), poi le correzioni (`54ac980`).
  - Unito a `main` il 12/11/2026 (`fd14834`).
- Rilievi:
  - ALTO-1: NON STIMABILE propagato da margine e stop_residui; avviso «controllo non verificabile» nella scheda invece di un `TypeError`;
  - ALTO-5: trade sovrapposti esclusi da R1;
  - ALTO-6/BASSO-1: stringhe dello strumento non vuote; tolleranza di 1e-9 tick sul rumore float;
  - MEDIO-3/4: `versioni_finali` rifiuta riferimenti fantasma; esito senza `chiude` rifiutato;
  - MEDIO-5/6/7: O_CLOEXEC esplicito; recupero dei soli lock orfani sicuri; `verifica` sotto lock;
  - MEDIO-10/11: `fmt` con esponenti estremi; P-01 con capitale nullo; chiavi TOML tra virgolette.
- Scostamenti motivati:
  - il costrutto `Valore(..., "divisione intera", ...)` suggerito non è valido nello schema: usato `combina`;
  - O_CLOEXEC era già garantito dalla PEP 446;
  - `TEMPLATE_RICONCILIAZIONE_DA25.toml` non esiste.
- Esito: 74/74 test su Python 3.9-3.13; mutanti non equivalenti uccisi 77/77 su 3.13 e 76/76 su 3.9.
- Questa voce è registrata qui e non prima: il mandato era limitato a `brain/guardian/`.

## 2026-11-12 · v1.16 (chiusura dell'audit Red Team sul Guardian e stato consolidato di `main`)

- Audit di verifica sui 13 file aggiornati:
  - nei 7 file del Guardian, 0 CRITICO e 0 ALTO;
  - 1 MEDIO corretto in TDD su `main`: `versioni_finali` ora rifiuta un esito con `chiude` verso una correzione invece dell'id radice, come `controlla_riferimenti` (`3372072` rosso, `18bd042` verde; nuovo mutante V78).
- **Binario B non verificato:** al 12/11/2026 22:46 UTC `origin/main` coincide con `main` locale e non contiene `brain/laboratorio/` né test in `brain/dati/`.
  - ALTO-2 residuo (`portfolio.on_fill`) e ALTO-7 (`engine`, ordine eseguito dopo un gap con lo stop del segnale) restano non verificati.
  - Lo stesso vale per le suite `brain/dati/tests` e `brain/laboratorio/tests`.
- Stato di `main`: 75/75 test del Guardian su Python 3.9, 3.11, 3.12 e 3.13; mutanti non equivalenti uccisi 78/78 su 3.13 e 77/77 su 3.9.
- Nessuna modifica a V3.3, lezioni, materiali di Gemini, `brain/dati/` o `brain/laboratorio/`.
