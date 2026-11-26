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
- **Emendamento del titolare (14/11/2026, registrato dal DGS in DGS-20261114-02; recepito qui il 17/11):** le prove di
  robustezza restano fuori da N **solo come veti fissi**, cioè con parametri e soglie scritti nella scheda **prima** dei
  dati. Se una prova di robustezza **orienta una scelta** (quale variante tenere, quale parametro usare, se riprovare),
  l'esclusione **decade** e quella prova **entra in N**. Nel registro delle prove il ruolo «robustezza» vale solo per i
  veti fissi; un uso diverso va registrato come prova selezionabile.

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
- **14/11/2026: l'utente delega a Claude la scelta del broker** e propone Alpaca.
  - **Alpaca: scartato.** Broker USA di azioni, ETF, opzioni e cripto via API; non offre XAUUSD spot né CFD, non usa MetaTrader 5 e non c'entra con FTMO. Sull'oro si arriverebbe solo con un ETF nell'orario della borsa USA. È un dato da conoscenza generale di Claude, da verificare se l'utente insiste.
  - **Scelta di Claude: FP Markets, conto demo MT5 «Raw».** Spread bassi più commissione; MT5, quindi Expert Advisor (DA-30); demo gratuita.
  - **Secondo broker di confronto, più avanti:** IC Markets o Pepperstone (MT5 Raw o Razor).
  - **Costi finali:** quelli che contano sono di FTMO (server MT5 proprio). Si misurano prima delle challenge.
  - Il conto demo da 50.000 USD della scheda attuale non ha un broker noto: la scheda va rifatta sul conto FP Markets.

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
- **Deciso dall'utente il 14/11/2026: INVERSIONE dei ruoli** (proposta di Claude).
  - **Sviluppo:** gli ultimi 3 anni già scaricati, dal 15/11/2023 in poi. Sono già stati visti, quindi vanno bene per sviluppare.
  - **Verifica sigillata:** tutto il periodo dal 2005 a circa il 31/10/2023 (date esatte dopo il conteggio dei buchi), con embargo prima dello sviluppo. Nessuno lo guarda: né i dati, né i grafici, né TradingView.
  - **Test finale:** il futuro, cioè la demo.
  - Motivi: si parte subito; i dati già visti vanno dove la contaminazione non fa danni; la verifica è più lunga (circa 18 anni, molti tipi di mercato) e più cieca.
  - Limiti: lo sviluppo copre un solo tipo di mercato e pochi trade, quindi molte idee falliranno in verifica; il mercato di oggi è diverso da quello del 2005–2012.
  - Sostituisce le strutture A/B/C precedenti (di Claude e di Gemini).
- **TradingView (14/11/2026):** nessun connettore disponibile. Si lavora con screenshot e indicatori Pine scritti da Claude (`laboratorio/tradingview/`).
  - Si guarda solo dal 15/11/2023 in poi; l'indicatore copre il periodo sigillato.
  - Vietato provare idee con lo Strategy Tester di TradingView: sarebbero prove non registrate.
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
- **Aggiornamento del 20/11/2026 (D-34 punto 2, lavoro di Claude):**
  - per il verdetto vale **solo** il registro canonico `laboratorio/registro_prove.json`, già usato dal sigillo e dall'esecutore;
  - i registri di Binario B (`laboratorio/trial_registry.json`, `dati/operativo/trial_registry_xauusd.json`) sono **eredità**: il modulo del verdetto li rifiuta e un test statico vieta che il verdetto o il perimetro di esecuzione li leggano;
  - il verdetto riporta N e l'impronta del registro letto.

  **Resta aperta** la ratifica di N unico su tutti i mercati (D-46).

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
  - **Correzioni dopo la revisione di Gemini G-20261114-01 (verificate da Claude):**
    - la potenza effettiva con il taglio a 600 trade è circa il 64%, non l'80% nominale;
    - l'obiettivo è in Sharpe standardizzato θ1 = μ1/σ = 0,10, con σ presa dal backtest prima della demo (mai stimata sui primi trade): con σ = 2R le soglie in R fisse daranno l'84% di indecise;
    - il controllo di fedeltà riguarda solo esecuzione e attriti (segnali, orari, prezzi, spread, slippage), mai P/L o percentuale di vincite.
    - Proposte ancora aperte: varianza di lungo periodo contro le perdite a grappoli e avvio del test dopo 30–50 trade; due chiavi per passare a FTMO; criterio di discordanza Dukascopy–MT5.
