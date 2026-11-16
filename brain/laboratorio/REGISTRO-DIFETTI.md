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
| 41 | 14/11 | processo di collaborazione | processo | **critica** | H-002 eseguita sui dati veri dello sviluppo prima del sigillo (analisi di Gemini, in risposta a un punto «DGS-03» la cui origine è da verificare); modifiche di Gemini ai file di Claude su un ramo di proposta. Nessun blocco tecnico l'ha impedito: gli script di Gemini usano il caricatore in modalità «sviluppo», che non richiede il sigillo | Claude, controllando i rami il 15/11 | lettura dei rami (non dei risultati) |
| 42 | 14/11 | scheda H-002 v3.1 §4.4 e `orb_londra.py` | scheda + codice | **critica** | Uscita di fine sessione senza quotazioni in [16:30, 16:45): si usa la chiusura precedente alle 16:30, scelta in base all'assenza di quotazioni successive (sguardo al futuro nella regola) | DGS (DGS-03) | lettura della scheda, controesempio con due percorsi |
| 43 | 13/11–15/11 | pacchetto per i revisori | processo | importante | «Nessun dato personale» dichiarato da Claude dopo aver controllato solo email e stipendio: nel pacchetto c'erano nome, utente GitHub e percorsi del Mac | DGS (DGS-10), conteggio dell'utente | ricerca nel pacchetto |
| 44 | 14/11 | `H-002-REVISIONI.md` R2/R4 | documentazione | minore | SR₀ del DSR presentato come soglia dello Sharpe osservato | DGS (DGS-01 §4.1) | ricalcolo |
| 45 | 15/11 | `scarica_cache.py` | codice + test | importante | `richiesta=DK.richiesta_http` fissata alla definizione: la sostituzione nel test della riga di comando non arrivava e il test faceva una richiesta **vera** a Dukascopy (scoperto perché il test si è bloccato). Il test ora verifica che la risposta finta sia stata usata; i test di questo modulo si fanno girare con la rete bloccata | Claude, durante il TDD | blocco del test |
| 46 | 15/11 | `scarica_cache.py` | progetto | importante | Fermo al primo errore HTTP sconosciuto: un solo giorno rifiutato (ASK, 01/01/2005) avrebbe bloccato per sempre lo scaricamento. Aggiunta `--continua-su-http` (giorno registrato e lasciato mancante, fermo dopo 20 errori di fila, codice 5) | utente, dal controllo della cache sul Mac | uso reale |
| 47 | 16/11 | `scarica_cache.py` | codice | importante | Scrittura «forzata su disco» con `os.fsync`, che su macOS lascia i dati nella cache del disco, e senza forzare la cartella dopo lo spostamento: allo spegnimento improvviso del Mac del 16/11 sono spariti **20 giorni** già scaricati (riscaricati alla ripartenza). Corretto con `F_FULLFSYNC` (ripiego su fsync) e forzatura della cartella; mutanti W21–W24. Rischio residuo: un file sopravvissuto vuoto o rovinato; lo rileva `controlla_cache` a fine scaricamento | utente (log dopo lo spegnimento), letto da Claude | confronto fra log prima e dopo |
| 48 | 16/11 | `esegui_h002.py`, `caricatore.py` | codice | importante | R12bis-A3-01: 14 moduli `brain.*` eseguiti fuori da `FILE_CODICE` (anche `esecuzione/__init__.py`): codice cambiato senza che il sigillo se ne accorga; mutante MC05 (togliere `criteri.py` dall'elenco) vivo | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 49 | 16/11 | `caricatore.py` | codice | importante | R12bis-A3-02: un giorno conta «non vuoto» con un solo minuto: dati quasi vuoti passano il controllo e brucerebbero la verifica con 0 trade | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 50 | 16/11 | `caricatore.py` | codice | minore | R12bis-A3-03: festività spostate (26/12, 2/1, 24/12 quando cadono nel fine settimana) non sono chiusure note: verifica bloccata (dalla parte sicura) se Dukascopy non quota | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 51 | 16/11 | `sigillo.py` | codice | importante | R12bis-A3-04: il registro delle prove si modifica a mano (N ridotto, «promossa» cambiata, verifica cancellata e rifatta) senza che nulla se ne accorga; varianti con suffissi qualsiasi; `--ora` non controllata. Limite già dichiarato («il blocco tecnico ferma solo l'uso accidentale») | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 52 | 16/11 | `dukascopy.py` | codice | importante | R12bis-B-01: `Retry-After` in forma di data fa cadere il programma (ValueError) | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 53 | 16/11 | `scarica_cache.py` | codice | importante | R12bis-B-02: file in cache senza riga di registro dopo un'interruzione; un file rovinato già in cache è saltato come «in cache» senza controllo | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 54 | 16/11 | `dukascopy.py`, `scarica_cache.py` | codice | minore | R12bis-B-03: HTTP 204 registrato come «vuoto-200»; `--pausa` negativa fa cadere il programma invece di dare codice 2 | Gemini (R12-bis) | sonde |
| 55 | 16/11 | `scarica_cache.py` | codice | minore | R12bis-B-05: un giorno salvato vuoto per un 404 non si riscarica mai | Gemini (R12-bis) | sonde |
| 56 | 16/11 | `riconta.py` | codice | importante | R12bis-C-01/C-02: argomenti in campi diversi (`arguments`, `params`), uscite di altri tipi, esecuzioni come `bash x.sh`, `source`, `./binario`, sottoagenti; date in altri formati (03/01/2005, 2005.01.03, 20150615, timestamp), percorsi Dukascopy senza BID/ASK, prezzi con virgola o 4 decimali: non visti | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 57 | 16/11 | `riconta.py` | codice | importante | R12bis-C-03: per le chiamate sensibili stampa fino a 140 caratteri dell'argomento, contenuti di file e prezzi non mascherati compresi | Gemini (R12-bis) | sonde, riprodotte da Claude |
| 58 | 16/11 | `dukascopy.py` | codice | importante | Impostazioni predefinite di `richiesta_http` (`apri`, `attesa`) fissate alla definizione: un test di Gemini (R12-bis, passo 13) ha fatto per errore una richiesta vera a Dukascopy (giorno dello sviluppo, 2/1/2024). Stessa classe del #45 | Claude, leggendo R12-bis | dichiarazione di Gemini |
| 59 | 16/11 | script di mutanti | test | importante | Un mutante con sintassi rotta contava come «ucciso»: R06 (`mutazioni_esecuzione.py`) lo era dalle correzioni R11 (commento tagliato a metà), W08 (`mutazioni_scarica_cache.py`) dopo le correzioni della notte (indentazione). Due uccisioni finte nei conteggi dichiarati. Ora i sei script controllano che il codice mutato sia valido e segnalano «NON VALIDO»; R06 e W08 corretti | Claude, rianalizzando i mutanti dopo R12-bis | controllo di sintassi su tutti i mutanti |
| 60 | 16/11 | `scarica_cache.py` | codice | importante | Nessuna protezione contro due scaricamenti sulla stessa cartella: il 15–16/11 sul Mac ne hanno girati due insieme (il primo, creduto spento, era ancora vivo: processo 8797). Richieste raddoppiate (tentativi 3, 2, 5), un processo uscito con codice 1. Corretto con un blocco esclusivo per cartella (`.scarica.lock`): il secondo esce con codice 2 senza fare richieste. **Correzione di una conclusione di Claude:** i «20 giorni persi allo spegnimento» attribuiti al #47 sono spiegati con più probabilità dai due processi; la correzione del #47 resta come protezione, ma la prova citata non lo dimostrava | utente (`pgrep`), letto da Claude | controllo dei processi |
| 61 | 16/11 | `esegui_h002.py` | codice | importante | R13-B-01: l'ambiente può far eseguire codice non sigillato (PYTHONPATH che ombra la libreria standard, sitecustomize, .pth); le impronte leggono i file del repository, non quelli davvero caricati. `FILE_CODICE` rimasta come costante morta (MC05_OLD vivo) | Gemini (R13) | sonde, riprodotte da Claude |
| 62 | 16/11 | `sigillo.py` | codice | importante | R13-B-02: `controlla_ancora` confronta con la HEAD locale: voci aggiunte e non committate modificabili, `--amend`, HEAD staccata, altro ramo, collegamento simbolico interno passano | Gemini (R13) | sonde, riprodotte da Claude |
| 63 | 16/11 | `caricatore.py` | codice | importante | R13-B-03: la completezza guarda solo il totale della sessione: 263 minuti tutti nel pomeriggio (nessuno nel range del mattino) passano; nelle vigilie basta un minuto | Gemini (R13) | sonde, riprodotte da Claude |
| 64 | 16/11 | `riserva.py` | codice | importante | R13-C1-01: il file della riserva si manomette senza che la ricostruzione se ne accorga (testa, voci già scritte, troncamento che riapre un'autorizzazione) | Gemini (R13) | sonde, riprodotte da Claude |
| 65 | 16/11 | `riserva.py` | codice | importante | R13-C1-02: accettati m=True, N globale ≤ 0 o decrescente, impronta dei dati vuota; ripetizione tecnica dopo l'esito; quarantena sulla parte protetta senza sblocco | Gemini (R13) | sonde, riprodotte da Claude |
| 66 | 16/11 | `test_scarica_cache.py`, script di mutanti | test | importante | R13-D-01: `test_pausa_negativa_codice_2` senza risposte finte: con il mutante W35 il test va in rete (o in attesa di 20 minuti con la rete bloccata) e lo script dei mutanti cade per tempo scaduto. Gli script non bloccano la rete da soli | Gemini (R13) | mutante W35 |
| 67 | 16/11 | `scarica_cache.py` | codice | importante | R13-A-01: un 404 (o un vuoto) azzera il conteggio degli errori di fila: con tutti i feriali rifiutati e i fine settimana in 404, il fermo dopo 20 di fila non scatta mai. **Claude aveva respinto B-04 (R12-bis) a torto** | Gemini (R12-bis e R13) | controprova su 60 giorni |
| 68 | 16/11 | `riconta.py` | codice | minore | R13-A-02: date compatte (20150615) non viste se vicine a un punto | Gemini (R13) | sonde |
| 69 | 16/11 | `sigillo.py`, `esegui_h002.py` | codice | minore | R13-B-06: nomi delle prove di robustezza liberi nel registro | Gemini (R13) | sonde |
| 70 | 16/11 | `potenza_soglia.py` | codice + test | minore | R13-C2-01: nessun controllo del dominio (mu, n = 1, sigma = 0, potenza = 1); mutante MPS04 (varianza con n invece di n − 1) vivo | Gemini (R13) | sonde e mutanti |
| 71 | 16/11 | test dell'ancora, della completezza e della potenza | test | importante | 6 mutanti vivi nella prima corsa dopo le correzioni R13 (N06, N07, N15, N24, N26, P12): ogni scenario era «coperto» da un ALTRO controllo che scattava per caso nello stesso test (es. HEAD staccata presa dal controllo del ramo remoto, potenza fuori dominio presa da uno StatisticsError). I test ora pretendono il messaggio del controllo giusto e scenari in cui scatta da solo | Claude, corsa dei mutanti del 16/11 sera | mutanti 6/6 uccisi dopo |

## Lettura (aggiornata al 15/11/2026, dopo R10)
| Componente | Critici | Importanti | Minori | Ultimo giro |
|---|---|---|---|---|
| Dati, DSR, sigillo dei dati (#1–#7) | 3 | 3 | 1 | 13/11 |
| Studi (#8) | 1 | — | — | 14/11 |
| Simulatore di H-002 (#9–#18, #20–#22) | 3 | 5 | 4 | 15/11: 1 importante, 2 minori; replica di Gemini 30/30 dopo la correzione |
| Programma dei criteri e sigillo (#19, #23–#40) | **8** | 8 | 3 | 15/11: primo giro 5 critici, secondo giro (R11) 3 critici |
| Processo di collaborazione (#41) | **1** | — | — | 14/11: esecuzione sui dati veri prima del sigillo |

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
