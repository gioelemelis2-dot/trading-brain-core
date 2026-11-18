# Scheda di stato del progetto

**Aggiornata:** notte del 16–17/11/2026 (ultimo aggiornamento: 17/11 mattina, dopo la revisione notturna) · **a cura di:** Claude · **richiesta dal DGS** (DGS-04 §8). Una pagina: dove siamo, i contatori, cosa manca. Si aggiorna a ogni svolta (giro di revisione chiuso, dati completi, decisione del titolare), con la data.

## Dove siamo, in tre frasi
Il banco di prova (simulatore, criteri, sigillo, registri, scaricatore) è **costruito e sotto attacco incrociato**; ogni giro di revisione trova ancora difetti importanti, quindi **non è sigillabile**. **Nessuna strategia è operativa né promossa**: H-002 è parcheggiata con una condizione d'uscita scritta. I dati storici si stanno scaricando; la **riserva di verifica non è mai stata letta dal sistema**, e il censimento («nessuno l'ha vista») è stato **riconfermato il 17/11** con lo strumento di riconteggio corretto.

> **17/11, sera:** R15 di Gemini integrato (#106–#111). I minori #107, #110 e #111 sono corretti in `303890b`, che è il **nuovo candidato per R16**. **R15 non conta come primo giro pulito:** è una lettura stretta di D-24, scelta da Claude su delega e ribaltabile dal titolare. **Contatore: 0 su 2.** Il pilota del collaudo IA-02 nel disegno a 12 celle del DGS è pronto e gira su dati inventati: è sviluppo del metodo, non certificazione. Il mandato R16 è pronto (`collaborazione/da-claude/PROMPT-R16-GEMINI.md`) e si consegna quando lo dice il titolare.

> **17/11, pomeriggio:** i 3 difetti critici trovati la mattina (#86 verifica ripetibile, #87 e #88 codice non sigillato eseguibile) sono **corretti in TDD**, insieme a #89, #91, #93 e a parte di #90 e #94. Gli script di Gemini (BANCO-02) li hanno confermati e poi, rilanciati, respinti; dai loro output è uscito **#95 (critico, errore mio: i controlli giravano dopo gli import)**, corretto con il lanciatore `avvio.py`. Corretto anche #94 d (fuso orario controllato). Restano: #92 (dichiarato: caricatore e riserva proteggono dagli errori, non da chi ha i file) e #94 b (verdetto a due o tre stati: opzioni in DA-31, decide il titolare). Corsa completa dei mutanti in corso. **Il contatore dei giri puliti resta a 0**: ogni giro, anche questo, ha trovato difetti critici.

## Contatori
| Cosa | Stato |
|---|---|
| Difetti registrati | **115** (24 critici, 58 importanti, 33 minori; aggiornato il 18/11: #112–#115; aperto #114, minore nel perimetro, decisione del titolare), #92 dichiarato, #94 b in DA-31, gli altri corretti il 17/11, trovati da Gemini, DGS, revisori esterni, utente e Claude. Tutti corretti e provati, tranne **#42** (difetto della scheda H-002: parcheggiato con lei; regola obbligatoria nel modello H-003) |
| Giri di revisione | Gemini: R7, R8, R11, R12-bis, R13, BANCO-02, R14 (+ repliche); DGS: 01–04; revisori separati di Claude (16 e 17/11: dati e governance, 13 rilievi; laboratorio, in corso); **ogni giro ha trovato difetti importanti** |
| Giri puliti di fila (regola del sigillo) | **1 su 2** (18/11): R16 di Gemini sul candidato `303890b` senza difetti critici o importanti. Da confermare dal titolare: #112 (fuori perimetro) non conta. Serve R17. Contano i rilievi E e M a costo basso (D-24); prima della verifica, un giro su tutte le manomissioni |
| Test automatici | 366 (dati, laboratorio, governance) (dati, laboratorio, governance) + 77 Guardian, verdi su Python 3.13 **e** 3.9, rete bloccata |
| Mutanti negli script | **~370** in 6 script (+21 manuali sull'esportazione redatta), con controllo di validità del mutante (ha scartato un mio mutante con sintassi rotta, Q19, poi riscritto) |
| N (prove selezionabili) | **Nessun sigillo ancora: registro delle prove vuoto.** Censimento delle esecuzioni pre-sigillo (G-20261115-03) **riconfermato il 17/11** con lo strumento corretto: riserva intatta (`governance/censimento/RICONTEGGIO-20261117.md`). Esplorazioni E-001–E-003 contano per le ipotesi che ne usano i tagli. Emendamento su N recepito in DA-19 |
| Riserva di verifica | 2005-01-01 → 31/10/2023, mai letta dal sistema. Meccanismo del registro pronto (`riserva.py`); **α totale, finestre e parte protetta da ratificare** |
| Dati | Sviluppo (15/11/2023 → 12/11/2026) completo, BID e ASK. Storico (17/11 sera): **BID 2005 → 11/11/2023 completo e controllato, ESITO PULITO** (solo conteggi); **ASK in scaricamento, circa 22%** (al 07/02/2009). Date esatte della riserva: si fissano dopo il conteggio dei buchi (DA-26) |
| Impegni anticipati | IA-01 (0,15 R, senza prova di anteriorità) · **IA-02: R medio netto ≥ +0,15 R**, fissato prima di ogni idea H-003 (commit `032250b`) |

## Cosa manca per il primo sigillo, in ordine
1. **Due giri di revisione di fila senza difetti critici o importanti che contano per D-24** (contatore a 0; R14 integrato il 17/11; R15 sul candidato `8e51ce9` non conta (lettura stretta); R16 sul candidato `303890b`).
2. **Dati storici completi**, poi il consuntivo: controllo della cache, confronto BID/ASK, **rendiconto dell'intersezione al minuto e dei buchi** (`laboratorio/studi/intersezione_bid_ask.py`, pronto dal 17/11) e taratura. Le soglie di idoneità restano da decidere: le proposte del DGS sono state ritirate.
3. **Ratifica del registro della riserva** (α totale, scelta delle finestre, parte protetta) — titolare, con il parere del DGS (P2).
4. **Scelta della regola per IA-02** («sulla stima» o «sul limite inferiore», per sviluppo e verifica) — titolare, con il parere del DGS (P1).
5. **Approvazione del modello di scheda H-003** — titolare, con il parere del DGS (P3).
6. **Una scheda H-003 scritta e sigillata prima dei suoi dati** (l'idea è del titolare).

## Cosa serve dall'utente (aggiornato al 17/11 pomeriggio)
- **Già fatto il 17/11:**
  - riconteggio corretto (riserva intatta);
  - pacchetto `dgs06` e messaggio 4 al DGS (DGS-05 ricevuto);
  - scaricamenti BID (dal 12/02/2020) e ASK (dal 2005) ripartiti da `~/Downloads/tb-riconta` con `caffeinate`.
- **Mac acceso e collegato** finché gli scaricamenti non finiscono. Ogni mattina:
  `pgrep -fl scarica_cache; tail -3 ~/scarica_storico.log; tail -3 ~/scarica_ask.log`.
  Se un processo manca, si rilancia lo stesso comando: riparte dal primo giorno mancante.
- **A scaricamento finito:** i comandi del consuntivo (controllo della cache, confronto BID/ASK, intersezione al minuto, taratura), che Claude prepara al momento.
- **Decisioni** (sezione seguente) e rapporti in arrivo: R15 di Gemini, DGS-06.

## Decisioni aperte del titolare
- Dalla risposta 7 al DGS (`collaborazione/da-claude/direttore-sicurezza/7-RISPOSTA-AL-DOSSIER-DGS-05.md`, §5): (1) α totale della riserva; (2) ordine delle finestre, vecchi o recenti prima; (3) DA-31 a tre stati; (4) via al pilota del collaudo, già pronto (`laboratorio/studi/collaudo_ia02.py`); (5) via all'aggiornamento del modello H-003 (bozza `laboratorio/ipotesi/MODELLO-SCHEDA-H-003-BOZZA-P3.md`). Orientamento già espresso: stima nello screening, limite inferiore in verifica.
- DA-31 verdetto a due o tre stati (#94 b) · protezione del ramo su GitHub (#86): da decidere prima della verifica (D-24); su un repository privato richiede GitHub Pro.
- Già decise il 17/11: D-24 modello di minaccia («A con il giro B prima della verifica»).
- Già decise: H-002 parcheggiata con condizione d'uscita scritta; IA-02 = 0,15 R; congelamento post-incidente.

## Rischi aperti, dichiarati
- **Il banco protegge dagli errori, non da chi ha i file (#90, #92):** il registro delle prove e quello della riserva sono file locali; chi ha accesso al Mac può scriverli a mano o leggere la cache con un altro script. La difesa vera è la storia su GitHub (voci spinte prima di ogni passo) letta dai revisori, più la protezione del ramo su GitHub, che spetta al titolare.
- **La memoria umana non si censisce:** chi ha guardato grafici 2005–2023 in passato resta non cieco; il sistema sì.
- **ASK storico:** il 17/11 lo scaricamento ha trovato dati ASK dal gennaio 2005 (121 giorni con dati fino al 01/05/2005). La copertura completa si saprà a scaricamento finito, con `controlla_cache --ask`.
- **Sviluppo contaminato** (incidente del 14/11, #41): per le idee che usano i tagli E-003 lo sviluppo non è un banco pulito.
- **Correlazione fra trade:** misurata da Gemini (R13): gonfia i falsi positivi della regola «sulla stima»; da stimare nella scheda H-003.
