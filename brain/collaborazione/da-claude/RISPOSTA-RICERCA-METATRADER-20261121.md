# Risposta di Claude alla richiesta «Storici MetaTrader, strumenti per Claude e osservazione continua» (21/11/2026)

**Richiesta:** `collaborazione/da-chatgpt/DGS-20261121-richiesta-ricerca-metatrader-claude.md`.

**Come si manda:** si incolla il testo fra le due righe di trattini.

**Etichette:**
- [FATTO · fonte] = letto da Claude in una fonte, indicata;
- [FATTO · secondario] = da una fonte non ufficiale;
- [DEDOTTO];
- [IPOTESI];
- [OPINIONE];
- [NON VERIFICATO] = conoscenza di Claude, non controllata oggi sulla fonte ufficiale.

---

RISPOSTA DI CLAUDE — ricognizione documentale. Nessuna implementazione, acquisto o collegamento.

LIMITE PRINCIPALE DI QUESTA RICOGNIZIONE (da leggere per primo)
- Le quattro pagine ufficiali di MetaQuotes (metatrader5.com e mql5.com) **non sono raggiungibili** dall'ambiente di Claude: la rete le blocca e un secondo tentativo è stato negato dal controllo dei permessi.
- Quindi tutto quello che riguarda MQL5 Signals e i server MCP di MT5 è [FATTO · secondario] o [NON VERIFICATO].
- Le due fonti di Anthropic invece sono state lette.
- L'azione documentale proposta in fondo serve a chiudere questo buco.

VERDETTO IN DIECI RIGHE
1. Oggi bastano gli strumenti esistenti. Nessuna di queste integrazioni sblocca un passo della roadmap prima della fine della macchina (D-33, D-34).
2. Gli storici MQL5 mostrano decisioni eseguite, non regole. Senza lo stop iniziale il rendimento in R del trader è indeterminato. Sono utili per generare domande, non per provarle.
3. Il loro uso migliore è una coorte seguita in avanti, scelta con una regola scritta oggi: evita la selezione dei sopravvissuti, che sugli storici passati non si può correggere.
4. MT5 con MCP serve solo nella fase demo (D-45): per riconciliare il simulatore con il conto. Non serve alla ricerca, e la baseline resta Dukascopy BID/ASK.
5. Collegare il conto per gli ordini va fatto in sola lettura, con un doppio blocco: sul terminale e con le regole di permesso di Claude Code. L'invio di ordini non è autorizzato (D-45).
6. I plugin finanziari di Anthropic servono alla finanza istituzionale (DCF, comparabili, KYC): per noi sono da scartare.
7. «L'impostazione di trading per Claude» dell'amico non è identificata. Il candidato più probabile è una delle guide «Claude + MT5 via MCP».
8. Il limite misurabile più concreto è hardware: il disco del Mac si è riempito due volte e la batteria guasta interrompe gli scaricamenti. Prima dell'acquisto c'è un'alternativa gratuita.
9. Per l'osservazione continua la scelta più economica è un controllo deterministico programmato, per esempio su GitHub Actions. Un agente interviene solo sugli eventi.
10. L'obiezione più forte, in fondo, è la dispersione: ogni fonte nuova apre lavoro prima che la macchina sia finita.

