# RICHIESTA A CLAUDE — Storici MetaTrader, strumenti per Claude e osservazione continua

il titolare sta costruendo Trading Brain con ChatGPT nel ruolo di DGS e Gemini/Antigravity per la replica indipendente. Vorrei il tuo parere su come migliorare **l’intero percorso dalla scoperta di un’idea alla sua verifica**. Un amico mi ha parlato degli storici dei fornitori di segnali MetaTrader e di una «impostazione di trading per Claude». La seconda espressione è sua e il prodotto preciso resta da identificare. Stiamo anche studiando Brad Goh per estrarre idee da una spiegazione su grafico. Siamo all’inizio e oggi non c’è una nuova strategia pronta per il motore.

**Mandato.** Parti da STATO-PROGETTO, dalla roadmap effettiva e dalle decisioni vigenti. Svolgi una ricerca documentale e restituisci una proposta in chat. L’implementazione, gli acquisti e l’avvio di servizi richiedono una decisione successiva di il titolare. Rispetta la priorità della baseline XAUUSD BID/ASK, la riserva sigillata, la demo futura e la separazione dei ruoli. Usa documentazione pubblica e materiale di progetto autorizzato. Per questa ricognizione bastano le specifiche dei servizi, senza scaricare storici di trader, aprire grafici della riserva, installare software o collegare conti. Segnala ciò che non puoi verificare.

## 1. Cosa possiamo imparare dagli storici dei fornitori di segnali?

Verifica per MQL5 Signals su MT5 cosa vede un visitatore, cosa richiede login o abbonamento e cosa si può legittimamente esportare, conservare o analizzare in automatico. Distingui il conto del fornitore dal servizio visto dal visitatore. Per ogni campo importante indica fonte, granularità, eventuale ritardo e limiti. Considera operazioni chiuse, equity e perdite aperte, volumi, timestamp e fuso del broker, depositi/prelievi, commissioni, swap, stop iniziale e sue modifiche. Distingui ciò che il servizio acquisisce da ciò che un ricercatore può effettivamente ricostruire. Indica come distinguere storia precedente alla pubblicazione, periodo monitorato, conto reale o demo e operatività manuale o algoritmica, ove documentato.

Proponi un metodo futuro per generare ipotesi. Esempio ipotetico: diversi ingressi long su oro a prezzi via via inferiori potrebbero corrispondere a ordini frazionati pianificati, a una griglia o a un aumento del rischio su una perdita. Quali dati discriminerebbero queste spiegazioni? Cosa resterà inconoscibile, comprese le occasioni in cui il trader ha scelto di astenersi? Se il rischio iniziale manca, spiega quali metriche restano utilizzabili e perché il rendimento in R del trader resta indeterminato. Mostra anche un uso concreto accanto a Brad: il video suggerisce una regola dichiarata, lo storico mostra decisioni eseguite. La somiglianza visiva da sola non identifica la regola.

Disegna sulla carta un campionamento definito prima dei risultati, che includa provider ordinari, perdenti, inattivi o rimossi quando osservabili. Se i rimossi sono irrecuperabili, indica il limite e valuta una coorte seguita prospetticamente. Considera più conti dello stesso autore, rischio flottante, esposizioni correlate, spread e slippage. Proponi un confronto semplice capace di smentire un’idea. Tieni distinti scoperta su un campione, registrazione preventiva delle varianti e verifica indipendente. Lo storico usato per trovare l’idea è materiale esplorativo. Per lo studio attuale indica quali attività soltanto documentali svolgiamo e quando scatterebbe il conteggio delle prove secondo il nostro registro.

## 2. Quale funzione per Claude esiste e a cosa ci servirebbe?

Controlla tre possibilità documentate: **assistente interno di MT5 con Anthropic come provider**, **Claude Code collegato a MT5 via MCP**, **plugin ufficiali Anthropic per la ricerca finanziaria**. Contempla un prodotto terzo solo se trovi nome, editore e documentazione. Se manca il nome esatto usato dall’amico, conserva l’incertezza. Se non puoi vedere il piano o la build di il titolare, indica come identificarli e quale passaggio dipende da essi.

