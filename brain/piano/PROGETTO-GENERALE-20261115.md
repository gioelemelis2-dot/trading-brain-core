<!-- Esportato dal documento condiviso «Trading Brain — Progetto generale» (claude.ai), revisione 45, il 15/11/2026. Gli schemi sono trascritti in testo. -->
# Trading Brain — Progetto generale

Nov 13, 2026 · l'utente

## Scopo e principi

Il Trading Brain è un ecosistema pluriennale di studio, ricerca quantitativa e controllo del rischio, pensato per arrivare a operare su un conto prop firm finanziato. Le AI ricercano entro perimetri autorizzati; ogni decisione rilevante e ogni accesso a denaro reale spettano all'utente (D-14).

**Quattro pilastri**

| Pilastro | Cosa fa | Dove vive |
| --- | --- | --- |
| Conoscenza | Manuale, moduli didattici, glossario, bibliografia | `brain/moduli`, `architettura`, `glossario`, `bibliografia` |
| Ricerca | Dati reali, laboratorio di backtest, conteggio delle prove (DSR) | `brain/dati`, `brain/laboratorio` |
| Protezione | Guardian G0 (limiti e regole personali) e journal | `brain/guardian` |
| Governance | Decisioni, standard, registri, continuità | `brain/governance`, `CONTINUITA.md` |

**Cosa non è**

- Non è consulenza finanziaria, fiscale o legale.
- Non è un sistema di trading automatico: nessun ordine parte dal Brain.
- Non opera con denaro reale senza autorizzazione esplicita dell'utente, gate per gate.

**Principi che non cambiano**

1. Decide l'utente. Le AI propongono, verificano e documentano.
2. Ogni numero ha un tipo: MISURA, DERIVATO, STIMA o IPOTESI (più REGOLA). Un risultato vale quanto il suo input più debole.
3. Nessun dato inventato. I dati simulati servono solo ai test e sono etichettati (D-04, D-05).
4. Prima i limiti deterministici, poi le probabilità: una stima può solo restringere un limite, mai allargarlo.
5. Tutto è riproducibile: test automatici, hash, manifest, storia git.
6. L'Out-of-Sample si sigilla prima di qualsiasi backtest e si apre una volta sola.
7. Claude e Gemini sono due centri di ricerca indipendenti e simmetrici; il sistema non dipende da un singolo fornitore (D-15).
8. Il Guardian avvisa e registra, non blocca (D-16).

## Obiettivi dell'utente e valutazione

L'obiettivo è un conto FTMO reale, ma solo dopo un vantaggio statistico dimostrato dai dati e una lunga incubazione su più conti demo gratuiti; poi la semi-automazione. Non c'è una data: il calendario lo decidono il criterio di promozione (DA-20) e lo storico raccolto nell'incubazione.

| Tema | Risposta dell'utente (13/11/2026) | Valutazione di Claude |
| --- | --- | --- |
| Obiettivo | FTMO solo dopo una lunga incubazione su più conti demo gratuiti di broker diversi, quando lo storico raccolto lo giustifica; nessuna fretta | Scelta corretta: l'incubazione lunga dà i trade che servono e confronta costi ed esecuzione di broker diversi. Due cautele: ogni strategia provata su ogni conto si conta nel registro delle prove, e un conto demo esegue meglio di uno reale (slippage e rifiuti d'ordine ridotti). La cosa più probabile è che le prime ipotesi falliscano: è il sistema che funziona, non un fallimento del progetto |
| Vantaggio statistico | Prima va dimostrato con i dati | Giusto. La prova viene dal backtest con Out-of-Sample sigillato; il demo da solo non può dimostrarlo (vedi «Quanto serve per validare una strategia») |
| Stile e timeframe | Misto; i timeframe dipendono dalle strategie | Ragionevole. Ma con 3 anni di dati su un solo strumento, una strategia da un trade a settimana non è validabile: troppi pochi trade |
| Strumenti | Scelti un po' alla volta, senza sovraccaricare | Giusto: ogni strumento in più moltiplica le prove, e quindi i trade necessari |
| Automazione | Obiettivo finale, appena i dati convincono | È un percorso a parte, con gate propri: oggi il Guardian non può bloccare né inviare ordini (D-16) e il laboratorio dei bot è sospeso (D-20) |
| Budget e piano di accumulo | Da ragionare insieme partendo dallo stipendio | Da fare prima del Gate 6. Stipendio e spese sono dati personali: restano fuori dal repository |
| Perdita massima | 1,5% al giorno (chiarito il 13/11/2026); il valore può cambiare con la strategia | Coincide con P-05, già confermata (750 USD su 50.000). Il limite totale resta quello interno del 10% (5.000 USD). Se cambia la strategia, cambia con la procedura DA-23, mai durante una sessione |
| TradingView | Già in uso per l'analisi dei grafici | Resta lo strumento per vedere; il motore per provare è il laboratorio (D-18) |
| Gemini | Continua a lavorare con Claude; compito da definire | In attesa del compito |
| Revisori | ChatGPT e DeepSeek | Utile: sono fornitori diversi. Va mandato loro solo il documento, senza dati personali |
| Preoccupazione | Essere presi in giro | Vedi gli impegni qui sotto |
| Esperienza | Circa 2 anni di trading, risultati altalenanti, strategie passate non profittevoli; si descrive emotivo e impulsivo | È proprio il caso per cui servono regole scritte, Guardian e semi-automazione. I risultati passati non contano come prova né a favore né contro nessuna idea: si riparte dai dati |
| Idee di partenza | Fibonacci e order block, anche insieme, più nuovi modi di leggere il mercato da cercare insieme; dettagli al momento delle ipotesi | Diventano ipotesi da scrivere in regole meccaniche e sigillare prima di guardare i dati. Le «nuove letture» vanno tenute in un numero limitato e deciso prima, altrimenti ogni tentativo in più alza i trade necessari |

**Impegni contro la compiacenza**

- Nessun risultato senza la prova che lo riproduce: test, hash, comando da rilanciare.
- Ogni fallimento si scrive e si conta, come i successi.
- Ogni numero porta il suo tipo: un'ipotesi non si presenta mai come una misura.
- Se una richiesta è sbagliata o una scadenza irrealistica, Claude lo dice prima di eseguire.
- I rilievi di Gemini e dei revisori si verificano sul codice reale, mai accettati sulla parola, e lo stesso vale per quelli di Claude.

## Stato al 13/11/2026

Le fondamenta tecniche sono pronte e verificate: 118 test su 118 verdi su Python 3.13 e 3.9. Manca ancora il primo dato di mercato reale (Gate 2, scaricamento in corso sul Mac), quindi nessuna strategia è stata testata.

