# 1 · Diagnosi del Brain attuale

Audit del **Manuale del Brain v1** (artifact `T4xESphh3BmonZPoprQBtb`, ultimo aggiornamento 23/09/2026; copia in `originale/manuale-v1.html`, sha256 `931685e6…6634`).
Eseguito il 11/11/2026 leggendo integralmente il testo (809 righe estratte, 42 lezioni).

## 1.1 Cosa contiene davvero

| Parte | Contenuto | Volume |
|---|---|---|
| Copertina, percorso, metodo, mantra | Percorso 0–10, regola del cancello, 7 frasi-mantra | — |
| **Modulo 0** · Fondamenta mentali e statistiche | 4 unità, **24 lezioni**, checklist (7 voci), 12 flashcard, cancello | ~60% del testo |
| **Modulo 1** · Come funzionano i mercati | 5 unità, **18 lezioni**, checklist (7), 10 flashcard, cancello | ~40% del testo |
| Moduli 2–10 | Solo titolo e sottotitolo nel percorso; blocco "in arrivo" | 0 lezioni |

Il manuale si presenta come "il tuo vault Obsidian, riscritto per essere studiato": una parte dei dati (statistiche S&P 500 / Nasdaq / Bitcoin 2016–2026, gap) viene dal vault dell'utente, che non è in questo repository.

### Inventario delle lezioni

**Modulo 0**

| Unità | Lezioni | Giudizio sintetico |
|---|---|---|
| 0.1 Onestà sull'obiettivo | 1 Verdetto onesto · 2 Perché i retail perdono · 3 Replication crisis e fattori · 4 Metodo scientifico | Solido e ben documentato; due citazioni imprecise (McLean-Pontiff, Novy-Marx/RMW) |
| 0.2 Modello mentale | 5 Mercato quasi-casuale · 6 Pensare in probabilità · 7 Processo vs risultato · 8 Le 10 regole | Buona didattica; teoria dell'efficienza solo accennata (manca Fama 1970, Lo 2004 è citato via libro) |
| 0.3 Ancora statistica | 9 Edge · 10 Aspettativa · 11 R · 12 Win rate e R:R · 13 Varianza e drawdown · 14 Campione · 15 Ergodicità · 16 Monte Carlo · 17 Statistica descrittiva · 18 Test e serie storiche | Punto più forte del manuale; numeri verificati (vedi 02). La lezione 18 comprime in una pagina temi che meritano un modulo (GARCH, cointegrazione, DSR, PBO) |
| 0.4 Fattore umano | 19 Cervello sotto rischio · 20 Bias · 21 Tilt · 22 Sonno · 23 Vita finanziaria · 24 Learning science | Utile operativamente; alcune affermazioni neuroscientifiche sono semplificate oltre l'evidenza |

**Modulo 1**

| Unità | Lezioni | Giudizio sintetico |
|---|---|---|
| 1.1 Mercati e motori | 1 Forex · 2 Indici · 3 Obbligazioni e curva · 4 Materie prime · 5 Cripto e volatilità come asset · 6 Correlazioni | Panoramica corretta ma da "scheda": driver elencati senza meccanismo né evidenza |
| 1.2 Strumenti | 7 Azioni ed ETF · 8 Futures · 9 Opzioni · 10 CFD, FX spot, derivati cripto · 11 Confronto · 12 Ordini · 13 Costi e fiscalità IT | Pratico e corretto; opzioni ridotte al minimo; fiscalità senza fonti né data di riferimento puntuale |
| 1.3 Cripto dalle fondamenta | 14 Whitepaper · 15 Stablecoin | Buono per un'introduzione |
| 1.4 Orizzonti | 16 Orizzonti · 17 Multi-timeframe | Buono; il multi-timeframe è presentato come regola senza evidenza empirica |
| 1.5 Come si scambia | 18 Microstruttura e market making | Una sola lezione per un'intera disciplina (Area C) |

## 1.2 Punti di forza (da conservare)

