# 06 · Qualità delle fonti, dei riferimenti e delle procedure di validazione

Audit AUDIT-ARCH-20261111.

## 1. Fonti
| Aspetto | Stato | Valutazione |
|---|---|---|
| Classificazione delle fonti (F1–F7) e degli stati di verifica (V/V-sec/C/X) | Definita e applicata in bibliografia e nelle lezioni nuove | **Buona**: dichiara onestamente che cosa non è stato letto |
| Stato effettivo della bibliografia | ≈ 2 V, 29 V-sec, 160 C (conteggio automatico approssimato) | **Debole**: oltre l'80% citato da memoria |
| Fonti delle lezioni nuove | 0 V; V-sec soprattutto da abstract e fonti secondarie | Sufficiente per `in_verifica`, **non** per `verificata` |
| Manuale v1 | Citazioni senza titolo, sede né stato; 2 errori accertati | Correzioni pronte, non applicate (S5 sospeso) |
| Regole FTMO | Solo fonti secondarie discordanti | **Insufficiente** per qualsiasi uso operativo |
| Accesso alle fonti | Alcuni siti bloccati dalla rete dell'ambiente (FRED, Yahoo, Stooq; alcuni PDF) | Limite strutturale da risolvere con abilitazioni o con l'aiuto di Gemini |

**Rischio principale:** il passaggio da C a V è il collo di bottiglia della qualità. Senza un piano, le lezioni restano `in_verifica` indefinitamente.

**Proposta (da approvare):**
1. Priorità alle ≈ 40 fonti citate come prova nelle lezioni L2.1–L2.6 (44 citazioni V-sec o C, con alcune ripetute tra lezioni) e nella seconda revisione.
2. Per ogni fonte portata a V, registrare che cosa è stato letto (abstract, tabella, pagina), da chi e quando, con una citazione breve.
3. Suddivisione: Gemini (R-006) per le fonti che il suo ambiente raggiunge, Claude per le altre.

## 2. Procedure di validazione
| Procedura | Dove | Maturità |
|---|---|---|
| Ricalcolo dei numeri con script | `strumenti/verifica_m0.py`, `sorpresa_monetaria.py`, `tassi_reali.py` | Buona; script dimostrativi più che test |
| Calcolo esatto come riferimento per i Monte Carlo | Seconda revisione (`c1`, `c4b`, `c8`) | **Alta**: è la procedura più solida del Brain |
| Più seed e numeri casuali comuni | Seconda revisione (`c2`, `c6`) | Alta |
| Test di mutazione | Seconda revisione (`c9`) | Alta; da estendere a tutti gli strumenti canonici |
| Impronte SHA-256 e manifest | Pacchetto per Gemini, revisione | Buona; serve una regola su quando rigenerarli (I-10) |
| Revisione incrociata Claude–Gemini | `collaborazione/` | Funzionante; trasferimenti via chat fragili (I-08, I-09) |
| Esecutore unico dei test | — | **Assente** (L-02) |
| Verifica sui dati reali | — | **Assente** (L-01) |
| Controllo delle fonti nel testo integrale | — | **Quasi assente** |

## 3. Errori miei trovati in questo audit (autoverifica)
| Dove | Errore | Stato |
|---|---|---|
| Seconda revisione §4.6 | "6 dei 7" invece di "4 dei 7" | Corretto con `ERRATA.md` |
| Contestazione C-04 | Rimando "(§3, C-05)" invece di "(§3, C-06)" | Segnalato all'utente; non ancora corretto nel file |
| `REGISTRO-MODIFICHE.md` | "185 voci" di bibliografia, oggi ≈ 190 | Da aggiornare (I-06) |

## 4. Raccomandazioni
1. **Esecutore unico dei test** (`strumenti/esegui_verifiche.py`): una sola chiamata che esegue tutti gli auto-test e scrive un rapporto con data e hash. È un piccolo strumento di qualità, non una nuova funzione di trading; da approvare.
2. **Regola dei manifest:** rigenerarli a ogni commit che tocca la cartella, oppure dichiarare sempre a quale commit si riferiscono.
3. **Archivio delle consegne** con manifest congelato (documento 05 §4).
4. **Piano C → V** (§1) con priorità per uso.
5. **Fonti ufficiali FTMO:** da leggere prima di qualsiasi lavoro sul Guardian (Gemini, R-003 esteso, o abilitazione di rete).
