# Registro unico delle decisioni aperte

**Ultimo aggiornamento:** 12/11/2026 (Claude). Le decisioni già prese sono in [`DECISIONI.md`](DECISIONI.md) (D-01…D-18) e **non vanno riaperte**.

**Scopo.** Riunire in un solo posto le decisioni che spettano all'utente, oggi sparse in cinque documenti:
- relazione dell'audit dell'11/11;
- proposta Parte B;
- audit dell'architettura V2;
- documento delle decisioni di Gemini;
- valutazione della controverifica.

Per ognuna indico alternative, conseguenze, posizione di Claude e posizione di Gemini, ciascuna con la fonte. Le raccomandazioni sono pareri: **nessuna decisione è presa qui**.

**Come usarlo.** Basta rispondere con l'identificativo e la scelta (per esempio «DA-01: B»). Ogni decisione presa passa in `DECISIONI.md` con data e fonte.

---

## Ordine consigliato

Le decisioni sono collegate tra loro. Questo è l'ordine che minimizza i blocchi.

```
DA-01 fonte di verità ──► DA-05 struttura delle cartelle ──► DA-07 stime sigillate
DA-03 sospensione dello sviluppo ──► tutto ciò che produce codice (DA-06, DA-11)
DA-15 dati ──► DA-17 strategie
DA-13 rulebook (Q-09) ──► DA-11 G0 minimo ──► DA-12 indicatori comportamentali
```

**Bloccanti:** DA-01, DA-03 e DA-15, **decise il 12/11/2026** insieme a DA-11 (D-19…D-22). Le altre possono attendere senza costi rilevanti.

---

## A. Fondamenta

### DA-01 · Fonte di verità unica, sincronizzazione e archivio delle consegne · **bloccante**
**Decisa il 12/11/2026 → D-19. Eseguita il 12/11/2026:** repository privato `gioelemelis2-dot/trading-brain-core`; storia della sola `brain/` migrata su `main` (albero identico, `7422e1fc…`). Restano da fare: test di scrittura di Gemini sul nuovo repository e archivio delle sue consegne. Il testo sotto resta come storia.
- **Situazione verificata:**
  - il Brain versionato è sul ramo GitHub `claude/vibrant-cannon-5uunho` del repository `l-Altro`, che sugli altri rami contiene un'applicazione TypeScript estranea;
  - Gemini lavora su una copia locale (dichiarato da Gemini; non verificabile da Claude);
  - le consegne di Gemini (V2–V3.3, architettura V2, controverifica) non sono archiviate nel Brain;
  - lo scambio avviene con ZIP via utente, e il push di Gemini su GitHub era già fallito durante il trasferimento V2.
- **Alternative:**
  - **A.** nuovo repository dedicato;
  - **B.** ramo dedicato nel repository attuale;
  - **C.** rinviare.
- **Conseguenze:**
  - A e B funzionano solo se **entrambi i modelli possono scrivere** nello stesso posto: va verificato prima per Gemini.
  - A richiede anche di estendere l'accesso della sessione di Claude al nuovo repository.
  - Con C restano due copie divergenti.
- **Parere di Claude:** prima un test pratico (Gemini pubblica un file di prova su un ramo); poi A o B, indifferentemente; in ogni caso, archivio delle consegne di Gemini con manifest (`audit/AUDIT-ARCH-20261111` §5.3; architettura V2, Audit §8.12).
- **Parere di Gemini:** A (Decisioni Gemini, 1).
- **Collegate:** D-02 (migrazione sospesa), DA-05.

### DA-02 · Master Mission e Protocollo comune
- **Situazione:** testi assenti in tutte le copie accessibili. Le schede STR citano §5.2, §5.3 e §7 del Master Mission. Il rulebook cita invece lezioni del Manuale v1, non il Master Mission.
- **Alternative:**
  - **A.** l'utente fornisce i testi originali;
  - **B.** nuovo documento fondativo redatto da Claude e Gemini e approvato dall'utente;
  - **C.** rinviare.
- **Conseguenze di B:** il nuovo documento deve avere un **nome diverso** e una numerazione propria. Le citazioni esistenti restano marcate «testo non disponibile», per non attribuire al nuovo testo ciò che il vecchio diceva.
- **Parere di Claude:** A se esiste; altrimenti B con nome nuovo (valutazione della controverifica, §7).
- **Parere di Gemini:** A, poi B in subordine (Decisioni Gemini, 2).
- **Collegate:** D-09.

