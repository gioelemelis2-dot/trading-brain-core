# Documento di continuità

Ultimo aggiornamento: **2026-11-19 sera** (sezione in testa); prima: 2026-11-15, dopo il mandato notturno su H-002 (programma dei criteri, strumento di sigillo, quaderno delle ipotesi; ramo `feat/esecutore-h002`, **non unito a main**). Leggere questo file per primo (vale anche per Gemini, insieme a `collaborazione/HANDOFF-GEMINI.md`).

## Aggiornamento del 19/11/2026, sera (LEGGERE PER PRIMO: sostituisce le sezioni più vecchie dove sono in contrasto)

**Priorità del titolare: prima la macchina, poi le strategie (D-33, D-34).**

**Ramo e stato:**
- Il ramo `feat/esecutore-h002` non è unito a `main` (`main` è indietro di oltre 140 file).
- Ultimo commit di questa sessione: vedi `git log`. Il registro delle modifiche arriva a v1.72; i difetti a #119.

**Contatore D-24 (sigillo):**
- **1 su 2.** R16 è pulito; **R17 di Gemini è in corso** sul candidato `e476a9a`, nel worktree `~/Downloads/tb-r17`, HEAD `02c51c6`, ramo `rev/gemini-r17`.
- Finora: suite 432 OK, collaudo IA-02 riprodotto, mutanti 165/165. Ne restano 136, poi Gemini consegna `G-20261118-R17.md`.
- Da fare alla consegna:
  - verificare che M-R17-02 e M-R17-03 coincidano con #117, già corretto;
  - se il giro è pulito, contatore a 2 su 2;
  - poi il giro su tutte le manomissioni (R18) e la decisione sulla protezione del ramo.

**Decisioni del 19/11** (`governance/DECISIONI.md`):
- **D-34 «definizione di fatto».** Elenco chiuso:
  1. criterio D-31 in un modulo nuovo (**fatto**: `laboratorio/verdetto/verdetto_d31.py`, 31 test, mutanti VD 47/48 su 3.13 e 3.9, VD13 equivalente);
  2. registro unico di N (**prossimo**);
  3. clausola sulle code, ora D-43: esposizione in R dichiarata e verificabile;
  4. tipi epistemici nei rapporti;
  5. prova generale a vuoto (i casi a risposta esatta li scrive il DGS, se accetta il messaggio 10);
  6. R17 più il giro sulle manomissioni;
  7. unione in `main` con la protezione del ramo.

  Il resto va a lotti e non riapre il contatore.
