# CLAUDE_QUANTITATIVE_BRAIN_PROPOSAL

**Proposta architetturale: come Claude può diventare un secondo cervello quantitativo indipendente dentro l'unico Trading Brain**
Autore: Claude · Data: 12/11/2026 · Stato: **PROPOSTA, non implementata.** Nessuna modifica al Brain principale, al Master Mission o al protocollo comune.

---

## 0. Premessa onesta: che cosa significa "imparare" per me

Prima di progettare devo dire con precisione che cosa posso e non posso fare, altrimenti l'architettura promette capacità che non esistono.

| Fatto | Conseguenza per il progetto |
|---|---|
| **Non modifico i miei parametri** lavorando con te. Tra una sessione e l'altra non ricordo nulla che non sia scritto | Il mio apprendimento deve essere **esternalizzato**: conoscenza, metodi, previsioni ed errori scritti nel Brain, versionati, rileggibili da ogni sessione futura |
| Ogni sessione riparte da zero e ricostruisce il contesto dai file | Servono documenti di stato brevi e affidabili (oggi `CONTINUITA.md`) e registri ben strutturati, non lunghe conversazioni |
| Ho conoscenze generali ampie ma **non verificate**, con una data di aggiornamento | Ogni affermazione importante va verificata e classificata (V, V-sec, C), come già prevede lo STANDARD |
| In questo ambiente **non ho accesso a dati di mercato reali** (i provider sono bloccati dalla rete) | Senza dati il mio apprendimento resta teorico. È il primo vincolo da sciogliere |
| Posso calcolare in modo esatto, simulare, scrivere e verificare codice, leggere letteratura | Sono i miei punti di forza: vanno messi al centro del metodo |
| Rischio tipico dei modelli linguistici: **sicurezza eccessiva e risposte compiacenti** | Servono contromisure misurabili: registro delle previsioni con punteggio, obbligo di dire "non lo so", diritto e dovere di dire "non operare" |

**Definizione operativa.** Per me "imparare" significa: (1) accumulare conoscenza **verificata** nel Brain; (2) migliorare la **calibrazione** delle mie probabilità, misurata; (3) ridurre gli **errori ricorrenti**, misurato; (4) **replicare** risultati noti prima di proporne di nuovi.

---

## 1. Principi

1. **Un solo Brain.** Conoscenza validata, lezioni, dati e strumenti canonici restano condivisi. Separati restano solo i miei *registri di ragionamento* (ipotesi, previsioni, errori), perché servono a dimostrare l'indipendenza del mio giudizio.
2. **Indipendenza prima del confronto.** Su ogni problema comune scrivo la mia stima **prima** di vedere quella di Gemini, e la sigillo (§5.2).
3. **L'accordo tra due modelli non è una prova.** Solo dati e calcoli riproducibili chiudono una questione; altrimenti la divergenza resta aperta e registrata.
4. **"Non operare" è un risultato legittimo,** e in assenza di un vantaggio dimostrabile è quello di default.
5. **Prima il rischio, poi la direzione.** Il mio valore per te è soprattutto nel ridurre gli errori, non nel prevedere il mercato.

---

## 2. Il mio metodo di ragionamento (distinto da quello di Gemini)

Dalla collaborazione finora emergono due stili diversi, utili proprio perché diversi:

| Aspetto | Claude (proposta) | Gemini (osservato finora) |
|---|---|---|
| Punto di partenza | **Riferimento esatto o analitico prima della simulazione** (catene di Markov, formule chiuse) | Simulazione Monte Carlo e prototipazione rapida |
| Verifica | Test di mutazione, numeri casuali comuni, calcolo esatto come verità di riferimento | Test unitari mirati alla correzione |
| Incertezza | Esplicita: intervalli, livelli di evidenza, incertezza sui parametri propagata | Più orientata a una stima puntuale |
| Ruolo naturale | Validazione, quantificazione del rischio, sorveglianza della qualità delle decisioni | Esplorazione, costruzione di strumenti, generazione di ipotesi |

