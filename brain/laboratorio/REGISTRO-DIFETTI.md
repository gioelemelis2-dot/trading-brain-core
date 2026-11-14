# Registro dei difetti (laboratorio)

**Scopo:** vedere in numeri se il codice sta convergendo, invece di fidarsi di chi lo scrive. Ogni difetto trovato si aggiunge qui, con:
- chi l'ha trovato e come;
- la gravità, calcolata sul **peso sulle decisioni** e non sull'imbarazzo.

**Gravità:**
- **critica:** fa sembrare una strategia migliore di quanto è, guarda il futuro, o renderebbe inutile un controllo (sigillo, DSR);
- **importante:** può cambiare un verdetto in alcune configurazioni;
- **minore:** nessun effetto sui verdetti (diagnostica, messaggi, casi quasi impossibili).

**Tipo:**
- **codice:** il programma faceva una cosa diversa dalla scheda;
- **scheda:** regola mancante o sbagliata;
- **test:** il codice era giusto, ma i test non avrebbero visto un errore (mutante sopravvissuto) oppure il test stesso era sbagliato.

Fonti: `laboratorio/ipotesi/H-002-REVISIONI.md` (R1–R8), `collaborazione/da-claude/ESITI.md`, `governance/REGISTRO-MODIFICHE.md`.

## Elenco (dal più vecchio)
| # | Data | Dove | Tipo | Gravità | Difetto | Trovato da | Come |
|---|---|---|---|---|---|---|---|
| 1 | 13/11 | `backtester/dsr.py` | codice | critica | Soglia del DSR senza la scala sqrt(V): con N ≥ 2 prove bocciava qualunque strategia | Gemini (G-20261113-01) | lettura e calcolo |
| 2 | 13/11 | `dsr.py` | codice | critica | DSR con NaN in ingresso = 1,0 (G3-01) | Gemini (G-20261113-03) | revisione dura |
| 3 | 13/11 | `partizione_date.py` | codice | critica | Verifica aggirabile declassando i blocchi di verifica (G3-02) | Gemini (G-20261113-03) | revisione dura |
| 4 | 13/11 | `dukascopy.py` | codice | importante | Buchi lunghi di giorno e picchi dentro la candela non fermavano lo scaricamento (G3-03) | Gemini | revisione dura |
| 5 | 13/11 | `dukascopy.py` | codice | importante | CSV scritto prima del controllo del nonce (G3-04) | Gemini | revisione dura |
| 6 | 13/11 | `dukascopy.py` | codice | minore | Record binari non validi accettati (G3-06) | Gemini | revisione dura |
| 7 | 13/11 | `partizione_date.py` | test | importante | Mutante P14 sopravvissuto (ruoli presi dal commitment) | Claude | mutation testing |
| 8 | 14/11 | `studi/studio_range.py` | codice | critica | Distorsione di selezione nel modo «stoppino» (40,5% contro 33,3% atteso su dati casuali); range che riusava i minuti della rottura | Claude | taratura su dati casuali |
| 9 | 14/11 | `backtester/engine.py` | codice | importante | Stop delle vendite sul BID e slittamento anche sul target limite (non usato per H-002) | Gemini (R2) | lettura del codice |
| 10 | 14/11 | `simulatori/orb_londra.py` | test | critica | Primo giro dei mutanti 14/20: i test, scritti dopo il codice, non avrebbero visto 6 difetti, fra cui uno sguardo al futuro nella mediana | Claude | mutation testing |
| 11 | 14/11 | `orb_londra.py` e scheda v2 | codice + scheda | critica | Stop in salto eseguito al livello invece che all'apertura del minuto: vantaggio irreale | Gemini (R3) | revisione |
| 12 | 14/11 | `orb_londra.py` e scheda v2 | codice + scheda | importante | Uscita di fine sessione che con un buco poteva scivolare molto più tardi; ingresso ritardato senza limite | Gemini (R3) | revisione |
| 13 | 14/11 | scheda v2 | scheda | importante | Festivi inglesi mancanti; minimo dell'ampiezza fisso a 3 USD (inadatto al 2005–2012) | Gemini (R3) | revisione |
| 14 | 14/11 | `test_orb_londra.py` | test | critica | Prima stesura del test sullo spread negativo: escludeva il giorno intero (sguardo al futuro proposto dal test) | Claude | rilettura prima del commit |
| 15 | 14/11 | scheda v3 | scheda | importante | La scheda dichiarava nel simulatore controlli che non c'erano (confronto casuale, DSR, robustezza, veto) | DeepSeek (R4, B3) | revisione |
| 16 | 14/11 | `orb_londra.py` | codice | importante | Benchmark su campioni di giorni diversi | DeepSeek (R4) | revisione |
| 17 | 14/11 | `orb_londra.py` | codice | minore | Sharpe con la deviazione di popolazione; `specchio` senza direzione dava KeyError; `resoconto` senza i giorni esclusi | DeepSeek (R4) | revisione |
| 18 | 14/11 | `test_orb_londra.py` | test | minore | Errori di calcolo di Claude nei valori attesi (0,992700 invece di 0,992684; somma 4,6 invece di 7,2) | Claude e DeepSeek | esecuzione dei test |
| 19 | 15/11 | `esecuzione/esegui_h002.py` | test | minore | Mutante E12 sopravvissuto: senza `--varianti` la verifica si fermava dopo aver letto i dati sigillati | Claude | mutation testing |
| 20 | 15/11 | `orb_londra.py` | codice | importante | D1: spread di riferimento dalla fine del range invece che dalle 08:30 (solo robustezza con range di 20 e 45 minuti; poteva cambiare il veto) | Gemini (R8) | **replica indipendente** |
| 21 | 15/11 | `orb_londra.py` | codice | minore | D2: once in virgola mobile, 49 invece di 50 ai bordi interi (~1 caso ogni 200 prezzi, −2% sulla taglia di quel trade) | Gemini (R8) | **replica indipendente** |
| 22 | 15/11 | `test_orb_londra.py` | test | minore | Due valori attesi sbagliati da Claude nei test nuovi (filtro del rischio dimenticato; minimo dei costi dimenticato) | Claude | esecuzione dei test, prima del commit |

## Lettura (aggiornata al 15/11/2026)
| Periodo | Critici | Importanti | Minori | Dove stavano |
|---|---|---|---|---|
| 13/11 (dati e DSR) | 3 | 3 | 1 | controlli di base: DSR, sigillo, scaricamento |
| 14/11 (studi e simulatore, prima della v3.1) | 4 | 5 | 2 | cuore della strategia: esecuzione degli stop, sguardo al futuro, giorni |
| 15/11 (dopo la v3.1) | 0 | 1 | 3 | bordi: robustezza, arrotondamenti, diagnostica |

- **Tendenza:** dal 15/11 nessun difetto critico; quello importante tocca solo la robustezza. Va confermato dai prossimi giri: due revisioni di fila senza rilievi critici o importanti sono una condizione del sigillo (bozza v3.2, §10).
- **Il controllo più efficace** sul codice di H-002 è stato la replica indipendente (#20, #21): ha trovato ciò che test, mutanti e tre revisori in lettura non avevano visto.
- **Contromisure prese:**
  - test contro lo sguardo al futuro con il taglio dei dati e test di simmetria (`TestStrutturali`);
  - replica di Gemini come cancello fisso prima del sigillo;
  - casi d'oro nella scheda (bozza v3.2).