- **D-35** tre esiti; i «non decidibili» si riprovano solo in demo.
- **D-36** screening: media > +0,25 R, L > 0, potenza ≥ 50%.
- **D-37** verdetto solo dal metro; veto per blocchi; minimi 1.000 sedute, 300 trade, 200 sedute attive.
- **D-38** α 5%, nessuna parte protetta; date esatte dopo l'ASK.
- **D-39** due copie dei dati.
- **D-40** niente previsioni giornaliere.
- **D-42** obiettivo +0,25 R con potenza 50%.
- **D-43** clausola sulle code.
- **D-44** intervalli < 1e-9 R invalidi (#119).
- **D-41** dossier sulla fonte P-001, eccezione limitata a D-33.
- **D-45** esecuzione con alert, poi conferma con un tocco; l'automatico non è autorizzato.

**Aperte:**
- **DA-32:** ore in cui il titolare può eseguire gli alert, da comunicare entro circa 10 giorni.
- **Decisione (d):** prova «manuale contro assistito» (`piano/LINEE-GUIDA-PROVA-UTILITA.md`); consiglio d-2.

**Fatti da ricordare:**
- **La riserva basta per circa 4 verifiche in tutto il progetto** (consumo per calendario e per tutti i mercati). La potenza scende con le aperture successive.
- **Audit globale e controverifica:**
  - audit: `collaborazione/da-claude/AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`, con errata in testa;
  - controverifica del DGS: DGS-11;
  - riscontro di Claude: `collaborazione/da-claude/RISCONTRO-DGS-11.md`.
- **L'esempio avverso dell'11,7% era un artefatto** (riscontro §2).

**Messaggi:**
- **Messaggio 10 al DGS** preparato (`direttore-sicurezza/13-...`). Contiene la capienza della riserva, D-24…D-45, la specifica del verdetto e la richiesta dei casi a risposta esatta. **ChatGPT ha esaurito l'uso fino al 21/11/2026:** si manda da quel giorno. Fino ad allora, nessun lavoro che dipende dal DGS.

**Fonte P-001 (Brad Goh, D-41):**
- Dossier, prima parte: `laboratorio/ipotesi/DOSSIER-FONTE-P001.md`. Elenchi dei 3 canali in `laboratorio/ipotesi/fonti/p001/`.
- **Sottotitoli:**
  - dal cloud sono bloccati da YouTube (anti-bot), e non si aggira;
  - sul Mac il titolare li scarica con `~/Downloads/yt-dlp_macos` (2026.10.26) in `~/Downloads/p001_sottotitoli/`;
  - non vanno nel repository.
- **Compito per Gemini** (`collaborazione/da-claude/PROMPT-P001-GEMINI-TRASCRIZIONI.md`): da dare **dopo R17**, con una prova su 10 video. Aggiungere che le trascrizioni ci sono già.

**Bozze di idee di Claude (19/11 sera), NON registrate per scelta del titolare.** In chat Claude ha abbozzato, solo a parole, tre ipotesi:
- (A) compressione asiatica ed espansione a Londra (Crabel con H-002);
- (B) falsa rottura del range asiatico a Londra (Raschke «Turtle Soup» con la «sweep» di ICT/Brad);
- (C) momentum intraday da Londra a New York sull'oro (Gao e coll., 2018).

Il titolare ha deciso di **non registrarle ora**: prima Claude legge il materiale di Brad e l'analisi dei video di Gemini. Questa nota serve solo alla provenienza: le bozze sono **anteriori** alla lettura delle trascrizioni di Brad, e Claude conosceva già i titoli dei suoi video.

**Mac:**
- **Batteria guasta:** sempre collegato alla corrente. Assistenza dopo R17 e la copia finale dei dati (`piano/PROCEDURA-ASSISTENZA-MAC.md`).
- **Spazio su disco con cali improvvisi** (14 → 10 → 5,8 GB). Sospetto: memoria di scambio. Da controllare con `sysctl vm.swapusage`.
- **ASK:** scaricamento in ciclo (circa 60%, aprile 2016 il 19/11 sera), log `~/scarica_ask.log`. Alla fine: controllo, intersezione BID/ASK, buchi per anno, date esatte della riserva (D-38), copia finale con due copie (D-39).

**Ambiente cloud di Claude:**
- Aggiunti `www.youtube.com` e `youtubei.googleapis.com` agli indirizzi permessi.
- yt-dlp è autorizzato dal titolare solo per elenchi e sottotitoli di P-001.

**Da fare quando c'è tempo:**
- riconciliazione del G0 su demo MT4 (micro-operazioni con stop; la demo è MT4, le specifiche sono MT5);
- commissione FP Markets per lato o andata e ritorno.

**Copia della chat:** consegnata al titolare il 19/11, fuori dal repository (registro v1.72).

## Aggiornamento del 17/11/2026, notte (leggere prima della sezione seguente)
- **Riserva di verifica: intatta, RICONFERMATA il 17/11** con lo strumento di riconteggio corretto (`governance/censimento/RICONTEGGIO-20261117.md`).
- **Comando dell'esecutore cambiato (#95):** `python3 -I -S -B brain/laboratorio/esecuzione/avvio.py …` (controlli prima degli import). Prima di ogni esecuzione vera: niente cartelle `__pycache__` in `brain`.
- **Scaricamenti (17/11):** BID ripreso dal 12/02/2020 e ASK dal 2005, entrambi da `~/Downloads/tb-riconta` con `caffeinate`; log `~/scarica_storico.log` e `~/scarica_ask.log`. Il BID si era fermato all'11/02/2020 senza messaggio (Mac spento o riavviato).
- **Pacchetto per il DGS:** usare `trading_brain_dgs05b.zip`; il vecchio `trading_brain_dgs05.zip` conteneva il nome dell'utente in uno ZIP annidato (#72).
- **Difetti:** registro fino a #85; revisione notturna integrata (REGISTRO-MODIFICHE v1.46). R14 di Gemini: mandato aggiornato, da consegnare dopo la revisione del laboratorio.

## Stato al 15/11/2026 sera (leggere prima di tutto il resto)
- **Scheda di stato aggiornata:** `governance/STATO-PROGETTO.md` (contatori, cosa manca per il sigillo, decisioni aperte).
- **Ramo:** `feat/esecutore-h002`, non unito a main. **Congelamento** dopo l'incidente #41: nessuna esecuzione sui dati veri, nessuna modifica alle regole di H-002 senza decisione dell'utente.
- **H-002:** «non decidibile · parcheggiata» (decisione dell'utente); esce dal parcheggio **solo** su dati successivi al 12/11/2026, sigillata prima, contata in N (`laboratorio/ipotesi/H-002-REVISIONI.md`). La patch di `tb-proposte` è archiviata e **non applicata**.
- **Riserva di verifica (2005 → 31/10/2023):** intatta per tutte le trascrizioni presenti sul Mac (censimento di Gemini + riconteggio completo di Claude con `riconta.py`, 16/11: 19 segnalazioni, tutte falsi allarmi). CSV della vecchia pipeline: solo sviluppo (dal 12/11/2023). Limite: ciò che l'utente ha guardato a mano non è contabile.
- **Esplorazioni sullo sviluppo:** E-001, E-002 (Claude), E-003 (Gemini, 14/11, fuori protocollo): contano in N per le ipotesi che ne usano i tagli.
- **Dati:** BID fino al 07/06/2009 e dal 12/11/2023; ASK solo dal 12/11/2023. Scaricamento con `dati/pipeline/scarica_cache.py --continua-su-http`, dal Mac (worktree `tb-scarica`).
- **In corso:** scaricamento storico avviato la notte del 15–16/11 (`~/scarica_storico.log`, worktree `tb-scarica`; BID dal 2009-06-08, poi ASK dal 2005-01-01). **Da avere dall'utente:** ora della nota dello 0,15 R e conferma che il «banco» è la taratura di Gemini (IA-01).
- **Dopo:** controllo della cache a scaricamento finito; righe «DA GUARDARE» di `riconta.py`; giro R12 (Gemini e DGS); regole generali chieste dal DGS; sigillo solo dopo due giri senza difetti gravi; poi una nuova ipotesi (H-003), con la soglia minima già fissata: **IA-02, R medio netto ≥ +0,15 R** (decidere nella scheda se sulla stima o sul limite inferiore, prima dei dati).
- **Lavoro della notte del 16/11 (Claude):** calcolo di potenza per IA-02 (`laboratorio/studi/risultati/potenza_IA-02.md`); registro della riserva (`laboratorio/esecuzione/riserva.py`, **da ratificare**: α totale, finestre, parte protetta); modello di scheda `laboratorio/ipotesi/MODELLO-SCHEDA-H-003.md` (**da approvare**). Gemini: mandato R12-bis (`collaborazione/da-claude/PROMPT-R12-BIS-GEMINI.md`).
- **Idea parcheggiata per il futuro:** Osservatorio del Ragionamento di Trading (`piano/IDEA-OSSERVATORIO-RAGIONAMENTO.md`). **Impegno di Claude:** a ogni ripresa controllare il cancello d'avvio (§4) e dire all'utente quando tutte le condizioni sono vere. Non si avvia prima.
- **ChatGPT sul Mac (16/11):** l'app desktop aveva acceso «Utilizzo del computer → Qualsiasi app» (controllo di tutte le app del Mac); spento dall'utente su consiglio di Claude. «Accesso completo» spento; area di lavoro `Documents/Codex`, fuori dal progetto. Regola: a ChatGPT non si concede accesso a `trading-brain-core`, ai worktree o a cartelle con dati; come DGS legge solo il pacchetto redatto.
- **Attenzione con TradingView:** guardare solo dal 15/11/2023 in avanti; ogni idea va scritta con data e periodo guardato prima di essere provata; ChatGPT è il DGS e non deve diventare autore delle idee che poi giudica.

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

Il G0 **non** è ancora utilizzabile per decidere: serve la riconciliazione con un estratto conto (DA-25).

**Migrazione al repository canonico (D-19): eseguita il 12/11/2026.**
- Il Brain vive ora in `gioelemelis2-dot/trading-brain-core` (privato).
- `main` contiene la storia della sola `brain/` (23 commit, albero identico all'origine: `7422e1fc…`) più la configurazione del repository.
- Il ramo `claude/vibrant-cannon-5uunho` di `l-Altro` resta come copia storica, non più aggiornata.
- Da fare: archiviare le consegne di Gemini nel nuovo repository.

**Ramo `feat/fix-g0-journal`:**
- 5 correzioni del mandato «Binario A»;
- 7 correzioni del contro-audit (P-05 contro il limite della prop firm; seconda parte di P-01; validazione all'ingresso del journal; correzioni in `brier()`; impronta esterna dell'ancora; positività in G0; documenti di continuità).
- 5 correzioni del mandato notturno (commissioni non negative; avvisi P-05 anche a limite personale superato; coerenza di correzioni ed esiti nel journal; dati di sessione e soglie validati; booleani rifiutati come numeri).
- TDD: **52/52 test verdi** con `-W error`; mutation testing: **44/44 mutanti non equivalenti uccisi** (`guardian/test/mutazioni_g0_journal.py`).
- Audit su Gemini: il ramo `feat/lab-dati-backtester` non è su GitHub; i 138 hash dichiarati nei materiali di Gemini ricevuti coincidono; l'hash falso del V3.3 citato nel mandato non compare in nessun materiale disponibile (`CONSEGNA_FIX_G0/AUDIT_OSTILE_SU_GEMINI.md`).
- Consegna in `collaborazione/da-claude/CONSEGNA_FIX_G0/`.
- Unito a `main` il 12/11/2026 (commit `138daf3`), su autorizzazione dell'utente.
- Rifinitura dopo l'audit incrociato con Gemini (macOS, Python 3.9.6):
  - Python 3.9+ (TOML portabile in `g0/_toml.py`; orari in un formato unico su ogni versione);
  - `probabilita` anche come `Decimal`;
  - lock esclusivo in `aggiungi()`, che corregge anche una collisione reale fra scrittori concorrenti sul file temporaneo dell'ancora.
  - 61/61 test su Python 3.9, 3.11, 3.12 e 3.13; mutanti non equivalenti uccisi: 58/58 su 3.13 e 57/57 su 3.9 (V48 equivalente prima di 3.11).

**Audit esterno «Red Team»: chiuso per il Guardian e per il Binario B.**
- Bonifica sul ramo `fix/red-team-guardian`, unito a `main` (`fd14834`): 13 rilievi in TDD (NON STIMABILE in limiti e scheda, trade sovrapposti in R1, stringhe dello strumento e rumore float nel tick, `versioni_finali` ed esiti senza `chiude`, lock con O_CLOEXEC, lock orfani e `verifica` sotto lock, `fmt` con esponenti estremi, P-01 con capitale nullo, chiavi TOML tra virgolette).
- Audit di verifica: 0 CRITICO e 0 ALTO nei 7 file del Guardian; 1 MEDIO (`versioni_finali` accettava `chiude` verso una correzione), corretto in TDD su `main` (`3372072` rosso, `18bd042` verde).
- **Binario B verificato** dopo la pubblicazione su `origin/main` (`30ea8e6`; `brain/guardian/` invariato rispetto a `591302a`).
  - ALTO-2 (atomicità di `portfolio.on_fill`): risolto. Controesempio indipendente di Claude: chiusura USD/JPY su conto EUR senza cambio → `ValueError` prima di ogni modifica; cassa, storico dei fill e posizione invariati.
  - ALTO-7 (SL/TP dopo un gap in `engine`): risolto. Controesempio: segnale LONG al close 100 con SL 95 e TP 105, apertura a 90 dopo il weekend → ordine respinto, nessuna operazione, cassa invariata.
  - Entrambi verificati su Python 3.13 e 3.9.

**Stato consolidato di `main`:**
- Suite unificata: **118/118 test verdi** con `python3 -s -B -W error`, su Python 3.13 e 3.9. Sono 77 di `brain/guardian/test`, 32 del Binario B e 9 dello scaricamento Dukascopy.
  - Dalla radice del repository: `python3 -s -B -W error -m unittest brain.dati.tests.test_pipeline brain.dati.tests.test_dukascopy brain.laboratorio.tests.test_backtester brain.laboratorio.tests.test_anti_frode_statico`.
- `brain/guardian/`: verde anche su Python 3.11 e 3.12 (76/76 all'ultima prova su quelle versioni, prima del test sulle frazioni).
- ALTO-8 (race nel recupero del lock orfano senza `fcntl`, da una revisione esterna) corretto in TDD sul ramo `fix/lock-orfano-toctou` e unito a `main`.
- Mutanti non equivalenti uccisi: 80/80 su 3.13 e 79/79 su 3.9 (V48 equivalente prima di 3.11, E01 equivalente su tutte le versioni). Riconfermati con le 14 regole personali attive.
- **Progetto generale** (13/11/2026), documento condiviso fuori dal repository: «Trading Brain — Progetto generale» (claude.ai). Contiene architettura, Gate 0–7 (i Gate 3–7 sono proposte da approvare), numeri per validare una strategia, regole, rischi e decisioni aperte, più i prompt per i revisori esterni (DeepSeek e ChatGPT, in corso).

**Gate operativi** (denominazione dell'utente; nel Brain non c'è ancora una definizione formale dei gate):
- **Gate 0, chiuso:** verifica completa del codice. Guardian e Binario B sono su `main`, con ALTO-2 e ALTO-7 verificati e 108/108 test.
- **Gate 1, configurato ma NON riconciliato** (rilievo di Gemini G-20261113-01; prima era scritto «chiuso»): conto demo broker ECN su MetaTrader 5, 50.000 USD, XAU/USD.
  - Il 13/11/2026 l'utente ha detto di **non avere easyMarkets**: il broker del conto va confermato. FP Markets è previsto come nuovo conto demo.
  - Scheda: `dati/reali/demo_broker_mt5_50k_xauusd.toml`, rinominata da `demo_mt5_50k_xauusd.toml`.
  - Regole interne 5% giornaliero (2.500 USD) e 10% totale (5.000 USD), simulate con lo schema `ftmo_2step`.
  - Commissione ECN round-turn 7,00 USD/lotto. Specifiche del contratto e commissione sono da verificare sul broker (stato C).
  - Regole personali confermate dall'utente il 12/11/2026: **P-01 = 0,5%** (250 USD per trade) e **P-05 = 1,5%** (750 USD al giorno).
  - Il 13/11/2026 confermate anche P-02…P-04 e P-06…P-14, su proposta di Claude. Valori: P-06 = 1 posizione aperta, P-08 = 15 minuti attorno alle news, P-11 = 15 minuti di pausa dopo una perdita, P-12 = 60 secondi prima del click, P-14 = 7 ore di sonno.
  - P-15 resta proposta: con lo 0,5% a trade coincide con P-05.
  - Nella scheda risultano «14 confermate su 15».
  - La «perdita massima 1,5%» indicata dall'utente è giornaliera, cioè coincide con P-05.
  - Scheda **non riconciliata** con la piattaforma (DA-25): finché non lo è, la scheda dichiara di non usarne i numeri per decidere.
- **Gate 2, dati: stato al 14/11/2026.**
  - **3 anni BID scaricati** (13/11): 71.008 candele da 15 minuti, dal 2023-11-12T23:00Z al 2026-11-13T00:00Z.
    - Buchi: 598 pause giornaliere, 156 fine settimana, 22 chiusure anticipate dei festivi USA (verificate sulle date), 0 anomali.
    - Il sigillo 70/30 creato in locale **non si pubblica** (provvisorio); il suo nonce resta in `~/.trading_brain/nonce/XAUUSD_15m/`.
  - **DA-26, inversione decisa dall'utente il 14/11:**
    - **sviluppo:** dal 15/11/2023 in poi (dati già visti);
    - **verifica sigillata:** dal 2005 a circa il 31/10/2023 (date esatte dopo il conteggio dei buchi per anno);
    - **test finale:** il futuro (demo).
  - Dukascopy ha l'oro almeno dal 2005; il 2003 ha risposto 429, quindi non si sa.
  - **Scaricamento storico BID dal 2005 in corso sul Mac**, senza sigillo, log `~/ciclo_storico.log`.
    - Proposta del 14/11: fermarlo, scaricare prima gli **ASK dei 3 anni recenti** (log `~/ciclo_ask_recente.log`), poi riprenderlo, e alla fine scaricare gli ASK storici.
  - **Codice su main:**
    - DSR con la scala sqrt(V) e input validati;
    - partizione per date con embargo (`dati/pipeline/partizione_date.py`), con verifica legata al file della partizione;
    - bande di prezzo per anno, salti di scala e ampiezza della candela;
    - opzione `--lato ASK`;
    - file compresso danneggiato = ErroreDati.
    - Test verdi su Python 3.13 e 3.9; mutanti 44/44 su entrambe (`dati/tests/mutazioni_dsr_partizione.py`).
- **Ricerca, stato al 14/11/2026:**
  - **Studio 1 (E-001, esplorativo, solo sviluppo):** `laboratorio/studi/studio_sessioni.py`, risultati in `laboratorio/studi/risultati/`, registro in `laboratorio/studi/REGISTRO-ESPLORAZIONI.md`.
    - La volatilità si concentra fra le 14 e le 17 italiane.
    - Nessuna struttura direzionale chiaramente diversa dal confronto casuale.
  - **H-001** (scalping nei micro-range a 1 minuto, idea dell'utente): bozza critica in `laboratorio/ipotesi/H-001-range-1m-BOZZA.md`.
    - Attende 4 risposte dell'utente.
    - **DA-30:** sarà automatizzata in demo (Expert Advisor MQL5, replica indipendente di Gemini).
  - **H-002** (rottura del range di apertura di Londra): scheda `H-002-ORB-v3.md` (v3.1), revisioni R1–R6 in `H-002-REVISIONI.md`, simulatore `laboratorio/simulatori/orb_londra.py` (43 test, mutanti 33/33).
    - Decisioni dell'utente: solo Londra, varianti V-T e V-S (N = 2), esclusi i range oltre 2 × la mediana.
    - **Mandato notturno 14–15/11 (ramo `feat/esecutore-h002`, NON unito a main):**
      - programma dei criteri completo in `laboratorio/esecuzione/`, con prove su mercati inventati: casuale bocciato, vantaggio noto trovato, sola tendenza bocciata;
      - strumento di sigillo pronto ma **non eseguito**: il registro `laboratorio/registro_prove.json` non esiste;
      - 11 ambiguità della scheda annotate con proposte (A1–A11 in `H-002-REVISIONI.md`), scheda non toccata;
      - quaderno delle ipotesi `laboratorio/ipotesi/QUADERNO-IPOTESI.md` (Q-01…Q-10, solo letteratura).
    - **Prossimo passo:** revisioni R7 (Gemini, DeepSeek, ChatGPT) del ramo → decisioni dell'utente sulle ambiguità → eventuale v3.2 → merge autorizzato → sigillo deciso dall'utente → screening sullo sviluppo con `esegui_h002.py`.
    - Servono prima i dati ASK dello sviluppo nella cache del Mac (`cache_dukascopy/XAUUSD_ASK`).
  - **TradingView:** nessun connettore. Indicatore Pine solo visivo in `laboratorio/tradingview/tb_sessioni.pine`; copre il periodo sigillato.
    - Si guarda solo dal 15/11/2023; vietato lo Strategy Tester per provare idee.
  - **DA-29:** arresto in demo con controllo di fedeltà (solo esecuzione) e test sequenziale di Wald (θ1 = Sharpe 0,10, σ dal backtest, potenza effettiva circa 64% con taglio a 600 trade).
    - Simulazione riproducibile: `laboratorio/studi/simulazione_sprt.py`.
- **INCIDENTE del 14/11 (da decidere):** Gemini ha eseguito H-002 sui dati veri dello sviluppo prima del sigillo (rami `rev/gemini-dgs03`, `rev/gemini-analisi-h002`), e ha modificato file di Claude su `rev/gemini-proposte-tester-dgs03`. Dettagli in `H-002-REVISIONI.md`, sezione «INCIDENTE»; difetto di processo #41.
  - **Fermo:** nessuna esecuzione su dati veri e nessuna modifica delle regole di H-002 finché l'utente non decide.
  - **Proposta di Claude:**
    1. congelare le regole di H-002 come sono nella v3.1, applicando solo le decisioni che non cambiano i trade;
    2. contare nel registro come prove tutte le varianti già eseguite sullo sviluppo;
    3. sigillare;
    4. eseguire lo screening ufficiale e accettarne l'esito, compresa la chiusura di H-002;
    5. la verifica 2005–2023 resta cieca.
  - **Rimedio tecnico proposto:** il caricatore rifiuta anche lo sviluppo senza un sigillo valido (oggi lo controlla solo la riga di comando).
- **ChatGPT = Direttore generale della sicurezza (DGS)** dal 15/11:
  - materiali in `collaborazione/da-claude/direttore-sicurezza/`;
  - consegne in `collaborazione/da-chatgpt/`;
  - giro R11 su H-002 a Gemini e al DGS sullo stesso commit.
- **Collaborazione:** le chat di Gemini sul sito non vedono il repository e possono ragionare su stati superati (è successo il 14/11 con un «mandato di audit» del vecchio sigillo 70/30, da NON eseguire). Per lo stato del progetto fanno fede il repository, Antigravity o Claude.
- Rami su GitHub già uniti e da pulire (con il via libera dell'utente): `feat/fix-g0-journal`, `fix/red-team-guardian`, `fix/lock-orfano-toctou`, `fix/dsr-e-partizione-date`, `rev/dati-diversificazione-gemini`, `rev/vettori-dsr-gemini`, `rev/gemini-20261114`, `rev/gemini-h002`.

**Pendenze aperte (controllo del 14/11/2026 contro il documento del progetto e le decisioni aperte):**
- **Utente:**
  - risposte per H-001;
  - broker del conto demo MT5 da 50.000 USD (DA-25, chiesto più volte);
  - apertura della demo FP Markets e screenshot delle specifiche XAUUSD;
  - esito della revisione esterna del documento del progetto (inviato a DeepSeek il 13/11);
  - piano di accumulo e budget (fuori dal repository).
- **Decisioni:**
  - DA-14 (Pine solo per visualizzare: proposta da adottare);
  - DA-17 (contaminazione: di fatto applicata con l'inversione, da chiudere);
  - DA-19 e DA-20 (registro unico; robustezza registrata ma fuori da N; sviluppo come screening e DSR sulla verifica);
  - DA-23 (procedura per modificare le regole personali; serve per lo scalping e l'automazione);
  - DA-27 e DA-28 (diversificazione, non urgenti);
  - criterio di discordanza Dukascopy–MT5 e le «due chiavi» per FTMO (proposte di Gemini G-20261114-01).
- **Claude:**
  - verificare le FAQ FTMO citate da Gemini (overnight, weekend, notizie, leva) e aggiornare `prop_firm_ftmo.toml`;
  - fonte di un calendario storico delle notizie (P-08);
  - conteggio dei buchi per anno sullo storico;
  - simulatore minuto per minuto: fatto (main); programma dei criteri: fatto sul ramo, in revisione;
  - aggiornare il documento del progetto.
- **Mai usati finora:** la scheda del Guardian G0 e il journal. Vanno avviati con la prima demo vera.

## Correzioni note ancora da applicare (dopo il via libera)
- Contestazione, punto C-04: il rimando "(§3, C-05)" va corretto in "(§3, C-06)".
- Registri: seconda revisione e stato dello Studio 01 nel `REGISTRO-CONOSCENZE.md`; Q-01…Q-07 in `DOMANDE-APERTE.md`; conteggio della bibliografia (audit I-02, I-03, I-06).

## Ripresa dopo interruzioni
Prompt pronto in [`PROMPT-RIPRESA.md`](PROMPT-RIPRESA.md). Regola: prima di un lavoro lungo, Claude programma un messaggio di ripresa con quel prompt; senza lavoro in corso non programma nulla.

## Convenzioni da mantenere
- Lingua: italiano. Mai segnare una fonte come V senza averla letta; mai una padronanza senza cancello superato dichiarato dall'utente; mai dati simulati presentati come reali.
- Repository: `gioelemelis2-dot/trading-brain-core` (D-19), ramo `main` più rami di lavoro dedicati (per esempio `feat/fix-g0-journal`); il vecchio ramo di `l-Altro` è solo storico.
- Gemini scrive solo in `collaborazione/da-gemini/`; Claude non modifica mai i materiali di Gemini.