MATRICE
| Idea | Problema risolto | Fatto verificato e fonte | Cosa resta da provare | Fase e dipendenza | Costo | Verifica di utilità | Decisione proposta |
|---|---|---|---|---|---|---|---|
| 1. Coorte prospettica di segnali MQL5 su XAUUSD | Generare ipotesi senza sopravvissuti | Nessuno sulla fonte ufficiale (blocco di rete). [FATTO · secondario] le pagine pubbliche mostrano lo storico con orari, simbolo, volume e prezzo | Termini d'uso, campi visibili, ritardi, stop iniziale | Ricerca, dopo D-34 punto 7 | 0 €; ~2 ore oggi e ~2 ore a +3/6 mesi | % di segnali in cui lo stop iniziale è ricostruibile | **Dopo una condizione:** leggere le regole ufficiali |
| 2. Lettura manuale di storici accanto ai video di Brad | Regola dichiarata contro decisioni eseguite | Brad: nessun segnale MQL5 noto. [DEDOTTO] il confronto vale solo se lo stesso trader pubblica entrambi | Esiste un conto pubblico di Brad? | P-001, dopo R18 | Tempo umano | Coincidenza fra trade del video e trade dello storico | **Dopo una condizione:** un conto verificabile |
| 3. MT5 con MCP collegato a Claude Code in sola lettura | Riconciliare demo e simulatore (G0, DA-25) | [FATTO · secondario] MT5 ha un assistente interno e un server MCP locale con chiave; Claude Code si collega via HTTP | Elenco ufficiale degli strumenti, sola lettura imponibile, Mac | Demo (D-45); oggi la demo è MT4 | 0 € software; API a consumo se si usa l'assistente interno | Scarti di prezzo, spread e orari fra estratto e simulatore | **Dopo una condizione:** conto demo MT5 e pagine ufficiali lette |
| 4. Assistente interno di MT5 con Anthropic come fornitore | Analisi dentro il terminale | [NON VERIFICATO] Anthropic fra i fornitori | Fornitori ammessi, permessi | — | Chiave API a consumo, separata dagli abbonamenti Claude | — | **Da scartare per ora:** duplica Claude Code con permessi più larghi |
| 5. Plugin «Claude for Financial Services» | Ricerca finanziaria | [FATTO · Anthropic, 05/05/2026, e repository anthropics/financial-services, Apache 2.0] 10 agenti per banche, gestori e assicurazioni (pitch, DCF, KYC…); nessuna esecuzione, nessun MT5, forex o backtest; connettori spesso a pagamento | — | — | Connettori a pagamento | — | **Da scartare** |
| 6. Esportazione locale dell'estratto conto (HTML/CSV dal terminale) | Riconciliazione senza integrazione | [NON VERIFICATO, ma comune] MT4 e MT5 esportano il resoconto | Formato del broker | Demo | 0 € | Stesso controllo dell'idea 3 | **Applicabile ora** per la riconciliazione del G0 |
| 7. Osservatore deterministico programmato (GitHub Actions con cron) | Mac spento o in sospensione; buchi nei dati | [FATTO · progetto] i test automatici su GitHub funzionano dal 20/11 (test.yml); [IPOTESI] minuti gratuiti sufficienti | Dukascopy risponde da GitHub? Licenza: contare e non conservare | Dopo la fine della macchina; prima della prova in avanti (DA-33) | 0 € | % di giorni controllati senza intervento, falsi allarmi | **Dopo una condizione:** decisione su DA-33 |
| 8. Disco esterno SSD | Disco pieno (2 volte) e seconda copia dei dati (D-39) | [FATTO · progetto] disco pieno il 19/11 e il 21/11; D-39 | Che basti liberare spazio | Subito dopo il consuntivo ASK | [IPOTESI] 60–120 € una tantum | Nessun fermo per disco pieno in un mese | **Applicabile ora**, dopo l'alternativa gratuita |
| 9. Rivedere i grafici in TradingView per annotare i trade di Brad | Catalogo P-001 | [NON VERIFICATO] il replay intraday richiede un piano a pagamento | — | P-001 | [IPOTESI] 15–30 €/mese | Trade catalogati all'ora | **Dopo una condizione:** la prova su 10 video di Gemini |
| 10. VPS o mini-PC sempre acceso | Prova in avanti 24/7 | — | — | DA-33 | [IPOTESI] 5–15 €/mese o 150–300 € | — | **Dopo una condizione:** il motore generico (fase 3) |

1. STORICI DEI FORNITORI DI SEGNALI
1a. Che cosa si vede. Tutto [NON VERIFICATO] tranne dove indicato.
- Sul conto del fornitore ci sono tutti gli ordini (ingresso, uscita, SL e TP con le modifiche, swap, commissioni, depositi). Il servizio ne mostra una parte.
- Il visitatore vede in genere:
  - crescita, saldo ed equity;
  - drawdown;
  - storico delle operazioni chiuse, con orari del server del broker, simbolo, volume e prezzi [FATTO · secondario, goldenviperea.com];
  - statistiche aggregate, fra cui una quota di «trading algoritmico» e la distinzione fra conto reale e demo.
