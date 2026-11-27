# Casi d'accettazione dell'ultimo lotto · DGS-21 con le rettifiche di DGS-22 · 27/11/2026

**Fonti:**
- `collaborazione/da-chatgpt/DGS-20261126-21-casi-accettazione-e-tolleranze-D2.md` (casi e lettere di risposta);
- `DGS-20261127-22-riscontro-Gemini-per-Claude.md` (rettifiche).

La revisione preparatoria di Gemini, a cui DGS-22 risponde, **non è nel repository**: la conosco solo attraverso DGS-22.

**Come leggere la colonna «Codice attuale».** Indica il commit, la prova disponibile e lo stato:
- **conforme:** l'atteso è osservato da un test o da una sonda;
- **scarto:** il comportamento è diverso dall'atteso, ed è provato;
- **da provare:** manca la prova;
- **aperto:** non è implementato.

«Sonde r20» indica le sonde di chiusura di Gemini rieseguite da me sul codice `0c28299` (`ricevute/2026-11-26-verifica-r19/VERIFICA-SONDE-CHIUSURA.md`). **Nulla qui sostituisce la ricevuta sul candidato congelato**, che deve osservare ogni riga dal processo reale.

## 0. Rettifica numerica di DGS-22, da applicare subito

- Per la prima apertura di P1 con una variante, la spesa è **0,025 = 1/40**, non 0,05: l'atteso `alfa_speso = 0.05` riferito a Gemini è **sbagliato**.
- Le 1.489 date consumate sono i giorni di calendario dal 04/01/2010 al 31/01/2014 inclusi.

[CALCOLATO qui] `(date(2014,1,31) − date(2010,1,4)).days + 1 = 1489`. La quota dal registro, `RV.quota(0.05, 1, 1)`, vale `0.025`: test `TestQuotaEsatta` (`29750b5`) e V-149 delle sonde r20.

## 1. Lettere di risposta (DGS-21) e codici d'uscita attuali

**DGS-22 ritira** la proposta di codice 0 per I e Q: si congela l'interfaccia esistente, dopo averla verificata. Il codice attuale si legge da `esegui_verifica.main`:
- `ValueError` o `NonSigillata` → **2**;
- esito tecnico «completata» o «rapporto rigenerato» → **0**;
- ogni altro esito tecnico («file difforme», «rifiutata per quota») → **3**.

| Lettera | Atteso (DGS-21, con le rettifiche di DGS-22) | Codice attuale | Stato |
|---|---|---|---|
| P | 0, completata, promossa; S, V, E; letture (1,1) | 0 | **conforme** (`test_percorso_ordinario_promossa`; V-143…V-149) |
| F | 2, fermo preliminare con causa; niente scritto; (0,0) | 2 | **conforme** nei casi provati (righe sotto) |
| G | 2, tentativo con causa e istantanea; S; (1,0); P1 aperta | 2 | **conforme** (`test_giorno_omesso_nel_registro_dello_scaricamento`, `23eab88`; S-147a/b) |
| A, W, C | attesa di conferma / ripresa sospesa / conferma | — | **aperto** (D-55 non è implementato) |
| I | errore nei dati, verdetto «non decidibile», consumo conservato | **3** («file difforme») | **da congelare**: DGS-22 chiede di tenere il codice esistente; ricevuta dal processo reale da fare |
| T | 2, fermo per ambiente dopo la lettura e prima dell'esito; S e V, nessuna E; (1,1) | 2 | **conforme** (`test_ambiente_ricontrollato_prima_dell_esito`, `096de07`; S-146b) |
| R | 0, rapporto rigenerato con byte identici; (0,0) | 0 | **conforme** (`test_ripresa_dopo_il_verdetto_senza_rileggere`; V-145, V-146) |
| Q | rifiuto durevole per quota, nessuna apertura | **3** («rifiutata per quota») | **da congelare**, come I |

Il nome di uno stato, da solo, non prova la compatibilità della riga di comando (DGS-22). Per ogni esito serve una ricevuta dal processo reale, con codice, stato tecnico e verdetto.

## 2. Requisito 1 · D-55, pubblicazione e testimone

**Opzione proposta: (ii).** È una decisione del titolare (D-55), ancora da prendere.

**Rettifiche di DGS-22:**
- la conferma persa va separata dalla storia divergente;
- nella sequenza valida, l'autorizzazione è già pubblicata quando il testimone la conferma;
- un testimone più avanti del remoto è un'incoerenza da riconciliare;
- l'istante originale dell'autorizzazione si conserva, e il tempo del nuovo tentativo si registra a parte.

