# Scheda di stato del progetto

**Aggiornata:** notte del 16–17/11/2026 (ultimo aggiornamento: 17/11 mattina, dopo la revisione notturna) · **a cura di:** Claude · **richiesta dal DGS** (DGS-04 §8). Una pagina: dove siamo, i contatori, cosa manca. Si aggiorna a ogni svolta (giro di revisione chiuso, dati completi, decisione del titolare), con la data.

## Dove siamo, in tre frasi
Il banco di prova (simulatore, criteri, sigillo, registri, scaricatore) è **costruito e sotto attacco incrociato**; ogni giro di revisione trova ancora difetti importanti, quindi **non è sigillabile**. **Nessuna strategia è operativa né promossa**: H-002 è parcheggiata con una condizione d'uscita scritta. I dati storici si stanno scaricando; la **riserva di verifica non è mai stata letta dal sistema**, ma la conclusione del censimento («nessuno l'ha vista») **va riconfermata**: lo strumento di riconteggio aveva quattro buchi (#75, #78, #80, #81), ora chiusi.

> **17/11, 9:30: la revisione del laboratorio ha trovato 3 difetti CRITICI APERTI (#86 verifica ripetibile, #87 e #88 codice non sigillato eseguibile) e 6 importanti (#89–#93).** Il banco di prova oggi NON garantisce che la verifica sia fatta una volta sola né con il codice sigillato. R14 non va consegnato finché non sono corretti.

## Contatori
| Cosa | Stato |
|---|---|
| Difetti registrati | **94** (22 critici, 51 importanti, 21 minori; conteggio del 17/11), **#86–#94 APERTI**, trovati da Gemini, DGS, revisori esterni, utente e Claude. Tutti corretti e provati, tranne **#42** (difetto della scheda H-002: parcheggiato con lei; regola obbligatoria nel modello H-003) |
| Giri di revisione | Gemini: R7, R8, R11, R12-bis, R13 (+ repliche); DGS: 01–04; revisori separati di Claude (16 e 17/11: dati e governance, 13 rilievi; laboratorio, in corso); **ogni giro ha trovato difetti importanti** |
| Giri puliti di fila (regola del sigillo) | **0 su 2 richiesti**. Prossimo: R14 (mandato pronto) |
| Test automatici | ~370 (dati, laboratorio, governance) + 77 Guardian, verdi su Python 3.13 **e** 3.9, rete bloccata |
| Mutanti negli script | **~370** in 6 script (+21 manuali sull'esportazione redatta), con controllo di validità del mutante (ha scartato un mio mutante con sintassi rotta, Q19, poi riscritto) |
| N (prove selezionabili) | **Nessun sigillo ancora: registro delle prove vuoto.** Censimento delle esecuzioni pre-sigillo (G-20261115-03): riserva intatta, **da riconfermare** con il riconteggio corretto (#75, #78, #80, #81). Esplorazioni E-001–E-003 contano per le ipotesi che ne usano i tagli. Emendamento su N recepito in DA-19 |
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
- Già decise: H-002 parcheggiata con condizione d'uscita scritta; IA-02 = 0,15 R; congelamento post-incidente.

## Rischi aperti, dichiarati
- **La memoria umana non si censisce:** chi ha guardato grafici 2005–2023 in passato resta non cieco; il sistema sì.
- **ASK storico forse inesistente:** senza, la verifica non misura gli stessi costi dello sviluppo; decidere prima come trattarla.
- **Sviluppo contaminato** (incidente del 14/11, #41): per le idee che usano i tagli E-003 lo sviluppo non è un banco pulito.
- **Correlazione fra trade:** misurata da Gemini (R13): gonfia i falsi positivi della regola «sulla stima»; da stimare nella scheda H-003.