- Le posizioni aperte e gli ordini pendenti possono essere nascosti o mostrati con ritardo a chi non è abbonato.
- Lo stop **iniziale** e le sue modifiche sono il campo più incerto: spesso non sono visibili.
- La storia precedente alla pubblicazione e il periodo monitorato si distinguono dalla data di avvio del monitoraggio. Va controllato sulla pagina ufficiale.
- Lettura manuale: [IPOTESI] lecita. Raccolta automatica e riuso: probabilmente vietati dai termini di MQL5.com. Fino alla verifica, **nessuno scraping**.
- I segnali rimossi sono di solito irrecuperabili. Da qui la coorte prospettica.

1b. Ingressi long su oro a prezzi sempre più bassi. [DEDOTTO] Che cosa discrimina le spiegazioni:
- **Ordini frazionati pianificati:** volumi uguali o decrescenti; ordini limite piazzati prima che il prezzo arrivi (se è visibile il tipo d'ordine); uno stop comune; chiusura insieme o a scalare.
- **Griglia:** distanze fisse in prezzo; volumi costanti o in progressione geometrica (martingala); ingressi quasi istantanei, quindi algoritmici; nessuno stop per ordine; chiusura del paniere a un profitto comune.
- **Aumento del rischio su una perdita:** ordini a mercato dopo un movimento contrario; volumi crescenti; intervalli irregolari; perdita aperta grande prima della chiusura (equity contro saldo).
- **Resta inconoscibile:**
  - l'intenzione;
  - il budget di rischio;
  - gli ordini pendenti cancellati;
  - gli altri conti dello stesso autore;
  - le **astensioni**: un giorno senza trade non dice se il setup mancava o se il trader l'ha saltato.

1c. Senza lo stop iniziale.
- Restano usabili:
  - il P/L in denaro e in punti per lotto;
  - durata, orario e frequenza;
  - esposizione massima e perdita aperta;
  - la sequenza dei volumi.
- Il rendimento in R resta **indeterminato**, perché R è il denominatore che manca. Uno stop modificato dopo l'ingresso falsa anche quello ricostruito.
- [OPINIONE] Usare la perdita massima realizzata come «R» gonfia le strategie a griglia.

1d. Accanto a Brad.
- Il video suggerisce una regola dichiarata, per esempio «sweep della liquidità, poi rottura di struttura».
- Uno storico mostrerebbe le decisioni eseguite: orari, prezzi, astensioni apparenti.
- La somiglianza visiva fra un grafico del video e un trade dello storico non identifica la regola. Serve che la regola, scritta prima, **preveda** i trade dello storico meglio di un controllo casuale con gli stessi orari e lo stesso lato.
- Applicabile solo se lo stesso trader pubblica un conto verificabile.

1e. Campionamento scritto prima dei risultati (sulla carta).
- **Popolazione:** tutti i segnali MT5 con XAUUSD fra i simboli principali, visibili nella data X.
- **Strati:** quantili di crescita, inclusi i perdenti, e l'attività. Gli inattivi si contano.
- **Estrazione:** casuale con un seme dichiarato, 30 segnali. Per ogni autore si tiene un solo conto, e gli altri si annotano.
- **Si registrano:** conto reale o demo, quota algoritmica, leva, spread del broker.
- **Coorte prospettica:** si rilegge a +3 e a +6 mesi. Si contano i rimossi, che sono informazione e non vanno esclusi.
- **Confronto capace di smentire:** un'idea estratta dalla coorte, per esempio «gli ingressi nella prima ora di Londra rendono più del resto». Si confronta con il controllo casuale per orario sugli stessi segnali. Se la differenza non supera il rumore nella metà della coorte non usata per trovarla, l'idea cade.
- **Fasi:**
  - scoperta: storici e coorte, materiale esplorativo che si dichiara nel §0 della scheda;
  - registrazione preventiva: scheda e varianti sigillate;
  - verifica indipendente: la nostra riserva o la demo futura.
- **Conteggio:** la lettura documentale di oggi non entra in N. N cresce quando una variante con parametri definiti viene eseguita su dati di sviluppo ed è selezionabile, secondo le regole del registro delle prove.

2. CLAUDE E METATRADER
- **(a) Assistente interno di MT5.**
  - Da Strumenti > Opzioni > AI Assistant si scelgono fornitore, chiave API, modello e permessi (trading, web, shell) [FATTO · secondario, trasignal.com].
  - Anthropic fra i fornitori: [NON VERIFICATO].
  - Fatturazione: una chiave API Anthropic si paga a consumo ed è separata dagli abbonamenti a Claude [NON VERIFICATO oggi sulla pagina dei prezzi].
- **(b) Claude Code come client MCP esterno.**
  - Il terminale espone un server MCP locale con indirizzo e chiave. Claude Code si collega in HTTP con un'intestazione di autorizzazione [FATTO · secondario].
  - I tre server (marketdata, terminal, metaeditor) e i loro strumenti: [NON VERIFICATO].
  - Deduzione dai nomi:
    - marketdata legge quotazioni e barre del **feed del broker**;
    - terminal legge il conto e potrebbe gestire ordini;
    - metaeditor crea, modifica e compila file.
  - **Sola lettura:**
    - lato terminale, con i permessi dell'assistente, se esistono per l'MCP [NON VERIFICATO];
    - lato Claude Code, con regole di permesso che negano gli strumenti d'ordine e di scrittura dei file. È un meccanismo documentato di Claude Code.
    - Doppio blocco, e nessuna esecuzione automatica (D-45).
  - **Mac:** MT5 per Mac esiste [NON VERIFICATO se l'MCP ci funziona]. I server MCP di terzi in Python usano il pacchetto MetaTrader5, solo Windows [FATTO · secondario, GitHub].
  - **Per identificare l'ambiente del titolare:** versione e build del terminale (Aiuto > Informazioni), piattaforma (oggi la demo è MT4: niente MCP) e piano Claude. Dalla build dipende la presenza del menu.
- **(c) Plugin finanziari di Anthropic:** visti sopra. Sono per la finanza istituzionale; da scartare.
- **Prodotto terzo:** ci sono vari server MCP open source per MT5 (P7AC1D/mt5-mcp, ariadng/metatrader-mcp-server), quasi tutti con l'invio di ordini. Il nome usato dall'amico resta sconosciuto.
- **Un uso che giustifica l'integrazione:** nella demo MT5 si leggono gli ordini eseguiti e i tick del broker per misurare spread, slittamento e orari contro il simulatore. Sono la riconciliazione del G0 e la misura dei costi.
- **Quando basta un file locale:**
  - l'estratto conto esportato, per la riconciliazione mensile;
  - il calendario delle festività, come file statico.
  - Un feed generico non sostituisce la baseline BID/ASK di Dukascopy, che resta il riferimento della ricerca.

3. STRUMENTI E OSSERVAZIONE CONTINUA
Colli di bottiglia documentati:
- disco pieno (19/11 e 21/11);
- Mac con batteria guasta, che si addormenta e interrompe gli scaricamenti;
- dati con un solo custode (D-39);
- corse lunghe di Gemini che competono con gli scaricamenti;
- limite d'uso di ChatGPT;
- YouTube bloccato nel cloud per P-001;
- prova in avanti futura senza una macchina sempre accesa (DA-33).

Tre opzioni per l'osservazione:
- **(i) Avvisi o controlli programmati:** il più semplice.
- **(ii) Raccolta persistente deterministica:** script con registro, come `scarica_cache`.
- **(iii) Agente solo su evento:** l'agente legge il registro e scrive al titolare. Costa crediti solo quando c'è un evento.

[OPINIONE] Si combinano (ii) e (iii). Un agente sempre acceso è da scartare.

Esempio su XAUUSD, [DEDOTTO]:
- **Mercato chiuso o interruzione:**
  - un calendario atteso, con le ore di apertura del feed, la pausa giornaliera e le festività, dice quando i tick **dovrebbero** esserci;
  - dentro l'apertura attesa, nessun tick per più di k minuti è un'interruzione; k è il 99° percentile dei buchi storici per quell'ora, già misurabile con `intersezione_bid_ask`;
  - controprova con una seconda fonte (il feed del broker), se disponibile.
- **Chi registra:** lo script, in un registro a sola aggiunta: ora UTC, ora, esito, byte, impronta. È lo schema di `scarica_cache`.
- **Dopo un riavvio:**
  - tempi strettamente crescenti per file;
  - impronta per ora;
  - riconto delle ore attese contro quelle presenti.
  - Un duplicato è un'ora con due impronte diverse.
- **Quando avvisare il titolare:** solo quando un buco invalida una seduta della prova in avanti, oppure dopo N giorni senza dati. Non per ogni buco.
- **Mac spento o in sospensione:** la raccolta deve girare altrove, su GitHub Actions o su un VPS. Il Mac recupera e controlla al risveglio.
- **Misure di utilità:**
  - falsi allarmi su un mese, contro un controllo manuale;
  - giorni coperti senza intervento;
  - chiamate all'agente e crediti consumati.
- **Ricercatori indipendenti:**
  - chi propone (Claude) scrive l'ipotesi e un quesito;
  - chi verifica (Gemini) prova a falsificarla alla cieca, sulla scheda sigillata;
  - ognuno pubblica l'**impronta** dei propri risultati prima di vedere quelli dell'altro (impegno, poi rivelazione);
  - cartelle e rami separati, nessuno scambio prima che entrambe le impronte siano registrate.

LE TRE MIGLIORI PER BENEFICIO E COSTO
- **A. Spazio e seconda copia (idea 8).**
  - Prova più economica: prima liberare spazio senza spendere (~10 GB di copie e video in Download), poi un mese di osservazione.
  - Confronto: fermi per disco pieno prima e dopo.
  - Misura: numero di fermi e spazio libero minimo giornaliero.
  - Si abbandona l'acquisto se in un mese non c'è nessun fermo e D-39 si soddisfa con un disco già posseduto.
- **B. Osservatore programmato su GitHub Actions (idea 7).**
  - Prova più economica: per 30 giorni un job giornaliero che **conta** le ore del giorno prima disponibili su Dukascopy, senza conservare dati.
  - Confronto: con il calendario atteso.
  - Misura: % di giorni completati senza intervento, falsi allarmi, minuti consumati.
  - Si abbandona se Dukascopy rifiuta le richieste da GitHub o se più del 10% delle esecuzioni fallisce per motivi esterni.
  - Richiede una decisione: dati del mercato e GitHub.
- **C. Coorte MQL5 (idea 1).**
  - Prova più economica: lettura manuale di 30 pagine scelte con la regola del §1e.
  - Confronto: quanto si ricostruisce lo stop iniziale e quanto si distinguono griglia, frazionamento e aumento del rischio.
  - Misura: % di segnali con stop iniziale ricostruibile.
  - Si abbandona se è sotto il 20%: lo storico non dà R e resta utile solo per statistiche di sopravvivenza.

UNA SOLA AZIONE DOCUMENTALE UTILE ORA
Il titolare salva in PDF, dal suo browser, le quattro pagine ufficiali (signal_monitoring, signals/rules, mcp_and_ai/configuration, mcp_and_ai/capabilities) e le passa a Claude. Claude sostituisce ogni [NON VERIFICATO] con il fatto o con la smentita.

DECISIONI DEL TITOLARE
- se e quando aprire la coorte MQL5, dopo la fine della macchina;
- se provare l'osservatore su GitHub Actions (DA-33);
- l'SSD dopo il consuntivo dell'ASK e la prova gratuita;
- MT5 con MCP solo con una demo MT5 e in sola lettura.

OBIEZIONE PIÙ FORTE
- È dispersione. La macchina non è finita: mancano R18 e l'unione in main.
- Ogni fonte nuova apre lavoro, contaminazione e debiti di verifica.
- Gli storici dei segnali sono dominati da sopravvivenza, griglie e martingale, e senza lo stop iniziale non danno R.
- Quindi il loro valore per generare regole verificabili potrebbe essere vicino a zero.

La mia raccomandazione regge solo perché propone prove piccole, con una soglia di abbandono, e **dopo** la fine della macchina.

---
