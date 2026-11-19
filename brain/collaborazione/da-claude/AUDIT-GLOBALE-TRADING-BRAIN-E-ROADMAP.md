# Audit globale del Trading Brain e della sua roadmap

**Autore:** Claude, su mandato del titolare del 19/11/2026 («Mandato a Claude — Revisione complessiva del Trading Brain e della sua roadmap»).
**Base esaminata:** ramo `feat/esecutore-h002`, commit `4c72573`. Il ramo `main` è fermo a `3063b98`: mancano 137 file e circa 35.700 righe del laboratorio.
**Natura:** audit documentale e metodologico **in sola lettura**. Non ho modificato codice, test, registri, roadmap, contatori o decisioni: questo rapporto è l'unico file scritto. Non ho aperto la riserva, i dati di mercato, risultati protetti o materiali della chat delle strategie. L'unico calcolo nuovo è un esempio **interamente inventato** (§3.2) e una formula di potenza (§3.1).
**Conflitto d'interessi dichiarato:** ho scritto gran parte del codice, dei test e delle specifiche che giudico. Per ogni conclusione indico chi ha prodotto l'evidenza e che cosa la smentirebbe.

> **ERRATA (19/11/2026, sera, dopo DGS-11).**
> - **Rischio n. 3 sovrastimato.** L'11,7% di false promozioni del §3.2 è in gran parte un artefatto del generatore inventato, dove le vincite erano tutte uguali.
> - **Con vincite realistiche:** 0/300 con perdite rare di −20 R e 5% con −50 R.
> - **Il rischio esiste solo per code di decine di R**, per esempio con stop molto stretti.
> - **Altre conclusioni da rileggere:** la capienza della riserva (circa 4 verifiche in tutto, omessa qui) e l'errore di metodo segnalato dal DGS (§8: ho giudicato la macchina intera con un solo criterio).
> - **Dettagli:** `RISCONTRO-DGS-11.md`.

---

## Pagina per il titolare

