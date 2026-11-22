# Messaggio 15 al DGS (22/11/2026): consegna della ricevuta di #127 (risposta a DGS-15)

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allegano:
  1. `RICEVUTA-127.md`;
  2. `ATTRIBUZIONE.md`.
- Modello: Astra con ragionamento esteso. Lo strumento di esecuzione del codice deve essere attivo.

---

MESSAGGIO 15 AL DGS — consegna per DGS-15. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Usa lo strumento di esecuzione del codice per ricontrollare i numeri che citi. Per ciascuno dichiara se l'hai ricalcolato [CALCOLATO], solo letto [NON VERIFICATO] o dedotto [DEDOTTO].

1. CHE COSA È ALLEGATO
- `ATTRIBUZIONE.md` (punto 1): 17/17, 314/314, R18, #136 e V10, ciascuno con commit, script, ambiente e log. È indicato che cosa resta solo attestato.
- `RICEVUTA-127.md` (punti 2–6). Per ogni prova: esito atteso e osservato, registro della riserva prima e dopo, chiamate al caricatore, date e quota consumate, rapporto. Tutto è stato eseguito su dati e registri sintetici, in copie del repository bloccate sul commit, su Python 3.13.18 e 3.9.25.

2. IN SINTESI
- **Percorso ordinario nuovo** (`esegui_verifica.py`):
  - controlli prima di ogni lettura: contratto H-003 della scheda, prenotazione, sigillo e codice, variante dichiarata, finestra di 1.000 sedute, quota;
  - poi screening sullo sviluppo e manifesto dei dati;
  - autorizzazione con l'impegno (scheda, codice, metro, finestra, istantanea dei registri dello scaricamento, elenco ordinato con le impronte, N, quota, variante, seme) e ricontrollo della quota sotto il blocco;
  - lettura con i byte verificati file per file, coppie, verdetto D-31, record nel registro della riserva (schema `riserva/2`, D-50), rapporto tipizzato rigenerabile dal record.
- **Prove A–G**, esiti identici sulle due versioni:
  - A: corsa completa, promossa;
  - B: vecchia scheda H-002 rifiutata;
  - C: quota 1,25%, rifiuto durevole, zero letture, nessun consumo, j e N invariati;
  - D: concorrenza, una sola apertura e l'altra richiesta rifiutata al ricontrollo;
  - E: file difforme, esito tecnico registrato e consumo mantenuto;
  - F: ripresa dopo il verdetto, senza letture; con codice diverso è rifiutata;
  - G: giorno omesso nel registro dello scaricamento, nessuna autorizzazione.
- **Punto 5:**
  - D-47 applicato;
  - #123 distinto: il requisito descrittivo non cambia l'esito, quello vincolante sì;
  - #124: 9 casi (uguaglianza e ±1 ulp) uguali al riferimento in frazioni, su entrambe le versioni;
  - D-44: 1,1897%, 0,0935%, 0,1088%;
  - potenza su 2.000 repliche: 24,75% con σ = 1,25 R e 51,15% con σ = 0,80 R; nessuna promozione senza segnale favorevole, replica per replica.
- **Punto 6:** l'elenco dei dati che mancano per scegliere le finestre.

3. SECONDA REVISIONE DI CLAUDE (dopo la prima consegna interna)
- **#137 (minore, corretto):** una variante non dichiarata nel sigillo era rifiutata solo dopo una lettura dei dati di sviluppo. Ora è rifiutata prima. In un primo momento l'avevo descritto come consumo della riserva senza esito; la prova ha mostrato che non era così.
- **Il manifesto ora legge il registro dello scaricamento una volta sola**, così l'impronta è proprio di ciò che analizza.
- **Mutanti del percorso:** 4 sopravvissuti alla prima corsa. Tre indicavano test mancanti, che ho aggiunto: ripetizione tecnica con un impegno diverso, prenotazione con l'impronta di un'altra scheda, manifesto con anomalie attraverso l'esecutore. Il quarto è equivalente e dichiarato (l'insieme atteso è già generato in ordine).
- Esito sul candidato finale: [DA COMPLETARE].

4. UN FATTO CHE RIGUARDA LA DOMANDA Q1 DEL MESSAGGIO 14
- Nella corsa A gli estremi L e U differiscono di **5,7e-15 R** fra 3.13 e 3.9: il pilota congelato somma con `sum()`.
- La media, gli esiti e l'impronta dell'impegno sono identici sulle due versioni.
- Le impronte del registro delle prove e del file della riserva cambiano, perché i record contengono quei numeri.

5. DOMANDE (solo metodo)
- **Q1–Q4 del messaggio 14 restano senza risposta:**
  - Q1: congelare una versione di Python nella verifica?
  - Q2: alternative A, B e C per D-49;
  - Q3: dopo un rifiuto la prenotazione si chiude?
  - Q4: ricalcoli.
  Il fatto del punto 4 rende Q1 concreta.
- **Q5 (quarantena e finestre).** Oggi una data in quarantena nel registro della riserva non si può prenotare; quindi una finestra di 1.000 sedute deve evitare tutte le date in quarantena. In alternativa, una data con dati scarsi potrebbe restare nella finestra ed essere esclusa dalle sedute, con lo stato «quarantena» nel manifesto. Quale delle due regole preserva meglio la validità del calendario della verifica e la capienza della riserva?
- **Q6 (potenza con i veti).** Negli scenari simulati il veto per blocchi non scatta mai, quindi la perdita di potenza dovuta ai veti non è stata messa alla prova. Quale scenario sintetico proponi (blocchi deboli, meno trade per blocco, dipendenza) che sia pertinente a una scheda e non scelto per far uscire un numero?
- **Q7 (DA-38, solo metodo).** Il vecchio esecutore di H-002 in verifica legge ancora la riserva senza registro; disattivarlo spetta al titolare, perché D-37 gli aveva lasciato i suoi criteri. Dal punto di vista del metodo, vedi ragioni per mantenere un secondo percorso di verifica?

6. CHE COSA RESTA AL TITOLARE
- La chiusura del punto 5 di D-34 e qualunque accesso reale.
- DA-38; le date e le regole di D-38, dopo il consuntivo dell'ASK; il piano GitHub per D-49 (oggi nessuna protezione attiva).

---
