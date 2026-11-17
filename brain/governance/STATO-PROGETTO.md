# Scheda di stato del progetto

**Aggiornata:** notte del 16–17/11/2026 (ultimo aggiornamento: 17/11 mattina, dopo la revisione notturna) · **a cura di:** Claude · **richiesta dal DGS** (DGS-04 §8). Una pagina: dove siamo, i contatori, cosa manca. Si aggiorna a ogni svolta (giro di revisione chiuso, dati completi, decisione del titolare), con la data.

## Dove siamo, in tre frasi
Il banco di prova (simulatore, criteri, sigillo, registri, scaricatore) è **costruito e sotto attacco incrociato**; ogni giro di revisione trova ancora difetti importanti, quindi **non è sigillabile**. **Nessuna strategia è operativa né promossa**: H-002 è parcheggiata con una condizione d'uscita scritta. I dati storici si stanno scaricando; la **riserva di verifica non è mai stata letta dal sistema**, e il censimento («nessuno l'ha vista») è stato **riconfermato il 17/11** con lo strumento di riconteggio corretto.

> **17/11, pomeriggio:** i 3 difetti critici trovati la mattina (#86 verifica ripetibile, #87 e #88 codice non sigillato eseguibile) sono **corretti in TDD**, insieme a #89, #91, #93 e a parte di #90 e #94. Gli script di Gemini (BANCO-02) li hanno confermati e poi, rilanciati, respinti; dai loro output è uscito **#95 (critico, errore mio: i controlli giravano dopo gli import)**, corretto con il lanciatore `avvio.py`. Corretto anche #94 d (fuso orario controllato). Restano: #92 (dichiarato: caricatore e riserva proteggono dagli errori, non da chi ha i file) e #94 b (verdetto a due o tre stati: opzioni in DA-31, decide il titolare). Corsa completa dei mutanti in corso. **Il contatore dei giri puliti resta a 0**: ogni giro, anche questo, ha trovato difetti critici.

## Contatori
| Cosa | Stato |
|---|---|
| Difetti registrati | **95** (23 critici, 51 importanti, 21 minori; conteggio del 17/11), #92 dichiarato, #94 b in DA-31, gli altri corretti il 17/11, trovati da Gemini, DGS, revisori esterni, utente e Claude. Tutti corretti e provati, tranne **#42** (difetto della scheda H-002: parcheggiato con lei; regola obbligatoria nel modello H-003) |
| Giri di revisione | Gemini: R7, R8, R11, R12-bis, R13 (+ repliche); DGS: 01–04; revisori separati di Claude (16 e 17/11: dati e governance, 13 rilievi; laboratorio, in corso); **ogni giro ha trovato difetti importanti** |
| Giri puliti di fila (regola del sigillo) | **0 su 2 richiesti**. Prossimo: R14 (mandato pronto) |
| Test automatici | ~370 (dati, laboratorio, governance) + 77 Guardian, verdi su Python 3.13 **e** 3.9, rete bloccata |
| Mutanti negli script | **~370** in 6 script (+21 manuali sull'esportazione redatta), con controllo di validità del mutante (ha scartato un mio mutante con sintassi rotta, Q19, poi riscritto) |
| N (prove selezionabili) | **Nessun sigillo ancora: registro delle prove vuoto.** Censimento delle esecuzioni pre-sigillo (G-20261115-03) **riconfermato il 17/11** con lo strumento corretto: riserva intatta (`governance/censimento/RICONTEGGIO-20261117.md`). Esplorazioni E-001–E-003 contano per le ipotesi che ne usano i tagli. Emendamento su N recepito in DA-19 |
| Riserva di verifica | 2005-01-01 → 31/10/2023, mai letta dal sistema. Meccanismo del registro pronto (`riserva.py`); **α totale, finestre e parte protetta da ratificare** |
| Dati | Sviluppo (15/11/2023 → 12/11/2026) completo, BID e ASK. Storico: BID in scaricamento (al 2016 la sera del 16/11), poi ASK dal 2005 (**esistenza da verificare**) |
| Impegni anticipati | IA-01 (0,15 R, senza prova di anteriorità) · **IA-02: R medio netto ≥ +0,15 R**, fissato prima di ogni idea H-003 (commit `032250b`) |

## Cosa manca per il primo sigillo, in ordine
1. **Due giri di revisione di fila senza difetti critici o importanti** (contatore a 0; R14 pronto).
2. **Dati storici completi** e controllo della cache pulito; poi taratura della soglia di completezza sui conteggi dei minuti.
3. **Ratifica del registro della riserva** (α totale, scelta delle finestre, parte protetta) — titolare, con il parere del DGS (P2).
4. **Scelta della regola per IA-02** («sulla stima» o «sul limite inferiore», per sviluppo e verifica) — titolare, con il parere del DGS (P1).
5. **Approvazione del modello di scheda H-003** — titolare, con il parere del DGS (P3).
6. **Una scheda H-003 scritta e sigillata prima dei suoi dati** (l'idea è del titolare).

## Cosa serve dall'utente (comandi sul Mac)
1. **Riconteggio corretto** (legge soltanto; da un worktree nuovo, senza toccare `tb-scarica`):
   ```
   git -C ~/Downloads/trading-brain-core fetch origin feat/esecutore-h002
   git -C ~/Downloads/trading-brain-core worktree add --detach ../tb-riconta FETCH_HEAD
   cd ~/Downloads/tb-riconta && python3 -I -s -B brain/governance/censimento/riconta.py ~/.gemini/antigravity ~/.claude/projects > ~/Downloads/riconta2.txt; echo "codice $?"
   ```
   Poi mandare `riconta2.txt` a Claude (stampa solo conteggi, date ed estratti dei comandi con i prezzi mascherati). Codice 2 = un percorso non esiste: dirlo.
2. **Pacchetto per il DGS:** inviare `trading_brain_dgs05b.zip`, mai `trading_brain_dgs05.zip` (#72). Se il vecchio è già partito, dirlo.
3. **Scaricatore (facoltativo, quando comodo):** la versione in corso non scrive il motivo dei nuovi tentativi e non ha le correzioni #73 e #83. Per aggiornarlo, prima mandare a Claude l'uscita di `ps -o command= -p $(pgrep -f scarica_cache)`; Claude risponde con i comandi esatti di arresto e ripartenza (la ripresa è sicura: scrittura atomica e controllo dei file alla ripartenza).

## Decisioni aperte del titolare
- P1 regola per IA-02 · P2 regole di spesa della riserva · P3 modello di scheda H-003 (pareri chiesti al DGS il 16/11).
- DA-31 verdetto a due o tre stati (#94 b) · protezione del ramo su GitHub (#86, azione del titolare).
- Già decise: H-002 parcheggiata con condizione d'uscita scritta; IA-02 = 0,15 R; congelamento post-incidente.

## Rischi aperti, dichiarati
- **Il banco protegge dagli errori, non da chi ha i file (#90, #92):** il registro delle prove e quello della riserva sono file locali; chi ha accesso al Mac può scriverli a mano o leggere la cache con un altro script. La difesa vera è la storia su GitHub (voci spinte prima di ogni passo) letta dai revisori, più la protezione del ramo su GitHub, che spetta al titolare.
- **La memoria umana non si censisce:** chi ha guardato grafici 2005–2023 in passato resta non cieco; il sistema sì.
- **ASK storico forse inesistente:** senza, la verifica non misura gli stessi costi dello sviluppo; decidere prima come trattarla.
- **Sviluppo contaminato** (incidente del 14/11, #41): per le idee che usano i tagli E-003 lo sviluppo non è un banco pulito.
- **Correlazione fra trade:** misurata da Gemini (R13): gonfia i falsi positivi della regola «sulla stima»; da stimare nella scheda H-003.
