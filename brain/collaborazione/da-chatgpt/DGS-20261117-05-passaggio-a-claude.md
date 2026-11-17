# Passaggio a Claude · Riallineamento DGS e proposte metodologiche

17 novembre 2026 · Preparato dal DGS su richiesta del titolare.

## Prima lettura

Questo dossier raccoglie i tre documenti prodotti dal DGS, con le rettifiche e le precisazioni successive. Il titolare chiede di coordinare il loro esame con i lavori già avviati da Claude e Antigravity. Il lavoro sul codice è affidato a Claude e gli audit tecnici seguono il mandato di Antigravity.

**Priorità confermata dal titolare:** concludere le revisioni, verificare lo storico XAUUSD BID/ASK e consolidare una baseline rigorosamente validata prima di sviluppare nuove strategie o ampliare il progetto.

L'ultimo stato esaminato dal DGS è il pacchetto redatto trading_brain_dgs06.zip, attribuito a c5ca93debf1438c991eb6d480fed697e7d74bca9. Il DGS ha controllato 369/369 impronte e il fascicolo riportava 0/2 giri puliti. Questi numeri descrivono quel pacchetto. Claude deve partire dalla versione corrente di STATO-PROGETTO.md e riportare gli avanzamenti già avvenuti, evitando di riaprire attività concluse sulla base di questo riepilogo storico.

## Come leggere i documenti allegati

| Ordine | Documento | Stato e uso |
|---|---|---|
| 1 | Questa nota | Riassume le decisioni espresse in conversazione e chiarisce il mandato di coordinamento. |
| 2 | DGS-05-addendum-metodo.md, allegato B | Rettifica la raccomandazione di adottare subito le soglie P5 e precisa il limite delle prove disponibili. |
| 3 | DGS-specifica-collaudo-IA02.md, allegato C | Proposta di disegno statistico da criticare, dimensionare e collocare nella roadmap. |
| 4 | DGS-05.md, allegato A | Riallineamento storico e pareri P1–P6, da interpretare insieme alle rettifiche dell'allegato B. |

I tre allegati sono riprodotti integralmente. Il ritiro della raccomandazione sulle soglie P5 prevale sulla proposta originaria. Le formulazioni imperative nella specifica descrivono il disegno candidato del DGS; la loro adozione richiede l'esame metodologico e le decisioni del titolare.

## Punti confermati nella conversazione successiva

1. Il titolare è disposto ad aspettare più dati per avere prove più forti sul superamento di +0,15 R netto medio. Esprime quindi una preferenza per la verifica sul limite inferiore. Metodo dell'intervallo, quote e requisiti informativi restano da definire.
2. Un'operazione comprende ingresso, uscite parziali e chiusura completa. La convenzione discussa è risultato netto complessivo diviso per budget di rischio fissato prima dell'ingresso. Incrementi di posizione, rientri e altri casi ulteriori richiedono una definizione nella futura scheda.
3. I piccoli buchi possono essere tollerati soltanto con regole anticipate e motivate. Le operazioni già aperte con risultato incerto rimangono nel rendiconto. Se l'incertezza può cambiare il verdetto, la promozione attende una verifica risolutiva. L'utente ha approvato questo principio; il trattamento quantitativo resta da progettare e convalidare.
4. Il DGS segnala i problemi al titolare, che li trasmette a Claude. Il titolare ha richiesto espressamente di lasciare il codice a Claude e di proteggere documenti sigillati e riserva. Per questo dossier il DGS ha consultato solo i propri documenti già prodotti e la conversazione.

## Preferenze future, da considerare dopo la baseline

- Il percorso iniziale sarà in demo.
- Il titolare lavorerà e potrà intervenire manualmente poche volte. Preferisce un percorso tra semiautomatico e automatico.
- È disponibile a intraday e posizioni di più giorni. La scelta dipenderà da strategia, mercato, liquidità del mercato e comportamento del prezzo.
- La disponibilità oraria precisa deve ancora essere raccolta. Queste preferenze orientano la futura valutazione di compatibilità operativa. L'automazione richiederà il percorso di validazione previsto dal progetto.
- Dopo la baseline, la fase osservativa con il DGS riguarda dati dal 15/11/2023 in avanti. L'idea appartiene al titolare e data e periodo osservato si registrano prima della prova.

## Proposte ancora aperte e correzioni del DGS

| Tema | Chiarimento per Claude |
|---|---|
| Completezza P5 | Ritirata la raccomandazione di ratificare subito 99% di sedute, 98% di minuti, 95% per terzo e massimo cinque minuti di buco. Questi valori erano prudenziali, privi di validazione di adeguatezza. L'anteriorità della scelta, da sola, non basta a renderla corretta. |
| Quote di errore | Il 5% globale e la spesa decrescente del DGS-05 sono proposte da valutare. |
| Collaudo Monte Carlo | gamma=1%, obiettivo p*=a/2 e probabilità di superamento per cella 90% sono scelte proposte dal DGS. Richiedono critica, stima dei costi e confronto con alternative motivate. |
| Esiti a tre stati | Il principio di sospendere una promozione quando mancano informazioni è condiviso. La formalizzazione complessiva di DA-31 deve essere completata prima dell'adozione. |
| Prove sintetiche | Il DGS ha eseguito esempi aritmetici e un riferimento gaussiano analitico. Un intervallo HAC/bootstrap, la procedura con selezione e la gestione dei buchi restano da collaudare. |
| H-002 | Il riferimento è la decisione documentata «non decidibile · parcheggiata» con condizione d'uscita del titolare. Il DGS ha riconosciuto la propria precedente omissione nel segnalare il conflitto con la regola storica binaria. |

## Risposta richiesta a Claude

Alla ripresa, integrare la lettura con gli incarichi già autorizzati e fornire un riscontro documentale conciso:

1. Stato corrente di baseline, candidato, mutanti, revisione di Antigravity e download, distinguendo completato, in corso e ancora da verificare. Per la riserva, usare soltanto evidenze e metadati ammessi dal protocollo.
2. Per ogni proposta del DGS: accolta, accolta in parte oppure respinta, con motivo e riferimenti. Indicare eventuali errori matematici, incoerenze, duplicazioni o costi sproporzionati.
3. Segnalare quanto è già coperto dal lavoro in corso. Per i punti ulteriori, distinguere ciò che serve prima della verifica della riserva, ciò che serve alla futura H-003 e ciò che può attendere una fase successiva.
4. Proporre il più piccolo passo metodologico necessario, con evidenza di accettazione e costo atteso. Per il collaudo, stimare prima la dimensione del lavoro e discutere il margine conservativo richiesto dalla regola U≤a, che può respingere anche un metodo esattamente al livello nominale.
5. Esporre le decisioni effettivamente richieste al titolare. Le proposte numeriche del DGS restano riconoscibili come tali fino alla ratifica.

