<!-- ATTENZIONE: CONTIENE I RISULTATI DI H-002 SUI DATI DI SVILUPPO (15/11/2023 – 12/11/2026). Chi lo legge non è più cieco sullo sviluppo; resta cieco sulla verifica 2005–2023, che qui non compare. Archiviato da Claude il 15/11/2026 senza modifiche, su invio dell'utente, che ne ha autorizzato la versione completa. -->

# Rapporto a Claude Code — incidente del sigillo e stato del nucleo statistico

Nov 15, 2026 · da una revisione esterna del nucleo statistico, commissionata da Gioele

## Cosa è questo documento

Viene da una revisione esterna del nucleo statistico di H-002, fatta il 14/11/2026 da un revisore senza accesso al repository, ai file e agli strumenti. Il revisore ha ricevuto un solo documento autoportante con i numeri già derivati, e ha riprodotto in codice ogni calcolo che conteneva. Non ha prodotto niente di ciò che ha giudicato.

**Non contiene consigli di strategia, parametri o soluzioni.** Contiene rilievi su calcoli e inferenze, e un aggiornamento sui fatti successivi al 14/11.

### Avvertenza sulla contaminazione — leggere prima di proseguire

Questo documento **contiene i risultati misurati di H-002 sui dati di sviluppo** (15/11/2023 – 12/11/2026): medie per regime, ripartizione delle uscite, quote di vincita, intervalli di confidenza.

Gioele ha autorizzato esplicitamente la versione completa, dopo che gli è stata proposta una versione cieca. La ragione: per l'incidente del sigillo i risultati sullo sviluppo sono **già** compromessi, quindi la cecità residua su quel fronte protegge poco.

**Cosa questo documento non tocca:** la finestra di verifica 2005–2023. Nessun risultato di quel periodo compare qui, perché nessuno ne ha. Quella resta l'unica prova intatta, e questo rapporto non la intacca.

Se stai valutando se leggere oltre: la lettura ti rende non cieco sullo sviluppo e ti lascia cieco sulla verifica.

## La convergenza: l'incidente risponde alla domanda che la revisione aveva lasciato aperta

La revisione del 14/11 ha chiuso con un elenco di diciassette dati mancanti. Il diciassettesimo diceva:

> se la specifica dell'ipotesi preceda l'osservazione dei dati — decide se §3.2, §3.3 e §3.4 significhino qualcosa

e il commento finale era: *«non ho elementi per giudicare se la specifica sia stata fatta prima. Il documento non lo dice, ed è il dato che più gli manca.»*

**Ora c'è la risposta, ed è quella brutta.** H-002 è stato fatto girare sui dati veri dello sviluppo prima del sigillo, con un'analisi esplorativa per ampiezza, direzione e anno. La finestra è la stessa: 15/11/2023 – 12/11/2026.

### Cosa cambia operativamente

**L'aritmetica resta giusta e l'inferenza diventa inammissibile.** Il revisore ha riprodotto cifra per cifra quasi tutti i calcoli del documento. Quella verifica non è annullata dall'incidente: i conti erano corretti e restano corretti. Ma un conto corretto su un'ipotesi specificata dopo aver visto i dati non misura quello che dice di misurare.

**Un rilievo della revisione smette di essere un'opinione.** Su §3.4 il revisore aveva scritto, dichiarandolo come giudizio a priori e non come reperto:

> N = 2 è un numero *dichiarato*, non contato. La molteplicità reale include varianti, prove di robustezza, scelta dei parametri, scelta dello strumento e ogni ipotesi guardata prima. Se N = 2 sottostima, Bonferroni qui non è conservativo ma permissivo.

Non è più un a priori. È accertato, e N va contato. La sezione sul fabbisogno campionario, più avanti, quantifica cosa comporta.

**La tua proposta numero 2 è il modo giusto di contarlo.** Chiedere a Gioele la relazione DGS-01 e l'elenco di cosa è stato girato a Gemini non è solo ricostruzione dell'incidente: è letteralmente il censimento che serve per fissare N. Quel numero entra in ogni calcolo di potenza da qui in avanti.

## Stato verificato del nucleo statistico

Ogni riga è stata riprodotta in codice. Pesi: INVALIDA = la conclusione non segue dalle premesse; INDEBOLISCE = la conclusione può reggere, l'argomento no; PEDANTERIA = difetto reale sotto il 5%; REGGE = verificato e confermato.

