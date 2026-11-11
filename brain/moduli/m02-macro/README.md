# Modulo 2 · Macro, politica monetaria e flussi

> Obiettivo: capire **che partita si gioca**: chi fissa il prezzo del denaro, come le aspettative entrano nei prezzi, come uno shock si propaga dai tassi fino al rischio del singolo trade.

| Prerequisiti | Durata stimata | Cancello |
|---|---|---|
| Modulo 0, Modulo 1 (in particolare 1.1, 1.2, 1.3, 1.8) | 4–6 settimane (unità 2.1: 1–2 settimane) | L4 |

## Stato delle lezioni

| Unità | Lezione | Stato | File |
|---|---|---|---|
| 2.1 Politica monetaria e mercati | L2.1 Banche centrali: mandati, strumenti, come si fissa il tasso | in_verifica v0.1 | [L2.1](L2.1-banche-centrali-e-strumenti.md) |
| | L2.2 Aspettative e sorprese | in_verifica v0.1 | [L2.2](L2.2-aspettative-e-sorprese.md) |
| | L2.3 La catena di trasmissione ai mercati | in_verifica v0.1 | [L2.3](L2.3-trasmissione-ai-mercati.md) |
| | L2.4 Tassi nominali, reali e inflazione attesa | in_verifica v0.1 | [L2.4](L2.4-tassi-reali-e-inflazione-attesa.md) |
| | L2.5 Bilancio della banca centrale: QE, QT, riserve | in_verifica v0.1 | [L2.5](L2.5-bilancio-banca-centrale-qe-qt.md) |
| | L2.6 Fed, BCE, BoJ, BoE: differenze che contano | in_verifica v0.1 | [L2.6](L2.6-fed-bce-boj-boe.md) |
| | Lab: event study su decisioni FOMC/BCE | bloccato: servono dati reali (rete o file dell'utente) | — |
| 2.2–2.7 | Vedi `architettura/ARCHITETTURA.md` | pianificate | — |

Nessuna lezione è ancora `verificata`: lo diventa quando tutte le fonti usate come prova sono lette (V) e gli esempi ricontrollati da un secondo revisore (Claude o Gemini, non l'autore). Ciclo di vita in `governance/STANDARD.md` §9.

Strumenti: [Protocollo di analisi di un movimento](PROTOCOLLO-ANALISI-MOVIMENTO.md) · [`strumenti/sorpresa_monetaria.py`](../../strumenti/sorpresa_monetaria.py) · [`strumenti/tassi_reali.py`](../../strumenti/tassi_reali.py)


## Cancello dell'unità 2.1 (intermedio)
Senza note, a voce o per iscritto:
1. Spiega il regime di pavimento della Fed e della BCE e colloca IORB, ON RRP, DFR. **(L2)**
2. Calcola sorpresa e probabilità implicita da due prezzi di futures dati. **(L3)**
3. Su una decisione reale recente: compila il protocollo pre/post evento, classifica lo shock (policy/informativo), percorri la catena di trasmissione segnando quali anelli sono osservati e quali ipotizzati. **(L4)**
4. Indica un anello con evidenza debole e descrivi il test che potrebbe rafforzarla o smentirla. **(L4→L5)**
5. Calcola un tasso reale esatto e scomponi un breakeven; scrivi le scritture contabili di un QE; spiega EUR/USD come confronto tra due banche centrali. **(L3)**

Superamento: tutti e cinque i punti, con calcoli corretti e almeno due spiegazioni alternative al punto 3. Si registra in `governance/REGISTRO-CONOSCENZE.md` con data.

## Cancello del Modulo 2 (finale, da completare quando il modulo è scritto)
Dato un evento macro reale, costruire il quadro (attese, sorpresa, catena di trasmissione con livelli di evidenza, spiegazioni alternative, conseguenze sul rischio) e dichiarare **cosa lo smentirebbe**. **(L4)**

## Flashcard di ripasso dell'unità (recupero misto)
| Domanda | Risposta |
|---|---|
| Perché una decisione attesa al 100% non muove i prezzi? | L'informazione è già incorporata nei futures: la sorpresa è zero |
| Target vs path? | Sorpresa sul tasso di oggi vs sul percorso futuro (comunicato); il path muove di più i tassi lunghi |
| Che cosa decide la size dopo uno shock macro? | La volatilità: a rischio fisso, stop più larghi → esposizione minore |
| Tasso guida BCE dal 2024? | DFR |
| Che cosa non controlla la banca centrale? | I tassi lunghi (premio a termine), il cambio, le azioni: li influenza soltanto |

## Ripasso spaziato
Rivedi le flashcard dopo 1 giorno, 1 settimana, 1 mese (Modulo 0.24). Riapri il protocollo a ogni riunione FOMC/BCE: è l'esercizio di applicazione ricorrente del modulo.