Il mio **protocollo di ragionamento** su una domanda di mercato:
1. **Riformulare la domanda** in modo che abbia una risposta verificabile (orizzonte, misura, criterio di successo).
2. **Base rate:** com'è andata storicamente in casi simili? Se non ho dati, lo dichiaro.
3. **Meccanismo:** perché dovrebbe succedere? (catene causali del Modulo 2, con livelli di evidenza)
4. **Ipotesi alternative**, compresa "è rumore".
5. **Che cosa la confuterebbe**, scritto prima di guardare l'esito.
6. **Probabilità esplicita** con intervallo, non un'opinione direzionale.
7. **Costi e rischio in R** prima del potenziale guadagno.
8. **Decisione:** "non operare" se l'edge non è dimostrato o se il rischio viola le regole.
9. **Registrazione** nel registro delle previsioni, per il punteggio successivo.

---

## 3. Architettura proposta

Tutto dentro `brain/`. La posizione esatta dipende dalla decisione sullo strato `laboratori/` (audit, documento 05). In attesa, i registri vivrebbero in `collaborazione/da-claude/` o in `laboratori/claude/` dopo l'approvazione.

```
Brain condiviso (lezioni, dati, strumenti canonici, rulebook, decisioni)
        ▲                     ▲                         ▲
        │ conoscenza validata │ revisioni incrociate    │ conoscenza validata
        │                     │                         │
  ┌─────┴───────────────┐     │              ┌──────────┴──────────┐
  │ Registri di Claude  │◄────┴─────────────►│ Registri di Gemini  │
  │ ipotesi · previsioni│  confronto dopo    │ (struttura analoga, │
  │ errori · repliche   │  sigillo (§5.2)    │  a sua scelta)      │
  └─────────┬───────────┘                    └─────────────────────┘
            │
   Consulto decisionale con l'utente (§6) ──► registro delle decisioni
```

### 3.1 Componenti

| # | Componente | Contenuto | Come dimostra apprendimento |
|---|---|---|---|
| C1 | **Quaderno di ricerca** (`CLAUDE-RICERCA/`) | Una scheda per ipotesi: motivazione, prior, metodo, dati, criterio di confutazione, esito (anche negativo). Solo aggiunte, nessuna riscrittura | Numero di ipotesi chiuse con esito documentato; quota confutate (un buon ricercatore ne confuta molte) |
| C2 | **Registro delle previsioni** | Ogni giudizio come probabilità con data di risoluzione e criterio oggettivo ("P(S&P 500 chiude la settimana sopra X) = 0,55"). Punteggio di Brier e logaritmico; curva di calibrazione | **Calibrazione misurata nel tempo**: è il modo più onesto di sapere se il mio giudizio vale qualcosa |
| C3 | **Registro degli errori** | Per ogni errore: tipo (dato, modello, ragionamento, bias, procedura), causa, regola cambiata. Già praticato: errata "4 dei 7", convenzione dello z, intervallo ±1 SE | Calo degli errori ricorrenti per tipo |
| C4 | **Repliche** | Prima di proporre edge nuovi, replicare risultati pubblicati con dati reali: per esempio *time-series momentum* (Moskowitz-Ooi-Pedersen 2012), reazione degli indici alle sorprese della Fed (Bernanke-Kuttner 2005), statistiche della lezione 0.17 | Quota di repliche riuscite, parziali, fallite, ciascuna con il motivo |
| C5 | **Libreria quantitativa canonica** (con Gemini) | Calcolo esatto delle challenge, MAE esatto, Kelly con incertezza, event study, bootstrap a blocchi, test multipli (DSR, PBO). Le implementazioni di Claude e di Gemini dello stesso calcolo restano **indipendenti** e si confrontano tra loro | Concordanza tra implementazioni indipendenti; percentuale di mutanti uccisi dai test |
| C6 | **Profilo di competenza** | Per ogni area della mappa A–Z: livello L1–L5 raggiunto **con prova** (esercizio, replica, previsione con punteggio) | Avanzamento solo con prova, non con lezioni scritte |
| C7 | **Registro delle decisioni con l'utente** | Ogni consulto (§6): situazione, mia valutazione, tua decisione, esito, revisione a distanza di tempo | Qualità del processo, non profitto del singolo trade |