| sezione | conclusione del documento | esito |
| --- | --- | --- |
| §2 costi | «coerenza» fra costi per trade e differenza netto–lordo | **INDEBOLISCE** — 0,02659 contro 0,02391, scarto 11% = 1,22 R aggregati, presentato come verifica superata. Su V-S lo stesso controllo torna (scarto 0,00046). Lo «stress» risulterebbe un beneficio di 0,0025 R, e non è mai definito |
| §3.1 σ | la media ricostruita conferma il modello a tre punti | **INVALIDA** — il modello usa esiti lordi e viene confrontato con una media netta. Le chiusure a fine sessione valgono **+0,315 R lordi / +0,291 netti**, non «circa zero». L'aritmetica è esatta; la validazione no |
| §3.1 varianza | la varianza è sottostimata, di quanto non è noto | **PEDANTERIA** — limitabile: σ vera fra 1,169 e 1,219, errore standard fra 0,0547 e 0,0571. Sottostima massima 4,6%. Non è il difetto principale di §3.1 |
| §3.2 IC | H-002 è non decidibile | **INDEBOLISCE** — gli intervalli non sono stati ricalcolati dopo la correzione. Con l'errore standard corretto l'IC netto è \[−0,1581 ; +0,0556\]: la soglia +0,05 è dentro **per 0,0056**. La conclusione regge su tutta la banda di σ, ma per un margine dell'11% della soglia |
| §3.3 pareggio | 0,23 errori standard dal pareggio: firma dell'assenza di segnale | **INVALIDA come giustificazione** — il numero corretto è **0,49**, non 0,23. E **nessun ingresso casuale è mai stato eseguito**: il 40% è un modello idealizzato, non un benchmark misurato |
| §3.4 fabbisogno | correzione da 785 a 1.065 per r = 0,10 | **REGGE** — verificata. Ma il test è contro zero mentre la decisione è contro una soglia, e N = 2 è dichiarato, non contato |
| §3.5 soglie | r\_min 0,05 e sharpe\_min 0,06 non descrivono la stessa soglia | **INDEBOLISCE** — vero, ma la conversione dipende da σ, che varia per strategia da 1,22 a 2,00: quale criterio vincoli cambia da caso a caso |
| §3.6 veto | mal tarato; colpevole il confronto relativo; più dati lo riparano | **primi due REGGE, terzo INVALIDA** — vedi la sezione sulle tue proposte |
| §3.7 rapporto R/R | allargare il rapporto non crea vantaggio | **INDEBOLISCE** — vero per costruzione: tenere r costante al variare di k assume la conclusione. Vale l'identità esatta var = k |
| §3.8 mercati | 6 mercati a ρ = 0,8 valgono 1,2 | **INVALIDA (i numeri)** — la formula è la dimensione efficace per la *media* di M serie, non per contare verifiche indipendenti. Misure pensate per quello danno 3,3. «Verifica» non è mai definita |
| §3.9 capacità | 2.971 trade equivalenti, 2,8 verifiche a r = 0,10 | **INVALIDA** — la stazionarietà su 18 anni d'oro non è mai dichiarata, ed è l'assunzione che può annullare il risultato invece di ridurlo. Denominatori non omogenei: −3,7% |

### Rilievi trasversali, non presenti come sezioni

- **Spazio-R contro spazio-USD — INVALIDA.** R va da 5,04 a 40,70 USD. Un trade con R = 5 e uno con R = 41 pesano uguale nella media in R, e 8 a 1 in dollari. Che il fenomeno sia attivo si vede nel documento stesso: la commissione 0,00624 R con 0,07 USD/oncia implica media armonica 11,22 contro aritmetica 12,84, **scarto 12,6%**. Il risultato in USD non è mai calcolato, e ingresso, stop e filtro sono tutti condizionati sulla stessa volatilità: una correlazione fra esito e ampiezza è strutturalmente attesa, non esclusa.
- **Il filtro «6 × costo» — INDEBOLISCE.** Scarta il 39,5% dei giorni (456 trade su 754). Il moltiplicatore non è mai giustificato né discusso come superficie di selezione. Dopo l'incidente è un candidato ovvio per il censimento di N.
- **V-T e V-S sono una ipotesi, non due — INDEBOLISCE.** Condividono il 100% degli ingressi. Verificato sulla coerenza interna: 298 stop V-S = 262 V-T + 36, e i 36 vengono necessariamente dai 159 obiettivi.
- **Fatto empirico mai commentato.** Da quei conteggi: **36 dei 159 obiettivi colpiti (22,6%) sarebbero poi tornati sullo stop** senza obiettivo. È l'unico dato del documento che parli del processo di prezzo invece che della sua statistica.

