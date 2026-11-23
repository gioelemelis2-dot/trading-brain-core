# Trading Brain — Progetto generale (aggiornato al 23/11/2026)

**Scritto da Claude il 23/11/2026, su richiesta del titolare.** Sostituisce come quadro corrente `PROGETTO-GENERALE-20261115.md`, che resta com'era (nessun documento si cancella).

**Fonti:**
- ramo `feat/esecutore-h002` (non unito a `main`), candidato `67380cd`;
- `governance/DECISIONI.md` (D-01…D-55) e `DECISIONI-APERTE.md`;
- `CONTINUITA.md`, `REGISTRO-MODIFICHE.md` (fino a v2.04), `laboratorio/REGISTRO-DIFETTI.md` (#1…#140);
- `piano/ROADMAP-20261117.md`, `piano/VISIONE-FABBRICA-MULTIMERCATO.md`;
- l'audit globale del 19/11 (`collaborazione/da-claude/AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`) e la revisione critica del 23/11 (`laboratorio/ricevute/2026-11-23-candidato-r19/REVISIONE-CRITICA-20261123.md`).

Ogni stato qui sotto rimanda a un documento del repository. Dove non è verificato lo dico.

---

## In una pagina

- **Che cos'è.** Un ecosistema pluriennale di studio, ricerca quantitativa e controllo del rischio, per arrivare a operare su un conto prop finanziato (FTMO). Le AI propongono, verificano e documentano. Decide il titolare, e nessun denaro reale si muove senza la sua autorizzazione esplicita (D-14).
- **Dove va (D-46, 20/11).** Una **fabbrica di ricerca multi-mercato**: molte strategie semplici, su molti mercati, seguite in parallelo con una prova in avanti simulata sui dati nuovi di ogni giorno. Solo le migliori passano alla demo con ordini veri, e solo dopo alla sfida. L'oro (XAUUSD) è il primo mercato, scelto per cominciare.
- **Dove siamo davvero.**
  - Abbiamo costruito con molto rigore **una parte sola**: la **macchina che giudica una strategia** (dati, sigillo, simulatore, screening, registro della riserva, verdetto statistico, registri). È quasi finita, non ancora certificata.
  - **Nessuna strategia è stata provata sulla riserva**, e oggi non c'è un'ipotesi candidata: la prossima idea spetta al titolare.
  - Guardian e journal sono costruiti ma **mai usati con dati veri**; la formazione è ferma.
- **Il collo di bottiglia non è il codice.** Sono tre cose:
  1. **la potenza statistica:** una strategia vera da +0,25 R a trade viene promossa al più una volta su due, e la riserva basta per **circa 4 verifiche** in tutto;
  2. **il tempo** della prova in avanti;
  3. **le idee:** il metro boccia con onestà, quindi servono molte idee buone.
- **Regola di priorità (D-33, D-52):** prima la macchina, poi le strategie.

---

## 1. Scopo e principi

**Quattro pilastri:**

| Pilastro | Cosa fa | Dove vive | Stato al 23/11 |
|---|---|---|---|
| Conoscenza | Manuale, moduli didattici, glossario, bibliografia | `brain/moduli`, `architettura`, `glossario`, `bibliografia` | Fermo: Modulo 2 in verifica, il resto sospeso (D-10, D-12, D-20) |
| Ricerca | Dati reali, laboratorio, macchina di verifica | `brain/dati`, `brain/laboratorio` | Lavoro principale dal 13/11 |
| Protezione | Guardian G0 consultivo, regole personali, journal | `brain/guardian` | Costruito e collaudato, mai usato: non riconciliato con un conto (DA-25) |
| Governance | Decisioni, standard, registri, continuità | `brain/governance`, `CONTINUITA.md` | Attiva: 55 decisioni, 140 difetti registrati |

**Principi che non cambiano:**
1. Decide il titolare. Le AI propongono, verificano e documentano.
2. Ogni numero ha un tipo: MISURA, DERIVATO, STIMA, IPOTESI o REGOLA (`governance/MODELLO-EPISTEMICO.md`). Dal 20/11 il rapporto del verdetto e quello dello screening stampano il tipo di ogni numero.
3. Nessun dato inventato fuori dai test. I dati sintetici servono solo ai test e sono dichiarati (D-04, D-05).
4. Prima i limiti deterministici, poi le probabilità.
5. Tutto è riproducibile: test automatici, impronte SHA-256, storia git, ricevute con comandi da rilanciare.
6. **La riserva di verifica (2005 → ottobre 2023) non la guarda nessuno.** Si apre una finestra alla volta, solo dal percorso ordinario e solo dopo la prenotazione e l'autorizzazione registrate (D-29, D-50, D-51).
7. Più centri indipendenti: Claude costruisce, Gemini rivede e attacca, il DGS (ChatGPT) controlla il metodo. Nessuno accetta sulla parola i rilievi dell'altro (D-15).
8. Il Guardian avvisa e registra, non blocca (D-16). L'esecuzione automatica senza conferma non è autorizzata (D-45).

**Che cosa non è:** non è consulenza; non è un sistema di trading automatico; non opera con denaro reale senza autorizzazione esplicita, gate per gate.

---

## 2. Obiettivi del titolare, in numeri

| Tema | Decisione | Fonte |
|---|---|---|
| Obiettivo finale | Conto FTMO, solo dopo un vantaggio dimostrato e una lunga incubazione in demo; nessuna data | Progetto 13/11; D-30 |
| Rendimento | «Essere in positivo»: l'1–2% al mese su un conto da 100.000 va benissimo | D-30 |
| Effetto minimo cercato | **+0,25 R a trade**, con potenza del 50% nella verifica. Si candidano solo idee che possono raggiungerlo | D-42, D-36 |
| Weekend | Chiuso, anche nei backtest | D-30 |
| Sfida FTMO | Solo dopo **più** strategie testate | D-30 |
| Rischio | 0,5% a trade (P-01), stop giornaliero 1,5% (P-05), limite totale interno 10% | Regole personali 12–13/11 |
| Esecuzione di una strategia certificata | 1) alert sul telefono e ordine inserito dal titolare; 2) solo se la demo va bene, ordine precompilato da confermare con un tocco; 3) esecuzione automatica **non autorizzata** | D-45 |
| Direzione | Fabbrica di ricerca multi-mercato; lo storico è il primo filtro, il futuro è la prova vera | D-46 |
| Previsioni giornaliere del titolare | No, per ora | D-40 |