Questa consegna richiede prima il confronto e il coordinamento. Il progetto mantiene la sequenza autorizzata dal titolare. L'esecuzione di ulteriori attività segue quella sequenza e gli incarichi in vigore.

## Coordinamento con Gemini / Antigravity

**Valutazione del DGS:** al momento è sufficiente il passaggio a Claude. Antigravity ha già un ruolo tecnico nel ciclo di revisione. Un secondo incarico metodologico parallelo rischierebbe di duplicare lavoro e valutare un candidato ancora in movimento.

Claude riporta quale mandato di Antigravity sia effettivamente attivo e a quale commit si riferisca. Se il piano metodologico, dopo il confronto, richiederà replica indipendente, il titolare potrà assegnare un incarico delimitato con versione, oggetto, input consentiti e risultato atteso. L'attuale dossier serve a preparare quella decisione.

## Limiti della consegna

Lo stato corrente del repository e dei processi sul Mac è noto a Claude e al titolare. Questo dossier riprende il checkpoint già esaminato dal DGS e documenta la discussione successiva. I calcoli precedenti restano attribuiti al DGS, con le ipotesi riportate negli allegati. Nessuno di essi costituisce una promozione di strategia o una certificazione universale del metodo. La fattibilità e la priorità delle nuove proposte devono essere confrontate con il lavoro reale già in corso.


---

# Allegato A · DGS-05 originale

# DGS-05 · Riallineamento del Trading Brain

17 novembre 2026 · Parere per il titolare · Pacchetto trading_brain_dgs06.zip

**Il banco resta a 0 giri puliti su 2. Nessuna apertura del Gate 4.** La ripresa parte da STATO-PROGETTO.md. La scheda riporta ancora «R14 pronto» nella lista delle prossime azioni. La voce v1.49 del registro modifiche documenta che R14 è già stato integrato e il registro difetti precisa quali correzioni sono parziali.

## Integrità

Ho verificato direttamente nello ZIP **369/369** SHA-256 della colonna sha256 e le dimensioni corrispondenti. I 371 membri comprendono LEGGIMI-PACCHETTO.md e MANIFEST.tsv, fuori dalle righe del manifest. Ho contato 29 voci marcate come redatte e 340 come invariate. Nessun duplicato. CRC riuscito, tutti i membri decodificabili in UTF-8 e i due ZIP dichiarati esclusi sono assenti.

Commit dichiarato dal LEGGIMI: `c5ca93debf1438c991eb6d480fed697e7d74bca9`. Il controllo dimostra la corrispondenza interna tra archivio e manifest. L'attribuzione alla cronologia Git, la completezza rispetto al repository e l'assenza di ogni dato personale rimangono fuori dal riscontro.

SHA-256 dello ZIP: `58d294292ffdceb9b931b64a5bb75bdcc0408d9efc0699fca78791a9e29af9a5`.

## Riscontro dei cinque punti

| Punto | Giudizio | Evidenza e limite |
|---|---|---|
| **1. Revisione tecnica** | **Verificato. In disaccordo con una lettura di «corretto» come chiusura indipendente.** | Ho ricontato **104** voci, **24 critiche**, 55 importanti e 25 minori. R12-bis, R13, BANCO-02, R14 e i due filoni di revisione separati risultano dal fascicolo. R14 di Gemini sulla base `6b1b136` riporta un critico e quattro importanti. #96 documenta la correzione del critico. #98 è segnato «corretto in parte». La corsa completa dei mutanti sul candidato finale risulta in corso. **0/2** giri puliti. Fonti: STATO-PROGETTO.md righe 8–17, REGISTRO-MODIFICHE.md v1.38–v1.49, REGISTRO-DIFETTI.md righe 107–125, G-20261117-R14.md righe 3–26 e 131–135. |
| **2. Decisioni del titolare** | **Verificato nei registri.** | H-002 è «non decidibile · parcheggiata». La condizione d'uscita richiede dati successivi al 12/11/2026, scheda sigillata prima di vederli e conteggio in N. IA-02 registra **+0,15 R netto per trade** per H-003 e successive. L'anteriorità è attestata nei documenti con riferimento a `032250b`. Cronologia Git e conversazione originaria non sono verificabili da questo ZIP. DA-19 esclude la robustezza da N solo come veto fisso. D-24 è attiva. Fonti: H-002-REVISIONI.md righe 373–383, IMPEGNI-ANTICIPATI.md righe 14–30, DECISIONI-APERTE.md righe 216–223, DECISIONI.md riga 30. |
| **3. Riserva 01/01/2005–31/10/2023** | **Verificato come esito documentato. Non verificabile come assoluto.** | Il riconteggio riporta **428 file, 2.583 esecuzioni, 112 segnalazioni** classificate e nessuna uscita attribuita alla cache vera della riserva. Il legame tra chiamata e uscita è euristico. Le letture manuali o fuori dalle trascrizioni restano non osservabili. #80 segnala inoltre che prezzi isolati sopra 1.900 e privi di date possono sfuggire al filtro specifico, anche dentro le trascrizioni. Le esecuzioni sulla cache di sviluppo, compreso #41, rientrano in un perimetro distinto. Fonti: RICONTEGGIO-20261117.md righe 3–30, G-20261115-03-censimento-esecuzioni.md §§1–2, 5, 7–8. |
| **4. Storico XAUUSD** | **Verificato come stato riportato. Copertura effettiva non verificabile.** | La scheda riporta sviluppo BID/ASK completo dal 15/11/2023 al 12/11/2026, BID storico completo fino all'11/02/2020 e in scaricamento dal 12/02/2020, ASK avviato dal 2005. I 121 giorni con dati ASK riportati fino al 01/05/2005 documentano l'esistenza iniziale. Il consuntivo manca. La causa dell'arresto specifico al 2020 non è attestata nei passaggi letti. Per l'episodio dei venti giorni, v1.42 rettifica l'attribuzione iniziale al riavvio e indica come più probabili due processi concorrenti. Fonti: STATO-PROGETTO.md righe 18–25 e 51, REGISTRO-MODIFICHE.md v1.39, v1.42 e v1.45. |
| **5. Incidenti #41 e #72** | **Verificato per gli incidenti registrati. Mancata spedizione del vecchio ZIP non verificabile.** | #41 è un'esecuzione su dati veri di sviluppo prima del sigillo, registrata come E-003. I tagli pertinenti entrano in N per le ipotesi che li usano. Un registro sigillato vuoto può quindi coesistere con prove selezionabili già fatte. #72 documenta il dato personale nell'archivio annidato e il controllo che l'aveva mancato. Lo ZIP presente esclude i due vecchi archivi. Fonti: REGISTRO-DIFETTI.md righe 62, 93 e 120–121, REGISTRO-ESPLORAZIONI.md riga 19, REGISTRO-MODIFICHE.md v1.46 e v1.49, LEGGIMI-PACCHETTO.md. |

