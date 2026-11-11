# 07 · Priorità di sviluppo per i prossimi tre mesi (proposta)

Audit AUDIT-ARCH-20261111 · Periodo indicativo: 12 settimane dalla chiusura del ciclo di revisione V2.
**Proposta da approvare**: sostituirebbe la roadmap sospesa di `piano/PIANO-ESPANSIONE.md`.

## Principio guida
Prima **consolidare e verificare** ciò che esiste, poi costruire le **fondamenta della ricerca** (metodo, dati, esecuzione), e solo dopo **backtest e strategie**. Il **Guardian consultivo** procede in parallelo perché protegge già il trading discrezionale.

## Mese 1 · Consolidamento e fondamenta (settimane 1–4)
| # | Attività | Chi | Uscita verificabile | Dipende da |
|---|---|---|---|---|
| 1.1 | Chiudere il ciclo V2: risposta di Gemini, revisione di Claude, decisione dell'utente sulla V3 | G → C → U | Rapporto conclusivo di confronto | Risposta di Gemini |
| 1.2 | Verifica di L2.1–L2.6 da parte di Gemini (R-001) e integrazione | G → C | Lezioni `verificata` o correzioni documentate | — |
| 1.3 | Inserire Master Mission e Protocollo comune; riallineare il protocollo | U → C | Differenze elencate e approvate | Testi dell'utente |
| 1.4 | Definizione condivisa del Trading Guardian e specifica G0 | C (bozza) → G (revisione) → U | Specifica approvata | Decisione 1 del documento 05 |
| 1.5 | Rulebook FTMO verificato su fonti ufficiali, con data | G (+ U per l'accesso) | Rulebook con fonte per ogni regola e test | Accesso a ftmo.com |
| 1.6 | Traccia 10.1, parte 1: inferenza, potenza, errore standard dello Sharpe, test multipli | C | 4–5 lezioni `in_verifica` con script | Sblocco dei cantieri (D-12) |
| 1.7 | Pulizia di registri e incoerenze (I-01…I-14) | C | Registri aggiornati | — |

**Cancello di fine mese:** V2 chiusa; specifica del Guardian approvata; rulebook con fonti; almeno 3 lezioni di 10.1 consegnate.

## Mese 2 · Metodo di ricerca e dati (settimane 5–8)
| # | Attività | Chi | Uscita | Dipende da |
|---|---|---|---|---|
| 2.1 | Modulo 8.1–8.3: protocollo di ricerca unico, bias dei dati, validazione temporale (walk-forward, CPCV, DSR, PBO) | C | Lezioni + esempi con soluzione esatta | 1.6 |
| 2.2 | Registro delle ipotesi (modello di scheda) e contatore delle prove | C (specifica) → G (revisione) | Modello approvato | 2.1 |
| 2.3 | Primi dati reali: una serie giornaliera e una intraday con metadati, licenza e hash | G o U (accesso) + C (controlli) | `dati/reali/` popolato o metadati + hash | Accesso ai dati |
| 2.4 | Riproduzione della tabella 0.17 sui dati reali | C | Esito per statistica: riprodotta / scostamento spiegato / non riprodotta | 2.3 o dati del vault |
| 2.5 | Motore di rischio canonico unico (fusione del duplicato D-01) con test comuni | G (codice) + C (test esatti) | Un solo motore, suite unica | 1.1 |
| 2.6 | Guardian G0: prototipo consultivo (calcolo dello stato, proiezione del rischio, journal) | G (codice) + C (test e revisione) | Prototipo su dati inseriti a mano | 1.4, 1.5, 2.5 |

**Cancello di fine mese:** protocollo e registro delle ipotesi approvati; prima serie reale validata; Guardian G0 provato su casi costruiti a mano.

## Mese 3 · Primo ciclo di ricerca completo (settimane 9–12)
| # | Attività | Chi | Uscita | Dipende da |
|---|---|---|---|---|
| 3.1 | Specifica del modello di esecuzione e casi di prova con soluzione esatta | C | Specifica + test | 2.1 |
| 3.2 | Motore di backtest di riferimento | G (codice) + C (revisione, mutazioni) | Motore che passa i casi esatti e i test contro il look-ahead | 3.1, 2.3 |
| 3.3 | **Primo studio pre-registrato**: un'ipotesi semplice e ben documentata in letteratura (es. trend following su un future liquido) per collaudare l'intera catena, **non** per trovare un edge | G e C (uno propone, l'altro revisiona) | Rapporto con esito, anche negativo | 2.2, 3.2 |
| 3.4 | STR-001 e STR-002 riformulati come ipotesi registrate | G | Schede nel registro | 2.2 |
| 3.5 | Modulo 6 (rischio di portafoglio), prime lezioni | C | Lezioni `in_verifica` | 1.6 |
| 3.6 | Guardian G0 in uso sul journal reale dell'utente (solo consultivo) | U + G + C | Rapporto d'uso di 2–4 settimane | 2.6 |

**Cancello di fine trimestre:** una catena completa ipotesi → dati → backtest → validazione → revisione → esito, documentata e riproducibile. **Nessuna operatività reale automatizzata.**

## Rischi del piano
| Rischio | Probabilità | Effetto | Mitigazione |
|---|---|---|---|
| Accesso ai dati reali bloccato | alta | Mese 2–3 in ritardo | Decidere presto: abilitazione di rete, dati dell'utente o pipeline nell'ambiente di Gemini |
| Regole FTMO non verificabili ufficialmente | media | Guardian e Studio 01 condizionati | Lavorare con regole parametriche dichiarate come ipotesi |
| Duplicazione Claude–Gemini | media | Spreco, incoerenze | LOCK, ripartizione approvata, revisione incrociata |
| Overfitting nel Discovery Lab | alta senza contromisure | Falsi edge | Registro delle ipotesi, contatore delle prove, fuori campione bloccato |
| Lezioni mai verificate (C → V) | alta | Brain non affidabile | Piano C → V per priorità d'uso |
| Pressione verso l'operatività reale | media | Rischio finanziario | Cancelli e autorizzazione scritta (STANDARD §6) |
| Perdita di continuità tra sessioni | media | Lavoro ripetuto | Checkpoint e `CONTINUITA.md` a ogni tappa |

## Decisioni che spettano all'utente
1. Approvare il piano (o le priorità diverse) e sbloccare i cantieri sospesi da D-12.
2. Decidere l'accesso ai dati reali.
3. Confermare la definizione del Guardian e lo strato `laboratori/`.
4. Fornire i testi fondativi.
