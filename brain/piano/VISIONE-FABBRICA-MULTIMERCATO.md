# Dalla strategia singola alla fabbrica di ricerca multi-mercato (20/11/2026)

**Su richiesta del titolare.** È un documento di **visione e proposta**. Non decide nulla e non modifica la macchina. Le scelte restano del titolare.

## Pagina per il titolare

- L'oro è **solo il primo mercato**, scelto per cominciare. Il progetto sarà molto più ampio: tanti mercati, tante sessioni, tanti parametri.
- Il limite delle «circa 4 verifiche» vale **per la riserva di un solo mercato**. Ogni mercato ha la sua riserva, quindi le verifiche storiche totali sono molte di più.
- **Lo sblocco vero non è scaricare più storico, è il futuro.** La demo in avanti è un campo di prova illimitato e sempre pulito: non si consuma mai. Lo storico diventa il primo filtro; la demo diventa il motore principale.
- La visione giusta non è «trovare la strategia perfetta sull'oro», ma costruire una **fabbrica di ricerca**: un flusso che prova idea × mercato × sessione × parametri, scarta quasi tutto, tiene i pochi sopravvissuti e li combina in un **portafoglio** di tante strategie semplici (il metodo di Unger).
- **La macchina che stiamo finendo è il controllo qualità di quella fabbrica.** Prima la finiamo e la collaudiamo su un caso; poi la trasformiamo in fabbrica.

## 1. Che cosa NON cambia nella macchina (buona notizia)

Gran parte di ciò che abbiamo costruito è **già neutro rispetto al mercato**: funziona su oro, GBPJPY o qualsiasi altro senza modifiche.

| Pezzo | Perché è già generale |
|---|---|
| **Metro del verdetto (D-31, `verdetto_d31.py`)** | Lavora su coppie giornaliere (risultato, numero di trade) espresse in R. Non sa nemmeno quale sia il mercato |
| **Collaudo IA-02** | Fatto su dati sintetici; vale per qualunque mercato nel suo dominio |
| **Registro della riserva (`riserva.py`)** | Conosce solo date, mai prezzi |
| **Registro delle prove (N)** | Conta per ipotesi, non per mercato |
| **Screening (D-36), minimi (D-37)** | Soglie in R, indipendenti dal mercato |

**Conseguenza:** il cuore non va rifatto per ogni mercato. È il risultato di averlo costruito con cura.

## 2. Che cosa è specifico e va reso generico (il vero nuovo lavoro)

Una cosa sola, oggi, è scritta a mano per ogni strategia: **il simulatore**, cioè il programma che esegue la strategia minuto per minuto. Oggi `orb_londra.py` è specifico della rottura del range di Londra sull'oro. Per fare tanti mercati e tante idee senza settimane di codice ogni volta, serve:

1. **Un motore generico e configurabile.** Una strategia si descrive con **regole e parametri** (quando entrare, dove mettere stop e target, quando non operare) e il motore la esegue, senza riscrivere codice. L'audit lo aveva indicato come il vero costo del progetto.
2. **Per ogni mercato, i suoi dati di contorno:**
   - lo storico BID/ASK (già lo sappiamo scaricare);
   - il **calendario e le sessioni** (per l'oro conta l'apertura di Londra; per l'indice S&P l'apertura di New York);
   - i **costi** (dimensione del contratto, commissione, spread), uno per mercato.

Queste parti hanno una **struttura unica** e un **contenuto per mercato**: si costruisce la struttura una volta, poi si aggiunge un mercato alla volta.

## 3. Storico (scarso) contro futuro (illimitato)

- La **riserva storica** è una risorsa scarsa e irripetibile: una volta vista, una finestra è consumata. Serve come **primo filtro**, non come prova infinita.
- Il **futuro** è illimitato e sempre pulito. La **demo in avanti** (con il test di Wald, DA-29) prova una strategia su dati che nessuno ha mai visto, su quanti mercati vogliamo, senza consumare niente.
- **Il motore della fabbrica, a regime, è la prova in avanti.** Lo storico dà il primo sì/no veloce; la prova in avanti dà la prova vera e continua.

**Correzione (20/11/2026, su domanda del titolare): «illimitato» non vuol dire «veloce».** Il futuro arriva un giorno alla volta, e il costo è il **tempo**. Con 15–20 trade al mese (stime, test di Wald):
- una strategia forte, circa +0,30 R, si riconosce in circa 100 trade, cioè **5–7 mesi**;
- una debole, circa +0,10 R, in alcune centinaia di trade, cioè **1,5–2 anni o più**.

**Il vantaggio non è la velocità, è il parallelismo.** Il tempo passa uguale per tutte le strategie sigillate: se ne possono seguire molte, su molti mercati, nello stesso momento, senza consumare niente.

