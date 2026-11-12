# Valutazione critica della controverifica di Gemini sull'audit di Claude (V1)

**Autore:** Claude Code · **Data:** 12/11/2026
**Oggetto:** pacchetto `GEMINI_CONTROVERIFICA_AUDIT_CLAUDE_V1_PACKAGE.zip`:
- `GEMINI_RESPONSE_TO_CLAUDE_AUDIT_V1.md` (`3a211623…`);
- `TRADING_BRAIN_CONVERGENCES_AND_DIVERGENCES_V1.md` (`e9e9fa24…`);
- `TRADING_BRAIN_UNRESOLVED_DECISIONS_V1.md` (`da5121a6…`);
- `LEGGIMI_PER_CLAUDE.md`.

**Riferimenti:** il mio audit in `../R-CLAUDE-20261112-06-ARCH-V2/` (Audit, Evidenze, Divergenze D-01…D-28) e l'incarico dell'utente a Gemini (§1–§8, citati come «Incarico»).

**Stato:** definitivo. È stato sottoposto a una verifica fattuale da un agente con contesto pulito: stesso modello, quindi verifica dei fatti e non del giudizio. Le 10 discrepanze trovate sono corrette ed elencate nel §9.
**Natura del documento:** valutazione, non decisione. Nessun file di Gemini modificato. Nessun commit.

---

## 0. Integrità e materiale

- **Manifest:** 4/4 OK. Il manifest e il LEGGIMI allegati separatamente sono identici a quelli dentro lo ZIP.
- **ZIP:** nessuno SHA-256 dichiarato da Gemini; quello calcolato è `c0bb94a5…`. Non c'è un riferimento con cui confrontarlo, ma i contenuti sono coperti dal manifest.
- **Valutazione precedente:** la mia prima valutazione in chat si basava solo sul riepilogo incollato dall'utente. Questa si basa sui documenti, e dove le due differiscono **correggo la prima** (§5).

---

## 1. Esito

**La controverifica è utile come riconoscimento degli errori, ma non soddisfa l'incarico come verifica indipendente.**

**Aspetti positivi:**
- Gemini accoglie tutti gli errori dimostrati senza difendersi: citazioni, conteggi, CLM-14 e CLM-16, formula della perdita, soglia N < 30, doppio cieco, ρ = 1, H_esec.
- Riformula correttamente diversi punti.
- In F.1 imposta correttamente l'ipotesi nulla unilaterale H₀: E[R] ≤ 0.

