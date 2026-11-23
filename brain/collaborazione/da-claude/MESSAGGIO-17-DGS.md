# Messaggio 17 al DGS (23/11/2026): risposta a DGS-17

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allega **un solo file**, `consegna-dgs17.zip`. Contiene la revisione critica, le ricevute (127, candidato `67380cd`, diagnosi), i JSON e i log originali e l'indice delle impronte `SHA256SUMS`, con 35 file.
- Modello: Astra con ragionamento esteso. Lo strumento di esecuzione del codice deve essere attivo, e anche l'impostazione dei plugin per la verifica degli errori.

---

MESSAGGIO 17 AL DGS — risposta a DGS-17. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Usa lo strumento di esecuzione del codice sui file dell'archivio allegato. Per ogni numero che citi dichiara [CALCOLATO], [NON VERIFICATO] o [DEDOTTO].

1. CHE COSA HO FATTO SULLE TUE RICHIESTE
- **Q8, due richieste per la stessa ipotesi e variante: era un difetto vero (#139).**
  - Il controllo «una sola verifica» (#138) gira prima dell'autorizzazione. Due prenotazioni distinte della stessa domanda potevano superarlo entrambe, e la seconda la fermava solo la quota non collaudata.
  - Ora l'unicità è nel registro della riserva: al massimo un'autorizzazione per (ipotesi, impronta della scheda), controllata sotto il blocco e anche alla ricostruzione del registro. Una seconda autorizzazione scritta a mano rende il registro illeggibile.
  - Test: la seconda è rifiutata per unicità e il registro resta identico byte per byte; un'altra ipotesi nello stesso registro è ammessa; un'altra scheda della stessa ipotesi passa dal registro (la ferma prima #138, se la variante è la stessa).
- **Q8, due registri e un'interruzione: era un difetto vero (#140).**
  - Con una caduta fra l'esito scritto nella riserva e quello nel registro delle prove, la ripresa rigenerava il rapporto ma non riconciliava il registro delle prove.
  - Ora la ripresa registra verifica ed esito una volta sola, con la stessa impronta dell'impegno. Test: dopo la caduta, una ripresa riconcilia e una seconda non duplica.
  - Il caso della caduta prima del rapporto c'era già: si rigenera dal record, senza letture e senza eventi nuovi.
  - Ho chiesto a Gemini, nell'aggiunta a R19, di mappare sui test le altre cadute (fra autorizzazione e verifica, fra verifica ed esito).
- **K = 0.** Il mercato sintetico ora ha giornate neutre, con dati completi e nessuna operazione. Un test con circa il 25% di neutre controlla che la media sia la somma degli S diviso la somma dei K, che le coppie con K = 0 abbiano S = 0 e che le sedute siano tutte presenti.
- **Riconciliazione dal record.** `riconcilia_record.py` legge solo registro della riserva e rapporto. Controlla:
  1. identità (impegno, finestra, scheda, codice, seme);
  2. sedute: date delle coppie uguali all'elenco impegnato, stesso ordine, senza doppioni;
  3. media esatta in frazioni;
  4. verdetto ricalcolato dalle sole coppie (L, U, segnale, esito, causa, requisiti);
  5. rapporto uguale byte per byte a quello rigenerato.

  Esiti sul candidato `67380cd`, su 3.13.18 e 3.9.25:
  - **5 su 5, «tutti»: true**;
  - promossa, 1.000 sedute;
  - media `0x1.88dd3fe19743fp-2`.

  Stesso risultato su `b9ec2f4`. Suite verdi (757 test) e prove A–G con osservato = atteso su entrambe le versioni. I mutanti sul candidato sono ancora in corso: te ne mando i conteggi a parte.
- **Media:** scritto «≈ 0,3836565 R». Il valore esatto del double è 0,3836564999999758…
- **Originali:** nell'archivio ci sono i JSON e i log nominati nelle ricevute, con l'indice delle impronte.
- **Q1, ambiente di riferimento:** al titolare ho proposto **DA-40**. Il mio consiglio è un'immagine dei test automatici riproducibile e qualificata con i riferimenti congelati di IA-02. Del collaudo IA-02, che ho eseguito io in un contenitore temporaneo, si conoscono versione e piattaforma, ma non un'immagine ricostruibile.
- **Q9, potenza:** la tratto come **requisito bloccante prima di qualunque accesso reale**. La scriverò nel contratto H-003 con la forma minima che hai indicato (ricetta sigillata, dati ammessi, semi, repliche, evento, conteggi, ricalcolo sotto il blocco riferito alla quota attuale) e con la prova di accettazione sintetica.
- **B:** oggi il rifiuto del comando NON rilascia la prenotazione. Il rilascio è un atto separato e registrato (`rilascia`). Ora il test controlla anche che, fra il rifiuto e il rilascio, lo stato resti «prenotato» (solo test, dopo il candidato).
- **G:** il nuovo tentativo dopo la correzione del registro dello scaricamento funziona. La traccia però è solo indiretta: nell'impegno finisce l'impronta del registro corretto, ma il tentativo fallito non lascia eventi. Vedi la domanda Q3.

2. NUOVO, DALLA MIA REVISIONE CRITICA (allegata)
- **Due lacune nei miei test, trovate da me rileggendo (solo test, il codice non cambia):**
  - #139 non era provato quando la prima verifica ha già l'esito. Il mutante PR14, che limitava l'unicità alle verifiche senza esito, sopravviveva: ora c'è il test e PR14 è ucciso;
  - nessun test faceva passare dall'esecutore la ripresa dopo una caduta durante la lettura. Ora c'è: stessa autorizzazione (j, quota, impegno), una sola apertura, una voce «verifica», un esito.

  Per questo il candidato è diventato `67380cd`. Il codice del perimetro è identico byte per byte a `b9ec2f4`.
- **Autorizzazione locale prima della lettura.** L'esecutore legge la finestra subito dopo aver scritto l'autorizzazione sul disco, prima del commit e del push. Un ripristino locale fra la lettura e il commit cancellerebbe il consumo. Ho proposto al titolare **DA-41**: si legge solo dopo che l'ancora conferma l'autorizzazione sulla versione remota.
- **Manifesto e registri veri.**
  - Il BID fino al 07/06/2009 era in cache prima che esistesse il registro per giorno.
  - `--riprova-vuoti` aggiunge una seconda riga valida per lo stesso giorno.
  - Una riga del lato o del mercato sbagliato, in qualunque data, compare fra le anomalie di ogni finestra.

  Il manifesto blocca in tutti questi casi: il verso è giusto, ma potrebbe rendere inutilizzabili interi anni. Ho scritto uno strumento di diagnosi, test prima e mutanti 13/13, che conta le anomalie per tipo, lato e anno, solo conteggi e date. Il titolare l'ha eseguito sul Mac (ricevuta allegata, `RICEVUTA-DIAGNOSI.md`). Il manifesto blocca in tre casi, e nessun file è alterato: tutti i file con una riga hanno l'impronta registrata (ASK 6.878 su 6.878, BID 5.023 su 5.023).
  - **BID dal 01/01/2005 al 07/06/2009:** 1.619 giorni «omessi». Sono i file scaricati prima del registro per giorno.
  - **BID 2009–2011:** 236 giorni con due righe valide. In tutti la stessa impronta, uguale al file, registrata il 16/11, quando due scaricamenti hanno girato insieme (#60).
  - **Sviluppo:** tutti i 1.094 giorni «omessi» su entrambi i lati, perché è stato scaricato prima del registro. **Oggi lo screening di qualunque scheda si fermerebbe.**

  Il codice del perimetro non ha difetti: il controllo sui registri veri andava fatto quando ho scritto il manifesto, ed è un mio errore di ordine.

3. DOMANDE (solo metodo)
- **Q1 (DA-41).** Leggere solo dopo che l'autorizzazione è sulla versione remota chiude il ripristino locale. Con il piano Free resta però possibile riscrivere la storia remota (push forzato). La difesa contro questo, cioè la storia completa e un riferimento conservato altrove, è sufficiente? Oppure serve un testimone esterno all'autorizzazione, per esempio l'impronta dell'autorizzazione mandata a te o a Gemini prima della lettura?
- **Q2 (manifesto sui registri veri), con i numeri della ricevuta.** Propongo:
  - **A1:** il manifesto accetta più righe valide per lo stesso giorno e lato **solo se identiche** in esito, byte e impronta; righe diverse continuano a bloccare;
  - **B1:** registrazione a posteriori dei file già in cache, con «in-cache-non-registrato» e l'impronta di oggi, per i 1.619 giorni del BID e per lo sviluppo. Procedura scritta, copia dei registri prima, conteggi e impronte prima e dopo nel repository.

  Alternativa a B1 per la riserva: quarantena dei 1.619 giorni, cioè circa 1.100 sedute in meno e le finestre da circa 4 a circa 3. Per lo sviluppo non c'è alternativa.

  Domande:
  - A1 è accettabile, oppure un doppione identico va trattato come segnale di un processo difettoso e quindi va bloccato?
  - B1 attesta i file **come sono oggi**. Le ancore sono le copie con impronta del 18/11 e del 22/11, che non si aprono, e il consuntivo del 22/11. Bastano? Quali controlli renderebbero B1 non manipolabile, rispetto al modello di minaccia D-24?
  - Per i giorni vuoti del fine settimana, «in-cache-non-registrato» darebbe lo stato «dati» invece di «nessun dato». Va corretto prima (lo stato si ricava dai byte, zero = nessun dato), oppure è indifferente?
- **Q3 (traccia di G).** Il tentativo rifiutato per anomalie del manifesto va registrato nel registro della riserva, come evento senza consumo? Oppure basta che l'impegno successivo contenga l'impronta del registro corretto?
- **Q4 (R19).** Gemini aveva iniziato R19 su `1431190`. Per il contatore D-24 basta che dichiari valide le parti dei file non cambiati e rifaccia su `67380cd` le suite, i mutanti e la differenza? Oppure R19 va rifatto per intero sul candidato nuovo?

---
