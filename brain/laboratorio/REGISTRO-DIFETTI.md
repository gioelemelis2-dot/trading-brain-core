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
| 23 | 15/11 | `esecuzione/esegui_h002.py` | codice | critica | P1: la verifica accettava varianti bocciate o mai provate in sviluppo | Gemini (R10) | **replica e sonde** |
| 24 | 15/11 | `esegui_h002.py` | codice | critica | P2: chiamate separate per variante svuotavano V del DSR (Gemini: DSR 0,07 → 0,99999 su un caso costruito) | Gemini (R10) | sonde |
| 25 | 15/11 | `esegui_h002.py` | codice | critica | P3: il programma girava con un sigillo da N = 1 | Gemini (R10) | sonde |
| 26 | 15/11 | `esegui_h002.py`, `criteri.py` | codice | critica | P4: anni senza trade ignorati e ultimi 5 anni contati dall'ultimo trade (verifica più indulgente) | Gemini (R10) | sonde |
| 27 | 15/11 | `esegui_h002.py` | codice | critica | P5: confronto casuale su giorni diversi da quelli della strategia (falso positivo possibile) | Gemini (R10) | sonde |
| 28 | 15/11 | `esegui_h002.py` | codice | importante | P6: cache vuota o sbagliata bruciava l'unica verifica | Gemini (R10) | sonde |
| 29 | 15/11 | `caricatore.py` | codice | importante | P7: embargo 1–14/11/2023 leggibile in verifica | Gemini (R10) | sonde |
| 30 | 15/11 | `sigillo.py` | codice | importante | P8: scritture concorrenti nel registro senza blocco; il test di Claude ha mostrato esecuzioni **perse** | Gemini (R10), confermato da Claude | test con 4 fili |
| 31 | 15/11 | `test_esecuzione.py`, `test_esegui_h002.py` | test | importante | 5 mutanti di Gemini sopravvissuti (V senza le altre promosse; confini di R medio, drawdown, 1/(T−1), ultimi 5 anni) | Gemini (R10) | mutanti nuovi |
| 32 | 15/11 | `test_esegui_h002.py` | test | minore | Test P4 di Claude troppo debole (2010 negativo: non distingueva 0 da 1/3), mutante E16 sopravvissuto | Claude | mutation testing |
| 33 | 15/11 | `criteri.py`, `esegui_h002.py` | codice | critica | R11-S1: verifica promossa con 2 trade; finestra di verifica scelta a mano | Gemini (R11) | sonde |
| 34 | 15/11 | `caricatore.py`, `esegui_h002.py` | codice | critica | R11-S2: file vuoti nei giorni feriali aggiravano il controllo dei dati | Gemini (R11) | sonde |
| 35 | 15/11 | `esegui_h002.py` | codice | critica | R11-S3: ripetizioni e seme liberi e non registrati | Gemini (R11) | sonde |
| 36 | 15/11 | `esegui_h002.py` | codice | importante | R11-S4: rapporto non scrivibile bruciava la verifica; esito non registrato | Gemini (R11) | sonde |
| 37 | 15/11 | `criteri.py` | codice | importante | R11-S5: copertura dei confronti non vincolante | Gemini (R11) | sonde |
| 38 | 15/11 | `esegui_h002.py` | codice | importante | R11-S6: cache diversa fra sviluppo e verifica; `anni=None` nell'API | Gemini (R11) | sonde |
| 39 | 15/11 | `sigillo.py` | codice | minore | R11-S7: varianti fuori dal sigillo accettate nel registro | Gemini (R11) | sonde |
| 40 | 15/11 | test del programma dei criteri | test | importante | 7 mutanti di Gemini (MR01–MR07) sopravvissuti | Gemini (R11) | mutanti nuovi |

## Lettura (aggiornata al 15/11/2026, dopo R10)
| Componente | Critici | Importanti | Minori | Ultimo giro |
|---|---|---|---|---|
| Dati, DSR, sigillo dei dati (#1–#7) | 3 | 3 | 1 | 13/11 |
| Studi (#8) | 1 | — | — | 14/11 |
| Simulatore di H-002 (#9–#18, #20–#22) | 3 | 5 | 4 | 15/11: 1 importante, 2 minori; replica di Gemini 30/30 dopo la correzione |
| Programma dei criteri e sigillo (#19, #23–#40) | **8** | 8 | 3 | 15/11: primo giro 5 critici, secondo giro (R11) 3 critici |

- **Correzione di quanto scritto prima:** il 15/11 avevo scritto «dal 15/11 nessun difetto critico». Valeva per il simulatore, non per il programma dei criteri. Scritto in una notte, al primo giro di revisione ha avuto **5 difetti critici**. Tutti erano nei collegamenti fra le parti (registro, sviluppo, verifica, riga di comando), non nei calcoli dei singoli criteri: la replica di Gemini dei calcoli coincide a 0.
- **Il simulatore converge:** dopo tre giri i difetti si sono spostati dal centro ai bordi, e la replica indipendente coincide al 100%.
- **Dopo R11:** il secondo giro ha trovato altri 3 critici, sempre nei collegamenti. Claude ha cambiato approccio: non più un buco alla volta, ma **nessuna scelta libera** nella riga di comando, e **codice sigillato** con le impronte. Il terzo giro dirà se basta.
- **Il programma dei criteri NON ha ancora mostrato convergenza:** servono altri giri. Per la regola d'uscita (proposta v3.2, §C) ne servono due di fila senza difetti critici o importanti.
- **Il controllo più efficace** resta la replica indipendente con sonde mirate (#20–#30). Test e mutanti scritti dall'autore non hanno visto i difetti nei collegamenti.
- **Contromisure prese:**
  - test strutturali (taglio dei dati, simmetria);
  - replica come cancello fisso;
  - casi d'oro;
  - controlli di coerenza nella riga di comando (sigillo, sviluppo, verifica, completezza dei dati), ognuno con il suo mutante.
