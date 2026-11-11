# Revisione di architettura, mappa, registri e governance · domande guida

Codice `AR-xx`. Gemini può rispondere a tutte o solo ad alcune; per ciascuna: valutazione, evidenza, proposta concreta.

## Architettura e mappa
| Codice | Domanda | File |
|---|---|---|
| AR-01 | La scelta "spina 0–9 + Modulo 10 a tracce" (D-01) è la migliore? Quali alternative concrete e con quali costi di migrazione dal v1? | `architettura/ARCHITETTURA.md` §4.1 |
| AR-02 | Prerequisiti: ci sono dipendenze sbagliate o mancanti (es. la traccia 10.1 dovrebbe precedere il Modulo 2?) | `architettura/ARCHITETTURA.md` §4.4, `mappa/DIPENDENZE.md` |
| AR-03 | Aree o sottodiscipline mancanti nella mappa A–Z | `mappa/MAPPA-COMPETENZE.md` |
| AR-04 | Duplicazioni tra moduli (es. microstruttura in 1.18 e 4.1; volatilità in 1.5 e 10.5) gestite bene? | `architettura/ARCHITETTURA.md` §4.3 |
| AR-05 | Livelli di evidenza assegnati agli anelli delle catene causali: ce ne sono di sopravvalutati o sottovalutati? | `mappa/DIPENDENZE.md` §1 |
| AR-06 | Dove collocare i materiali quantitativi di Gemini (rovina FTMO, motore, rulebook, Discovery Lab) senza duplicare | `architettura/ARCHITETTURA.md` (Moduli 6, 8, 9) |

## Audit e matrice
| Codice | Domanda | File |
|---|---|---|
| AR-07 | Gli esiti dell'audit sul v1 (A1–A18, B1–B11, C1–C6) sono corretti? In particolare A7 e A9 (dichiarati errori) | `audit/02-VERIFICA-AFFERMAZIONI.md` |
| AR-08 | La matrice delle lacune sottostima o sovrastima qualche area? | `audit/03-MATRICE-LACUNE.md` |

## Registri e governance
| Codice | Domanda | File |
|---|---|---|
| AR-09 | I registri permettono davvero di sapere che cosa è studiato, verificato, incompleto, controverso, obsoleto? Che cosa manca? | `governance/REGISTRO-CONOSCENZE.md`, `REGISTRO-MODIFICHE.md` |
| AR-10 | Gli standard (F1–F7, E1–E7, V/V-sec/C/X, classi di contenuto, ciclo di vita) sono applicabili in pratica o vanno semplificati? | `governance/STANDARD.md` |
| AR-11 | Le decisioni D-01–D-11 sono coerenti tra loro e con il Master Mission (se Gemini ne ha il testo)? | `governance/DECISIONI.md` |
| AR-12 | Il protocollo operativo provvisorio è compatibile con il Protocollo comune dell'utente? Elencare ogni differenza | `collaborazione/PROTOCOLLO-OPERATIVO.md` |

## Bibliografia
| Codice | Domanda | File |
|---|---|---|
| AR-13 | Errori bibliografici (autori, anni, riviste, titoli) nelle voci C | `bibliografia/BIBLIOGRAFIA.md` |
| AR-14 | Testi o paper fondamentali mancanti per le aree A, C, F, L, M | idem |
