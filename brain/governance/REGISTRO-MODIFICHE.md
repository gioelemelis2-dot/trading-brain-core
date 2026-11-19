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

## 2026-11-15 · v1.28 (revisione R7 di Gemini sul programma dei criteri: 8 difetti corretti)

- **Gemini:**
  - conferma 30/30 sul simulatore corretto;
  - replica alla cieca del programma dei criteri: differenza 0 sui calcoli;
  - P1–P8 nei collegamenti fra sigillo, registro, sviluppo, verifica e riga di comando: 5 critici e 3 importanti.
- **Correzioni in TDD** (`6a29aa2` rosso, poi verde). Mutanti: programma dei criteri 70/70 (14 nuovi, di cui 5 di Gemini), simulatore 40/40, su Python 3.13 e 3.9.
- **Applicate in via prudenziale,** da ratificare dall'utente: A2, A3, A8 (fine provvisoria 31/10/2023) e A11 (finestra ancorata alla fine). Nuove proposte A19–A21.
- **Registro dei difetti:** #23–#32. È corretta la lettura del 15/11: la convergenza vale per il simulatore, non ancora per il programma dei criteri.
- **Prompt R11** per Gemini e ChatGPT; il prompt R9-bis non inviato è stato sostituito.

## 2026-11-15 · v1.29 (ChatGPT come Direttore generale della sicurezza)

- **Richiesta dell'utente:** ChatGPT non è più solo revisore, ma Direttore generale della sicurezza (DGS). Ruolo critico e costruttivo, mai compiacente, con tutta la documentazione.
- **Materiali in `collaborazione/da-claude/direttore-sicurezza/`:**
  - guida per l'utente;
  - istruzioni permanenti del Progetto ChatGPT (5.053 caratteri);
  - messaggio 1 (insediamento e ispezione generale);
  - messaggio 2 (revisione tecnica R11);
  - controllo della prima relazione da parte di DeepSeek;
  - indice dei documenti.
- **Cartella `collaborazione/da-chatgpt/`** per le consegne del DGS, archiviate senza modifiche.
- **`piano/PROGETTO-GENERALE-20261115.md`:** esportazione del documento condiviso «Progetto generale». Gli schemi dei gate e dell'architettura sono trascritti; le parti superate sono annotate.

## 2026-11-15 · v1.30 (secondo attacco di Gemini R11: nessuna scelta libera, codice sigillato)

- **Gemini R11:** 3 difetti critici, 4 importanti e 1 minore, di nuovo nei collegamenti.
- **Correzione di classe** (`d4a5dc9` rosso, `f248f8a` verde):
  - periodi, ripetizioni e seme fissi nel codice;
  - impronte del codice nel sigillo;
  - controllo dei giorni feriali vuoti;
  - impronta dei dati e stessa cache fra sviluppo e verifica;
  - esito della verifica nel registro;
  - copertura minima 90% dei confronti (A23, in via prudenziale).
- **Stato:** 229 test verdi più 77 del Guardian; mutanti 40/40 e 89/89 su Python 3.13 e 3.9.
- **Registro dei difetti** #33–#40; proposta v3.2 con A22–A25 e le posizioni di Gemini su A12–A21.

## 2026-11-15 · v1.31 (incidente del sigillo: blocco tecnico e controllo della cache)