**Rettifica del DGS.** In DGS-04 ho registrato la decisione su H-002 senza esplicitare il conflitto con il §8 della scheda v3.1, che usava una regola di screening binaria. Il rilievo di Claude su questa omissione è fondato. Lo screening storico e la decisione del titolare devono restare leggibili come eventi distinti. La decisione e la condizione d'uscita registrate il 15/11 sono il riferimento di questa revisione.

## P1 · IA-02

**Sviluppo sulla stima, verifica sul limite inferiore.** Sullo sviluppo, `R medio netto stimato ≥ +0,15 R` è un criterio di ammissione insieme agli altri vincoli e a un minimo informativo fissato prima. Si riportano anche incertezza e contaminazioni. In verifica, testare `H₀: μ ≤ +0,15 R`. Per promuovere, il limite inferiore unilaterale alla quota assegnata alla variante deve superare la soglia, e gli altri requisiti vincolanti devono essere soddisfatti. Il DSR, da solo, non attesta il superamento di +0,15 R netto.

**La correlazione in R13 è simulata.** Il 27,22% di passaggi con 450 trade e media vera +0,10 R viene da un modello AR(1) con ρ = 0,25; non è una correlazione empirica di H-003. La scheda deve fissare il metodo che preserva la dipendenza e il clustering per seduta quando pertinente, mantenendo l'estimando per trade. Userei lo sviluppo per stimare varianza, frequenza e sensibilità, e fisserei le scelte metodologiche prima dell'apertura.

Nell'approssimazione normale indipendente del fascicolo, con σ = 1,25 R, media vera +0,20 R e potenza 80%, servono **4.906 trade** alla quota unilaterale 2,5% e **6.544** alla quota 0,8333%, per una variante. Sono calcoli illustrativi. I circa 2.500 trade del rapporto sono una proiezione al ritmo di H-002 per l'intera riserva. Una candidata sottodimensionata attende dati futuri. L'effetto alternativo plausibile si motiva prima della prenotazione.

Fonti: IMPEGNI-ANTICIPATI.md righe 14–30, potenza_IA-02.md righe 7–57, G-20261116-R13.md righe 105–113.

## P2 · Spesa della riserva

**Propongo α totale 5%**, con quota di coorte `α_j = 0,05/[j(j+1)]` e ripartizione `α_j/m` se sono possibili `m` promozioni. Prime tre quote di coorte: 2,5%, 0,8333%, 0,4167%. La protezione contro almeno una falsa promozione nel programma dipende da test validi alla quota assegnata, tenuto conto della dipendenza e delle informazioni già rilasciate. Il conteggio N per il DSR resta distinto da j e m. Impegnare prima della prenotazione famiglia, domanda, test, calendario, N e quota prevista; confermarli all'autorizzazione.

- **Finestra.** Scegliere la prima partenza cronologica compatibile con la potenza conservativa, e da quella data la durata minima che soddisfa tutti i criteri di scheda, inclusi riscaldamento, embargo e requisiti per anno. Usare metadati di qualità e stime sullo sviluppo. Il primo accesso autorizzato consuma l'intero perimetro esposto sull'universo dichiarato, incluso il riscaldamento esposto. Esito, guasto e risultato inconclusivo non riaprono le date.
- **Parte protetta.** Prima di assegnare la prima finestra, conservare l'ultimo intervallo contiguo idoneo per almeno una verifica successiva plausibile, dimensionata al livello della seconda apertura e al numero di promozioni previsto da quel disegno. Fissare i confini dalla copertura attestata e dalle stime conservative. Se entrambi gli intervalli non stanno nella riserva, raccogliere dati prospettici. Una scelta esplicita di un'unica apertura storica spetta al titolare prima dell'accesso.
- **Condizione di apertura.** #92 distingue contabilità e custodia. Serve evidenza che il percorso autorizzato legga soltanto lo snapshot prenotato e registri il consumo prima della lettura, con impegno datato esterno al file locale. Una prova sintetica della sequenza è evidenza distinta dall'esistenza di riserva.py. Il custode dichiara qualità e integrità senza rilasciare prezzi, rendimenti o conteggi dei segnali della candidata.

Fonti: riserva.py righe 1–23, 62–147 e 187–218, STATO-PROGETTO.md righe 18–27 e 48–50, REGISTRO-DIFETTI.md #92.

## P3 · Modello H-003

**Approvazione dopo quattro integrazioni.** Il modello copre già origine dell'idea, regole prospettiche, casi d'oro, replica e conteggio dei tagli.

1. **Decisioni su barre M1.** Fissare il primo istante in cui ogni informazione è disponibile. Se la stessa barra è compatibile con più percorsi, per esempio stop e target entrambi toccati, fissare prima la regola conservativa, contare i casi e replicarla. Trattare in anticipo la stessa ambiguità attorno a ingressi, uscite e buchi.
2. **Primario, confronti e gradi di libertà.** Specificare formula e denominatore di R netto, unità di rischio, costi e benchmark a parità di date eleggibili, esecuzione e rischio. Elencare ogni via di promozione, taglio ereditato, variante, veto, N e m. Una diagnostica usata per selezionare diventa una prova selezionabile.
3. **Coerenza del campione.** Dichiarare metodo dell'intervallo, dipendenza, potenza, minimo di trade e di unità temporali. Definire anni parziali e «ultimi cinque anni». Un intervallo senza cinque anni valutabili non può soddisfare quel criterio.
4. **Esito incompleto.** Il §8 apre a «non decidibile», poi chiude l'ipotesi se nessuna variante passa. Scrivere prima quale evidenza futura può risolvere l'incertezza, con quale regola congelata e con quale nuovo impegno, secondo DA-31.