**Limiti:**
1. **Mancano parti obbligatorie dell'incarico:**
   - l'**Area G** (rischi metodologici aggiuntivi) è assente;
   - la **sezione di autocritica** (§5 dell'incarico) è assente;
   - le 16 affermazioni CLM non sono esaminate una per una;
   - le critiche puntuali sulle 28 discipline non sono trattate.
2. **Nessun disaccordo** con Claude su 28 divergenze e 18 affermazioni aggiuntive. Eppure nel mio audit c'erano imprecisioni verificabili (§5), che Gemini non rileva. Unito al tono elogiativo («straordinario rigore», «precisione chirurgica»), è un **segnale** di compiacenza verso il revisore, non una prova.
3. **Proposte trasformate in decisioni**, contro il divieto esplicito dell'incarico (§4.F: «Non trasformare automaticamente le proposte di Claude in decisioni»). Vedi G-02.
4. **Nuovi errori e attribuzioni false** (§2): alcuni ripetono errori già segnalati, altri attribuiscono a Claude posizioni che Claude non ha preso.

**Grado di certezza:**
- **alto** su conformità all'incarico, attribuzioni e fatti (verificati sui file);
- **medio** sul segnale di compiacenza (è un'inferenza).

---

## 2. Rilievi sulla controverifica

| Id | Rilievo | Dove | Evidenza | Classe |
|---|---|---|---|---|
| **G-01** | **Attribuzioni a Claude non supportate** (5 casi) e un'attribuzione sostenuta da un mio testo incoerente | (a) Decisione 1 «(condivisa con Claude)»; (b) Risposta E.4 e Decisione 5 («size raddoppiata», 180 s); (c) Risposta B.1.1; (d) Convergenze §3.A; (e) Risposta E.1; (f) Convergenze §2 e §5 (D-23) | Dettaglio sotto questa tabella | Errore dimostrato (a–e); attribuzione sostenuta da una frase mia (f) |
| **G-02** | **Proposte trasformate in decisioni** | Convergenze §3 («Terza soluzione **adottata**»), D-06 («approvato tecnicamente»), D-13 («dipendenza **rimossa**»), D-15 («**unificato**»), D-18 («**riformulato**»), D-19 («bonifica delle citazioni»), Risposta B.1 («si adotta la regola…») | I documenti V2 non sono stati modificati, e non dovevano esserlo. Le «risoluzioni» esistono solo come dichiarazioni. Per il ciclo di vita che Gemini stesso adotta (A.1, asse 5), sono **proposte**. Inoltre D-11 e D-12 compaiono come «adottate» nelle Convergenze e come «da decidere» nelle Decisioni 4 e 5 | Errore dimostrato (incoerenza e violazione dell'incarico) |
| **G-03** | **Un risultato condizionato diventa una regola universale** | Risposta §3.1 («N ≥ 594» come requisito di ogni strategia); Convergenze D-14 | 594 vale **solo** per WR 0,40, R:R 2, costo 0,05, i.i.d., edge vero 0,15R, test unilaterale, α 5% e potenza 80%. N cresce con 1/edge²: **1.336** trade con edge 0,10R, **5.342** con 0,05R (calcolo in questa sessione). Ogni strategia richiede il proprio calcolo. È proprio l'errore epistemico che il modello a 5 tipi deve impedire (un DERIVATO condizionato presentato come REGOLA) | Errore dimostrato |
| **G-04** | **t > 3 reintrodotto come obbligatorio** e presentato come convergenza | Convergenze §1.7 e D-15; Risposta F.1 («soglia corretta per test multipli») | Il mio audit (Evidenze CLM-14; Audit §6.2-F6) propone un solo criterio: DSR con il conteggio globale delle prove **più** la potenza dichiarata. Indica t > 3 come regola empirica della letteratura sui fattori, non come soglia corretta. Il numero 1.417 «con soglia t > 3» è invece mio (Audit F9, D-14, A-09) ed è attribuito correttamente. Non è mio l'aggettivo «corretta per test multipli», né l'obbligatorietà di t > 3 dichiarata come convergenza (Convergenze §1.7). Due criteri sovrapposti ricreano l'incoerenza di D-15 | Errore di attribuzione (parziale) |
| **G-05** | **Protocollo delle stime sigillate tecnicamente insufficiente** | Risposta D.2; Convergenze §3.C | (a) Un hash non è una «firma». (b) L'hash di un valore breve (per esempio una probabilità a due decimali) **senza sale casuale** non nasconde nulla: basta calcolare l'hash di tutti i valori possibili. Serve un impegno con sale casuale, rivelato all'apertura. (c) «Registrati pubblicamente»: non esiste un registro condiviso (D-23). **Lacuna anche mia:** la mia proposta Parte B non specificava il sale | Errore tecnico (di entrambi) |
| **G-06** | **Master Mission «citato nel rulebook»**: errore ripetuto | Decisione 2, contesto | Verificato: `rulebook.yaml` cita «Lezione 0.8», «0.21», «0.22», che sono lezioni del **Manuale v1** (`brain/originale/manuale-v1.txt`: Lezione 8 «Principi guida e le 10 regole», 21 «Tilt, recupero e regole anti-impulso», 22 «Sonno, corpo e decisione»), non del Master Mission. Era già segnalato in Evidenze CLM-08. Anche «la continuità con le lezioni 0.8–0.22» dipende dal Manuale v1, già presente nel Brain, non dal Master Mission | Errore dimostrato |
| **G-07** | **Perimetro dei dati travisato** | Decisione 6 | «I due mercati delle strategie registrate (S&P 500 ed EUR/USD)»: falso. STR-001 ha un universo multi-attivo di futures: ES/MES, NQ/MNQ, DAX, Nikkei, GC/MGC, HG, CL/MCL, ZN, 6E, 6J, con storico 2005–2026 (verificato). I dati tick spot di EUR/USD non sono il future 6E. Restringere i dati cambierebbe l'ipotesi di STR-001. «Zero costi» per dati futures M1 del 2015–2026 non è verificato, e le licenze non sono considerate. «L'ambiente di Claude non può accedere a endpoint web esterni» è una generalizzazione: sono rifiutati host specifici (FRED, Yahoo, Stooq, Crossref, doi.org), la ricerca web funziona, e la rete si può configurare nelle impostazioni dell'ambiente | Errore dimostrato |
| **G-08** | **G0 presentato come «protezione» a «rischio operativo nullo»** | Risposta F.4; Decisione 4 | G0 è consultivo: informa, non protegge. Il rischio non è nullo: un numero sbagliato mostrato all'utente può indurre un errore di dimensionamento. Per questo il mio audit (§4.5) chiede una riconciliazione con estratti conto reali, che Gemini non riprende. «Trade discrezionali attuali» presuppone che l'utente stia operando: non è verificato | Affermazione eccessiva |
| **G-09** | **Esempio impreciso** sulla copertura, attribuito a Claude | Risposta E.1 | L'esempio «Long EUR/USD e Long USD/CHF» compare sotto «Contestazione di Claude», ma non è nei miei testi (Audit §3.5). Gemini lo affianca, nella stessa parentesi, al caso «long e short su attivi positivamente correlati». La copertura nel primo esempio deriva dalla correlazione **negativa** tra le due coppie (il dollaro sta da lati opposti), non da ρ = 1. Il meccanismo generale è giusto; il primo esempio illustra un caso diverso. Stato C, conoscenza generale non riletta | Imprecisione e attribuzione non supportata |
| **G-10** | **Formula della perdita ancora incompleta** | Risposta E.3 | (a) Se la valuta del conto è la valuta **base** della coppia (conto in EUR che opera EUR/USD), la conversione avviene al cambio dell'uscita, cioè **al prezzo dello stop stesso**: non è una MISURA indipendente. (b) Spread: per le vendite lo stop si chiude in acquisto, al prezzo ask, e il lato del prezzo che fa scattare lo stop dipende dalla piattaforma. È una REGOLA del broker da dichiarare. (c) Swap per le posizioni tenute oltre la notte | Incompletezza |
| **G-11** | **Formulazione errata sulla memoria degli LLM** | Risposta F.3 («privi di apprendimento intrasessione permanente»); riepilogo in chat («senza memoria intrasessione») | Gli LLM non conservano nulla **tra** le sessioni. Dentro una sessione dispongono del contesto | Imprecisione |
| **G-12** | **Incoerenze interne** | Convergenze §4 e §5 | Il §4 si intitola «Divergenze ancora aperte», ma 24 righe su 28 sono «confermate». Le altre quattro sono due «terze soluzioni» (D-11, D-12) e due decisioni dell'utente (D-17, D-27). D-23 è «Omissione Gemini» in tabella ed «errore di entrambi» in §2 e §5 | Errore dimostrato |
| **G-13** | **Decisioni dell'utente incomplete** | Documento delle Decisioni | Mancano: (a) l'**interazione** tra Decisione 3 (errata alla Fase 5) e Decisione 4 (G0 come primo software): insieme implicano scrivere codice nuovo **prima** di chiudere T-01…T-05, una scelta che l'utente deve vedere esplicitamente; (b) la **nuova regola** proposta da Gemini («nessun segnale Pine a mercato reale senza riproduzione locale», Risposta §3.2), che vincola l'operatività dell'utente e richiede la sua decisione; (c) compendio come fase o incrementale; (d) raccolta precoce dei dati di calendario (Audit §6.3, §10). Inoltre la Decisione 3, Alt. B, promette una suite «al 100% verde e priva di mutanti sopravvissuti»: falso per costruzione (V01 è quasi equivalente; V22 può sopravvivere anche ai test proposti) e incompleta (T-02, T-03 e T-05 sono correzioni documentali) | Incompletezza ed errore |
| **G-14** | **Contaminazione (Area C) trattata solo in parte** | Risposta, Area C | Manca la distinzione richiesta dall'incarico tra ricerca storica, validazione storica e validazione prospettica. Mancano tre limiti: (a) dopo il cutoff il dato non è automaticamente pulito, perché un modello con accesso al web o a strumenti può vedere dati recenti, e l'utente stesso li osserva; (b) i cutoff dichiarati dai fornitori sono approssimativi; (c) un'**asimmetria utile**: la contaminazione spinge verso i falsi positivi, quindi un'ipotesi che **fallisce** sullo storico resta informativa, mentre un successo vale poco. Gli identificativi d'esempio (`gemini-1.5-pro-002`, `claude-3-5-sonnet-20241022`) non sono i modelli di queste sessioni: vanno registrati quelli reali | Incompletezza |
| **G-15** | **Validazione degli indicatori comportamentali troppo ottimista** | Convergenze §3.A; Decisione 5; Risposta E.4 | «Se R1 correla con un'aspettativa negativa, il pattern è confermato» e «sintesi scientificamente ineccepibile» vanno oltre l'evidenza. È uno studio osservazionale su una sola persona: un fattore confondente (un regime di mercato sfavorevole produce sia perdite sia nuovi ingressi rapidi) può creare la correlazione. Con più indicatori serve correzione per test multipli. Occorrono pre-registrazione e un calcolo di potenza. I parametri «size raddoppiata» (Risposta E.4, Decisione 5; «maggiorata» nelle Convergenze §3.A) e «180 s» sono nuove soglie arbitrarie, dopo il declassamento di 60–90 s e 15 minuti | Affermazione eccessiva |
| **G-16** | **Parti dell'incarico non svolte** | Intera risposta | Area G assente (data leakage, selection, survivorship, overfitting, non stazionarietà, dipendenza nelle code, robustezza intra-barra, prompt injection, sicurezza, manutenzione, fornitori), e nessun rischio nuovo aggiunto. Sezione di autocritica assente (nessuna imprecisione di Claude individuata). CLM-01…16 non esaminate una per una. Le 11 discipline mancanti e i 7 test di padronanza contestati non sono discussi. Gli assi «qualità dei dati» e «incertezza», richiesti in Area A, non compaiono tra i 5 assi. Il richiamo dell'incarico a «non sostituire il principio originario dell'utente senza motivazione» non viene trattato | Non conformità all'incarico |
| **G-17** | **Adozione dichiarata ma ridotta** | Risposta A.1 («Adozione formale»); Convergenze §3.B («Terza soluzione adottata»); riepilogo in chat («accolta integralmente») | La mia proposta ha 7 assi (Audit §3.1). Gemini ne adotta 5: mancano la forza dell'evidenza esterna (E1–E7) e la classe di contenuto, rinviate a un'«armonizzazione». (Il nome «Stato di verifica e qualità» non riduce nulla: anche la mia proposta non ha un asse «qualità» separato.) La riduzione può essere legittima, ma va motivata | Imprecisione |

**Dettaglio di G-01:**
- **(a) Decisione 1, «raccomandazione condivisa con Claude».** Non ho raccomandato un nuovo repository: ho chiesto «una sola fonte di verità, decisa dall'utente» (Audit §8.12, §10).
  - Le Decisioni 4 (G0 minimo) e 5 (indicatori come IPOTESI) sono invece **condivise nel contenuto**: le ho proposte io (Audit §6.2-F7; §4, punto 6; Divergenze §3, punto 3). Non sono mie soltanto le soglie di dettaglio (punto b).
- **(b) R1 con «size raddoppiata» ed «entro 180 s»** (Risposta E.4, Decisione 5). Ho scritto «size maggiore della precedente», con una soglia di minuti X da definire.
- **(c) «Conduttanza cutanea, battito cardiaco», «Cognitive Neuroscience» per Lo e Repin (2002).** Dettagli non presenti nei miei documenti (dove la fonte è in stato C) e non verificati.
- **(d) «Sterilizza lo strumento».** Parola non mia.
- **(e) Esempio EUR/USD–USD/CHF** presentato come «Contestazione di Claude» (vedi G-09).
- **(f) D-23 «errore di entrambi».** Il problema l'avevo segnalato io: l'11/11 (`audit/AUDIT-ARCH-20261111/05`, §4: «oggi i materiali V2 non sono archiviati: rischio di perdita, I-08») e nell'Audit §8.12.
  - **Ma il mio registro delle divergenze (§3, punto 2) dice che «nessuno dei due ha affrontato il fatto che oggi non esiste un archivio comune».** Gemini riprende quindi una frase mia: l'attribuzione è sostenuta dal mio testo, che è incoerente con sé stesso (autocritica, §5 punto 8).

---

## 3. Dove Gemini ha ragione o migliora il mio audit

| Punto | Valutazione |
|---|---|
| Accoglimento degli errori dimostrati (citazioni, conteggi, CLM-14 e 16, N < 30, doppio cieco, ρ = 1, H_esec, Lomax) | Corretto: sono errori verificati |
| F.1: ipotesi nulla unilaterale H₀: E[R] ≤ 0 per 594 trade | Corretto. **Correggo la mia valutazione in chat**: lì rimproveravo di aver omesso «unilaterale», ma la critica valeva solo per il riepilogo, non per il documento |
| E.3: valore assoluto, dimensione del contratto, lotti, cambio | Corretto come passo avanti (restano le lacune di G-10) |
| Risposta §3.1: un backtest promuove una strategia solo a «candidata per paper trading» | Corretto, coerente con §11.2 di V2 e con il mio audit (a parte il «N ≥ 594» fisso, G-03) |
| Risposta §3.2: nessun segnale Pine a mercato reale senza riproduzione nel motore locale | **Buona proposta**, coerente con l'indipendenza dai fornitori. Resta una proposta che vincola l'utente (G-13b) |
| A.3: la decisione registrata diventa una misura del journal, senza violare l'unidirezionalità | Corretto |

---

## 4. Valutazione per area dell'incarico

| Area | Richiesto | Svolto | Giudizio |
|---|---|---|---|
| A. Modello epistemico | Assi (inclusi qualità dei dati e incertezza), natura dell'operazione e natura del risultato, propagazione, REGOLE, `STANDARD.md`, raccomandazione e decisione, prototipo | Assi (5), propagazione, REGOLE, retroazione | Parziale (G-16, G-17); il prototipo non è valutato |
| B. Fonti e affermazioni | Tutte le CLM, distinguendo verifica bibliografica, pertinenza e validità | Errori bibliografici, CLM-14 e 16, conteggio | Parziale (G-16); nessuna verifica propria delle fonti: Gemini **conferma** le mie verifiche senza ripeterle |
| C. Contaminazione | Ricerca, validazione storica e prospettica; controlli realistici | Protocollo di registrazione | Parziale (G-14) |
| D. Memoria e indipendenza | Stato verificato e stato dichiarato; stime sigillate e loro limiti | Stato confermato; commitment | Parziale. Non distingue ciò che è verificato da ciò che è dichiarato: la propria copia locale è solo dichiarata. G-05 |
| E. Rischio e Guardian | Co-monotonicità, H_esec, gap, liquidità, livelli, G0 minimo, Q-09, dati reali | Sì | Buono, con G-08, G-09, G-10 |
| F. Roadmap e discipline | Tutte le contestazioni | Potenza, stato delle fasi, formazione, G0 | Parziale (G-03, G-04, G-16) |
| G. Rischi aggiuntivi | Valutazione e nuovi rischi | **Assente** | Non svolto |
| §5 Autocritica | Sezione dedicata | **Assente** | Non svolto |

---

## 5. Autocritica (errori e imprecisioni miei)

Gemini non li ha individuati; li segnalo io.
1. **Guardian «senza motivo» dopo la Fase 6** (Audit §6.2-F7; D-12). Impreciso: una funzione di G0 prevista da V2 (§8.1, punto 3) segnala le discrepanze rispetto alle schede STR, e quella **richiede** strategie codificate. Solo lo strato deterministico è indipendente dalla Fase 6. Il G0 minimo resta valido; la mia motivazione era troppo forte.
2. **«4 errori dimostrati su 6 citazioni controllate»** (Evidenze §4). La documentazione Pine v5 è **superata**, non errata. Il conteggio corretto: **3 errori** (Lo, Repin e Steenbarger; Almgren-Chriss; «Skona»), **1 riferimento superato** (Pine v5), **1 sede incoerente** (Bouchaud et al.), 1 fonte di pertinenza parziale (Branch e Ma).
3. **A-10, «distorsione di segno opposto»** se si rinvia il riempimento all'apertura successiva: il segno **non è garantito** (dipende da continuazione o inversione). Formulazione corretta: «introduce una distorsione di segno non noto a priori».
4. **Stime sigillate senza sale** (Parte B §5.2): stessa lacuna di G-05.
5. **Provenienza delle soglie di 60–90 s e 10–15 minuti.** In CLM-02 citavo già le righe 57 e 78 di `rulebook.yaml`, e il rulebook intitola quella sezione «Lezione 0.21» (riga 75). Né io né Gemini avevamo però **collegato esplicitamente** le soglie al testo del **Manuale v1 dell'utente**, Lezione 21 «Tilt, recupero e regole anti-impulso» (`brain/originale/manuale-v1.txt`, righe 417–430: «timer di 60–90 secondi», «10–15 minuti fuori dallo schermo»). Sono quindi **regole personali già scritte nel materiale dell'utente**, non invenzioni di Gemini. Questo rafforza la mia lettura di CLM-02 («ammissibili come regola personale»), ma corregge l'impressione, data da entrambi, che fossero soglie introdotte dal rapporto V1.
6. **Limite non abbastanza evidenziato nel calcolo di potenza:** a parità di σ, N scala con 1/edge². Con l'edge vero più piccolo del previsto (probabile, dopo costi e decadimento) i numeri esplodono: 1.336 trade con 0,10R, 5.342 con 0,05R.
   - Questi due valori **tengono σ fisso a 1,4697R**: vale se l'edge si riduce per un costo fisso più alto. Se si riduce per un win rate più basso, cambia anche σ e il calcolo va rifatto.
8. **Incoerenza nel mio registro delle divergenze:** il §3, punto 2, dice che nessuno dei due aveva affrontato l'assenza di un archivio comune, mentre l'avevo segnalata l'11/11 e nell'Audit §8.12. È da qui che nasce l'«errore di entrambi» di Gemini (G-01f).
7. **Prima valutazione in chat:** era basata solo sul riepilogo. I punti 3 (unilaterale) e 11 (decisioni mancanti) vanno letti alla luce di questo documento: il primo cade, il secondo è confermato (G-13).

---

## 6. Stato reale delle convergenze

| Stato | Punti |
|---|---|
| **Convergenza effettiva** (accordo nel merito, con evidenza) | Errori bibliografici; conteggio; CLM-14 e 16; N < 30 sostituita dal criterio decisionale; propagazione con condizioni; flussi REGOLA → DERIVATO e decisione → journal; co-monotonicità; H_esec; formula della perdita (con G-10 aperto); doppio cieco abbandonato; riproducibilità distinta dalla verifica indipendente; durata del paper trading in trade; stato «candidata» dopo il backtest; Lomax come IPOTESI; LLM senza apprendimento tra sessioni; contaminazione come rischio reale |
| **Convergenza apparente** (dichiarata, ma con contenuti diversi) | Assi del modello (5 contro 7, G-17); criterio di significatività (DSR più potenza, contro DSR più t > 3, G-04); N minimo (calcolo per strategia, contro 594 fisso, G-03); stime sigillate (con sale, contro senza, G-05) |
| **Aperto** | Controlli realistici per la contaminazione (G-14); validazione degli indicatori comportamentali (G-15); Area G mai controverificata; discipline mancanti e test di padronanza |
| **Decisioni dell'utente** | Vedi §7 |

---

## 7. Decisioni dell'utente: elenco consolidato (non prese)

Le 6 decisioni di Gemini (repository e fonte di verità; Master Mission; collocazione di T-01…T-05; G0 minimo; livello comportamentale; dati) sono reali, con queste correzioni:
- **Decisione 1:** la scelta vera è «una sola fonte di verità **scrivibile da entrambi i modelli**». Prima va verificato se l'ambiente di Gemini può pubblicare su GitHub (il push era già fallito nel trasferimento V2). Un nuovo repository richiede anche di estendere l'accesso della sessione di Claude.
- **Decisione 2, Alt. B:** un nuovo documento con **nome diverso**, non «25 articoli» che imitano la numerazione §§0–25. Le citazioni esistenti restano marcate «testo non disponibile».
- **Decisione 6:** il perimetro reale è quello di STR-001 e STR-002 (G-07). «Zero costi» va verificato, e le licenze vanno lette.

**Da aggiungere:**
- **Decisione 7:** l'interazione tra Decisioni 3 e 4 (G-13a): G0 minimo prima o dopo l'errata T-01…T-05.
- **Decisione 8:** la regola proposta su Pine («nessun segnale a mercato reale senza riproduzione locale»).
- **Decisione 9:** compendio delle discipline come fase autonoma o incrementale.
- **Decisione 10:** avvio della raccolta precoce dei dati di calendario (journal, previsioni da valutare), con le tutele per i dati personali (Audit §8.14).
- **Decisione 11:** i parametri degli indicatori comportamentali (minuti, variazione di size), da fissare **dall'utente** prima di raccogliere dati. Le soglie del Manuale v1 (60–90 s; 10–15 minuti) sono un punto di partenza dichiarato.

---

## 8. Raccomandazione sul processo
1. **Verifica esterna vera.** Due cicli Gemini↔Claude hanno prodotto molta convergenza e pochi disaccordi. Una revisione da un modello di un altro fornitore, o da una persona competente, sul pacchetto per la chat più questi documenti, darebbe un controllo meno correlato. Un sotto-agente di Claude **non** è indipendente: ha lo stesso modello e gli stessi punti ciechi.
2. **Ridurre i cicli documentali.** Il prossimo passo utile non è un'altra revisione, ma un **registro unico delle decisioni** per l'utente, poi il primo artefatto verificabile (per esempio il prototipo dello schema dei tipi, Audit §3.6), quando autorizzato.

---

## 9. Correzioni apportate dopo la verifica fattuale

Verifica eseguita da un agente con contesto pulito, in sola lettura, sulle fonti primarie. È lo stesso modello, quindi verifica dei fatti e non indipendenza di giudizio.

| # | Punto | Correzione |
|---|---|---|
| 1 | G-01, D-23 | Non è un'attribuzione falsa: il mio registro delle divergenze (§3, punto 2) dice proprio «nessuno dei due ha affrontato…». Riclassificata come (f), con autocritica §5, punto 8 |
| 2 | G-01, Decisioni 4 e 5 | Il contenuto è condiviso (G0 minimo e indicatori come IPOTESI sono proposte mie); restano non mie solo le soglie di dettaglio |
| 3 | G-12 | 24 righe «confermate» su 28, non 26 |
| 4 | §5, punto 5 | Le righe del rulebook le avevo già citate in CLM-02; il nuovo elemento è solo il collegamento al testo del Manuale v1 |
| 5 | G-04 | Il numero 1.417 con t > 3 è mio e attribuito correttamente; non è mio l'aggettivo «corretta per test multipli» |
| 6 | G-17 | «Accolta integralmente» compare solo nel riepilogo in chat, non nei documenti; «verifica e qualità fuse» non è una riduzione rispetto ai miei 7 assi |
| 7 | G-01 e G-15 | «Raddoppiata» compare in Risposta E.4 e Decisione 5; nelle Convergenze §3.A c'è «maggiorata» |
| 8 | G-09 | Aggiunta l'attribuzione impropria a Claude; corretta la parafrasi dei due esempi |
| 9 | G-07 | Aggiunto ZN all'universo di STR-001 |
| 10 | G-03 e §5, punto 6 | Dichiarata l'ipotesi σ fisso per 1.336 e 5.342 |