- **Incidente del 14/11** (difetto #41): H-002 eseguita sui dati veri dello sviluppo prima del sigillo. Registrato in `H-002-REVISIONI.md`. Revisione esterna del nucleo statistico archiviata in `collaborazione/da-revisori-esterni/` (contiene risultati sullo sviluppo).
- **Blocco tecnico** (`0d4a4b9` rosso, `7d2fc71` verde): il caricatore controlla il sigillo anche nello sviluppo.
- **Controllo d'integrità della cache** (`dati/pipeline/controlla_cache.py`, `ddc5f88` rosso, poi verde). Conta, anno per anno:
  - giorni senza file, feriali vuoti, file illeggibili o troncati, giorni corti;
  - temporanei rimasti dopo uno spegnimento.

  Mai prezzi. Test 8/8; mutanti 11/11 su Python 3.13 e 3.9 (al primo giro 9/11: aggiunto un test con un problema alla volta).

## 2026-11-15 · v1.32 (registro degli impegni anticipati)

- **Nuovo `governance/IMPEGNI-ANTICIPATI.md`:** impegni scritti prima di vedere un risultato, da confrontare dopo con la scelta effettiva. Non sono regole operative, non sono sigilli, non entrano in N.
- **IA-01 (utente, 14/11):** vantaggio minimo che sceglierebbe oggi, 0,15 R per trade, fissato prima del «banco di taratura del motore». La soglia operativa resta quella della scheda H-002 v3.1.

## 2026-11-15 · v1.33 (stato dei dati sul Mac e scaricatore solo-cache)

- **Controllo della cache sul Mac** (eseguito dall'utente):
  - BID storico fino al 07/06/2009, poi niente fino al 12/11/2023;
  - ASK storico quasi assente (fermo il 01/01/2005 per un errore HTTP);
  - nessun file illeggibile, nessun temporaneo; 10 giorni corti, tutti festività;
  - scaricamento fermo dallo spegnimento del Mac.
- **Riserva di verifica oggi:** 1.155 giorni feriali su 4.912 (23,5%), finché lo storico non è completo.
- **Nuovo `dati/pipeline/scarica_cache.py`** (`b59eb0f` rosso, poi verde):
  - scarica solo nella cache da una data a un'altra, senza attese sui giorni già presenti, senza CSV e senza prezzi;
  - registro CSV per giorno, scritto subito su disco;
  - tre esiti distinti: 404, risposta vuota, guasto (richiesta 1 di DGS-04);
  - controlla ogni file prima di salvarlo e lo forza su disco; si ferma su un errore HTTP sconosciuto.
- **`dukascopy.richiesta_http`:** stessa politica di nuovi tentativi; `scarica_http` invariato.
- **Prove:** test 30/30 su Python 3.13 e 3.9; mutanti 12/12. Al primo giro un mio test usava l'attesa vera e bloccava il mutante W12: corretto.

## 2026-11-15 · v1.34 (scaricatore: errori HTTP isolati non bloccano più tutto)

- **Perché:** l'ASK storico si è fermato il 01/01/2005 con un errore HTTP. Non è il difetto «404 confuso con la risposta vuota» della richiesta 1 di DGS-04: il 404 era già gestito. È un altro codice 4xx (lo dirà il registro), su cui lo scaricatore si fermava per progetto. Un solo giorno rifiutato avrebbe bloccato tutto (difetto #46).
- **`scarica_cache.py --continua-su-http`** (`f35ad7b` rosso, poi verde):
  - l'errore si registra come `http-<codice>`;
  - il giorno resta **senza file**, quindi «mancante» per `controlla_cache`, mai «nessun dato»;
  - si va avanti; fermo dopo 20 errori HTTP di fila (blocco vero);
  - alla fine codice d'uscita 5 se ci sono stati giorni in errore.
  - Senza l'opzione il comportamento è quello di prima.
- **Difetto #45 (mio):** il test della riga di comando faceva una richiesta vera a Dukascopy, perché la funzione di richiesta era fissata alla definizione. Corretto, e il test verifica che la risposta finta sia stata usata.
- **Prove:** test 33/33 per lo scaricamento (11 di `scarica_cache`, 22 di `dukascopy`); 250 test su `dati` e `laboratorio` e 77 su Guardian, verdi su Python 3.13 e 3.9 con la rete bloccata; mutanti 20/20 su entrambe le versioni (8 nuovi, W13–W20).

## 2026-11-15 · v1.35 (censimento di Gemini, patch di tb-proposte, riconteggio indipendente)

- **Censimento di Gemini archiviato** (`collaborazione/da-gemini/G-20261115-03-…`), con la lettura di Claude: riserva intatta secondo Gemini; «non decidibile» nato da una riclassificazione retroattiva (passo 2986); esplorazione **E-003** registrata e contata in N.
- **Patch di `tb-proposte` verificata** (impronta ricostruita da `1fec51c`, uguale a quella sul Mac) e archiviata, **non applicata**: allenta tre criteri dopo i numeri e permette di riprovare sugli stessi dati.
- **H-002:** decisione dell'utente «parcheggiata per ora»; condizione d'uscita proposta da Claude, in attesa della risposta.
- **Nuovo `governance/censimento/riconta.py`** (`29fc8ff` rosso, poi verde): riconteggio indipendente dalle trascrizioni JSONL di Antigravity e di Claude Code e dai log dei task.
  - Conta tutti gli strumenti, non solo `run_command`; riconosce le esecuzioni anche come `(cd x; python3 …)`, `/usr/bin/python3`, script di shell e input a processi aperti.
  - Il controllo principale: uscite con **date della riserva** (anche negli URL di Dukascopy, con i mesi da 0) e **numeri con la forma di un prezzo**.
  - Stampa solo conteggi, passi, ore, date ed estratti dei comandi con i prezzi mascherati; non conserva il testo delle uscite.
- **Prove:** test 7/7 su Python 3.13 e 3.9; mutanti 12 uccisi su 12 non equivalenti (Z12 equivalente: il testo delle uscite non è mai conservato, ora garantito da un test e dal mutante Z13). Provato sulle trascrizioni di questa sessione: 2 segnalazioni, entrambe falsi allarmi (date di un mercato inventato, festività inglesi), come previsto per un controllo che segnala e lascia il giudizio a una persona.

## 2026-11-15 · v1.36 (condizione d'uscita di H-002, primo riconteggio sul dump)

- **H-002:** approvata dall'utente la condizione d'uscita dal parcheggio: solo su dati successivi al 12/11/2026, sigillata prima, contata in N; mai rieseguita sullo sviluppo.
- **Censimento:** primo riconteggio indipendente sul dump di Gemini: confermate le 16 esecuzioni sui dati veri, tutte sullo sviluppo; 18 passi in più trovati con una rete più larga, tutti innocui. Il controllo completo sulle trascrizioni originali resta da fare sul Mac.
- **`CONTINUITA.md`:** in testa, lo stato del 15/11 sera e le azioni in corso.

## 2026-11-16 · v1.37 (riconteggio chiuso, IA-02)

- **Censimento delle esecuzioni chiuso:** riserva 2005 → 31/10/2023 intatta per trascrizioni (Gemini e Claude Code sul Mac), letture di file e CSV su disco; 19 segnalazioni di `riconta.py`, tutte falsi allarmi. Limite: ciò che l'utente ha guardato a mano.
- **IA-01:** l'utente non ricorda data e riferimento: resta una dichiarazione senza prova di anteriorità.
- **IA-02 (nuovo, vincolante per H-003 e successive):** R medio netto ≥ +0,15 R per trade, deciso prima di qualsiasi idea di H-003. Da decidere nella scheda di H-003, prima dei dati: soglia sulla stima o sul limite inferiore dell'intervallo.

## 2026-11-16 · v1.38 (lavoro notturno: mandato R12-bis, potenza di IA-02, registro della riserva)

- **Mandato R12-bis per Gemini** (`collaborazione/da-claude/PROMPT-R12-BIS-GEMINI.md`): regole dopo l'incidente (nessun dato vero, cache e scaricamento intoccabili, commit con identità propria, elenco completo dei comandi); bersagli: programma dei criteri, `scarica_cache.py`, `riconta.py`.
- **Calcolo di potenza per IA-02** (`laboratorio/studi/potenza_soglia.py`, documento `studi/risultati/potenza_IA-02.md`): regola sulla stima o sul limite inferiore; con circa 450 trade il limite inferiore ucciderebbe quasi ogni idea, con circa 2.500 diventa sensato. Proposta: stima nello sviluppo, limite inferiore nella riserva. Test 5/5 su 3.13 e 3.9, mutanti 8/8.
- **Registro della riserva di verifica** (`laboratorio/esecuzione/riserva.py`, richiesta 3 di DGS-04), **presentato per ratifica**: prenotazione, autorizzazione atomica prima della lettura dei dati (contatore j, N globale, quota α_j = α_tot/[j(j+1)]/m), rilascio, quarantena, parte protetta con sblocco esplicito, esito; lo stato si ricostruisce rigiocando gli eventi e un file manomesso è rifiutato. Test 15/15 su 3.13 e 3.9 (`68a2146` rosso), mutanti 24/24 dopo 4 test aggiunti (V02, V16, V19, V24 sopravvissuti al primo giro: buchi nei test, non nel codice). Le regole di spesa (α totale, scelta delle finestre, parte protetta) restano decisioni dell'utente.
- **Modello di scheda per H-003** (`laboratorio/ipotesi/MODELLO-SCHEDA-H-003.md`), da approvare: origine e contaminazione al §0, IA-02 nello screening e nella verifica (regola da scegliere), uscite solo in avanti (DGS-03), N con i tagli esplorativi, tre esiti solo con risoluzione su dati nuovi, casi d'oro e regola d'uscita per il sigillo obbligatori.

## 2026-11-16 · v1.39 (difetto #47: scrittura su disco affidabile anche su macOS)

- **Cosa è successo:** il Mac si è spento durante lo scaricamento; alla ripartenza 20 giorni già scaricati (novembre–dicembre 2009) non erano in cache e sono stati riscaricati. Nessun dato sbagliato è entrato, ma la garanzia «scritto e forzato su disco» non valeva su macOS.
- **Correzione** (`c49da94` rosso, poi verde): `_forza` usa `F_FULLFSYNC` dove c'è (macOS) e ripiega su `fsync`; dopo lo spostamento atomico si forza anche la cartella; il registro CSV usa la stessa funzione.
- **Prove:** test verdi su 3.13 e 3.9 (con la rete bloccata); mutanti 24/24 su entrambe le versioni (W21–W24 nuovi).
- **Effetto sullo scaricamento in corso:** nessuno; usa ancora la versione di prima (worktree `tb-scarica`). La correzione vale dal prossimo avvio. A fine scaricamento `controlla_cache` deve risultare pulito: un file vuoto o rovinato lasciato dallo spegnimento si vedrebbe lì.

## 2026-11-16 · v1.40 (R12-bis: giudizio e correzioni dello scaricatore)

- **R12-bis di Gemini integrato** (`3ad6d77`): tutte le sonde riprodotte da Claude con la rete bloccata; difetti #48–#58 nel registro; B-04 respinto con motivo (`H-002-REVISIONI.md`, sezione R12-bis). La regola d'uscita per il sigillo resta a zero giri puliti.
- **Scaricatore corretto** (`3b0c744` rosso, poi verde):
  - #52: `Retry-After` letto anche come data; illeggibile o passato: attesa crescente normale;
  - #58: `attesa` e `apri` di `richiesta_http` risolte alla chiamata (la causa della richiesta in rete accidentale di Gemini);
  - #54: codice vero della risposta (204 resta «vuoto-204»); codici diversi da 200, 204 e 404 trattati come errori; `--pausa` negativa: codice 2;
  - #53: alla ripresa ogni file in cache è decodificato; uno rovinato si mette da parte (`.<giorno>.rovinato`) e si riscarica; uno buono senza riga si registra («in-cache-non-registrato»);
  - #55: `--riprova-vuoti` richiede di nuovo i giorni feriali salvati vuoti.
- **Prove:** 43 test (scaricatore e Dukascopy) verdi su 3.13 e 3.9, con la rete bloccata; mutanti 37/37 su entrambe le versioni (W25–W37 nuovi; W01, W02, W09, W15, W24 riallineati al codice nuovo).
- Lo scaricamento in corso sul Mac usa ancora la versione di prima: la nuova vale dal prossimo avvio.
- **Riconteggio corretto** (`123d227` rosso, poi verde; #56, #57):
  - argomenti letti da qualunque campo della chiamata; ogni record che non è testo dell'utente o del pianificatore conta come uscita, e così un formato sconosciuto;
  - esecuzioni anche come `bash x.sh` (anche dentro il JSON), `source`, `./binario`, awk, perl, node e sottoagenti;
  - date anche come 03/01/2005 (due letture), 03.01.2005, 2005.01.03, 20150615, timestamp in secondi o millisecondi, percorsi Dukascopy senza BID/ASK; trovato e corretto anche un difetto di Claude nella regola dei percorsi (non distingueva le maiuscole: `backup/2015/05/15` letto con i mesi da 0);
  - prezzi con virgola, separatore delle migliaia, fino a 4 decimali, da 100 a 9.999;
  - dei campi con contenuti (file scritti, sostituzioni, prompt) si stampa solo il nome.
- **Prove:** 14 test verdi su 3.13 e 3.9; nuovo script permanente `governance/censimento/mutazioni_riconta.py`, 29/29 su entrambe le versioni (4 sopravvissuti al primo giro: buchi nei test, chiusi). Sulle trascrizioni di Claude le segnalazioni passano da 2 a 13: è il prezzo di una rete più larga.

## 2026-11-16 · v1.41 (R12-bis: programma dei criteri corretto, mutanti validi)

- **Programma dei criteri** (`dce72ee` rosso, `774573d` verde):
  - #48: le impronte coprono tutto il codice `brain` che l'esecutore può eseguire, ricavato dagli import (anche dentro le funzioni) e dagli `__init__.py`: 23 file invece dei 7 scritti a mano; il caricatore, chiamato senza impronte, ricontrolla dal disco i file registrati al sigillo;
  - #49: un giorno feriale è completo solo con almeno metà dei minuti della sessione di Londra (08:00–16:45); vigilie tollerate. **Soglia provvisoria**, da confermare con i conteggi dei minuti della cache vera (solo conteggi);
  - #50: un solo calendario (`dati/pipeline/calendario.py`) per il caricatore e `controlla_cache`, con 26/12, Lunedì dell'Angelo e i giorni spostati di 1/1 e 25/12;
  - #51: il registro delle prove deve continuare la versione su git (`ANCORA_GIT`): **va committato dopo ogni esecuzione**; varianti con nomi esatti (suffisso solo per la robustezza); `--ora` nel formato del registro; alla verifica si ricalcola l'impronta dei dati dello sviluppo.
- **Errori di Claude trovati facendo:** un test anti-frode del progetto ha fermato una scorciatoia sugli orari (`.replace(tzinfo=…)`) nel codice di `Retry-After`: corretto il codice. Mutanti non validi contati come uccisi (#59): corretti gli script.
- **Prove:** 306 test (dati, laboratorio, censimento) e 77 di Guardian verdi su 3.13 e 3.9; mutanti tutti uccisi su entrambe le versioni: esecuzione 111/111 (22 nuovi), scaricatore 37/37, riconteggio 29/29, controllo della cache 11/11, simulatore 40/40, DSR e partizione 44/44.
- **Regola d'uscita per il sigillo:** contatore dei giri puliti a zero (R12-bis ha trovato difetti importanti). Prossimo giro: R13.

## 2026-11-16 · v1.42 (difetto #60: un solo scaricamento per cartella)

- **Cosa è successo:** sul Mac giravano due scaricamenti insieme (il primo, creduto spento con il Mac, era vivo). Uno è uscito con codice 1 senza lasciare traccia nel log; l'altro (versione vecchia) era ancora attivo.
- **Correzione** (`42bd2ec` rosso, poi verde): blocco esclusivo su `<cache>/.scarica.lock`; un secondo scaricamento sulla stessa cartella esce con codice 2 e non fa richieste.
- **Correzione di una conclusione precedente:** la perdita di 20 giorni (v1.39, #47) è spiegata con più probabilità dai due processi in contemporanea. La correzione `F_FULLFSYNC` resta, come protezione.
- **Prove:** test verdi su 3.13 e 3.9; mutanti 39/39 su entrambe (W38, W40 nuovi; W39 tolto perché equivalente: chiudere il file libera comunque il blocco).

## 2026-11-16 · v1.43 (pacchetto redatto e messaggio 3 per il DGS)

- **Nuovo `governance/esporta_redatto.py`** (`4760f10` rosso, `186352f` verde; richiesta DGS-10, difetto #43): esporta il contenuto esatto di un commit, sostituisce nei file di testo le stringhe date al lancio (non scritte nel repository) e i nomi utente nei percorsi del Mac, scrive `MANIFEST.tsv` con le impronte prima e dopo, e si ferma se un dato resta in un file o nel nome di un file. Test 6/6 su 3.13 e 3.9, mutanti 12/12 (X05 e X11 sopravvissuti al primo giro: buchi nei test, chiusi).
- **Pacchetto `trading_brain_dgs05.zip`** dal commit `5b405f4`: 357 file, 26 redatti; SHA-256 `7319c67b990cdeb2…`. Ricontrollato in modo indipendente dallo strumento: nessun nome, utente, email, nome del computer o percorso personale; «stipendio» compare solo come voce che resta fuori dal repository, senza cifre.
- **Messaggio 3 al DGS** (`collaborazione/da-claude/direttore-sicurezza/5-MESSAGGIO-3-PARERI.md`): aggiornamento da DGS-04 e tre pareri per il titolare (soglia IA-02, regole della riserva, modello di scheda) più il controllo del pacchetto.

## 2026-11-16 · v1.44 (notte: chiusura della corsa R13 e log dei tentativi dello scaricatore)

- **Corsa dei mutanti su 3.13 dopo le correzioni R13:** 289/295 al primo giro; i 6 vivi (#71) erano buchi dei test, chiusi in TDD (`46eea94` rosso): ora ogni controllo dell'ancora git scatta DA SOLO con il suo messaggio, i minuti fuori sessione non riempiono i terzi, la potenza fuori dominio dà il nostro errore.
- **Log dei nuovi tentativi (richiesta dell'utente, pomeriggio del 16/11):** `dukascopy.richiesta_http` accetta `annota` e scrive una riga per ogni NUOVO tentativo (motivo: codice HTTP o tipo di errore di rete, attesa in secondi); lo scaricatore la collega al log con il giorno e il lato. Comportamento invariato; il registro CSV resta com'è (ha già il conteggio dei tentativi; cambiare le colonne romperebbe la continuità dei CSV in corso). Mutanti nuovi W42, W43.
- Corsa completa di convalida (3.13: scaricatore, esecuzione, DSR; poi tutta la 3.9) lanciata in sottofondo; esiti nel prossimo aggiornamento.

## 2026-11-17 · v1.45 (notte: strumenti per la fine dello scaricamento, convalida R13)

- **Corsa dei mutanti su 3.13 dopo le correzioni R13 e il log dei tentativi:** scaricatore 42/42, esecuzione 170/170, DSR e partizione 44/44 (più controllo della cache 11/11, riconteggio 31/31, simulatore 40/40 nella corsa precedente). Corsa completa su 3.9: ancora da fare.
- **`laboratorio/studi/taratura_completezza.py`** (`361fd5e` rosso, poi verde): per tarare le soglie PROVVISORIE di completezza (#49, #63) sui conteggi veri della cache: minuti in sessione e per terzo, percentili, giorni sotto una griglia di soglie, vigilie a parte, chiusure note escluse. Solo conteggi e date, mai prezzi. Mutanti TA01–TA06 6/6 (TA01 vivo al primo giro: mancava una festività CON dati; test aggiunto).
- **`controlla_cache --ask`**: confronto BID/ASK sullo stesso periodo (giorni con il file da un lato solo, vuoti da un lato solo), codice d'uscita 1 se non allineati. Mutanti Q12–Q16, 16/16.
- **Revisione notturna a occhi freschi** (revisore separato) su dati e governance: 13 rilievi, da riprodurre e smistare (vedi il prossimo aggiornamento). La revisione del nucleo del laboratorio è stata interrotta due volte dal limite d'uso: da riprendere.

## 2026-11-17 · v1.46 (notte: fuga nel pacchetto DGS-05, revisione notturna integrata)

- **#72, critico, errore mio:** il pacchetto `trading_brain_dgs05.zip` conteneva il nome dell'utente dentro uno ZIP annidato (4 file), e il mio controllo indipendente non apriva gli archivi. Corretto `esporta_redatto.py` (`1573ad7`): 7 codifiche, NFC/NFD, maiuscole, archivi rifiutati salvo esclusione dichiarata. Pacchetto rigenerato: `trading_brain_dgs05b.zip` (commit `1573ad7`, 364 file, 27 redatti, 2 archivi esclusi e dichiarati, SHA-256 `ccf54d6b…`), scansione indipendente anche degli archivi: pulito. **Il vecchio pacchetto non va inviato.**
- **Revisione notturna (dati e governance), 13 rilievi:** riprodotti uno per uno; veri corretti in TDD come #73–#84 (test rossi `34a4048`, `8757279`; correzioni `37fde1e`); 1, 2, 9 già chiusi in #72; 11 respinto in parte con il motivo nel REGISTRO-DIFETTI; 13 respinto per la parte sulla lettura della risposta.
- **Conseguenza da non nascondere:** quattro difetti del riconteggio (#75 comandi su più righe, #78 date compatte, #80 uscite con soli prezzi, #81 `toolUseResult`) toccano il censimento G-20261115-03 («riserva intatta»). La conclusione **va riconfermata** rilanciando il riconteggio corretto sul Mac.
- **#85** (revisore del laboratorio): completezza per minuti distinti (`cb34b05` rosso, `67ff7a6`).
- Mutanti: riconteggio 46/46, controllo della cache 20/20 (Q19 scartato prima come NON VALIDO dal controllo di validità: sintassi rotta, riscritto), scaricatore 48/48, su 3.13 e 3.9; X21 manuale sull'esportazione. Corsa completa su 3.9 di tutti gli script: in corso.
- **Revisione del nucleo del laboratorio (ripresa dopo l'interruzione), 14 rilievi:** registrati come #86–#94, **APERTI**. Riprodotti da Claude: #86 (verifica ripetuta con un secondo registro o un ramo nuovo) e #89 (la mia correzione #85 era incompleta). Gli altri sono riprodotti dal revisore su una copia e vanno riprodotti da Claude prima di correggerli. Non corretti stanotte: è finito il tempo concesso (fino alle 9). R14 bloccato.

## 2026-11-17 · v1.47 (pomeriggio: correzione dei difetti del laboratorio)

- **Riprodotti da Claude prima di correggere:** #87 (bytecode preparato: «AMBIENTE OK» con il codice dell'attaccante eseguito) e #88 (sysconfig falso), su 3.13 e 3.9, in una copia di `brain` (`1e6240f`). Un mio primo test di #88 era sbagliato (il modulo avvelenato si fermava da solo, il test passava per il motivo sbagliato): riscritto con copie funzionanti, come l'attacco del revisore.
- **Correzioni in TDD:** #86 (`69a82b5` rosso; registro canonico, verifica cercata in tutta la storia git, N massimo della storia), #87 e #88 (`7940914`), #89 (decodifica: minuti allineati e non ripetuti; la mia #85 era incompleta), #90 in parte (un solo esito, dopo la verifica), #91 (controllo dell'ambiente prima degli esiti), #93 (testa della riserva ricontrollata), #94 a, c, e.
- **Conseguenza pratica:** con #87 il programma si ferma se in `brain` ci sono cartelle `__pycache__` (create da esecuzioni senza `-B`). Prima di ogni esecuzione vera: cancellarle. Nel container ne ho cancellate di vecchie (file generati, ignorati da git).
- **Test modificati, dichiarati:** S7 in `test_esecuzione` ora registra la verifica prima dell'esito (#90); il test #85 della cache ora si aspetta un file non valido (#89).
- **Mutanti nuovi:** N35 (riscritto), N37–N52, P14, P15, W50, W51. Corsa completa su 3.13 e 3.9 in corso.- **#94 d** (`870225c` rosso, `975e942`): il fuso di Londra è confrontato con la regola europea dell'ora legale, giorno per giorno sui due periodi, prima di ogni esecuzione. Scritto in una copia di lavoro separata mentre girava la corsa dei mutanti, poi riportato sul ramo. Un mio test sbagliato corretto prima del commit: Dublino ha gli stessi orari di Londra e non è un errore.
- **#94 b:** opzioni in DA-31, nessuna scelta.
- **Mutanti del controllo della cache:** Q11 si era staccato dalla riga che avevo cambiato con #85 (lo script l'ha segnalato: «la sostituzione compare 0 volte»), riagganciato; Q21 dichiarato equivalente dopo #89. 20/20 su 3.13 e 3.9. Scaricatore 50/50 e riconteggio 46/46 su entrambe le versioni.

## 2026-11-17 · v1.48 (pomeriggio: riconteggio, BANCO-02, lanciatore)

- **Riconteggio corretto sul Mac** (`riconta2`, `riconta3`): 112 segnalazioni, tutte classificate per origine; nessuna dalla cache vera. **La riserva resta intatta** per tutto ciò che è contabile (`governance/censimento/RICONTEGGIO-20261117.md`). Passo 3360 confermato innocuo da Gemini (cartella temporanea, cache sintetica, dati veri esclusi). Lo strumento ora indica l'origine di ogni uscita (`60fa2de` rosso, `e3eeb08`; mutanti Z48–Z52, 51/51 su 3.13 e 3.9; due vivi al primo giro, Z49 e Z51, erano buchi dei miei test).
- **BANCO-02 di Gemini** (commit `0c65580` su `rev/gemini-banco02`): #86–#91 riprodotti tutti in modo indipendente su `296b014`. Rilanciati da Claude sul codice corretto, con il registro canonico: #86, #87, #88, #89 e #91 RESPINTI. #90 RIUSCITO, ed era atteso: una voce di sviluppo scritta a mano non si può impedire in un file locale (limite dichiarato).
- **#95, critico, errore mio:** gli output di BANCO-02 mostravano il codice avvelenato ESEGUITO anche quando l'attacco era respinto. Le mie correzioni #87 e #88 controllavano dopo gli import. Riprodotto, poi corretto con il lanciatore `brain/laboratorio/esecuzione/avvio.py`. Il comando documentato cambia:
  `python3 -I -S -B brain/laboratorio/esecuzione/avvio.py --modalita … --rapporto …`
- **Test modificati, dichiarati:** i test con il controllo dell'ambiente simulato dichiarano l'avvio dal lanciatore; il test del comando documentato ora cerca il lanciatore.
- **Mutanti nuovi:** N55–N61. La corsa del laboratorio è stata fermata e rilanciata sul codice finale.
- **D-24 (decisione del titolare):** modello di minaccia della regola d'uscita: contano i rilievi E e M a costo basso; prima della verifica un giro su tutte le manomissioni e la decisione sulla protezione del ramo. Aggiornati la proposta v3.2 §C, il modello di scheda H-003 §11, la scheda di stato e il mandato R14.

## 2026-11-17 · v1.49 (sera: R14 di Gemini integrato)

- **R14 di Gemini:** 1 critico (R14-01) e 4 importanti (R14-02…05), più minori. Riprodotti da Claude R14-01 (cartella `statistics/` con `__init__.pyc`) e R14-02 (Python di Apple, simulato con `PYTHONPYCACHEPREFIX`). Tutti corretti in TDD come #96–#104.
- **Regola nuova dell'esportazione redatta:** solo testo UTF-8, ogni altro file rifiutato salvo esclusione dichiarata. Più semplice e più robusta delle firme degli archivi.
- **Test modificati, dichiarati:**
  - nel test dell'esportazione non c'è più un binario nel repository di prova;
  - il bytecode d'attacco va sempre in `__pycache__`;
  - un mio test della storia parziale era costruito male: il clone non indicava il ramo. Corretto e controllato al contrario: fallisce sul codice vecchio.
- **Contatore dei giri puliti:** resta a zero.
- **Corsa completa dei mutanti:** in corso sul codice finale.
- **DGS:** il DGS si era fermato a DGS-04 (archivio di `83c8956`); il messaggio 3 e i pacchetti `dgs05` e `dgs05b` non sono mai stati inviati (quindi la fuga #72 non è mai uscita). Preparati il messaggio 4 di riallineamento e il pacchetto `trading_brain_dgs06.zip` (commit `c5ca93d`, SHA-256 `58d29429…`, 369 file, 29 redatti, due zip esclusi; ricontrollato in modo indipendente, nessun residuo).
- **Corsa completa dei mutanti sul codice finale (17/11 sera):** esecuzione 213/213 su 3.13 e 3.9 (205 nella corsa completa, 8 riagganciati o coperti e rifatti a parte; N57 dichiarato equivalente), simulatore 40/40, DSR 44/44, riconteggio 53/53, controllo della cache 20/20, scaricatore 50/50. Errore mio registrato come #105 (mutanti staccati dalle mie correzioni). 366 test verdi su 3.13 e 3.9.

## 2026-11-17 · v1.50 (pomeriggio, titolare assente: strumenti di contorno e preparazioni)

Nulla di questo tocca il candidato `8e51ce9` su cui lavora R15.

- **Rendiconto dell'intersezione BID/ASK e dei buchi** (`laboratorio/studi/intersezione_bid_ask.py`; test rossi `ff…` poi `577887c`). Richiesta del DGS (DGS-05 P5).
  - Per seduta: minuti comuni validi (BID e ASK presenti, ASK ≥ BID su apertura e chiusura, confronto solo interno), solo BID, solo ASK, comuni non validi, mancanti, conteggi per terzo, buco più lungo con i bordi, stato dei file per lato.
  - Per anno: conteggi e percentili, più una griglia DIAGNOSTICA di soglie, dichiarata come non decisione.
  - Solo conteggi e date: un test e un mutante (IX14) provano che nessun prezzo esce, nemmeno nel JSON.
  - **Errori miei, trovati prima del commit del codice:**
    - un conto sbagliato in un test (10 minuti mancanti nel primo terzo lo portano al 94,3%, sotto il 95%);
    - 5 mutanti vivi su 16 al primo giro su 3.13: i test non coprivano l'ASK sotto il BID solo in apertura, l'esclusione per la sola quota della seduta, la cartella ASK mancante e gli stati per anno; IX14 era progettato male (non inseriva prezzi).

    Test rafforzati e dichiarati come scritti dopo i mutanti; IX14 riscritto.
- **Bozza del modello H-003** con le integrazioni P3 del DGS e DA-31 (`laboratorio/ipotesi/MODELLO-SCHEDA-H-003-BOZZA-P3.md`). **NON applicata:** è la decisione 5 del titolare. Ogni punto è marcato [DOC] o [METODO]. L'affermazione «stop prima del target nella stessa barra, come H-002» è stata controllata su `H-002-ORB-v3.md` (riga 85) e su `orb_londra.py` (righe 231–239).
- **Pilota del collaudo IA-02** (`laboratorio/studi/collaudo_ia02.py`; test rossi poi codice).
  - Contiene tre metodi (ingenuo, HAC Newey–West con regola dei ritardi fissata, bootstrap a blocchi mobili), il generatore AR(1) stazionario, i limiti di Clopper–Pearson e 4 celle impegnate.
  - Riproduce i riferimenti analitici del DGS (F = 1,664691 e 2,991111; tassi 6,4371% e 12,8551%).
  - **NON eseguito con le repliche vere:** è la decisione 4 del titolare.
  - **Errore mio:** nella risposta 7 avevo stimato «qualche ora di calcolo»; misurato, il pilota completo richiede qualche minuto. Corretto.

## 2026-11-17 · v1.51 (pomeriggio: R15 di Gemini)

- **R15 consegnato alle 15:03** (`6509a00`, integrato con un merge: solo la cartella di Gemini).
  - Candidato `8e51ce9` e ambiente dichiarati.
  - **Verifica di R14:** tutte le correzioni chiuse.
  - **Taratura su 80 mercati inventati:** 0/20 promozioni senza vantaggio; 2/20 con vantaggio debole; 16/20 e 17/20 con vantaggio medio e forte.
  - Rilievi:
    - #106, importante dubbio: un mio test sul Python di Apple;
    - #107–#111, minori nel perimetro.
- **#106 corretto (solo test):** il caso «senza -B» si salta, dichiarandolo, dove `-I` implica già `-B`; il controllo della cartella esterna del bytecode diventa un test a sé. Sul Python di Apple il mutante N63 diventa **equivalente** (lì `-B` non può mancare): dichiarato.
- **#108, misura:** il rendiconto dell'intersezione conta a parte i minuti con estremi incrociati (mutanti IX17, IX18), così i dati veri diranno quanto conta il rilievo.
- **Minori #107, #109, #110, #111 nel codice sigillato: NON corretti.** Il titolare aveva chiesto di non toccare `8e51ce9`. Proposte in `collaborazione/da-claude/PROPOSTA-MINORI-R15.md`.
- **Contatore:** 0 su 2. R15 diventa il **primo giro pulito** se il titolare esclude i due casi «dubbio» (#106 è un difetto di un test, #108 una scelta di metodo).
- **DGS-06 ricevuto (sera):** controllo riga per riga della risposta 7, ricalcoli indipendenti e quattro bozze (DA-31 completa, testi P3, pilota a 12 celle, procedura per l'ordine delle finestre). **Errata di Claude** registrata in fondo alla risposta 7: arrotondamenti per difetto, conclusione «da +0,25 R» troppo forte, «non passa mai» sbagliato, stima dei tempi insufficiente. Le bozze del DGS sono proposte: nessuna applicata.


## 2026-11-17 · v1.52 (sera, su delega del titolare: minori di R15 e pilota nel disegno del DGS)

- **Delega:** il titolare ha scritto «per le domande che mi hai fatto fai quello che ritieni più utile». Scelte di Claude, tutte reversibili dal titolare:
  - **minori #107, #110, #111 corretti prima di R16** (TDD: test rossi `6f8fd86`, codice `303890b`; mutanti K15a–K15d, W52). Nuovo candidato per R16: `303890b`. #109 resta registrato (scelta di metodo, non un errore del codice).
  - Nei test, **due chiamate allo screening ora passano la copertura in modo esplicito**: prima si appoggiavano al valore predefinito sbagliato (1,0) di #107. La pipeline vera la imposta sempre (`esegui_h002`). Dichiarato.
  - **R15 NON conta come primo giro pulito: lettura stretta di D-24.** #106 era un errore in un mio test; dichiararlo innocuo andrebbe a mio vantaggio (conflitto d'interessi). Il titolare può ribaltare la scelta. **Contatore: 0 su 2.**
  - **Ordine delle finestre, DA-31, modello H-003: NON toccati.** Restano al titolare.
- **Pilota del collaudo IA-02 nel disegno del DGS (DGS-06 §2c)** (`laboratorio/studi/pilota_ia02.py`; test rossi `616c428`, poi codice).
  - 12 celle: gaussiane iid, AR(1) ρ = 0,25, conteggi casuali con componente comune, perdite rare. D = 1.000; HAC di Bartlett con L = 6; bootstrap circolare a blocchi ℓ = 10 con intervallo basic, B = 3.999; M = 3.000.
  - **Differenza dichiarata dal disegno:** niente PCG64 di NumPy (il progetto usa solo la libreria standard). I flussi vengono da un SHA-256 della stessa tupla (master, fase, cella, replica, componente).
  - **È SVILUPPO del metodo, non certificazione:** la scelta di metodo, margine e soglia va poi validata su repliche nuove (fase diversa).
  - **Costo misurato** in tempo di CPU: circa 0,13 s per replica, quasi tutto bootstrap. Totale circa 4.700 s, circa 20 minuti su 4 processi.
  - **Errori miei nei test:**
    1. Il test rosso del quantile bootstrap usava dati con blocchi tutti uguali (periodo 5, blocco 10): tutte le medie coincidevano e i ranghi non venivano provati davvero. Ho aggiunto, dopo il codice, un caso con medie diverse (dichiarato).
    2. In quel caso aggiunto avevo scritto l'indice 97 per il rango 97 (giusto: 96). L'ha fermato il test stesso; ho corretto il test, non il codice.
    3. Nessun test controllava come si classificano promozioni, bocciature e coperture di una cella. Ho aggiunto, dopo il codice, un confronto col calcolo a mano su casi scelti perché contengano ogni esito (dichiarato).
  - Mutanti PI01–PI20 in `mutazioni_esecuzione.py`, modulo di test nella SUITE.
    4. Prova rapida dei mutanti PI sul solo modulo del pilota: **PI05, PI09 e PI20 sopravvissuti, tutti per test deboli miei.** Il test dei conteggi non guardava la componente comune; nel test HAC a mano K medio valeva 1, quindi K̄² = K̄; Z era confrontato con sé stesso. Aggiunti tre controlli dopo i mutanti (dichiarato): varianza di S nei giorni con K = 3, caso HAC con K̄ ≠ 1, valore di Z. Ora la prova rapida li uccide tutti e 20; la corsa ufficiale con la SUITE completa segue.
- **Dati (sul Mac del titolare, sera):**
  - **Scaricamento BID finito** (08/06/2009 → 11/11/2023): 3.914 giorni già in cache, 1.356 scaricati, 0 errori http, 0 rovinati, 0 «404»; 1 file trovato in cartella ma non registrato (il giorno del riavvio dell'11/02/2020), ora registrato.
  - **Controllo `controlla_cache` sul BID 2005-01-01 → 2023-11-11: ESITO PULITO.** Nessun giorno senza file, nessun feriale vuoto, nessun file illeggibile, nessun temporaneo rimasto. Le chiusure note vuote sono 1–3 per anno. I 30 giorni «corti» visti sono vigilie e festività (Venerdì Santo, 2 gennaio, 26 dicembre). Solo conteggi: nessun prezzo letto né stampato.
  - **ASK in corso:** circa il 22% (al 07/02/2009), con rallentamenti di Dukascopy (HTTP 503) gestiti dai tentativi.

## 2026-11-17 · v1.53 (notte: protocollo DGS-07 adottato e impegnato)

- **DGS-07 ricevuto**: protocollo deterministico per scegliere (fase 1) e validare (fase 2) il metodo del test IA-02. **Il titolare l'ha adottato «così com'è» (D-25).** DGS-06 e DGS-07 sono archiviati senza modifiche in `collaborazione/da-chatgpt/`.
- **Impegno prima della lettura** (`laboratorio/studi/IMPEGNO-PROTOCOLLO-IA02.md`, commit `4f076c4`): impronte, versione del pilota, ambiente, serializzazione dei semi, matrice, soglie, e attestazione di chi ha visto cosa.
  - **Dichiarazione di Claude:** durante i test ha visto piccoli conteggi della fase 0 (40 repliche, B = 99, celle 2, 3, 7). Per DGS-07 la fase 1 resta quindi **sviluppo** e l'impegno non si descrive come anteriore a ogni lettura. La fase 2 è prospettica.
  - **Errore mio, per omissione:** nel messaggio 5 al DGS avevo scritto «nessuno ha ancora visto i risultati» senza dichiarare quei conteggi di fase 0.
- **#112 (errore mio):** il bootstrap del pilota accettava un intervallo di ampiezza nulla, contro DGS-06 §2c. Il mio test rosso si aspettava proprio quel valore e io avevo adattato il codice al test invece che al disegno. L'ha fatto emergere DGS-07 §2a.3. Corretto in TDD (`069e09a` → `4883dd9`).
- **Rendiconto del protocollo** (`laboratorio/studi/protocollo_ia02.py`, TDD):
  - conteggi E, P, B, I per metodo × margine × cella;
  - Clopper–Pearson unilaterale (riproduce i valori del DGS: 60/3.000 e 248/12.000);
  - dieci controlli e classifica della fase 1;
  - verdetto della fase 2, che esegue da sola l'inventario dei semi e i 216 confronti fra flussi.
- **Pilota:** salva i limiti grezzi per replica con l'impronta della propria versione e può girare con un solo metodo. Un test prova che ordine delle celle e numero di processi non cambiano il file.
- **Mutanti:** PI21–PI25 e PR01–PR27. Nella prova rapida è sopravvissuto PI24: nessun test vedeva un errore salvato come intervallo finto. Ho aggiunto il test dopo il mutante (dichiarato).
- **Corsa dei mutanti su 303890b interrotta:** si è fermata al limite di tempo (circa 2,5 ore) senza risultati, perché avevo fatto girare insieme Python 3.13, Python 3.9, il pilota e i test su 4 processori. Errore di pianificazione mio. Rilanciata in sequenza, con l'uscita riga per riga.

## 2026-11-18 · v1.54 (notte: collaudo IA-02 eseguito secondo DGS-07)

- **Riavvio del contenitore (23:30 circa):** si sono fermati la corsa dei mutanti e la prima corsa della fase 1, che non aveva scritto nulla e quindi non è stata vista da nessuno. Tutto era già su GitHub. Rilanciata la fase 1 nella versione che salva i limiti grezzi (impegno §4).
- **Fase 1** (3.000 repliche, 8 candidati): ammissibili solo HAC e bootstrap con Δ = 0,05. **Vince il bootstrap** per la somma delle promozioni (421 contro 416), a parità sul minimo. Candidato congelato e pubblicato prima della fase 2 (`7ac484e`).
- **Fase 2** (12.000 repliche nuove, solo il candidato): **CONFERMATO NEL DOMINIO DEL PILOTA**. 10 controlli su 10; semi 720.000/720.000 distinti; 0 segnalazioni su 216 confronti fra flussi.
- **Osservazioni di Claude** (impegno §6 e §8), da portare al DGS e al titolare:
  1. La regola «U_CP ≤ 0,025» esclude un metodo tarato esattamente: serve un tasso vero intorno al 2% o meno. Si poteva dedurre prima dei risultati.
  2. Il margine è imposto dalla cella delle perdite rare.
  3. Con Δ = 0,05 a 1.000 sedute la potenza è circa 3% a +0,20 R e 53–72% a +0,30 R.
  4. Fra bootstrap e HAC hanno deciso 5 promozioni su circa 420.
- **Roadmap:** riscritta (`piano/ROADMAP-20261117.md`), con il controllo dei passaggi.
  - Archiviato il dossier del DGS del 17/11, che mancava.
  - Errata: il Gate 1 era scritto «chiuso» ma è configurato e NON riconciliato (rilievo G-20261113-01, l'ha notato il titolare). P-11 e P-14 sono già confermate.
- **Conto per i costi:** la demo MT5 non è disponibile per la società europea di FP Markets, né dal sito né dall'app. Il titolare ha creato una demo MT4 Raw. Opzioni da riprendere: conto MT5 Raw reale a saldo 0 in sola lettura (consigliata, con password «investor»), demo MT4 o demo cTrader. Nessun dato del conto è registrato qui.

## 2026-11-18 · v1.55 (notte: mutanti completi sul candidato)

- **Mutanti, corsa completa sulla punta del ramo** (perimetro identico a `303890b`), una versione di Python alla volta:
  - `mutazioni_esecuzione`: su 3.13 la prima corsa ha dato 295/298;
  - su 3.9: 133/133 più 164/164, cioè 297 su 297.
- **I 3 casi della corsa su 3.13, tutti miei:**
  - **PI15** non valido: la correzione di #112 aveva cambiato la riga che il mutante cercava (stesso tipo di errore di #105). Riallacciato.
  - **PI10** sopravvissuto: dopo #112 il controllo `V > 0` è ridondante. **Dichiarato equivalente**, con il motivo scritto nello script.
  - **K15c** sopravvissuto: il test di #110 accettava qualunque ValueError, e l'elenco vuoto ne produceva uno lo stesso più avanti. Il test ora controlla il messaggio. K15c non era mai stato verificato prima, perché le corse su `303890b` si erano interrotte.
  - Dopo le correzioni: 14/14 su K15 e PI1x, sia su 3.13 sia su 3.9.
- **Altri script, tutti al 100% su 3.13 e su 3.9:** scaricatore 51/51 (con W52), controllo della cache 20/20, riconteggio 53/53, ORB 40/40, DSR e partizione 44/44.
- **Messaggio 6 al DGS** pronto (`collaborazione/da-claude/direttore-sicurezza/9-MESSAGGIO-6-RISULTATI-IA02.md`): risultati delle fasi 1 e 2, osservazioni, richiesta di opzioni per il titolare.

## 2026-11-18 · v1.56 (mattina: R16 di Gemini integrato)

- **R16 integrato e verificato sul codice** (`H-002-REVISIONI.md`, sezione R16). Nuovi difetti #113–#115, tutti minori.
  - #113 e #115: test deboli di Claude, corretti; mutanti IX19, CO12 e PI26 uccisi 3/3 su 3.13 e 3.9.
  - #114: iteratore in `criteri.verifica`, nel perimetro; aperto, opzioni al titolare.
- **Contatore D-24: 1 su 2.** R16 è il primo giro pulito, da confermare dal titolare per il caso di #112, fuori perimetro.
- **ASK:** al 30/12/2011 la mattina del 18/11, circa 37%. **Errata di Claude:** la stima «10–12 ore» del 17/11 era troppo ottimista; a questo ritmo, con molti 503 di Dukascopy, servono ancora circa 1,5–2 giorni.
- **Osservazione per il titolare:** i rapporti di Gemini contengono percorsi locali del Mac con il nome dell'utente (anche nei giri precedenti). I file di Gemini non si modificano (D-11). Proposta: nel prossimo mandato chiedere di scrivere `~` al posto del percorso completo. L'esportazione per il DGS li redige già.

## 2026-11-18 · v1.57 (mattina: decisioni del titolare, #114 corretto)

- **Decisioni del titolare:**
  - D-26: #112 non conta per D-24, contatore **1 su 2**;
  - D-27: #114 si corregge subito;
  - D-28: percorsi con `~` nei mandati a Gemini;
  - D-29 e D-30: trascritte DA-26 (partizione) e DA-29 (obiettivi), che erano decise ma figuravano solo fra le aperte.
- **#114 corretto in TDD** (test rosso nel commit delle decisioni, codice in `e476a9a`): `criteri.verifica` legge `anni` una volta sola.
  - Nuovo mutante K15e; K15c riallacciato al testo nuovo.
  - Mutanti di `criteri.py`: **33/33 su 3.13 e su 3.9**.
  - **Nuovo candidato per R17: `e476a9a`.** Rispetto a `303890b` nel perimetro cambia solo `criteri.py` (due righe).
- **Messaggio 6 al DGS:** il titolare l'ha incollato in ChatGPT; si attende DGS-08.

## 2026-11-18 · v1.58 (DGS-08 ricevuto)

- **DGS-08** archiviato in `collaborazione/da-chatgpt/DGS-20261118-08-riscontro-ia02.md`. Concorda con selezione e verdetto della fase 2 (ricalcoli indipendenti); elenca ciò che resta attestato da Claude (impegno §9).
- **Errata di Claude:** l'osservazione «un metodo tarato non può passare; nessuno l'ha scritto» era sbagliata due volte. Passare è improbabile, non impossibile (4,14% in fase 1, 0,099% in fase 2), e la prudenza era scritta in DGS-07 §2a.7. È la seconda volta che esagero in questo modo: lo stesso errore del «non passa mai», già corretto in DGS-06.
- **Opzioni per la regola futura di IA-02 (DGS-08 §4c), decisione del titolare:**
  1. bootstrap con Δ = 0,05 così com'è;
  2. più sedute;
  3. famiglia di strategie senza perdite rare;
  4. nuovo protocollo.
  Nessuna richiede di riaprire il verdetto.
- **Regole di spesa (DGS-08 §4d):** spiegate con l'esempio di α = 5%; restano da decidere.

## 2026-11-18 · v1.59 (strategie esterne e GBPJPY)

- **D-31:** il titolare sceglie il metro severo in verifica (opzione A di DGS-08).
- **Il titolare sta analizzando strategie con ChatGPT, anche su GBPJPY.** Claude ha segnalato tre punti:
  1. **Grafici di GBPJPY** solo dal 15/11/2023 in poi, come per l'oro, e censimento di quanto già visto: altrimenti la riserva di GBPJPY si brucia.
  2. **Conflitto di ruolo:** il DGS non dovrebbe giudicare il metodo di strategie che ha contribuito a progettare. Opzioni al titolare: un altro revisore (DeepSeek o Gemini) per quelle schede, oppure il DGS fuori dalla progettazione.
  3. **GBPJPY è un mercato nuovo:** servono DA-27, scaricamento, stesse date dell'oro e adattamento degli strumenti.
- **Rischio delle strategie pubblicate:** l'autore le ha provate quasi certamente sugli anni che per noi sono riserva.
- **Messaggio 7 al DGS** pronto (`collaborazione/da-claude/direttore-sicurezza/10-MESSAGGIO-7-STRATEGIE-E-GBPJPY.md`).
- **Separazione dei ruoli, primo passo:** il titolare analizza le strategie in una **chat separata** di ChatGPT; il messaggio 7 va nella chat del DGS, con la nota sulla memoria fra chat. Nella chat delle strategie il titolare incolla le regole: dati e grafici solo dal 15/11/2023, provenienza di ogni idea, regole meccaniche, nessun ruolo di revisione. In attesa: elenco degli anni di GBPJPY già guardati.

## 2026-11-18 · v1.60 (Mac instabile: copia di sicurezza dei dati veri)

- Il Mac del titolare si spegne anche con la batteria carica. **Lo scaricamento ASK però non si è mai fermato**: stessi processi 6113 e 6114 di ieri, al 02/02/2013 circa. Il secondo avvio è stato respinto da «GIÀ IN CORSO»: la protezione contro due scaricamenti ha funzionato.
- **Copia di sicurezza di `brain/dati/reali/`:** `dati_reali_20261118.zip`, 136 MB, SHA-256 `0aec0b91f6a6f1633b301572261ebef534f626c4af488acc8f41f19e10d14113`. Fatta dal titolare con zip, senza aprire i file.
- **Procedura prima e dopo l'assistenza:** `piano/PROCEDURA-ASSISTENZA-MAC.md`. Claude la richiama quando il titolare porta il Mac in assistenza.
- **Copia dei dati fuori dal Mac:** il titolare ha copiato `dati_reali_20261118.zip` nel proprio cloud. **Diagnosi software:** macOS 14.5 (maggio 2024), modalità risparmio energetico sempre attiva, nessuna app che limita la carica. Prossimi passi: risparmio energetico «Solo con batteria», aggiornamento di macOS, nuovo avvio dello scaricamento ASK, controllo di «Low Power Sleep» nei giorni successivi.

## 2026-11-18 · v1.61 (DGS-09: idee pubblicate, GBPJPY, ruoli)

- **DGS-09** archiviato (`collaborazione/da-chatgpt/DGS-20261118-09-idee-pubblicate-gbpjpy-ruoli.md`).
- **Fatto importante, segnalato dal DGS:** nella chat del DGS è arrivato un riassunto del lavoro che il titolare sta facendo nella chat delle strategie (il video su GBPJPY). La memoria di ChatGPT passa informazioni fra le chat, quindi **due chat separate non bastano** per una revisione cieca. Proposte del DGS: progetti distinti con memoria limitata al progetto, oppure chat temporanea; per le schede che richiedono cecità, un revisore che non le ha progettate.
- **Istituiti** su proposta del DGS:
  - registro della provenienza delle idee (`laboratorio/ipotesi/PROVENIENZA-IDEE.md`), prima riga retrospettiva P-001 per il video su GBPJPY;
  - censimento dell'esposizione a GBPJPY (`governance/censimento/CENSIMENTO-GBPJPY.md`).
  Entrambi da completare dal titolare.
- **GBPJPY** resta pianificazione finché non si chiude la base sull'oro (sequenza in 6 passi, DGS-09 §2a). D-31 vale per GBPJPY solo con una corrispondenza motivata al dominio collaudato; se cambia una condizione materiale (quota, durata, stress), serve una giustificazione o un collaudo specifico.
- **Mac aggiornato a macOS 14.8.9 (23J631)** il 18/11 pomeriggio. Prima, gli installatori di app già installate o mai installate sono stati spostati nel Cestino; le app restano. Un primo controllo di Claude sulle app installate era sbagliato (`ls` con due percorsi dava «manca» anche per app presenti): fermato prima di qualunque azione e corretto. **Scaricamento ASK ripartito** (nuovi processi) dal 30/05/2013, con il primo tentativo in URLError subito dopo il riavvio; i tentativi successivi lo gestiscono.
- **Costi del broker, primo passo (Gate 1, DA-25):** il titolare è entrato in MT5 con il conto Raw reale a saldo 0, in sola lettura. Specifiche di XAUUSD.cyr registrate in `dati/costi/SPECIFICHE-FPMARKETS-XAUUSD-20261118.md`:
  - commissione 6 USD per lotto all'ingresso, da confermare con un estratto conto;
  - margine pari a una leva 1:20;
  - spread istantaneo di 0,40 USD.
  Lo spread per ora del giorno richiede l'esportazione dei tick dalla versione desktop di MT5.
- **Strumento dei costi del broker** (`dati/pipeline/costi_tick.py`, TDD: test rossi `b38d426`, poi codice): legge i tick esportati da MT5 desktop, calcola lo spread per ora UTC e per la sessione di Londra e il costo in R per diverse distanze dello stop. **Rifiuta l'intero file se contiene un tick anteriore al 15/11/2023** (riserva, D-29) e non stampa prezzi. Mutanti CT01–CT12: con lo script del controllo della cache, **32/32 su 3.13 e 3.9**.
- **Messaggio 8 al DGS:** il file allegato non era arrivato a ChatGPT; il titolare incolla le parti (A) e (B) in due messaggi. **Incoerenza mia nella bozza del modello H-003:** le sezioni D (metodo «da scegliere») ed E (soglie +0,15) sono anteriori a D-31 e non le avevo riallineate quando ho aggiunto G–J. Segnalata al DGS con richiesta di testo allineato (+0,20 / +0,10, bootstrap).