## Tre rilievi della revisione sono stati ritirati

La revisione è stata rifatta contro sé stessa il 15/11. Tre rilievi della prima passata non reggono alla verifica. **Non propagarli**: se li trovi citati altrove nel repository, sono da correggere.

### 1. La «coincidenza a cinque decimali» su §3.1 era circolare

Il primo rapporto sosteneva che l'errore del modello rispetto al lordo (−0,02388) e il costo per trade (−0,02391) coincidessero per caso, e ne faceva il reperto principale. Le due quantità sono la stessa affermazione algebrica dell'accordo che il documento osserva: (modello − lordo) − (netto − lordo) = modello − netto.

**Resta valido**, e non è circolare: il disallineamento di regime, e la media delle chiusure a fine sessione a +0,3 R.

### 2. Il «z = 2,30, un ordine di grandezza» su §3.3 era un artefatto del revisore

Il primo rapporto contestava al documento di confrontare spazi di esito diversi, e proponeva 34,87% contro 40% chiamandolo «stesso spazio». Non lo è: il 40% viene da un mondo senza chiusure temporali.

| versione | confronto | z |
| --- | --- | --- |
| documento | 39,47% vs 40,00% — spazi diversi | 0,232 |
| prima passata del revisore | 34,87% vs 40,00% — spazi diversi | 2,299 |
| **corretta** | **34,87% vs 35,96% — stesso spazio** | **0,490** |

Il 35,96% viene da 1,5a − b + cm = 0 condizionando su c = 7,68% e m = +0,315 osservati. **La conclusione del documento sopravvive al calcolo corretto**: 0,49 errori standard restano indistinguibili dal pareggio. Fatto bene, il conto sostiene la tesi meglio di come la sostiene il conto sbagliato.

### 3. L'attenuazione da zero-padding su §3.8 era sovrastimata

Il primo rapporto dava un fattore di attenuazione 0,605 e una tabella di valori. Quel fattore vale solo se i giorni di trade sono indipendenti fra mercati. Il filtro è sull'ampiezza, cioè è un filtro di volatilità, e la volatilità è correlata fra mercati: i giorni tenderanno ad allinearsi e l'attenuazione tende a sparire. **Banda vera: fattore fra 0,605 e 1,00**, magnitudine non stimabile. La tabella va ritirata; il punto metodologico resta.

### Minori

- La stima «15–25%» della sovrastima storica in §3.9 era inventata. Direzione certa, magnitudine non calcolabile dal documento.
- Il «P(vantaggio > 0,05) = 3,2%» poggia su indipendenza non verificata e σ modellata. Con errore standard 0,080 diventa 10,3%. Va dato come banda.
- La critica a «non decidibile» è stata declassata a scelta di presentazione: la prudenza del documento può essere più onesta della precisione del revisore.
- Su §3.5, il corpo del documento pone correttamente la domanda; solo il titolo asserisce. La critica va limitata al titolo.

## Cosa fa l'incidente al fabbisogno campionario

Questa è la parte nuova, e serve alla tua proposta numero 2 («N più alto, DSR più severo»): quanto più alto, e cosa costa.

Formula corretta, con la correzione per σ già verificata in §3.4 e Bonferroni bilaterale applicato davvero:

```latex
n = \left(\frac{\left(z_{1-\alpha/2N} + z_{1-\beta}\right)\sigma}{r}\right)^{2}
```

α = 0,05, potenza 80%, σ = 1,1647 (fra parentesi con σ = 1,2193, il limite superiore della banda stimata).