| Caso | Atteso | Codice attuale |
|---|---|---|
| Conferma persa e ripresa A → C → R | Una sola autorizzazione per P1, una spesa di 0,025, la stessa impronta, un solo esito. Incrementi del caricatore: A (1,0), C (0,1), R (0,0). Per C da una copia nuova serve uno screening completo, durevole e legato all'impegno. Osservare gli accessi effettivi ai dati: una chiamata al caricatore può aprire più file | **aperto** |
| Storia incompatibile | Nessuna lettura né nuova spesa, anche da copia nuova e con un'altra prenotazione: W per la vecchia P1, F per una richiesta nuova | In parte: il rifiuto per storia divergente c'è già (#145, `7edaa2a`; S-145). Il testimone è **aperto** |
| Conferme concorrenti a turni fissati | Il secondo lavoratore trova il record completo e rigenera il rapporto senza accedere ai dati | **aperto** (manca il testimone). Per la rigenerazione senza letture vedi R |

## 3. Requisiti 12–18

| Req. | Caso (DGS-21, con le rettifiche di DGS-22) | Atteso | Codice attuale |
|---|---|---|---|
| 12 · #143 | `--scheda PERCORSO` e `--scheda=PERCORSO`, anche con gli argomenti in ordine diverso | P, stesso oggetto logico | **conforme** per le due forme (`test_forma_con_uguale_accettata`, `test_positivo_completo_dal_lanciatore`, `f38f938`; S-143 c, V-143). L'ordine diverso è **da provare** |
| 12 | `--scheda` ripetuta, anche con lo stesso valore; opzione abbreviata | F «argomenti» | **conforme** (`test_doppia_scheda…`, `test_abbreviazione…`, `TestOpzioniDellEsecutore`; S-143 a) |
| 12 | **Un'altra opzione ripetuta** (`--registro`, `--ora`, …) | F «argomenti» | **scarto, #153:** l'esecutore usa in silenzio l'ultimo valore (provato il 27/11: `--registro A --registro B` → usa B) |
| 12 | Argomento posizionale inatteso; opzione obbligatoria assente o vuota | F | Assente o posizionale: errore di `argparse`, **codice 2**, da provare dal processo. Vuota: `--ora ""` → F (#146 c); `--prenotazione ""` → «sconosciuta», 2 (solo letto nel codice). **Da provare** riga per riga |
| 12 | Sigillo senza uno dei moduli obbligatori; identità della scheda diversa | F «sigillo incompleto» / «identità difforme», codice applicativo non avviato | **conforme** (`test_sigillo_senza_esegui_verifica…`, `TestIdentitaDellaScheda`; S-143 b). Per attestare il lanciatore stesso serve una base di fiducia esterna: **aperto**, D-54 |
| 13 · #144 | Anomalia già nel catalogo (feriale vuoto, assente o incompleto; 20 feriali vuoti) | G, nessuna coppia di verifica | **aperto** (#144; S-144: oggi «promossa») |
| 13 | Lacuna vista solo nei dati, dopo il consumo | Data e causa registrate, consumo conservato. **Rettifica DGS-22:** senza un veto accertato, «non decidibile»; con un veto accertato e indipendente dalla lacuna, «bocciata per veto» (precedenza di D-35), con la lacuna nel rapporto. Se la lacuna tocca il blocco decisivo, il veto non è accertato | **aperto** |
| 13 | Sedute davvero senza operazioni (**rettifica DGS-22**) | Congelare il calendario e i dati indispensabili (due lati, date accessorie). Provare separatamente: lacuna nell'intervallo d'apertura, su un solo lato, nel periodo storico del segnale. Una data accessoria difettosa identifica anche le sedute che rende non valutabili. Solo una seduta valutabile senza segnali dà (0,0), allineata con l'elenco impegnato | **aperto** (V-144 prova solo il caso pulito con sedute neutre) |
| 14 · #145 | Ipotesi/variante già verificata nella storia; budget diverso da D-38; testa incompatibile; date già consumate altrove; storia non riconciliabile | F, prima della quota, dello screening e della spesa | **conforme** (`TestAncoraEStoria`, `TestAlfaTotale`, `7edaa2a`; S-145 a/b) |
| 14 | **Una sola data** già consumata nella finestra proposta, anche con un'altra prenotazione (DGS-22) | F | La regola è un'intersezione inclusiva degli intervalli (codice letto il 27/11), quindi basta un giorno. **Manca il test con un solo giorno in comune: da aggiungere** |
| 14 | Concorrenza sulla stessa chiave, a turni fissati | Un solo vincitore; il perdente ha codice 2, nessuna nuova autorizzazione, nessuna V né E, nessuna lettura dal ricontrollo | In parte: unicità sotto il blocco (#139, PR12/PR13) e `test_due_richieste_una_sola_apertura_alla_quota`. Il caso esatto a turni fissati è **da provare** |
| 15 · #146 | Ora impossibile; soglia non finita; ipotesi vuota o fatta di spazi | F, nessuna scrittura di sviluppo | **conforme** (`TestRegressioniR1906`, `096de07`; S-146c/d/e) |
| 15 | Ambiente cambiato dopo la lettura / ripresa in ambiente incompatibile | T / F senza rigenerare; ripristinato l'ambiente, R | **conforme** (`test_ambiente_ricontrollato_prima_dell_esito`, `…alla_ripresa`; S-146b) |
| 15 | Fuso (**rettifica DGS-22**): fuso locale del processo e calendario di Londra sono due proprietà distinte. Per il calendario serve un oracolo indipendente sugli istanti UTC e sulle date di seduta ai confini dell'ora legale | Profilo ammesso: stessi istanti, seduta giusta. Profilo errato: fermo prima dell'autorizzazione | Fermo con tzdata errato: **conforme** (`test_fuso_alterato_*`; S-146a). Fuso locale del processo (`TZ=America/New_York`) senza effetto: **osservato** (S-146a). **Manca l'oracolo esplicito** (27/03/2026 08:00 UTC e 30/03 07:00 UTC = 08:00 locali; 29/03 23:30 UTC = 30/03 locale): **da aggiungere** |
| 15 | Inversione del verdetto in S-146a ([NON VERIFICATO] per DGS-22) | — | **Riprodotta da me** sul commit `7f35740`: stessa impronta dell'impegno, «promossa» +0,5363 contro «bocciata» −0,2796. Log: `ricevute/2026-11-26-verifica-r19/log/sonde_chiusura_gemini_su_7f35740_py313.jsonl`, commit `b906018` |
| 16 · #147 | Nel catalogo di verifica: dominio estraneo, data dell'URL diversa, impronta vuota, di lunghezza errata o non esadecimale, ciascuno da solo | G | **conforme** (`test_manifesto`, `898b0aa`; S-147a/b) |
| 16 | **Controlli di provenienza su entrambi i cataloghi** (DGS-22): un catalogo di sviluppo invalido ferma prima di S e delle letture | F prima di S | La funzione è la stessa per i due cataloghi. Il fermo dello sviluppo prima di S per anomalie è provato (`test_registro_dello_scaricamento_dello_sviluppo_con_anomalie`). **Manca un test con URL o impronta non validi proprio nello sviluppo: da aggiungere** |
| 16 | Convenzione delle date nell'URL (mese contato da 0) | Verificata sulla specifica della fonte | [NON VERIFICATO] sulla fonte. **Provato solo** che l'uscita di `url_giorno` è identica in tutte le versioni dal 15/11 (v2.18) |
| 16 | Digest valido ma byte difformi alla lettura | I, «file difforme» | **conforme** nel comportamento (`test_file_difforme_dopo_l_autorizzazione`). Il codice è 3: da congelare (§1) |
| 17 · #148 | Destinazione già cartella o genitore indisponibile | F | **conforme** (`test_rapporto_cartella…`, `29750b5`; S-148) |
| 17 | **Errore tardivo di consegna**, dopo record ed esito durevoli | 2 «rapporto non consegnato», consumo ed esito conservati, nessun rapporto parziale; riparata la destinazione, R | **scarto, #152:** record, esito, S, V ed E sono durevoli e la ripresa dà R con byte identici, ma il processo esce con **codice 1 e traceback** (`OSError` non catturato) e lascia un **file temporaneo orfano**. Prova: `ricevute/2026-11-27-accettazione/` |
| 18 · #149 | Budget D-38, prima apertura, una variante | P | **conforme** (V-149) |
| 18 | Prima apertura con due varianti | Q | Quota 1/80 ≠ 2,5% → «rifiutata per quota», codice 3 (`test_quota_non_collaudata…`). Il codice è da congelare (§1) |
| 18 | Budget fuori da D-38, anche con la quota che coinciderebbe | F «budget invalido» | **conforme** (`TestAlfaTotale`; S-149: «α 0,15 diverso da D-38») |

## 4. Che cosa ne segue per il lotto

**Scarti nuovi:**
- **#152:** errore tardivo di consegna del rapporto;
- **#153:** opzioni ripetute diverse da `--scheda`.

**Prove da aggiungere:**
- una sola data in comune;
- l'oracolo del fuso;
- la provenienza nel catalogo di sviluppo;
- l'ordine diverso degli argomenti;
- gli argomenti assenti o posizionali dal processo;
- la concorrenza a turni fissati.

**Aperti:**
- #144, con la precedenza del veto e le sedute valutabili;
- D-55, cioè A, W, C e il testimone;
- l'attestazione del lanciatore (D-54).

**Interfaccia:** i codici 3 per I e Q vanno congelati dopo la ricevuta dal processo reale.