### DA-03 · Sospensione dello sviluppo (D-10, D-12) · **bloccante**
**Decisa il 12/11/2026 → D-20.** Il testo sotto resta come storia.
- **Situazione:** D-12 sospende ogni nuovo modulo in attesa del dossier di revisione di Gemini sulle lezioni (`GEMINI_PEER_REVIEW_CLAUDE.md`, richiesta R-001), **mai consegnato**. Restano congelate le lezioni L2.4–L2.6 e sospesi:
  - unità 2.2–2.3;
  - traccia 10.1;
  - generatore HTML;
  - piano a tre mesi.
- **Alternative:**
  - **A.** revocare la sospensione e approvare il piano a tre mesi;
  - **B.** revocarla solo per i lavori che nomini esplicitamente;
  - **C.** mantenerla finché Gemini non consegna la revisione delle lezioni.
- **Parere di Claude:** B. La sospensione è nata per una revisione che non è arrivata, e oggi blocca anche lavori utili e a basso rischio.
- **Collegate:** DA-06, DA-11, R-001.

### DA-04 · Conferma di D-08 (aggiunte non distruttive)
- **Domanda:** nuovi file e cartelle di supporto sono «modifiche strutturali importanti» (D-07)?
- **Alternative:** confermare D-08 oppure respingerla (in quel caso ogni nuova cartella richiede approvazione).
- **Parere di Claude:** confermare. Spostamenti, rinomine e cancellazioni restano soggetti a D-07.

### DA-05 · Struttura per i laboratori e i registri di ricerca
- **Alternative:**
  - **A.** strato `laboratori/` (audit 11/11);
  - **B.** `ricerca/claude/` e `ricerca/gemini/` (architettura V2 di Gemini);
  - **C.** restare in `collaborazione/` in modo provvisorio.
- **Parere di Claude:** decidere dopo DA-01: la struttura va creata nella fonte di verità definitiva, non due volte.
- **Parere di Gemini:** B.

---

## B. Metodo scientifico

### DA-06 · Modello epistemico e prototipo
- **Situazione:** Claude e Gemini concordano sul fatto che il modello a 5 tipi va separato in assi. Divergono sul numero: Claude 7, Gemini 5, senza le classi E1–E7 e la classe di contenuto (valutazione della controverifica, G-17).
- **Alternative:**
  - **A.** approvare i 7 assi e autorizzare il **prototipo** dello schema: tre calcoli del Guardian con test di rifiuto (Audit §3.6);
  - **B.** approvare i 5 assi di Gemini;
  - **C.** rinviare.
- **Conseguenze:** il prototipo è codice nuovo: richiede DA-03 e va confrontato con DA-11 (T-01…T-05).
- **Parere di Claude:** A.

### DA-07 · Stime sigillate come regola comune
- **Proposta:** prima di confrontarsi, ogni modello registra la propria stima con un **impegno crittografico con sale casuale**, rivelato all'apertura. Un hash senza sale non nasconde un valore breve.
- **Alternative:** adottarla nel protocollo comune, oppure no.
- **Parere di Claude:** adottarla.
- **Parere di Gemini:** adottarla, ma senza sale (controverifica, D.2).
- **Collegate:** DA-01 (serve un registro condiviso).

### DA-08 · Proposta Parte B di Claude
- **Domande:**
  - approvare, modificare o respingere `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md`;
  - avviare il formato di **consulto** (anche solo in modalità paper).
- **Parere di Claude:** approvare con le correzioni emerse dopo (sale nelle stime sigillate, D-15 simmetria); consulto solo dopo DA-11.

### DA-09 · Compendio delle discipline
- **Alternative:**
  - **A.** fase autonoma (Fase 2 di Gemini);
  - **B.** schede incrementali, scritte quando un componente le richiede, con prove a risposta nota sul modello L1–L5 di `STANDARD.md`.
- **Parere di Claude:** B (Audit §7).
- **Parere di Gemini:** riformula la Fase 2 come «memoria esterna», senza scegliere tra A e B.

### DA-10 · Revisione esterna
- **Domanda:** sottoporre audit, controverifica e valutazione a un modello di **un altro fornitore** o a una persona competente.
- **Materiale:** pacchetto pronto in `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/`.
- **Parere di Claude:** sì. Due cicli Claude↔Gemini hanno prodotto molta convergenza e pochi disaccordi.

---

## C. Rischio e Trading Guardian

