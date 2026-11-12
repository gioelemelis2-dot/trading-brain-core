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