- **Da aggiungere (Gemini G-20261113-01, accolto da Claude):**
  - permutation test, ablation e sensibilità dei parametri (±20–30%: la strategia deve reggere);
  - in demo, un arresto sequenziale al posto della regola grezza dei 100 trade;
  - per Fibonacci e order block, ogni variante di tracciamento conta come una prova.

### DA-30 · Esecuzione automatica della strategia H-001 sul conto demo
**Nota del 14/11/2026:** H-001 è chiusa dopo lo Studio 2. Il percorso di automazione qui sotto resta valido per la prima strategia che supererà i test.
**Deciso dall'utente il 14/11/2026:** la strategia di scalping nei micro-range (H-001) sarà **automatizzata fin dall'inizio** sul conto demo, dopo revisione e test. Non sarà eseguita a mano.

**Proposta di Claude (da confermare):**
- **Strumento:** Expert Advisor in MQL5 su MetaTrader 5. Il pacchetto Python per MetaTrader 5 funziona solo su Windows; l'utente usa un Mac.
- **Percorso, nessun passo saltato:**
  1. Scheda H-001 completata con le risposte dell'utente e **sigillata**.
  2. Spread e commissioni reali misurati sul conto demo (FP Markets).
  3. Motore di backtest a 1 minuto con ordini limite, in Python, scritto da Claude in TDD e rivisto da Gemini.
  4. Backtest sullo sviluppo; se passa i criteri scritti, **una sola** verifica sul periodo sigillato.
  5. **Replica indipendente:** Gemini scrive l'Expert Advisor in MQL5 partendo dalla sola scheda sigillata, senza leggere il codice Python di Claude. I trade dell'Expert Advisor nel tester di MT5 e quelli del backtest Python sullo stesso periodo devono coincidere; ogni differenza è un errore da trovare.
  6. Demo automatica, con controllo di fedeltà nei primi 20–30 trade e test sequenziale di Wald (DA-29).
- **Protezioni dentro l'Expert Advisor** (sono parte della strategia, non del Guardian: D-16 resta invariata):
  - si rifiuta di operare se il conto non è demo (`ACCOUNT_TRADE_MODE_DEMO`);
  - rischio per trade P-01; stop giornaliero P-05; una posizione alla volta (P-06);
  - finestra notizie P-08;
  - numero massimo di trade al giorno;
  - stop obbligatorio su ogni ordine;
  - registro di ogni ordine, da riportare nel journal.