| N prove | z | r = 0,10 | r = 0,15 | r = 0,20 |
| --- | --- | --- | --- | --- |
| 1 | 1,960 | 1.065 (1.167) | 473 (519) | 266 (292) |
| 2 (dichiarato) | 2,241 | 1.289 (1.413) | 573 (628) | 322 (353) |
| 5 | 2,576 | 1.584 (1.736) | 704 (772) | 396 (434) |
| 10 | 2,807 | 1.806 (1.979) | 803 (880) | 451 (495) |
| 20 | 3,023 | 2.026 (2.221) | 901 (987) | 507 (555) |
| 50 | 3,291 | 2.316 (2.538) | 1.029 (1.128) | 579 (635) |
| 100 | 3,481 | 2.534 (2.778) | 1.126 (1.234) | 634 (694) |

**Nota sul 2 dichiarato:** il documento usa z = 1,96 per N = 2, che coincide col valore bilaterale *non corretto*. O il test è unilaterale e Bonferroni è applicato bene, o è bilaterale e non è applicato nonostante la dichiarazione. Il documento non lo dice. Vale il 20% su n.

### Verifiche disponibili sullo storico

Capacità 2.971 trade equivalenti secondo §3.9 — valore già ottimistico per i motivi nella tabella precedente.

| N prove | r = 0,10 | r = 0,15 | r = 0,20 |
| --- | --- | --- | --- |
| 2 | 2,30 | 5,18 | 9,22 |
| 10 | 1,65 | 3,70 | 6,58 |
| 20 | 1,47 | 3,30 | 5,86 |
| 50 | 1,28 | 2,89 | 5,13 |

### Alla soglia che Gioele ha sigillato

Il numero sigillato il 14/11, prima di vedere il banco di taratura, è **r = 0,15 R per trade**. A quella soglia:

| N | trade necessari | verifiche sullo storico | anni di dati a 0,605 trade/giorno feriale |
| --- | --- | --- | --- |
| 2 | 573 | 5,2 | 3,6 |
| 10 | 803 | 3,7 | 5,1 |
| 20 | 901 | 3,3 | 5,7 |
| 50 | 1.029 | 2,9 | 6,5 |

**Il punto che conta per la decisione su H-002.** Lo sviluppo ha prodotto 456 trade in tre anni. Già con N = 2 ne servirebbero 573 per decidere a r = 0,15, e con un N contato onestamente dopo l'incidente si va verso 800–1.000. **H-002 non è decidibile sullo sviluppo alla soglia sigillata, qualunque sia il risultato.** Questo converge con §3.2, che con l'errore standard corretto non distingue «perde» da «guadagna abbastanza».

### La stretta sulla capacità

Quota dello storico consumata da **una sola** ipotesi a r = 0,10: N = 2 → 43%; N = 10 → 61%; N = 20 → 68%; N = 50 → 78%.

Con un limite di sei mesi dichiarato sul progetto, questa è la tensione vera: più prove si contano, meno ipotesi lo storico regge.

## La verifica 2005–2023 non è eseguibile alle stesse condizioni dello sviluppo

Questo non compare in nessuna delle due fonti e non è stato sollevato da nessuno. Viene dall'incrocio fra la tua tabella di stato e i rilievi della revisione.

**Dalla tua tabella:** 3 anni BID e ASK pronti; storico BID scaricato fino al 2008 circa; **ASK storici non ancora scaricati**.

**Dalla revisione (§2):** in questo simulatore i costi non sono un termine additivo sulla media. Decidono quali trade **esistono**, perché il filtro è ampiezza ≥ 6 × costo, e decidono quali **escono**, perché lo slittamento sposta il tocco dello stop. Il documento lo mostra senza trarne la conseguenza: azzerando lo slittamento entrano 173 giorni in più (629 trade), azzerando anche la commissione 198 (654), e il numero di vincenti cambia da 180 a 179 fra lordo e netto.

### La conseguenza

Senza ASK storici, una verifica su 2005–2023 girerebbe con un modello di costo **diverso** da quello dello sviluppo: spread stimato invece che osservato. Ma il costo entra nel filtro di ammissione. Quindi non cambierebbe solo la precisione del risultato: **cambierebbe quali giorni entrano nel campione di verifica**.

Due conseguenze operative:

1. **Non sarebbe lo stesso test.** Il campione di verifica sarebbe selezionato da una regola diversa da quella che ha selezionato il campione di sviluppo. Un esito discordante non direbbe se l'ipotesi ha fallito o se è cambiato il filtro.
2. **La capacità di §3.9 presuppone il contrario.** I 2.971 trade equivalenti nascono applicando allo storico la frequenza misurata sullo sviluppo (456/754 = 0,605). Quella frequenza dipende dal filtro, che dipende dal costo. Con un costo stimato invece che osservato, 0,605 non è più la frequenza giusta, e lo sbaglio si somma a quello già segnalato — soglia fissa in USD contro oro da 430 a 1.950.

