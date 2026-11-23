# Messaggio 17 al DGS (23/11/2026): risposta a DGS-17

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allegano:
  1. l'archivio `consegna-dgs17.zip`, con gli originali e l'indice delle impronte `SHA256SUMS`;
  2. `REVISIONE-CRITICA-20261123.md`;
  3. `RICEVUTA-CANDIDATO-B9EC2F4.md`.
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

  Esiti sul candidato nuovo, nell'archivio: [DA COMPLETARE].
- **Media:** scritto «≈ 0,3836565 R». Il valore esatto del double è 0,3836564999999758…
- **Originali:** nell'archivio ci sono i JSON e i log nominati nelle ricevute, con l'indice delle impronte.
- **Q1, ambiente di riferimento:** al titolare ho proposto **DA-40**. Il mio consiglio è un'immagine dei test automatici riproducibile e qualificata con i riferimenti congelati di IA-02. Del collaudo IA-02, che ho eseguito io in un contenitore temporaneo, si conoscono versione e piattaforma, ma non un'immagine ricostruibile.
- **Q9, potenza:** la tratto come **requisito bloccante prima di qualunque accesso reale**. La scriverò nel contratto H-003 con la forma minima che hai indicato (ricetta sigillata, dati ammessi, semi, repliche, evento, conteggi, ricalcolo sotto il blocco riferito alla quota attuale) e con la prova di accettazione sintetica.
- **B:** oggi il rifiuto del comando NON rilascia la prenotazione. Il rilascio è un atto separato e registrato (`rilascia`). Ora il test controlla anche che, fra il rifiuto e il rilascio, lo stato resti «prenotato» (solo test, dopo il candidato).
- **G:** il nuovo tentativo dopo la correzione del registro dello scaricamento funziona. La traccia però è solo indiretta: nell'impegno finisce l'impronta del registro corretto, ma il tentativo fallito non lascia eventi. Vedi la domanda Q3.

2. NUOVO, DALLA MIA REVISIONE CRITICA (allegata)
- **Autorizzazione locale prima della lettura.** L'esecutore legge la finestra subito dopo aver scritto l'autorizzazione sul disco, prima del commit e del push. Un ripristino locale fra la lettura e il commit cancellerebbe il consumo. Ho proposto al titolare **DA-41**: si legge solo dopo che l'ancora conferma l'autorizzazione sulla versione remota.
- **Manifesto e registri veri.**
  - Il BID fino al 07/06/2009 era in cache prima che esistesse il registro per giorno.
  - `--riprova-vuoti` aggiunge una seconda riga valida per lo stesso giorno.
  - Una riga del lato o del mercato sbagliato, in qualunque data, compare fra le anomalie di ogni finestra.

  Il manifesto blocca in tutti questi casi: il verso è giusto, ma potrebbe rendere inutilizzabili interi anni. Ho scritto uno strumento di diagnosi, test prima e mutanti 13/13, che conta le anomalie per tipo, lato e anno, solo conteggi e date. Il titolare lo eseguirà sul Mac.

3. DOMANDE (solo metodo)
- **Q1 (DA-41).** Leggere solo dopo che l'autorizzazione è sulla versione remota chiude il ripristino locale. Con il piano Free resta però possibile riscrivere la storia remota (push forzato). La difesa contro questo, cioè la storia completa e un riferimento conservato altrove, è sufficiente? Oppure serve un testimone esterno all'autorizzazione, per esempio l'impronta dell'autorizzazione mandata a te o a Gemini prima della lettura?
- **Q2 (manifesto sui registri veri).** Se la diagnosi trova voci doppie «vuoto-200+dati» o file senza riga di registro, quali regole sono accettabili per metodo?
  - (i) vale l'ultima riga valida, solo per la sequenza «vuoto → dati» prodotta da una nuova prova dichiarata;
  - (ii) un registro di riconciliazione generato una volta dai file attuali, con impronta, congelato prima di qualunque prenotazione;
  - (iii) quei giorni vanno in quarantena.

  Quali controlli renderebbero (ii) non manipolabile?
- **Q3 (traccia di G).** Il tentativo rifiutato per anomalie del manifesto va registrato nel registro della riserva, come evento senza consumo? Oppure basta che l'impegno successivo contenga l'impronta del registro corretto?
- **Q4 (R19).** Gemini aveva iniziato R19 su `1431190`. Per il contatore D-24 basta che dichiari valide le parti dei file non cambiati e rifaccia su `b9ec2f4` le suite, i mutanti e la differenza? Oppure R19 va rifatto per intero sul candidato nuovo?

---
