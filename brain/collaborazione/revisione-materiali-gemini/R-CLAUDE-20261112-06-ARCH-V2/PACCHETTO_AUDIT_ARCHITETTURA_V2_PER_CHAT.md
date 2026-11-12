# Audit indipendente della revisione architetturale V2 del Trading Brain

**Documento di trasmissione** · Autore dei contenuti: Claude Code · Data: 12/11/2026

## Contesto
Il Trading Brain è un progetto di ricerca quantitativa sul trading, in lingua italiana, con due modelli di ricerca indipendenti: Claude Code e Gemini Antigravity. Il proprietario umano prende tutte le decisioni.

Gemini ha consegnato una revisione dell'architettura e della roadmap pluriennale, composta da tre documenti:
- `TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md`;
- `TRADING_BRAIN_CLAIMS_AUDIT_V1.md`;
- `TRADING_BRAIN_ARCHITECTURE_CHANGELOG_V2.md`.

Su incarico dell'utente, Claude ne ha condotto un audit indipendente e avversariale. Questo file raccoglie, **senza modifiche**, i tre documenti prodotti.

## Contenuto
1. `CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md`: rapporto completo dell'audit.
2. `CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md`: verifica delle 16 affermazioni di Gemini, delle affermazioni aggiuntive e delle fonti.
3. `CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md`: registro delle divergenze tra Claude e Gemini.

## Esito in breve
- La revisione di Gemini è **una buona base di principi, non ancora una base esecutiva affidabile**.
- **Rispettati:** Guardian solo consultivo (G0), V3.3 congelata, nessuna gerarchia tra i modelli, limiti deterministici prima delle probabilità.
- **Problemi principali:**
  - modello epistemico a 5 tipi descritto ma non progettato;
  - citazioni dichiarate verificate ma con errori dimostrati;
  - conteggi e due classificazioni errati nell'audit delle affermazioni;
  - roadmap con stati prematuri e soglie arbitrarie;
  - memoria condivisa tra i due modelli non ancora esistente;
  - rischio di contaminazione delle ipotesi dovuta all'addestramento dei modelli, non trattato.
- Claude dichiara anche due imprecisioni proprie (divergenze D-03 e D-04).

## Limiti dichiarati
- Il rapporto V1 di Gemini, a cui si riferisce il changelog, non era disponibile.
- La rete dell'ambiente di Claude non raggiungeva Crossref né doi.org: solo 6 citazioni sono state verificate con la ricerca web, le altre sono indicate come «C» (non rilette).
- Nessuna decisione è stata presa al posto dell'utente.

## Impronte SHA-256 dei tre documenti originali
```
186dad0dd1463bb06a8d8bbad33c7550e6d1068e493d2ee5775b1698e803d6d8  CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md
1315cf2d17599d0ec8511a883e4977fd9c59a10687e52c38129a2c125ac0ddc4  CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md
b48e1717de1a4241f36756f14b839163f06b2496f1208b59595e614514209eb5  CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md
```

I documenti originali sono separati qui sotto da una linea orizzontale. I riferimenti tra loro (link relativi, cartelle `output/` e `verifiche/`) rimandano alla cartella di consegna nel repository del Brain.


---

<!-- INIZIO DOCUMENTO: CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md -->

# Audit architetturale indipendente della revisione V2 di Gemini (V1)

**Autore:** Claude Code · **Data:** 12/11/2026
**Oggetto:**
- `TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md` (SHA-256 `62dda32d…`);
- `TRADING_BRAIN_CLAIMS_AUDIT_V1.md` (`d0f6729c…`);
- `TRADING_BRAIN_ARCHITECTURE_CHANGELOG_V2.md` (`5465113e…`).

**Documenti collegati:**
- [`CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md`](CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md): affermazioni e fonti;
- [`CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md`](CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md): divergenze.

**Natura del documento:** analisi e proposte. Nulla di quanto segue è stato implementato. Non ho modificato originali, codice, ZIP, manifest o rulebook. Non ho fatto commit né push, e non ho avviato alcuna fase.

---

## 0. Integrità, metodo e limiti

**Integrità** (`output/integrita_pacchetto.txt`):
- i tre documenti coincidono con gli hash dichiarati, e il manifest interno è 4/4 OK;
- lo **ZIP non coincide** con lo SHA-256 annunciato (`f4794a55…` contro `64470738…`);
- lo ZIP contiene un file non annunciato (`LEGGIMI_CLAUDE.md`).

Probabilmente lo ZIP è stato rigenerato dopo l'annuncio. I contenuti esaminati sono comunque quelli certificati.

**Metodo:**
- Ho letto integralmente i quattro file e confrontato ogni affermazione verificabile con le fonti primarie del progetto: codice V3.3, `rulebook.yaml`, schede STR, `STANDARD.md`, struttura del repository `l-Altro`.
- Ho ricalcolato ciò che si poteva calcolare (`verifiche/potenza_campione.py`).
- Ho verificato al web le citazioni più dubbie (`output/verifica_fonti_web.txt`).

**Limiti:**
1. Manca il rapporto V1 di Gemini: il changelog e l'audit delle affermazioni si possono verificare solo per coerenza interna.
2. Crossref e doi.org sono rifiutati dalla rete: i DOI non sono stati risolti; 6 fonti sono V-sec, le altre C.
3. Non ho accesso alla copia del Brain sul Mac di Gemini.
4. Il Master Mission non esiste in alcuna copia accessibile: le verifiche di conformità sono fatte rispetto alle decisioni dell'utente come formulate nell'incarico.

---

## 1. Esito complessivo

**Giudizio:** la revisione V2 è una **buona base di principi**. Non è ancora una **base esecutiva affidabile**.

**Che cosa è solido** (lo confermo spiegando perché, nei §2–§5):
- rispetto delle decisioni A, C e D;
- precedenza dei limiti deterministici;
- stato NON STIMABILE;
- separazione tra raccomandazione e decisione;
- esclusione del motore V3.3 dal rischio di portafoglio;
- livelli di validazione dei risultati (§11.2: TEORIA → LIVE-REAL);
- pre-registrazione con hash;
- riconoscimento della falsa concordanza tra modelli.

Il changelog corregge errori reali della V1 e lo fa in modo trasparente.

**Che cosa non regge, in ordine di importanza:**
1. **Il modello epistemico è descritto, non progettato** (§3):
   - fonde il *tipo* con lo *stato di validazione*;
   - nel diagramma mancano i flussi necessari (la REGOLA non entra nei derivati);
   - aggiunge **tre tassonomie parallele** (§2.2, §2.3, §11.2) senza raccordo con quelle già in vigore in `STANDARD.md`.

   Così com'è produrrebbe proprio la confusione che vuole impedire.
2. **La bibliografia dichiarata «verificata» contiene errori dimostrati.** Una citazione è sbagliata in rivista, volume, pagine, DOI e contenuto; un DOI è errato; un autore ha il nome sbagliato; una fonte compare in due sedi diverse. L'audit delle affermazioni ha inoltre conteggi errati e due classificazioni sbagliate (CLM-14, CLM-16).
3. **Roadmap:**
   - lo stato è dichiarato in modo prematuro (Fasi 1–7 «correnti»);
   - alcune dipendenze sono discutibili: il Guardian arriva dopo la validazione delle strategie; il bot precede il paper trading;
   - i criteri di uscita sono incoerenti tra loro;
   - compaiono **nuove soglie arbitrarie** (E[R] < 0,10R; 3–6 mesi; N < 30; 10 anni × 3 classi di attivo) nello stesso documento che declassa le soglie arbitrarie.
4. **Indipendenza e memoria condivisa non esistono ancora nei fatti** (§8.2, §8.12). Oggi:
   - il Brain esiste in almeno due copie non sincronizzate (GitHub e Mac);
   - le consegne di Gemini non sono archiviate nel Brain versionato;
   - il canale tra i due modelli è l'utente.
5. **Il piano «formativo» (28 discipline) tratta i due LLM come studenti che accumulano competenze** (§7). Un LLM non conserva apprendimento tra le sessioni: si accumulano soltanto memoria esterna e strumenti verificati. I test di padronanza vanno ripensati come prove con risposta nota.