---

## 3. Stato al 23/11/2026

| Componente | Stato | Prove | Limite principale |
|---|---|---|---|
| Ramo di lavoro | `feat/esecutore-h002`, **non unito a `main`** (molto indietro) | Storia completa su GitHub | La protezione del ramo (D-49) non si può applicare con il piano GitHub Free (DA-39 aperta) |
| Test automatici | **746** sul candidato `b9ec2f4` (dati, laboratorio, governance, Guardian), verdi su Python 3.13 e 3.9 con la rete bloccata; 12 aggiunti dopo | Log in `laboratorio/ricevute/` | Provano i casi immaginati, non la logica nella sua interezza |
| Mutanti | Perimetro dell'esecuzione 299/299; verdetto 131/132 (VD13 equivalente); percorso di verifica 57/58 su `1431190` (MF09 equivalente), ora 62 mutanti con #139, #140 e PR14. Gli altri script erano al 100% all'ultima corsa completa | Script `mutazioni_*.py`, log nelle ricevute | Sul candidato `67380cd` le corse sono in corso |
| Difetti | **140 registrati** (#1…#140), tutti corretti o dichiarati. Gli ultimi: #139 (due autorizzazioni della stessa domanda) e #140 (ripresa che non riconciliava i registri) | `laboratorio/REGISTRO-DIFETTI.md` | Ogni giro di revisione ha trovato ancora qualcosa |
| Giri di revisione puliti (regola del sigillo, D-24) | **1 su 2** dopo R18 (D-48). **R19 in corso** con Gemini: giro ordinario completo più tutte le manomissioni, ora sul candidato `67380cd` | `collaborazione/da-gemini/`, D-53 | Se R19 trova un difetto importante, il contatore riparte |
| Dati XAUUSD | **Completi**, BID e ASK: riserva dal 2005 all'11/11/2023, sviluppo dal 15/11/2023 al 12/11/2026. Consuntivo: 6.889 giorni allineati, 4.823 sedute, di cui circa 4.400–4.800 ammissibili secondo la soglia di qualità. Nessuna quotazione incrociata | `laboratorio/ricevute/2026-11-22-consuntivo-ask/` | Una sola fonte (Dukascopy); il confronto con MT5 non è fatto |
| Custodia dei dati | Copia finale da 179 MB, SHA-256 `40b401ab…b1f32c`, su iCloud e Google Drive, impronta verificata su entrambe (D-39) | `piano/PROCEDURA-ASSISTENZA-MAC.md` | Il Mac resta l'unica macchina che li usa |
| Riserva di verifica | **Mai letta dal sistema.** Regole di spesa decise: α totale 5%, quota α_j = α/[j(j+1)]/m (D-38). Registro con prenotazione, rifiuto, autorizzazione, esito (schema `riserva/2`, D-50) | `laboratorio/esecuzione/riserva.py` | Mancano: date esatte, embargo, quarantena; il registro vero non è ancora creato |
| Macchina di verifica | Percorso ordinario completo (`esegui_verifica.py`): scheda H-003, prenotazione, quota, screening sullo sviluppo, manifesto dei dati, impegno, autorizzazione, lettura con i byte verificati, verdetto D-31, record, rapporto rigenerabile | `ricevute/2026-11-22-percorso-127/RICEVUTA-127.md`, prove A–G | Provata **solo su dati sintetici**; vedi «Punti deboli» |
| Verdetto statistico (D-31) | Bootstrap circolare a blocchi (ℓ = 10, B = 3.999), margine 0,05 R. Promossa se il limite inferiore supera **+0,20 R**, bocciata se il superiore è sotto **+0,10 R**; decisioni in frazioni esatte (#124) | Collaudo IA-02 su dati sintetici; riprodotto da Gemini | Severo: vedi §6 |
| Ipotesi | **Nessuna candidata.** H-001 chiusa dopo lo Studio 2. H-002 (rottura del range di Londra) parcheggiata; per portarla in verifica servirebbe una scheda H-003 nuova (D-51). Il modello di scheda H-003 è approvato in parte (D-32) | `laboratorio/ipotesi/` | La prossima idea è del titolare |
| Fonte P-001 (idee di un trader esterno) | Dossier e catalogo pilota di 10 video; **in pausa** (D-33, D-52) | `laboratorio/ipotesi/DOSSIER-FONTE-P001.md` | — |
| Guardian G0 e journal | Costruiti, 77 test, mutanti al 100%. **Non utilizzabili per decidere** finché non sono riconciliati con un conto | `brain/guardian` | Il broker del conto demo e la commissione sono da confermare (DA-25) |
| Conoscenza | Modulo 2, lezioni L2.1–L2.6 in verifica; il resto è sospeso | `brain/moduli` | Non c'è un registro dei cancelli superati dal titolare |

---

## 4. Architettura

**La catena di una strategia, oggi:**

1. **Idea** del titolare, o da una fonte esterna registrata con la sua provenienza (D-32).
2. **Scheda H-003** scritta e **sigillata prima di guardare i dati.** Contiene regole, varianti, seme, veto per blocchi, esposizione alle code in R (D-43), ore operative (DA-32) e un contratto leggibile dalla macchina.
3. **Screening sullo sviluppo** (dal 15/11/2023, dati già visti). Passa solo se: media > +0,25 R, limite inferiore > 0 e potenza stimata della verifica ≥ 50% (D-36, D-47). I dati di sviluppo si leggono con i byte verificati contro il registro dello scaricamento.
4. **Prenotazione** di una finestra della riserva (1.000 sedute fissate per calendario, D-37), poi controllo della quota.
5. **Manifesto** dei dati della finestra, costruito dai soli registri, senza aprire i file. Poi l'**impegno**: scheda, codice, finestra, sedute, N, quota, sviluppo. Poi l'**autorizzazione** registrata.
6. **Lettura** della finestra, una volta sola, con i byte verificati file per file. Poi il **verdetto D-31** con il veto per blocchi: promossa, bocciata o non decidibile (D-35).
7. **Record** nel registro della riserva e **rapporto** rigenerabile dal record. Ogni prova si conta in N (registro unico delle prove).
8. Se promossa: **prova in avanti simulata** (D-46), poi **demo** con il Guardian e il journal, con arresto secondo il test di Wald (DA-29).
9. Solo dopo, e con l'autorizzazione esplicita: la **sfida FTMO**.

**Lanciatore:** `avvio.py verifica` legge l'ipotesi dal contratto e controlla il codice sigillato **prima di importare qualunque cosa**. L'esecutore si ferma se è chiamato senza lanciatore. La vecchia verifica di H-002 è disattivata (D-51).

**Neutro rispetto al mercato:** verdetto, registro della riserva, registro delle prove, screening.
**Ancora specifico dell'oro e di Londra:** il simulatore (`orb_londra.py`) e il controllo di qualità nel caricatore. Il **motore generico** che esegue una strategia descritta da regole e parametri è la fase successiva (visione, §2).

---

## 5. Percorso a gate (aggiornato)

| Gate | Stato al 23/11 | Esce quando |
|---|---|---|
| 0 · Verifica del codice di base | ✅ chiuso 12/11 | — |
| 1 · Conto demo e regole personali | 🔄 configurato, **non riconciliato**. 14 regole personali confermate; P-15 in sospeso; broker del conto da 50.000 USD sconosciuto; demo FP Markets MT4 Raw creata; commissione da confermare | Estratto conto riconciliato con la scheda G0 (DA-25) |
| 2 · Dati storici e riserva | 🔄 dati completi e custoditi; consuntivo fatto | Date esatte, embargo e quarantena decisi (D-38); diagnosi del manifesto sui registri veri pulita o risolta; registro vero della riserva creato |
| 2½ · Macchina certificata (D-34) | 🔄 elenco chiuso: (1) D-31 nel codice ✅; (2) registro unico di N ✅; (3) esposizione alle code ✅ nel modello; (4) tipi nei rapporti ✅; (5) prova generale a vuoto ✅; (6) due giri puliti più tutte le manomissioni: **1 su 2, R19 in corso**; (7) unione in `main` con la protezione del ramo: **bloccata dal piano Free** (DA-39) | Punti 6 e 7 chiusi, più i requisiti prima del primo accesso reale (sotto) |
| 3 · Screening sullo sviluppo | ⏳ nessuna ipotesi candidata | Una scheda H-003 sigillata supera lo screening |
| 4 · Verifica sulla riserva (irreversibile) | ⏳ | Verdetto D-31 registrato |
| 5 · Prova in avanti e demo | ⏳ | Almeno 100 trade e 3 mesi; costi ed esecuzione come nel backtest; arresto di Wald |
| — | **Soglia del denaro reale: serve l'autorizzazione esplicita del titolare (D-14)** | — |
| 6 · Sfida FTMO | ⏳ solo dopo più strategie testate (D-30) | Sfida superata senza violare i limiti |
| 7 · Conto finanziato | ⏳ | Si torna al Gate 5 se le metriche peggiorano oltre una soglia decisa prima |

**Requisiti prima del primo accesso reale alla riserva**, oltre al gate 2½. Sono tutti aperti, e in parte sono emersi il 23/11:
1. **D-55:** l'esecutore legge la finestra solo **dopo** che l'autorizzazione è pubblicata su GitHub. Decisa, da scrivere in TDD.
2. **D-54:** il risultato ufficiale lo calcola **un solo ambiente riproducibile**, qualificato con i riferimenti del collaudo IA-02 e registrato nell'impegno. Deciso, da costruire.
3. **Procedura di potenza nel contratto H-003.** Oggi la potenza stimata è un numero **dichiarato** dalla scheda, non calcolato dalla macchina (DGS-17 Q9). Va resa ricalcolabile e controllata prima dell'autorizzazione.
4. **Registri dello scaricamento da completare:** la diagnosi del 23/11 ha trovato righe mancanti (BID fino al 07/06/2009, tutto lo sviluppo) e doppioni identici. Opzioni A1 e B1, da decidere dopo il DGS.
5. **Prova positiva completa dal lanciatore**, con un repository git di prova (chiesta a Gemini in R19).
6. **Prova della storia git con il GitHub vero**, non solo con un remoto finto.

---

## 6. Quanto può dimostrare la macchina (i numeri che contano)

- **Una verifica** usa 1.000 sedute (circa 4 anni) e richiede almeno 300 trade e 200 sedute con trade (D-37).
- **Quante verifiche:** con circa 4.400–4.800 sedute ammissibili, le finestre disgiunte sono **al massimo 4**, prima dell'embargo e delle date accessorie (consuntivo del 22/11). Ogni verifica successiva è più severa: la quota scende da 2,5% a 0,83%, poi 0,42%… (D-38).
- **Potenza** [STIMA, dai calcoli del collaudo e di DGS-14]: per una strategia vera da **+0,25 R** a trade il metro promuove circa:
  - il **25%** delle volte con deviazione per trade di 1,25 R;
  - il **51%** con deviazione 0,8 R.

  Da +0,20 R quasi mai. Quindi la macchina boccia con onestà, ma promuove solo vantaggi forti e regolari.
- **Code** [STIMA, esempio inventato dell'audit del 19/11]: con perdite gravi nello 0,2% dei trade, il metro può promuovere per errore circa **una volta su nove**. Per questo ogni scheda dichiara l'esposizione massima in R (D-43); un collaudo nuovo serve se l'esposizione esce dal dominio provato.
- **Conseguenza pratica.** La riserva è un **primo filtro scarso**, non la prova finale. La prova vera e illimitata è il futuro (D-46), e il suo costo è il **tempo**:
  - circa 5–7 mesi per riconoscere una strategia da +0,30 R;
  - 1,5–2 anni per una da +0,10 R.

  Il parallelismo su molte strategie è ciò che lo rende sostenibile.

---

## 7. Regole permanenti

| Area | Regola | Fonte |
|---|---|---|
| Capitale | Nessuna operazione con denaro reale senza autorizzazione esplicita, data per un gate preciso | D-14 |
| Capitale | Guardian consultivo; esecuzione automatica senza conferma non autorizzata | D-16, D-45 |
| Dati | Sviluppo dal 15/11/2023 (già visto); riserva 2005 → circa 31/10/2023, cieca | D-29 |
| Dati | Grafici XAUUSD e GBPJPY, TradingView compreso, solo dal 15/11/2023 | D-29 |
| Dati | Nessun dato vero nei test, rete bloccata nei test | Prassi, `CONTINUITA.md` |
| Dati | La copia dei dati si copia, non si apre e non si guarda | D-39 |
| Riserva | Spesa con α totale 5% e quota α/[j(j+1)]/m; ogni accesso passa da prenotazione, impegno e autorizzazione registrati; rifiuti durevoli | D-38, D-50 |
| Riserva | Una sola verifica per ipotesi e scheda; la verifica passa solo dal percorso ordinario | #138, #139, D-51 |
| Riserva | Lettura solo dopo l'autorizzazione pubblicata su GitHub; un ambiente di riferimento | D-55, D-54 |
| Ricerca | Ipotesi sigillata prima dei dati; ogni prova contata in N; screening D-36; verdetto solo dal metro D-31 | D-31, D-35…D-37 |
| Ricerca | Prima la macchina, poi le strategie | D-33, D-52 |
| Qualità | TDD: test rossi committati da soli, poi codice, poi mutanti su Python 3.13 e 3.9; equivalenti dichiarati | Prassi |
| Qualità | Sigillo solo dopo due giri di revisione puliti di fila e un giro su tutte le manomissioni | D-24, D-48 |
| Qualità | Ogni difetto va nel registro dei difetti, ogni modifica nel registro delle modifiche; gli errori di Claude si dichiarano | Prassi |
| Collaborazione | Nessuno modifica i materiali dell'altro centro; il DGS non accede al repository e riceve solo pacchetti redatti, senza dati personali | D-11, D-15, D-28 |
| Regole personali | Si cambiano solo a mercato chiuso, per iscritto, con versione | DA-23 |
| Storia | Nessun documento si cancella: si corregge con note datate | README, D-17 |

---

## 8. Ruoli

| Ruolo | Che cosa fa | Non fa |
|---|---|---|
| Titolare | Decide (D-01…D-55), autorizza i gate, esegue i comandi sul Mac (scaricamenti, consuntivi, copie), porta le idee | — |
| Claude (Claude Code, nel cloud) | Costruisce la macchina in TDD, tiene registri e continuità, prepara mandati e messaggi, propone opzioni | Non decide; non accede ai dati veri né al Mac |
| Gemini (sul Mac del titolare) | Giri di revisione indipendenti (R7…R19) con prove e manomissioni su copie; catalogo P-001 | Non tocca dati veri, cache, scaricamenti, impostazioni di GitHub; non modifica il codice del progetto |
| DGS · ChatGPT | Controllo di metodo e statistica (DGS-01…DGS-17); ricalcola i numeri con il proprio strumento | Non accede al repository |
| Altri revisori (DeepSeek) | Revisioni puntuali, in passato | — |

**Ciclo di ogni modifica:**
1. test rossi;
2. codice;
3. suite verdi su 3.13 e 3.9;
4. mutanti;
5. ricevuta con log e impronte, in un worktree bloccato sul commit;
6. registri;
7. revisione di Gemini e del DGS;
8. unione solo con l'autorizzazione del titolare.

---

## 9. Rischi e punti deboli, in ordine di peso

1. **La macchina può non promuovere mai nulla di utile.** Il metro è severo, la riserva basta per circa 4 verifiche, e serve un vantaggio di +0,25 R ben regolare. Contromisura: candidare solo idee forti (D-42) e spostare il peso sulla prova in avanti (D-46). Segnale per cambiare strada: le prime 3–5 ipotesi ben formate escono «non decidibili» per mancanza di potenza.
2. **Lettura della riserva prima che l'autorizzazione sia su GitHub.** Un ripristino locale cancellerebbe la traccia. Decisa la correzione (D-55), da scrivere.
3. **Potenza dichiarata e non calcolata.** Chi scrive la scheda può dichiarare un numero che supera lo screening. È bloccante prima del primo accesso reale.
4. **Protezione del ramo assente** con GitHub Free (DA-39). Oggi la difesa è la storia git, controllata dall'esecutore, più le revisioni.
5. **Registri dello scaricamento incompleti** (diagnosi del 23/11, `laboratorio/ricevute/2026-11-23-diagnosi-manifesto/`). Nessun file è alterato, ma il BID fino al 07/06/2009 e **tutto lo sviluppo** non hanno righe nel registro, e ci sono 236 doppioni identici. Oggi il manifesto blocca, e **lo screening di qualunque scheda si fermerebbe**. Opzioni A1 e B1 al DGS (messaggio 17), poi la decisione del titolare.
6. **Un solo simulatore**, specifico di Londra e dell'oro. Ogni idea nuova oggi richiede codice nuovo e giri di revisione: il costo di un'ipotesi va misurato in settimane.
7. **Il ciclo di revisioni non converge da solo.** Ogni giro trova ancora difetti, gli ultimi due il 23/11. D-34 ha chiuso l'elenco, ma non il flusso dei rilievi.
8. **Una sola fonte di dati** e costi del broker non misurati (DA-25).
9. **Memoria umana:** chi ha guardato i grafici del 2005–2023 in passato non è cieco; il sistema sì.
10. **Pilastri non usati:** Guardian, journal e formazione non aiutano ancora il titolare a decidere.
11. **Volume di Claude.** Molti documenti e test non sono progresso verso un vantaggio. È un rischio dichiarato fin dal 13/11.

---

## 10. Decisioni aperte

| Id | Che cosa | Serve per |
|---|---|---|
| D-38 (parametri) | Date esatte della riserva, embargo (proposta: 10 giorni di borsa), quarantena (proposta: oltre il 5% dei minuti mancanti) | Gate 2 |
| DA-39 | Protezione del ramo con GitHub Free. Consiglio di Claude: restare su Free finché il lavoro è sintetico, poi Pro (circa 4 USD al mese) prima del primo accesso reale | Gate 2½ |
| DA-25 | Broker e riconciliazione del conto demo; commissione | Gate 1 |
| DA-32 | Ore in cui il titolare può eseguire gli alert | Ogni scheda H-003 |
| DA-33 | Dove gira la prova in avanti quotidiana | Fase della fabbrica |
| DA-27, DA-28 | Mercati, ordine, calendario comune; registro unico delle prove su tutti i mercati | Diversificazione |
| P-15, overnight | Perdite consecutive; posizioni overnight (bloccano le idee Q-02, Q-08, Q-10) | Schede future |
| DA-02 | Il testo fondativo (Master Mission) non è mai stato trovato | Metodo |
| Unione in `main` | Mai senza autorizzazione | Gate 2½ |

---

## 11. Prossimi passi, in ordine

1. **Chiudere R19** su `67380cd`: corse di Claude in corso; Gemini riceve l'aggiunta al mandato.
2. **Registri dello scaricamento** (A1 e B1, dopo il DGS e la decisione del titolare). Poi la proposta delle date della riserva, dell'embargo e della quarantena (D-38).
3. **Messaggio 17 al DGS**, con l'archivio degli originali.
4. **D-55 e procedura di potenza** in TDD, poi un giro di revisione dedicato.
5. **D-54:** immagine di riferimento riproducibile e qualificata.
6. **DA-39**, prima del primo accesso reale; poi l'unione in `main`.
7. **Prima idea H-003** del titolare, compatibile con +0,25 R e con le sue ore (DA-32).
8. Dopo: il motore generico, il secondo mercato, la prova in avanti quotidiana (D-46).

**In parallelo, quando c'è tempo del titolare:** riconciliazione del G0 con 2–3 micro-operazioni in demo (DA-25); confronto Dukascopy–MT5 a campione; calendario storico delle notizie (P-08).

---

## 12. Che cosa è superato rispetto al documento del 15/11

- **«IS 70% / OOS 30%» e `commitment.json`:** superati dall'inversione (D-29). La riserva è il periodo 2005–2023, lo sviluppo quello dal 15/11/2023.
- **«Ricerca In-Sample»:** ora si chiama «screening sullo sviluppo» (D-36).
- **«Criterio DA-20»:** sostituito dal verdetto D-31, dai tre esiti D-35, dallo screening D-36 e dai minimi D-37.
- **La tabella «Quanto serve per validare» del 13/11** (Bonferroni, trade necessari) era illustrativa. Il metro in vigore è il bootstrap D-31, con i numeri del §6.
- **Gate 1 «chiuso»:** falso, era già stato smentito il 13/11 (non riconciliato).
- **H-001 e H-002 come prime strategie:** H-001 è chiusa; H-002 è parcheggiata e la sua verifica è disattivata (D-51).
- **Claude Code sul Mac:** non si usa; sul Mac lavorano il titolare e Gemini.
- **«Un mercato alla volta» come unico orizzonte:** resta l'ordine, ma la direzione è la fabbrica multi-mercato (D-46).