- **Regole personali:** P-11 e P-12 riguardano il trading manuale. Per l'Expert Advisor valgono i suoi limiti scritti; l'utente non interviene a mano sui trade dell'Expert Advisor.
- **Da verificare:**
  - MT5 per Mac del broker con Expert Advisor funzionanti;
  - Mac acceso e collegato nelle ore di trading, oppure un VPS (ha un costo: decide l'utente);
  - regole FTMO sugli Expert Advisor e sulle «pratiche vietate», prima di qualunque passaggio a FTMO.
- **Soldi veri:** mai senza autorizzazione esplicita (D-14).

### DA-31 · Verdetto della verifica: due stati o tre (difetto #94 b, 17/11/2026) · **decisione del titolare, parere del DGS**
- **CHIUSA il 19/11/2026 con D-35:** tre esiti (DGS-10 §4, opzione 2); i «non decidibili» si riprovano solo con dati nuovi (demo).
- **Il problema:** oggi la verifica dà «promossa» o «bocciata». Con meno di 30 trade, o con risultati tutti uguali, il DSR non si può calcolare e la variante risulta «bocciata». Nel registro una strategia scarsa e una che non ha prodotto abbastanza trade sembrano la stessa cosa. Il registro della riserva prevede invece tre esiti: promossa, bocciata, non decidibile.
- **Opzione A, lasciare due stati:** «non stimabile» resta «bocciata». È la scelta più severa. Si perde però l'informazione, e una strategia con pochi trade non può essere riprovata senza contare come prova nuova.
- **Opzione B, tre stati** (promossa / bocciata / non decidibile): «non decidibile» quando il DSR non è calcolabile. In nessun caso promuove. Una riprova costa comunque una nuova prenotazione della riserva e conta in N.
- **Opzione C, tre stati con soglia scritta prima:** come B, ma la scheda dell'ipotesi fissa in anticipo anche il numero minimo di trade attesi. Sotto quel numero l'esito è «non decidibile» e la scheda va rivista come ipotesi nuova.
- **Cosa non cambia in nessun caso:** la verifica si fa una volta sola; «non decidibile» non promuove e non restituisce la riserva consumata.
- **Effetto sul codice:** B e C toccano `criteri.verifica` ed `esegui_h002`; si fanno in TDD prima del primo sigillo.

---

## Fonti di questo registro
- `audit/AUDIT-ARCH-20261111/RELAZIONE-AUDIT.md` §5;
- `collaborazione/da-claude/CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md` §10;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-07-CONTROVERIFICA-GEMINI/CLAUDE_EVALUATION_OF_GEMINI_COUNTERCHECK_V1.md` §7;
- `TRADING_BRAIN_UNRESOLVED_DECISIONS_V1.md` di Gemini (non archiviato nel Brain: vedi DA-01);
- `CONTINUITA.md`;
- `collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/REVISIONE_ESTERNA_TRADING_BRAIN_CHATGPT.md` §8.

### DA-32 · Finestre orarie in cui il titolare può eseguire gli alert (19/11/2026) · **da comunicare dal titolare**
- **Perché serve:** una strategia promossa si esegue con alert sul telefono. Il titolare inserisce l'ordine e il Guardian controlla le regole (D-14, D-16). Se gli alert cadono in ore in cui il titolare non è disponibile, i trade saltati rendono i risultati diversi da quelli collaudati.
- **Uso:** vincolo della scheda H-003. Ogni ipotesi dichiara le sue ore operative; si candidano solo ipotesi compatibili con le finestre del titolare.
- **Stato:** il titolare comunicherà giorni e ore entro circa 10 giorni (19/11/2026).

### DA-33 · Dove gira la prova in avanti quotidiana (20/11/2026) · **da decidere più avanti**
- **Perché serve (D-46):** la prova in avanti simulata richiede che, ogni giorno, qualcosa scarichi i dati nuovi e faccia girare le strategie sigillate.
- **Opzioni da preparare:**
  - il Mac del titolare (oggi ha la batteria guasta ed è l'unico custode dei dati);
  - un computer dedicato sempre acceso;
  - un servizio nel cloud, con costi e custodia dei dati da valutare.
- **Prerequisito:** il motore generico (fase 3 della visione). Non è urgente.

### DA-34 · Potenza esattamente al 50% nello screening (21/11/2026) · **da decidere dal titolare**
**Decisa il 22/11/2026 → D-47.** Il testo sotto resta come storia.
- **Il problema (DGS-12 §2):** D-36 scrive «potenza stimata ≥ 50%», ma nella stessa riga dice «confronti stretti: l'uguaglianza non passa». Il codice, D-42 e la specifica del verdetto usano «≥»: con potenza esattamente 50% la variante passa.
- **Opzioni:**
  - **(a)** «≥ 50%»: il 50% esatto passa. «L'uguaglianza non passa» vale per le soglie in R (media e limite inferiore). Nessuna modifica al codice.
  - **(b)** «> 50%»: il 50% esatto non passa. Si cambia il confronto nel modulo, con test e mutanti.
- **Consiglio di Claude: (a).** È la formula scritta e la lettura di D-42 («potenza del 50%»). Una potenza stimata esattamente al 50,00% è un caso quasi solo teorico, quindi la scelta conta soprattutto per la chiarezza del testo.

### DA-35 · Contatore D-24 dopo R18 (21/11/2026) · **da decidere dal titolare**
**Decisa il 22/11/2026 → D-48.** Il testo sotto resta come storia.
- **Il fatto:** R18 (il giro su tutte le manomissioni) ha trovato tre difetti **importanti** nel perimetro sigillato, di tipo E/M e costo basso:
  - #125: copia parziale del repository non vista;
  - #126: ASK uguale al BID accettato;
  - #127: riserva non collegata all'esecutore.
- Sono difetti che avrebbero contato anche in R16 e R17. Le correzioni cambiano il perimetro, quindi serve un **nuovo candidato**.
- **Opzioni:**
  - **(a) Rigorosa:** contatore a 0 su 2 sul nuovo candidato. Servono due giri ordinari puliti più un giro sulle manomissioni. Costa circa 3 giri (1–2 settimane).
  - **(b) Come D-27 (#114):** il contatore resta 2 su 2. Il prossimo giro (R19) rifà sul nuovo candidato tutte le prove toccate dalle correzioni **e** l'intero giro sulle manomissioni (D-24); se è pulito, la condizione D-24 è soddisfatta. Costa 1 giro.
  - **(c) Intermedia:** contatore a 1 su 2 (R17 resta valido, R16 no). R19 è un giro ordinario completo più le manomissioni, e se è pulito si arriva a 2 su 2. Costa 1 giro, ma più lungo di (b).
- **Consiglio di Claude: (c).**
  - I tre difetti sono di classe «facile» (E e M a costo basso), proprio quella che il contatore deve garantire. Quindi (b) sarebbe troppo indulgente: R16 e R17 non li hanno visti.
  - (a) ripete lavoro già fatto bene sul resto del perimetro, che non cambia.
  - Con (c) R19 rifà tutto il perimetro, non solo le prove toccate.

### DA-36 · Protezione del ramo su GitHub (21/11/2026) · **da decidere dal titolare (D-24)**
**Decisa il 22/11/2026 → D-49.** Il testo sotto resta come storia.
- **Opzioni preparate da Gemini** (R18, compito D; `collaborazione/da-gemini/G-20261121-R18.md`):
  1. **Minima:** niente push forzati né cancellazioni; i test automatici obbligatori; scavalcamento possibile per il titolare.
  2. **Con revisione:** come la 1, più modifiche solo tramite richiesta di unione (PR) e approvazione del titolare per i file della CI, il perimetro, il verdetto e i registri (CODEOWNERS).
  3. **Rigida:** come la 2, senza scavalcamento nemmeno per il titolare, storia lineare ed etichette `sigillo-*` e `riserva-*` non modificabili.
- **Che cosa NON copre nessuna opzione:** il repository e i registri **locali** prima del push (#90, #98), la cache dei dati (fuori da GitHub, #129), `avvio.py` modificato sul Mac.
- **Consiglio di Claude: la 2, con le etichette `sigillo-*` e `riserva-*` protette della 3.**
  - Ferma il caso più probabile: un agente che modifica test, CI o registri e li fa entrare senza che il titolare lo veda.
  - Lascia al titolare lo scavalcamento per le urgenze, che resta comunque registrato.
- **Limite da verificare:** in un repository personale l'approvazione richiesta non può venire dall'autore stesso. Va controllato se serve un secondo account o se bastano le regole dei Ruleset.

### DA-37 · Dove si registra il rifiuto per quota non collaudata (22/11/2026) · **da decidere dal titolare**
**Decisa il 22/11/2026 → D-50.** Il testo sotto resta come storia.
- **Il caso:** la prima verifica usa la quota 2,5% (una variante, prima apertura), l'unica collaudata. Se una richiesta arriva a una quota diversa (per esempio 1,25% con due varianti, o 0,83% alla seconda apertura), il percorso si ferma **prima** di autorizzare e di leggere i dati (DGS-13 §A). Serve una traccia verificabile del rifiuto.
- **Opzioni (DGS-14, Q2):**
  - **(i)** un evento nuovo «rifiutata per quota» nel registro della riserva, legato alla prenotazione. Contiene: identità della richiesta, impronta della scheda, finestra, j previsto, m, quota calcolata e quota collaudata, motivo. Non spende date né quota e non crea una prova N. Cambia lo schema del registro (`riserva/1` → `riserva/2`) e quindi il perimetro.
  - **(ii)** una riga nel registro delle prove. Quel registro però conta N, e il rifiuto non è una prova.
  - **(iii)** solo nel rapporto. Il rapporto può mancare proprio quando il percorso si ferma.
- **Consiglio del DGS e di Claude: (i).** È l'unica traccia che resta legata alla prenotazione e che un revisore può ricostruire anche dopo un riavvio. Il costo è un cambio di schema, con test e mutanti, che entra comunque nel nuovo candidato di R19.

### DA-38 · Che cosa fare della verifica nel vecchio esecutore di H-002 (22/11/2026) · **da decidere dal titolare**
**Decisa il 22/11/2026 → D-51.** Il testo sotto resta come storia.
- **Il fatto (#127):** oggi `esegui_h002 --modalita verifica` legge la riserva 2005 → FINE_VERIFICA senza passare dal registro della riserva (né prenotazione, né autorizzazione, né quota) e decide con i criteri annuali di H-002. D-37 aveva lasciato quei criteri «nel perimetro attuale: valgono per H-002». Il nuovo esecutore ordinario (`esegui_verifica`) rifiuta la vecchia scheda di H-002 prima di ogni autorizzazione, come raccomanda DGS-14 Q3, ma il vecchio comando esiste ancora.
- **Opzioni:**
  - **(a) Disattivare la verifica di `esegui_h002`:** resta solo lo sviluppo. La verifica passa soltanto dal percorso ordinario D-31 con una scheda H-003. Se H-002 dovesse mai andare in verifica, servirebbe una scheda H-003 nuova, cioè un'ipotesi nuova. Costo: riscrivere circa 20 test e togliere i mutanti del ramo di verifica; cambia il perimetro (entra in R19).
  - **(b) Collegarla alla riserva:** la verifica di H-002 resta con i suoi criteri annuali, ma passa da prenotazione, quota e autorizzazione come il percorso nuovo. Costo alto: due percorsi di verifica da mantenere e da rivedere, e due regole di decisione diverse.
  - **(c) Lasciarla com'è:** sconsigliato. È il difetto #127: un comando legge tutta la riserva senza lasciare traccia nel registro.
- **Consiglio di Claude: (a).** Un solo percorso, che è quello collaudato (D-31), e nessuna lettura della riserva fuori dal registro. H-002 non è oggi una candidata: lo sviluppo ne resta come riferimento.

### DA-39 · D-49 con il piano GitHub Free (22/11/2026) · **da decidere dal titolare**
- **Il fatto:** il titolare ha il piano **GitHub Free** (22/11). Su un repository **privato** personale con Free non ci sono né rulesets, né protezione dei rami, né CODEOWNERS (verificato da Gemini sulla documentazione di GitHub, notte del 22/11). Quindi **D-49 oggi non si può applicare**: nessuna protezione è attiva.
- **Opzioni:**
  - **(a) Passare a GitHub Pro**, circa 4 USD al mese, e applicare D-49 con le istruzioni di Gemini (`G-20261122-NOTTE.md`, §B.5).
  - **(b) Rendere pubblico il repository:** sconsigliato. Contiene la storia delle decisioni, i registri e il lavoro sulle fonti; i dati veri restano comunque fuori da GitHub.
  - **(c) Restare su Free senza protezione lato server**, con le difese che ci sono già: registri ancorati a GitHub, impronte del codice sigillato, test automatici che segnalano (senza bloccare), riproduzione indipendente di Gemini e del DGS.
- **Consiglio di Claude:** (c) **finché il lavoro è sintetico**, poi (a) **prima del primo accesso reale alla riserva**. La protezione serve quando c'è qualcosa di irreversibile da proteggere, cioè le date della riserva e i sigilli veri. Il costo, intorno ai 50 USD l'anno, è piccolo rispetto al rischio di una verifica non attribuibile.

### DA-40 · Ambiente di riferimento del risultato ufficiale (23/11/2026) · **DECISA: (b), D-54**
- **Il fatto:** sul candidato le due versioni di Python dei test automatici (3.13 e 3.9) danno lo stesso verdetto, la stessa media bit per bit e la stessa impronta dell'impegno. **L e U invece differiscono di 102 ulp**, circa 5,7e-15 R, per via della somma del pilota congelato. Le decisioni sono prese in frazioni esatte (#124), quindi oggi non cambiano. Resta però da dire **quale ambiente produce il numero ufficiale** (DGS-16 e DGS-17 Q1).
- **Opzioni:**
  - **(a)** L'ambiente Linux del collaudo IA-02, se dai suoi artefatti si ricostruiscono interprete esatto, architettura, dipendenze, codice, semi e configurazione, e vi si riproducono i riferimenti congelati.
  - **(b)** Una sola immagine dei test automatici, riproducibile (sistema, Python e versione esatti), qualificata rieseguendo i riferimenti congelati del collaudo IA-02 e documentando le differenze.
  - **(c)** Il Mac del titolare (Python 3.9): sconsigliato. La versione cambia con gli aggiornamenti di sistema e l'ambiente non si ricostruisce altrove.
- **In ogni caso:** l'identità dell'ambiente che calcola va registrata nell'impegno, separata dalla macchina da cui il titolare lancia la richiesta. L'altra versione e il Mac restano prove di portabilità.
- **Consiglio di Claude:** **(b)**. Il collaudo IA-02 l'ho eseguito io in un contenitore temporaneo, di cui oggi si conoscono la versione di Python e la piattaforma, ma non un'immagine ricostruibile. Per (a) mancherebbe proprio la prova di ricostruzione che il DGS chiede.
- **Fonte:** DGS-17 Q1; RICEVUTA-127 §4.

### DA-41 · Autorizzazione su GitHub prima della lettura dei dati (23/11/2026) · **DECISA: (a), D-55**
- **Il fatto:** oggi l'esecutore scrive l'autorizzazione nel registro della riserva sul disco e **subito dopo legge la finestra**. Il commit e il push vengono dopo.
  - Se fra la lettura e il commit il registro locale venisse riportato indietro (per errore o sotto pressione), la lettura non lascerebbe traccia.
  - La stessa finestra si potrebbe poi leggere di nuovo, con un'altra scheda.
  - L'ancora e la storia git proteggono solo ciò che è già su GitHub. È il limite dichiarato #90/#98, e vale anche per il percorso nuovo.
- **Opzioni:**
  - **(a) Lettura solo dopo la pubblicazione.**
    1. L'esecutore scrive l'autorizzazione e si ferma.
    2. Il titolare (o il lanciatore) fa commit e push.
    3. Una seconda chiamata, con lo stesso impegno, legge i dati solo se l'ancora conferma che l'autorizzazione è già nella versione remota.

    Tecnicamente è la ripresa che esiste già, più un controllo. Costa un passo in più per ogni verifica.
  - **(b) Lasciare com'è**, con la regola scritta «commit e push subito dopo ogni verifica». Più semplice, ma si affida alla disciplina.
- **Consiglio di Claude:** **(a), prima del primo accesso reale.** Va scritta in TDD, con i mutanti, e portata in un giro di revisione. Con il piano Free (DA-39) è la difesa più forte disponibile senza costi.
- **Fonte:** revisione critica di Claude del 23/11 (`laboratorio/ricevute/2026-11-23-candidato-r19/REVISIONE-CRITICA-20261123.md`, punto B.1).

### DA-42 · Criterio d'uscita dal Gate 2½ (riscrittura di D-24), da fissare PRIMA dei risultati di R19 (23/11/2026) · **da decidere dal titolare**
- **Il problema** (chat di Claude e Claude, `governance/CONVERGENZA-REVISIONI-20261123.md`):
  - D-24 chiede due giri senza critici né importanti, su un perimetro che continua a crescere;
  - ogni correzione è codice nuovo, quindi anche un «congelamento» continua a produrre materiale da rivedere;
  - la proposta di congelamento del 23/11 non diceva se una correzione durante i giri riapre il contatore.
- **Proposta della chat di Claude:** uscita con «zero critici per K giri consecutivi, di cui almeno uno su tutte le manomissioni»; gli importanti diventano un elenco dichiarato, non un blocco. Motivo: lo scopo del gate è che la macchina non lasci passare un risultato falso, cioè la famiglia dei critici.
- **Controllo di Claude sulla premessa** [DEDOTTO dalle descrizioni nel registro dei difetti, lette per i 14 importanti dal 18/11]:
  - per definizione del registro, «importante» = **può cambiare un verdetto in alcune configurazioni**: non è solo qualità del software;
  - per **direzione dell'errore**, dei 14 importanti dal 18/11:
    - **10 sono permissivi**, cioè potevano far passare qualcosa che non doveva passare: #124 (decisioni invertite a filo), #125 (prenotazione consumata riusabile), #126 (spread a zero: R medio da −0,31 a +0,22 su un mercato inventato), #127 (tutta la riserva letta in una verifica), #131 (intervallo invalido presentato come stima valida), #132 (seme libero), #133 (N manipolabile), #135 (CI verde senza test), #138 e #139 (seconda lettura della riserva);
    - **3 sono prudenti**, cioè bloccavano o rifiutavano: #122, #123, #142;
    - **1 è di coerenza fra i registri:** #140;
  - con il solo criterio «zero critici», il gate si sarebbe potuto chiudere il 20/11 con #125, #126, #131–#133 e #139 ancora aperti.
- **Autocritica di Claude:** le gravità le assegnano Claude e Gemini, cioè chi scrive e chi rivede, senza un arbitro. #126 rientra alla lettera nella definizione di «critica» («fa sembrare una strategia migliore di quanto è») ed è stato classificato importante. Quindi anche il dato «zero critici dal 18/11» è più debole di come l'ho presentato.
- **Opzioni:**
  - **(a) D-24 com'è**, con l'ultimo lotto e il congelamento. Rischio: nessuna data d'uscita.
  - **(b) Proposta della chat:** zero critici per K giri; importanti dichiarati. Rischio: lascia aperti difetti che possono far passare un risultato falso o spendere la riserva.
  - **(c) Proposta di Claude, la direzione dell'errore:**
    1. **Bloccanti:** i critici e gli importanti **permissivi**, cioè quelli che possono produrre una promozione o un verdetto falso, una lettura della riserva fuori registro, o un risultato non riproducibile.
    2. **Non bloccanti:** gli importanti **prudenti** (bloccano, rifiutano, danno un errore con il consumo conservato) e i minori. Vanno in un elenco dichiarato, nel rapporto, e si correggono a lotti.
    3. **Uscita:** 2 giri consecutivi senza bloccanti, di cui almeno uno su tutte le manomissioni.
    4. **Correzioni durante i giri:** ogni correzione fa un candidato nuovo. Quella di un bloccante **riapre il contatore**; quella di un non bloccante no, ma la sua differenza entra nel giro successivo.
    5. **Limite vincolante:** dopo 4 giri dal congelamento senza uscita, ci si ferma. Il titolare decide se dichiarare i limiti con l'elenco o cambiare approccio, senza un quinto giro automatico.
    6. **Classificazione:** chi trova il difetto propone gravità e direzione; Claude non classifica da solo i propri difetti; nei casi contestati sente il DGS e decide il titolare (come in D-24).
    7. **Fissato adesso**, prima dei risultati di R19: la stessa disciplina delle ipotesi.
- **Parere del DGS (DGS-19, 25/11):**
  - (a) è applicabile su un perimetro congelato;
  - (b) dipende troppo da chi assegna l'etichetta «critico»;
  - (c) è sostenibile **con un criterio verificabile per il rinvio**.

  Il DGS contesta anche la mia etichetta «prudenti» per #122 e #123: trasformare una bocciatura in un esito riprovabile, o far bloccare un requisito descrittivo, **cambia una decisione**. E #140 riguarda la coerenza dell'esito e del consumo, che è una condizione d'uscita.
- **(c′) Opzione (c) emendata dal DGS, oggi la proposta di Claude:**
  1. **Scheda per ogni difetto:**
     - caso concreto;
     - esito atteso e osservato;
     - conseguenza sul verdetto o su un nuovo tentativo;
     - effetto su autorizzazione e consumo;
     - riconciliazione dei registri;
     - disponibilità del percorso valido;
     - prova associata al candidato.
  2. **Bloccante:** ogni difetto che viola una di queste proprietà nel perimetro del gate. **Rinviabile** solo un rifiuto prudenziale circoscritto che conserva lo stato corretto, il cui recupero è provato e che lascia esercitabile il percorso valido. Se l'impatto è incerto, il giudizio resta aperto.
  3. **Condizione d'uscita in più:** una richiesta valida deve poter completare il percorso ordinario, e ogni esito deve produrre il seguito previsto dalle regole. Lo prova un test positivo completo; #142 mostra perché serve.
  4. **Perimetro congelato**, esplicitato prima del giro a cui si applica. Servono 2 giri puliti consecutivi, di cui uno su tutte le manomissioni.
     - La correzione di un bloccante riavvia il contatore.
     - Ogni modifica successiva all'ultima prova ha una verifica d'impatto sul candidato finale.
     - **Stop dopo 4 giri** senza uscita, con decisione del titolare.
  5. **Classificazione:** chi trova il difetto propone gravità e conseguenze; il revisore indipendente verifica la prova, non solo l'etichetta. Se concordano basta la loro traccia. Se il dissenso incide sull'uscita, il DGS esplicita l'interpretazione e il titolare decide.
  6. **Nessun credito retroattivo al contatore** da questo parere.
- **Che cosa si sapeva di R19 al momento della scelta** (DGS-19 chiede di registrarlo), al 26/11. Gemini lavora sul candidato **`1431190`**. Dai suoi messaggi di avanzamento, riportati dal titolare:
  - mutanti 57/58 (percorso), 131/132 (verdetto), 95/96 (N,K: N63 vivo sul Python di Apple, caso #106 noto), 71/71, 62/62;
  - una sonda **R19-04** su una «doppia verifica completa su un ramo divergente», con α totale e m manipolati. Il contenuto non è consegnato né riprodotto.

  **L'esito di R19 non è noto.** Se il titolare decide prima della consegna di Gemini, il criterio vale per la chiusura di R19 sul candidato finale. Se decide dopo, vale dal giro successivo (DGS-19).
- **Consiglio di Claude (aggiornato al 26/11): (c′),** decisa **prima** che Gemini consegni R19. Versione originale del consiglio: (c). Prende dalla chat il punto giusto (l'uscita deve dipendere dal rischio di un risultato falso, non dalla qualità del codice), ma non tratta come innocui difetti che per definizione possono cambiare un verdetto. Prima di decidere conviene il parere di metodo del DGS (messaggio 18).
