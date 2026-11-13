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

## I. Dati e autoinganno (13/11/2026)

### DA-26 · Partizione dei dati prima del sigillo · **bloccante per il Gate 2**
- **Problema:** il sigillo (`commitment.json`) prova che i dati Out-of-Sample non sono stati modificati, non che nessuno li abbia guardati. Con 3 anni e una divisione 70/30, l'Out-of-Sample sono gli ultimi ~11 mesi. L'utente li ha visti sui grafici, e Claude ne conosce l'andamento a grandi linee dall'addestramento: il test non è davvero cieco.
- **Contromisura approvata dall'utente il 13/11/2026:**
  - più anni di storico;
  - un periodo vecchio tenuto come verifica;
  - il futuro, cioè l'incubazione sui conti demo, come test finale.
- **Da decidere:** quanti anni (prima va verificato da quale anno Dukascopy ha XAUUSD), quale periodo di sviluppo, quale periodo di verifica.
- **Fino ad allora:** il sigillo sui 3 anni con 70/30 è provvisorio e non va pubblicato come definitivo.
- **Strumento pronto (ramo `fix/dsr-e-partizione-date`, da unire con l'autorizzazione dell'utente):**
  - partizione per date UTC in blocchi di sviluppo e verifica, con embargo, da un file TOML scritto prima (`dati/pipeline/partizione_date.py`, opzione `--partizione` dello scaricatore);
  - senza file non si sigilla nulla.