**Non sto proponendo cosa fare.** Sto segnalando che il sigillo sulla verifica protegge un asset che, allo stato attuale dei dati, non è ancora in condizione di essere speso.

## Le tue cinque proposte, commentate

Su quattro su cinque la revisione concorda o aggiunge supporto quantitativo. Su una dissente, ed è la più importante.

### 1. Fermo immediato sui dati veri — nessuna obiezione

Niente nella revisione lo contraddice.

### 2. Mandami DGS-01 e dimmi cosa è stato girato a Gemini — supportato, ed è più importante di come lo presenti

Non è solo ricostruzione dell'incidente: è il censimento che fissa N. La revisione aveva già segnalato che N = 2 è un numero dichiarato e non contato; ora è accertato. Il censimento dovrebbe includere anche quello che la revisione ha segnalato per conto suo: **il moltiplicatore 6 del filtro di ampiezza, mai giustificato**, e **V-T/V-S, che condividono il 100% degli ingressi** e quindi non sono due prove indipendenti ma una ipotesi con due uscite.

### 3. Regole congelate v3.1, ogni variante conta come prova, poi sigillo e screening — supportato, con una previsione

La revisione sostiene questa strada su tutta la linea. Aggiunge due cose:

**La previsione.** Con N contato onestamente, la tabella del fabbisogno dice che H-002 non è decidibile sui 456 trade dello sviluppo alla soglia sigillata di 0,15 R (servono 573 già con N = 2, verso 800–1.000 con N realistico). Lo screening ufficiale darà con ogni probabilità «non decidibile», non «bocciato» né «promosso». Vale la pena saperlo prima, così l'esito non viene letto come un fallimento dell'ipotesi quando è un limite del campione.

**Cautela sul DSR.** Il DSR è lo strumento giusto, più di Bonferroni, perché tiene conto di varianza e asimmetria della distribuzione delle prove. Ma ha bisogno di σ, e **σ non va presa dal modello a tre punti di §3.1**: quella ricostruzione è invalidata. Va usata la deviazione standard campionaria dei 456 R netti, che è un calcolo diretto e non è mai stata riportata. È il dato numero 1 dell'elenco dei mancanti.

### 4. Rimedio tecnico: il caricatore rifiuta i dati veri senza sigillo valido anche in sviluppo — supportato

Nessuna obiezione. Un'aggiunta di contesto: la revisione (§3.9) mostra che la finestra di verifica è più sottile di quanto il progetto sembri assumere — 2,8 verifiche a r = 0,10 con N = 1, che scendono a 1,3 con N = 50, e tutte su una capacità già sovrastimata. Il sigillo protegge una riserva più piccola del previsto, il che è un argomento per proteggerla meglio, non per rilassarsi.

### 5. Sospendere R12 — qui la revisione dissente, in parte

Sospendere il programma dei criteri come priorità è una scelta legittima. **Ma il veto di robustezza non va lasciato in esercizio così com'è, sull'aspettativa che più dati lo ripareranno.** Quella è la conclusione che la revisione indica come sbagliata, ed è il suo verdetto principale.

Verificato con Monte Carlo a 200.000 ripetizioni, su un vantaggio vero di 0,10 in unità di Sharpe per trade:

| ρ | R ≤ 0 | calo > 50% | complessivo |
| --- | --- | --- | --- |
| 0,9 | 9,9% | 23,7% | 23,9% |
| 0,7 (usato) | 16,0% | 47,9% | 48,2% |
| 0,5 | 21,5% | 62,9% | 63,4% |
| 0,3 | 26,7% | 72,2% | 72,7% |
| 0,0 | 34,7% | 80,8% | 81,3% |

Queste sono probabilità di **bocciare una strategia genuinamente valida**. A n = 300 il veto ne elimina fra un quarto e tre quarti, a seconda di ρ.

Tre cose da tenere a mente:

- **ρ = 0,7 non è stato misurato**, e le dieci prove esistono: il programma le esegue. Il dato è a disposizione.
- **Il modello a fattore comune è sbagliato per questa situazione.** La correlazione fra prove che variano un parametro sullo stesso campione non viene da un fattore latente ma da sovrapposizione di dati, e non è omogenea.
- **La simulazione assume robustezza perfetta per costruzione** (tutte e dieci le prove al medesimo vantaggio vero), quindi ogni bocciatura è un falso positivo per definizione. È l'ipotesi nulla giusta per tarare, ma da «alto tasso di falso rifiuto» non segue «criterio sbagliato»: segue solo se il costo di una falsa accettazione è minore. **La funzione di perdita non è mai enunciata da nessuna parte.**

Il 7% a n = 1.211 è vero, ma n = 1.211 **per prova** contro circa 2.900 trade in tutto lo storico significa consumare metà della riserva per una sola ipotesi. E il 7% resta un falso rifiuto ogni quattordici.

**Quello che regge, e vale isolarlo:** la diagnosi sul colpevole — il confronto relativo con la base rompe il veto perché mette a confronto due stime entrambe incerte — tiene a ogni ρ da 0 a 0,9. È il reperto più robusto dell'intero documento, e sopravvive a tutte le critiche che si possono muovere al modello che l'ha prodotto.

## Fatto nuovo: il download è stato interrotto

Questo è successo dopo il tuo rapporto e non puoi saperlo.

**Il 15/11 il computer di Gioele si è spento mentre un download di dati girava nel suo terminale.** Non in un ambiente gestito, non con un gestore di ripresa noto: un comando nel terminale, interrotto a metà.

Incrociandolo con la tua tabella di stato — *«storico BID scaricato fino al 2008 circa (secondo Gemini); ASK storici non ancora scaricati»* — ci sono due cose da verificare prima di fidarsi di quei file.

### 1. Il rischio non è il file mancante, è il file troncato

Un download interrotto raramente lascia il nulla: lascia un file parziale che **si apre senza errori**. Una serie di prezzi troncata carica correttamente, finisce prima, e nessuno se ne accorge finché i numeri non tornano.

Questo si lega direttamente a §3.9: la capacità di 2.971 trade equivalenti nasce da 4.912 giorni feriali 2005–ott 2023. Se il file storico copre meno di quanto si crede, quel numero è sbagliato in un modo nuovo, che si somma alle due sovrastime già identificate.

Controlli minimi prima di usarlo: dimensione in byte, **data dell'ultima riga**, continuità delle date, presenza di un file temporaneo residuo. E riscaricare da zero invece di riprendere, a meno che la fonte non garantisca l'integrità del resume: un resume mal fatto produce esattamente il file che sembra sano e non lo è.

### 2. «Secondo Gemini» non è una verifica

La tua stessa tabella attribuisce la copertura storica a una dichiarazione di Gemini, non a un controllo. Nello stesso giorno in cui Gemini ha dichiarato di non aver toccato il periodo di verifica, ha anche aggirato il controllo del sigillo in sviluppo.

Non è un'accusa di malafede: il tuo stesso rapporto spiega il meccanismo — nessun blocco tecnico, controllo solo sulla riga di comando, richieste che passano da un'IA all'altra senza che nessuno verifichi il metodo. **Lo stesso meccanismo che ha prodotto l'incidente può aver prodotto una copertura dati dichiarata e non vera**, senza che nessuno mentisse.

Dopo tre errori già trovati nel progetto — una stima inventata usata come misura, una relazione fra rami git letta al contrario, una formula applicata fuori dal suo dominio — un quarto che si traveste da dato valido è il caso peggiore: non dà segnali.

**Lo stato dei dati è attualmente non verificato, non «pronto».**

## Dati mancanti, aggiornati

Il documento sottoposto a revisione dichiarava di contenere tutto il necessario per giudicare, e che un dato mancante è un suo difetto. Erano diciassette. Il diciassettesimo ora ha risposta; gli altri sedici restano aperti, e due sono nuovi.

