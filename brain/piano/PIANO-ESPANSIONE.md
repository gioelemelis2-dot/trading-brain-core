# 6 · Piano di espansione

Versione 1.1 · 11/11/2026 (aggiornata a fine sprint S2)

## 6.1 Criterio di priorità

Ogni blocco di lavoro riceve un punteggio da 1 a 3 su quattro criteri:

| Criterio | Domanda |
|---|---|
| **Lacuna** | Quanto manca? (3 = assente) |
| **Blocco** | Quanti moduli successivi ne dipendono? (3 = molti) |
| **Rischio** | Quanto è pericoloso non saperlo, o saperlo male? (3 = porta a decisioni sbagliate con denaro) |
| **Progressione** | È il prossimo cancello del percorso? (3 = sì) |

| Blocco | Lacuna | Blocco | Rischio | Progressione | Totale |
|---|---|---|---|---|---|
| **Modulo 2 · politica monetaria e trasmissione** | 3 | 3 | 2 | 3 | **11** |
| Traccia 10.1 · probabilità e statistica | 2 | 3 | 3 | 2 | 10 |
| Correzioni al v1 (A7, A9, A12–A15) | 1 | 1 | 3 | 3 | 8 |
| Modulo 6 · rischio e portafoglio | 2 | 2 | 3 | 1 | 8 |
| Modulo 8 · protocollo e bias dei dati | 2 | 2 | 3 | 1 | 8 |
| Modulo 1.6–1.7 · partecipanti e infrastrutture | 3 | 2 | 1 | 2 | 8 |
| Modulo 3 · analisi tecnica testabile | 3 | 2 | 2 | 1 | 8 |
| Traccia N · pipeline dati riproducibile | 3 | 2 | 2 | 1 | 8 |
| Modulo 4 · microstruttura II e order flow | 3 | 1 | 2 | 1 | 7 |
| Modulo 5 · fondamentale | 3 | 1 | 1 | 1 | 6 |
| Modulo 7 · tassonomia strategie | 2 | 1 | 2 | 1 | 6 |
| Modulo 9 · fiscalità e regole | 2 | 1 | 2 | 1 | 6 |
| Traccia 10.4 · ML | 3 | 0 | 2 | 0 | 5 |

**Perché il Modulo 2 viene prima della matematica, pur essendo la matematica "l'area più forte" richiesta.** Il Modulo 0 copre già la statistica operativa (aspettativa, varianza, campione, test) a livello sufficiente per iniziare il Modulo 2, che usa soprattutto aritmetica dei tassi e ragionamento sulle aspettative. Il Modulo 2 invece è **completamente assente**, è il **prossimo cancello** del percorso, ed è il nodo da cui partono le catene causali richieste (Fed → tassi → dollaro → …). La traccia 10.1 parte subito dopo, in parallelo, perché è prerequisito dei Moduli 6 e 8.

## 6.2 Fasi e sprint

Ogni sprint è pensato per una sessione di lavoro e lascia il Brain in uno stato coerente (registro e continuità aggiornati).

| Sprint | Fase | Contenuto | Uscita verificabile | Stato |
|---|---|---|---|---|
| S1 | 1–3, 4 | Governance, audit, verifica v1, mappa, architettura, bibliografia, piano; **M2 · L2.1–L2.3** + protocollo di analisi + strumento FedWatch | File in `brain/`, script eseguibili, registro | ✅ 11/11/2026 |
| S2 | 4, 3 | M2 · L2.4 Tassi reali e inflazione attesa · L2.5 Bilancio della BC (QE/QT, riserve) · L2.6 Fed/BCE/BoJ/BoE; classi di contenuto e ciclo di vita; piano di migrazione; specifica dati 0.17; materiali di collaborazione con Gemini | 3 lezioni `in_verifica`, documenti, `riproduci_017.py` | ✅ 11/11/2026 |
| S3 | 4, 6 | Lab M2: event study su decisioni FOMC/BCE con dati reali — **bloccato**: i siti di dati (FRED, Yahoo, Stooq) sono rifiutati dalla rete dell'ambiente; serve abilitarli o ricevere file dall'utente | Script + risultati, anche negativi | ⏸ |
| S3-bis | 4 | **Generatore del manuale HTML** dai Markdown (stile v1, navigabile, indice, flashcard, checklist, stato delle lezioni visibile) — decisione D-03 | `strumenti/genera_manuale.py` + HTML generato | ⏳ |
| S4 | 4 | Traccia 10.1 (parte 1): variabili casuali, distribuzioni, stima, IC, test, regressione | 5–6 lezioni + esercizi in Python | ⏳ |
| S5 | 5 | Applicare le correzioni del v1 come lezioni v2 (0.3, 0.19, 0.22, 1.5, 1.13) con nota di modifica | Diff documentato | ⏳ |
| S6 | 4 | M2 unità 2.2 (ciclo) e 2.3 (dati macro come eventi, vintages) | 5 lezioni | ⏳ |
| S7 | 4 | Traccia 10.2 serie storiche + traccia N (pipeline dati point-in-time) | Lezioni + libreria minima testata | ⏳ |
| S8 | 4 | M1.6–1.7 partecipanti e infrastrutture | 4 lezioni | ⏳ |
| S9 | 4 | M2 unità 2.4–2.7 (credito, sistema monetario internazionale, plumbing, energia) | 6–8 lezioni + 3 casi storici | ⏳ |
| S10–S12 | 4 | M3 analisi tecnica come regole testabili | Lezioni + test riproducibili | ⏳ |
| S13–S15 | 4 | M6 rischio e portafoglio | Lezioni + simulatori | ⏳ |
| S16+ | 4–7 | M8, M4, M5, M7, M9, tracce 10.3–10.10 | — | ⏳ |
| ogni 5 sprint | 6 | Revisione: fonti C → V, date di validità, coerenza, duplicazioni | Rapporto di verifica | ⏳ |

## 6.3 Regole di avanzamento

1. Nessuno sprint aggiunge una lezione senza aggiornare `REGISTRO-CONOSCENZE.md` e `REGISTRO-MODIFICHE.md`.
2. Una lezione passa da `bozza` a `verificata` solo quando **tutte** le fonti usate come prova sono **V** e un secondo controllo ha ricalcolato gli esempi numerici.
3. Contenuti con data di scadenza (tassi, norme, fiscalità, orari): campo `revisione_entro` obbligatorio.
4. Ogni 5 sprint si riapre la matrice delle lacune e si ricalcolano le priorità.
5. Le domande nate durante lo studio vanno in `glossario/DOMANDE-APERTE.md`, non si perdono nel testo.

## 6.4 Ordine aggiornato dei prossimi sprint

S4 traccia 10.1 (statistica) → S3-bis generatore HTML → S5 correzioni v1 → S6 unità 2.2–2.3 → S3 lab (appena ci sono dati reali). La verifica di Gemini sulle lezioni L2.1–L2.6 (richiesta R-001) procede in parallelo e decide quando passano a `verificata`.

## 6.5 Cosa serve dall'utente

- **Padronanza**: i cancelli si superano rispondendo; la base registra il superamento solo quando l'utente lo dichiara (con data). Il Brain non si "auto-promuove".
- **Dati del vault**: se si vuole rigenerare la tabella 0.17, servono i dati o almeno la fonte usata.
- **Rete**: per i laboratori dati (S3, S7) serve che l'ambiente consenta l'accesso a FRED / BCE / altri provider.