**Grado di certezza:**
- alto sui punti 2 e 4 e sulle incoerenze interne (verificati su file e fonti);
- medio-alto sui punti 1 e 3 (ragionamento progettuale, con controesempi);
- medio sul punto 5 (dipende da come l'utente intende «formazione»).

---

## 2. Principi A–E

| Principio | Esito | Evidenza | Conseguenza |
|---|---|---|---|
| **A. Ecosistema e autonomia bounded** | **Rispettato** nei testi (§1, DEC-01, DEC-02, §5 criterio 4) | Promozione nel Core, capitale e ordini riservati all'utente; nessuna gerarchia permanente (DEC-03) | La **memoria condivisa** non è progettata: §5 descrive cartelle, non un meccanismo di sincronizzazione tra due ambienti separati (§8.12). La simmetria è dichiarata, ma i due nodi non hanno pari accesso: Claude lavora su GitHub, Gemini su file locali; nessuno legge l'area dell'altro senza passare dall'utente |
| **B. Modello a 5 tipi** | **Descritto, non ancora applicabile** | §3 | Vedi §3: servono schema e assi separati |
| **C. Guardian G0** | **Rispettato** | §8: zero blocchi, zero intercettazioni, zero kill switch, zero attese forzate | Le osservazioni tecniche sono nel §4 |
| **D. V3.3 congelata** | **Rispettato** | Nessuna V3.3.1 o V3.4; T-01…T-05 requisiti; valori T-02 corretti (0,77998 / 0,85717 / 0,66858) | **Ambiguità da sciogliere (decisione dell'utente):** l'utente ha detto «requisiti di ingresso della successiva fase *tecnica*». Gemini li colloca come gate della **Fase 5**, ma le Fasi 3 (modulo per il Brier score) e 4 (pipeline dei dati) sono già tecniche e la precedono. Come scritto, del codice nuovo nascerebbe prima che l'errata sia chiusa |
| **E. TradingView e motore** | **Coerente nella sostanza, non nella forma** | §6.2 motivato; ma DEC-06 lo riduce a «visualizzazione e telemetria» | DEC-06 non coincide con la decisione dell'utente, che include Pine Script, Strategy Tester e segnali (§5) |

---

## 3. Modello epistemologico: verifica di applicabilità

La domanda dell'incarico è se l'architettura permetta **davvero** di applicare il modello. Risposta: **non ancora**, per sei motivi concreti, ognuno con una correzione.

### 3.1 Tipo e stato di validazione sono fusi
In §3.2 «Status(Output) = min(Status(Input))» si applica a un ordine totale MISURA > DERIVATO > STIMA > IPOTESI. Ma così:
- una STIMA calibrata e una non calibrata hanno lo stesso rango;
- una REGOLA verificata sulla fonte ufficiale e una V-sec sono indistinguibili, e la REGOLA è fuori dall'ordinamento;
- NON STIMABILE, che è uno **stato** e non un tipo, non trova posto.

**Correzione:** assi **ortogonali** per ogni grandezza.

| Asse | Valori | Esiste già in `STANDARD.md`? |
|---|---|---|
| Tipo epistemico | MISURA, DERIVATO, STIMA, IPOTESI, REGOLA | No (nuovo) |
| Condizioni | insieme {H₁…Hₖ} delle ipotesi da cui dipende il valore | No (nuovo) |
| Stato di verifica | fonte: V / V-sec / C / X · ipotesi: aperta / corroborata / falsificata · stima: calibrata / non calibrata / NON STIMABILE | Sì, per le fonti (§3) |
| Forza dell'evidenza esterna | E1–E7 | Sì (§2) |
| Livello di validazione del risultato | TEORIA, SIMULATO, IN-SAMPLE, OOS, WALK-FORWARD, FORWARD-PAPER, LIVE-REAL | No (il §11.2 di Gemini va bene così) |
| Ciclo di vita dell'artefatto | progettato, documentato, implementato, testato, validato, validato empiricamente, in uso | No (manca anche nel documento di Gemini: §6) |
| Classe di contenuto | VERIFICATO, IN VERIFICA, IPOTESI, ESERCIZIO, SIMULATO, REALE | Sì (§8) |

Le tassonomie del documento di Gemini (§2.2 gerarchia delle fonti, §2.3 sette etichette, §11.2 livelli) vanno **mappate** su questi assi e non aggiunte in parallelo. Esempi di sovrapposizione:
- `PROPOSTA TECNICA` e `DECISIONE ARCHITETTURALE` (§2.3) sono stati di una **decisione**, non tipi di informazione;
- `EVIDENZA CONSOLIDATA` / `LIMITATA` / `CONTRASTANTE` duplicano E1–E3.

### 3.2 La propagazione perde l'informazione utile
Il changelog dice che misura più ipotesi dà «IPOTESI»; il testo principale dice «IPOTESI CONDIZIONATA». Entrambe le forme perdono **quali** ipotesi condizionano il risultato. Eppure è proprio questo che serve per decidere e per l'analisi di sensibilità.

**Correzione:**
- il risultato conserva il tipo del calcolo e porta con sé l'unione delle condizioni;
- se il calcolo usa una stima, porta anche l'incertezza propagata, in forma analitica o per simulazione, dichiarata.

Esempio: «P(violazione) = 0,31 [DERIVATO | H: edge = 0,15R, i.i.d., MAE browniano]» è più utile e più onesto di «IPOTESI».

### 3.3 Mancano flussi necessari
Nel diagramma la REGOLA entra solo nella RACCOMANDAZIONE, e l'IPOTESI solo nella STIMA. Ma il margine residuo al pavimento giornaliero, cioè il numero più importante del Guardian, è **MISURA + REGOLA → DERIVATO**. Anche le simulazioni sono **IPOTESI → DERIVATO** (condizionato).

Manca anche il percorso di ritorno, che non viola il principio «mai dalle decisioni alle misure»: la **decisione registrata diventa una MISURA** del journal (che cosa è stato deciso, quando, con quali informazioni). Senza questo percorso non si possono valutare le decisioni a posteriori.

### 3.4 NON STIMABILE con una soglia fissa è sbagliato
- La soglia N < 30 (changelog §3.2) è smentita dal progetto stesso: con **N = 300** l'edge di riferimento non è distinguibile da zero (Q-01).
- **Criterio corretto:** una grandezza è NON STIMABILE *per una decisione* quando il suo intervallo di incertezza contiene valori che porterebbero a decisioni diverse.
- La stimabilità quindi dipende dalla decisione, non solo da N. Per esempio, 25 osservazioni bastano a escludere un tasso di violazione del 50%, ma non a distinguere 2% da 4%.

### 3.5 I «limiti deterministici» dipendono da un'ipotesi di esecuzione
La perdita allo stop e il «numero esatto di stop consecutivi tollerabili» (§3.3) sono deterministici **solo se lo stop viene eseguito al suo prezzo**. Con gap e slippage, che il §7.1 riconosce per i backtest, la perdita è maggiore.

**Correzione** (vale anche per la mia risposta in chat, che aveva lo stesso difetto):
- (a) perdita allo stop come **DERIVATO | H_esec**;
- (b) riserva per gap e slippage come **STIMA** (dai dati di esecuzione reali) o, finché i dati mancano, come **IPOTESI** dichiarata e prudente;
- (c) il conteggio degli stop residui si calcola su (a) + (b) e si dichiara che dipende da H_esec.

Anche il limite ρ = 1 va riformulato: il caso peggiore è «**tutti gli stop colpiti insieme**» (perdite co-monotone), non «correlazione unitaria». Con posizioni di segno opposto, ρ = 1 riduce la perdita.

### 3.6 Lo schema non è specificato
Mancano:
- formato dei record;
- campi obbligatori con unità;
- meccanismo di applicazione nel codice (per esempio, un tipo che non si può sommare a un altro senza dichiarare le condizioni);
- test che dimostrino che un numero senza tipo viene rifiutato.

Finché manca questo, il modello resta allo stato **progettato**, non **implementato** (A-17).

**Esperimento proposto (non avviato):** un prototipo minimo dello schema su tre calcoli reali del Guardian (perdita allo stop, margine al pavimento, somma dei rischi aperti), con test che falliscono se:
- un valore non ha tipo;
- un DERIVATO usa una STIMA senza dichiararla;
- un limite viene allargato da una probabilità.

**Che cosa è giusto e va conservato:**
- la precedenza dei limiti deterministici e la «regola aurea» (una stima può solo restringere un limite);
- la distinzione tra raccomandazione e decisione;
- l'obbligo di NON STIMABILE;
- l'unidirezionalità.

---

## 4. Trading Guardian G0

**Conformità alla decisione dell'utente: piena.** §8.1 elenca ciò che il Guardian non fa, in modo esplicito e verificabile, e l'esclusione del kill switch è coerente con G0.

Osservazioni tecniche:
1. **Formula della perdita incompleta** (A-16):
   - manca il valore assoluto in §8.3;
   - mancano moltiplicatore del contratto, valore del tick e **cambio** verso la valuta del conto;
   - il cambio è una MISURA con ora e fonte.

   Per CFD e FX il risultato senza questi elementi è sbagliato di ordini di grandezza.
2. **Pavimento giornaliero.** La base di calcolo (saldo o equity a mezzanotte, fuso orario, posizioni aperte) è una REGOLA della prop firm con fonte e data. Oggi lo stato è V-sec, non verificato sul regolamento ufficiale. Q-09 deve risolverla prima di qualsiasi calcolo: altrimenti il margine «deterministico» si basa su una regola non verificata.
3. **Percentuali di esempio** («4,0%», «8,5%»): sono buffer personali, non limiti FTMO. Vanno tipizzati come REGOLA personale.
4. **Accesso ai dati del conto.** G0 deve leggere posizioni ed equity, quindi servono credenziali in **sola lettura**, conservate fuori dal repository. È un requisito di sicurezza non trattato (§8.15).
5. **Test di accettazione.** «Precisione 10⁻⁶ su 1.000 scenari sintetici» verifica l'aritmetica, ma non che il Guardian calcoli ciò che il broker calcola davvero. Serve una **riconciliazione** con estratti conto reali (MISURA): dato un giorno di operatività, il margine calcolato deve coincidere con quello del broker entro la sua tolleranza di arrotondamento.
6. **Livello comportamentale.**
   - Gemini sceglie la sola misurazione, senza interpretazioni. È prudente, ma toglie all'utente la funzione che ha chiesto esplicitamente: segnalare FOMO, revenge trading e overtrading.
   - Una terza soluzione: misure oggettive più **indicatori definiti prima** (per esempio «R1 = nuovo ingresso entro X minuti da una perdita con size maggiore della precedente»), con l'interpretazione etichettata come IPOTESI («pattern compatibile con…»).
   - Gli indicatori si validano nel tempo sui dati dell'utente: R1 precede davvero risultati peggiori? Altrimenti si scarta.
   - Questo rispetta G0 (nessun blocco) e il divieto di diagnosi presentate come fatti.
7. **Dipendenza dalla Fase 6:** vedi §6. Lo strato deterministico di G0 non ha bisogno di strategie validate.

---

## 5. TradingView e motore quantitativo

La separazione è **tecnicamente motivata**:
- ricerca, backtest e validazione richiedono riproducibilità, dati sotto controllo, librerie scientifiche e registrazione delle prove;
- Pine Script ha limiti di esecuzione e non offre questi strumenti (stato C);
- c'è anche un argomento di **indipendenza dal fornitore**, coerente con la visione: i risultati di ricerca non devono dipendere da una piattaforma chiusa.

Il documento la presenta come scelta (CLM-07 riformulata), e va bene. Correzioni:
1. **DEC-06 non corrisponde alla decisione dell'utente.** TradingView è previsto anche per Pine Script, Strategy Tester e segnali. Proposta di formulazione:
   - TradingView per grafici, prototipi rapidi in Pine e segnali o allarmi;
   - i risultati dello Strategy Tester sono `[IN-SAMPLE · piattaforma terza]` e **non** valgono come evidenza finché il motore locale non li riproduce da una specifica scritta;
   - la discrepanza tra i due motori è essa stessa una misura utile (costi, riempimenti, dati).
2. **Affermazioni senza supporto in §6.2:** «webhook a bassissima latenza», calcolo «illimitato», «zero costi» (i dati storici di qualità hanno costi e licenze, §8.14).
3. **Versione:** Pine Script v6 dal 10/12/2024 (V-sec), non v5.
4. **Rischio di dipendenza inverso:** se i segnali reali nascono in TradingView, la strategia in uso è il codice Pine, non quello validato in locale. Serve una **specifica unica**, per esempio pseudo-codice versionato, da cui derivano entrambe le implementazioni, e un test di equivalenza dei segnali su dati comuni.

---

## 6. Roadmap

### 6.1 Ciclo di vita: dichiarazioni premature
- Il diagramma marca F0 come conclusa e **F1–F7 come «correnti»**. Nessuna è avviata e l'utente non ha autorizzato avvii (A-12).
- §11.2 distingue bene i livelli di validazione dei **risultati**, ma la roadmap non indica per ciascun componente lo stato **progettato → documentato → implementato → testato → validato → validato empiricamente → in uso**. Esempio: «Monte Carlo Validato» (F5) non dice validato rispetto a che cosa.
- **Proposta:** una tabella di stato per componente, aggiornata solo con evidenza (hash, test, revisione).

### 6.2 Fase per fase

| Fase | Necessità | Problemi rilevati | Proposta |
|---|---|---|---|
| F0 Consolidamento | Sì | Coerente | Archiviare le consegne di Gemini nel Brain versionato (oggi assenti: §8.12) |
| F1 Governance e repository | Sì | Il gate dipende dal Master Mission, che potrebbe non esistere; la «verbale di assenza» è prevista: bene | Includere la **sincronizzazione** tra le copie (§8.12), non solo la scelta del repository |
| F2 Compendio delle 28 discipline | Parziale | Fase documentale **lunga e senza verifica empirica** prima di ogni capacità concreta. Il gate è una «verifica incrociata a doppio cieco» che si basa proprio sulla concordanza tra modelli che §4.1.4 dichiara priva di valore | Rendere il compendio **incrementale e guidato dai bisogni**: ogni scheda nasce quando un componente la richiede, con una prova a risposta nota (§7) |
| F3 Due cervelli | Sì | Gate «senza collusione» non verificabile; il «doppio cieco» è irrealizzabile (stili riconoscibili, l'utente come canale) | Sostituire con **stime sigillate** (hash prima della lettura reciproca) e registro degli accessi (§8.2) |
| F4 Dati | Sì | (a) **Fattibilità:** l'accesso ai dati è oggi il vero collo di bottiglia (FRED, Yahoo e Stooq rifiutati dalla rete di Claude; fornitore, costi e licenze non decisi). (b) Gate «10 anni × 3 classi di attivo» arbitrario. (c) Modelli di regime (Markov switching, GMM) sono ricerca, non infrastruttura | Gate legato ai dati **necessari alle ipotesi registrate**; decisione dell'utente su fornitore e budget prima della fase; spostare i modelli di regime in F6 |
| F5 Motore | Sì | Collocazione di T-01…T-05 (§2, D); «test di penetrazione sul look-ahead» buono | Chiarire con l'utente se T-01…T-05 precedono anche F3 e F4 |
| F6 Strategy Lab | Sì | Gate incoerente con §11.1 e R-01 (p < 0,01 contro t > 3 contro Bonferroni/Holm); nessuna **potenza statistica**; «catalogo approvato» dopo il solo backtest, in conflitto con la regola di §11.2 | Un solo criterio: DSR con conteggio delle prove **più** potenza dichiarata; l'esito è «candidata per forward», non «approvata» |
| F7 Guardian G0 | Sì, **prima** | Dipende da F6 (strategie codificate) senza motivo: lo strato deterministico richiede solo Q-09, dati del conto e lo schema dei tipi | Proposta: **G0 minimo** (rischio a stop, margini, somma dei rischi, journal) subito dopo F1 e Q-09, in parallelo a F4. È anche il primo componente con utilità reale e rischio basso |
| F8 Bot Lab | Discutibile come prerequisito | Precede F9, ma il paper trading di una strategia, anche manuale, non richiede un sistema di gestione degli ordini. «Circuit breakers» = G1/G2: richiedono un'autorizzazione separata | Rendere F8 **opzionale** e successiva o parallela a F9 |
| F9 Paper trading | Sì | «3–6 mesi» non giustificato: per l'edge di riferimento servono **594 trade** con potenza 80% (14 mesi a 2 trade al giorno) e **1.417** con soglia t > 3 [DERIVATO condizionato] | Durata espressa in numero di trade, da un calcolo di potenza pre-registrato |
| F10 Operatività | Sì | Coerente (supervisione umana) | Criteri di arresto pre-registrati (deriva dell'edge, violazioni) |

### 6.3 Dati che richiedono tempo di calendario
Alcuni dati si accumulano **solo nel tempo**: journal delle decisioni e del comportamento, esecuzioni reali, previsioni da valutare con il Brier score. Nella roadmap compaiono tardi (F7, F9). Poiché la loro raccolta è il collo di bottiglia della validazione, **va avviata presto**, appena autorizzata, con strumenti minimi (§9). Il valore aspettato della raccolta precoce è alto e il costo basso.

### 6.4 Fasi mancanti o sottodimensionate
- **Governance dei dati:** fornitori, licenze, costi, versioni dei dati e date di revisione dei dati macro.
- **Sicurezza:** credenziali, accessi in sola lettura, prompt injection da contenuti esterni.
- **Sincronizzazione della memoria tra i due ambienti.**
- **Revisione periodica** di regole e fonti (le regole delle prop firm cambiano, per esempio il limite di tempo eliminato nel 2023, stato V-sec).

---

## 7. Le 28 discipline

**Valutazione generale.** L'elenco è ampio e quasi tutto pertinente. Ma un elenco non è un percorso, e un test non è una prova di padronanza.

### 7.1 Problema di fondo: che cosa significa «formare» un LLM
- Né Claude né Gemini conservano apprendimento tra le sessioni: la competenza «accumulata» esiste solo come **memoria esterna** (note, strumenti verificati, registri) e come **prestazione dimostrata** su compiti.
- Lo dichiaravo già nella mia proposta Parte B (§0). Il documento di Gemini non lo tratta e parla di «formazione dei due cervelli» (F3) come se studiare un compendio cambiasse il modello.
- **Conseguenza:** la padronanza si misura solo con **prove a risposta nota, eseguite e registrate**. Si accumula sotto forma di strumenti testati e di calibrazione misurata.

### 7.2 Test di padronanza discutibili
| # | Test proposto | Problema |
|---|---|---|
| 3 | Residuo \|f(x)\| < 10⁻¹⁵ | Soglia sotto la precisione raggiungibile in molte configurazioni (V3.3 usa 10⁻⁷ per buone ragioni); misura lo strumento, non la competenza |
| 4 | «Dimostrazione formale di indipendenza stocastica e convergenza quasi certa» | Non è un compito definito: non si «dimostra» l'indipendenza di dati di mercato |
| 5 | «Copertura nominale **esatta** su campioni finiti» | Impossibile per proporzioni discrete: Wilson approssima, Clopper-Pearson è conservativo. Il test non è superabile |
| 7 | «Dimostrazione di stazionarietà dei residui» | Si può solo non rifiutare un'ipotesi; ADF e KPSS hanno potenza limitata |
| 15 | «Correlazione dimostrata tra dispersione macro e persistenza dei trend» | È un risultato di ricerca ipotetico, non un test di padronanza; lo presuppone vero |
| 20 | «La rimozione della causa annulla l'anomalia» | Non realizzabile su dati osservazionali di mercato: non si può intervenire sul mercato |
| 24 | «Query su 10 anni di tick in < 2 s» | Requisito di prestazione arbitrario, non di competenza |

**Proposta:** riformulare i test sul modello già in vigore (`STANDARD.md` §5, livelli L1–L5), con prove di tre tipi:
- (a) riprodurre un risultato pubblicato noto;
- (b) recuperare parametri noti da dati `[SIMULATO]` generati con seme dichiarato;
- (c) trovare errori inseriti apposta (come le mutazioni V01–V25).

La prova la prepara l'altro nodo o l'utente, e l'esito viene registrato.

### 7.3 Discipline mancanti o sottodimensionate
1. **Potenza statistica e dimensione del campione:** decisiva per F6 e F9 (§6.2).
2. **Bootstrap e ricampionamento per serie dipendenti** (bootstrap a blocchi, stazionario): necessari per intervalli onesti nei backtest.
3. **Modelli di volatilità** (GARCH, volatilità realizzata): assenti; l'econometria elenca solo ARIMA, radici unitarie e cointegrazione.
4. **Dipendenza nelle code e copule:** il rischio di portafoglio oltre ρ.
5. **Metodi Monte Carlo** (riduzione della varianza, CRN, errore standard): usati in tutte le revisioni V3.x e non elencati.
6. **Catene di Markov e programmazione dinamica:** il calcolo esatto che ha validato V3.x.
7. **Valutazione delle previsioni e regole di punteggio proprie** (Brier, log-score, calibrazione): usate in §4 e non elencate.
8. **Meccanica degli strumenti e specifiche di contratto** (CFD, futures, FX, roll, swap, margini, cambi): indispensabile per il Guardian (§4.1).
9. **Regolamenti delle prop firm e dei broker** come competenza documentale (fonti, date, versioni).
10. **Inferenza sequenziale** (SPRT, monitoraggio del decadimento dell'edge): utile per F9 e F10.
11. **Sicurezza operativa** (credenziali, accessi).

### 7.4 Sovrapposizioni e collocazioni
- 7 (econometria) e 17 (regimi); 21 (ML) e 22 (ottimizzazione); 23 (falsificazione) e 26 (MLOps, per il decadimento): sovrapposizioni gestibili, ma da dichiarare.
- 14 (analisi tecnica) e 16 (intermarket) poggiano su testi divulgativi o professionali (F6–F7 di `STANDARD.md`): vanno trattati come **fonti di ipotesi**, non come discipline con base scientifica equivalente.
- 28 «Etica ed epistemologia»: contiene solo epistemologia. L'etica (conflitti di interesse, comunicazione del rischio all'utente) non è trattata.

### 7.5 Fonti
Vedi il documento sulle affermazioni, §4. Due errori ricadono nella tabella:
- riga 12, Bouchaud et al. attribuito a «Quantitative Finance», incoerente con §15;
- riga 19, Lo, Repin e Steenbarger attribuito a «Cognitive Neuroscience»: errato.

---

## 8. Criticità individuate in modo indipendente

Per ciascun rischio indico pertinenza (alta, media, bassa) e controllo proposto. Non è un elenco generico: includo solo ciò che riguarda questo progetto.

### 8.1 Compiacenza (sycophancy) — pertinenza **alta**
Il rischio maggiore non è la compiacenza tra i due modelli, ma la **compiacenza di entrambi verso l'utente**. Gli incarichi contengono decisioni già prese, e un modello tende a confermarle.
- **Controllo:** ogni incarico separi «decisioni da rispettare» da «questioni da valutare»; i rapporti includano una sezione «dove credo che la decisione dell'utente sia discutibile» (qui: §2-D, §4.6, §6.2-F7).
- **Autovalutazione:** nelle revisioni V3.x il mio giudizio è stato verificato da test eseguibili, non dall'accordo; dove ho sbagliato (Q-08, ρ = 1, «deterministico») l'ho scoperto rileggendo il mio ragionamento, non per un controllo esterno.

### 8.2 Falsa indipendenza dei registri — pertinenza **alta**
- Oggi tutto ciò che Gemini sa del lavoro di Claude, e viceversa, passa dall'utente.
- Le cartelle `ricerca/claude` e `ricerca/gemini` starebbero nello stesso Brain, leggibile da entrambi.
- **Controllo:**
  - **stime sigillate:** ogni nodo registra la propria stima con hash *prima* di leggere quella dell'altro (protocollo già proposto nella Parte B, §5.2);
  - registro degli accessi;
  - le divergenze si confrontano solo dopo il sigillo.

### 8.3 Contaminazione delle ipotesi — pertinenza **alta**, **non trattata** dal documento
- Gli LLM sono addestrati su testi che includono la storia dei mercati fino alla loro data di cutoff. Un'ipotesi proposta da un LLM può incorporare implicitamente il comportamento del mercato dei periodi che poi verranno usati come «fuori campione».
- Le schede STR dichiarano OOS 2018–2023 e forward 2024–2026: periodi noti a entrambi i modelli.
- **Controllo:**
  - un fuori campione **pulito**, per ipotesi generate da LLM, esiste solo **dopo la data di cutoff del modello e dopo la data di registrazione dell'ipotesi**;
  - i periodi storici valgono come prova debole, non come OOS;
  - registrare data di registrazione e versione del modello per ogni ipotesi.

### 8.4 Qualità delle fonti — pertinenza **alta** (dimostrata)
- Questo stesso pacchetto contiene citazioni errate dichiarate «verificate».
- **Controllo:** stato V solo con registrazione della verifica; per ogni citazione, chi l'ha verificata e come; controllo a campione da parte dell'altro nodo.

### 8.5 Data leakage — pertinenza **media-alta**
- Oltre al look-ahead (trattato bene in §6.1):
  - prezzi aggiustati calcolati con informazione futura (aggiustamenti per dividendi e roll);
  - dati macro **rivisti** al posto delle versioni disponibili all'epoca (vintage);
  - normalizzazioni calcolate sull'intero campione;
  - uso dell'ATR o della volatilità della barra corrente.
- **Controllo:** dataset «point-in-time» con data di disponibilità per ogni valore; test automatico di leakage in F5.

### 8.6 Test multipli — pertinenza **alta**
- Due nodi che esplorano in parallelo moltiplicano le prove. Le idee scartate «a mente» da un LLM non vengono registrate.
- **Controllo:** un **contatore globale** condiviso delle prove (anche di quelle abbandonate), unico per entrambi i nodi; il DSR usa quel contatore.

### 8.7 Bias di selezione — pertinenza **media**
- Le ipotesi tratte dalla letteratura sono quelle pubblicate, e gli effetti pubblicati tendono a ridursi dopo la pubblicazione (McLean e Pontiff, già nell'audit del Brain).
- **Controllo:** stima a priori ridotta dell'effetto per le anomalie pubblicate; registrazione della fonte dell'ipotesi.

### 8.8 Bias di sopravvivenza — pertinenza **media**
- Liste di strumenti attuali, CFD che cambiano, contratti cancellati, prop firm sopravvissute.
- **Controllo:** universo definito alla data di ogni test.

### 8.9 Overfitting — pertinenza **alta**
- Trattato bene: DSR, CPCV, plateau dei parametri.
- In aggiunta: limitare i gradi di libertà per ipotesi *prima* del test.

### 8.10 Non stazionarietà — pertinenza **alta**
- Vale anche per le **regole** (FTMO ha cambiato il limite di tempo nel 2023) e per i costi.
- **Controllo:** ogni REGOLA ha data di validità e data di prossima verifica; ogni stima ha una finestra dichiarata e un monitoraggio sequenziale.

### 8.11 Robustezza dei backtest — pertinenza **alta**
- Va aggiunto l'**ordine intra-barra** quando stop e target sono toccati nella stessa barra: assumere il caso peggiore.
- Il «divieto del same-bar fill» va riformulato (A-10).

### 8.12 Affidabilità della memoria condivisa — pertinenza **alta** (dimostrata)
- **Fatti verificati:**
  - il Brain versionato è sul ramo GitHub `claude/vibrant-cannon-5uunho` del repository `l-Altro`, che sugli altri rami contiene un'applicazione TypeScript estranea;
  - Gemini lavora su una copia locale (`~/.gemini/antigravity/brain/…`);
  - le consegne di Gemini (V2–V3.3 e questa revisione) **non** sono archiviate nel Brain versionato: `collaborazione/da-gemini/consegne/` contiene solo il README;
  - il trasferimento avviene con ZIP via utente, e in questo pacchetto lo ZIP non coincideva con l'hash annunciato.
- **Conseguenza:** non esiste oggi una «memoria scientifica condivisa». Esistono due archivi e un canale manuale. I manifest SHA-256 proteggono l'integrità dei singoli pacchetti, non la sincronizzazione.
- **Controllo:**
  - **una sola fonte di verità**, decisa dall'utente (D-01 di Gemini, decisione 3 del mio audit);
  - archivio delle consegne con manifest;
  - ogni nodo inizia la sessione verificando l'hash dello stato corrente del Brain.

### 8.13 Riproducibilità — pertinenza **media** (finora gestita bene)
- Le revisioni V3.x hanno riprodotto JSON byte per byte. Vanno registrate versione dell'interprete e dipendenze.
- Per le analisi fatte da LLM vanno registrati modello e versione, perché il fornitore può cambiarli.

### 8.14 Governance dei dati — pertinenza **media-alta**
- Licenze dei fornitori (redistribuzione, uso), costi, dati personali nel journal (salute, sonno, stato emotivo: dati sensibili dell'utente).
- **Controllo:** registro delle licenze; journal conservato in locale e fuori dai servizi esterni senza consenso esplicito.

### 8.15 Sicurezza — pertinenza **media**, che cresce con G0
- Credenziali del conto (solo lettura, mai nel repository).
- **Prompt injection** da contenuti esterni letti dagli LLM (pagine web, PDF, commenti): un testo malevolo potrebbe tentare di modificare regole o registri.
- **Controllo:** contenuti esterni trattati come dati; modifiche alle REGOLE solo con approvazione dell'utente e diff registrato.

### 8.16 Dipendenza dai fornitori di modelli — pertinenza **media**
- Entrambi i «cervelli» sono servizi proprietari che cambiano versione e comportamento. Anche l'ambiente di Claude ha limiti di rete che oggi impediscono di scaricare dati e risolvere DOI.
- **Controllo:**
  - tutto ciò che conta è in file aperti (Markdown, Python, CSV/Parquet), eseguibili senza i modelli;
  - versione del modello registrata per artefatto;
  - test che non dipendono dal modello.

### 8.17 Manutenzione nel lungo periodo — pertinenza **alta**
- **Il volume documentale cresce più in fretta del contenuto validato:** quattro cicli V3→V3.3 per difetti in gran parte documentali; questo pacchetto propone 10 fasi e 28 discipline prima di qualsiasi dato reale.
- Con una sola persona come decisore e canale, il rischio di abbandono o di revisioni superficiali è concreto.
- **Controllo:**
  - un limite esplicito al rapporto documenti/artefatti validati;
  - preferire piccoli incrementi verificabili;
  - errata invece di nuove versioni complete (come già deciso per V3.3).

---

## 9. Esperimenti e verifiche necessari (proposte, non avviati)

1. **Prototipo dello schema dei tipi** (§3.6) su tre calcoli del Guardian, con test di rifiuto.
2. **Riconciliazione del Guardian** con un estratto conto reale di una giornata (§4.5).
3. **Verifica della regola del pavimento giornaliero** sulla fonte ufficiale della prop firm, con data (Q-09).
4. **Prova di indipendenza con stime sigillate** su un problema `[SIMULATO]` con risposta nota: ogni nodo stima un parametro (per esempio il win rate da 200 trade simulati) e registra stima e intervallo con hash; si misurano calibrazione e correlazione degli errori.
5. **Calcolo di potenza pre-registrato** per ogni ipotesi prima di F6 e F9 (modello in `verifiche/potenza_campione.py`).
6. **Audit delle citazioni a campione:** l'altro nodo verifica 10 citazioni scelte a caso nella bibliografia approvata.
7. **Test di equivalenza dei segnali** TradingView/motore locale da una specifica comune (§5.4), quando esisterà una strategia codificata.

---

## 10. Decisioni che spettano all'utente (non prese)

1. Fonte di verità unica del Brain e sincronizzazione tra i due ambienti (§8.12; D-01).
2. Se T-01…T-05 precedono **qualsiasi** fase tecnica (anche F3 e F4) o solo F5 (§2-D).
3. Se anticipare un **G0 minimo** (strato deterministico più journal) prima di F6 (§6.2).
4. Se il livello comportamentale di G0 debba includere indicatori pre-definiti con interpretazione etichettata come IPOTESI, o solo misure (§4.6).
5. Formulazione di DEC-06 su TradingView (§5).
6. Fornitore, budget e licenze dei dati (§6.2-F4).
7. Se F2 sia una fase autonoma o un compendio incrementale (§6.2).
8. Se e quando avviare la raccolta precoce di dati di calendario: journal e previsioni da valutare (§6.3).

---

## 11. Sintesi del grado di certezza

| Conclusione | Certezza | Base |
|---|---|---|
| Principi A, C e D rispettati | Alta | Lettura testuale |
| Modello a 5 tipi non ancora applicabile | Medio-alta | Analisi progettuale con controesempi (§3) |
| Bibliografia con errori dimostrati | Alta | Ricerca web (V-sec), coerenza interna |
| Conteggio e classificazioni CLM-14 e CLM-16 errati | Alta | Tabella; codice V3.3 |
| Stato della roadmap dichiarato in modo prematuro | Alta | Diagramma; assenza di autorizzazioni |
| Durata del paper trading non giustificata | Alta, condizionata alle ipotesi dichiarate | Calcolo di potenza |
| Memoria condivisa non esistente nei fatti | Alta | Repository, cartelle, procedura di trasferimento |
| Contaminazione delle ipotesi dovuta all'addestramento degli LLM | Media (meccanismo plausibile, entità non misurata) | Ragionamento; da verificare con l'esperimento 4 |

<!-- FINE DOCUMENTO: CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md -->


---

<!-- INIZIO DOCUMENTO: CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md -->

# Verifica delle affermazioni, delle fonti e delle classificazioni (V1)

**Autore:** Claude Code · **Data:** 12/11/2026
**Oggetto:** affermazioni contenute in `TRADING_BRAIN_CLAIMS_AUDIT_V1.md` (CLM-01…CLM-16) e affermazioni sostanziali di `TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md` non incluse nell'audit
**Documenti collegati:** [`CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md`](CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md), [`CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md`](CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md)

## 0. Condizioni della verifica

- **Integrità.** I tre documenti coincidono con gli SHA-256 dichiarati da Gemini, e il manifest interno è 4/4 OK. Lo ZIP ricevuto però **non** coincide con lo SHA-256 dichiarato: è `f4794a55…`, non `64470738…`. Contiene inoltre un file non annunciato, `LEGGIMI_CLAUDE.md`, coperto dal manifest (`output/integrita_pacchetto.txt`).
- **Documento mancante.** Il rapporto strategico V1 di Gemini (12/11/2026, 14:35) non è stato fornito. Posso quindi giudicare le affermazioni **come le cita l'audit di Gemini**, non verificare che le citazioni siano fedeli all'originale.
- **Fonti:**
  - Crossref e doi.org sono rifiutati dalla rete dell'ambiente: nessun DOI risolto direttamente.
  - Ho verificato con la ricerca web le 6 citazioni più dubbie (`output/verifica_fonti_web.txt`); il loro stato è **V-sec** (schede bibliografiche, testo integrale non letto).
  - Tutte le altre fonti sono **C**: note dalla mia conoscenza e non rilette. Le uso solo per indicare compatibilità o incompatibilità, mai come prova.
- **Fonti primarie del progetto, lette in questa sessione:** `archivio_storico/rulebook.yaml`, `STR_001`, `STR_002`, `prop_risk_engine_v3_3.py` (pacchetto V3.3), `brain/governance/STANDARD.md`, struttura del repository `l-Altro`.

Scala usata (richiesta dall'utente): **CONFERMATA · CONFERMATA CON LIMITI · RIFORMULATA · NON VERIFICATA · CONTRADDETTA · NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI.**
Per ogni voce indico due giudizi distinti:
1. **la mia classificazione dell'affermazione originale**;
2. **se la classificazione assegnata da Gemini è corretta.**

---

## 1. Conteggio dell'audit di Gemini

La sintesi dichiara 4 ritirate, 3 ipotesi, 2 proposte, 5 confermate con limiti, 1 riformulata e 1 non verificata. Contando la tabella:

| Esito di Gemini | Voci | Numero reale | Dichiarato |
|---|---|---|---|
| RITIRATA | CLM-01, 03, 06, 09, 15 | **5** | 4 |
| DECLASSATA A IPOTESI | CLM-02, 11, 12 | 3 | 3 |
| DECLASSATA A PROPOSTA | CLM-13 | **1** | 2 |
| CONFERMATA CON LIMITI | CLM-04, 05, 10, 14, 16 | 5 | 5 |
| RIFORMULATA | CLM-07 | 1 | 1 |
| NON VERIFICATO | CLM-08 | 1 | 1 |

**Errore dimostrato.** La sintesi (righe 50–54), `LEGGIMI_CLAUDE.md` e il messaggio di consegna riportano 4 e 2 invece di 5 e 1. Il totale (16) è corretto. Probabilmente CLM-09 è stato contato come «proposta». È un errore minore, ma in un documento dedicato all'onere della prova.

---

## 2. Le 16 affermazioni

### CLM-01 · Guardian come firewall che blocca gli ordini
- **Categoria:** scelta progettuale presentata come prescrizione.
- **Evidenze:** `rulebook.yaml` (82 righe, verificato) contiene `blocking: true` su più cancelli (per esempio GATE_06, riga 57-58). La decisione dell'utente è G0 consultivo.
- **Fonti primarie:** decisione dell'utente (incarico); `rulebook.yaml`.
- **Evidenze contrarie:** nessuna a favore del blocco in questa fase.
- **Assunzioni e limiti:** nessuna legge scientifica impone o vieta un blocco; è una scelta di governance. Un blocco automatico non è «scientificamente infondato» in sé: è **non autorizzato** e prematuro.
- **Mia classificazione:** **CONTRADDETTA**, dalla decisione dell'utente, non da evidenze di mercato.
- **Classificazione di Gemini (RITIRATA):** corretta nella sostanza. La motivazione «nessuna fonte scientifica a supporto» però confonde una scelta ingegneristica con una legge scientifica: l'argomento giusto è l'autorizzazione e il rischio operativo, non l'assenza di letteratura.

### CLM-02 · Attesa di 60–90 s prima del click e pausa di 15 minuti dopo una perdita
- **Categoria:** regola comportamentale presentata come necessità.
- **Evidenze:** `rulebook.yaml` riga 57 (GATE_06, 60–90 s, `blocking: true`) e riga 78 (`mandatory_pause_after_loss_minutes: 15`), verificate. Nessun dato del trader.
- **Fonti citate:**
  - Loewenstein (1996), stato C;
  - Lo, Repin e Steenbarger (2005), V-sec: AER 95(2), studio con questionari su 80 day trader. Trova una prestazione peggiore nei trader con reazioni emotive più intense. Non studia tempi di attesa.
- **Evidenze contrarie:** nessuna fonte citata studia la durata ottimale di una pausa.
- **Limiti:** una pausa può restare **legittima come regola personale** (tipo REGOLA, origine «personale»). Non serve una prova scientifica per adottarla, serve solo non presentarla come scientifica.
- **Mia classificazione:** **NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI** come necessità universale. È invece **ammissibile come regola personale dichiarata**.
- **Classificazione di Gemini (DECLASSATA A IPOTESI):** corretta per la parte scientifica. Incompleta: l'alternativa «regola personale scelta dall'utente» viene ignorata, e un'ipotesi non è l'unica forma legittima di quella regola.

### CLM-03 · Ruoli fissi (Gemini sviluppa, Claude verifica)
- **Categoria:** organizzativa.
- **Evidenze:** prassi V3–V3.3 (verificabile dai pacchetti); decisione dell'utente di simmetria (incarico).
- **Mia classificazione:** **CONTRADDETTA** dalla decisione dell'utente.
- **Classificazione di Gemini (RITIRATA):** corretta.
- **Precisazione:** l'argomento «resilienza in caso di sostituzione» è sensato, ma è una motivazione progettuale, non una prova.

### CLM-04 · Campionatore MAE esatto entro 2·10⁻¹⁵
- **Categoria:** risultato computazionale.
- **Evidenze:** la mia revisione V3.3 (`R-CLAUDE-20261112-05-V33/output/v33_f_precisione.txt`): errore ≤ 1,73·10⁻¹⁵ rispetto a F(d) calcolata in aritmetica decimale a 60 cifre, su 6 configurazioni × 9 valori di u.
- **Fonti:** derivazione nella revisione V3.1 (funzione di scala del moto browniano con deriva). Borodin e Salminen (2002), stato C: compatibile, non riletto.
- **Limiti:**
  - l'esattezza vale per il modello; il modello (moto browniano senza salti, MAE solo sui trade vincenti) **non** è un'ipotesi verificata sui prezzi reali;
  - la verifica copre 54 punti, non tutto il dominio.
- **Mia classificazione:** **CONFERMATA CON LIMITI.**
- **Classificazione di Gemini:** corretta.
- **Imprecisione nella colonna «evidenza»:** attribuisce il confronto a 60 cifre alla «test suite V3.3», ma è una mia verifica esterna; la suite non lo contiene.

### CLM-05 · Slippage Lomax con momenti verificati in forma chiusa
- **Categoria:** l'affermazione ne contiene due:
  - (a) i momenti sono corretti → risultato matematico;
  - (b) il Lomax è un modello adeguato dello slippage → ipotesi empirica.
- **Evidenze:**
  - (a) verificata due volte (forma chiusa più Monte Carlo, revisioni V3.2 e V3.3);
  - (b) nessun dato di slippage reale del progetto.
- **Fonti:** Lomax (1954) e Johnson, Kotz e Balakrishnan (1994), stato C; Bouchaud, Farmer e Lillo, esistenza V-sec (arXiv 0809.0822), sede non confermata.
- **Mia classificazione:** (a) **CONFERMATA**; (b) **NON VERIFICATA**.
- **Classificazione di Gemini (CONFERMATA CON LIMITI):** accettabile, ma fonde due affermazioni di tipo diverso. Il testo principale (§7.3) scrive che il Lomax «modella **efficacemente** le code pesanti»: senza dati è un'affermazione non verificata.

### CLM-06 · Le assunzioni V3.3 bastano per il rischio di portafoglio
- **Categoria:** estensione metodologica.
- **Evidenze:** `simulate_phase_v3_3` gestisce un conto e trade sequenziali, con ipotesi S-09 dichiarate nel codice (verificato).
- **Mia classificazione:** **CONTRADDETTA**.
- **Classificazione di Gemini (RITIRATA):** corretta.

### CLM-07 · TradingView come strumento perimetrale
- **Categoria:** scelta architetturale.
- **Evidenze:** sono limiti reali (stato C, documentazione non riletta):
  - Pine Script gira in un ambiente sandbox con limiti di tempo e memoria;
  - non permette librerie esterne né calcolo scientifico generale;
  - lo Strategy Tester ha assunzioni di esecuzione proprie.
- **Fonte citata:** «Pine Script v5 Reference Manual». **Non aggiornata:** TradingView ha annunciato Pine Script v6 il 10/12/2024 (V-sec).
- **Mia classificazione:** **RIFORMULATA**, come scelta motivata e non come legge.
- **Classificazione di Gemini:** corretta.
- **Incoerenze nel testo principale:**
  - DEC-06 riduce TradingView a «visualizzazione e telemetria», mentre la decisione dell'utente include Pine Script, Strategy Tester e segnali;
  - §6.2 contiene affermazioni non verificate («webhook a bassissima latenza», calcolo «illimitato» in locale, «zero costi» senza considerare il costo dei dati).

### CLM-08 · Master Mission come carta costituzionale
- **Categoria:** documentale.
- **Evidenze:** le schede STR-001 e STR-002 citano la Master Mission (§5.2, §5.3, §7; verificato). `rulebook.yaml` **non** la cita esplicitamente: cita «§9, Lezione 0.8», riferimento ambiguo, probabilmente al Manuale v1. Il testo non è presente né nel Brain su GitHub né, secondo Gemini, sul Mac.
- **Mia classificazione:** **NON VERIFICATA.**
- **Classificazione di Gemini:** corretta. Imprecisione: la colonna «evidenza» include `rulebook.yaml` tra i file che la citano.

### CLM-09 · Applicare subito T-01…T-05 in una cartella v3.3.1
- **Categoria:** operativa.
- **Evidenze:** decisione dell'utente (V3.3 congelata; T-01…T-05 requisiti di ingresso).
- **Mia classificazione:** **CONTRADDETTA** dalla decisione dell'utente.
- **Classificazione di Gemini (RITIRATA):** corretta.
- **Nota:** l'errata era una mia proposta. Ho scritto «applicarle all'inizio della fase successiva», non «subito». La versione V1 di Gemini ne aveva anticipato i tempi.

### CLM-10 · DSR e CPCV «eliminano» l'overfitting
- **Categoria:** metodologica.
- **Fonti:** Bailey e López de Prado (2014), JPM 40(5); López de Prado (2018). Stato C. La formula del DSR riportata in §7.2 è compatibile con quella dell'articolo, con la curtosi non in eccesso.
- **Limiti aggiuntivi rispetto a Gemini:**
  - il DSR richiede **il numero vero di prove e la varianza degli Sharpe tra le prove**: se le prove non sono registrate (anche quelle «mentali» di un LLM che scarta idee prima di eseguirle), il DSR è sottostimato;
  - la CPCV corregge la dipendenza temporale tra campioni, non la selezione dell'idea fatta conoscendo la storia.
- **Mia classificazione:** l'affermazione originale («eliminano») è **CONTRADDETTA**. La versione corretta («riducono, a condizioni precise») è **CONFERMATA CON LIMITI**.
- **Classificazione di Gemini (CONFERMATA CON LIMITI):** da precisare: è confermata la riformulazione, non l'affermazione originale.

### CLM-11 · STR-001 genera un alpha significativo con E[R] ≥ +0,15R
- **Categoria:** ipotesi di performance.
- **Evidenze:**
  - nessun backtest del progetto;
  - nella scheda (riga 97) +0,15R è un **criterio di valutazione**, non un risultato.
- **Fonti:** Moskowitz, Ooi e Pedersen (2012); Hurst, Ooi e Pedersen (2017). Stato C.
- **Evidenze contrarie e incongruenze:**
  1. STR-001 si chiama «TSMOM», ma il suo ingresso è un **breakout di Donchian a 20 giorni** (riga 54). Il TSMOM di Moskowitz e colleghi usa il segno del rendimento a 12 mesi. La letteratura citata sostiene una famiglia di strategie, non questa regola specifica.
  2. La scheda è detta «pre-registrata» (11/11/2026) con fuori campione 2018–2023 e forward 2024–2026 (righe 123–124): sono periodi già trascorsi e osservabili. Lo segnalai in Q-07.
- **Mia classificazione:** **NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI.**
- **Classificazione di Gemini (DECLASSATA A IPOTESI):** corretta.
- **Incoerenza:** la colonna «evidenza» continua a chiamare la scheda «(pre-registrata)», mentre la Fase 6 riconosce che 2018–2026 è già stato osservato.

### CLM-12 · I piccoli gap dell'S&P 500 si chiudono per riassorbimento dell'inventario dei market maker
- **Categoria:** ipotesi microstrutturale.
- **Fonti verificate (V-sec):**
  - **Lou, Polk e Skouras (2019)**, JFE 134(1): 192–213. Il terzo autore è Skouras, non «Skona» come scrive Gemini. L'articolo studia la scomposizione overnight/intraday dei rendimenti di 14 strategie cross-sectional e **non** tratta la chiusura dei gap né l'inventario dei market maker.
  - **Branch e Ma (2012)**, Journal of Applied Finance 22(2): correlazione negativa tra rendimenti overnight e intraday **dei singoli titoli**. È una regolarità compatibile con un'inversione, non con il meccanismo dichiarato né con un future sull'indice.
- **Valutazione:** la frase di Gemini «la letteratura documenta l'effetto medio» è più forte di ciò che le due fonti sostengono. Nessuna delle due documenta il meccanismo d'inventario.
- **Mia classificazione:** **NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI**.
- **Classificazione di Gemini (DECLASSATA A IPOTESI):** corretta come esito. Le fonti però sono citate in modo errato (autore) e usate oltre il loro contenuto.

### CLM-13 · Creare subito un repository dedicato
- **Categoria:** operativa.
- **Evidenze verificate:**
  - il repository GitHub `l-Altro` è un'applicazione TypeScript/pnpm (personaggio 3D) sui rami `main` (vuoto), `personaggio-3d`, `fase-*` e `antigravity-professore`;
  - il Brain vive **solo** sul ramo `claude/vibrant-cannon-5uunho`, cartella `brain/` (177 file tracciati).
  - Gemini lavora invece su una copia locale in `~/.gemini/antigravity/brain/…` e in `~/Downloads/l-Altro-personaggio-3d/`.
- **Mia classificazione:** l'affermazione che il workspace sia condiviso con codice estraneo è **CONFERMATA**. Che occorra crearlo «subito» spetta all'utente.
- **Classificazione di Gemini (DECLASSATA A PROPOSTA):** corretta.
- **Il quadro di D-01 è incompleto:** dice che i file sono «untracked» in `Downloads` e ignora che il Brain di Claude è già versionato su GitHub. Le copie sono quindi **almeno due**, non sincronizzate (vedi l'audit, §8.12).

### CLM-14 · p < 0,01 o t > 2,5 «garantisce» la solidità
- **Categoria:** criterio statistico.
- **Fonte:** Harvey, Liu e Zhu (2016), RFS 29(1). Stato C. È coerente con l'uso che ne fa Gemini: soglia t ≈ 3 per i nuovi fattori, in presenza di centinaia di fattori testati.
- **Mia classificazione:** l'affermazione originale è **CONTRADDETTA**: nessuna soglia di p «garantisce» solidità, tanto meno senza contare le prove.
- **Classificazione di Gemini (CONFERMATA CON LIMITI):** **errata come etichetta**. Gemini la smentisce nel merito e poi la classifica come confermata. Andava classificata come CONTRADDETTA, o come RIFORMULATA nella nuova regola.
- **Limiti della nuova regola:** t > 3 è una regola empirica per la scoperta di fattori in una letteratura con pubblicazione selettiva. Non sostituisce il conteggio esplicito delle prove (DSR, FDR) e non dice nulla sulla **potenza**: con edge piccoli servono migliaia di trade (§3, A-09).
- **Incoerenza interna del documento:** il gate della Fase 6 usa p < 0,01 (cioè t ≈ 2,58), §11.1 usa t > 3–3,5, §12 (R-01) usa Bonferroni/Holm.

### CLM-15 · La convergenza tra Claude e Gemini prova la validità
- **Categoria:** epistemologica.
- **Fonti:** Sharma et al. (2023, arXiv 2310.13548), stato C. **Pertinenza parziale:** studia la tendenza a compiacere l'**utente** umano, non la correlazione degli errori tra due modelli. Il rischio di errori correlati tra modelli è plausibile (dati di addestramento simili, contesto condiviso tramite l'utente), ma la fonte citata non lo dimostra.
- **Mia classificazione:** **CONTRADDETTA** come prova di validità.
- **Classificazione di Gemini (RITIRATA):** corretta. La formula del testo principale (§4.1.4, «valore probatorio **nullo**») è però troppo forte: un accordo raggiunto in modo indipendente (stime sigillate prima del confronto) è un'evidenza debole e non nulla; un accordo raggiunto dopo aver letto l'altro vale quasi zero. Vedi A-02.

### CLM-16 · Il «criterio di Kelly continuo NormalDist().inv_cdf» garantisce la crescita massima
- **Categoria:** finanziaria teorica.
- **Evidenze verificate:**
  - `prop_risk_engine_v3_3.py` **non calcola alcuna frazione di Kelly**: `calculate_kelly_confidence_interval` restituisce solo E[R], SE e l'IC di E[R];
  - la riga 80 citata da Gemini è un controllo d'input;
  - `NormalDist().inv_cdf` calcola il quantile dell'intervallo e non ha relazione con Kelly;
  - il f* del progetto (0,3363%) è un'**euristica di vincolo sul drawdown**, f* = 2·m·D/(s²·ln(1/α)), non la frazione di Kelly che massimizza la crescita.
- **Fonti:** Kelly (1956), MacLean, Thorp e Ziemba (2011), Baker e McHale (2013). Stato C. Il loro uso nel testo (Kelly frazionario sotto incertezza dei parametri) è compatibile con queste fonti.
- **Mia classificazione:** **CONTRADDETTA**. L'affermazione confonde tre oggetti diversi, e l'evidenza citata non contiene ciò che le viene attribuito.
- **Classificazione di Gemini (CONFERMATA CON LIMITI):** **errata**. I limiti descritti su Kelly sono corretti, ma l'affermazione esaminata è falsa, e la sua «evidenza» (riga 80) non esiste.

---

## 3. Affermazioni sostanziali non incluse nell'audit di Gemini

| Id | Affermazione (documento principale) | Dove | Evidenza / argomento | Mia classificazione |
|---|---|---|---|---|
| A-01 | «Tutti i riferimenti citati … sono stati verificati» | §15, riga 575 | Errori dimostrati: Lo, Repin e Steenbarger (2005) in rivista, volume, pagine e DOI sbagliati, e presentato come «misurazione fisiologica» (era un questionario); DOI di Almgren-Chriss errato (`JOR.2000.042` invece di `JOR.2001.041`); Bouchaud-Farmer-Lillo citato in due sedi diverse (§10 e §15); Lou-Polk-«Skona». Nessuna traccia del metodo di verifica | **CONTRADDETTA** |
| A-02 | «La concordanza tra Claude e Gemini ha valore probatorio nullo» | §4.1.4 | Un accordo raggiunto in modo indipendente (stime sigillate prima del confronto) è un'evidenza debole ma informativa; un accordo dopo lettura reciproca vale circa zero | **RIFORMULATA**: «non costituisce verifica; vale come evidenza debole solo se raggiunta senza contatto» |
| A-03 | «Somma lineare dei rischi, scenario peggiore di correlazione unitaria ρ = 1» | §8, §8.3, §12 R-06 | La somma dei rischi fino agli stop è il caso «tutti gli stop colpiti insieme». Con posizioni di segno opposto su strumenti positivamente correlati, ρ = 1 **riduce** la perdita (copertura). Il caso peggiore è la co-monotonicità delle perdite, non ρ = 1 | **RIFORMULATA** (la mia risposta in chat sul sistema di valutazione del rischio conteneva la stessa formulazione imprecisa: lo riconosco nel registro delle divergenze, D-03) |
| A-04 | Perdita allo stop e «numero esatto di stop consecutivi tollerabili» come limiti deterministici | §3.3, §8 | Sono deterministici **solo se lo stop viene eseguito al suo prezzo** (ipotesi H_esec). Con gap o slippage la perdita è maggiore (§7.1 lo riconosce per i backtest, ma non per il Guardian) | **CONFERMATA CON LIMITI**: «derivato deterministico condizionato a H_esec», più una riserva per i gap da dichiarare come stima o ipotesi |
| A-05 | «Registri fisicamente separati» garantiscono l'indipendenza | §4.1.1, R-02 | Entrambi i registri stanno nello stesso Brain, che entrambi i modelli possono leggere; l'utente trasferisce i testi da un modello all'altro; la separazione delle cartelle non impedisce la lettura | **NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI** (servono stime sigillate con hash prima della lettura reciproca e un registro degli accessi) |
| A-06 | «Replicabilità indipendente: lo script eseguito dalla controparte produce risultati identici» | §5, criterio 1 | Rieseguire lo stesso codice verifica la **riproducibilità**, non l'indipendenza; un errore nel codice si riproduce identico. Le revisioni V3.x hanno trovato errori grazie a **reimplementazioni indipendenti** (calcolo esatto, forme chiuse) | **RIFORMULATA**: riproducibilità più verifica con metodo indipendente |
| A-07 | «Se win-rate con N < 30 → NON STIMABILE» | changelog §3.2 | La stimabilità dipende dalla precisione necessaria per la decisione, non da una soglia fissa: con N = 300 l'edge di riferimento non è distinguibile da zero (Q-01); con N = 25 un tasso di violazione può già escludere valori estremi | **CONTRADDETTA** come criterio generale |
| A-08 | «Se E[R] < 0,10R la strategia viene rigettata» | §12 R-04 | Soglia arbitraria, introdotta nello stesso documento che declassa le soglie arbitrarie (CLM-02). Il criterio corretto dipende da costi stimati con incertezza e dalla varianza | **NON DIMOSTRABILE**; declassare a proposta |
| A-09 | Paper trading di «3–6 mesi» basta per verificare la discrepanza tra backtest ed esecuzione | §9, Fase 9 | [DERIVATO condizionato a WR 0,40, R:R 2, i.i.d., edge 0,15R] Per un test con potenza 80% servono **594 trade**: circa 14 mesi a 2 trade al giorno, 4,7 mesi a 6. Con soglia t > 3 servono **1.417 trade** (`output/potenza_campione.txt`). La durata va fissata in numero di trade da un calcolo di potenza, non in mesi | **NON DIMOSTRABILE** come durata generale |
| A-10 | «Divieto del same-bar fill» salvo dati tick | §7.1 | Un ordine stop a riposo viene eseguito **nella** barra in cui il prezzo attraversa il livello, al livello o all'apertura se c'è un gap. Rinviarlo all'apertura successiva introduce una distorsione di segno opposto. Il problema reale è l'ordine intra-barra quando stop e target sono toccati nella stessa barra: va risolto assumendo il caso peggiore (Q-07 chiedeva proprio un riempimento al livello o all'apertura in caso di gap) | **RIFORMULATA** |
| A-11 | «Webhook nativi a bassissima latenza» | §6.2 | Nessuna misura né fonte | **NON VERIFICATA** |
| A-12 | Fase 0 «completata», Fasi 1–7 «correnti» | §9, classi del diagramma | Nessuna fase 1–7 è stata avviata, e l'utente non ha autorizzato avvii | **CONTRADDETTA** |
| A-13 | Lo, Repin e Steenbarger (2005): «misurazione fisiologica dello stress e dell'arousal» | §15 n. 11; §10 riga 19 | V-sec: studio con questionari giornalieri e inventari di personalità. La misura fisiologica è in Lo e Repin (2002), stato C | **CONTRADDETTA** |
| A-14 | Loewenstein, Barber-Odean e Lo-Repin-Steenbarger «dimostrano» che l'arousal altera la percezione del rischio e favorisce l'overtrading | §8.2 | Barber e Odean (2001) studiano overconfidence e genere, non l'arousal (stato C). L'insieme delle fonti sostiene un nesso tra emozioni, overconfidence e risultati, non un meccanismo dimostrato | **RIFORMULATA** («evidenze compatibili», non «dimostra») |
| A-15 | Gerarchia delle evidenze: teoremi al 3° posto, sotto gli studi empirici | §2.2 | Mette sullo stesso asse due domande diverse: la correttezza di una derivazione e la verità empirica delle sue ipotesi. Un teorema è certo entro le sue ipotesi; il problema è se le ipotesi valgono. Inoltre `STANDARD.md` §1–§2 (F1–F7, E1–E7) esiste già e non viene richiamato | **RIFORMULATA** |
| A-16 | Formula della perdita allo stop: Size × (Entry − SL) + Fees | §8.3 (in §3.1 c'è il valore assoluto) | Per vendite allo scoperto serve il valore assoluto. Per CFD, futures e FX servono anche moltiplicatore, valore del tick e cambio verso la valuta del conto. Il cambio è a sua volta una MISURA con ora e fonte | **CONFERMATA CON LIMITI** (incompleta) |
| A-17 | Il modello a 5 tipi «impedisce la contaminazione» | changelog §2; §3 | Il documento descrive i tipi, ma non specifica schema, campi, formato né meccanismo di applicazione nel codice. Una descrizione non impedisce nulla finché non è applicata e testata | **NON DIMOSTRABILE CON LE EVIDENZE DISPONIBILI** (progettato, non implementato) |
| A-18 | «Propagazione: il risultato di misura e ipotesi assume lo status di IPOTESI» | changelog §3.1, contro «IPOTESI CONDIZIONATA» in §3.2 | Incoerenza interna. Etichettare il risultato «IPOTESI» perde l'informazione utile, cioè **quali** ipotesi lo condizionano. Più corretto: tipo del calcolo, più l'insieme delle condizioni {H…} | **RIFORMULATA** |

---

## 4. Bibliografia del documento principale (§15) e della tabella §10

| Fonte (come citata) | Verifica | Problemi |
|---|---|---|
| Almgren e Chriss (2000), J. of Risk 3(2) 5–39, DOI 10.21314/JOR.2000.042 | V-sec | **DOI errato**: corretto `10.21314/JOR.2001.041`; anno di stampa 2000/2001 |
| Bailey e López de Prado (2014), JPM 40(5) 94–107 | C | — |
| Barber e Odean (2001), QJE 116(1) | C | Usata per l'arousal (§8.2): pertinenza impropria |
| Borodin e Salminen (2002), 2ª ed. | C | — |
| Bouchaud, Farmer e Lillo (2009) | V-sec (esistenza: arXiv 0809.0822) | DOI e pagine non confermati; **due sedi diverse** nel documento (§10: «Quantitative Finance»; §15: Handbook) |
| Brier (1950) | C | — |
| Harvey, Liu e Zhu (2016), RFS 29(1) 5–68 | C | — |
| Hurst, Ooi e Pedersen (2017), JPM 44(1) | C | Usata per una regola di Donchian (vedi CLM-11) |
| Kahneman e Tversky (1979) | C | — |
| Kelly (1956) | C | — |
| **Lo, Repin e Steenbarger (2005)** | V-sec | **Citazione errata**: AER 95(2) 352–359, non «Cognitive Neuroscience 17(10) 1693–1759»; DOI non pertinente; contenuto descritto in modo errato |
| López de Prado (2018) | C | — |
| Moskowitz, Ooi e Pedersen (2012), JFE 104(2) | C | Vedi CLM-11 |
| Sharma et al. (2023) | C | Pertinenza parziale (CLM-15) |
| White (2000), Econometrica 68(5) | C | — |
| Tabella §10: Strang, Rudin, Burden-Faires, Shiryaev, Casella-Berger, Gelman et al., Hamilton, Karatzas-Shreve, Embrechts et al., Markowitz, McNeil et al., Kirkpatrick-Dahlquist, Obstfeld-Rogoff, Murphy, Ang-Bekaert, Thaler, Pearl, Hastie et al., Boyd-Vandenberghe, Kleppmann, Martin, Kreuzberger et al., Stallings, Popper | C | Testi esistenti e pertinenti per la disciplina, a mia conoscenza; non riletti. Murphy (1991) e Kirkpatrick-Dahlquist sono testi divulgativi o professionali (F6–F7 di `STANDARD.md`), non fonti «scientifiche fondamentali» |
| Fonti nell'audit delle affermazioni: Lou, Polk e «Skona» (2019) | V-sec | **Nome dell'autore errato** (Skouras); contenuto non pertinente al meccanismo |
| Branch e Ma (2012) | V-sec | Pertinenza parziale |
| Pine Script v5 Reference Manual | V-sec (indiretta) | Non aggiornata: v6 dal 10/12/2024 |

**Bilancio:**
- su 6 citazioni controllate al web, **4 hanno errori dimostrati** (Lo, Repin e Steenbarger; Almgren-Chriss; Lou-Polk-Skouras; Pine v5) e **1 ha sede incoerente** (Bouchaud et al.);
- il campione è stato scelto puntando le citazioni sospette, quindi questo tasso **non** è rappresentativo dell'intera bibliografia;
- basta però a smentire «tutti i riferimenti … verificati».

**Raccomandazione (decisione dell'utente):** nessuna fonte entra nella bibliografia del Brain con stato V senza una registrazione della verifica (data, URL o identificativo, chi l'ha fatta), come già prescrive `STANDARD.md` §3.

---

## 5. Sintesi

| Giudizio sulla classificazione di Gemini | Voci |
|---|---|
| Corretta | CLM-01 (motivazione imprecisa), 03, 04, 06, 07, 08, 09, 11, 12 (esito corretto, fonti errate), 13, 15 |
| Corretta ma da precisare | CLM-02 (manca l'alternativa «regola personale»), CLM-05 (due affermazioni fuse), CLM-10 (si conferma la riformulazione, non l'originale) |
| **Errata** | **CLM-14** (classificata confermata, ma contraddetta nel merito); **CLM-16** (affermazione falsa, evidenza inesistente) |
| Errore di conteggio | Sintesi: 4 e 2 invece di 5 e 1 |

**Grado di certezza:**
- **alto** per i rilievi su codice, file del progetto, conteggi e citazioni verificate al web;
- **medio** per le valutazioni di pertinenza delle fonti in stato C;
- **non valutabile** la fedeltà delle citazioni al rapporto V1, che manca.

<!-- FINE DOCUMENTO: CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md -->


---

<!-- INIZIO DOCUMENTO: CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md -->

# Registro delle divergenze tra l'analisi di Claude e la revisione V2 di Gemini (V1)

**Autore:** Claude Code · **Data:** 12/11/2026
**Riferimenti:** [`CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md`](CLAUDE_INDEPENDENT_ARCHITECTURE_AUDIT_V1.md) (abbreviato «Audit») e [`CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md`](CLAUDE_EVIDENCE_AND_CLAIMS_REVIEW_V1.md) (abbreviato «Evidenze»).
**Scopo:** non stabilire chi ha ragione, ma rendere esplicita ogni differenza, il motivo e la conseguenza. Dove anch'io avevo torto, o una visione incompleta, lo dichiaro.

**Categorie di giudizio:**
- **EO** errore oggettivo, dimostrabile con codice, file o fonti;
- **INT** interpretazione differente;
- **SCE** scelta architetturale;
- **APE** questione aperta, che spetta all'utente;
- **NR** non risolvibile con le evidenze disponibili.

---

## 1. Divergenze

| Id | Questione | Posizione di Gemini | Mia posizione | Evidenze | Giudizio | Conseguenza progettuale |
|---|---|---|---|---|---|---|
| D-01 | Conteggio dell'audit delle affermazioni | 4 ritirate, 2 proposte | 5 ritirate (CLM-01, 03, 06, 09, 15), 1 proposta (CLM-13) | Tabella dell'audit di Gemini | **EO** | Correggere sintesi e LEGGIMI |
| D-02 | Propagazione del tipo | Il risultato di misura più ipotesi diventa «IPOTESI» (changelog) o «IPOTESI CONDIZIONATA» (§3.2) | Il risultato conserva il tipo del calcolo più l'**insieme delle condizioni {H…}** e l'incertezza propagata | Incoerenza interna tra i due documenti; perdita dell'informazione necessaria all'analisi di sensibilità (Audit §3.2) | **SCE** (con incoerenza **EO**) | Lo schema dei metadati deve avere un campo «condizioni» |
| D-03 | Limite di portafoglio | «Somma lineare, ρ = 1 = caso peggiore» | Il caso peggiore è «tutti gli stop colpiti insieme» (perdite co-monotone). Con posizioni di segno opposto ρ = 1 riduce la perdita. **La mia risposta in chat conteneva la stessa formulazione imprecisa** | Argomento matematico (Audit §3.5) | **EO** (di entrambi) | Rinominare il limite; il calcolo (somma dei rischi a stop) resta valido |
| D-04 | Natura dei «limiti deterministici» | Perdita allo stop e stop consecutivi residui sono deterministici | Sono **DERIVATO condizionato a H_esec** (esecuzione dello stop al prezzo). Serve una riserva per gap e slippage, come STIMA o IPOTESI. **Anche la mia risposta in chat li presentava come deterministici senza condizione**, pur segnalando a parte l'ipotesi «stop senza gap» | §7.1 di Gemini riconosce i gap nei backtest ma non nel Guardian | **EO** (incompletezza di entrambi) | Il Guardian mostra la perdita a stop più la riserva per gap, e dichiara H_esec |
| D-05 | Criterio NON STIMABILE | Soglia N < 30 | Criterio legato alla decisione: NON STIMABILE quando l'intervallo contiene valori che porterebbero a decisioni diverse | Q-01: con N = 300 l'edge di riferimento non è distinguibile da zero | **EO** | Criterio nello schema; nessuna soglia fissa |
| D-06 | Tipo e stato di validazione | Un solo ordinamento (min sui tipi) | Assi ortogonali: tipo, condizioni, stato di verifica, evidenza esterna, livello di validazione, ciclo di vita, classe di contenuto | Audit §3.1: lo stato NON STIMABILE e la qualità delle regole non trovano posto nell'ordinamento | **SCE** | Proposta di schema da approvare |
| D-07 | Tassonomie | Nuove: §2.2 gerarchia delle fonti, §2.3 sette etichette, §11.2 livelli | Mapparle su `STANDARD.md` (F1–F7, E1–E7, V/V-sec/C/X, classi §8, L1–L5); conservare §11.2, che manca in `STANDARD.md` | `STANDARD.md` in vigore dall'11/11/2026 non è mai citato nel documento di Gemini | **EO** (omissione) e **SCE** | Un'unica «carta dei metadati» |
| D-08 | Valore della concordanza tra modelli | «Nullo» | Debole ma non nullo se raggiunta **senza contatto** (stime sigillate); circa nullo se raggiunta dopo lettura reciproca; mai una verifica | Ragionamento; CLM-15 | **INT** | Protocollo delle stime sigillate |
| D-09 | «Replicabilità indipendente» | La controparte riesegue lo script e ottiene lo stesso risultato | È **riproducibilità**. L'indipendenza richiede un **metodo diverso** (calcolo esatto, forma chiusa, reimplementazione) | Le revisioni V3.x hanno trovato gli errori solo con metodi indipendenti | **EO** (concettuale) | Il criterio di promozione nel Core richiede entrambe |
| D-10 | Indipendenza dei registri | Cartelle separate più «doppio cieco» | Le cartelle non impediscono la lettura; il doppio cieco è irrealizzabile (stili riconoscibili, utente come canale). Servono stime sigillate con hash e registro degli accessi | Audit §8.2 | **EO** (sulla fattibilità del doppio cieco) e **SCE** | F3 riformulata |
| D-11 | Livello comportamentale del Guardian | Solo misure oggettive, nessuna interpretazione | Misure **più** indicatori definiti prima, con interpretazione etichettata come IPOTESI e validata sui dati dell'utente | L'utente ha chiesto di segnalare FOMO, revenge trading e overtrading; G0 resta consultivo in entrambe le versioni | **SCE / APE** | Decisione dell'utente (Audit §10, punto 4) |
| D-12 | Posizione del Guardian nella roadmap | F7, dopo F6 (strategie validate) | Un G0 **minimo** (strato deterministico più journal) può precedere F6: richiede solo Q-09, dati del conto e schema dei tipi | Analisi delle dipendenze (Audit §6.2) | **SCE / APE** | Decisione dell'utente (Audit §10, punto 3) |
| D-13 | Ordine F8 → F9 | Il bot precede il paper trading | Il paper trading non richiede un sistema di gestione degli ordini; F8 opzionale e parallela | Audit §6.2 | **SCE** | Dipendenza da rimuovere |
| D-14 | Durata del paper trading | 3–6 mesi | In numero di trade da un calcolo di potenza: per l'edge di riferimento **594** trade (potenza 80%), **1.417** con t > 3 [DERIVATO condizionato] | `output/potenza_campione.txt` | **EO** (condizionato alle ipotesi dichiarate) | F9 espressa in trade, con piano pre-registrato |
| D-15 | Criterio di significatività | p < 0,01 (gate F6), t > 3–3,5 (§11.1), Bonferroni/Holm (R-01) | Un solo criterio: DSR con conteggio globale delle prove, più potenza dichiarata | Incoerenza tra tre sezioni dello stesso documento | **EO** (incoerenza) | Gate F6 riscritto |
| D-16 | Riempimento nella stessa barra | Vietato senza dati tick | Gli stop a riposo si riempiono nella barra di attraversamento, al livello o all'apertura in caso di gap. Il problema è l'ordine intra-barra stop/target: si assume il caso peggiore | Q-07 (revisione V3.1) chiedeva proprio questo per STR-001 | **EO** (metodologico) | Regola di esecuzione riformulata |
| D-17 | Collocazione di T-01…T-05 | Gate di ingresso della Fase 5 | Ambigua: F3 e F4 sono già fasi tecniche. L'utente ha detto «successiva fase tecnica» | Testo della decisione nell'incarico | **APE** | Decisione dell'utente (Audit §10, punto 2) |
| D-18 | TradingView (DEC-06) | «Visualizzazione e telemetria» | Grafici, prototipi Pine, Strategy Tester e segnali (come deciso dall'utente). Risultati dello Strategy Tester etichettati e mai usati come evidenza senza riproduzione locale | Decisione dell'utente nell'incarico | **EO** (scostamento dalla decisione) | Riformulare DEC-06 |
| D-19 | Bibliografia | «Tutti i riferimenti … verificati» | Errori dimostrati: Lo, Repin e Steenbarger (2005) in rivista, DOI e contenuto; DOI di Almgren-Chriss; «Skona»; Bouchaud et al. in due sedi; Pine v5 | Ricerca web (V-sec), `output/verifica_fonti_web.txt` | **EO** | Registro delle verifiche delle fonti (Evidenze §4) |
| D-20 | Classificazioni CLM-14 e CLM-16 | Confermate con limiti | CLM-14 contraddetta (smentita nel merito dallo stesso Gemini); CLM-16 contraddetta: il motore V3.3 **non calcola** alcuna frazione di Kelly | `prop_risk_engine_v3_3.py` | **EO** | Correggere l'audit |
| D-21 | «Formazione» dei due cervelli | Fasi 2–3: compendio e formazione | Un LLM non conserva apprendimento tra le sessioni. Si accumulano memoria esterna, strumenti verificati e calibrazione misurata; la padronanza si dimostra con prove a risposta nota | Natura dei modelli; Parte B §0 | **INT** (sull'esito pratico, **NR**: non so quanto un compendio migliori le prestazioni in sessione) | Test di padronanza riformulati (Audit §7.2) |
| D-22 | Contaminazione da addestramento | Non trattata | Le ipotesi generate da LLM possono incorporare la storia nota al modello; un OOS pulito esiste solo dopo il cutoff del modello e la data di registrazione | Audit §8.3 | **NR** sull'entità; **EO** sull'omissione del rischio | Registrare data e versione del modello per ogni ipotesi; i periodi storici valgono come prova debole |
| D-23 | Stato attuale del workspace | File «untracked» in `Downloads` | Il Brain di Claude è versionato su GitHub (ramo `claude/vibrant-cannon-5uunho`); le consegne di Gemini non sono nel Brain versionato; esistono almeno due copie non sincronizzate | `git ls-tree`, cartella `da-gemini/consegne` | **EO** (quadro incompleto) | D-01 deve includere la sincronizzazione, non solo il nuovo repository |
| D-24 | Gerarchia delle evidenze | Teoremi al 3° posto, sotto gli studi empirici | Assi diversi: correttezza della derivazione e verità empirica delle ipotesi | Evidenze A-15 | **INT** | Mappatura su E1–E7 più asse del tipo |
| D-25 | Soglia di costo | «E[R] < 0,10R → rigetto» | Soglia arbitraria, introdotta mentre si declassano le soglie arbitrarie | Evidenze A-08 | **EO** (incoerenza) | Declassare a proposta |
| D-26 | Formula della perdita allo stop | Size × (Entry − SL) + Fees | Valore assoluto; moltiplicatore, valore del tick, cambio (MISURA) | Evidenze A-16 | **EO** (incompletezza) | Specifica del calcolo in Q-09 / G0 |
| D-27 | Gate dei dati (F4) | 10 anni × 3 classi di attivo | Gate legato ai dati necessari alle ipotesi registrate; prima, la decisione su fornitore, licenze e costi | Rete dell'ambiente di Claude che rifiuta FRED, Yahoo, Stooq, Crossref; costi non valutati | **SCE / APE** | Decisione dell'utente sui dati |
| D-28 | Adeguatezza del Lomax | «Modella efficacemente le code» | Momenti corretti (confermato); adeguatezza allo slippage reale **non verificata** | Nessun dato di esecuzione | **EO** (affermazione non supportata) | Etichettare come IPOTESI fino ai dati di esecuzione |

---

## 2. Dove Gemini ha ragione (confermo, con motivazione)

| Punto | Perché lo confermo |
|---|---|
| G0 interamente consultivo, senza kill switch | Coerente con la decisione dell'utente. **Correggo un mio testo precedente:** il mio audit dell'11/11 (`audit/AUDIT-ARCH-20261111/05`, §3.3, componente 6) prevedeva per G0 un «blocco della sessione nel journal», formula ambigua rispetto a «non blocca nulla». La versione di Gemini è più netta |
| Esclusione del motore V3.3 dal rischio di portafoglio | Le ipotesi S-09 (trade sequenziali, nessuna posizione a mezzanotte) lo rendono non valido per posizioni simultanee: verificato nel codice |
| Precedenza dei limiti deterministici; una stima non allarga mai un limite | Corretto e importante: protegge dall'errore di stima nei regimi estremi |
| Livelli di validazione TEORIA → LIVE-REAL e divieto di usare il livello k come prova per k+1 | Corretto, e manca in `STANDARD.md`: va conservato |
| Pre-registrazione con hash | Corretto; va completata con data e versione del modello (D-22) |
| Declassamento delle soglie di 60–90 s e 15 minuti come leggi scientifiche | Corretto (con la precisazione che restano ammissibili come regole personali, CLM-02) |
| Simmetria dei ruoli | Coerente con la decisione dell'utente e utile alla resilienza |
| Changelog trasparente sugli errori della V1 | Buona pratica: rende il ciclo verificabile |
| Repository condiviso con codice estraneo | Verificato: il repository `l-Altro` contiene un'applicazione TypeScript sugli altri rami |

## 3. Dove entrambi avevamo una visione incompleta (terze soluzioni)

1. **Limiti «deterministici»** (D-04) e **ρ = 1** (D-03): stessa imprecisione in Gemini e nella mia risposta in chat. Soluzione: derivato condizionato a H_esec, riserva per gap, caso peggiore definito come «tutti gli stop colpiti».
2. **Indipendenza tra i nodi** (D-08, D-10): Gemini propone cartelle e doppio cieco; la mia Parte B proponeva stime sigillate, ma nessuno dei due ha affrontato il fatto che oggi **non esiste un archivio comune** (D-23). Soluzione: prima la fonte di verità unica e la sincronizzazione, poi i protocolli di indipendenza.
3. **Comportamento del trader** (D-11): né «solo misure» né «diagnosi». Indicatori pre-definiti, interpretazione come IPOTESI, validazione sui dati dell'utente.

## 4. Questioni non risolvibili con le evidenze disponibili

- Esistenza e contenuto del Master Mission (§§0–25).
- Fedeltà delle 16 citazioni al rapporto V1 di Gemini, non fornito.
- Entità della contaminazione da addestramento nelle ipotesi generate da LLM (D-22): si può stimare solo con esperimenti (Audit §9).
- Quanto un compendio disciplinare migliori le prestazioni effettive di un LLM nelle sessioni (D-21).
- DOI di Bouchaud, Farmer e Lillo, e in generale tutti i DOI: Crossref non è raggiungibile da questo ambiente.

## 5. Decisioni che spettano all'utente
Elencate nell'Audit, §10. Non ne ho presa nessuna.

<!-- FINE DOCUMENTO: CLAUDE_ARCHITECTURE_DIVERGENCES_V1.md -->
