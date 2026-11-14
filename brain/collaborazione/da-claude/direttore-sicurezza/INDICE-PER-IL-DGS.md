# Indice per il Direttore generale della sicurezza (DGS)

**Cosa contiene l'archivio:** `trading_brain_completo.zip`, cioè
- la copia esatta del repository (git archive del ramo `feat/esecutore-h002`);
- 11 file di Gemini dai rami non ancora uniti (aggiunti nell'archivio, non nel ramo);
- il documento «Progetto generale» esportato (ora anche nel repository, in `brain/piano/`);
- il `MANIFEST.tsv`: per ogni file, impronta SHA-256, righe e byte.

**Il commit di riferimento** è in testa al MANIFEST.

## 1. Ordine di lettura consigliato
1. `brain/piano/PROGETTO-GENERALE-20261115.md`: scopo, obiettivi, roadmap a gate, rischi, regole. Lo stato è fermo al 13/11, con le note di Claude sulle parti superate.
2. `brain/CONTINUITA.md`: stato e pendenze, documento di ripresa.
3. `brain/governance/DECISIONI.md` e `DECISIONI-APERTE.md`: decisioni prese (D-…) e da prendere (DA-…).
4. `brain/governance/STANDARD.md` e `MODELLO-EPISTEMICO.md`: regole di qualità e tipi di evidenza.
5. `brain/laboratorio/REGISTRO-DIFETTI.md`: 32 difetti trovati, con gravità e lettura.
6. `brain/laboratorio/ipotesi/`:
   - schede di H-002 (v3.1 in vigore, proposta v3.2) e storia delle revisioni R1–R10 (`H-002-REVISIONI.md`);
   - H-001 chiusa;
   - quaderno delle idee Q-01…Q-10.
7. Codice di H-002:
   - simulatore: `laboratorio/simulatori/orb_londra.py`;
   - programma dei criteri e sigillo: `laboratorio/esecuzione/`;
   - test e mutanti: `laboratorio/tests/`.
8. `brain/governance/PIANO-DIVERSIFICAZIONE.md`: dopo l'oro, altri mercati.
9. Il resto, per aree (sotto).

## 2. Mappa per aree
| Cartella | File | Cosa c'è | Note per il DGS |
|---|---|---|---|
| `brain/governance/` | 7 | decisioni, standard, modello epistemico, registro delle conoscenze, registro delle modifiche (storia completa), piano di diversificazione | `REGISTRO-CONOSCENZE.md` è in parte arretrato (vedi CONTINUITA, «Correzioni note») |
| `brain/dati/` | 20 | pipeline Dukascopy (scaricamento, controlli, partizione per date con embargo, sigillo con nonce), riferimenti (festivi UK ufficiali), test | i dati scaricati e il nonce NON ci sono (stanno solo sul Mac dell'utente) |
| `brain/laboratorio/` | 41 | backtester e DSR, studi E-001 ed E-002, ipotesi, simulatore di H-002, programma dei criteri, test, mutanti, indicatore TradingView | `trial_registry.json` è il vecchio registro vuoto (A7: da congelare) |
| `brain/guardian/` | 24 | Guardian G0 consultivo (scheda pre-trade, limiti, regole personali), journal con catena di hash, test | consultivo: non blocca ordini (D-16) |
| `brain/collaborazione/` | 175+ | protocollo, LOCK, rapporti di Gemini (`da-gemini/`), lavori di Claude (`da-claude/`), revisioni di Claude sui materiali di Gemini (V2–V3.3, architettura), pacchetti | qui va anche `da-chatgpt/` (tuo) |
| `brain/audit/` | 14 | diagnosi del manuale v1, verifica delle affermazioni, matrice delle lacune, audit architetturale dell'11/11 | |
| `brain/moduli/`, `glossario/`, `bibliografia/`, `mappa/`, `architettura/` | 14 | conoscenza: Modulo 2 (lezioni in verifica), glossario, bibliografia, mappe | sviluppo della conoscenza sospeso (D-12, D-20) |
| `brain/originale/` | 2 | manuale v1 originale (23/09/2026), intatto | |
| `brain/piano/` | 3 | Progetto generale (esportato il 15/11, schemi trascritti), piano di espansione, piano di migrazione | piano di migrazione: mai approvato |
| `brain/strumenti/` | 4 | piccoli script di verifica | |

## 3. Stato dei rami (al momento dell'archivio)
| Ramo | Stato | Cosa contiene |
|---|---|---|
| `main` | unico riferimento ufficiale | tutto fino al simulatore di H-002 (43 test) e alla scheda v3.1 |
| `feat/esecutore-h002` | **NON unito**, è la base di questo archivio | programma dei criteri, sigillo, correzioni D1/D2 e P1–P8, test strutturali, proposta v3.2, registro dei difetti |
| `fix/orb-replica-gemini` | NON unito; già compreso in `feat/esecutore-h002` | correzioni D1 e D2 |
| `rev/gemini-replica-h002`, `rev/gemini-esecutore-h002`, `rev/gemini-h002-v2` | NON uniti; i loro file sono nell'archivio (sotto `brain/collaborazione/da-gemini/`) | rapporti, repliche, sonde di Gemini |
| altri rami `rev/…`, `fix/…`, `feat/fix-g0-journal` | già uniti a main | da cancellare quando l'utente lo autorizza |

## 4. Cose superate che Claude conosce (controllale e cercane altre)
- «IS 70% / OOS 30%» nell'architettura e nel Gate 2: superato da DA-26 (inversione del 14/11).
- «easyMarkets» nel Gate 5: superato (broker FP Markets, DA-25).
- La scheda H-002 v3.1 dice che il programma dei criteri «va scritto»: ora c'è, sul ramo non unito.
- Gate 3–7: proposte di Claude, mai approvate formalmente dall'utente.
- Il numero dei test cambia a ogni giro: fa fede `H-002-REVISIONI.md`, non le schede.

## 5. Cosa NON c'è, ed è voluto
- Dati di mercato (cache Dukascopy, CSV) e nonce del sigillo: solo sul Mac dell'utente.
- Dati personali (stipendio, budget, journal dei trade, conti).
- Le chat originali con Claude, Gemini, DeepSeek e ChatGPT: nel repository ci sono i riassunti verificati, con gli esiti.
- Gli ZIP dei materiali V3/V3.1/V3.2/V3.3 di Antigravity: mai archiviati (impronte nelle revisioni).