| Componente | Stato | Prove | Limite principale |
| --- | --- | --- | --- |
| Repository `trading-brain-core` | Attivo, unica fonte di verità (D-19) | Storia completa su `main` | Rami già uniti ancora presenti su GitHub |
| Guardian G0: limiti, perdita allo stop, scheda | Operativo, consultivo | 77 test; 80/80 mutanti uccisi (3.13), 79/79 (3.9) | Non riconciliato con un estratto conto reale (DA-25) |
| Journal: catena di hash, ancora, lock, Brier, indicatore R1 | Operativo | Compreso nei 77 test | R1 spento finché l'utente non fissa i parametri |
| Regole personali | 14 confermate su 15 (P-01 = 0,5%, P-05 = 1,5%; P-02…P-14 il 13/11/2026) | Visibili nella scheda | P-15 in sospeso; 9 regole sono domande della checklist, senza controllo automatico |
| Pipeline dati: ingestione e sigillo OOS | Operativa | 13 test + 9 dello scaricamento Dukascopy | Formato Dukascopy dedotto, controllato ma non documentato |
| Laboratorio: backtester a eventi e DSR | Operativo | 19 test; ALTO-2 e ALTO-7 verificati da Claude | Mutazioni del laboratorio dichiarate da Gemini, non rieseguite da Claude |
| Gate 1: conto demo broker ECN MT5 da 50.000 USD | Configurato | Scheda G0 funzionante | Specifiche XAU/USD e commissione da verificare sul broker |
| Gate 2: storico XAUUSD 15 minuti | In corso sul Mac | Circa il 95% dei giorni scaricati | `commitment.json` non ancora creato |
| Gate 3: journal operativo e registro delle prove | Inizializzati, vuoti | Registro letto dal calcolatore DSR | Nessuna prova registrata |
| Conoscenza: Modulo 2, lezioni L2.1–L2.6 | In verifica | Registro delle conoscenze | Altri moduli sospesi (D-20) |
| Simulatore prop V3.3 di Gemini | Congelato con riserve (D-17) | Revisione ed errata T-01…T-05 | Non è il motore di ricerca: è un riferimento storico |

## Architettura

La ricerca non tocca mai il conto, e sul conto non parte nessun trade senza la scheda del Guardian. Le due parti si parlano solo attraverso due passaggi controllati: la strategia candidata e il journal.

