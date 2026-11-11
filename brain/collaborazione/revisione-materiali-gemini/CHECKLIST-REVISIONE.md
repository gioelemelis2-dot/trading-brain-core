# Checklist di revisione dei materiali quantitativi di Gemini

Versione 1.0 · 11/11/2026 · PROVVISORIA. Si compila una copia per ogni consegna (dentro il rapporto) segnando per ogni voce: ✅ conforme · ⚠️ con riserve · ❌ non conforme · ❓ non verificabile · n/a.

Principio: **si verifica, non si presume.** Ogni ✅ indica che cosa è stato fatto per arrivarci (comando eseguito, fonte letta, calcolo ripetuto).

---

## A · Ricezione e integrità
| Id | Controllo | Come si verifica |
|---|---|---|
| A1 | Esiste un `MANIFEST` con elenco dei file, SHA-256, data, commit di origine | Ricalcolo `sha256sum` e confronto |
| A2 | Versione di Python e dipendenze con versione esatta (es. `requirements.txt` bloccato) | Lettura; installazione in ambiente pulito |
| A3 | Semi casuali dichiarati per ogni risultato simulato | Lettura del codice e dei risultati |
| A4 | Origine e licenza di ogni dato reale usato; dati simulati marcati come tali | Metadati, `[REALE]`/`[SIMULATO]` |
| A5 | Nessun file del Brain canonico modificato dalla consegna | `git diff` del branch di Gemini limitato a `collaborazione/da-gemini/` |

## B · Riproducibilità
| Id | Controllo | Come si verifica |
|---|---|---|
| B1 | I test unitari passano in ambiente pulito | Esecuzione; numero di test passati/falliti/saltati |
| B2 | I risultati principali si riottengono identici con lo stesso seme | Riesecuzione e confronto numerico |
| B3 | Con semi diversi i risultati cambiano entro l'errore Monte Carlo atteso | 5–10 semi; dispersione vs √(p(1−p)/n) |
| B4 | Tempi di esecuzione e risorse dichiarati e realistici | Misura |

## C · Rulebook (YAML) e regole della prop firm
Le regole FTMO **non sono state verificate su ftmo.com** in questa sessione: le fonti secondarie consultate il 11/11/2026 concordano su alcuni punti (formato a 2 fasi: target 10% e 5%, perdita giornaliera massima 5%, perdita massima 10%, almeno 4 giorni di trading) e **divergono** su altri (limiti di tempo; base di calcolo del limite giornaliero; regole del formato "1-Step"). Il rulebook va quindi controllato contro le pagine ufficiali **alla data indicata nel rulebook**.

| Id | Controllo | Perché conta |
|---|---|---|
| C1 | Ogni regola ha **fonte ufficiale, data di consultazione e tipo di account** (2-Step, 1-Step, account finanziato) | Le regole cambiano e differiscono tra prodotti |
| C2 | **Base del limite giornaliero**: percentuale del capitale iniziale o del saldo di inizio giornata? Saldo o equity (P/L aperto incluso)? Commissioni e swap inclusi? | Le fonti divergono; cambia molto la probabilità di fallimento |
| C3 | **Orario di reset** del giorno (mezzanotte CE(S)T secondo le fonti) e gestione dell'ora legale | Un "giorno" sbagliato sposta le violazioni |
| C4 | **Perdita massima**: statica (dal capitale iniziale) o trailing (dal massimo, a fine giornata)? | Statica e trailing danno rischi molto diversi |
| C5 | Target, giorni minimi, limite di tempo (se esiste), regole aggiuntive (es. "best day"/consistenza, news, weekend) | Completezza |
| C6 | Il YAML ha uno **schema** validato e un test per ogni regola | Errori di battitura silenziosi |
| C7 | Le regole sono **separate dal motore** (nessun valore cablato nel codice) | Aggiornabilità |

## D · Motore quantitativo
| Id | Controllo | Come si verifica |
|---|---|---|
| D1 | **Ordine dei controlli**: le violazioni si verificano dopo ogni operazione/tick o solo a fine giornata? È coerente con C2–C4? | Lettura del codice; caso di test costruito a mano |
| D2 | **P/L aperto** (floating) e oscillazioni dentro il trade sono modellati o ignorati? Se ignorati, è dichiarato? | Codice; confronto con C2 |
| D3 | **Costi**: spread, commissioni, swap, slippage, gap oltre lo stop | Codice; sensibilità |
| D4 | **Dimensionamento**: rischio fisso in valuta o in % del capitale corrente? Arrotondamento dei lotti? | Codice |
| D5 | **Indipendenza dei trade**: assunta? Esistono correlazioni intraday o autocorrelazione degli esiti? | Codice; test sui dati |
| D6 | Condizioni al contorno: uguaglianza esatta alla barriera (≤ o <), più trade aperti contemporaneamente, ultimo giorno | Test costruiti a mano |
| D7 | Confronto con il riferimento indipendente `strumenti/riferimento_rovina.py` sui casi che entrambi possono rappresentare | Differenza entro l'errore standard (o spiegata) |

