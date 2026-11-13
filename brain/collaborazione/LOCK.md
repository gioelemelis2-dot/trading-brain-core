# Bacheca delle attività (LOCK)

Leggere prima di iniziare. Regole in [`PROTOCOLLO-OPERATIVO.md`](PROTOCOLLO-OPERATIVO.md) §4 (provvisorio).

**Aggiornata il 13/11/2026 (commit `b9e4cc8`): leggere prima `CONTINUITA.md`.** Le righe di stato precedenti erano ferme all'11–12/11 e sono superate.

Stato generale:
- G0 consultivo e journal: completi su `main`.
- Laboratorio (Binario B, `dati/pipeline`, `laboratorio/backtester`): preso in carico da Claude su mandato dell'utente.
- **Gate 2:** dati XAUUSD in scaricamento sul Mac dell'utente. Il sigillo sui 3 anni con 70/30 è **provvisorio** (DA-26), perché l'Out-of-Sample degli ultimi ~11 mesi è già stato visto.
- **Proposte aperte:** piano di diversificazione (`governance/PIANO-DIVERSIFICAZIONE.md`, DA-27, DA-28).

**Regola per tutti, Gemini compreso:** nessuno analizza i dati storici prima che le ipotesi siano scritte e sigillate (Gate 3). Come Claude, anche Gemini conosce dall'addestramento l'andamento dei mercati recenti.

## File congelati
| File | Motivo | Da | Fino a |
|---|---|---|---|
| `moduli/m02-macro/L2.4-tassi-reali-e-inflazione-attesa.md` | Revisione di Gemini (R-001) | 2026-11-11 | consegna del rapporto e sua integrazione |
| `moduli/m02-macro/L2.5-bilancio-banca-centrale-qe-qt.md` | idem | 2026-11-11 | idem |
| `moduli/m02-macro/L2.6-fed-bce-boj-boe.md` | idem | 2026-11-11 | idem |
| `collaborazione/da-gemini/**` | Materiali di Gemini: Claude non li modifica mai (D-11) | sempre | — |

## In corso
| Attività | File coinvolti | Chi | Inizio | Fine prevista |
|---|---|---|---|---|
| Scaricamento XAUUSD da Dukascopy (Gate 2) | `dati/reali/` (dati esclusi da git) | utente, sul Mac | 2026-11-12 | fine del ciclo; poi DA-26 |
| Revisione critica indipendente di DA-26, DA-27, DA-28 e del piano di diversificazione | sola lettura; rapporto in `da-gemini/` | Gemini | alla richiesta dell'utente | — |
| Scaricamento XAUUSD dal 2005 (senza sigillo) e conteggio dei buchi per anno, per decidere DA-26 | `dati/reali/` (dati esclusi da git) | utente, sul Mac | dopo il merge | — |
| Estensione dello scaricatore a più strumenti (fase D1) | `dati/pipeline/dukascopy.py`, `dati/tests/` | Claude | dopo DA-26 e DA-27 | — |

## Sospese (D-10)
| Attività | Chi |
|---|---|
| Traccia 10.1 (statistica) | Claude |
| Generatore del manuale HTML (S3-bis) | Claude |
| Unità 2.2–2.3, correzioni v1 (S5), lab event study (S3) | Claude |
| Migrazione in un repository autonomo | — (D-02 sospesa) |

## Concluse
| Attività | Chi | Data | Esito |
|---|---|---|---|
| Correzione del DSR, partizione per date, controlli dei dati (ramo `fix/dsr-e-partizione-date`) e revisioni di Gemini G-20261113-01…04 | Claude e Gemini | 2026-11-13 | merge su main autorizzato dall'utente, commit `8ba5373`; aperti G3-05, G3-07, G4-01 |
| Sprint S1 | Claude | 2026-11-11 | commit `fbb5256` |
| Sprint S2 | Claude | 2026-11-11 | commit `9cbcca4` |
| Preparazione della prima revisione reciproca | Claude | 2026-11-11 | vedi REGISTRO-MODIFICHE |
