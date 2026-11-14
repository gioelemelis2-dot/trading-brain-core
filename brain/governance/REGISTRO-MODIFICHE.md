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

## 2026-11-12 · v1.17 (ALTO-8: race nel recupero del lock orfano del journal)

- Da una revisione esterna. Nel ripiego senza `fcntl`, fra il ricontrollo del lock orfano e la sua rimozione, un altro processo poteva rimuovere l'orfano e creare il proprio lock; la rimozione cancellava allora un lock vivo.
- Ramo `fix/lock-orfano-toctou`, in TDD:
  - test rosso (`062cdef`): riproduzione deterministica con due thread; esito osservato: due scrittori nella sezione critica, id duplicato, catena interrotta, ancora disallineata;
  - correzione (`7a53063`): l'orfano si rimuove solo tenendo `<lock>.recupero`, creato con `O_EXCL`;
  - unito a `main` su autorizzazione dell'utente.
- La stessa revisione segnalava come aperto il MEDIO su `versioni_finali`: era già corretto su `main` (`18bd042`); la revisione leggeva una versione precedente.
- ALTO-2 e ALTO-7 del Binario B restano non verificati: su GitHub non c'è codice del Binario B.
- Esito: 76/76 test su Python 3.9, 3.11, 3.12 e 3.13; mutanti non equivalenti uccisi 79/79 su 3.13 e 78/78 su 3.9 (nuovo V79).

## 2026-11-12 · v1.18 (verifica del Binario B; Gate 0 e 1 chiusi, Gate 2 aperto, Gate 3 inizializzato)

- `main` allineato a `origin/main` (`30ea8e6`, fast-forward). Il Binario B è ora su GitHub; `brain/guardian/` è invariato rispetto a `591302a`.
- **Verifica del Binario B**, con controesempi indipendenti di Claude e senza modificare i file di Gemini:
  - ALTO-2 (`portfolio.on_fill`): risolto; con il cambio mancante l'errore arriva prima di ogni modifica dello stato;
  - ALTO-7 (`engine`, SL/TP dopo un gap): risolto; l'ordine incoerente con l'apertura reale viene respinto.
- **Suite unificata:** 108/108 test (76 Guardian più 32 Binario B) con `python3 -s -B -W error`, su Python 3.13 e 3.9; nessun file scritto nel repository dall'esecuzione.
- **Gate 1:**
  - `dati/reali/demo_mt5_50k_xauusd.toml` → `demo_broker_mt5_50k_xauusd.toml`: conto demo broker ECN MT5 da 50.000 USD; regole interne 5%/10% simulate con lo schema `ftmo_2step`; commissione ECN round-turn 7,00 USD/lotto su XAU/USD. Tolto il nome dell'operatore, dato personale non necessario alla scheda;
  - `guardian/regole/regole_personali.toml` (il percorso indicato, `g0/regole_personali.toml`, non esiste): **P-01 = 0,005** e **P-05 = 0,015** confermate dall'utente;
  - la scheda mostra «2 confermate su 15» e il margine P-05 di 750 USD. Con un trade [ESEMPIO] non salvato (0,10 lotti, stop a 25 USD, 0,70 di commissione) la perdita allo stop è 250,70 USD e l'avviso P-01 scatta (0,501% contro 0,500%), anche su Python 3.9 con il parser TOML minimale.
- **Test resi indipendenti dalle scelte dell'utente:** `TestFix3` e i tre helper `regole_con` ora partono da regole tutte non confermate. Prima `TestFix3` presupponeva «0 confermate» nel file reale e falliva dopo le conferme. Mutation testing riconfermato: 79/79 su 3.13.
- **Gate 3 inizializzato:**
  - `dati/operativo/journal_broker_mt5_50k/`, con `.gitignore` che esclude i dati personali del journal (DA-16) e un LEGGIMI d'uso;
  - `dati/operativo/trial_registry_xauusd.json`, `TRIAL_REGISTRY_V1` con 0 prove, letto correttamente da `DSRCalculator`.