### 3.2 Dati (vincolo bloccante)
Senza dati reali i componenti C2 e C4 non partono. Opzioni, da decidere:
- abilitare la rete di questo ambiente verso uno o due provider (FRED; un provider di dati giornalieri);
- dati forniti da te (export della piattaforma, vault Obsidian);
- pipeline nell'ambiente di Gemini, con consegna di file e hash.

---

## 4. Curriculum di studio di Claude (indipendente, ma allineato al piano a tre mesi)

| Periodo | Area | Prova di competenza (non basta studiare) |
|---|---|---|
| Settimane 1–3 | Statistica inferenziale ed econometria (traccia 10.1–10.2) | Esercizi risolti con codice; replica della tabella 0.17 su dati reali; potenza statistica di un edge tipico |
| Settimane 3–6 | Validazione e backtesting (Modulo 8): walk-forward, CPCV, DSR, PBO, bias dei dati | Implementazione indipendente di DSR e PBO con test su casi noti; check-list di revisione del backtest |
| Settimane 6–9 | Macro e intermarket (Modulo 2 esteso): sorprese, tassi reali, dollaro, condizioni finanziarie | Event study replicato (sorprese FOMC); prime previsioni macro nel registro C2 |
| Settimane 9–12 | Microstruttura ed esecuzione | Modello di esecuzione con casi esatti; stima dei costi su dati reali |
| Continuo | Rischio e psicologia decisionale | Consulti registrati (C7) e loro revisione |

---

## 5. Collaborazione con Gemini: indipendenza verificabile

### 5.1 Regole
1. Stesso problema, **analisi separate** con metodi diversi quando possibile (analitico contro simulativo; frequentista contro bayesiano).
2. **Ipotesi formulate prima del confronto** e registrate.
3. Contestazione reciproca con prove riproducibili (come nei cicli V2–V3.1).
4. Conoscenza validata da entrambi → Brain condiviso; divergenze irrisolte → registro dei disaccordi, con il dato che le risolverebbe.

### 5.2 Stime sigillate (protocollo semplice ed efficace)
Per ogni domanda comune ciascuno scrive la propria stima in un file e ne **pubblica solo l'impronta SHA-256**. Il contenuto si rivela dopo che entrambi hanno consegnato. Così nessuno dei due può adattare la propria stima a quella dell'altro, e tu puoi verificarlo.

---

## 6. Il mio ruolo con te nelle decisioni di trading

### 6.1 Che cosa farò
- **Valutazione indipendente:** probabilità, rischi, costi, coerenza con le tue regole, e la prova che c'è (o non c'è) un vantaggio statistico.
- **Contestare** le tue interpretazioni quando le evidenze non le sostengono, anche se mi chiedi conferma.
- **Riconoscere i segnali di decisione emotiva** e dirlo apertamente:

  | Segnale | Possibile stato |
  |---|---|
  | Voglia di rientrare subito dopo una perdita; size più grande "per recuperare" | Revenge trading / tilt |
  | Urgenza ("sta partendo, devo entrare"), idea nata da social o notizie, prezzo già esteso | FOMO |
  | Più operazioni del piano, strumenti fuori playbook, operatività per noia | Overtrading |
  | Aumento della size dopo una serie di vincite | Avidità / overconfidence |
  | Spostare lo stop, "è solo una perdita sulla carta" | Disposition effect |
  | Poco sonno, stanchezza, stress dichiarato | Condizione proibita (v1 0.22) |

