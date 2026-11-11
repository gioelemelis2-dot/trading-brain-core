# Bacheca delle attività (LOCK)

Leggere prima di iniziare. Regole in [`PROTOCOLLO-OPERATIVO.md`](PROTOCOLLO-OPERATIVO.md) §4 (provvisorio).

Stato generale: **SVILUPPO SOSPESO** (D-12) · Fase: **revisione indipendente di Gemini in corso** — Claude non avvia attività fino a nuova indicazione dell'utente.

**Versione di riferimento della revisione: commit `1b051df`** (le impronte in `pacchetto-per-gemini/MANIFEST.sha256` corrispondono a quel commit). I commit successivi toccano solo file di continuità e registro (`CONTINUITA.md`, `collaborazione/LOCK.md`, `governance/DECISIONI.md`, `governance/REGISTRO-MODIFICHE.md`).

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
| Revisione L2.4–L2.6, architettura e registri | sola lettura del Brain; scrittura in `da-gemini/` | Gemini | da avviare | — |
| Consegna materiali FTMO / motore / test / rulebook / Discovery Lab | `da-gemini/consegne/` | Gemini | da avviare | — |
| Revisione indipendente dei materiali di Gemini | `revisione-materiali-gemini/` | Claude | alla ricezione | — |

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
| Sprint S1 | Claude | 2026-11-11 | commit `fbb5256` |
| Sprint S2 | Claude | 2026-11-11 | commit `9cbcca4` |
| Preparazione della prima revisione reciproca | Claude | 2026-11-11 | vedi REGISTRO-MODIFICHE |