- **Gate 2 aperto:** in attesa del CSV storico XAUUSD 15m.
- I gate sono la denominazione operativa dell'utente: nel Brain non ne esiste ancora una definizione formale.
- Nessuna modifica a V3.3, lezioni o ai file di codice e test di Gemini.

## 2026-11-12 · v1.19 (Gate 2 preparato, non chiuso; frazioni con 3 decimali nella scheda)

- **Esecuzione sul Mac non possibile da questa sessione:** nessuna cartella condivisa con il Remote Control. Il lavoro è stato fatto nel container cloud e pubblicato su GitHub.
- **Scaricamento Dukascopy dal cloud non riuscito:**
  - l'host `datafeed.dukascopy.com` è stato aggiunto all'ambiente cloud personale;
  - il server ha poi risposto con 429 e connessioni chiuse;
  - i tentativi ripetuti sono stati fermati dal controllo dei permessi della sessione.
  - Nessun dato inventato o simulato in sostituzione.
- **`brain/dati/pipeline/dukascopy.py`**, da eseguire sul Mac:
  - candele BID da 1 minuto aggregate a 15 minuti UTC, con pause, nuovi tentativi su 429/5xx, cache locale e User-Agent generico;
  - controlli che fermano su scala o ordine dei campi sbagliati (formato non documentato), OHLC incoerenti e ordine non crescente;
  - buchi classificati: pausa giornaliera; fine settimana (solo se contiene un sabato intero, regola corretta durante i test); chiusure lunghe da verificare; anomali, che fermano salvo `--accetta-buchi`;
  - CSV e `meta.json` con SHA-256, ingestione, partizione 70/30 e `commitment.json` con nonce fuori dal repository.
  - 9 test offline, con file `.bi5` costruiti e un finto server che risponde 429.
- `.gitignore`: esclusi CSV, cache, partizioni `.jsonl` e `*.secret`; versionati i soli metadati e il sigillo.
- **Scheda del G0:** le frazioni si mostrano con 3 decimali; P-01 si legge «0,005» invece di «0,01». In TDD (`8d1ae16` rosso, `5961613` verde), con il nuovo mutante V80.
- **Esito:** 118/118 test (77 Guardian, 32 Binario B, 9 Dukascopy) su Python 3.13 e 3.9; mutanti non equivalenti uccisi 80/80 su 3.13 e 79/79 su 3.9.
- Il Gate 2 si chiude quando `XAUUSD_15m.meta.json` e `commitment.json` sono su GitHub.

## 2026-11-13 · v1.20 (regole personali confermate; progetto generale)

- **Regole personali:** l'utente ha confermato la proposta di Claude («confermo la prop»).
  - P-02…P-04 e P-06…P-14 sono attive. Valori: P-06 = 1 posizione aperta, P-08 = 15 minuti attorno alle news ad alto impatto, P-11 = 15 minuti, P-12 = 60 secondi, P-14 = 7 ore.
  - P-15 resta proposta (coincide con P-05 allo 0,5% a trade).
  - La scheda mostra «14 confermate su 15». Commit `92339cb`.
- **Perdita massima:** l'utente ha chiarito che l'1,5% è giornaliero, cioè coincide con P-05.
- **Verifiche:** 118/118 test su Python 3.13 e 3.9; mutanti non equivalenti uccisi 80/80 su 3.13 e 79/79 su 3.9, con le regole attive.
- **Progetto generale** in un documento condiviso, «Trading Brain — Progetto generale». Contiene:
  - obiettivi dell'utente e valutazione di Claude;
  - architettura e Gate 0–7 (i Gate 3–7 sono proposte);
  - calcolo dei trade necessari per validare una strategia;
  - proposta sulle regole personali, rischi, decisioni aperte;
  - prompt per i revisori esterni.
- Esportato in PDF per DeepSeek. Primo giro di domande all'utente in corso.

## 2026-11-13 · v1.21 (contro l'autoinganno; DA-26)