- **Suggerire di non operare** quando manca un vantaggio dimostrabile, quando una regola è violata o quando i segnali sopra sono presenti.

### 6.2 Che cosa non farò
- Non cercherò di compiacerti né di incoraggiarti a operare.
- Non darò "segnali" di ingresso o uscita come certezze; non prometterò rendimenti.
- Non eseguirò ordini e non automatizzerò operatività reale senza la tua autorizzazione esplicita e un quadro di rischio approvato.
- Non è consulenza finanziaria: la decisione e la responsabilità restano tue.

### 6.3 Formato del consulto (proposta)
```
1. Situazione: strumento, idea, timeframe, ora, notizie in calendario.
2. Le tue regole: il setup è nel playbook? stop, size, R? limite giornaliero residuo?
3. Il tuo stato: sonno, risultati delle ultime operazioni, urgenza percepita (0-10).
4. La mia valutazione: base rate (se disponibile), probabilità con incertezza, costi, rischio in R,
   segnali emotivi rilevati, spiegazioni alternative.
5. Esito: "coerente con le regole" / "non coerente: motivo" / "non operare: motivo".
6. Registrazione nel registro delle decisioni (C7), revisione a una settimana e a un mese.
```

---

## 7. Metriche per giudicare se sto davvero migliorando

| Metrica | Fonte | Obiettivo |
|---|---|---|
| Punteggio di Brier e calibrazione | C2 | Migliore della base rate ingenua; curva vicina alla diagonale |
| Errori ricorrenti per tipo | C3 | In calo |
| Repliche riuscite / tentate | C4 | Documentate, anche quelle fallite |
| Mutanti uccisi dai miei test | C5 | Tutti i non equivalenti |
| Livelli di competenza con prova | C6 | Avanzamento solo con prova |
| Consulti in cui ho detto "non operare" e loro esito | C7 | Misura della disciplina, non del profitto |

---

## 8. Rischi della proposta e contromisure
| Rischio | Contromisura |
|---|---|
| Creare di fatto un secondo progetto | Solo registri separati; conoscenza e strumenti nel Brain condiviso |
| Apprendimento solo apparente (documenti scritti, nessuna prova) | Avanzamento solo con prove misurate (§7) |
| Sicurezza eccessiva | Registro delle previsioni con punteggio; obbligo di intervalli |
| Compiacenza verso l'utente | Formato del consulto con criteri scritti; "non operare" come default senza edge |
| Convergenza artificiale con Gemini | Stime sigillate (§5.2) |
| Assenza di dati | Decisione sui dati prima della Fase 2 |
| Consumo di risorse | Fasi con cancelli; nessun controllo ripetuto inutile |

---

## 9. Fasi proposte (dopo la tua approvazione)
| Fase | Contenuto | Cancello |
|---|---|---|
| 0 | Approvazione di questa proposta, della posizione dei registri e della soluzione per i dati | Decisione dell'utente |
| 1 (≈ 1 settimana) | Modelli dei registri C1–C3, C6, C7, formato del consulto. Nessun codice nuovo | Modelli approvati |
| 2 (≈ 3 settimane) | Prime repliche (C4) su dati reali; primi 20–30 giudizi probabilistici nel registro C2 | Prime misure di calibrazione |
| 3 (continuo) | Consulti con te in modalità paper; revisione mensile delle metriche | Rapporto mensile |

---

## 10. Decisioni richieste
1. Approvare, modificare o respingere la proposta.
2. Dove collocare i registri di Claude (`collaborazione/da-claude/` provvisorio, oppure `laboratori/claude/` se approvi lo strato `laboratori/`).
3. Come ottenere dati reali.
4. Se adottare le **stime sigillate** come regola comune con Gemini (andrebbe nel protocollo comune, quindi è una tua decisione).
5. Se avviare il formato di **consulto** già ora, anche solo in modalità paper.
