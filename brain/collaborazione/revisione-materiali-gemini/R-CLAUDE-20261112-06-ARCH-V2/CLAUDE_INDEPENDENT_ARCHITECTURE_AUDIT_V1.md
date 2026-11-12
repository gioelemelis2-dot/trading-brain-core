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