Dopo la baseline, il titolare formula le idee osservando esclusivamente dati dal 15/11/2023 in avanti. Prima della prova annota data e periodo visto. Il DGS contesta la lettura, cerca controesempi e verifica la falsificabilità. L'idea rimane del titolare.

Fonte: MODELLO-SCHEDA-H-003.md §§0–12.

## P4 · DA-31

**Tre stati, opzione C con due minimi distinti.** Fissare il minimo tecnico per calcolare le statistiche e il minimo informativo richiesto dal disegno. Trenta trade, dove bastano per calcolare una statistica, non costituiscono un piano di potenza.

| Verdetto | Regola da preregistrare per le nuove ipotesi |
|---|---|
| **Promossa** | Dati idonei, minimi informativi raggiunti, limite inferiore sopra IA-02 e tutti i requisiti vincolanti passati. |
| **Bocciata** | Su una prova valida, limite superiore sotto IA-02 oppure fallimento di un requisito dichiarato in anticipo come veto terminale su misure valide. Fissare anche il metodo per il limite superiore. |
| **Non decidibile** | Dati insufficienti, statistica non stimabile o intervallo che lascia aperto il superamento di IA-02, in assenza di un veto terminale validamente accertato. |

Solo «promossa» consente di avanzare. Il non decidibile consuma date e quota. Un eventuale riesame preregistrato usa dati nuovi, e ogni nuova prova selezionabile entra in N. Se cambia la regola o il disegno per recuperare l'esito si registra una nuova ipotesi.

Fonti: DECISIONI-APERTE.md righe 391–397, MODELLO-SCHEDA-H-003.md righe 82–94, riserva.py righe 140–147.

## P5 · Criteri anticipati di accettazione dello storico

**Parere del 17/11/2026.** Ho visto soltanto lo stato aggregato dello scarico, senza conteggi di completezza, CSV o quotazioni. I minimi sotto definiscono l'idoneità tecnica proposta per XAUUSD M1 nella sessione di Londra del banco. Le soglie sono una scelta prudenziale del DGS, da ratificare prima del consuntivo. Potenza e vincoli della candidata richiedono una verifica propria.

| Controllo | Proposta di accettazione |
|---|---|
| **Calendario e denominatore** | Estremi inclusivi 01/01/2005–31/10/2023. Versionare il calendario prima del consuntivo, con ora legale Europe/London. Griglia ordinaria [08:00,16:45) di Londra, 525 minuti. Escludere solo chiusure documentate prima di leggere i conteggi. Trattare le sedute abbreviate sulla finestra effettiva documentata, in un riepilogo separato. Valutare il 2023 fino al 31/10. |
| **Integrità** | Ogni giorno e lato attesi hanno uno stato riconciliato con inventario e log. Per ogni file accettato verificare byte e SHA-256 nello snapshot, decodifica, timestamp UTC univoci e allineati al minuto. Zero file mancanti, vuoti o illeggibili su seduta attesa nel perimetro accettato. Nessun errore o temporaneo irrisolto. Un 404 o due vuoti coincidenti su data aperta sono anomalie. |
| **BID/ASK allineati** | Conta il minuto UTC comune ai due lati con quotazioni valide per l'esecuzione e ASK ≥ BID al controllo previsto. Rendicontare minuti solo BID, solo ASK, comuni non validi e mancanti su entrambi. Due file per giorno o conteggi uguali non dimostrano l'allineamento. Nessun riempimento né propagazione del prezzo precedente. |
| **Seduta e buchi** | Una seduta ordinaria è ammissibile con **≥98%** di minuti comuni validi (**515/525**), **≥95%** in ogni terzo (**167/175**) e nessuna sequenza di oltre **5 minuti** mancanti o non validi, bordi inclusi. Stesse percentuali per le sedute abbreviate documentate, arrotondate per eccesso sul periodo effettivo. Una candidata può richiedere finestre critiche più complete, fissate prima dell'apertura. |
| **Copertura annuale** | Per ogni anno **≥99%** delle sedute attese ammissibili e nessuna coppia di sedute attese consecutive non ammissibili. Riportare anche i conteggi mensili. Tenere nel denominatore le sedute aperte con file presenti ma di qualità insufficiente. Una seduta aperta con file mancante, vuoto o illeggibile richiede ripristino oppure rigetto del perimetro interessato. |
| **Ricevuta e verdetto** | Consegnare versione del controllore e del calendario, ID e impronte di snapshot e log, limiti, tabelle annuali e mensili, eccezioni con intervallo e motivo, esiti per lato e intersezione, quarantene e riesiti dopo riscarico. Al DGS bastano conteggi e impronte. Un perimetro sotto soglia non è assegnabile. Eventuali esclusioni si fissano prima dell'apertura, ricalcolando la potenza sulla capacità residua. |

**I due strumenti non bastano a dimostrare l'intersezione al minuto.** Il confronto `--ask` controlla presenza e vuoto per giorno. La taratura lavora per lato e mostra una griglia. Il custode deve rendicontare la congiunzione dei timestamp sulla griglia attesa e riconciliarla con il manifest della cache. Se il minimo fallisce, ripristinare i dati o dichiarare il perimetro non accettato. La griglia di taratura serve a diagnosticare le carenze, senza scegliere a posteriori la soglia più comoda.

Fonti: STATO-PROGETTO.md righe 19–25 e 51, REGISTRO-MODIFICHE.md v1.45, controlla_cache.py righe 49–103 e 128–182, taratura_completezza.py righe 25–63 e 78–105.

## P6 · Rischio residuo per D-24

**Due giri “puliti” riferiti a candidati o ambienti diversi possono dare una falsa convergenza.** R14 ha documentato un comportamento specifico di Apple Python 3.9. Per ciascun giro che conta, annotare commit esatto, ambiente, perimetro e prove eseguite, con riscontro sul profilo effettivo della verifica. Se una modifica materiale tra i giri invalida una parte delle evidenze, rieseguire quella parte sul candidato finale prima di contare entrambi i giri. È un criterio per attribuire l'evidenza alla versione sottoposta a D-24.

Fonti: DECISIONI.md riga 30, STATO-PROGETTO.md righe 13–17, G-20261117-R14.md righe 5, 17–21 e 119–126, REGISTRO-MODIFICHE.md v1.49.

## Letture e autocritica