**[Schema dell'architettura, trascritto da Claude il 15/11/2026]** La ricerca produce le candidate, il conto demo le prova sotto il Guardian.
- **Conoscenza** (vale per tutto): manuale v1, moduli, glossario, bibliografia (Modulo 2 in verifica).
- **Ricerca:**
  1. Dati storici e sigillo OOS: Dukascopy XAUUSD 15m, controlli, ingestione; «IS 70% / OOS 30%, sigillo commitment.json».
  2. Laboratorio: backtester a eventi con costi espliciti; registro delle prove e Deflated Sharpe.
  3. Strategia candidata: criterio DA-20 in IS, poi OOS una volta (Gate 3 e Gate 4).
- **Operatività sul conto demo:** Guardian G0 consultivo (scheda pre-trade, limiti, perdita allo stop; regole personali: avvisa, non blocca) → conto demo MT5 da 50.000 USD (l'utente decide ed esegue; XAU/USD, commissione ECN 7 USD/lotto) → journal (trade, decisioni, previsioni, stato; catena di hash, Brier, indicatore R1).
- **Frecce:**
  - la candidata passa al Guardian;
  - il journal riporta i risultati al laboratorio.
- **Governance** (decisioni, standard, registri, CONTINUITA.md). **Persone:** decide l'utente; Claude e Gemini ricercano.
- *Nota di Claude: «IS 70% / OOS 30%» è SUPERATO dalla decisione DA-26 del 14/11 (sviluppo dal 15/11/2023, verifica sigillata 2005 → circa 31/10/2023). Broker demo: FP Markets (DA-25).*

Una strategia nasce dai dati sigillati, passa il criterio di promozione e arriva al Guardian. Ogni trade sul conto demo finisce nel journal, che riporta i risultati reali al laboratorio. Conoscenza, governance e persone valgono per tutte le parti.

## Percorso a gate

I Gate 0 e 1 sono chiusi e il 2 è in corso; i Gate 3–7 sono una proposta di Claude da approvare. Ogni gate ha un criterio di uscita misurabile, e nessuno si salta.

**[Schema del percorso a gate, trascritto da Claude il 15/11/2026]** Due gate chiusi, uno in corso, cinque proposti fino al conto finanziato.
| Gate | Stato (13/11) | Contenuto | Esce quando |
|---|---|---|---|
| 0 · Verifica del codice | chiuso 12/11 | Guardian e Binario B su main; ALTO-2 e ALTO-7 verificati con controesempi indipendenti | 108/108 test verdi con -W error su Python 3.13 e 3.9 |
| 1 · Conto demo e regole personali | chiuso 12/11 | Conto demo broker ECN MT5 da 50.000 USD, XAU/USD; regole interne 5% giornaliero e 10% totale | scheda G0 funzionante con P-01 = 0,5% e P-05 = 1,5% confermate |
| 2 · Dati storici e sigillo Out-of-Sample | in corso | XAUUSD 15 minuti da Dukascopy; partizione da decidere (DA-26) | partizione decisa, dati sigillati, meta.json e commitment.json verificati su GitHub |
| 3 · Ricerca In-Sample | proposto | prima DA-19 e DA-20 decisi; ogni ipotesi scritta e sigillata, ogni prova contata | una candidata supera il criterio DA-20 sui soli dati In-Sample |
| 4 · Validazione Out-of-Sample | proposto | sigillo aperto una volta sola; se non regge si torna al Gate 3, prova contata | il criterio regge anche Out-of-Sample |
| 5 · Incubazione su più conti demo gratuiti | proposto | broker diversi; scheda G0 e journal su ogni conto; costi verificati | ogni strategia ha almeno 100 trade e 3 mesi; costi e aderenza come nel backtest |
| — | soglia | **da qui si spende denaro reale (costo della sfida): serve l'autorizzazione esplicita dell'utente (D-14)** | — |
| 6 · Sfida prop firm | proposto, con autorizzazione | prodotto da scegliere (es. FTMO 2-Step); regole rilette sul sito ufficiale | sfida superata senza violare i limiti FTMO né le regole personali |
| 7 · Conto finanziato | proposto, con autorizzazione | operatività con il capitale della prop, sempre con scheda G0 e journal | si torna al Gate 5 se le metriche peggiorano oltre la soglia decisa in anticipo |

*Note di Claude (15/11):*
- *Gate 2:* la partizione è decisa (DA-26: inversione); 3 anni BID e ASK scaricati; lo storico BID dal 2005 è in corso sul Mac; gli ASK storici vanno ancora scaricati.
- *Gate 3:* la «ricerca In-Sample» ora si chiama «screening sullo sviluppo». H-002 è la prima ipotesi ed è in revisione prima del sigillo.
- *Gate 5:* il nome «easyMarkets» è superato (l'utente non ha quel conto); il broker demo è FP Markets (DA-25).

Un gate fallito non si ripete con altre prove nascoste: si torna indietro e la prova resta contata nel registro. La linea tratteggiata segna il primo costo reale: la sfida della prop firm, che richiede l'autorizzazione esplicita dell'utente.

## Quanto serve per validare una strategia

Per un vantaggio modesto servono circa 600 trade con una sola prova, e circa 1.300 dopo 20 prove. Il conto demo non basta a dimostrarlo: la prova viene dal backtest con Out-of-Sample sigillato; il demo misura costi, esecuzione e disciplina.

**Formula:** n = \[ (z(1 − α/N) + z(1 − β)) / SR \]²

n = trade necessari; SR = media divisa per la deviazione del risultato per trade, in R (1R = il rischio del trade); test a una coda al 5% (alpha), potenza 80% (beta = 0,20), N = prove fatte (correzione di Bonferroni, prudente; il Deflated Sharpe del laboratorio è più preciso). I profili sono IPOTESI illustrative, non strategie esistenti.

| Profilo (ipotesi) | Media per trade | SR per trade | Trade, 1 prova | Trade, 20 prove | Trade, 100 prove |
| --- | --- | --- | --- | --- | --- |
| 60% vincenti, 1:1, senza costi | +0,200R | 0,20 | 148 | 320 | 410 |
| 60% vincenti, 1:1, costi 0,05R | +0,150R | 0,15 | 264 | 568 | 729 |
| 40% vincenti, 2:1, senza costi | +0,200R | 0,14 | 334 | 719 | 922 |
| 40% vincenti, 2:1, costi 0,05R | +0,150R | 0,10 | 594 | 1.278 | 1.639 |
| 55% vincenti, 1:1, senza costi | +0,100R | 0,10 | 612 | 1.318 | 1.690 |
| 55% vincenti, 1:1, costi 0,05R | +0,050R | 0,05 | 2.448 | 5.272 | 6.762 |

Con 250 USD di rischio a trade, 0,05R sono 12,50 USD fra spread, commissione e slippage: i costi reali di XAU/USD vanno misurati sul demo. Pochi centesimi di R di costi possono quadruplicare i trade necessari.

| Frequenza | Trade In-Sample (2,1 anni) | Trade Out-of-Sample (0,9 anni) | Trade in 3 mesi di demo |
| --- | --- | --- | --- |
| 2 al giorno | \~1.050 | \~450 | \~125 |
| 1 al giorno | \~525 | \~225 | \~62 |
| 3 a settimana | \~315 | \~135 | \~38 |
| 1 a settimana | \~109 | \~47 | \~13 |

**Cosa ne segue**

- Strategie intraday (1–2 trade al giorno): i 3 anni bastano per vantaggi medio-forti (SR per trade da 0,14 in su), non per un vantaggio da 0,10 dopo molte prove.
- Strategie settimanali: non validabili con 3 anni di un solo strumento. Servono più anni di storico o la stessa regola su più strumenti.
- Demo: con 100 trade l'intervallo al 95% della media è ±0,20R, più largo del vantaggio stesso. Criterio proposto per il Gate 5: almeno 100 trade e almeno 3 mesi, con costi, slippage e aderenza alle regole entro le ipotesi del backtest.
- FTMO: con lo 0,5% a trade, il target del 10% vale +20R e la perdita massima −20R. Senza vantaggio la sfida è un lancio di moneta (50%); con +0,05R a trade circa 88% in \~400 trade; con +0,10R circa 98% in \~200 trade. Stima IPOTESI (moto browniano, senza limite giornaliero né code grasse).
- Tempi: se la prima ipotesi regge, i Gate 3–4 richiedono settimane; se non regge, mesi. Il Gate 5 richiede almeno 3 mesi. Per scelta dell'utente non c'è una data: FTMO arriva quando l'incubazione su più conti demo ha prodotto uno storico sufficiente.

## Regole permanenti

Queste regole valgono per ogni gate e ogni componente; cambiarle richiede una decisione scritta dell'utente nel registro `DECISIONI.md`.

| Area | Regola | Fonte |
| --- | --- | --- |
| Capitale | Nessuna operazione con denaro reale senza autorizzazione esplicita, data per un gate preciso | D-14 |
| Capitale | Il Guardian è consultivo: calcola, avvisa, registra; livelli che bloccano (G1, G2) solo con nuova autorizzazione | D-16 |
| Dati | Nessun dato inventato; dati simulati solo nei test, etichettati | D-04, D-05 |
| Dati | Dati a costo zero finché una strategia non merita un test serio | D-21 |
| Dati | Dati personali (journal, stato, conto) mai su git né inviati a servizi esterni senza consenso | DA-16, `.gitignore` |
| Ricerca | Out-of-Sample sigillato con `commitment.json` prima di ogni backtest; aperto una sola volta | Pipeline dati |
| Ricerca | Ogni prova di ricerca va contata nel registro delle prove (DSR), anche se fallisce | DA-19 |
| Qualità | Ogni modifica al codice in TDD: test rosso, poi correzione, poi mutation testing su Python 3.13 e 3.9 | Prassi del Binario A |
| Qualità | Lavoro su un ramo dedicato; merge su `main` solo dopo verifica e autorizzazione | Prassi del Binario A |
| Collaborazione | Nessuno modifica i materiali dell'altro centro di ricerca; si integra solo con proposte documentate | D-11, D-15 |
| Regole personali | Si cambiano solo a mercato chiuso, per iscritto, con versione | DA-23 |
| Storia | Nessun documento si cancella: si corregge con note datate (es. V3.3 congelata, errata separata) | README, D-17 |

## Regole personali: proposta per P-02…P-15

P-02…P-14 vengono dal Manuale v1 dell'utente (lezioni 8, 21 e 22); solo P-15 viene dal vecchio rulebook di Gemini. La proposta di Claude è stata confermata dall'utente il 13/11/2026: 12 regole attive, cinque con un valore numerico; P-15 resta in sospeso. Ogni cambio futuro segue la procedura DA-23.

| Regola | Testo | Origine | Proposta di Claude | Controllo automatico |
| --- | --- | --- | --- | --- |
| P-02 | Stop deciso prima dell'ingresso e inserito subito; non si allarga mai | Manuale, L8 | Confermare | Da aggiungere: il journal confronta lo stop iniziale con quello finale |
| P-03 | Nessun ingresso senza checklist pre-trade | Manuale, L8 | Confermare: la scheda del G0 è la base della checklist | Parziale |
| P-04 | Solo i setup scritti; fuori dalle regole si sta fermi | Manuale, L8 | Confermare. Finché nessuna strategia supera il Gate 4, i trade sul demo sono esercizio e non contano come prova | No |
| P-06 | Un solo rischio per fattore correlato alla volta | Manuale, L8 | Confermare: al massimo 1 posizione aperta su XAU/USD | Da aggiungere (conteggio delle posizioni) |
| P-07 | Ogni trade nel journal entro fine giornata, con stato e voto di aderenza | Manuale, L8 | Confermare | Sì, dalle date dei record |
| P-08 | Niente trade con news ad alto impatto, stanchezza, tilt, noia | Manuale, L8 | Confermare: 15 minuti prima e dopo le news ad alto impatto. È prudenza, non un risultato statistico; lo stesso filtro va applicato nel backtest | Serve un calendario delle news (fonte da scegliere) |
| P-09 | Non modifico le regole durante la sessione | Manuale, L8 | Confermare | No (procedura DA-23) |
| P-10 | Se non so perché sono in un trade, esco | Manuale, L8 | Confermare | No |
| P-11 | Dopo una perdita: 10–15 minuti fuori dallo schermo | Manuale, L21 | 15 minuti, il valore più protettivo del Manuale | Sì, già nella scheda |
| P-12 | 60–90 secondi fra «vedo il setup» e «clicco»; trade detto ad alta voce | Manuale, L21 | 60 secondi | No |
| P-13 | Dopo il kill switch, il giorno dopo a size dimezzata finché 5 trade con aderenza almeno 4 su 5 | Manuale, L21 | Confermare così com'è | Parziale (il journal ha il voto di aderenza) |
| P-14 | Meno di 6–7 ore di sonno: size ridotta o nessun trade | Manuale, L22 | 7 ore, il valore più protettivo | Sì, già nella scheda |
| P-15 | Massimo di perdite consecutive al giorno | Rulebook di Gemini, non nel Manuale | Non confermare ora: con lo 0,5% a trade, 3 perdite fanno l'1,5% e P-05 scatta comunque. Diventa utile se il rischio per trade scende | Sì, già nella scheda |

Nel file delle regole (commit 92339cb) le 12 regole sono attive; la scheda del G0 mostra «14 regole personali confermate su 15». P-11 e P-14 si controllano da sole quando la scheda riceve minuti dall'ultima perdita e ore di sonno; le altre sono domande della checklist.

## Ruoli e metodo di lavoro

Cinque ruoli, un solo repository: ognuno lavora sul proprio perimetro e consegna attraverso GitHub, con prove verificabili.

| Ruolo | Responsabilità | Perimetro | Non fa |
| --- | --- | --- | --- |
| Utente | Decide, autorizza merge e gate, conferma le regole personali, opera sulla piattaforma | Tutto | — |
| Claude (cloud) | Guardian, journal, governance, revisioni, verifica del Binario B | `brain/guardian`, governance, continuità; laboratorio e dati dal 12/11/2026 | Non tocca i materiali di Gemini; non esegue nulla sul Mac |
| Claude Code sul Mac | Compiti che richiedono il computer dell'utente: scaricamenti, MetaTrader, file locali | Cartella locale del repository | Non decide: esegue e riporta |
| Gemini (Antigravity) | Centro di ricerca simmetrico: proposte, laboratorio, audit incrociati | I propri rami e consegne | Non modifica i materiali di Claude |
| Revisori esterni (ChatGPT, Red Team) | Revisione avversariale di codice e documenti | Sola lettura | Non scrivono nel repository |

**Ciclo di ogni modifica**

1. Mandato scritto dell'utente, con perimetro e criteri di accettazione.
2. Ramo dedicato da `main` (es. `fix/...`, `feat/...`).
3. Test che falliscono, committati da soli (fase rossa).
4. Correzione fino a tutti i test verdi con `-W error` su Python 3.13 e 3.9.
5. Mutation testing: ogni mutante non equivalente deve essere ucciso; gli equivalenti si dichiarano con la motivazione.
6. Documentazione: `LEGGIMI`, `CONTINUITA.md`, voce nel `REGISTRO-MODIFICHE.md`.
7. Revisione: un altro centro o un revisore esterno; ogni rilievo si verifica sul codice reale prima di accettarlo.
8. Merge su `main` e push, solo dopo l'autorizzazione dell'utente.

## Come cresce

Il progetto cresce per aggiunte, non per riscritture: ogni espansione entra da un punto previsto, con la sua prova, senza toccare ciò che è già verificato. I formati dei file hanno una versione (`journal/1`, `TRIAL_REGISTRY_V1`, `SEALED_OOS_RESEARCH_COMMITMENT_V2`), quindi un cambio di formato è una nuova versione, mai una modifica silenziosa.

| Espansione | Cosa serve | Dove si tocca | Prova richiesta |
| --- | --- | --- | --- |
| Nuovo strumento (es. EUR/USD, NAS100) | Specifiche lette sul broker (stato V), scheda dello strumento, storico dati | Scheda in `dati/reali`, `[[strumento]]` nel TOML | Perdita allo stop calcolata a mano e confrontata con la scheda |
| Nuova fonte dati | Licenza verificata, formato controllato, metadati con SHA-256 | Nuovo modulo in `dati/pipeline`, come `dukascopy.py` | Test offline con file costruiti; controlli che fermano su dati incoerenti |
| Nuova strategia | Ipotesi scritta e sigillata prima del test; prova contata nel registro | Registro delle prove, laboratorio | Backtest solo In-Sample; Out-of-Sample aperto una volta; DSR sul numero reale di prove |
| Nuova prop firm o prodotto | Regole lette sul sito ufficiale, con data | Oggi `limiti.py` gestisce solo FTMO 2-Step, 1-Step e Instant: va aggiunto un prodotto | Esempi numerici ufficiali come test |
| Nuova regola personale | Conferma scritta dell'utente, a mercato chiuso | `guardian/regole/regole_personali.toml` e controlli della scheda | Test con soglia uguale, sopra e sotto il valore |
| Guardian che blocca (G1, G2) | Nuova decisione esplicita dell'utente | Nuovo componente, separato dal G0 | Da definire prima di scriverlo |
| Nuovo modulo didattico | Revoca mirata della sospensione | `brain/moduli` | Cancello di competenza superato |
| Nuovo centro di ricerca o modello AI | Registro di ricerca separato | Cartella di collaborazione dedicata | Confronto indipendente, senza condividere le conclusioni prima |

## Rischi e punti deboli noti

Il rischio più grande non è tecnico: è trovare una strategia che sembra funzionare solo perché ne sono state provate tante. Il secondo è che i numeri del Guardian non sono ancora stati confrontati con un conto reale.

| Rischio | Impatto | Contromisura | Stato |
| --- | --- | --- | --- |
| Out-of-Sample già visto: gli ultimi \~11 mesi sono noti all'utente (grafici) e a grandi linee a Claude (addestramento); il sigillo impedisce di cambiarli, non di guardarli | Alto: un test «fuori campione» che non lo è davvero | Più anni di storico e un periodo vecchio di verifica (DA-26); il futuro, cioè l'incubazione sui conti demo, è il test finale | Approvato il 13/11/2026; da applicare prima del sigillo |
| Sovra-adattamento (troppe prove sugli stessi dati) | Alto: strategia illusoria | Out-of-Sample sigillato, ogni prova contata, DSR sul numero reale di prove | Strumenti pronti, 0 prove registrate |
| Guardian non riconciliato con il conto | Alto: margini sbagliati in operatività | Riconciliazione con un estratto conto MT5 (DA-25) | Da fare |
| Costi reali diversi dai costi del backtest (spread, commissioni, slippage, swap) | Medio-alto | Costi espliciti nel backtester; confronto con il conto demo | Commissione 7 USD/lotto da verificare; swap non modellati |
| Una sola fonte dati, formato non documentato | Medio | Controlli che fermano su dati incoerenti; confronto a campione con i prezzi MT5 | Controlli fatti; confronto da fare |
| Comportamento (tilt, aumento della size dopo una perdita) | Alto | Regole personali con avvisi; journal con indicatori | 14 regole su 15 confermate |
| Regole della prop firm che cambiano | Medio | Regole con data di lettura e fonte; nuova verifica prima di ogni sfida | Lette il 12/11/2026 |
| Accordo apparente fra le AI (una conferma l'altra senza verificare) | Medio | Centri indipendenti, revisori esterni, ogni rilievo verificato sul codice | Prassi in uso |
| Dati personali esposti | Medio | Journal e conto fuori da git; nessun invio a servizi esterni | In uso |
| Licenza dei dati storici | Basso-medio | CSV fuori da git; termini Dukascopy da leggere | Da verificare |
| Lavoro legato a un solo computer o a una sessione | Medio | Tutto su GitHub; `CONTINUITA.md` aggiornato a ogni passo | In uso |

## Contro l'autoinganno

Il punto più debole del metodo è che i dati «sigillati» non sono ciechi: gli ultimi 11 mesi li abbiamo già visti, l'utente sui grafici e Claude nell'addestramento. Le otto contromisure qui sotto sono state approvate dall'utente il 13/11/2026.

**Punti deboli dichiarati**

- Il sigillo prova che i dati Out-of-Sample non sono stati modificati, non che nessuno li abbia guardati: il CSV completo è sul Mac.
- I test verdi provano solo i casi immaginati: lo script Dukascopy ha avuto tre difetti, due scoperti solo sul Mac.
- Formato dei dati Dukascopy dedotto; costi del broker non verificati; motore del laboratorio controllato solo sui due difetti gravi segnalati.
- I calcoli dei trade necessari sono ottimistici: trade indipendenti, niente code grasse. La realtà ne richiede di più.
- Il mutation testing prova che i test scoprono difetti inventati, non che la logica sia corretta.
- Claude tende a essere accomodante e a produrre molto: il volume di documenti e test non è progresso verso un vantaggio.

**Contromisure**

1. Il futuro è il test finale: l'Out-of-Sample storico vale come «semi-cieco»; nessuna strategia va su FTMO senza aver retto nell'incubazione sui conti demo.
2. Più anni e periodi diversi: scaricare più storico (quanto ne ha Dukascopy è da verificare) e tenere un periodo vecchio come verifica, deciso prima del sigillo (DA-26).
3. Una seconda fonte: confronto a campione dei prezzi Dukascopy con lo storico esportato da MT5.
4. Costi veri prima di qualsiasi risultato: specifiche reali dei conti demo (broker del conto MT5 50K attuale da confermare; nuovi demo, tra cui FP Markets) prima dei backtest.
5. Replica indipendente: ogni strategia programmata separatamente da Claude e da Gemini dalla stessa regola scritta; risultati diversi = errore da trovare.
6. Regole decise prima: ipotesi sigillate, numero massimo di prove per giro, confronto con ingressi casuali, criterio di arresto se non si trova nulla.
7. «Come lo sai?»: nessuna affermazione di Claude o Gemini senza un comando che la riproduce o una fonte; revisioni esterne a ogni gate.
8. Niente nuova infrastruttura finché la prima ipotesi non è stata testata.

## Diversificazione su più mercati

La diversificazione è centrale, ma moltiplica un vantaggio statistico solo se il vantaggio c'è già. Dieci strategie senza vantaggio, messe insieme, danno zero, con meno oscillazioni. Ogni mercato in più è anche un'occasione in più di trovare qualcosa per caso. Per questo il piano parte dai dati e dal conteggio delle prove, non dalle strategie. Abbiamo mesi: un mercato alla volta, con la stessa cura dell'oro.

**Cosa cambia rispetto all'oro** (verificato nel codice il 13/11/2026)

- **Lo scaricatore conosce solo XAUUSD.** La scala dei prezzi (0,001) e il controllo di plausibilità (1.000–10.000 USD) sono dell'oro. Ogni strumento ha i suoi: vanno ricavati e protetti con controlli, come per l'oro.
- **Orari diversi.** I cambi sono aperti 24 ore per 5 giorni. Indici e petrolio hanno pause ogni giorno e festività. La regola attuale sui buchi (fine settimana solo se contiene un sabato intero) va adattata a ogni strumento: altrimenti le pause normali vengono segnalate come buchi, oppure i buchi veri vengono scambiati per pause normali.
- **Il backtester segue un solo strumento alla volta.** Per un portafoglio su più mercati serve un'estensione, scritta prima nei test.
- **Il registro delle prove è per strumento** (`trial_registry_xauusd.json`). Le prove vanno contate tutte insieme, su tutti i mercati.

**Regole del piano** (proposte, da confermare)

1. **Stesso calendario per tutti i mercati:** il periodo di sviluppo e quello di verifica sono le stesse date per ogni strumento. Se studio l'euro del 2015 mentre il 2015 dell'oro è chiuso, vedo il dollaro di quell'anno, e il periodo chiuso dell'oro non è più cieco.
2. **Un mercato alla volta,** con la procedura dell'oro: controlli, buchi, metadati, sigillo.
3. **Mercati dichiarati prima.** Ogni ipotesi scrive in anticipo su quali mercati vale e con quali parametri. Un vantaggio vero deve reggere su mercati simili senza ritoccare nulla. Provare un'idea su 10 mercati e tenere i 3 dove funziona è autoinganno.
4. **Ogni coppia ipotesi–mercato è una prova** nel registro. Il totale di tutte le prove entra nel calcolo del Deflated Sharpe Ratio (DSR).
5. **La diversificazione si misura, non si presume.** Le correlazioni si calcolano sul periodo di sviluppo, guardando anche i periodi di crisi, quando i mercati tendono a muoversi tutti insieme.
6. **P-06 resta: una posizione aperta alla volta.** Per ora la diversificazione è in sequenza: mercati diversi, una posizione per volta. Più posizioni insieme solo con una modifica scritta (DA-23) e dopo l'incubazione.

**Mercati candidati.** Sono da verificare per ognuno: il codice su Dukascopy, l'anno di inizio dei dati e la disponibilità su FTMO e sui broker demo.

| Gruppo | Strumenti | Perché | Attenzione |
| --- | --- | --- | --- |
| Metalli | XAUUSD (in corso), XAGUSD | Argento: si muove per le stesse cause dell'oro, utile per provare se un'idea sull'oro regge | Molto correlato all'oro: non diversifica davvero |
| Cambi principali | EURUSD, GBPUSD, USDJPY, AUDUSD | Costi bassi, mercato aperto 24 ore per 5 giorni, storico lungo | Dipendono tutti dal dollaro |
| Indici azionari | S&P 500, Nasdaq 100, DAX | Si muovono per ragioni diverse dai cambi | Orari di sessione, festività, salti all'apertura |
| Energia | Petrolio WTI o Brent | Dipende dall'offerta, non dai tassi | Scadenze dei contratti dentro i CFD, salti di prezzo |
| Cripto | BTCUSD (forse, più avanti) | Aperta 7 giorni su 7 | Storico breve, regole FTMO diverse |

Ordine proposto:

1. EURUSD;
2. S&P 500;
3. XAGUSD, come prova di robustezza delle idee sull'oro;
4. GBPUSD e USDJPY;
5. DAX e petrolio;
6. le cripto solo alla fine, se ha senso.

**Tempi** (stime)

- **Oro:** 3 anni sono circa 1.100 richieste. Sul Mac sono servite più di 12 ore, per i blocchi di Dukascopy.
- **Tutti i mercati:** 10 mercati per 15 anni sono circa 55.000 richieste. Con la sola pausa di 1,5 secondi fanno almeno 23 ore; con i blocchi, qualche settimana di notti.
- Un mercato a settimana va benissimo. Lo spazio su disco è poco, ma la cache resta fuori da git.

**Cosa serve, oltre ai prezzi, per avere idee e provarle bene**

| Cosa | A cosa serve | Da dove | Stato |
| --- | --- | --- | --- |
| Seconda fonte di prezzi per ogni mercato | Scoprire errori nei dati | Storico MT5 dei broker demo | Da fare |
| Costi reali per mercato e per ora: spread, commissione, swap | Un vantaggio piccolo sparisce con i costi | Conti demo, registrando lo spread nelle varie ore | Da fare |
| Calendario storico delle notizie | P-08 e test intorno alle notizie | Fonte da trovare e verificare | Aperto |
| Orari, festività, ora legale per mercato | Riconoscere i buchi e le sessioni | Specifiche dei broker | Da fare |
| Definizioni scritte di Fibonacci e order block | Trasformarli in regole che si possono provare | Tu, prima di guardare i dati | Quando decidi |
| Effetti già noti nella letteratura (momentum, stagionalità delle sessioni, giorni della Fed) | Fonte di ipotesi | Articoli pubblicati | Da raccogliere; gli effetti pubblicati tendono a ridursi dopo la pubblicazione (McLean e Pontiff, 2016) |
| Journal dei conti demo | Idee dai tuoi errori e dalle tue intuizioni | Journal | Attivo |

**Fasi**

| Fase | Cosa | Finisce quando |
| --- | --- | --- |
| D0 | Oro: DA-26 decisa, sigillo definitivo | `commitment.json` pubblicato |
| D1 | Scaricatore per più strumenti: scala, prezzi plausibili, orari e festività per ognuno | Test verdi su Python 3.13 e 3.9, una richiesta di prova per strumento |
| D2 | Download, un mercato alla volta, con lo stesso calendario | Metadati e sigillo per ogni mercato |
| D3 | Seconda fonte e costi reali per ogni mercato | Confronto Dukascopy–MT5 entro una tolleranza decisa prima |
| D4 | Un solo registro delle prove; backtester su più strumenti | Solo dopo la prima ipotesi testata sull'oro (contromisura 8); test e mutation testing passati |
| D5 | Ipotesi con i mercati dichiarati prima, provate; Gemini replica in modo indipendente | Criteri di DA-20 rispettati |
| D6 | Portafoglio: correlazioni, rischio totale entro l'1,5% al giorno | Durante l'incubazione demo |

Nuove decisioni: **DA-27** (mercati, ordine, calendario comune) e **DA-28** (registro unico, mercati dichiarati prima).

## Decisioni aperte

Quattro decisioni bloccano i prossimi gate: il criterio per promuovere una strategia (DA-20), come contare le prove (DA-19), la riconciliazione del conto (DA-25) e la regola sui segnali di TradingView (DA-14). Le altre migliorano il metodo ma non fermano il lavoro. Già decise: DA-01, DA-03, DA-11, DA-15.

| ID | Decisione | Serve per | Note |
| --- | --- | --- | --- |
| DA-26 | Partizione dei dati prima del sigillo: quanti anni, quale periodo di sviluppo, quale periodo vecchio di verifica | Gate 2 | Nuova, dal 13/11/2026: il sigillo sui 3 anni con 70/30 resta provvisorio finché non è decisa |
| DA-20 | Criterio unico per promuovere una strategia da ricerca a «candidata forward», fissato prima dei test | Gate 4 | Proposta: DSR, potenza statistica, robustezza ai parametri, costi realistici, criteri di falsificazione |
| DA-19 | Conteggio delle prove di ricerca: tutte le varianti eseguite, di entrambi i modelli, in un registro unico | Gate 3 | Registro già inizializzato, da adottare come regola |
| DA-25 | Dati del conto per completare e riconciliare il G0 | Gate 5 | Conto demo configurato; manca l'estratto conto per il confronto |
| DA-14 | Nessun segnale Pine a mercato senza essere specificato, testato e riprodotto dal motore locale | Gate 5 | Proposta condivisa da Claude e Gemini |
| DA-07 | Stime sigillate prima di ogni confronto fra i due modelli | Gate 3 | Il meccanismo esiste già nel journal |
| DA-22 | Impedire che un centro legga il registro dell'altro prima del proprio impegno sigillato | Gate 3 | Legata a DA-07 |
| DA-21 | Dati point-in-time: revisioni, contratti continui, ora legale | Nuovi strumenti | Per XAU/USD spot il rischio è basso |
| DA-12 | Indicatori comportamentali del Guardian (R1 e successivi) | Gate 5 | R1 esiste ed è spento senza parametri |
| DA-23 | Procedura per cambiare una regola personale | Sempre | Regola già scritta nel file; da formalizzare |
| DA-24 | Dove conservare i dati del journal | Gate 3 | Di fatto: in locale, fuori da git; da confermare |
| DA-13 | Formato del rulebook e verifica delle regole della prop firm | Gate 6 | Regole FTMO verificate il 12/11/2026 |
| DA-17 | Revisione delle vecchie schede strategia e regola sulla contaminazione | Gate 3 | Da decidere prima di guardare i dati In-Sample |
| DA-05, DA-06, DA-09 | Struttura dei laboratori, modello epistemico a 5 o 7 tipi, compendio delle discipline | Metodo | Non bloccano |
| DA-02, DA-04, DA-08, DA-10, DA-16, DA-18 | Testi fondativi, aggiunte non distruttive, proposta Parte B, revisione esterna, raccolta precoce dei dati, correzioni minori | Metodo | Non bloccano |
| DA-27 | Mercati della diversificazione: quali, in che ordine, stesso calendario di sviluppo e verifica per tutti | Diversificazione (D1–D2) | Nuova, dal 13/11/2026: proposta nella sezione «Diversificazione su più mercati» |
| DA-28 | Registro unico delle prove su tutti i mercati; mercati di ogni ipotesi dichiarati prima | Gate 3 | Nuova, dal 13/11/2026: lega DA-19 alla diversificazione |
| DA-29 | Obiettivi in numeri e criteri di arresto. Deciso: weekend chiuso, obiettivo in positivo (1–2% al mese va bene), challenge solo dopo più strategie testate. Proposti: soglia +0,05R netti a trade, arresto in demo a −10R o aspettativa ≤ 0 dopo 100 trade, massimo 20 ipotesi a giro, prime ipotesi solo intraday | Gate 3 | Nuova, dal 13/11/2026: completa DA-20; parte decisa, parte da confermare |

## Prossimi passi

In ordine: prima si chiude il Gate 2, poi si fissano le regole della ricerca, e solo dopo si scrive la prima ipotesi. Invertire l'ordine renderebbe i risultati non credibili.

- [ ] &#91;Superato dall'inversione di DA-26 del 14/11: il sigillo 70/30 non si pubblica\] Finire lo scaricamento XAUUSD 15m sul Mac e pubblicare `XAUUSD_15m.meta.json` e `commitment.json` (utente con Claude Code sul Mac)
- [ ] Verificare metadati e sigillo, registrare date In-Sample e Out-of-Sample, chiudere il Gate 2 (Claude)
- [ ] Decidere come contare le prove (DA-19) e il criterio di promozione di una strategia (DA-20), prima di qualsiasi backtest (utente, su proposta di Claude e Gemini)
- [ ] Riconciliare la scheda del conto demo con MetaTrader 5: estratto conto, specifiche XAU/USD, commissione reale (DA-25)
- [ ] Confrontare a campione i prezzi Dukascopy con quelli del broker MT5, per misurare la differenza di fonte
- [ ] Decidere le regole personali successive: pausa dopo una perdita (P-11), ore di sonno (P-14), perdite consecutive (P-15)
- [ ] Scrivere la prima ipotesi di strategia, sigillarla e registrarla come prova n. 1 (apertura del Gate 3)
- [ ] Far revisionare questo documento da almeno un revisore esterno (prompt nella sezione successiva)
- [ ] Togliere da GitHub i rami già uniti a `main`

Aggiunti dopo le risposte dell'utente del 13/11/2026:

- [x] Chiarire «perdita massima 1,5»: al giorno (è già P-05) o totale (incompatibile con lo 0,5% a trade)
- [x] Confermare o correggere la proposta su P-02…P-15 (sezione «Regole personali: proposta»)
- [ ] Ragionare insieme sul piano di accumulo e sul budget per le sfide, prima del Gate 6, tenendo stipendio e spese fuori dal repository
- [ ] Definire il compito di Gemini
- [ ] Disegnare il percorso dell'automazione con i suoi gate (simulazione, demo automatico, reale), da approvare dopo il Gate 5

Aggiunti con le contromisure contro l'autoinganno (13/11/2026):

- [x] Non pubblicare il sigillo dei 3 anni come definitivo: è provvisorio fino alla decisione DA-26
- [x] Verificare da quale anno Dukascopy ha lo storico XAUUSD (sul Mac, una richiesta di prova)
- [x] Decidere la partizione (DA-26): anni totali, periodo di sviluppo, periodo vecchio di verifica
- [ ] Scaricare gli anni in più (i 3 già in cache non si riscaricano) e sigillare secondo DA-26
- [ ] Esportare da MT5 lo storico XAUUSD di un periodo breve, per il confronto con Dukascopy

Aggiunti con il piano di diversificazione (13/11/2026), dopo il sigillo dell'oro:

- [ ] Decidere i mercati, l'ordine e il calendario comune (DA-27) e il registro unico (DA-28)
- [ ] Una richiesta di prova per ogni mercato candidato: codice, anno di inizio, scala dei prezzi
- [ ] Estendere lo scaricatore a più strumenti, prima nei test
- [ ] Scaricare e sigillare un mercato alla volta, con lo stesso calendario
- [ ] Raccogliere da ogni broker demo le specifiche e lo spread per ora, per ogni mercato

**Aggiornamento del 14/11/2026.** Fatti:

- 3 anni BID scaricati e controllati;
- inversione dei dati decisa (DA-26): sviluppo dal 15/11/2023, verifica sigillata 2005–2023;
- prezzi ASK aggiunti allo scaricatore;
- Studio 1 sulle sessioni: nessuna direzione diversa dal caso, volatilità fra le 14 e le 17 italiane;
- indicatore TradingView solo visivo;
- arresto in demo con test di Wald (DA-29);
- H-001 da automatizzare (DA-30);
- H-002 (rottura del range di Londra) rivista da DeepSeek e Gemini.

Da fare:

- [ ] Scaricare gli ASK dei 3 anni recenti, poi lo storico BID dal 2005, poi gli ASK storici (Mac)
- [ ] Contare i buchi per anno e fissare le date esatte della verifica sigillata (DA-26)
- [ ] H-002: versione 2, ultima rilettura, sigillo; simulatore minuto per minuto BID/ASK in TDD; test sullo sviluppo
- [ ] H-001: le 4 risposte dell'utente, poi la scheda completa
- [ ] Dire il broker del conto demo da 50.000 USD e riconciliare la scheda (DA-25)
- [ ] Aprire la demo FP Markets e misurare spread e commissione di XAUUSD per ora del giorno
- [ ] Decidere DA-14, DA-17, DA-19, DA-20 e DA-23
- [ ] Verificare le FAQ FTMO (overnight, weekend, notizie, leva) e aggiornare le regole del G0
- [ ] Trovare una fonte di calendario storico delle notizie (P-08)
- [ ] Iniziare a usare la scheda del G0 e il journal con la prima demo

**Aggiornamento del 15/11 (mandato notturno su H-002).** Fatti, sul ramo `feat/esecutore-h002`, non unito a main:

- programma dei criteri completo (§6–§8 della scheda v3.1), riusabile per le ipotesi future, in `laboratorio/esecuzione/`;
- prove su mercati inventati: casuale bocciato (R medio −0,03), vantaggio noto trovato (R medio 0,25 e 0,34), sola tendenza bocciata;
- strumento di sigillo pronto ma non eseguito: il registro delle prove non esiste ancora;
- 49 test verdi su Python 3.13 e 3.9; mutation testing 56 mutanti, primo giro 55/56, il sopravvissuto ucciso con un test nuovo;
- 11 ambiguità della scheda annotate con proposte (A1–A11 in `H-002-REVISIONI.md`), scheda non toccata;
- quaderno delle ipotesi Q-01…Q-10, solo dalla letteratura (`QUADERNO-IPOTESI.md`).

Da decidere:

- [ ] Revisioni R7 del programma (Gemini, DeepSeek, ChatGPT)
- [ ] Decisioni sulle ambiguità A1–A11 ed eventuale v3.2 della scheda
- [ ] Merge del ramo e sigillo di H-002 (decide l'utente)
- [ ] Data esatta della fine della verifica (DA-26) prima del sigillo
- [ ] Overnight e weekend: senza una decisione restano bloccate Q-02, Q-08 e Q-10
- [ ] Prossima idea da scrivere come scheda: proposta Q-01 (momento intraday)

## Prompt di revisione

Due testi pronti da copiare. Il primo lo compili tu e lo mandi a Claude: le risposte rendono specifici i gate 3–7, oggi solo proposti. Il secondo va a un revisore esterno (ChatGPT, Gemini o una persona), insieme al link di questo documento.

**1. Domande per l'utente** (compila e manda a Claude)

```markdown
Risposte per il progetto Trading Brain

1. Obiettivo finale: quale prop firm e quale prodotto (es. FTMO 2-Step 100.000 USD)? Entro quando?
2. Stile: discrezionale, sistematico o misto? Su quali timeframe e in quali orari operi?
3. Strumenti: solo XAU/USD o anche altri? In che ordine di priorità?
4. Tempo disponibile: quante ore al giorno e quanti giorni a settimana?
5. Budget: quanto puoi spendere per sfide prop e dati, e da quando?
6. Rischio: oltre a P-01 (0,5%) e P-05 (1,5%), qual è la perdita massima che accetti sul conto prima di fermarti?
7. Forward test sul demo: per quanto tempo, o per quanti trade, prima di passare alla sfida?
8. TradingView: lo usi già? Per cosa (grafici, Pine, alert)?
9. Regole personali: quali fra P-02 e P-15 vuoi confermare adesso, e con quali valori?
10. Gemini: continua come secondo centro di ricerca? Su quali parti?
11. Chi altro rivedrà il progetto?
12. Che cosa ti preoccupa di più, oggi?
```

**2. Prompt per un revisore esterno**

```markdown
Sei un revisore avversariale di progetti di ricerca quantitativa e gestione del rischio nel trading.
Ti allego il documento «Trading Brain — Progetto generale». Non riassumerlo e non lodarlo.

Cerca, con riferimento alla sezione esatta:
1. Incoerenze fra principi, regole permanenti, gate e prossimi passi.
2. Criteri di uscita dei gate mancanti, vaghi o non misurabili.
3. Rischi statistici: sovra-adattamento, data snooping, sopravvivenza, costi irrealistici, dati non point-in-time.
4. Rischi operativi e comportamentali non coperti dal Guardian o dal journal.
5. Punti in cui il progetto non può crescere senza riscritture.
6. Decisioni aperte che dovrebbero essere bloccanti e non lo sono, o il contrario.

Per ogni rilievo: gravità (CRITICO, ALTO, MEDIO, BASSO), sezione, problema in una frase,
prova o controesempio, correzione proposta. Ordina per gravità.
Se un punto ti è indifferente o lo ritieni corretto, non citarlo.
```

## Fonti

Tutto viene dal repository privato `gioelemelis2-dot/trading-brain-core`, ramo `main`, commit `7154e1c` (13/11/2026). I gate 3–7 e il criterio della tabella dei gate sono proposte di Claude, non decisioni.

- [CONTINUITA.md](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/CONTINUITA.md): stato e gate
- [DECISIONI.md](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/governance/DECISIONI.md): decisioni D-01…D-23
- [DECISIONI-APERTE.md](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/governance/DECISIONI-APERTE.md): DA-01…DA-25
- [REGISTRO-MODIFICHE.md](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/governance/REGISTRO-MODIFICHE.md): storia v1.12…v1.19
- [guardian/LEGGIMI.md](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/guardian/LEGGIMI.md): Guardian G0, test e mutazioni
- [regole\_personali.toml](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/guardian/regole/regole_personali.toml): P-01…P-15
- [demo\_broker\_mt5\_50k\_xauusd.toml](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/dati/reali/demo_broker_mt5_50k_xauusd.toml): scheda del Gate 1
- [dukascopy.py](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/dati/pipeline/dukascopy.py): scaricamento del Gate 2
- [Roadmap V2 di Gemini](https://github.com/gioelemelis2-dot/trading-brain-core/blob/main/brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md): fasi 0–10 e criteri di passaggio