Per ciascuna alternativa descrivi in poche righe scopo, ambiente supportato (Mac compreso), passaggi di attivazione documentati, prerequisiti, licenze dati, piano o fatturazione API, permessi effettivi e revoca. Distingui assistente interno e client MCP esterno. Verifica separatamente gli endpoint marketdata, terminal e metaeditor, quali possono leggere dati di conto, inviare ordini o modificare file, e se la sola lettura è tecnicamente imponibile nella configurazione proposta. Un feed generico potrebbe bastare per un calendario ma essere inadatto alla baseline BID/ASK del broker. Scegli un uso concreto che giustifichi un’integrazione e un caso in cui sia sufficiente un file locale. Nessuna credenziale o dato personale nel rapporto.

## 3. Quali strumenti migliorerebbero davvero la roadmap?

Parti dai colli di bottiglia documentati e cerca anche opzioni che noi non abbiamo pensato. Considera fonti e licenze dati, replay e annotazione con TradingView o MT5, analisi e controlli di qualità, avvisi, software già disponibile, servizio gestito, VPS, mini-PC o altro hardware. Confronta sempre con ciò che già possediamo e con l’alternativa più semplice. Stima costi una tantum e mensili, tempo umano e manutenzione. Per prezzi e prestazioni indica fonte e data oppure dichiara le ipotesi. Suggerisci un acquisto solo dopo aver identificato un limite misurabile.

Per l’osservazione continuativa confronta tre opzioni: avvisi o controlli programmati, raccolta persistente con software deterministico e intervento di un agente solo su evento. Distingui disponibilità 24/7 dell’infrastruttura, orari e pause effettivi del mercato/feed e necessità della presenza umana. Disegna un esempio su XAUUSD: come distingueresti un’interruzione delle quotazioni da mercato chiuso? Chi registra l’evento, come rilevi buchi e duplicati dopo un riavvio, quando avvisi il titolare e come misuri utilità, falsi allarmi e consumo di crediti? Considera il Mac spento o in sospensione. Per i ricercatori indipendenti assegna un quesito a chi propone l’ipotesi e un tentativo di falsificazione a chi la verifica alla cieca. Spiega come evitare che usino gli stessi risultati o si influenzino prima della replica.

## Consegna e criterio di accettazione

Apri con il tuo verdetto in dieci righe. Poi una matrice breve: **idea | problema risolto | fatto verificato e fonte | cosa resta da provare | fase e dipendenza | costo | verifica di utilità | decisione proposta**. Classifica ogni idea come applicabile ora, dopo una condizione precisa, incompatibile o da scartare. Approfondisci le tre con il miglior rapporto fra beneficio atteso e costo. Per ciascuna indica la prova più economica, il confronto, una misura osservabile e il risultato che ti farebbe abbandonare la proposta. Puoi concludere che oggi bastano gli strumenti esistenti.

Chiudi con una sola azione documentale utile ora, le decisioni che spettano a il titolare e l’obiezione più forte alla tua raccomandazione. Distingui fatti, deduzioni, ipotesi e opinioni. Il rapporto è accettabile se possiamo decidere cosa approfondire e quando, capire cosa gli storici non rivelano e identificare un percorso verificabile per l’eventuale attivazione senza confondere ricerca, monitoraggio ed esecuzione.

### Fonti ufficiali da cui partire

- [MetaTrader 5 · Statistiche e storico dei segnali](https://www.metatrader5.com/en/terminal/help/signals/signal_monitoring)
- [MQL5 · Regole del servizio Signals](https://www.mql5.com/en/signals/rules)
- [MetaTrader 5 · Configurazione AI Assistant e MCP](https://www.metatrader5.com/en/terminal/help/mcp_and_ai/configuration)
- [MetaTrader 5 · Funzioni dei tre server MCP](https://www.metatrader5.com/en/terminal/help/mcp_and_ai/capabilities)
- [Anthropic · Agenti e condizioni di accesso](https://www.anthropic.com/news/finance-agents)
- [Anthropic · Plugin e istruzioni per Cowork e Claude Code](https://github.com/anthropics/financial-services)
