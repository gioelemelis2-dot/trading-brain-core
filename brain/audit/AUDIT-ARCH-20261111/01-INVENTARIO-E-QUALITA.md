# 01 · Inventario e qualità dei moduli

Audit AUDIT-ARCH-20261111 · Base: commit `a764e61` · Misure: `strumenti/misure_20261111.txt` (script `strumenti/misure_brain.py`, sola lettura).

## 1. Che cosa c'è nel Brain oggi

| Strato | Contenuto | Stato reale |
|---|---|---|
| **Formazione** | Manuale v1: Moduli 0–1, 42 lezioni, 2 cancelli (`originale/`) · Modulo 2, unità 2.1: 6 lezioni (`moduli/m02-macro/`) · protocollo di analisi di un movimento | v1 intatto, con 2 errori e 8 imprecisioni noti e non ancora corretti · L2.1–L2.6 `in_verifica` · nessun cancello superato |
| **Governance** | STANDARD (fonti F1–F7, evidenze E1–E7, stati V/V-sec/C/X, classi di contenuto, ciclo di vita), DECISIONI D-01…D-12, registri | Completa sulla carta, applicata in modo disomogeneo (§3) |
| **Mappa e architettura** | Mappa A–Z, dipendenze, architettura spina 0–9 + tracce 10.x, piano a sprint, piano di migrazione (sospeso) | Solo didattica: **non prevede un posto per sistemi software** (Strategy Discovery Lab, Trading Guardian) |
| **Audit e fonti** | Diagnosi v1, verifica di 18 citazioni e 11 calcoli, matrice lacune, bibliografia (~190 righe) | Matrice ferma a prima di L2.4–L2.6; bibliografia per l'84% citata da memoria (C) |
| **Strumenti** | 4 script in `strumenti/` (verifica v1, sorpresa monetaria, tassi reali, riproduzione 0.17) + strumenti di revisione in `collaborazione/` | Tutti eseguibili con la sola libreria standard; nessun esecutore unico dei test |
| **Dati** | Regole reali/simulati, richiesta dati 0.17 | **Nessun dato reale nel Brain** (rete verso i provider bloccata; dati del vault non ancora forniti) |
| **Collaborazione** | Handoff, protocollo provvisorio, LOCK, richieste R-001…R-009, pacchetto per Gemini, checklist e modello di revisione, seconda revisione V2 con 11 strumenti, errata, contestazione | Funzionante; i materiali V2 di Gemini **non sono archiviati nel Brain** (ci sono solo i loro hash) |

## 2. Qualità dei moduli formativi

### 2.1 Manuale v1 (Moduli 0–1)
| Criterio | Valutazione | Evidenza |
|---|---|---|
| Correttezza numerica | **Alta**: tutti gli 11 calcoli ricontrollati sono corretti | `audit/02-VERIFICA-AFFERMAZIONI.md` §B |
| Correttezza delle citazioni | **Media**: 2 errori (McLean-Pontiff, Novy-Marx/RMW), 8 imprecisioni | §A dello stesso file |
| Struttura | Diversa dal modello a 20 sezioni (definizione → esempio → errori → sintesi); nessuna fonte con stato; nessun livello di evidenza | Per scelta: il v1 è conservato intatto |
| Verifica dell'apprendimento | Flashcard e checklist presenti; 2 cancelli (L1–L3); nessun cancello L4/L5 | `originale/manuale-v1.txt` |
| Utilità per il passaggio al quantitativo | **Buona come base**: aspettativa, R, varianza, campione, ergodicità, Monte Carlo, test multipli. La lezione 0.18 condensa in una pagina temi che richiedono un modulo intero | Lezioni 0.9–0.18 |

### 2.2 Modulo 2, unità 2.1 (L2.1–L2.6)
| Lezione | Sezioni | Stato | Fonti V / V-sec / C | Etichette di classe | Flashcard | Esercizi |
|---|---|---|---|---|---|---|
| L2.1 | 20/20 | in_verifica | 0 / 4 / 3 | **assenti** | 8 | 4 |
| L2.2 | 20/20 | in_verifica | 0 / 5 / 4 | **assenti** | 8 | 4 |
| L2.3 | 20/20 | in_verifica | 0 / 2 / 5 | **assenti** | 6 | 4 |
| L2.4 | 20/20 | in_verifica | 0 / 2 / 4 | 30 | 7 | 4 |
| L2.5 | 20/20 | in_verifica | 0 / 3 / 4 | 36 | 6 | 4 |
| L2.6 | 20/20 | in_verifica | 0 / 5 / 3 | 42 | 7 | 4 |

**Giudizio:**
- La struttura è completa e uniforme; gli esempi numerici sono riprodotti da script.
- **Nessuna lezione può diventare `verificata`**: nessuna fonte è letta nel testo integrale, e manca il secondo revisore (R-001 a Gemini, non ancora restituita).
- L2.1–L2.3 vanno allineate alle etichette di classe (STANDARD §8), quando lo sviluppo sarà riaperto.
- Pertinenza al trading quantitativo: **indiretta**. Il Modulo 2 dà il contesto (regimi, eventi, trasmissione) ma non gli strumenti della ricerca sistematica.

### 2.3 Lavoro quantitativo (strumenti e revisioni)
| Elemento | Qualità | Nota |
|---|---|---|
| Calcolo esatto delle challenge (`R-CLAUDE…/verifiche/c1_esatto_challenge.py`) e riferimento di rovina (`revisione-materiali-gemini/strumenti/riferimento_rovina.py`) | Alta: verificati contro formule chiuse e contro il motore di Gemini | **Due strumenti con scopo sovrapposto** (§ documento 02) |
| Motore V2 di Gemini | Corretto per il modello i.i.d.; 4 difetti (C-01…C-04) | Non archiviato nel Brain; in attesa della risposta di Gemini |
| Procedure di revisione (checklist, mutazioni, numeri casuali comuni, calcolo esatto) | **Il punto più maturo del Brain** in termini di validazione | Riutilizzabili per lo Strategy Discovery Lab |

## 3. Indicatori sintetici (11/11/2026)

| Indicatore | Valore |
|---|---|
| Lezioni scritte (v1 + nuove) | 42 + 6 |
| Lezioni `verificata` | **0** |
| Cancelli superati dall'utente | **0** registrati |
| Fonti bibliografiche lette (V) / confermate indirettamente (V-sec) / da memoria (C) | ≈ 2 / 29 / 160 (conteggio automatico sulle righe delle tabelle, approssimato) |
| Dati reali disponibili | 0 serie |
| Strumenti verificati con test | 4 script canonici con auto-test o esempi; 11 strumenti di revisione con risultati archiviati |
| Aree della mappa con copertura ≥ 25% | 4 su 17 (`audit/03-MATRICE-LACUNE.md`, da aggiornare) |
