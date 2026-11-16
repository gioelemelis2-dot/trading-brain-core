# Scheda di stato del progetto

**Aggiornata:** notte del 16–17/11/2026 · **a cura di:** Claude · **richiesta dal DGS** (DGS-04 §8). Una pagina: dove siamo, i contatori, cosa manca. Si aggiorna a ogni svolta (giro di revisione chiuso, dati completi, decisione del titolare), con la data.

## Dove siamo, in tre frasi
Il banco di prova (simulatore, criteri, sigillo, registri, scaricatore) è **costruito e sotto attacco incrociato**; ogni giro di revisione trova ancora difetti importanti, quindi **non è sigillabile**. **Nessuna strategia è operativa né promossa**: H-002 è parcheggiata con una condizione d'uscita scritta. I dati storici si stanno scaricando; la **riserva di verifica non è mai stata letta dal sistema**.

## Contatori
| Cosa | Stato |
|---|---|
| Difetti registrati | **71** (17 critici, 39 importanti, 15 minori), trovati da Gemini, DGS, revisori esterni, utente e Claude. Tutti corretti e provati, tranne **#42** (difetto della scheda H-002: parcheggiato con lei; regola obbligatoria nel modello H-003) |
| Giri di revisione | Gemini: R7, R8, R11, R12-bis, R13 (+ repliche); DGS: 01–04; un revisore esterno; **ogni giro ha trovato difetti importanti** |
| Giri puliti di fila (regola del sigillo) | **0 su 2 richiesti**. Prossimo: R14 (mandato pronto) |
| Test automatici | ~340 (dati, laboratorio, governance) + 77 Guardian, verdi su Python 3.13 **e** 3.9, rete bloccata |
| Mutanti negli script | **338** in 6 script (+12 manuali sull'esportazione redatta), con controllo di validità del mutante; ultima corsa completa in corso stanotte |
| N (prove selezionabili) | **Nessun sigillo ancora: registro delle prove vuoto.** Censimento delle esecuzioni pre-sigillo chiuso (G-20261115-03): riserva intatta. Esplorazioni E-001–E-003 contano per le ipotesi che ne usano i tagli. Emendamento su N recepito in DA-19 |
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

## Decisioni aperte del titolare
- P1 regola per IA-02 · P2 regole di spesa della riserva · P3 modello di scheda H-003 (pareri chiesti al DGS il 16/11).
- Già decise: H-002 parcheggiata con condizione d'uscita scritta; IA-02 = 0,15 R; congelamento post-incidente.

## Rischi aperti, dichiarati
- **La memoria umana non si censisce:** chi ha guardato grafici 2005–2023 in passato resta non cieco; il sistema sì.
- **ASK storico forse inesistente:** senza, la verifica non misura gli stessi costi dello sviluppo; decidere prima come trattarla.
- **Sviluppo contaminato** (incidente del 14/11, #41): per le idee che usano i tagli E-003 lo sviluppo non è un banco pulito.
- **Correlazione fra trade:** misurata da Gemini (R13): gonfia i falsi positivi della regola «sulla stima»; da stimare nella scheda H-003.
