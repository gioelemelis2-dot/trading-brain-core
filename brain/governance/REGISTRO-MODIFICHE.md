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

## 2026-11-19 · v1.62 (R17 in corso: correzioni anticipate)

- **#117:** due test deboli di Claude in `protocollo_ia02`, trovati da Gemini in R17 (M-R17-02, M-R17-03). Corretti con due test dichiarati; mutanti PR28 e PR29, uccisi su 3.13 (PR20–PR29: 10/10).
- **Script dei mutanti** (`mutazioni_esecuzione`, `mutazioni_scarica_cache`, `mutazioni_controlla_cache`): ora **stampano ogni esito appena è pronto**. Prima accumulavano tutto e stampavano solo alla fine: in R17 la corsa di Gemini con un solo processo è andata in timeout senza stampare nulla, e l'ha dovuta dividere in quattro blocchi. Difetto pratico rilevato da Gemini.
- **Scaricamento ASK:** fermato con codice 3 (molti 503 di Dukascopy sul 29/09/2013), a 4.290 file. Rilanciato con un ciclo che riprova ogni 30 minuti solo per il codice 3.
- **Batteria:** nessun «Low Power Sleep» dopo l'aggiornamento (ultimo il 18/11 alle 13:37), con il registratore attivo.
- **Verifica:** PR20–PR29 10/10 anche su 3.9. Gli script modificati funzionano: CT01–CT09 9/9 e W5x 3/3 su 3.13, con ogni esito stampato appena pronto.

## 2026-11-19 · v1.63 (DGS-10: revisione del modello di scheda H-003)

- **DGS-10** archiviato (`collaborazione/da-chatgpt/DGS-20261119-10-revisione-modello-h003.md`). Il modello A+B richiede correzioni prima del sigillo. **Incoerenza principale nel §8:** D, E e I potrebbero dare verdetti diversi alla stessa prova. Proposta: una sola definizione del metro (I) e una sola tabella dei verdetti (E). Testi sostitutivi pronti per A–J. Classificazione [DOC]/[METODO] clausola per clausola.
- **Errore di Claude segnalato dal DGS:** nella bozza (sezione I) avevo scritto «la quota scende all'1,25% per una seconda variante **o una seconda apertura**». È sbagliato: con α = 5% e a = α/[j(j+1)m], l'1,25% corrisponde a j = 1 e m = 2 (due varianti nella prima apertura), mentre una seconda apertura (j = 2, m = 1) dà lo 0,8333%. Avevo confuso i due casi.
- **Decisioni del titolare aperte** (DGS-10 §4 e §5):
  - DA-31, due stati o tre stati, con la tabella delle priorità;
  - politica di riesame del «non decidibile»;
  - regola dello screening;
  - minimi e anni valutabili (D).
- **Ordine consigliato dal DGS:** subito G, H, F; prima del sigillo della prima scheda, I e le decisioni; dopo il sigillo, screening, poi compatibilità e prenotazione.
- **Mac (19/11, notte):** quarta ibernazione e terza con lo stesso schema, ripresa dal registratore: a batteria 90% → 12% in un minuto, dopo l'aggiornamento di macOS. **Diagnosi: batteria guasta (hardware).** Assistenza da programmare dopo la consegna di R17 e la copia finale dei dati (`piano/PROCEDURA-ASSISTENZA-MAC.md`). Il ciclo di scaricamento ASK è sopravvissuto.
- **D-33:** strategie in pausa finché la macchina non è finita. **Errore di priorità di Claude:** avevo preparato prompt per catalogare le operazioni dell'autore prima di aver chiuso l'infrastruttura, contro l'ordine concordato e contro DGS-09. Il titolare l'ha fermato.

## 2026-11-19 · v1.64 (audit globale e messaggio 9 al DGS)

- **Audit globale** su mandato del titolare, in sola lettura (`collaborazione/da-claude/AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`, commit `a77c7c6` e `1f61536`). Durante l'audit nessun altro file è stato modificato: questa voce di registro è scritta dopo la consegna.
- **Rischi principali:**
  1. Potenza del metro D-31 contro gli obiettivi del titolare: circa 24% a +0,25 R con 1.000 sedute, in un'approssimazione normale dichiarata come stima.
  2. Il criterio D-31 non è nel codice della verifica sigillata (`criteri.verifica` controlla «R medio netto > 0»).
  3. False promozioni con perdite rare fuori dal dominio collaudato: 11,7% su un esempio inventato.
- **Altri rilievi:**
  - i file di conteggio di N sono tre;
  - il ciclo di revisioni non ha una «definizione di fatto»;
  - Guardian, journal e previsioni non sono mai stati usati;
  - la documentazione di continuità è vecchia.
- Questi rilievi **non sono ancora nel REGISTRO-DIFETTI**: si assegnano con le decisioni del titolare.
- **Errore trovato nella seconda lettura:** avevo proposto la riconciliazione del G0 sulla demo senza dire che la demo è MT4, mentre le specifiche dei costi sono del conto MT5. Corretto nel rapporto.
- **Messaggio 9 al DGS** (`direttore-sicurezza/12-MESSAGGIO-9-AUDIT-GLOBALE.md`): richiesta di controverifica dei sei punti, con ricalcolo autonomo della potenza e di 0,998^1000.

## 2026-11-19 · v1.65 (documento unico delle decisioni)

- **`governance/DECISIONI-DA-PRENDERE-20261119.md`:** otto decisioni aperte per finire la macchina, con le opzioni e il consiglio di Claude. **Nessuna è decisa:** spettano al titolare.
  1. Definizione di fatto e collocazione del criterio D-31.
  2. DA-31 e politica dei «non decidibili».
  3. Screening.
  4. Minimi e anni.
  5. Regole di spesa.
  6. Metro contro obiettivi.
  7. Custodia dei dati.
  8. Pilastri fermi.
- **Omissione dell'audit, trovata da Claude preparando le decisioni:** il registro consuma le date per calendario e per tutti i mercati. Con 4.912 giorni feriali nella riserva e D = 1.000 sedute, **bastano circa 4 verifiche in tutto il progetto**. Con α_j = 5%/[j(j+1)], la potenza a +0,30 R scende da circa 72% (1ª apertura) a circa 39% (4ª), come stima. Le quote dalla 2ª apertura non sono collaudate. Aggiunta come punto 9 al messaggio 9 del DGS.
- **Incoerenza segnalata:** con 1.000 sedute (circa 4 anni) il criterio «ultimi 5 anni positivi» non si può valutare senza anni parziali (già indicato in DGS-10 §6); le opzioni sono nella decisione 4.

## 2026-11-19 · v1.66 (decisioni D-34 … D-40)

- Il titolare ha deciso sul documento unico: **1-A** (D-34), **2-B-y** (D-35, chiude DA-31), **3-C con +0,25 R** (D-36), **4-A** (D-37), **5-A** (D-38), **7-A** (D-39), **no alla 8** e **la 6 dopo il DGS** (D-40).
- Per la 2 e la 3, le precisazioni (riesame «y» e soglia +0,25 R) sono state chieste da Claude con una domanda esplicita: il titolare aveva risposto solo «2 b» e «3 c».
- **Lavoro tecnico che ne segue (D-34):** modulo nuovo per il criterio D-31 con i tre esiti, lo screening D-36 e i minimi D-37, in TDD; registro unico di N; poi la prova generale a vuoto.