### DA-11 · G0 minimo anticipato e collocazione di T-01…T-05
**Decisa il 12/11/2026 → D-22.** Il testo sotto resta come storia.
- **Contesto:** D-17 rende T-01…T-05 requisiti di ingresso della «successiva fase tecnica». Se il G0 minimo è il primo software, l'errata va chiusa **prima** di scriverlo, oppure si decide esplicitamente il contrario.
- **Alternative:**
  - **A.** errata T-01…T-05, poi G0 minimo (perdita a stop con H_esec, margini, somma dei rischi a stop, journal) subito dopo Q-09;
  - **B.** G0 minimo prima dell'errata, che si chiude al gate della Fase 5 (raccomandazioni di Gemini combinate);
  - **C.** G0 alla Fase 7.
- **Conseguenze:** A rispetta alla lettera D-17. B anticipa l'utilità, ma scrive codice nuovo con il debito di V3.3 ancora aperto.
- **Parere di Claude:** A. L'errata è piccola: uno script di mutazione, due test e correzioni documentali.
- **Parere di Gemini:** G0 minimo anticipato (Decisione 4) ed errata alla Fase 5 (Decisione 3).

### DA-12 · Indicatori comportamentali del Guardian
- **Alternative:**
  - **A.** misure oggettive più indicatori **definiti in anticipo**, con interpretazione etichettata come IPOTESI e validata sui tuoi dati;
  - **B.** solo misure.
- **Parametri:** se A, i parametri (minuti, variazione di size) li fissi **tu**, prima della raccolta. Punto di partenza: le regole già scritte nel tuo Manuale v1, Lezione 21 (timer di 60–90 secondi; 10–15 minuti lontano dallo schermo). Le soglie «180 s» e «size raddoppiata» proposte da Gemini sono arbitrarie.
- **Limite:** è uno studio osservazionale su una persona. Una correlazione non prova un nesso causale, e con più indicatori serve una correzione per test multipli.
- **Parere di Claude e di Gemini:** A (il contenuto è condiviso).

### DA-13 · Rulebook (Q-09) e verifica delle regole della prop firm
- **Alternative di formato:**
  - **A.** due file separati, regole della prop firm e regole personali (Gemini);
  - **B.** un file con il campo «origine».
- **In entrambi i casi** ogni regola della prop firm va verificata sulla fonte ufficiale con data: base del pavimento giornaliero, orario di reset, max loss statico o trailing, limiti di tempo. Oggi lo stato è V-sec.
- **Parere di Claude:** A va bene; la verifica sulla fonte ufficiale è la parte che conta.

### DA-14 · Regola sui segnali Pine
- **Proposta di Gemini, condivisa da Claude:** nessun segnale generato in Pine va a mercato reale senza essere stato specificato, testato e riprodotto dal motore locale.
- **Alternative:** adottarla, oppure lasciare all'utente l'uso libero dei segnali TradingView.
- **Conseguenza:** vincola la tua operatività, quindi la decisione è tua (D-18).

---

## D. Dati

### DA-15 · Fornitore, budget, licenze e perimetro dei dati · **bloccante**
**Decisa il 12/11/2026 → D-21.** Il testo sotto resta come storia.
- **Situazione:**
  - dalla rete dell'ambiente di Claude sono rifiutati FRED, Yahoo, Stooq, Crossref e doi.org; la rete si può configurare nelle impostazioni dell'ambiente;
  - STR-001 richiede futures giornalieri 2005–2026 su 10 mercati;
  - STR-002 richiede dati M1 del future ES dal 2015.
- **Alternative:**
  - **A.** dati gratuiti o forniti da te, limitati alle ipotesi registrate, con licenze lette;
  - **B.** fornitore commerciale;
  - **C.** abilitare host specifici nell'ambiente di Claude.
- **Conseguenze:** «costo zero» non è verificato per i dati futures. Le licenze possono vietare la redistribuzione, anche tra i due modelli.
- **Parere di Claude:** A per iniziare, con un registro delle licenze, più C per le fonti pubbliche (FRED).
- **Parere di Gemini:** A, poi B prima del paper trading. Gemini però definisce il perimetro come «S&P 500 ed EUR/USD», cosa che non corrisponde a STR-001.

### DA-16 · Raccolta precoce dei dati che richiedono tempo
- **Proposta:** avviare subito, con strumenti minimi, il **journal** delle decisioni e del comportamento e il registro delle **previsioni da valutare**. La validazione ne richiede mesi.
- **Tutele:** il journal contiene dati personali sensibili (sonno, stato emotivo): conservazione locale, nessun invio a servizi esterni senza tuo consenso.
- **Parere di Claude:** sì, appena decisi DA-01 e DA-12.