- **Autovalutazione di Claude**, chiesta dall'utente («stiamo procedendo come scienziati rigorosi?»). Problema principale: l'Out-of-Sample sui 3 anni (gli ultimi ~11 mesi) è già stato visto dall'utente e, a grandi linee, da Claude. Il sigillo impedisce di modificarlo, non di guardarlo.
- **Contromisure approvate dall'utente:**
  - il futuro (incubazione) come test finale;
  - più anni e un periodo vecchio di verifica (nuova **DA-26**, bloccante per il Gate 2);
  - seconda fonte di dati e costi veri prima di ogni risultato;
  - replica indipendente Claude/Gemini e regole decise prima;
  - «come lo sai?»;
  - niente nuova infrastruttura fino alla prima ipotesi testata.
- **Sigillo:** quello sui 3 anni con 70/30 è provvisorio.
- **Scaricamento Dukascopy:** timeout di lettura, connessioni chiuse e risposte troncate sono nuovi tentativi (TDD: `994373f` rosso, `42cf512` verde). Su Python 3.9 `socket.timeout` non è un `TimeoutError` e faceva fermare lo script sul Mac.
- **Utente:** circa 2 anni di trading, strategie passate non profittevoli. Le idee di partenza (Fibonacci e order block, anche insieme) diventano ipotesi da sigillare al Gate 3; i dettagli si scrivono prima di guardare i dati.
- **Percorso:** FTMO solo dopo una lunga incubazione su più conti demo gratuiti di broker diversi; nessuna data.

## 2026-11-13 · v1.22 (piano di diversificazione; DA-27, DA-28)

- **Richiesta dell'utente:** diversificazione centrale, più mercati, più backtesting, raccogliendo prima i dati come per l'oro.
- **Nuovo `governance/PIANO-DIVERSIFICAZIONE.md` (proposta):**
  - cosa cambia rispetto all'oro, verificato nel codice: scaricatore solo XAUUSD, backtester su un solo strumento, registro delle prove per strumento;
  - 6 regole: calendario comune, un mercato alla volta, mercati dichiarati prima, conteggio unico, correlazioni misurate, P-06 invariata;
  - mercati candidati e ordine, tempi stimati, dati oltre ai prezzi, fasi D0–D6.
- **Nuove decisioni aperte:** DA-27 (mercati e calendario comune) e DA-28 (registro unico e mercati dichiarati prima).
- **Documento del progetto:** nuova sezione «Diversificazione su più mercati».

## 2026-11-13 · v1.23 (rilievi di Gemini G-20261113-01: DSR, partizione per date, bande di prezzo)

- **Revisione critica di Gemini** (G-20261113-01). Claude ha letto solo il riassunto: il ramo non era su GitHub. Rilievi verificati sul codice e accolti; esiti in `collaborazione/da-claude/ESITI.md`.
- **Correzioni sul ramo `fix/dsr-e-partizione-date`,** autorizzate dall'utente, in TDD (`c74ca2b` rosso, `19b70de` verde):
  - DSR con la scala sqrt(V) di Bailey e López de Prado: prima, con N ≥ 2 prove, bocciava qualunque strategia;
  - partizione per date con embargo (`partizione_date.py`);
  - niente più 70/30; bande di prezzo per periodo;
  - controllo dei salti di scala.
- **Mutation testing:** nuovo `dati/tests/mutazioni_dsr_partizione.py`, 26/26 su Python 3.13 e 3.9. Al primo giro il mutante P11 (la verifica ignorava il sigillo) era sopravvissuto: aggiunto un test.
- **Divisione del lavoro in `LOCK.md`:** Claude corregge; Gemini prepara vettori di prova indipendenti per il DSR e rivede il ramo.
- **Merge su main solo con l'autorizzazione dell'utente,** dopo la revisione di Gemini.

## 2026-11-13 · v1.24 (revisione dura di Gemini sul ramo: 6 difetti corretti)