**Due livelli di prova in avanti, da non confondere:**
1. **Prova in avanti simulata.** Ogni giorno si scaricano i dati nuovi e si fanno girare le strategie sigillate sul simulatore. È automatica, senza conto, senza ordini e senza il tempo del titolare. Serve per **tante strategie in parallelo**.
2. **Demo con ordini sul broker.** Solo per le poche migliori: misura la fedeltà dell'esecuzione reale (slittamenti, spread, DA-29) rispetto alla simulazione.

**Anche qui la statistica vale:** seguendo molte strategie in avanti, alcune sembreranno buone per caso. Le prove in avanti si contano nel registro, con le soglie fissate prima.

Con queste precisazioni, il problema della scarsità si sposta: lo storico non è più il collo di bottiglia; lo diventa il **tempo**, che si gestisce con il parallelismo.

## 4. L'ampiezza non è gratis (la sfumatura onesta)

- **Mercati correlati danno poca informazione nuova.** Oro e argento si muovono insieme; euro e sterlina contro dollaro pure. Dieci mercati possono valere 3–4 «famiglie» davvero indipendenti. Vanno **dichiarati come famiglia** (già previsto, DGS-09 §2) e contati come tali.
- **La statistica conta tutte le prove (N), su tutti i mercati** (DA-28). Provare un'idea su 10 mercati sono 10 tentativi: se 1 passa, va chiesto se è vero o se è l'1 su 10 fortunato. L'ampiezza **ridistribuisce** la severità, non la elimina.
- **La risorsa scarsa vera è l'informazione indipendente**, non il numero di mercati.

Questo non frena la visione: la rende onesta, ed è esattamente ciò che la macchina serve a garantire.

## 5. Che cosa NON va integrato adesso

- **Non allarghiamo la «definizione di fatto» (D-34).** L'elenco chiuso resta quello. Il motore generico è una **fase nuova, dopo**, non un'aggiunta ora. Allargare adesso riaprirebbe il ciclo di revisioni senza fine (rischio n. 4 dell'audit).
- **Prima si finisce e si collauda la macchina stretta** su un caso (la prova generale a vuoto), così sappiamo che la catena regge. Poi la si industrializza.

L'unico lavoro «da fare adesso», ed è **quasi gratis**, è un **controllo di progetto**: verificare che i pezzi attuali non abbiano dentro assunzioni «solo oro» che costerebbe care togliere dopo.

**Primo esito del controllo (20/11/2026, ricerca nel codice):**
- **neutri davvero:** `verdetto_d31.py`, `riserva.py`, `sigillo.py` (registro delle prove). Nessun riferimento all'oro o a Londra;
- **`criteri.py`:** neutro nella logica, ma legge le metriche nel formato del simulatore di H-002 e usa le soglie di H-002 come valori predefiniti;
- **`caricatore.py`: NON neutro.** Il simbolo è già un parametro (predefinito `XAUUSD`), ma il **controllo di qualità dei dati usa una sessione di Londra fissa (8:00–16:45)** scritta nel codice, e importa una funzione dal simulatore di Londra. È un'assunzione «oro-Londra» da rendere parametro (sessione per mercato) quando si aggiunge il secondo mercato.

Quindi la correzione della §1: il cuore del verdetto è neutro; **il caricatore dei dati è legato alla sessione di Londra** e andrà generalizzato nella fase 4. Non va toccato ora: è nel perimetro sigillato e funziona correttamente per l'oro.

## 6. Sequenza proposta

| Fase | Che cosa | Stato |
|---|---|---|
| **1. Macchina stretta** | Finire l'elenco D-34; prova generale a vuoto | In corso |
| **2. Controllo di progetto** | Confermare che i pezzi sono neutri rispetto al mercato; elencare le poche assunzioni «oro» da togliere | Rapido, da fare |
| **3. Motore generico** | Simulatore configurabile con regole e parametri; 2 giri di revisione propri | Dopo la fase 1 |
| **4. Secondo mercato** | Aggiungere un mercato non correlato all'oro (per esempio un indice o una coppia forex): dati, calendario, costi | Dopo la fase 3 |
| **5. Fabbrica e portafoglio** | Flusso idea × mercato × sessione × parametri; demo in avanti come motore principale; portafoglio di sistemi | Visione |

## 7. Decisioni per il titolare (da preparare, non da prendere ora)

1. **Ordine dei mercati.** C'è già una proposta (DA-27, `PIANO-DIVERSIFICAZIONE.md`): EURUSD, S&P 500, argento, GBPUSD e USDJPY, DAX, petrolio; cripto alla fine. Da confermare e legare alle **famiglie di correlazione**.
2. **Riserva: una per mercato o una condivisa**, e come trattare i mercati correlati sulle stesse date. Oggi il registro consuma per calendario; serve la regola per più mercati.
3. **N globale su tutti i mercati** (DA-28): da ratificare.
4. **Quando spostare il peso sulla demo in avanti** come prova principale, invece dello storico.

**Niente di tutto questo cambia l'ordine di oggi:** prima la macchina, poi Brad come caso pilota, poi la fabbrica. La visione ampia **non accelera** il primo passo; lo rende più sensato, perché il primo passo è già costruito per reggere tutto il resto.