---

## E. Strategie

### DA-17 · Revisione delle schede STR (Q-07) e regola sulla contaminazione
- **Contesto:**
  - le schede dichiarano come fuori campione periodi già trascorsi e noti ai modelli;
  - le ipotesi generate da LLM possono incorporare la storia vista durante l'addestramento.
- **Alternative:**
  - **A.** riscrivere le schede dichiarando i periodi osservati. Lo storico vale come prova **debole**: un fallimento è informativo, un successo vale poco. La validazione forte avviene solo su dati successivi al cutoff del modello e alla registrazione, raccolti in forward;
  - **B.** rinviare alla Fase 6.
- **Parere di Claude:** A, dopo DA-15.

---

## F. Pendenze minori

### DA-18 · Correzioni note da applicare
- Contestazione C-04: il rimando «(§3, C-05)» va corretto in «(§3, C-06)».
- Aggiornamento di `REGISTRO-CONOSCENZE.md`, `glossario/DOMANDE-APERTE.md` e dei conteggi della bibliografia (audit I-02, I-03, I-06).
- Correzioni del mio audit dell'architettura emerse dopo (valutazione della controverifica, §5 e §9).
- **Alternative:** autorizzare oppure no.
- **Parere di Claude:** autorizzare: sono correzioni documentali senza rischio.

---

## G. Decisioni aggiunte dalla revisione esterna (ChatGPT, 12/11/2026, §8)

### DA-19 · Conteggio delle prove di ricerca
- **Proposta:** si contano **tutte le varianti eseguite e registrate**, da entrambi i modelli e in tutte le sessioni, in un registro unico. Non si contano pensieri non osservabili.
- Il conteggio alimenta il DSR (DA-20).

### DA-20 · Criterio di promozione da ricerca a «candidata forward»
- **Proposta:** un criterio unico, definito prima dei test: DSR calcolato sul conteggio di DA-19, calcolo di potenza per l'ipotesi specifica, robustezza ai parametri, costi realistici, criteri di falsificazione.
- Nessuna soglia fissa universale (né t > 3, né 594 trade).

### DA-21 · Dati point-in-time
- **Da decidere:** regole per revisioni dei dati macro (versioni storiche), contratti continui e roll, cambi di sessione e ora legale.

### DA-22 · Limiti di accesso ai registri dei due modelli
- **Da decidere:** come impedire che un centro legga il registro dell'altro prima del proprio impegno sigillato (DA-07).
- **Nota:** impegno con nonce casuale segreto di 256 bit; registro append-only con data affidabile; l'hash non è una firma e non prova l'autore.

### DA-23 · Modifica delle regole personali
- **Da decidere:** procedura per cambiare una regola personale: solo a mercato chiuso, con motivazione scritta, periodo di attesa e versione registrata.

---

## H. Informazioni e scelte necessarie per usare G0 e journal (12/11/2026)

### DA-24 · Dove conservare i dati del journal
- **Alternative** (`guardian/journal/LEGGIMI.md`):
  - **A.** sul tuo computer;
  - **B.** nel repository privato, compilato da Claude in sessione;
  - **C.** misto: trade, decisioni e previsioni nel repository; stato personale solo in locale.
- **Parere di Claude:** C. Protegge i dati sensibili e permette di lavorare insieme sul resto.

### DA-25 · Dati del conto per completare e riconciliare il G0
- Prodotto FTMO (2-Step, 1-Step, Instant) e tipo di conto (Standard o Swing), dimensione, valuta e piattaforma.
- Strumenti operati e loro specifiche presso il broker.
- Conferma o modifica delle regole personali P-01…P-15 e dei valori «DA DEFINIRE».
- Un estratto conto, anche demo, per la riconciliazione: senza riconciliazione il G0 non si usa per decidere.
- Dettaglio in `guardian/regole/LEGGIMI.md`.

---

## Fonti di questo registro
- `audit/AUDIT-ARCH-20261111/RELAZIONE-AUDIT.md` §5;
- `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/CLAUDE_EVALUATION_OF_GEMINI_COUNTERCHECK_V1.md` §7;
- `TRADING_BRAIN_UNRESOLVED_DECISIONS_V1.md` di Gemini (non archiviato nel Brain: vedi DA-01);
- `CONTINUITA.md`;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md` §8.