## E · Studio Monte Carlo (10.000 simulazioni)
| Id | Controllo | Note |
|---|---|---|
| E1 | **Distribuzione degli esiti dei trade**: da dove viene? Dati reali (quali, fonte), ipotesi parametriche, bootstrap di un journal? Etichettata `[REALE]`/`[SIMULATO]`/`[IPOTESI]` | È l'ipotesi che decide tutto |
| E2 | **Errore Monte Carlo**: con n = 10.000 l'errore standard di una probabilità p è √(p(1−p)/10.000), al massimo ≈ 0,5 punti percentuali; i risultati riportano intervalli di confidenza? | Differenze sotto ~1 punto tra scenari non sono distinguibili |
| E3 | **Incertezza sui parametri** (es. win rate stimato da N trade): propagata o ignorata? | Un win rate stimato da 50 trade ha errore ≈ ±14 punti (Modulo 0.14) |
| E4 | Code grasse, cambi di regime, strisce: il modello di generazione li permette? | Coerenza con Modulo 0.13 e 0.17 |
| E5 | Bootstrap semplice vs a blocchi (se c'è dipendenza) | Modulo 0.16 "Limiti" |
| E6 | Definizione di "rovina": fallimento della challenge, perdita della quota d'iscrizione, perdita di capitale proprio? | Il Brain distingue rovina operativa e finanziaria |
| E7 | Convergenza: i risultati sono stabili tra 5.000 e 10.000 (o 50.000) simulazioni? | Grafico o tabella |
| E8 | Sensibilità: rischio per trade, R:R, trade al giorno, costi, regole (C2, C4) | Tabella di scenari |

## F · Test unitari
| Id | Controllo |
|---|---|
| F1 | Coprono ogni regola del rulebook e i casi limite (barriera esatta, cambio di giorno, ora legale, gap) |
| F2 | Un test **fallirebbe** se la regola fosse implementata in modo sbagliato (prova: alterare temporaneamente la regola in una copia e verificare che il test fallisca) |
| F3 | Esistono test con risultati noti in forma chiusa (es. rovina classica) |
| F4 | I test non dipendono dalla rete, dall'orario o da dati esterni non versionati |

## G · Strategy Discovery Lab
| Id | Controllo | Riferimento nel Brain |
|---|---|---|
| G1 | Numero di varianti provate **registrato** (log delle prove), non solo la migliore | 0.3, 0.4, 0.18 (test multipli) |
| G2 | Separazione in-sample / out-of-sample decisa **prima**; walk-forward o CPCV | 0.4, Modulo 8 |
| G3 | Correzioni per test multipli (soglia t > 3, Deflated Sharpe Ratio, PBO) | 0.18, Modulo 8 |
| G4 | Costi realistici inclusi in ogni risultato | 1.13 |
| G5 | Bias dei dati: look-ahead, survivorship, dati rivisti, fusi orari | Modulo 8.2 |
| G6 | Ogni "scoperta" etichettata come **ipotesi**, con spiegazione economica e criterio di abbandono | 0.3 (5 domande), 0.4 |
| G7 | Nessuna strategia presentata come pronta per denaro reale | STANDARD §6 |

## H · Interpretazione e coerenza con il Brain
| Id | Controllo |
|---|---|
| H1 | Le conclusioni non vanno oltre le ipotesi (probabilità **condizionate** a modello e regole) |
| H2 | Coerenza con Modulo 0: strisce (0.13), campione (0.14), ergodicità/sizing (0.15), Monte Carlo (0.16), affermazione C1 sul rischio di rovina (audit) |
| H3 | Il costo atteso della challenge (quota × probabilità di fallimento ripetuto) è discusso, se rilevante |
| H4 | Nessuna promessa di rendimento, nessun invito a leva o a operatività reale |
| H5 | Collocazione proposta nell'architettura (9.4 prop firm, 6.2 rischio di rovina, Modulo 8 lab) senza duplicare contenuti esistenti |

## I · Esito per materiale
| Materiale | Riproducibile | Corretto nel merito | Ipotesi accettabili | Pronto per integrazione |
|---|---|---|---|---|
| G-MAT-1 Studio Monte Carlo | | | | |
| G-MAT-2 Motore | | | | |
| G-MAT-3 Test | | | | |
| G-MAT-4 Rulebook | | | | |
| G-MAT-5 Discovery Lab | | | | |

## Fonti consultate per preparare questa checklist (11/11/2026)
Solo fonti **secondarie** sulle regole FTMO (siti di recensione e guide; nessuna pagina di ftmo.com letta direttamente), tra cui: pineconnector.com, propfirm-escape-pod.pages.dev, thegodfunded.com, ftmo.oanda.com (FAQ ospitata), jptradingcapital.com, mql5.com. Stato: **V-sec / da verificare** sulle pagine ufficiali.