**La missione, ricostruita dalle fonti.**
- Il Brain nasce il **23/09/2026** come **manuale di studio** (moduli 0–10 con «cancelli»). L'11–12/11 diventa un **ecosistema pluriennale** di studio, ricerca quantitativa e controllo del rischio, per arrivare a un conto prop finanziato (D-14, Progetto generale §Scopo).
- Ha quattro pilastri: **conoscenza, ricerca, protezione, governance**.
- Le AI propongono e verificano; tu decidi; nessun denaro reale senza autorizzazione esplicita.
- Il documento fondativo originale (**Master Mission**) **non è mai stato trovato** (DA-02, aperta dall'11/11): la missione è ricostruita da decisioni e piani, non da un testo fondativo.

**Lo stato reale, in quattro righe.**
1. Abbiamo costruito con molto rigore **una parte sola** del sistema: il banco che giudica una strategia. Sono 117 difetti trovati e corretti in circa 10 giorni, la prima revisione pulita su due, un metro statistico collaudato.
2. **Nessuna strategia è stata provata**, e il banco **non è ancora completo** per farlo. La regola di verifica che hai scelto (D-31) non è ancora dentro il codice che giudica, e ogni nuova strategia richiede un suo simulatore.
3. Gli altri pilastri sono **costruiti ma mai usati** (Guardian, diario, registro delle previsioni) oppure **fermi** (formazione, consulto): il sistema oggi **non ti aiuta ancora a decidere**.
4. I dati veri stanno su **un solo Mac**, con la batteria guasta (copia nel cloud del 18/11).

**I tre rischi prioritari.**
1. **Il metro è più severo dei tuoi obiettivi.** Il tuo obiettivo (1–2% al mese) corrisponde a circa **+0,10 / +0,27 R a trade**. Con 1.000 sedute il metro promuove una strategia vera da +0,25 R solo **una volta su quattro**, e da +0,20 R quasi mai (§3.1). Il rischio è una macchina corretta che **non promuove mai** niente di utile per te.
2. **Il banco non è ancora «finito» per una strategia nuova**, e il ciclo di revisioni non ha un criterio di fine. Ogni nuovo strumento genera nuovi giri di revisione (§2.3).
3. **Le perdite rarissime ingannano tutti i controlli.** In un esempio inventato, con perdite gravi nello 0,2% dei trade il metro promuove per errore circa **una volta su nove** (11,7% su 300 prove) invece di meno del 2,5% (§3.2). Il collaudo copriva solo perdite rare all'1%.

**La prossima dimostrazione utile, con le risorse che abbiamo.**
- **(a) Prova generale a vuoto:** una strategia **inventata**, con verità nota, fatta passare per **tutta** la catena (scheda → sigillo → screening → prenotazione → verifica con D-31 → rapporto con i tipi «misura/stima/ipotesi») su mercati sintetici.
- **(b) Riconciliazione del Guardian** con 2–3 micro-operazioni sul conto **demo** MT4: chiude il Gate 1 e mette alla prova il pilastro «protezione».

Nessuna delle due richiede una strategia vera o la riserva (§4).

**Le decisioni che ti servono**, in ordine (§4.4):
1. che cosa fare del divario fra metro e obiettivo (§4.4 A);
2. una «definizione di fatto» della macchina, cioè l'elenco chiuso di ciò che manca e la fine del ciclo di revisioni;
3. dove custodire i dati oltre il Mac;
4. se e quando riattivare consulto, calibrazione e formazione, oggi fuori dalla roadmap.

**Perché vale la pena proseguire.** Il banco fa bene ciò che promette: i falsi positivi sono sotto controllo, misurati e riproducibili (0/100 mercati senza vantaggio promossi; verdetto del collaudo riprodotto da Gemini). Anche un sistema che **boccia** con onestà ti protegge da perdite reali.

**Che cosa renderebbe ragionevole cambiare strada:**
- se, a macchina finita, le prime 3–5 ipotesi ben formate risultano tutte «non decidibili» per mancanza di potenza, e non «bocciate»: il disegno sarebbe inadatto alla scala dei tuoi obiettivi;
- se il costo di un'ipotesi (simulatore più revisioni) resta di settimane.

---

## 1. Mappa: obiettivi, capacità, stato

Legenda dello stato:
- **D** deciso;
- **P** proposto;
- **R** rinviato o parcheggiato;
- **S** superato;
- **Di** soltanto discusso;
- **?** origine da confermare.

| Obiettivo del titolare | Capacità richiesta | Fonte e data | Stato documentato | Prova disponibile | Dipendenze | Fase prevista |
|---|---|---|---|---|---|---|
| Imparare a ragionare e operare (percorso formativo) | Manuale per moduli con cancelli; lezioni verificate | `originale/manuale-v1` (23/09); D-01, D-03 (11/11) | **D** come base di conoscenza. Modulo 2: 6 lezioni «in_verifica» v0.1. Sviluppo sospeso (D-10, D-12) e riaperto solo per L2.4–L2.6 (D-20) | Lezioni con fonti V-sec; **nessun registro dei cancelli superati** dal titolare | Revisione esterna (DA-10); tempo del titolare | **Nessuna fase nella roadmap del 17/11** → idea senza posto |
| Un «cervello» che contesta le letture, riconosce FOMO e suggerisce di astenersi | Consulto strutturato; indicatori comportamentali | Proposta di Claude (12/11, `CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` §6); DA-12 | **P** (proposta mai approvata); DA-12 **aperta**. Esiste un indicatore, `pattern_r1` (rientro dopo una perdita), nel journal | Test unitari del journal; **nessun uso reale** | Journal con dati veri; parametri fissati dal titolare (DA-12) | **Nessuna fase** → idea senza posto |
| Che il sistema «impari» | Apprendimento esternalizzato: registri versionati, calibrazione, errori, repliche | Proposta §0 e §3 (12/11) | **P**. Il sistema non modifica sé stesso: impara solo ciò che viene scritto e approvato (D-14: «promozione della conoscenza validata» con approvazione umana). Realizzati: registro dei difetti (117 voci), errori dichiarati, registro delle previsioni nel journal | Registro dei difetti; registro delle previsioni implementato ma **vuoto** | Uso del titolare; dati | Parziale; calibrazione **mai avviata** |
| Distinguere misura, derivato, stima, ipotesi, regola fino all'ultimo rapporto | Schema dei valori con tipo, condizioni, incertezza, fonte | `MODELLO-EPISTEMICO.md` (DA-06 proposta; applicato al G0, D-20); Progetto generale, principio 2 | **D per il G0**, **P per il resto**. **Il laboratorio non lo applica**: i rapporti di screening e verifica stampano valore, soglia e ✅ senza tipo né incertezza (`criteri.py` righe 190–204) | 77 test del Guardian sul tipo epistemico | DA-06 | **Lacuna d'interfaccia** (§2.2 I2) |
| Protezione: regole personali e limiti FTMO | G0 consultivo: scheda pre-trade, limiti, stress | D-16, D-22; Q-09 (12/11) | **D, implementato**: 14 regole personali confermate, regole FTMO verificate il 12/11. **Uso per decidere NON AUTORIZZATO** finché `riconciliato = false` | 77 test, mutanti; **nessuna riconciliazione** con un estratto conto | Conto demo con il broker reale (DA-25) | Gate 1, **in corso** |
| Diario, analisi degli errori, previsioni | Journal a catena solo in aggiunta, previsioni con punteggio di Brier | DA-16, D-20 (12/11) | **D, implementato**; **zero dati reali** (la cartella contiene solo LEGGIMI e il lock) | 32 test | Uso del titolare | Gate 5, ma utilizzabile da subito |
| Dati storici XAUUSD e riserva cieca | Scaricatore, controllo, intersezione BID/ASK, censimento | DA-26 → D-29 (14/11) | **D**. BID 2005–2023 completo e PULITO (18/11); **ASK al 57% circa**; intersezione e buchi per anno da fare; date esatte della riserva da decidere | `controlla_cache`, riconteggio del 17/11 | Mac (batteria guasta), Dukascopy | Gate 2 |
| Spendere la riserva poche volte e bene | Registro della riserva: α_j = α/[j(j+1)]/m, finestre, parte protetta | `riserva.py` (16/11); DGS-08 §4d | **Implementato, non ratificato** (α, finestre, parte protetta aperte) | Test e mutanti | Decisioni del titolare | Gate 2–4 |
| Un banco di prova di cui fidarsi | Sigillo, caricatore BID/ASK, criteri, lanciatore, registro delle prove | H-002 (13–17/11); D-24 | **D**: perimetro a **1 giro pulito su 2** (D-26); R17 in corso | 432 test e mutanti al 100% su 3.13 e 3.9 (Claude); R16 pulito (Gemini, Apple Python); taratura su 200 mercati (Gemini) | R17; giro su tutte le manomissioni; protezione del ramo; unione in `main` | Gate 2½ |
| Un metro statistico che non promuova il caso | Intervallo IA-02 collaudato (D-31) | IA-02 (`032250b`); DGS-07/08; D-25, D-31 | **D** sulla carta: bootstrap con Δ = 0,05 R confermato **su dati sintetici**. **Non integrato** nel codice che giudica una strategia | Impegno con impronte; verdetto riprodotto da Gemini (R17 B) | Un criterio generico da costruire e collaudare nel perimetro | Gate 2½ → 3 |
| Simulare la strategia minuto per minuto | Simulatore specifico; motore a eventi generico | `orb_londra.py` (H-002); `backtester/engine.py` («Binario B», 11/11) | **Due motori**: quello di H-002 è specifico, quello generico **non è usato dalla catena** (`criteri.py` importa solo il DSR) | Test di entrambi | Per H-003 servirà un simulatore nuovo o adattato | Gate 3 |
| Contare tutte le prove (N) | Registro unico delle prove | DA-19 (emendata il 14/11); DA-28 | **Tre file di conteggio**: `laboratorio/trial_registry.json` e `dati/operativo/trial_registry_xauusd.json` (Binario B, entrambi a 0) e il registro canonico `laboratorio/registro_prove.json` (#86, non ancora creato). DA-28 **aperta** | — | DA-28 | Gate 3 (§2.2 I3) |
| Costi realistici | Specifiche del broker, spread, commissione | DA-25; `dati/costi/` (18/11) | Specifiche registrate; **commissione da confermare** (per lato o in totale); export dei tick non disponibile nell'app MT5 per Mac | Specifiche lette dal titolare | Risposta del broker | Gate 1/3 |
| Scrivere strategie verificabili | Modello di scheda H-003 | `MODELLO-SCHEDA-H-003.md` (16/11); DGS-10; D-32 | **Parzialmente approvato** (G, H, F); restano DA-31, screening, minimi, costi | — | Decisioni del titolare | Gate 3 |
| Idee esterne senza contaminare | Registro di provenienza; censimento per mercato | DGS-09; D-32; D-33 | **D**; lavoro su P-001 **in pausa** (D-33) | Righe P-001 | — | Continuo |
| Provare in demo e sapere quando fermarsi | Fedeltà al backtest; test di Wald | DA-29 (proposta di Claude, delegata il 13/11); `simulazione_sprt.py` | **Delegato e proposto**, simulato su dati inventati | Simulazione riproducibile | Strategia promossa; conto demo | Gate 5 |
| Superare la sfida FTMO | Probabilità di superamento e rovina | Progetto generale (stima IPOTESI); «studio rovina 10.000 Monte Carlo» di Gemini | Stima di Claude **etichettata IPOTESI** (moto browniano, senza limite giornaliero né code); lo studio di Gemini è **annunciato e mai ricevuto** (REGISTRO-CONOSCENZE) | Formula chiusa di riferimento (strumento di revisione) | Vantaggio misurato in demo | Gate 6 |
| Semi-automazione | Expert Advisor su MT5 | DA-30; D-18 | **R** dopo il Gate 5 | — | Strategia promossa | Dopo il Gate 5 |
| Più mercati (GBPJPY…) | Calendario comune, registro unico, adattamenti | DA-27, DA-28; PIANO-DIVERSIFICAZIONE; DGS-09 §2 | **P**, pianificazione; censimento di GBPJPY aperto | — | Base sull'oro chiusa | Dopo il sigillo dell'oro |
| Osservare il proprio ragionamento | Osservatorio: previsioni registrate prima dell'esito | `piano/IDEA-OSSERVATORIO-RAGIONAMENTO.md` (16/11) | **R**, parcheggiata con condizioni | — | Journal; cancelli | Futura |
| Grafici e segnali | TradingView/Pine solo visivo; motore indipendente | D-18, DA-14 | **D** | Indicatore delle sessioni | — | Ausilio |
| Testo fondativo | Master Mission e Protocollo comune | D-09; DA-02 (11/11) | **Testi assenti, origine da confermare**; DA-02 aperta | — | Il titolare | Aperta da 8 giorni |
| Fonte unica di verità | Repository autonomo | D-02, D-19 | Repository creato; **tutto il laboratorio è su un ramo non unito** | git | Unione autorizzata | Prima della verifica |

**Funzioni costruite senza uno scopo ancora rintracciabile nella catena attuale** (da dichiarare «eredità» o da rimuovere, con decisione):
- il motore a eventi e i registri di prova di «Binario B»;
- le parti della pipeline legate alla vecchia partizione 70/30 (`partitioning.py`, accanto a `partizione_date.py`), superata da D-29.

Le ho viste a campione: «senza scopo» è un rischio plausibile, non un difetto dimostrato.

**Contrasti fra vecchie idee e decisioni successive**:
- **«IS 70% / OOS 30%, sigillo commitment.json»** (architettura dell'11–15/11) contro **D-29** (inversione, 14/11). Guida D-29.
- **Gate 1 «chiuso»** (tabella del 13/11) contro il rilievo G-20261113-01 («configurato ma non riconciliato»). Guida il rilievo, corretto il 19/11.
- **Regole personali «proposta»** (`guardian/LEGGIMI.md`) contro le **14 confermate** nel file delle regole. Guida il file: la documentazione è vecchia.

---

## 2. Coerenza, validità, fattibilità

### 2.1 Tre domande per le capacità principali

| Capacità | Quale problema risolve per il titolare | Che cosa produce oggi | Quale prova distinguerebbe utile da convincente |
|---|---|---|---|
| Banco di prova | Non credere a strategie che sembrano funzionare per caso | Verdetti su mercati **sintetici**: 0/100 promozioni senza vantaggio, 38/50 con vantaggio medio (Gemini, R16) | Su un'ipotesi vera, un verdetto riproducibile da un terzo, con potenza dichiarata prima. Oggi nessuna |
| Metro IA-02 | Non promuovere vantaggi sotto 0,15 R | Un intervallo collaudato su 12 scenari, 1.000 sedute | La potenza utile per i tuoi obiettivi (§3.1) e la tenuta fuori dal dominio (§3.2) |
| Guardian G0 | Rispettare limiti e regole sotto pressione | Una scheda pre-trade **mai riconciliata** con un conto | Avvisi corretti e falsi avvisi su operazioni demo reali (§4.3) |
| Journal e previsioni | Imparare dai propri errori e misurare la calibrazione | Struttura vuota | 30 o più previsioni con punteggio di Brier confrontato con una base ingenua |
| Riserva e provenienza | Non ingannarsi riusando dati già visti | Censimenti e registri | Un'apertura della riserva contabilizzata senza contestazioni |

**Un esempio seguito fino in fondo:** il verdetto «CONFERMATO NEL DOMINIO DEL PILOTA».
1. Impegno preregistrato con impronte (`IMPEGNO-PROTOCOLLO-IA02.md` §1–§8).
2. File dei limiti archiviato (SHA-256 `564eba71…`).
3. Rendiconto meccanico.
4. Ricalcolo indipendente delle soglie (DGS-08) e riproduzione del verdetto (Gemini, R17 B).

La tracciabilità **funziona**. Ma l'output arriva al titolare come «confermato», mentre la cosa che conta (potenza a +0,20 R: 3%) sta in una nota. È il caso del «numero giusto che risponde a una domanda diversa» (§3.1).

### 2.2 Interfacce fra le parti: passaggi precisi e conseguenze

- **I1. La verifica sigillata non usa la regola che hai scelto.**
  - `criteri.verifica` (perimetro sigillato) controlla «R medio netto > 0», DSR, anni e drawdown, ma **non** il limite inferiore di D-31 (`criteri.py`, criteri a riga 167 e seguenti).
  - Era la specifica di H-002, anteriore a IA-02. Per H-003 il criterio D-31 va **costruito, collaudato e messo nel perimetro**.
  - Conseguenza: «macchina finita» oggi significa «finita per H-002». Evidenza: lettura del codice (Claude). Lo smentirebbe un modulo D-31 già nel perimetro che non ho trovato.
- **I2. I rapporti del laboratorio non portano il tipo epistemico.**
  - Il principio 2 del Progetto generale («ogni numero ha un tipo») vale nel G0 ma non nei rapporti di screening e verifica (`criteri.py` righe 190–204).
  - Conseguenza: un «R medio 0,31 ✅» stampato su 780 sedute di sviluppo può arrivare al titolare come un fatto, mentre è una **stima** con un intervallo largo.
- **I3. Tre registri delle prove.** Il DSR di «Binario B» legge `laboratorio/trial_registry.json`; il sigillo e l'esecutore usano `registro_prove.json`; esiste anche `dati/operativo/trial_registry_xauusd.json`. Conseguenza: N potrebbe essere contato in modo diverso a seconda dello strumento usato. Rischio plausibile: oggi sono tutti vuoti, ma DA-28 è aperta.
- **I4. Una metrica per trade letta come protezione del conto.**
  - IA-02 e il drawdown in R della verifica non dicono quanto è probabile violare il limite **giornaliero** FTMO (5% = 10 R con lo 0,5% a trade).
  - La stima «con +0,05 R circa 88% in ~400 trade» del Progetto generale è correttamente etichettata IPOTESI, ma ignora il limite giornaliero e le code.
  - Il ponte giusto è G0 più stress, oggi mai riconciliati.
- **I5. Accordo fra agenti scambiato per prova indipendente.**
  - La replica di Gemini nasce dalla **stessa specifica** scritta da Claude, e il DGS ricalcola **sui conteggi di Claude** (lo dice DGS-08: «attestazioni»).
  - Errori comuni passano: #112 (contratto del bootstrap) lo ha trovato il DGS leggendo la specifica, non la replica; #106 e K15c sono stati trovati tardi.
  - La memoria di ChatGPT ha passato contesto fra chat (DGS-09 §3).
  - Conseguenza: «tre AI concordano» vale meno di quanto sembri.
- **I6. Prezzi di Dukascopy contro prezzi del broker.** Il banco usa lo spread di Dukascopy; il broker potrebbe essere diverso. C'è un solo confronto istantaneo (0,40 $ presso il broker il 18/11). Prova mancante.
- **I7. Moduli «decisionali» che scavalcano il titolare: nessuno trovato.** Il G0 non blocca (D-16), nessun ordine parte dal Brain, la scelta meccanica del collaudo l'ha adottata il titolare (D-25). Coerente.

### 2.3 Fattibilità organizzativa

| Fattore | Stato misurabile oggi | Rischio |
|---|---|---|
| Ritmo del lavoro | 343 commit dal 10/11; giri R7–R17; 117 difetti | **Ciclo senza fine**: ogni strumento nuovo (pilota, protocollo, costi, intersezione) diventa perimetro di revisione. Non esiste una «definizione di fatto» della macchina |
| Costo di un'ipotesi | H-002: circa 5 giorni fra scheda, simulatore e revisioni, senza arrivare all'esecuzione | Ogni ipotesi richiede **un simulatore specifico** più due giri puliti: settimane per ogni idea |
| Tempo del titolare | Oltre 10 decisioni aperte (riserva, DA-31, screening, minimi, costi, protezione del ramo, unione, DA-02, DA-12…) | Le decisioni si accodano; il lavoro tecnico va più veloce di quello decisionale |
| Dati | Un solo Mac; batteria guasta; Dukascopy instabile (503); disco pieno il 19/11 | Un singolo punto di guasto; riscaricare richiede giorni |
| Credito degli agenti e continuità | `CONTINUITA.md` fermo al 17/11; `STATO-PROGETTO` con contatori vecchi (366 test, ~370 mutanti) | Una sessione nuova ricostruirebbe un contesto superato |
| Aggiungere un mercato | Dati, censimento, adattamento degli strumenti, collaudo del dominio (DGS-09 §2) | Moltiplica il costo per ogni ipotesi |

**Dipendenze circolari:** non ne ho trovate di vere. Sigillo → screening sullo sviluppo → diagnostica del dominio → prenotazione è una sequenza lineare (DGS-10 §6). C'è però un **circolo pratico**: ogni correzione nel perimetro crea un candidato nuovo, che richiede di ripetere le prove toccate (D-24, P6). Se ogni giro trova un minore nel perimetro e lo si corregge, il contatore non si chiude mai. È successo con #107, #110, #111 e #114.

---

## 3. Che cosa potrebbe farci fallire

### 3.1 La potenza del metro contro gli obiettivi del titolare (rischio n. 1)

**Calcolo verificabile.**
- Ipotesi: un trade per seduta, risultati indipendenti, dispersione σ = 1,25 R.
- Limite inferiore ≈ media − 1,96·σ/√D; promozione se il limite supera 0,20 R.
- Probabilità di promozione = 1 − Φ((0,20 + 1,96·σ/√D − μ)/(σ/√D)).

| Sedute D | μ = 0,10 | 0,15 | 0,20 | **0,25** | **0,30** | 0,40 |
|---|---|---|---|---|---|---|
| 780 (sviluppo, circa 3 anni) | 0 | 0,1% | 2,5% | 20% | 61% | 99% |
| **1.000 (dominio collaudato)** | 0 | 0,1% | 2,5% | **24%** | **72%** | 100% |
| 2.000 | 0 | 0 | 2,5% | 43% | 95% | 100% |
| 4.000 | 0 | 0 | 2,5% | 72% | 100% | 100% |

- **Controllo di coerenza:** il pilota (Claude, fase 2) ha misurato **71,6%** a μ = 0,30 nella cella gaussiana: coincide con il 72% della formula.
- **Obiettivo del titolare (D-30):** l'1–2% al mese, con lo 0,5% a trade e 15–20 trade al mese, vale **+0,10 / +0,27 R a trade**.
- **Conseguenza:** quasi tutto l'intervallo degli obiettivi sta dove il metro promuove al massimo una volta su quattro, e a +0,20 R quasi mai.
- In più, i criteri di verifica si sommano (DSR, 60% di anni positivi, ultimi 5 anni, drawdown): la potenza complessiva è **più bassa** di questa tabella.

**Aggravante: le strategie «da guadagni alti» hanno più dispersione.** Con target 3R e il 35% di vincenti, σ ≈ 1,9 R. Per l'80% di potenza a 1.000 sedute serve allora μ ≈ 0,20 + 2,8·σ/√1000 ≈ **0,37 R a trade**. Con σ = 1,25 basta circa 0,31 R.

| Voce | Contenuto |
|---|---|
| **Meccanismo** | margine Δ = 0,05 (scelto per contenere le perdite rare, DGS-07/08) e numerosità fissa |
| **Effetto** | per mesi nessuna promozione, anche con idee giuste ma modeste |
| **Evidenza** | formula e pilota (Claude), DGS-08 §3c (ricalcolo del DGS) |
| **Come accorgersene prima** | calcolare la potenza **nella scheda**, prima del sigillo, con σ e frequenza stimate dallo sviluppo |
| **Rimedi** | §4.4 A |
| **Rischio residuo** | dimostrare con dati storici un vantaggio di +0,10–0,20 R a trade è difficile per **qualunque** metodo onesto. È un limite della statistica, non della macchina |
| **Classe** | **difetto dimostrato di adeguatezza** fra disegno e obiettivo; non un errore di calcolo |

### 3.2 Un caso in cui tutti i controlli passano e l'indicazione è sbagliata (rischio n. 3)

- **Assunzione centrale del mio lavoro:** «se la strategia reale somiglia a una delle 12 celle, il metro ne controlla i falsi positivi».
- **Esempio interamente inventato:**
  - vantaggio vero di **+0,15 R** (proprio sul confine IA-02), σ = 1,25 R;
  - perdite rare gravi con frequenza **q = 0,2%**, invece dell'1% della cella 11;
  - 1.000 sedute, il bootstrap del pilota (blocchi da 10, intervallo basic; B = 999 per velocità, dichiarato), Δ = 0,05.
- **Risultato** (script `esempio_avverso.py` nella cartella di lavoro di Claude, 300 repliche):

| Frequenza delle perdite | False promozioni | Repliche senza nessuna perdita |
|---|---|---|
| q = 1% (dentro il collaudo) | **4/300 = 1,3%** | 0/300 |
| **q = 0,2% (fuori dal collaudo)** | **35/300 = 11,7%** (Clopper–Pearson 95% circa 8–16%) | 35/300 |

- Il meccanismo è semplice: quando nel campione la perdita rara **non compare**, la strategia sembra perfetta. Succede con probabilità 0,998^1000 ≈ **13,5%**.
- **Nello sviluppo** (circa 780 sedute) la perdita non compare con probabilità 0,998^780 ≈ **21%**: la diagnostica del dominio vedrebbe «nessuna perdita rara» e la strategia sembrerebbe somigliare alle celle gaussiane.

**Quale controllo lo intercetterebbe:**
- **sulla carta:** DGS-10 §6 («l'assenza di perdite rare nello sviluppo lascia incerta la coda»), che è una bozza non ancora applicata;
- **in pratica:** soltanto una **regola strutturale** nella scheda: stop obbligatorio, perdita massima per trade limitata e dichiarata (per esempio ≤ 3 R anche con salti di prezzo), stress sui salti.

Oggi il modello vigente chiede di gestire lo stop scavalcato in un buco (§4.3), ma **non obbliga** ad avere uno stop né limita la perdita massima.

| Voce | Contenuto |
|---|---|
| **Evidenza** | simulazione di Claude, verificabile in modo indipendente con la formula 0,998^1000 |
| **Rimedio** | clausola obbligatoria nel modello: stop e perdita massima per trade; stress dei salti; domanda esplicita sulle code nella diagnostica |
| **Rischio residuo** | strategie con code sconosciute (eventi mai visti) |
| **Classe** | **rischio dimostrato su un esempio, prova mancante sul reale** |

### 3.3 Registro dei rischi materiali (ordinati per impatto)

| # | Meccanismo | Effetto | Evidenza (chi) | Come accorgersene prima | Rimedi | Rischio residuo | Classe |
|---|---|---|---|---|---|---|---|
| 1 | Metro severo e numerosità fissa (§3.1) | Nessuna promozione utile | Formula e pilota (Claude); DGS-08 | Potenza nella scheda | §4.4 A | Limite statistico | Dimostrato |
| 2 | Macchina incompleta per H-003: D-31 non nel codice (I1); simulatore specifico; registro N non unico (I3) | La prima ipotesi aspetta settimane, oppure viene giudicata con un criterio diverso da D-31 | Codice (Claude) | Elenco chiuso «definizione di fatto» | §4.4 B | Errori nel nuovo codice | Dimostrato |
| 3 | Code fuori dal dominio (§3.2) | Falsa promozione possibile fino all'11% o più | Esempio (Claude) | Clausola sulle code | Stop obbligatorio; stress | Eventi mai visti | Dimostrato sull'esempio |
| 4 | Ciclo di revisioni senza criterio di fine (§2.3) | Lavoro senza avvicinarsi a una prova di utilità | 343 commit, R7–R17, 117 difetti | Contare i giri per «definizione di fatto» | Congelare il perimetro; minori del contorno a lotti; limite di tempo | Qualche difetto residuo dichiarato | Plausibile, con segnali forti |
| 5 | Dati su un solo Mac (batteria guasta) | Settimane perse; custodia della riserva incerta | Diagnosi del 19/11 | Impronte e copie verificate | Seconda custodia con impronte (cloud del titolare o seconda macchina) | Errore umano nelle copie | Dimostrato (guasto) |
| 6 | Indipendenza solo apparente (I5) | Errori comuni a tutte le AI | #112, #106, K15c; DGS-09 §3 | Revisori che **non** leggono la specifica di Claude | Specifica scritta da chi replica; contesti isolati | Un modello può sbagliare come un altro | Plausibile |
| 7 | Pilastri dormienti: formazione, consulto, calibrazione, journal | Il sistema non aiuta a decidere meglio; manca il prodotto per l'uso quotidiano | Cartelle vuote; DA-12 aperta | Una misura d'uso | §4.4 D | — | Dimostrato |
| 8 | Documentazione vecchia (CONTINUITA, STATO, LEGGIMI del Guardian); lavoro non unito a `main` | Ripresa su un contesto sbagliato | Date dei file | Controllo delle date a ogni ripresa | Aggiornare o generare dallo stato | — | Dimostrato |
| 9 | Prezzi Dukascopy diversi da quelli del broker (I6) | Costi sottostimati | Un solo confronto | Confronti a orari diversi | Stress dei costi del +50% (già nel modello) | — | Prova mancante |
| 10 | Testo fondativo assente (DA-02) | Obiettivi interpretati diversamente nel tempo | DA-02 aperta | — | Scrivere un documento fondativo breve, approvato dal titolare | — | Dimostrato |

**Il rischio opposto (sistema troppo prudente o lento) è reale:** coincide con i rischi 1, 2 e 4. Il sistema può essere corretto e inutilizzabile allo stesso tempo.

**Aree rimaste scoperte:**
- il contenuto delle lezioni del Modulo 2 e del manuale (letto solo l'indice);
- il codice di «Binario B», il motore e il DSR (solo intestazioni e collegamenti);
- gran parte dei rapporti di Gemini e dei pacchetti di revisione (a campione);
- i materiali della chat delle strategie (esclusi dal mandato).

Non dichiaro esaustività.

---

## 4. Una strada per dimostrare che il progetto funziona

Tre affermazioni vanno tenute separate, ognuna con le sue prove:
1. **(C) il sistema calcola correttamente**;
2. **(A) il sistema aiuta a prendere decisioni migliori**;
3. **(V) una futura strategia ha un vantaggio economico**.

Oggi abbiamo prove solide **solo di C**, e solo in parte.

### 4.1 Oggi, senza una strategia

| Passaggio | Domanda | Prova | Riferimento | Misura | Successo (soglia proposta) | Arresto | Decisione resa possibile |
|---|---|---|---|---|---|---|---|
| **D1 Prova generale a vuoto** (C) | La catena intera giudica correttamente una strategia con verità nota? | Ipotesi **inventata** con regole meccaniche; mercati sintetici con vantaggio noto (0; 0,15; 0,30 R) e una «riserva» sintetica; catena completa scheda → sigillo → screening → prenotazione → verifica D-31 → rapporto | Verdetti attesi dalla verità nota | Esiti corretti per scenario; tempo e numero di interventi manuali | Vantaggio 0 mai promosso; 0,30 promosso nelle proporzioni della potenza attesa (±10 punti); rapporto con tipo e incertezza su ogni numero; **nessuna modifica al protocollo durante la prova** | Un passaggio della catena non esiste o richiede di cambiare regole | «La macchina è finita» diventa verificabile; si sblocca H-003 |
| **D2 Riconciliazione del G0** (C, poi A) | Le perdite allo stop, le commissioni e i margini calcolati coincidono col broker? | 2–3 micro-operazioni (0,01 lotti) sul **conto demo MT4** già aperto, con stop definito; estratto conto | Estratto del broker | Differenza G0 − broker per voce | Perdita allo stop entro ±2% o ±1 USD; commissione esatta; per lato o in totale chiarito | Differenze non spiegate | Chiude il Gate 1; il G0 diventa usabile per decidere. **Limite:** la demo è MT4 Raw, mentre le specifiche registrate sono del conto MT5 Raw (ROADMAP riga 35): la riconciliazione prova i calcoli del G0, non i costi del conto che si userà |
| **D3 Tracciabilità** (C) | Una conclusione si ricostruisce fino alla fonte? | Già fatta sul collaudo IA-02 (impronte, riproduzione di Gemini) | — | — | **Già soddisfatta** | — | Basta riusarla come modello |
| **D4 Calibrazione del titolare** (A, facoltativa) | Le tue previsioni sono calibrate? | 30 previsioni registrate **prima** dell'esito nel journal (direzione o livello entro un orario, con probabilità) | Base ingenua (50% o frequenza storica) | Punteggio di Brier | Brier < base ingenua con intervallo dichiarato | Previsioni vaghe o registrate dopo | Base per l'Osservatorio e per il consulto |
| **D5 Input mancanti** (C) | Il sistema dichiara «non stimabile» invece di inventare? | Già coperto nel G0 (NON STIMABILE); da estendere ai rapporti del laboratorio (I2) | — | — | Ogni numero del rapporto ha tipo e incertezza | — | Coerenza con il principio 2 |

**Domande impossibili oggi:** se esiste un vantaggio (V); se il G0 o il consulto migliorano le decisioni (A, serve uso reale); quanto costano davvero i trade presso il broker.

### 4.2 Quando esisterà un'ipotesi formalizzata dal titolare

- **Prerequisiti:**
  - D1 superata;
  - D-31 nel perimetro;
  - registro N unico;
  - costi confermati;
  - decisioni su riserva, DA-31, screening e minimi;
  - **potenza calcolata nella scheda** prima del sigillo;
  - clausola sulle code (§3.2).
- **Prova:** una scheda sigillata, eseguita sullo sviluppo con lo screening congelato, poi (se promossa) la diagnostica del dominio e la prenotazione.
- **Che cosa aggiunge:** la prova che la catena regge su dati veri, cioè che C vale anche fuori dal sintetico.
- **Esiti corretti possibili:** promossa, **bocciata**, **non decidibile**. Un «non decidibile» con la potenza dichiarata prima è un **successo dello strumento**, non un fallimento.
- **Misure:** tempo dalla scheda al verdetto (soglia proposta ≤ 2 settimane) e numero di giri di revisione per il simulatore nuovo (≤ 2).
- **Arresto:** se servono cambi di regola dopo i dati, l'ipotesi va riscritta come nuova (N + 1).

### 4.3 Quando sarà autorizzata la demo

| Misura | Come | Confronto | Successo proposto | Che cosa resta spiegabile dal caso |
|---|---|---|---|---|
| Fedeltà d'esecuzione | Primi 20–30 trade confrontati con ciò che il simulatore avrebbe fatto gli stessi giorni (DA-29) | Simulatore | ≥ 90% dei segnali coincidenti; costi entro ±25% | Slittamento e notizie |
| Rispetto delle regole | Violazioni registrate nel journal | Regole personali | 0 violazioni non dichiarate | — |
| Guardian | **Avvisi giusti** (violazioni intercettate) e **avvisi ingiustificati** | Revisione a posteriori di ogni avviso | Falsi avvisi < 10% degli avvisi; nessuna violazione non avvisata | Pochi eventi: intervalli larghi |
| Arresto statistico | Test di Wald (DA-29) | H0 = 0, H1 = +0,10 R | Soglie già simulate | Con +0,10 R servono in media circa 350 trade |
| Utilità per il titolare (A) | Confronto con la procedura manuale, prima e dopo il G0 | Stesse regole, periodi diversi | Meno violazioni a parità di numero di trade | Contesto di mercato diverso, apprendimento: **non** è una prova causale |

### 4.4 Ostacoli prioritari: alternative, costi, prova per scegliere

**A. Potenza contro obiettivi (§3.1).**

| Alternativa | Costo | Compromesso | Prova per scegliere |
|---|---|---|---|
| A1. Tenere D-31 e cercare solo strategie con vantaggio atteso ≥ 0,35 R e potenza calcolata nella scheda | Basso | Meno idee candidabili | Potenza a priori ≥ 50% per l'idea specifica |
| A2. Più sedute per verifica (D = 2.000–4.000), con un collaudo nuovo e preregistrato del dominio | Medio (un nuovo collaudo); consuma più riserva | La riserva basta per meno aperture | Capienza della riserva dopo il consuntivo dei buchi |
| A3. Nuovo protocollo su un dominio ristretto (stop obbligatorio, perdita massima limitata) per recuperare margine (DGS-08 opzione C) | Medio-alto, e può fallire | Vale per meno strategie | Esito di un collaudo nuovo |
| A4. Spostare il peso della prova sulla **demo prospettica** (test di Wald) e usare la riserva come filtro | Tempo: mesi | Prova più lenta ma «pulita» | Frequenza dei trade della strategia |
| A5. Ridurre l'ambizione del Brain: prima strumento di rischio e disciplina (G0, journal, consulto), poi ricerca | Basso | Rinvia la «macchina delle strategie» | Valore d'uso misurato (D2, D4) |

**B. Definizione di fatto della macchina** (contro il ciclo senza fine).
- Elenco chiuso:
  1. D-31 nel perimetro;
  2. registro N unico;
  3. clausola sulle code;
  4. tipi epistemici nei rapporti;
  5. D1 superata;
  6. R17 più il giro sulle manomissioni;
  7. unione in `main` con la protezione del ramo.
- Tutto il resto, compresi i minori negli strumenti di contorno, va **a lotti** e non riapre il contatore.
- Costo: una decisione. Prova: il numero di giri necessari per chiudere l'elenco.

**C. Custodia dei dati.**
- C1: copia verificata con impronta a ogni passo (già avviata).
- C2: una seconda macchina o un archivio permanente del titolare.
- Prova: un ripristino di prova da copia, con `controlla_cache` identico.

**D. Pilastri dormienti.**
- D1: avviare **subito** il journal e D4 (costo: 10 minuti al giorno del titolare).
- D2: riprendere la proposta del consulto come procedura **scritta**, senza codice nuovo.
- D3: rinviare tutto in modo esplicito, con una data di riesame.
- Prova: uso effettivo dopo 4 settimane.

**La prossima dimostrazione utile con le risorse già disponibili:** **D2 (riconciliazione del G0 sulla demo)**, perché costa circa un'ora del titolare e chiude un gate. Subito dopo **D1 (prova generale a vuoto)**, che sblocca H-003 e trasforma «macchina finita» in un fatto verificabile.

---

## 5. Che cosa ho letto

- **Per intero:**
  - `STATO-PROGETTO.md`;
  - `DECISIONI.md` (D-01–D-33);
  - `MODELLO-EPISTEMICO.md`;
  - `guardian/LEGGIMI.md`;
  - `CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL.md` (§0, §3.1, §6–§10);
  - `ROADMAP-20261117.md`;
  - `PROCEDURA-ASSISTENZA-MAC.md`;
  - `MODELLO-SCHEDA-H-003.md` e la bozza;
  - `IMPEGNO-PROTOCOLLO-IA02.md`;
  - DGS-06–DGS-10;
  - `criteri.py` (screening, verifica, rapporti).
- **A campione:**
  - `PROGETTO-GENERALE-20261115.md` (scopo, architettura, gate, prossimi passi);
  - `CONTINUITA.md` (intestazioni);
  - `DECISIONI-APERTE.md` (DA-02, DA-12, DA-19, DA-20, DA-25, DA-26, DA-29);
  - `REGISTRO-CONOSCENZE.md`;
  - indice del manuale v1;
  - intestazioni di `backtester/engine.py` e `dsr.py`;
  - struttura delle cartelle.
- **Fuori:**
  - il testo delle lezioni;
  - `bibliografia`;
  - `audit/01–03` (solo titoli);
  - la maggior parte di `collaborazione/` (235 file);
  - il codice del Guardian;
  - i materiali della chat delle strategie e i dati di mercato (esclusi dal mandato).

---

## Seconda lettura: il mio errore più probabile

- **L'errore più probabile è nel rischio n. 1.**
  - La tabella usa σ = 1,25 R, un trade per seduta, indipendenza e l'approssimazione normale.
  - Con più trade per seduta l'errore standard può scendere; con dipendenza fra sedute sale.
  - **Quindi:** la tabella è una **stima** (tipo IPOTESI, condizioni {σ = 1,25; K = 1; iid}).
  - La conclusione qualitativa regge solo se σ e frequenza reali non sono molto più favorevoli. La coincidenza con il pilota a μ = 0,30 (72% contro 71,6%) la sostiene, ma solo per quella cella.
- **Secondo punto da controllare:** dico che `criteri.verifica` «non implementa D-31». È vero per il codice sigillato attuale. **Potrebbe essere stato inteso** che il criterio D-31 entri con la scheda H-003 come codice nuovo: in quel caso non è un errore del passato, ma un **lavoro mancante** non scritto da nessuna parte. È comunque necessario.

---

## Controverifica richiesta al DGS

| # | Domanda | Conclusione provvisoria | Spiegazione alternativa più forte | Estratto minimo | Calcolo o passaggio verificabile | Decisione che cambia se ho torto |
|---|---|---|---|---|---|---|
| 1 | Il metro D-31 ha potenza adeguata agli obiettivi (+0,10/+0,27 R a trade)? | No: 24% a +0,25 R con 1.000 sedute | Con K > 1 trade per seduta o σ < 1,25 la potenza sale | Tabella §3.1; DGS-08 §3c | 1 − Φ((0,20 + 1,96σ/√D − μ)/(σ/√D)); confronto col 71,6% del pilota | Se la potenza è adeguata, l'alternativa A non serve |
| 2 | Le perdite rare sotto l'1% producono false promozioni fuori controllo? | Sì: 11,7% con q = 0,2% | Strategie reali con stop non hanno perdite di −28 R | §3.2 | P(nessuna perdita in 1.000) = 0,998^1000 ≈ 0,135 | Se no, la clausola sulle code non serve |
| 3 | Senza D-31 nel perimetro, la macchina è «finita»? | No, per qualunque H-003 | Era inteso come codice della scheda | `criteri.verifica`: «R medio netto > 0» | Lettura del criterio citato | Cambia l'elenco della definizione di fatto (§4.4 B) |
| 4 | Tre file di conteggio di N sono un rischio? | Sì, finché DA-28 è aperta | I due di Binario B sono eredità inerte | Nomi e percorsi dei tre file (§2.2 I3) | Verificare quale file legge ciascun modulo | Se sono inerti, basta dichiararli eredità |
| 5 | Il ciclo di revisioni ha bisogno di un criterio di fine? | Sì | Il rigore attuale è proporzionato al rischio della verifica | Contatore e cronologia (R15 non contato, #114 corretto, nuovo candidato) | Contare le correzioni nel perimetro per giro | Se no, si continua così |
| 6 | L'accordo fra tre AI va pesato come prova indipendente? | No, è indipendenza parziale | Fornitori diversi riducono gli errori comuni | #112 trovato dal DGS e non dalla replica; DGS-09 §3 | Elenco dei difetti per chi li ha trovati | Cambia chi scrive la specifica della replica |