- **Fatti del 13/11/2026 (Mac dell'utente; nessun prezzo guardato):**
  - **Scaricamento dei 3 anni finito:** 71.008 candele da 15 minuti, dal 2023-11-12T23:00Z al 2026-11-13T00:00Z, 0 giorni senza dati.
  - **Buchi:** 598 pause giornaliere, 156 fine settimana (= 3 × 52), 22 chiusure lunghe, 0 anomali.
  - **Le 22 chiusure lunghe** sono chiusure anticipate nei festivi USA: Thanksgiving, MLK, Presidents' Day, Memorial Day, Juneteenth, 4 luglio, Labor Day, Natale e Capodanno. Claude ha controllato date e giorni della settimana. Quando il festivo cade di venerdì (Venerdì Santo, 4 luglio 2025, Juneteenth 2026) il buco si unisce al fine settimana: è coerente.
  - **Sigillo 70/30 creato in locale ma NON pubblicato:** è provvisorio. Il nonce è in `~/.trading_brain/nonce/XAUUSD_15m/` e va conservato.
  - **Prova degli anni su Dukascopy:**
    - 2005, 2008, 2011, 2014 e 2024: risposta 200, 11–16 KB;
    - 2003: risposta 429 (troppe richieste), quindi non sappiamo ancora se ci sono dati.
  - **Il 2005 pesa meno** (10,9 KB contro circa 14–15 KB): forse meno minuti scambiati. La qualità degli anni vecchi va misurata con i buchi per anno.
- **Deciso dall'utente il 13/11/2026:** scaricare XAUUSD dal 2005, senza sigillo. Cosa usare e come dividerlo si decide dopo aver contato i buchi anno per anno.
  - Motivi: più tipi di mercato (dal 2008 al 2022), abbastanza trade per la potenza statistica, anni recenti già visti dall'utente.
  - Limiti dichiarati: mercato del 2005 diverso da quello di oggi, quindi gli anni vecchi servono per la verifica e non per lo sviluppo; qualità dei dati vecchi da misurare.
- **Proposta di Gemini (G-20261113-01):**
  - blocco A: verifica vecchia;
  - blocco B: circa 10 anni di sviluppo, con walk-forward interno;
  - blocco C: dal 2024 a oggi, già visto, solo come filtro dei costi attuali;
  - blocco D: il futuro, cioè la demo;
  - embargo di 14 giorni; regole in ATR o percentuale, mai in USD fissi.
  - Il periodo vecchio è una verifica su un altro regime, **non un test cieco**: anche i modelli conoscono il 2008, il 2013 e il 2020.
- Le altre contromisure approvate (seconda fonte di dati, costi veri, replica indipendente, regole decise prima, «come lo sai?», niente nuova infrastruttura) sono nel documento «Trading Brain — Progetto generale», sezione «Contro l'autoinganno».

### DA-27 · Mercati della diversificazione e calendario comune
- **Proposta (13/11/2026):** dettagli in `governance/PIANO-DIVERSIFICAZIONE.md`.
  - Ordine: EURUSD, S&P 500, XAGUSD (come prova di robustezza), GBPUSD e USDJPY, DAX e petrolio; cripto solo alla fine.
  - Stesso periodo di sviluppo e stesso periodo di verifica, in date, per tutti i mercati, perché i mercati legati fra loro fanno trapelare il periodo chiuso.
  - Un mercato alla volta, dopo il sigillo dell'oro.
- **Da verificare per ogni mercato:** il codice su Dukascopy, l'anno di inizio e la disponibilità su FTMO e sui broker demo.

### DA-28 · Registro unico delle prove e mercati dichiarati prima
- **Proposta:**
  - ogni coppia ipotesi–mercato è una prova, in un unico conteggio che entra nel DSR (estende DA-19);
  - ogni ipotesi dichiara prima su quali mercati vale e con quali parametri, e non si ritocca da un mercato all'altro.
- **Oggi:** il registro è per strumento (`dati/operativo/trial_registry_xauusd.json`).

### DA-29 · Obiettivi in numeri e criteri di arresto (completa DA-20)
**Deciso dall'utente il 13/11/2026:**
- **Weekend chiuso:** nessuna posizione aperta nel weekend. Ogni ipotesi lo rispetta, e così il backtest.
- **Obiettivo:** essere in positivo. L'1–2% al mese su un futuro conto FTMO da 100.000 va benissimo; il 5% al mese sarebbe bello, ma l'utente sa che è molto alto.
- **Challenge FTMO:** solo dopo avere più strategie testate.
- **Arresto:** «ci fermiamo quando la probabilità non è a nostro favore». Va tradotto in numeri.

**Proposte di Claude, da confermare:**
- **Obiettivi tradotti in R.** Con P-01 = 0,5% a trade, l'1% al mese vale +2R al mese netti e il 2% vale +4R. Con 15–20 trade al mese servono circa +0,10–0,25R netti a trade. Il 5% al mese è +10R al mese, circa l'80% l'anno composto: non è un obiettivo di progetto.
- **Soglia minima per promuovere una strategia:** aspettativa netta di almeno +0,05R a trade, dimostrata statisticamente (DSR con tutte le prove contate). Obiettivo: +0,10R.
- **Arresto di una strategia in demo:**
  - drawdown di 10R dall'inizio (il 5% a 0,5% di rischio, metà del limite FTMO);
  - oppure aspettativa ≤ 0 dopo 100 trade.
  - Con 100 trade l'incertezza è di circa ±0,2R: la regola protegge dal danno, non dimostra nulla.
- **Arresto di un giro di ricerca:** al massimo 20 ipotesi a giro. Se nessuna passa, ci si ferma e si ripensa, senza allentare i criteri.
- **Overnight (l'utente non sa):**
  - le prime ipotesi sono solo intraday;
  - l'overnight è ammesso solo se l'ipotesi lo dichiara prima e il backtest include lo swap.
  - Le regole FTMO sull'overnight nel conto Standard sono da verificare (`prop_firm_ftmo.toml`, stato V-parziale).
- **Arresto in demo: scelta di Claude su delega dell'utente (13/11/2026), modificabile.** Sostituisce la regola dei 100 trade e del −10R.
  - **Controllo di fedeltà (primi 20–30 trade):** ogni trade della demo si confronta con quello che il backtest avrebbe fatto negli stessi giorni (segnali, prezzi di ingresso, spread, slippage). Una differenza sistematica ferma la strategia: il backtest non descrive la realtà.
  - **Test sequenziale di Wald (SPRT) sul risultato in R:** H0 aspettativa 0, H1 aspettativa +0,10R, α = 5%, β = 20%, σ stimata dal backtest (circa 1R).
    - Si ferma se il totale in R è ≤ −15,6 + 0,05 × n.
    - C'è evidenza se è ≥ +27,7 + 0,05 × n.
    - Dopo 600 trade senza decisione: «non dimostrata».
    - Le soglie si ricalcolano con la σ vera della strategia.
  - **Simulazione riproducibile** (`laboratorio/studi/simulazione_sprt.py`, seme fisso, output identico su Python 3.13 e 3.9):
    - 6.000 sequenze di trade inventate per ogni livello di vantaggio, con risultati estratti da una normale di dispersione 1R. Non sono strategie reali;
    - senza vantaggio: fermata nell'86,2% dei casi, promossa per errore nel 3,7%, indecisa nel 10,1%;
    - con +0,10R: promossa nel 64,3%, fermata per errore nel 17,1%, indecisa nel 18,6%, 348 trade in media;
    - la vecchia regola (100 trade) lasciava sopravvivere il 39,2% delle sequenze senza vantaggio.
    - Probabilità di passare la fase 1 FTMO: la formula coincide con la simulazione entro circa 2 punti.
  - **Conseguenza:** la demo da sola non dimostra in fretta un vantaggio piccolo: 350 trade a 3 a settimana sono più di 2 anni. Il peso statistico lo porta il backtest lungo (DSR con tutte le prove). La demo verifica la fedeltà e che i risultati non contraddicano il backtest. Più strategie in parallelo accorciano i tempi.
  - **CUSUM:** per controllare se il vantaggio si esaurisce dopo la promozione, più avanti, su FTMO.
- **Da aggiungere (Gemini G-20261113-01, accolto da Claude):**
  - permutation test, ablation e sensibilità dei parametri (±20–30%: la strategia deve reggere);
  - in demo, un arresto sequenziale al posto della regola grezza dei 100 trade;
  - per Fibonacci e order block, ogni variante di tracciamento conta come una prova.

---

## Fonti di questo registro
- `audit/AUDIT-ARCH-20261111/RELAZIONE-AUDIT.md` §5;
- `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/CLAUDE_EVALUATION_OF_GEMINI_COUNTERCHECK_V1.md` §7;
- `TRADING_BRAIN_UNRESOLVED_DECISIONS_V1.md` di Gemini (non archiviato nel Brain: vedi DA-01);
- `CONTINUITA.md`;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md` §8.