## 2026-11-19 · v1.67 (modulo del verdetto D-31)

- **`laboratorio/verdetto/verdetto_d31.py`** (D-34, fuori dal perimetro sigillato), in TDD: test rossi `e9231cb`, poi il codice.
  - **Tre esiti** con la tabella delle priorità di DGS-10 §4 (D-35).
  - **Minimi** di D-37: 1.000 sedute, 300 trade, 200 sedute con trade.
  - **Screening** di D-36: media > +0,25 R, L > 0, potenza ≥ 50%.
  - **Veto per blocchi**: soglia e minimo li fissa la scheda.
  - **Metro di riferimento collaudato:** `pilota_ia02.intervallo_bootstrap`, con impronta congelata `717e5599…`. Il modulo si rifiuta di calcolare se il pilota cambia.
- **Verifica:**
  - 32 test verdi su 3.13 e 3.9;
  - mutanti VD01–VD46 con `tests/mutazioni_verdetto.py`: **45/46 su 3.13 e 3.9**. VD13 è dichiarato equivalente.
- **Difetto #118:** tre errori miei nei test rossi, corretti prima della consegna.
- **Precisazione su D-36 (da confermare dal titolare):** i confronti stretti valgono per la media (> +0,25 R) e per il limite (> 0); la potenza è «≥ 50%», come scritto nella decisione.
- **Restano**, dall'elenco D-34:
  - il registro unico di N;
  - la clausola sulle code;
  - i tipi epistemici nei rapporti;
  - il collegamento all'esecutore;
  - la prova generale a vuoto;
  - i 2 giri di revisione del modulo.

## 2026-11-19 · v1.68 (DGS-11: controverifica dell'audit)

- **DGS-11** archiviato (`collaborazione/da-chatgpt/DGS-20261119-11-controverifica-audit.md`, nome del titolare sostituito).
- **Riscontro di Claude:** `collaborazione/da-claude/RISCONTRO-DGS-11.md`. Tutti i numeri del DGS sono confermati.
- **Errore di Claude, confermato e corretto:** l'11,7% di false promozioni dell'audit (rischio n. 3) era in gran parte un **artefatto del generatore**: vincite tutte uguali, più un intervallo di ampiezza circa 1e-13 accettato per arrotondamento. Rifatto con B = 3.999 e vincite realistiche: 0/300 con code di −20 R, 5% con −50 R. Errata aggiunta in testa all'audit; difetto #119 aperto.
- **Errore di metodo dell'audit**, accettato (DGS-11 §8): ho giudicato la macchina intera con le proprietà di un solo criterio.
- **Nuove decisioni per il titolare** (riscontro §5):
  - (a) metro contro obiettivi, con le opzioni A6 e A7 aggiunte dal DGS;
  - (b) testo della clausola sulle code;
  - (c) regola per il difetto #119;
  - (d) prova «manuale contro assistito» nella roadmap.
- **Il DGS non aveva:** il punto 9 del messaggio 9 e le decisioni D-24 … D-40. Da mandare con la prossima richiesta.

## 2026-11-19 · v1.69 (D-41: dossier sulla fonte P-001, prima parte)

- **Rete:** con l'approvazione del titolare, aggiunti `www.youtube.com` e `youtubei.googleapis.com` agli indirizzi permessi dell'ambiente. yt-dlp è autorizzato dal titolare per elenchi e sottotitoli.
- **Elenchi completi** dei tre canali (2.446 elementi, solo metadati) in `laboratorio/ipotesi/fonti/p001/`.
- **Sottotitoli bloccati dal controllo anti-bot di YouTube** sulle richieste dal cloud: non aggirato. Proposto un comando da lanciare sul Mac.
- **`laboratorio/ipotesi/DOSSIER-FONTE-P001.md`:** canali, percorso dichiarato e incoerenze, conteggio delle 111 operazioni dichiarate di Brad Trades (perdite mostrate nel 29–34% dei casi, dimensioni cresciute di circa 10 volte, importi solo in dollari), modello di business e incentivi, stile del canale, metodo (concetti ICT/SMC), che cosa la fonte può dare e che cosa no.
- **Nessuna scheda e nessuna prova.**

## 2026-11-19 · v1.70 (decisioni D-42 … D-44; #119 corretto; linee guida della prova di utilità)

- **Decisioni del titolare sul riscontro a DGS-11:**
  - (a) **D-42:** obiettivo +0,25 R con potenza 50%, metro invariato;
  - (b) **D-43:** clausola sulle code come esposizione verificabile in R; modifica il punto 3 di D-34;
  - (c) **D-44:** delegata a Claude, intervalli sotto 1e-9 R invalidi;
  - (d) il titolare chiede prima le linee guida: `piano/LINEE-GUIDA-PROVA-UTILITA.md`.
- **#119 corretto** nel modulo del verdetto, in TDD. Mutanti VD01–VD48: **47/48 su 3.13 e 3.9**, VD13 equivalente dichiarato.
- **Errore mio nello script dei mutanti:** VD05 non trovava più il testo dopo la modifica della riga. Corretto e ucciso.

## 2026-11-19 · v1.71 (messaggio 10 al DGS; correzione di un conteggio)

- **Messaggio 10 al DGS** (`direttore-sicurezza/13-MESSAGGIO-10-RISERVA-DECISIONI-VERDETTO.md`). Contiene:
  - la capienza della riserva, cioè il punto 9 non arrivato;
  - le decisioni D-24 … D-45;
  - la specifica del modulo del verdetto;
  - la proposta che i **casi a risposta esatta** della prova generale a vuoto li scriva il DGS, che non ha scritto l'esecutore (DGS-11 §7).
- **Correzione di un mio errore di conteggio.** In v1.67 e in chat avevo scritto «32 test» per il modulo del verdetto. Erano 30 allora e sono **31** oggi, con il test di #119.

## 2026-11-19 · v1.72 (copia di sicurezza della chat)

- Su richiesta del titolare, Claude ha consegnato **due copie della chat** (12/11 → 19/11/2026, 22:35 UTC). Contengono dati personali, quindi stanno **fuori dal repository**: il titolare le custodisce nel suo cloud.
  - **Copia leggibile:** 566 messaggi del titolare, 1.007 risposte di Claude e 2 riassunti automatici. SHA-256 `b0b6226f…5837`.
  - **Copia completa grezza** (`.jsonl.gz`, 49 MB). SHA-256 `d07fef9a…ee`.
- Le decisioni, i registri e i documenti restano comunque su GitHub, a ogni passo.

## 2026-11-20 · v1.73 (visione multi-mercato e ricerca di fonti)

- **`laboratorio/ipotesi/fonti/RICERCA-FONTI-20261120.md`:** ricerca di fonti oltre P-001 (accademiche, campioni certificati, test indipendenti), valutate con i criteri del dossier. **Nessuna idea registrata:** la scelta è del titolare.
  - Una prova contraria pertinente: il test meccanico indipendente del «Silver Bullet» ICT, anche su GC (oro), è negativo.
  - Il fixing di Londra cambia regime nel 2015, dentro la riserva.