- **Integrali nel merito.** LEGGIMI-PACCHETTO.md, STATO-PROGETTO.md, DECISIONI.md, IMPEGNI-ANTICIPATI.md, RICONTEGGIO-20261117.md, potenza_IA-02.md, MODELLO-SCHEDA-H-003.md. MANIFEST.tsv verificato per tutte le righe.
- **Parziali.** REGISTRO-MODIFICHE.md v1.38–v1.49 e richiami a E-003. REGISTRO-DIFETTI.md #41–#104 e conteggio integrale. DECISIONI-APERTE.md DA-19 e DA-31. H-002-REVISIONI.md R11, parcheggio e avvio R12-bis. Sezioni pertinenti dei rapporti R13, R14 e G-20261115-03, riga E-003 del REGISTRO-ESPLORAZIONI.md e sezioni pertinenti di riserva.py, controlla_cache.py e taratura_completezza.py.
- **Senza lettura di merito.** Altri membri, incluse sonde e mutanti. R12-bis e BANCO-02 sono riscontrati tramite i registri e i rimandi documentali. Ho eseguito controlli d'integrità e calcoli illustrativi, senza replicare le prove tecniche. Corrispondenza con Git, consegne esterne, cecità fuori dalle trascrizioni, correzioni post-R14 e copertura effettiva restano nei limiti sopra indicati.
- **Giudizio del DGS.** I minimi P5 potrebbero escludere periodi con feed strutturalmente discontinuo. Sono limiti di idoneità proposti ex ante. Anche il 5% di P2 è una scelta di governance. La potenza reale di H-003 resta da stimare per la sua scheda.


---

# Allegato B · Addendum metodologico

# DGS-05 · Addendum metodologico 1

17 novembre 2026 · Primo esame delle definizioni e delle garanzie statistiche · Proposte per H-003 e successive.

## Esito e rettifiche

Il titolare accetta di attendere più dati per ottenere evidenza più forte sul superamento di IA-02. Questo conferma la preferenza per una verifica sul limite inferiore. Metodo dell'intervallo, disegno, quote d'errore e soglie tecniche devono ancora essere giustificati e ratificati.

**Ritiro la raccomandazione immediata di ratificare i numeri P5 del DGS-05.** Le percentuali 99/98/95 e il limite di cinque minuti erano scelte prudenziali senza una validazione della loro adeguatezza. Restano ipotesi da esaminare. Il consenso del titolare riguarda piccoli buchi gestiti con regole anticipate. L'anteriorità di una regola protegge dalla scelta opportunistica, ma da sola non ne dimostra la validità.

**Rettifico anche la precedente implicazione che basti attendere.** Il vantaggio può essere inferiore alla soglia o cambiare nel tempo. Un campione più grande non corregge automaticamente errori di selezione, esecuzione o modello. Ogni inferenza riguarda il processo e il periodo definiti dal disegno. Il trasferimento al futuro richiede una successiva verifica prospettica.

Il 5% globale, la spesa decrescente e i tre stati del DGS-05 restano proposte. Una formula di spesa controlla la somma delle quote, mentre la validità dei test determina se quelle quote corrispondono all'errore reale. Il presente lavoro riguarda il metodo e usa esempi matematici inventati.

## 1. Che cosa significa +0,15 R

**Verificato nel pacchetto c5ca93d.** H-002-ORB-v3.md §5, righe 94–98, definisce capitale fisso, budget di rischio di 500 USD, quantità arrotondata per difetto e R = profitto netto / 500. Il simulatore orb_londra.py, righe 246–254, calcola il dimensionamento includendo commissione e slittamento allo stop, poi divide il netto per rischio_usd. Il modello H-003 ha ancora campi da compilare e rinvia a H-002 per diverse metriche.

**Proposta per le future schede.** Rendere esplicita la stessa convenzione, salvo diversa decisione anticipata del titolare:

R_i = P/L netto dell'operazione i / B_i,

con B_i budget monetario di rischio fissato prima dell'ingresso, positivo, nella stessa valuta del P/L. Documentare la regola di B_i, arrotondamenti, stop pianificato, quantità e valore monetario del punto. Riportare anche il rischio pianificato effettivamente utilizzato. Ogni posizione originata da un ingresso è un'operazione; uscite parziali si ricompongono nella stessa unità. Reingressi e incrementi di posizione richiedono una definizione nella scheda. Questa è una proposta di convenzione, con H-002 come precedente documentato.

Il numeratore deve includere tutti i costi pertinenti. Lo spread è incorporato nei prezzi del lato eseguibile; evitare di sottrarlo due volte. Commissioni, conversione e finanziamento, se applicabili, hanno formula e fonte. Lo slittamento deve avere un modello dichiarato. Uno stop con gap può perdere oltre 1 R. Il denominatore resta quello impegnato prima del risultato.

**Controllo aritmetico eseguito.** Profitto netto 75 USD, budget 500 USD, rischio pianificato effettivamente impiegato 400 USD. Le due normalizzazioni producono 0,15 e 0,1875. Sono quantità diverse: il superamento di IA-02 va giudicato sulla convenzione fissata, senza cambiare denominatore dopo il risultato.

**Estimando proposto.** Media di R per operazione della politica congelata, sulle opportunità definite dal calendario e dai filtri disponibili al momento della decisione. I giorni senza operazioni non entrano come trade da zero R. Entrano nelle serie di calendario usate per studiare frequenza, dipendenza ed esposizione. La scheda deve indicare come tratta le operazioni incompletamente osservate e quali limiti impediscono di stimare questa media.

## 2. Controesempio esatto sull'incertezza

Ho calcolato un riferimento matematico con 450 osservazioni gaussiane congiunte, media vera 0,15 R, deviazione marginale nota 1,25 R e correlazione rho^k al ritardo k. Il test usa erroneamente sigma/sqrt(n), soglia unilaterale nominale 2,5%. Il calcolo è analitico, senza dati di mercato e senza errore Monte Carlo.

F = 1 + 2 × somma per k=1…n−1 di [(1−k/n) rho^k].

Var(media) = sigma² F/n. La probabilità di falsa promozione al confine della null è 1−Phi[z_(0,975)/sqrt(F)].

| rho ipotizzato | F esatto a n=450 | Falsa promozione del test ingenuo |
|---:|---:|---:|
| 0 | 1,000000 | 2,5000% |
| 0,25 | 1,664691 | 6,4371% |
| 0,50 | 2,991111 | 12,8551% |