- **Revisione di Gemini** G-20261113-03 sul commit `2d16a46`. Claude ha riprodotto tutti i rilievi prima di correggerli; esiti in `collaborazione/da-claude/ESITI.md`.
  - G3-01: DSR con NaN = 1,0.
  - G3-02: verifica aggirabile declassando tutti i blocchi di verifica.
  - G3-03: buchi lunghi di giorno e picchi dentro la candela non fermavano.
  - G3-04: CSV scritto prima del controllo del nonce.
  - G3-06: record binari non validi.
  - G3-05 resta aperto (con DA-19 e DA-28).
- **Correzioni** in TDD: `d0c8c4d` rosso, poi verde.
- **Mutation testing:** 40 mutanti (14 nuovi), 40/40 su Python 3.13 e 3.9. Al primo giro il mutante P14 (ruoli presi dal commitment) era sopravvissuto: aggiunto un controllo sul sigillo dei blocchi declassati.
- **Collaborazione:** Gemini ha lavorato in un worktree separato senza toccare i file di Claude. I suoi rami sono stati pubblicati dall'utente.

## 2026-11-15 · v1.25 (mandato notturno: programma dei criteri di H-002, sigillo, quaderno delle ipotesi)

- **Ramo `feat/esecutore-h002`, NON unito a main** (merge solo con l'autorizzazione dell'utente, dopo le revisioni).
- **TDD:**
  - `ecbae88` rosso, `7cf50ae` verde: sigillo e registro delle prove, criteri generici, caricatore BID/ASK;
  - `c8ef3aa` rosso, `78f41e4` verde: esecutore di H-002 e prove su mercati inventati.
- **Mutation testing** (`laboratorio/tests/mutazioni_esecuzione.py`, 56 mutanti): primo giro 55/56 su Python 3.13 e 3.9. Il sopravvissuto E12 è ucciso da un test aggiunto (`fdf4afe`). Secondo giro intero: 56/56 su entrambe.
- **Nessun dato reale usato, nessuna richiesta a Dukascopy, nessun sigillo.** Scheda H-002 v3.1 invariata; ambiguità A1–A11 in `laboratorio/ipotesi/H-002-REVISIONI.md`.
- **Quaderno delle ipotesi** `laboratorio/ipotesi/QUADERNO-IPOTESI.md`: 10 idee dalla letteratura, senza dati; fonti incerte segnate.
## 2026-11-15 · v1.26 (replica indipendente di Gemini: 2 errori del simulatore di H-002 corretti)

- **Replica alla cieca di Gemini** (G-20261115-01, ramo `rev/gemini-replica-h002`): coincidenza su 25 configurazioni su 30. Due errori reali, riprodotti da Claude prima di correggerli:
  - D1: spread di riferimento dalla fine del range invece che dalle 08:30 (tocca solo la robustezza);
  - D2: once in virgola mobile, 49 invece di 50 ai bordi interi.
- **Correzione in TDD** sul ramo `fix/orb-replica-gemini`: `b26be54` rosso, poi verde. 46 test e 35/35 mutanti su Python 3.13 e 3.9.
- **Ambiguità nuove** A12–A14 (solo diagnostiche, o casi limite) in `laboratorio/ipotesi/H-002-REVISIONI.md`, R8. Scheda non toccata.
- **Merge su main solo con l'autorizzazione dell'utente.**

## 2026-11-15 · v1.27 (controlli strutturali, registro dei difetti, proposta v3.2)

- **Ramo `fix/orb-replica-gemini`:**
  - test contro lo sguardo al futuro (taglio dei dati) e di simmetria;
  - 8 casi scoperti segnalati da Gemini;
  - mutanti 40/40 su Python 3.13 e 3.9 (`cd7fdb9`).
- **`laboratorio/REGISTRO-DIFETTI.md`:** 22 difetti trovati dal 13/11, con gravità, scopritore e metodo. Dal 15/11 nessun difetto critico.
- **`laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md`:** solo proposta.
  - Ambiguità A1–A14 da decidere.
  - 16 casi d'oro, ognuno legato a un test che passa.
  - Regola d'uscita per il sigillo: replica 100%, mutanti 100%, due revisioni di fila pulite, impronte anche del codice.