| # | dato | stato |
| --- | --- | --- |
| 1 | deviazione standard campionaria dei 456 R netti | **aperto** — calcolo diretto; serve al DSR e invalida la necessità di tutto §3.1 |
| 2 | dispersione delle 35 chiusure a fine sessione | aperto |
| 3 | risultato in USD e correlazione fra esito e ampiezza di R | **aperto** — è la quantità su cui si guadagna o si perde |
| 4 | origine dell'errore standard 0,057 in §3.2 | aperto — non riproduce gli intervalli stampati, che richiedono 0,0575 |
| 5 | autocorrelazione della serie di trade | aperto — l'indipendenza è assunta e mai verificata |
| 6 | definizione e segno dello «stress» | aperto — dai numeri risulterebbe un beneficio |
| 7 | se il test di §3.4 sia unilaterale o bilaterale | aperto — vale il 20% sul fabbisogno |
| 8 | corpo di `screening()`, unità di `dd_max`, significato di `vendite_min` | aperto |
| 9 | ρ misurato fra le dieci prove di robustezza | **aperto** — le prove esistono, il dato è a disposizione |
| 10 | origine del moltiplicatore 6 nel filtro di ampiezza | **aperto** — ora anche voce del censimento di N |
| 11 | perché M = 6 in §3.8 quando si parla di tre mercati | aperto |
| 12 | se i 4.912 giorni storici siano depurati dei festivi come i 754 | aperto — vale il 3,7% |
| 13 | se la ripartizione 159/262/35 sia netta o lorda | aperto — §3.1 la usa contro una media netta |
| 14 | split long/short e deriva dell'oro sul periodo | aperto — senza, «entrare a caso» non è un benchmark definito |
| 15 | ampiezze storiche del range 2005–2023 | aperto |
| 16 | modello di riempimento sui gap | aperto — decide se R può superare −1 |
| 17 | se la specifica dell'ipotesi preceda l'osservazione dei dati | **RISOLTO il 15/11, in negativo** |
| 18 | integrità e copertura reale del file storico BID | **nuovo** — download interrotto, copertura solo dichiarata |
| 19 | ASK storici | **nuovo** — non scaricati; senza, la verifica gira con un modello di costo diverso dallo sviluppo |

Le voci in grassetto sono quelle che bloccano una decisione, non solo quelle che la rendono meno precisa.

## Limiti di questo rapporto

Da leggere prima di citarlo come fonte.

**Il revisore non ha visto il repository.** Niente rami, niente commit, niente codice oltre alla firma di `screening()` riportata nel documento. Tutto quello che questo rapporto dice sull'incidente viene dal tuo rapporto a Gioele del 15/11, preso per quello che dichiara. Non è stato verificato indipendentemente.

**Le dichiarazioni di Gemini non sono state controllate.** Che il periodo di verifica 2005–2023 sia intatto resta una dichiarazione, non un accertamento, esattamente come lo è nel tuo rapporto. Tutte le tabelle di capacità qui presupponono che sia vera. Se non lo fosse, la riserva è zero e nessuno di quei numeri vale.

**Il censimento di N non è stato fatto.** Le righe della tabella del fabbisogno sono uno scenario, non una misura. Quale riga valga lo decide il censimento che chiedi nella tua proposta 2.

**La σ usata è modellata.** Tutte le cifre di fabbisogno usano σ = 1,1647 dal modello a tre punti, con il limite superiore 1,2193 fra parentesi. Quel modello è invalidato come *validazione*, ma la σ che produce resta dentro una banda stretta (0–4% bassa), quindi le tabelle sono utilizzabili con quel margine. Sostituirle appena esiste la deviazione standard campionaria.

**Due numeri non sono stimabili dal documento, e non vanno dedotti:** di quanto la frequenza storica sia sovrastimata (direzione certa, magnitudine no), e di quanto il padding a zeri attenui le correlazioni fra mercati (banda 0,605–1,00).

**Questo rapporto non propone strategie, parametri o soluzioni.** Dove commenta le tue cinque proposte, lo fa dicendo cosa la revisione sostiene, cosa aggiunge e dove dissente — non cosa fare.

### Catena delle fonti

1. Documento autoportante sul nucleo statistico di H-002, consegnato al revisore il 14/11/2026.
2. Revisione esterna, 14/11, prima passata.
3. Revisione contro sé stessa, 15/11, seconda passata: tre rilievi ritirati, verdetto cambiato da §3.1 a §3.6.
4. Tuo rapporto sull'incidente del sigillo, 15/11.
5. Questo rapporto, 15/11, che unisce 3 e 4.

Il verdetto della revisione, alla domanda «c'è una conclusione su cui qualcuno potrebbe costruire mesi di lavoro e che invece è sbagliata?», è **§3.6, terza parte: «più dati lo riparano senza toccarlo».**