1. **Postura epistemica corretta fin dalla prima pagina**: base rate contro il retail, replication crisis, "tratta ogni backtest come un paper". È la qualità più rara nei materiali di trading.
2. **Numeri concreti e verificabili**: le tabelle di strisce di perdite, t-statistic, ergodicità e sconto dei flussi sono corrette (verificate con calcolo esatto, `strumenti/verifica_m0.py`).
3. **Didattica attiva**: definizione → esempio → errori → sintesi → flashcard → checklist → cancello. Coerente con la learning science che il manuale stesso insegna (lezione 0.24).
4. **Ragionamento in R e in aspettativa** come lingua comune di tutto il percorso.
5. **Fattore umano trattato con contromisure strutturali** (attrito, regole, kill switch), non con esortazioni.

## 1.3 Limiti strutturali

| # | Limite | Conseguenza |
|---|---|---|
| L1 | **Monolite HTML** di 128 KB, con progressi salvati nel browser | Non versionabile per lezione, non collegabile, difficile da aggiornare senza riscrivere; i progressi non sono un registro verificabile |
| L2 | **Fonti in forma di menzione** ("Hou, Xue, Zhang (2020)") senza titolo, rivista, link, né stato di verifica | Non si può controllare la provenienza; due citazioni risultano errate |
| L3 | **Nessun livello di evidenza** | Si leggono con lo stesso peso un risultato replicato (momentum) e una semplificazione divulgativa (testosterone e "winner effect") |
| L4 | **Nessuna data di validità** sui contenuti che invecchiano | Fiscalità, regole ESMA, orari di sessione, costi, tassi: tutto senza "aggiornato al" |
| L5 | **Collegamenti solo lineari** ("Poi → Modulo 1") | Mancano le reti causali che l'utente chiede (es. Fed → tassi → dollaro → …) |
| L6 | **Cancelli solo L1–L3** (ricordo, calcolo, scelta di strumento) | Nessun cancello chiede analisi critica (L4) o progettazione di un test (L5) |
| L7 | **Matematica implicita**: si usano t-test, σ, GARCH, regressione senza un percorso che li costruisca | Il Brain "usa" strumenti che non ha studiato; Area F è il prerequisito mancante più grave per i Moduli 4–8 |
| L8 | **Dati del vault non riproducibili** (tabella lezione 0.17, statistiche sui gap) | Valori probabilmente corretti ma non verificabili senza script e dati: vanno rigenerati con pipeline documentata |
| L9 | **Moduli 2–10 assenti** | Circa l'80% del perimetro richiesto dalla missione non esiste ancora |

## 1.4 Che cosa sa fare oggi il Brain (onestamente)

| Livello | Stato |
|---|---|
| L1–L2 su probabilità operative, aspettativa, R, drawdown, bias | **Presente** (contenuti solidi; padronanza non registrata) |
| L1–L2 su strumenti, ordini, costi | **Presente** |
| L1 su macro, curva, correlazioni | **Superficiale** |
| L3 su dati reali | **Quasi assente**: nessun esercizio su dati scaricabili, nessuno script |
| L4 analisi critica | **Presente solo come atteggiamento** (Modulo 0), non come metodo esercitato |
| L5 ricerca | **Assente**: il protocollo in 7 passi (lezione 0.4) è corretto ma non è mai stato applicato |

## 1.5 Conclusione della diagnosi

Il v1 è una **buona porta d'ingresso**: atteggiamento scientifico, statistica operativa e psicologia sono sopra la media dei materiali sul trading. Non è ancora un Brain multidisciplinare. Le priorità che emergono:

1. **Struttura**: passare da un monolite a file modulari con registro, fonti verificabili, livelli di evidenza (fatto in questa fase).
2. **Contesto macro (Modulo 2)**: è il prossimo cancello del percorso, è del tutto assente, ed è il nodo da cui partono quasi tutte le catene causali richieste. → **primo intervento** (vedi `piano/PIANO-ESPANSIONE.md`).
3. **Fondamenta quantitative (traccia Q, Area F)**: prerequisito di 4, 7, 8. → secondo intervento, in parallelo.
4. **Correzioni puntuali al v1** (vedi `02-VERIFICA-AFFERMAZIONI.md`).