- **`piano/VISIONE-FABBRICA-MULTIMERCATO.md`:** su richiesta del titolare, visione da «strategia singola» a «fabbrica di ricerca multi-mercato».
  - Le «circa 4 verifiche» valgono per la riserva di **un** mercato; ogni mercato ha la sua.
  - La demo in avanti è un campo di prova illimitato; lo storico fa da primo filtro.
  - Portafoglio di molti sistemi semplici.
  - **La definizione di fatto (D-34) NON si allarga:** il motore generico è una fase successiva.
- **Controllo di progetto (ricerca nel codice), primo esito:**
  - neutri rispetto al mercato: `verdetto_d31.py`, `riserva.py`, `sigillo.py`;
  - **`caricatore.py` non è neutro:** il controllo di qualità usa una sessione di Londra fissa (8:00–16:45) e importa una funzione dal simulatore di Londra. Da rendere parametro alla fase del secondo mercato; non si tocca ora (perimetro sigillato, corretto per l'oro).
- **Errore mio corretto prima di pubblicare:** nella prima stesura della visione avevo scritto che i pezzi erano «già quasi tutti neutri» senza averlo verificato. La ricerca nel codice ha trovato l'eccezione del caricatore; il documento è stato corretto.

## 2026-11-20 · v1.74 (correzione della visione: il costo della prova in avanti è il tempo)

- **Su domanda del titolare («in che senso?»), Claude corregge una propria esagerazione** nella visione multi-mercato. Aveva scritto che la demo in avanti è «un campo di prova illimitato».
  - È **pulita** e **non si consuma**, ma arriva un giorno alla volta: il suo costo è il **tempo**.
  - Stime con il test di Wald e 15–20 trade al mese: circa 5–7 mesi per un vantaggio di circa +0,30 R; 1,5–2 anni o più per circa +0,10 R.
  - Il vantaggio è il **parallelismo**.
- **Aggiunta la distinzione fra:**
  - **prova in avanti simulata:** automatica, sui dati nuovi di ogni giorno, senza conto né ordini, per molte strategie;
  - **demo con ordini sul broker:** solo per le migliori, per la fedeltà d'esecuzione (DA-29).
- **Le prove in avanti si contano in N** come le altre.

## 2026-11-20 · v1.75 (D-34 punto 2: registro unico di N nel verdetto)

- **Accertato.** Il percorso della verifica sigillata usa già il solo registro canonico `registro_prove.json` (sigillo ed esecutore). Il DSR di `criteri.verifica` riceve N come argomento. I registri di Binario B sono usati solo da `DSRCalculator` quando viene istanziato, cosa che la verifica non fa: sono inerti.
- **Modulo del verdetto, in TDD** (test rossi `c5ee654`, poi il codice):
  - `contesto_prove(registro)` legge N dal registro canonico, con l'impronta SHA-256 del file letto;
  - rifiuta i registri ereditati di Binario B, un registro assente o malformato, e un registro cambiato durante la lettura;
  - `verdetto` riporta `contesto_prove` e `quota`, e **rifiuta ogni quota diversa dal 2,5%** (D-31: un'altra richiede un collaudo);
  - test statico: né il verdetto né il perimetro di esecuzione leggono `trial_registry` o istanziano `DSRCalculator`.
- **Verifica:** 38 test verdi su 3.13 e 3.9; mutanti VD01–VD57 **56/57 su 3.13 e 3.9**, VD13 equivalente dichiarato.
  - Durante la scelta dei mutanti ho aggiunto un caso di test (una sottoclasse di float) per VD55: dichiarato.
- **DA-28:** i registri di Binario B sono dichiarati eredità; resta aperta la ratifica di N unico su tutti i mercati (D-46).
- **Domanda aggiunta al messaggio 10 per il DGS** (punto 5): il ruolo di N nel verdetto di H-003, dopo che D-37 ha tolto il DSR dai requisiti.

## 2026-11-20 · v1.76 (D-34 punto 4: rapporto del verdetto tipizzato)

- **Modulo del verdetto, in TDD** (test rossi `9f6f4c5`, poi il codice).
  - `voci_rapporto(v)` dà ogni numero con **tipo** (MISURA, DERIVATO, STIMA, IPOTESI, REGOLA), **incertezza** e **fonte**:
    - sedute, trade e sedute con trade: MISURA;
    - media del campione: DERIVATO, esatto sul campione;
    - N dal registro: MISURA, con l'impronta;
    - soglie e quota: REGOLA (D-31, D-38);
    - vantaggio della strategia: **STIMA** con l'intervallo e il metodo, oppure **NON STIMABILE**.
  - **Misure, derivati e regole prima della stima** (MODELLO-EPISTEMICO §4).
  - `rapporto(v)` dà il testo, chiuso da «Esito della regola, non una raccomandazione a operare: la decisione resta del titolare (D-14)».
- **Risolve, per il verdetto, il rilievo I2 dell'audit:** un «R medio» stampato come fatto, mentre è una stima.
- **Verifica:** 45 test verdi su 3.13 e 3.9; mutanti VD01–VD69 **68/69 su 3.13 e 3.9**, VD13 equivalente.
  - Un test aggiunto per il mutante VD68 (riga dei casi a filo nel testo): dichiarato.
- **Resta da fare:** i rapporti dello screening e degli altri strumenti; il collegamento all'esecutore.

## 2026-11-20 · v1.77 (D-34 punto 3: clausola sulle code nel modello H-003)

- **`MODELLO-SCHEDA-H-003.md` §5:** applicata la clausola **«Esposizione alle code»** (D-43). La scheda dichiara prima del sigillo:
  - la distanza di stop prevista;
  - il salto di prezzo peggiore plausibile, con fonte;
  - l'esposizione massima per trade in R.

  Uno stop non è un tetto garantito.
- **Confronto con il dominio del collaudo:** perdite rare di circa −12,3 R con probabilità 1% (celle 11 e 12 del pilota). Fuori dal dominio serve un collaudo mirato.
- **Testata del modello aggiornata:** D-35, D-36, D-37 e D-42 sono decise. Il loro testo si integra dopo la risposta del DGS al messaggio 10, per non scrivere due volte le stesse clausole.
- **Nota di Claude:** anche le celle 11 e 12 del collaudo usano una distribuzione a **due soli valori**, come il generatore G1 dell'esempio avverso. Con q = 1% la probabilità di un campione senza perdite rare è trascurabile (0,99^1000 ≈ 4·10⁻⁵), quindi l'artefatto di #119 non tocca il collaudo. È già noto come fonte dei casi a filo (#116).

## 2026-11-20 · v1.78 (test automatici su GitHub; #120; rapporto tipizzato dello screening)

- **Test automatici su GitHub**, approvati dal titolare (`.github/workflows/test.yml`):
  - a ogni push e pull request, tutte le suite di test, su Python 3.13 e 3.9, con la rete bloccata;
  - lo script `.github/scripts/esegui_test.py` **trova da solo** tutti i file `test_*.py` (fuori da `collaborazione/`) e li esegue uno per processo, più la suite del Guardian. Un test nuovo non può restare fuori;
  - i mutanti veloci (verdetto D-31, controllo della cache e costi) si lanciano a mano («Run workflow»).
- **Prima corsa locale dello script:** ha trovato il **difetto #120** (`costi_tick.py` usava `.replace(tzinfo=…)`, vietato dal controllo anti-frode). Corretto. Dopo la correzione: **25 suite verdi su 3.13 e 3.9**.
- **Gli script dei mutanti del verdetto** ora escono con 0 quando gli unici vivi sono gli equivalenti dichiarati («atteso EQUIVALENTE» nel nome), che restano stampati.
- **Rapporto tipizzato dello screening** (D-34 punto 4, test rossi `f67a7b2`):
  - `voci_screening` e `rapporto_screening`: media sullo sviluppo come DERIVATO con l'avvertenza «gonfiata dalla selezione fra varianti»; soglie D-36 come REGOLA; potenza e intervallo come STIMA;
  - lo screening ora riporta anche la potenza stimata;
  - la riga finale dice che lo screening non è una prova.
- **Mutanti VD01–VD77: 76/77 su 3.13 e 3.9**, VD13 equivalente.
- **Errore mio corretto:** la riga di formattazione era copiata due volte, e il mutante VD67 non era più univoco. Ora c'è una funzione comune `_riga`.
- **Da verificare:** subito dopo il primo push GitHub non mostrava esecuzioni. Forse le Actions vanno abilitate nelle impostazioni del repository.

## 2026-11-20 · v1.79 (test automatici verdi; lettura di P-001, notte)

- **GitHub Actions:**
  - prima corsa: il 3.9 non c'è più su Ubuntu 26.04 (`ubuntu-latest`). Ora il 3.9 gira su `ubuntu-24.04`;
  - **corse n. 3 e 4 verdi su 3.13 e 3.9** (25 suite);
  - i push che toccano solo file `.md` non fanno partire i test, per non consumare i minuti gratuiti con modifiche ai documenti.
- **P-001 (D-41), note di lettura** (`laboratorio/ipotesi/fonti/p001/NOTE-LETTURA-CLAUDE.md`):
  - ep. 7 (zone; **due definizioni diverse di «mitigazione»**: 50% della zona oppure primo contatto);
  - ep. 12 (killzone; la **«Asia sweep»**, che coincide con la bozza B di Claude: provenienza condivisa);
  - ep. 13 (liquidità; l'affermazione «ogni movimento è preceduto da una sweep» **non è falsificabile** così come è detta; pista accademica sugli stop ai numeri tondi, da verificare);
  - ep. 27 (metodo di revisione: numeri troppo piccoli, rischio di sovradattamento);
  - ep. 31 (prop firm: limiti compatibili con le nostre regole).
- **Rischio dichiarato dal vivo:** 6 operazioni in R; il rischio cresce di 20–50 volte in 20 mesi; violazioni ammesse della regola dell'1%; uscite decise dalla paura.
- **Misura della selezione:** 7 perdite citate a voce su 9 hanno un video. **Il canale non nasconde sistematicamente le perdite che lui nomina**; lacuna nel giugno 2025.
- **Compito di Gemini aggiornato:** campi per la dimensione, l'uscita manuale e le operazioni multiple; segnalazione delle 12 trascrizioni tradotte.

## 2026-11-20 · v1.80 (R17 integrato: contatore 2 su 2; mandato R18 pronto)

- **R17 di Gemini integrato:** `collaborazione/da-gemini/G-20261118-R17.md` e i due script, dal ramo `rev/gemini-r17` (`1b67ecf`).
- **Verifiche di Claude:**
  - perimetro identico a `e476a9a`, anche alla punta attuale del ramo;
  - lo script dei mutanti alla versione `02c51c6` contiene esattamente 301 mutanti, coperti dai blocchi di Gemini senza sovrapposizioni;
  - M-R17-02 e M-R17-03 = #117 (già corretto);
  - R17-03: riprodotto il bordo (a).
- **D-24:** nessun difetto critico o importante, nessun caso dubbio. **R17 è il secondo giro pulito consecutivo: contatore 2 su 2** sul candidato `e476a9a` (`H-002-REVISIONI.md`).
- **Nuovo difetto #121** (minore, fuori dal perimetro, da correggere a lotti): tre bordi su input anomali in `protocollo_ia02`.
- **Mandato R18 pronto** (`collaborazione/da-claude/PROMPT-R18-GEMINI.md`). Contiene:
  - il giro su **tutte** le manomissioni, a qualunque costo, richiesto da D-24 prima della verifica;
  - il **primo giro di revisione del modulo del verdetto** (D-34: due giri propri);
  - le opzioni sulla protezione del ramo, da decidere dal titolare.

  Priorità consigliata: R18 prima del compito su P-001.

## 2026-11-21 · v1.81 (messaggio 10 aggiornato; regola sui modelli; stato dell'ASK)

- **Messaggio 10 al DGS:** in testa al contesto c'è l'aggiornamento del 21/11 (R17 pulito e contatore 2 su 2, R18 in corso, D-34 punti 1–4 fatti, test su GitHub). Si manda oggi.
- **Regola del titolare:** a ogni compito Claude indica quale modello usare (Claude Code, ChatGPT, Gemini), per non sprecare token (`CONTINUITA.md`, sezione del 21/11).
- **ASK:**
  - il disco del Mac si è riempito per la seconda volta (21/11, 01:26, fermo al 08/04/2017);
  - nessun dato perso (scrittura atomica);
  - lo scaricamento è ripartito in ciclo ed era al 15/11/2019;
  - la cache ASK pesa 81 MB, quindi lo spazio basta;
  - la causa del pieno è transitoria e non accertata.
- **Correzione (errore di Claude):** il messaggio 10 era già stato incollato al DGS il 19/11 sera e aspetta risposta; non si rimanda. Claude aveva dimenticato l'invio, segnalato dal titolare. Al DGS va solo un sollecito con l'aggiornamento breve.
- **Controllo del contesto del DGS** (`collaborazione/da-claude/direttore-sicurezza/14-CONTROLLO-CONTESTO-DGS.md`):
  - prima della risposta al messaggio 10, il DGS dichiara che cosa vede ancora e risponde a 11 domande di controllo con etichetta [VISIBILE]/[RICORDO]/[NON SO];
  - la chiave di correzione resta a Claude;
  - la regola per decidere se proseguire o ripartire con un pacchetto nuovo è proposta, e la decide il titolare.

## 2026-11-21 · v1.82 (DGS-12: prova generale sui casi del DGS; #122–#124; modello H-003 riallineato)

- **DGS-12 archiviato** (`collaborazione/da-chatgpt/DGS-20261121-12-riserva-e-verdetto.md`).
  - Controllo del contesto: 11 su 11, allegati del messaggio 10 visibili.
  - Tutti i numeri ricalcolati da Claude e confermati.
- **Prova generale a vuoto (D-34 punto 5) sui 15 casi del DGS** (`laboratorio/tests/test_prova_generale_dgs12.py`, test scritti prima):
  - M e N coincidono esattamente con il riferimento indipendente del DGS: stesso flusso di indici, L e U uguali alla quinta cifra;
  - A e B sul simulatore: +0,40 R e −2,50 R (stop scavalcato).
- **Difetti trovati dalla prova e corretti:** #122 (veto per blocchi con esiti ignoti, importante per il modulo) e #123 (segnale del metro, ruoli dei requisiti e rapporto). **#124 aperto:** `sum()` fra 3.9 e 3.12+.
- **Verifiche:** 73 test verdi su 3.13 e 3.9; mutanti del verdetto 93/94 su entrambe (VD13 equivalente), con 17 mutanti nuovi (VD78–VD94); la suite di mutanti ora comprende anche la prova generale.
- **D-44 sul collaudo, confronto appaiato:** cambia 1 intervallo su 180.000 (fase 2, cella 11, replica 1.904, da falsa promozione a errore). Il conteggio avverso e il verdetto del collaudo non cambiano.
- **Modello di scheda H-003:** §5 con le precisazioni di DGS-12 su D-43; §8 riallineato a D-31, D-35, D-36, D-37, D-42 (la versione del 15/11 era superata); controlli del §12 aggiornati.
- **Nuova decisione aperta DA-34:** uguaglianza della potenza al 50% nello screening. Consiglio di Claude: (a).
- **Messaggio 11 al DGS:** `collaborazione/da-claude/RISCONTRO-DGS-12.md`.

## 2026-11-21 · v1.83 (ricognizione su storici MetaTrader e strumenti per Claude)

- **Richiesta del DGS archiviata:** `collaborazione/da-chatgpt/DGS-20261121-richiesta-ricerca-metatrader-claude.md`.
- **Risposta di Claude:** `collaborazione/da-claude/RISPOSTA-RICERCA-METATRADER-20261121.md`.
  - **Verdetto:** oggi bastano gli strumenti esistenti.
  - **Tre prove piccole, con soglia di abbandono, dopo la fine della macchina:** spazio e seconda copia; osservatore programmato; coorte MQL5.
- **Limite:**
  - le pagine ufficiali di metatrader5.com e mql5.com non sono leggibili dall'ambiente di Claude;
  - gli indirizzi sono stati aggiunti all'ambiente, ma la lettura è stata negata dal controllo dei permessi;
  - le parti relative sono marcate «NON VERIFICATO»;
  - azione proposta: il titolare passa le pagine in PDF.

## 2026-11-21 · v1.84 (pagina per gli amici; correzione sulla riserva multimercato)

- **Pagina «Trading Brain in breve» aggiornata**, con lo stesso link: la visione multimercato (mappa dei mercati, catena della fabbrica, storia e futuro, due percorsi nella roadmap) e lo stato al 21/11.
- **Correzione (errore di Claude):**
  - la pagina e `piano/VISIONE-FABBRICA-MULTIMERCATO.md` dicevano «circa 4 verifiche per ogni mercato»;
  - la regola in vigore invece consuma la riserva per calendario, comune a tutti i mercati (confermato da DGS-12 §1);
  - le verifiche sono quindi circa 4 in tutto il progetto, salvo una decisione diversa del titolare;
  - corretti la pagina e il documento di visione.

## 2026-11-21 · v1.85 (R18 integrato e verificato: non pulito; #125–#135)

- **R18 di Gemini integrato** (`collaborazione/da-gemini/G-20261121-R18.md` e due script; solo la cartella di Gemini).
- **Verifica di Claude:**
  - R18-01 riprodotto (copia parziale senza blob);
  - R18-02 e R18-03 confermati sul codice;
  - R18-07, R18-08 e R18-09 riprodotti sul modulo del verdetto;
  - R18-11 confermato.
- **Registrati da #125 a #135.** Importanti nel perimetro: **#125, #126, #127**. Importanti fuori dal perimetro: #131, #132, #133 (modulo del verdetto) e #135 (CI).
- **D-24: R18 non è pulito.**
  - Servono le correzioni, un nuovo candidato e un nuovo giro sulle manomissioni.
  - Il trattamento del contatore (oggi 2 su 2 su `e476a9a`) è una decisione del titolare.
- **Disco pieno di notte:** non è Gemini (picco di 5,23 MiB) né lo scaricamento. Sospetto: gli snapshot locali di Time Machine o un aggiornamento di macOS.

## 2026-11-21 · v1.86 (correzioni di R18; nuovo candidato in preparazione)

- **Test scritti prima** (`e72af87`, rossi sul codice di allora), **poi il codice** (`f338381`):
  - **#125:** `versioni_nella_storia` rifiuta la copia parziale (`remote.*.promisor`, `extensions.partialclone`) e ogni versione presente ma illeggibile; un commit in cui il file è stato cancellato si salta come prima;
  - **#126:** `caricatore.carica` rifiuta BID e ASK nella stessa cartella, cartelle o file collegati simbolicamente e ogni giorno in cui tutti i minuti dell'ASK coincidono con il BID. Le fixture dei test esistenti, che usavano ASK identico al BID per comodità, sono state adattate;
  - **#128:** la quota `alfa_j` deve essere un float finito;
  - **#131–#134**, nel modulo del verdetto:
    - intervallo invalido non presentato come stima;
    - seme intero obbligatorio;
    - contesto di N controllato e obbligatorio per promuovere;
    - registro collegato rifiutato;
    - coppie solo in lista e somme finite;
    - banda dei «vicini» con il tipo;
  - **#135:** `esegui_test.py` richiede almeno un test eseguito e non tutti saltati, e confronta le suite trovate con `.github/scripts/suite_attese.txt` (27 suite).
- **Verifiche:**
  - 27/27 suite verdi su 3.13 e 3.9;
  - mutanti del verdetto **117/118** su entrambe (VD13 equivalente), con 24 mutanti nuovi (VD95–VD118, compresi i 5 sopravvissuti di Gemini);
  - mutanti nuovi del perimetro **Q01–Q11: 11/11** su entrambe.
  - La corsa completa di `mutazioni_esecuzione` è da fare (R19 e Claude).
- **Aperti:**
  - **#127**: collegamento fra esecutore e riserva. La verifica di H-002 usa oggi tutta la riserva, quindi serve una scelta di progetto;
  - #129 e #130: limiti dichiarati;
  - #124 e #121: minori, a lotti.
- **Decisioni del titolare:** DA-34 (potenza al 50%), DA-35 (contatore D-24 dopo R18), DA-36 (protezione del ramo).

## 2026-11-21 · v1.87 (DGS-13: rettifica su D-44, ricevuta della prova generale, attribuzione di R18)

- **DGS-13 archiviato.** Numeri ricalcolati e confermati (limiti Beta al 99,9%: 1,1897%, 0,0935%, 0,1088%).
- **Rettifica accolta (errore di Claude):** nel confronto D-44 mancava il secondo conteggio avverso. Le false bocciature più gli errori della cella 11 passano da 2 a 3 (limite da 0,0935% a 0,1088%). Il verdetto del collaudo non cambia.
- **Ricevuta della prova generale:** `collaborazione/da-claude/RICEVUTA-PROVA-GENERALE-20261121.md`.
  - Contiene commit, impronte, 17/17 test su 3.13 e 3.9 e i rapporti di M e N.
  - **D-34 punto 5 resta aperto per il percorso intero** (scheda → sigillo → screening → prenotazione → verdetto → rapporto), che non esiste finché non si corregge #127.
- **#123:** la parte (b) è riclassificata importante per il modulo, su proposta del DGS.
- **Modello di scheda H-003:** metodo di DGS-13 §B per la potenza con i veti.
- **Messaggio 12 al DGS:** `collaborazione/da-claude/RISCONTRO-DGS-13.md`.

## 2026-11-21 · v1.88 (corsa completa dei mutanti del perimetro dopo R18: #136)

- **Corsa completa dei mutanti dell'esecuzione** su 3.13: 311/314 prima della correzione.
  - C01 e C08 erano vivi perché due test del caricatore erano diventati ciechi dopo #126.
  - V10 non si applicava più dopo #128.
- **#136 (errore di Claude):** i test ora controllano il messaggio d'errore e V10 è riallineato. Solo test e script dei mutanti; il codice del perimetro non cambia.
- **Regola di lavoro:** dopo ogni correzione del perimetro si riesegue la corsa completa dei mutanti, non solo quelli nuovi.
- **Esito dopo la correzione:** 314/314 mutanti uccisi su 3.13.18 e 314/314 su 3.9.25. Su 3.9 la corsa è stata divisa in due parti (169 + 145) per il limite di due ore; nessun equivalente dichiarato.

## 2026-11-22 · v1.89 (decisioni del titolare su DA-34, DA-35, DA-36)

- **D-47 (DA-34 a):** nello screening la potenza deve essere ≥ 50%; il 50% esatto passa. Il codice non cambia.
- **D-48 (DA-35 c):** contatore D-24 a 1 su 2. R19 sul nuovo candidato è un giro ordinario completo più le manomissioni.
- **D-49 (DA-36):** opzione 2 più le etichette protette della 3; il titolare conserva lo scavalcamento. Da applicare dopo aver verificato chi può approvare in un repository personale.
- DGS-13 ricaricato dal titolare il 22/11: identico a quello archiviato il 21/11 (confronto byte per byte), nessuna nuova risposta.

## 2026-11-22 · v1.90 (fine dell'ASK; messaggio 13 al DGS; mandato notturno a Gemini)

- **Scaricamento ASK finito** il 21/11 alle 23:50: «FINITO ASK 2005-01-01 → 2023-11-11: in cache 5.337, scaricati 1.552, 404 0, vuoti 0, HTTP 0, rovinati 0» (riga del log letta dal titolare). Il consuntivo (controllo della cache, intersezione BID/ASK, buchi per anno: soli conteggi e date) gira sul Mac.
- **Messaggio 13 al DGS** (`collaborazione/da-claude/MESSAGGIO-13-DGS.md`): decisioni D-47–D-49, #136, fine dell'ASK e progetto di #127 per la sua critica prima dei test (prenotazione → controllo della quota → autorizzazione con l'impronta presa dal registro dello scaricamento → verdetto D-31 → rendiconto).
- **Mandato notturno a Gemini** (`MANDATO-NOTTE-20261122-GEMINI.txt`): #124 con un riferimento in aritmetica esatta; ricerca su come applicare D-49 in un repository personale; P-001 solo se avanza tempo.

## 2026-11-22 · v1.91 (DGS-14: riscontro alla prova generale e parere sul progetto di #127)

- **DGS-14 archiviato** (`collaborazione/da-chatgpt/DGS-20261122-14-riscontro-e-progetto-127.md`). Numeri ricalcolati da Claude e confermati: potenze 24,35%, 12,94%, 8,48%, 6,15%; errori standard massimi 0,02551, 0,02089, 0,01895, 0,01781 R; 4.912 feriali dal 01/01/2005 al 31/10/2023.
- **La ricevuta della prova generale non è arrivata al DGS** (non era fra gli allegati): andrà allegata al prossimo messaggio.
- **D-34 punto 5 resta aperto**, come atteso: si chiude con la prova sintetica del percorso intero dopo #127.
- **Progetto di #127, accolto con queste precisazioni:**
  - **Q1:** l'impronta dal registro dello scaricamento è accettata come impegno ai byte attesi. Va costruita sull'insieme atteso (mercato, lato, data, comprese le date accessorie) e confrontata con il registro, così che emergano anche voci mancanti, doppie o sul lato sbagliato. Va congelata nell'autorizzazione, insieme a scheda, codice, finestra, N e quota. Alla lettura si controllano i byte effettivamente decodificati; un file difforme dopo l'autorizzazione dà un esito tecnico registrato e il consumo resta.
  - **Q2:** il DGS raccomanda un evento «rifiutata per quota» nel registro della riserva. Va al titolare come **DA-37**.
  - **Q3:** H-002 si usa solo come oggetto sintetico, confezionato in una scheda conforme al modello H-003 e senza deroghe nel percorso. Una prenotazione vera richiede una scheda H-003 sigillata; la vecchia scheda H-002 si rifiuta prima dell'autorizzazione.
  - **Q4:** criteri per scegliere la finestra (calendario utilizzabile, potenza ottenibile, capienza residua, pertinenza e regola di spareggio). Si presentano al titolare con il consuntivo, una riga per finestra candidata.
  - **Criterio di accettazione:** una prova sintetica collega tutti i passaggi con l'identità di scheda e candidato. Tre casi capaci di invertire il giudizio: quota non collaudata (zero aperture del caricatore), file difforme dopo l'autorizzazione, ripresa dopo il verdetto registrato e prima del rapporto.
- **#136, rifinito su indicazione del DGS:** i test del periodo ora partono da un caso valido (cartelle distinte, ASK ≠ BID, sigillo) e cambiano solo il periodo; ogni rifiuto ha il suo controllo positivo.
- **Modello di scheda H-003:** controllo «promossa ⇒ segnale favorevole» replica per replica, e riferimento di potenza di DGS-14.
- **Da segnalare al titolare:** con D = 1.000 sedute, un trade per seduta e σ = 1,25 R, il metro ha solo il 24% di potenza alla prima apertura. Per lo screening D-36 (potenza ≥ 50%) servono circa 2.400 trade, oppure una dispersione ≤ 0,81 R.

## 2026-11-22 · v1.92 (consegna notturna di Gemini; #124 corretto nel modulo del verdetto)

- **Consegna di Gemini** (`rev/gemini-notte22`, `6fb7949`, base `128e8ba`) archiviata in `collaborazione/da-gemini/G-20261122-NOTTE.md` con lo script `notte22_somme_esatte.py`. Il compito C (P-001) non è stato eseguito: il mandato non era nella sua sessione.
- **#124, compito A:** 9 divergenze su 23 casi a filo di soglia, su Apple Python 3.9.6 (sul Mac non c'è Python ≥ 3.12).
  - **6 nel modulo del verdetto** (N22-A1), riprodotte da Claude su 3.9.25. **Corrette** con `math.fsum` nelle medie di verdetto, screening e blocchi; test rossi in `eb411c2`, poi il codice. Mutanti VD119–VD125.
  - **3 nel pilota congelato** (N22-A2): non si tocca. L vicino a 0 nello screening ora si segnala nel rapporto, come già L e U vicini alle soglie.
- **D-49, compito B:**
  - **[VERIFICATO da Gemini]** Su GitHub Free un repository privato personale non ha né rulesets, né protezione dei rami, né CODEOWNERS: serve GitHub Pro.
  - L'autore di una richiesta di unione non può approvarla da solo. Gemini propone tre alternative: un secondo account per gli agenti; approvazioni a 0 con richiesta di unione e test obbligatori; approvazione a 1 con scavalcamento.
  - **Limite nuovo:** gli agenti che usano le credenziali del titolare ne ereditano lo scavalcamento.
  - Istruzioni clic per clic nel rapporto.
- **Verifica dopo la correzione di #124:**
  - suite completa verde su 3.13.18 e 3.9.25; mutanti del caricatore C01–C09 9/9 su entrambe, con i test del periodo riscritti da casi validi;
  - la prima corsa dei mutanti del verdetto ha dato 121/125: VD26, VD35 e VD72 non si applicavano più, perché la correzione aveva cambiato le loro righe (stessa classe di errore di V10 in #136, errore di Claude). Riallineati, 3/3 su entrambe;
  - **totale: 124/125 su 3.13.18 e su 3.9.25, con VD13 equivalente dichiarato.**

## 2026-11-22 · v1.93 (D-50; messaggio 14 al DGS; secondo mandato a Gemini)

- **D-50 (DA-37 i):** il rifiuto per quota non collaudata diventa un evento del registro della riserva (schema `riserva/2`), da scrivere nel nuovo candidato.
- **Messaggio 14 al DGS** (`collaborazione/da-claude/MESSAGGIO-14-DGS.md`), con la ricevuta della prova generale e il rapporto notturno di Gemini allegati. Su richiesta del titolare, il DGS deve usare lo strumento di esecuzione del codice per ricalcolare i numeri. Domande:
  - #124: congelare una versione di Python nella verifica?
  - D-49: confronto metodologico delle alternative A, B e C;
  - schema `riserva/2`: dopo un rifiuto la prenotazione si chiude?
  - ricalcolo di S1, B1, B3, della tabella di potenza e dei limiti Beta.
- **Secondo mandato a Gemini** (`MANDATO-GEMINI-20261122-B.txt`): verifica indipendente della correzione di #124 e mutanti del verdetto su 3.9; prova P-001 sui 10 video, con il mandato riportato intero, perché nella notte non era nella sua sessione.
- Il messaggio di Gemini inoltrato dal titolare è lo stesso già archiviato (`6fb7949`): niente di nuovo da registrare.

## 2026-11-22 · v1.94 (DGS-15: percorso ordinario di verifica, #127, ricevute)

- **DGS-15 archiviato** (`collaborazione/da-chatgpt/DGS-20261122-15-mandato-ricevuta-127.md`): mandato per la ricevuta di #127, in sei punti. Non risponde alle domande Q1–Q4 del messaggio 14.
- **Punto 1, attribuzione** (`laboratorio/ricevute/2026-11-22-attribuzione/ATTRIBUZIONE.md`, con i log):
  - 17/17 attribuiti a `f5d0cad`; 314/314 a `6ce6388`, con le due parti su 3.9;
  - R18 diviso fra `efcfcbc` e le riesecuzioni;
  - dimostrazione di #136 su 3.13 e 3.9 e spiegazione di V10;
  - suite e mutanti del verdetto rifatti in una copia bloccata su `dfe0227`: verdi, 124/125.
- **Errore di Claude, corretto:** ho modificato `test_riserva.py` mentre la corsa di attribuzione leggeva la stessa cartella. La corsa non sarebbe stata attribuibile a un solo commit. L'ho fermata e rifatta in un worktree bloccato sul commit. **Regola:** le corse da attribuire si fanno sempre in una copia bloccata sul commit.
- **Codice nuovo (test prima, poi codice):**
  - schema `riserva/2` (D-50): rifiuto durevole, quota prevista, ricontrollo della quota sotto il blocco, impegno legato all'impronta, record del verdetto, `prenotazione()`;
  - `manifesto.py`: insieme atteso contro il registro dello scaricamento;
  - byte verificati nel caricatore (`FileDifforme`);
  - `esegui_verifica.py`, l'esecutore ordinario con la scheda H-003;
  - mercato sintetico per le prove;
  - mutanti del percorso (`mutazioni_percorso.py`, 40).
- **Ricevuta di #127** (`laboratorio/ricevute/2026-11-22-percorso-127/RICEVUTA-127.md`): prove A–G su 3.13 e 3.9 con esiti identici. Gli estremi L e U differiscono di 5,7e-15 R fra le versioni, per le somme del pilota congelato (N22-A2): è un caso concreto per Q1 del messaggio 14.
- **#127 in parte corretto.** Resta il vecchio esecutore di H-002 in verifica: **DA-38** al titolare, perché D-37 gli aveva lasciato i suoi criteri.

## 2026-11-22 · v1.95 (consegne di Gemini del mandato B; #124 seconda parte; seconda revisione di Claude)

- **Gemini, compito A** (`rev/gemini-verifica124`, `1855fde`, base `b0763c5`), archiviato in `collaborazione/da-gemini/G-20261122-VERIFICA124.md` con lo script:
  - la prima correzione di #124 regge per la dipendenza dalla versione;
  - **sei divergenze residue** contro le frazioni esatte (V124-01..06): tre cambiano una decisione a filo, una è descrittiva, una riguarda la banda di vicinanza e una la finitezza;
  - 4 mutanti nuovi sopravvissuti;
  - mutanti del verdetto 124/125 su Apple 3.9.6.
  - **Riprodotte da Claude e corrette** (test `3b5f4ea`, codice `85dd9b7`): decisioni in frazioni esatte, medie arrotondate una volta, finitezza sui valori assoluti. #124 è **riclassificato importante per il modulo**, perché può cambiare una decisione.
  - **Errore di Claude nel test di V124-06:** prima avevo scritto che la somma esatta di (1,5e308; 1,5e308; −1,5e308) non fosse finita, mentre lo è. La regola giusta per proteggere il pilota è la somma dei valori assoluti; ho corretto il test prima del codice.
- **Gemini, compito B** (`rev/gemini-p001`, `21399c6`), archiviato in `collaborazione/da-gemini/P001-CATALOGO-GEMINI.md`. Catalogo pilota di 10 video, 11 operazioni, lavorato solo sulle trascrizioni:
  - ingresso, stop e dimensione leggibili in 0 casi su 11;
  - 9 motivazioni su 11 dette prima dell'esito;
  - incoerenze fra titoli e cifre, e lo stop allargato a mano in 3 video su 6;
  - recuperati 9 sottotitoli mancanti su 11.
  Gemini si è fermato come da mandato: **il via per gli altri 101 video spetta al titolare** (D-33, D-41).
- **Seconda revisione di Claude** del percorso nuovo:
  - #137, la variante non dichiarata nel sigillo, ora rifiutata prima di ogni lettura;
  - il manifesto legge il registro dello scaricamento una volta sola;
  - test aggiunti per i mutanti vivi PR08, EV03 ed EV08; MF09 dichiarato equivalente.
- **Corse finali su `d866e4b`:** suite verdi su 3.13.18 e 3.9.25. Il modulo del verdetto è cambiato dopo (`85dd9b7`), quindi le corse di attribuzione si rifanno sul candidato nuovo.

## 2026-11-22 · v1.96 (candidato finale di #127; controllo di applicabilità dei mutanti; messaggio 15)

- **Decisioni del titolare:** D-51 (DA-38 a: disattivare la verifica di `esegui_h002`, da applicare con i test prima); D-52 (P-001 in pausa, «prima la macchina»). Il titolare ha il **piano GitHub Free**, quindi D-49 non si può applicare: **DA-39** è aperta.
- **Errore ripetuto di Claude (terza volta):** dopo #124 seconda parte, VD30, VD39 e VD111 non si applicavano più e VD44 era vivo. **Contromisura strutturale:** il test `test_mutanti_applicabili`, nella suite, controlla che ogni mutante dei tre script si applichi una volta sola. Ha trovato subito anche V07, V17 e V18, rotti da `riserva/2`. Tutti riallineati, con un test nuovo per VD44, in `db3c85f`.
- **Candidato finale `aca694f`**, worktree bloccato, 3.13.18 e 3.9.25:
  - suite verdi;
  - prove A–G identiche;
  - mutanti del percorso 40/41 (MF09 equivalente);
  - mutanti del verdetto 131/132 (VD13 equivalente);
  - controlli del punto 5 identici.
- **Da fare:** la corsa completa di `mutazioni_esecuzione.py` sul candidato nuovo, dopo D-51.
- **Messaggio 15 al DGS** completato (`collaborazione/da-claude/MESSAGGIO-15-DGS.md`).
- Engram, proposto da un conoscente del titolare come «memoria»: valutato da Claude. Sono strumenti di memoria per agenti, non protezioni del repository; sconsigliato per il progetto. Il titolare è d'accordo.

## 2026-11-22 · v1.97 (DGS-16: riscontro alla ricevuta di #127)

- **DGS-16 archiviato** (`collaborazione/da-chatgpt/DGS-20261122-16-riscontro-ricevuta-127.md`). Numeri ricalcolati da Claude e confermati:
  - limiti Beta 1,189728%, 0,093538%, 0,108806%;
  - riferimento normale 24,35% e 50,66%;
  - 0,5 − ulp(0,5) = 0,4999999999999999, mentre il vicino immediato è 0,49999999999999994.
- **I «40 feriali in più» sono spiegati:** dall'08/02/2010 al 31/01/2014 ci sono 1.040 feriali e 1.000 sedute. I 40 giorni esclusi sono le chiusure del calendario di H-002 (`orb_londra.esclusi`): festività inglesi, vigilie e 31 dicembre. L'elenco completo andrà nella ricevuta.
- **Pareri del DGS:**
  - Q1: fissare un ambiente di riferimento prima della verifica e usare l'altro come prova di portabilità;
  - Q2: rinviare Pro va bene durante il lavoro sintetico, con le prove sulle identità vere prima del primo accesso reale;
  - Q3: chiudere la prenotazione dopo un rifiuto per quota va bene, ma vanno esplicitate le transizioni di B e G (date ancora prenotate: correzione, ripresa, rilascio);
  - Q5: tenere la regola attuale sulla quarantena; l'alternativa va al titolare solo dopo una simulazione;
  - Q6: una prova logica dei veti e, separata, una stima con un generatore registrato prima;
  - Q7: con D-51 ogni protezione va provata sull'ingresso nuovo.
- **Richieste a Claude:**
  - legare i due JSON finali al commit e ai test;
  - per la corsa A, dire chi prepara sigillo, prenotazione e potenza;
  - elenco delle sedute fissato prima dell'apertura e coppie usate;
  - rapporto originale, record e rapporto rigenerato confrontabili, con i comandi;
  - verdetto e valori numerici separati fra le due versioni (anche in esadecimale);
  - allegare gli estratti Q2 e Q4 del messaggio 14;
  - per R19, la versione con D-51 e le protezioni provate sull'ingresso ordinario.

## 2026-11-22 · v1.98 (D-51 applicato, prima parte; DGS-16: sedute nell'impegno, ricevute)

- **D-51, prima parte** (test rosso `TestD51VerificaDisattivata`, poi il codice):
  - `esegui_h002 --modalita verifica` si ferma **subito**, prima di sigillo, registri, ambiente e caricatore: codice 2, messaggio che rimanda al percorso ordinario;
  - tolto il ramo di verifica ormai irraggiungibile, con la funzione `esegui_verifica` di `esegui_h002`, `_esiti_sviluppo` e la parte di verifica del rapporto;
  - le protezioni comuni restano sullo sviluppo: registro canonico, registro non committato, storia parziale, copia senza blob (per le ultime due la seconda versione del registro si crea con un sigillo invece che con una verifica); il rapporto viene scritto prima degli esiti, ora provato sullo sviluppo;
  - tolti 16 test e 15 mutanti propri della vecchia verifica; N38 e N42 riallineati. Mutanti del perimetro ora **299**;
  - suite su 3.13 e 3.9 verdi.
- **Ancora da fare per D-51** (`PIANO-D51.md` §3), con test scritti prima, nel percorso ordinario:
  - ancora e storia per il registro delle prove e quello della riserva (verifica già fatta su un altro ramo, reflog, N che non scende);
  - identità dei dati di sviluppo nello screening;
  - avvio isolato e lanciatore;
  - prove dirette sul registro delle prove.
  **Fino ad allora queste protezioni mancano nel percorso nuovo:** è dichiarato e serve prima di R19.
- **DGS-16:**
  - l'elenco delle 1.000 sedute è nell'impegno prima dell'autorizzazione; il record ha le coppie datate in ordine e i 40 feriali esclusi (test rossi in `abbdde2`);
  - provate le transizioni di G (ripresa della stessa prenotazione dopo la correzione) e di B (rilascio);
  - lo script della ricevuta produce record, rapporto originale e rapporto rigenerato confrontabili, i valori in esadecimale e la provenienza: sigillo e prenotazione li prepara il collaudo, la potenza è un valore dichiarato nel contratto;
  - prova logica dei veti: blocco debole in 4 posizioni, controllo omogeneo, 49, 50 e 51 trade; risultato atteso indipendente, in frazioni.

## 2026-11-23 · v1.99 (notte: DGS-16 completato; PIANO-D51 §3.1 e §3.2 nel percorso ordinario)

- **DGS-16, ricevute rieseguite su `4659dc8`** (worktree bloccato, 3.13.18 e 3.9.25), log `dgs16_*`:
  - rapporto originale uguale byte per byte a quello rigenerato dal record, su entrambe le versioni; il rapporto rigenerato nella ripresa F ha la stessa impronta;
  - impronta dell'impegno identica fra le versioni; media identica bit per bit; L e U diversi di 102 ulp;
  - prova logica dei veti uguale all'atteso indipendente in tutti gli 8 casi;
  - mutanti del percorso 42/43 su entrambe (MF09 equivalente).
- **PIANO-D51 §3.2** (test rossi, poi codice):
  - lo sviluppo si legge con il manifesto e i byte verificati contro il registro dello scaricamento;
  - l'impronta dello sviluppo è nell'impegno e nello screening registrato;
  - uno screening già registrato con un'altra impronta è rifiutato.
- **PIANO-D51 §3.1** (test rossi, poi codice):
  - registri canonici e ancorati a GitHub; storia completa;
  - prenotazione consumata in un'altra versione rifiutata; j e N che non scendono;
  - `ANCORA_GIT` acceso nel codice (con un test);
  - mutanti EV20–EV28.
- **`CONTINUITA.md`** aggiornata con lo stato e i passi mancanti.