Usando la varianza vera del modello il tasso torna esattamente al 2,5%. Questo riferimento presuppone varianza e dipendenza note. Non convalida un metodo che deve stimarle dai dati. Il caso al confine è necessario nel collaudo: una null composta mu ≤ 0,15 comprende anche mu = 0,15.

NIST documenta che il metodo tradizionale d'incertezza della media, basato sull'indipendenza, è inappropriato per misure autocorrelate. [NIST](https://www.nist.gov/publications/calculation-uncertainty-mean-autocorrelated-measurements?pub_id=151800)

Newey–West fornisce una covarianza consistente sotto condizioni dichiarate. La consistenza è un risultato asintotico. La ricerca sulla selezione automatica dei ritardi riporta anche distorsioni della dimensione del test in simulazione. La semplice menzione «HAC» non certifica il campione del progetto. [Newey–West](https://www.nber.org/papers/t0055) · [Selezione dei ritardi](https://www.nber.org/papers/t0144)

## 3. Protocollo candidato per il successivo collaudo

1. Test primario unilaterale H0: mu ≤ 0,15 R, con promozione soltanto se il limite inferiore valido supera 0,15. Congelare quota per variante, via di promozione e famiglia prima dell'apertura. Un intervallo bilaterale al 95% ha coda inferiore al 2,5%; le aperture successive o le coorti con più varianti possono richiedere code più piccole.
2. Conservare il calendario. Per ogni seduta d, memorizzare S_d, somma degli R delle operazioni attribuite alla seduta secondo una regola fissata, e K_d, numero di operazioni. La media per trade è somma S_d / somma K_d. Sedute aperte osservabili senza trade hanno (0,0); dati mancanti hanno uno stato diverso. La dipendenza va studiata senza comprimere automaticamente i giorni senza trade.
3. Esaminare come candidati un intervallo HAC sulla media per trade e un ricampionamento a blocchi delle coppie giornaliere (S_d,K_d). Con HAC, una possibile linearizzazione usa S_d−mu_hat K_d e il denominatore medio K. Questa è una proposta da derivare e collaudare, non un intervallo già approvato. La semplice media giornaliera degli R medi delle singole sedute attribuirebbe pesi diversi ai trade.
4. Il metodo primario e la regola di scelta dei ritardi o blocchi vanno fissati prima della riserva. Metodi secondari hanno un ruolo dichiarato. Scegliere dopo i risultati quello che promuove introdurrebbe un'altra occasione di selezione.
5. Collaudare null sotto soglia e al confine, più alternative sopra soglia, con campioni piccoli/grandi, più dipendenze, code asimmetriche, perdite rare e volatilità variabile. Inserire scenari con clustering di trade per giorno, frequenza casuale e cambi di regime. I cambi di regime servono anche a individuare quando l'estimando o l'ipotesi di stabilità diventano inadeguati.
6. Separare calibrazione e verifica finale del metodo usando semi e scenari di verifica impegnati prima del tuning. Quantificare l'errore Monte Carlo sui tassi di falsa promozione e sulla potenza. Il numero di repliche deve consentire di risolvere le code della quota più piccola. La tolleranza numerica e la regola d'accettazione del collaudo richiedono una motivazione e un impegno prima dei risultati. Non sono ancora fissate in questo addendum.
7. Verificare il controllo congiunto sul programma di promozioni: stesso disegno di selezione, screening e aperture previsto nella pratica. Per una garanzia globale servono p-value validi condizionatamente alle informazioni disponibili prima della prova. Quote che sommano al 5% non riparano p-value invalidi.

Il DSR corregge aspetti della selezione tra molte prove e della non normalità nell'inferenza sullo Sharpe. Il test della media netta oltre IA-02 resta da costruire sull'estimando sopra. [Bailey–López de Prado](https://davidhbailey.com/dhbpapers/deflated-sharpe.pdf)

## 4. Buchi nei dati: prova che la sola percentuale non basta

**Esempio deterministico eseguito.** 200 operazioni da +0,5 R e 100 da −1 R hanno media zero. Se buchi selettivi rendono non osservabili 50 perdite e il backtest le elimina, le 250 osservate hanno media +0,20 R. L'esempio costruito dimostra un possibile errore di selezione; non ne stima la probabilità sul feed.

Inoltre, una singola barra mancante può occultare lo scatto dello stop. Due percorsi completi compatibili con le barre osservate possono avere lo stesso prezzo prima e dopo il buco, ma diversi esiti dello stop durante il buco. Anche completezza molto alta può lasciare il P/L non identificato. Un modello di uscita alla prima quotazione successiva deve distinguere una vera assenza di quotazioni eseguibili da una perdita di dati del fornitore. Nel secondo caso il mercato potrebbe aver toccato lo stop durante l'intervallo mancante.

**Procedura proposta.** Usare percorsi sintetici completi come riferimento e maschere di mancanza casuali, concentrate presso ingressi/uscite e associate a volatilità o movimenti avversi. Confrontare segnali, numero di trade, P/L, media e verdetto prima e dopo la maschera. Fissare prima le condizioni testate e il criterio di accettazione. I percorsi sintetici devono includere almeno due sequenze intrabar compatibili con gli stessi OHLC ma con diverso ordine di stop e target.

**Conseguenze metodologiche già individuate.** Un filtro prima dell'ingresso può usare soltanto informazioni allora disponibili. Se una seduta viene eliminata perché ha buchi successivi, il risultato sul sottocampione deve essere dichiarato e non può essere trasferito automaticamente alla politica eseguibile. Una posizione già aperta resta tra le operazioni da rendicontare. Se il suo P/L non è ricostruibile, servono dati sostitutivi attendibili oppure limiti dell'esito motivati. Un semplice −1 R non è un limite di perdita garantito in presenza di gap. Se i limiti non sono identificabili, si dichiara l'incertezza e si rinvia il verdetto.

La completezza va sempre rendicontata per file, giorno e intersezione dei timestamp BID/ASK. Le percentuali sono diagnostiche fino a quando il criterio di idoneità è giustificato. Il controllo dei valori OHLC e ASK/BID va eseguito dal custode con output ammessi definiti; la riserva rimane separata dal lavoro di ricerca.

## 5. Evidenze, limiti e prossimo passo

**Compiuto.** Lettura integrale della scheda di stato; lettura mirata di H-002 §5 e relativi passaggi del simulatore e del modello H-003; controllo delle fonti statistiche indicate; calcoli deterministici di normalizzazione, selezione da dati mancanti e tasso d'errore nel modello gaussiano correlato. La verifica dell'archivio 369/369 è quella del DGS-05. Il codice di progetto non è stato attaccato né modificato.

**Non compiuto.** Stima di dipendenza reale, collaudo di un intervallo HAC/bootstrap, simulazione completa della selezione e dei dati mancanti, replica indipendente dei calcoli, nuova ratifica delle quote e dei minimi. Nessuna quotazione della riserva è stata letta. Questi controesempi individuano errori possibili senza certificare il metodo sostitutivo.

**Prossimo passo concreto.** Completare la specifica di R e dell'unità statistica nella futura scheda, poi definire il protocollo di collaudo con scenari, semi, numero di repliche e criterio di accettazione prima di eseguire la calibrazione. Le scelte di governance rimangono del titolare. Il DGS propone e verifica il metodo; l'idea della strategia appartiene al titolare.

## Calcolo riproducibile

Python standard, senza dipendenze né dati esterni. Codice usato per i tre controesempi.

```python
from math import sqrt
from statistics import NormalDist

n = 450
alpha = 0.025
normal = NormalDist()
critical = normal.inv_cdf(1 - alpha)

for rho in (0.0, 0.25, 0.50):
    factor = 1 + 2 * sum(
        (1 - lag / n) * rho ** lag
        for lag in range(1, n)
    )
    false_promotion = 1 - normal.cdf(critical / sqrt(factor))
    print(rho, factor, false_promotion)

print('R con budget', 75 / 500)
print('R con rischio impiegato', 75 / 400)
print('Media completa', (200 * 0.5 - 100) / 300)
print('Media dopo esclusioni', (200 * 0.5 - 50) / 250)
```


---

# Allegato C · Specifica di collaudo IA-02

# Specifica di collaudo metodologico IA-02

17 novembre 2026 · Nota del DGS per Claude e per il titolare · Stato: proposta da esaminare prima di implementazione e simulazioni.

## Scopo e perimetro

Verificare se la procedura che promuove una strategia quando il limite inferiore supera +0,15 R mantiene il tasso dichiarato di falsa promozione nei casi sintetici stabiliti prima. Il risultato riguarda il dominio di scenari collaudato. La validità sui dati reali richiede anche che le ipotesi del metodo siano difendibili per quel processo.

Questa nota usa la conversazione e fonti statistiche pubbliche. Nessuna nuova lettura del pacchetto, delle schede sigillate, del codice di progetto o dei dati è stata effettuata per prepararla. Implementazione e prove eseguibili spettano a Claude. Il titolare trasmette la nota.

## Principi concordati e scelte ancora aperte

- Il titolare accetta di attendere più dati per ottenere evidenza più forte sul superamento di IA-02.
- Un'operazione comprende ingresso, uscite parziali e chiusura completa. La convenzione discussa usa risultato netto diviso per budget di rischio fissato prima dell'ingresso.
- Un'operazione aperta con esito non ricostruibile rimane nel rendiconto. Se l'incertezza può cambiare il giudizio, la promozione attende una verifica risolutiva. Metodo dei limiti ancora da definire.
- Quote d'errore, metodo dell'intervallo, piano di collaudo e regole di spesa restano proposte. Le soglie di completezza 99/98/95 e cinque minuti del DGS-05 non sono validate né ratificate. La raccomandazione di ratificarle subito è stata ritirata.

## 1. Oggetto del collaudo

Per una quota nominale a, testare H0: mu ≤ 0,15 R. L'evento di interesse è «limite inferiore > 0,15 R». La quota riguarda le false promozioni ripetendo il disegno sotto la null; non esprime la probabilità personale che una specifica strategia sia buona.

Separare due risultati del collaudo:

1. Validità dell'intervallo primario, valutata prima dei veti accessori. Un veto che respinge quasi tutto potrebbe nascondere un intervallo invalido.
2. Frequenza delle promozioni finali dell'intera procedura, inclusi screening, selezione delle varianti, veti e aperture previste. Riportare anche tasso di non decidibili, errori di esecuzione e potenza.

## 2. Perché il semplice confronto con la percentuale nominale non basta

Ogni replica sintetica indipendente produce un indicatore di falsa promozione. In uno scenario fissato, k promozioni su M repliche stimano p tramite k/M. Anche questo numero è incerto. Una percentuale appena inferiore ad a può essere compatibile con un vero p superiore ad a.

Propongo limiti binomiali esatti unilaterali Clopper–Pearson. Per 0 ≤ k < M, il limite superiore è U = quantile Beta(1−delta; k+1, M−k); con k=M, U=1. Per k=0, U=1−delta^(1/M). Il limite inferiore è L = quantile Beta(delta; k, M−k+1) per k>0 e L=0 per k=0. Sono limiti frequentisti sul tasso di errore dello specifico generatore. [NIST, limiti binomiali esatti](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm)

Se si vogliono conclusioni simultanee su K confronti scenario–campione–quota, con rischio Monte Carlo complessivo gamma, usare delta=gamma/(2K) per ciascuna coda. La correzione considera entrambi i limiti. Le repliche dentro ogni scenario devono essere indipendenti; usare semi comuni tra metodi o scenari può essere consentito, poiché la correzione per unione non richiede indipendenza tra scenari.

**Proposta del DGS, da ratificare:** gamma=1% per l'insieme delle conclusioni del collaudo finale. È una scelta di governance della precisione del collaudo, distinta da a e dall'eventuale 5% globale del programma strategie.

| Esito della validazione nello scenario | Regola proposta |
|---|---|
| Compatibile con il limite richiesto, con evidenza sufficiente | U ≤ a |
| Violazione dimostrata al livello del collaudo | L > a |
| Non risolto | L ≤ a < U |

Per ammettere il metodo sul dominio preregistrato, tutte le celle obbligatorie devono avere U ≤ a. Una cella non risolta richiede altro lavoro. Una cella fallita non si elimina dal dominio dopo aver visto il risultato. Un dominio ristretto può essere una nuova proposta motivata, con condizioni di applicabilità riconoscibili prima del test reale.

**Limite cruciale:** un metodo esattamente al confine p=a difficilmente soddisfa U≤a. Questa regola richiede un margine conservativo per una certificazione empirica positiva. Non basta aumentare M per rendere probabile l'ammissione di un metodo esattamente al confine. Il margine e la perdita di potenza conseguente vanno dichiarati.

## 3. Numero di repliche e protezione dal riadattamento

Proposta di pianificazione: calibrare per un obiettivo p*=a/2 negli scenari obbligatori, verificando la perdita di potenza. Il fattore 1/2 è una scelta prudenziale del DGS da discutere prima dei risultati, non una costante statistica universalmente giusta.

Per ogni cella, scegliere prima M tale che, sotto p*, la probabilità di ottenere U(k,M)≤a sia almeno 90%, calcolata mediante la distribuzione binomiale esatta. La probabilità del 90% è per cella; non implica 90% per il superamento congiunto di tutte le celle. Se serve anche una probabilità congiunta di superamento, fissarla esplicitamente e dimensionare di conseguenza. Claude deve fornire il calcolo di costo prima della corsa completa. Evitare l'adozione automatica di un numero tondo di repliche.

Usare due fasi:

1. Calibrazione su scenari e semi dichiarati, con registro delle modifiche del metodo.
2. Verifica finale su nuove repliche indipendenti, dopo congelamento di algoritmo, parametri, generatore, scenari e criteri. Il risultato finale viene letto una sola volta all'orizzonte deciso.

Se si cambia metodo dopo la verifica finale, quella verifica diventa materiale di sviluppo. La validazione successiva usa nuove repliche e un budget Monte Carlo che tenga conto delle nuove occasioni di certificazione. Il gamma non riparte automaticamente a ogni tentativo. La gestione concreta del budget tra tentativi va definita prima del primo test finale. Eventuali letture intermedie richiedono un disegno sequenziale specifico; il piano ordinario qui proposto usa M fissato.

## 4. Matrice di scenari da rendere numericamente completa

Prima dell'implementazione Claude propone una matrice finita, con K esplicito e motivazione di ogni livello. I parametri qui sotto sono requisiti di copertura, con gli esatti livelli ancora da fissare.

| Famiglia | Cosa deve mettere alla prova |
|---|---|
| Riferimento gaussiano indipendente | Null al confine, sotto soglia e alternative sopra soglia. Controllo con soluzione teorica. |
| Gaussiano correlato | Dipendenza negativa e positiva, compresi i riferimenti rho=0,25 e 0,50 già calcolati nell'addendum. Inizializzazione stazionaria o trattamento del transitorio dichiarato. |
| Esiti asimmetrici e perdite rare | Media vera nota; varianza finita dichiarata. Scenari con perdite poco frequenti ma rilevanti e probabilità di non osservarle nel campione. |
| Volatilità variabile e dipendenza persistente | Copertura delle ipotesi ammesse dal metodo e stress fuori dominio segnalati come tali. |
| Frequenza variabile e più trade per seduta | Conservazione dell'estimando per operazione, dipendenza dentro e tra giorni, giorni aperti senza trade. |
| Mancanze casuali e informative | Buchi associati a volatilità ed esiti avversi. Rendicontazione delle posizioni già aperte e dei casi non identificabili. |
| Selezione e aperture | Più varianti correlate, screening e scelta coerenti con il disegno effettivo. Frequenza di almeno una falsa promozione nel programma simulato. |
| Cambi di regime | Dichiarare il parametro bersaglio per il periodo. Valutare quando manca una giustificazione per trasferire il risultato al futuro. |

Per ciascuna famiglia fissare dimensioni campionarie, quote a pertinenti, mu, dispersione, dipendenza, distribuzione dei costi e frequenza. Le quote definitive dipendono dalla decisione P2. Sotto la null includere mu=0,15 e valori inferiori; non assumere automaticamente che il confine sia il caso peggiore per tutte le procedure. Nel collaudo della potenza usare alternative motivate e riportare la curva, senza scegliere soltanto quelle favorevoli.

HAC e bootstrap a blocchi sono candidati da confrontare durante la calibrazione. Le condizioni di validità, il metodo di scelta dei ritardi/blocchi e la procedura applicata a frequenze casuali devono essere scritti. La selezione automatica dei ritardi HAC può presentare distorsioni della dimensione del test in campioni finiti. [Newey e West, Automatic Lag Selection](https://www.nber.org/papers/t0144)

## 5. Condizioni di correttezza da segnalare a Claude

| Problema metodologico | Evidenza richiesta |
|---|---|
| Identificare a con probabilità che una strategia sia buona | Definizione frequentista del tasso controllato e dell'unità di ripetizione. |
| Confondere mu nota del generatore e media realizzata del campione | Parametro teorico verificato separatamente. Evitare ricentraggi ex post che eliminino artificialmente la variabilità della media. |
| Considerare indipendenti operazioni correlate | Riferimenti analitici riprodotti e confronto con il metodo candidato. |
| Fare sparire errori e non decidibili | Ogni replica resta nel denominatore. Errori numerici o interruzioni richiedono diagnosi; non diventano successi di validità. Riportare separatamente probabilità di promozione, astensione ed errore. |
| Promuovere un metodo che si astiene sempre | Curve di potenza e tassi di non decidibile. Il limite d'errore da solo non prova utilità. |
| Selezionare l'intervallo più favorevole | Metodo primario congelato prima della validazione finale; ruolo dei secondari dichiarato. |
| Cancellare trade con dati mancanti | Conteggi completi e verifica dell'effetto sul verdetto. Limiti giustificati o non decidibile quando il P/L non è identificabile. |
| Trattare un campione finito di scenari come garanzia universale | Dominio esplicito, condizioni di applicabilità e rischi residui. |

## Consegna richiesta a Claude

Prima fase: esaminare criticamente questa specifica, indicando errori, costi e alternativa motivata dove serve. Restituire proposta completa di metodo primario, dominio, matrice con K, quote esaminate, budget Monte Carlo tra tentativi, M per cella, semi e versioni impegnate, criterio di accettazione e output previsti. Collegare la proposta alla sequenza di lavoro autorizzata dal titolare e alla chiusura della baseline.

L'implementazione e la validazione eseguita sono una fase successiva da riportare con log ed esiti. Questa nota non attesta che il metodo abbia superato alcuna simulazione. Per i valori gamma=1%, p*=a/2 e probabilità per cella 90% si richiede un parere motivato prima della ratifica: sono proposte del DGS, non decisioni già prese dal titolare.

**Autocritica del DGS.** La regola U≤a è deliberatamente esigente e può richiedere molti calcoli, soprattutto per quote piccole. Un modello più conservativo può perdere molta potenza. Scenari troppo semplici o costruiti dal solo autore possono lasciare difetti invisibili. Anche dopo esito positivo, l'applicabilità al mercato e la qualità dei dati richiedono prove proprie. La verifica indipendente deve poter contestare sia la procedura sia il generatore.
