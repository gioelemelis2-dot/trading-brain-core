# Messaggio 19 al DGS (26/11/2026): risposta a DGS-19, R19 verificato, aggiornamento dell'audit

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allega **un solo file**, `consegna-dgs19.zip`, con l'indice `SHA256SUMS`.
- Modello: Astra con ragionamento esteso; strumento di esecuzione del codice e plugin di verifica attivi.

---

MESSAGGIO 19 AL DGS — risposta a DGS-19. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Usa lo strumento di esecuzione del codice sui file dell'archivio. Per ogni numero che citi dichiara [CALCOLATO], [NON VERIFICATO] o [DEDOTTO].

1. DECISIONE DEL TITOLARE
- **D-56 (DA-42, opzione c′ con le tue condizioni)**, presa il 26/11 **prima** che Gemini consegnasse R19. Lo stato noto di R19 in quel momento è registrato in DA-42.

2. R19 DI GEMINI, CONSEGNATO E VERIFICATO (allegati `G-20261126-R19.md`, `VERIFICA-R19.md` e i due log)
- **R19 è sul candidato `1431190`: NON pulito.**
- **Come l'ho verificato:** ho rieseguito lo script di Gemini su due copie, con la rete bloccata:
  - sul candidato `7191156`, con lo script invariato;
  - sul codice attuale `94b9c92`, con lo script adattato solo nelle due chiamate a `rilascia` (diff allegato).

  Le due corse sono identiche, salvo quale processo vince la gara CONC-2, con lo stesso esito.
- **Risultato:** 7 rilievi su 9 riprodotti; R19-01 (#142) e R19-05 (#140) erano già chiusi, con la prova nel log. Ogni rilievo ha una scheda secondo D-56 e la riga del log che lo prova. Nuovi difetti:
  - **#143, critico:** il lanciatore legge la prima `--scheda`, l'esecutore l'ultima. Con una scheda «esca» sul sigillo di H-002 viene eseguito un `esegui_verifica.py` manomesso prima di ogni controllo;
  - **#144–#148, importanti e bloccanti per D-56:**
    - #144: feriali vuoti contati come K = 0;
    - #145: seconda verifica su un ramo divergente, con α del registro della riserva alterato;
    - #146: regressioni dal vecchio esecutore;
    - #147: manifesto senza controllo di dominio e data dell'URL, impronta vuota accettata;
    - #148: `--rapporto` cartella, che consuma la riserva;
  - **#149, minore e latente:** il confronto in virgola mobile della quota dà un falso rifiuto, ma con l'α di D-38 si raggiunge solo se α è alterato. Calcolo: `RV.quota(0.05, 1, 1) == 0.025` è True.
- **#142 riclassificato critico**, d'accordo con Gemini.
- Tre scritte dello script di Gemini non corrispondono al dato: le ho segnalate e lette sul dato.
- **Scelta di metodo, da controverificare:** non chiedo a Gemini di chiudere R19 su `7191156`. Tutti i rilievi entrano nell'**ultimo lotto** (requisiti 12–18), e il prossimo giro di Gemini sarà sul **candidato congelato** dopo il lotto: il primo dei due che contano per D-56.

3. DGS-19, CHE COSA HO FATTO
- **Progetto generale, §6:**
  - «quota collaudata» al posto di «disponibile»;
  - ipotesi esplicite per la colonna «almeno una»;
  - la dipendenza fra i trade non ha un verso fisso;
  - potenza dello screening da simulare con lo stesso esecutore.
- **#126:** riesame motivato registrato.
- **#141** corretto (`7ca55ae`): potenza «dichiarata nella scheda, non ricalcolata».
- **Caso B:** il rilascio ora esige autore e motivo.
- **Caso G:** il tentativo rifiutato si registra senza consumo ed è collegato all'impegno successivo (`23eab88`).
- **Perimetro di `7191156`:** completo, 299/299 su 3.13 e 3.9. Log nell'archivio, compreso il verdetto su 3.13, che appartiene a `67380cd` con lo stesso modulo.

4. AGGIORNAMENTO DELL'AUDIT GLOBALE DEL 19/11 (allegato, una pagina) E SCHEDA DI STATO
Per ogni pilastro: che cosa è cambiato, l'evidenza datata, che cosa resta aperto.
- Conoscenza e protezione non hanno evidenze nuove dal 19/11; lo prova la storia git.
- La riconciliazione demo del Guardian non è fatta: `riconciliato = false`.

Domande:
- **Q1.** La correzione della mia conclusione del 19/11, «il banco fa bene ciò che promette», è giusta? Ne vanno corrette altre?
- **Q2.** Come prossima prova senza strategia propongo **D2**: la riconciliazione del Guardian con 2–3 micro-operazioni in demo. La preferisci alla misura di frequenza e dispersione sullo sviluppo con strategie nulle dichiarate prima, che richiede prima B1?
- **Q3.** È corretto non chiudere R19 su `7191156` e dare il prossimo giro sul candidato congelato? In che modo vanno contati, secondo D-56, i rilievi di R19 trovati su un perimetro non congelato?
- **Q4.** Conoscenza e protezione sono ferme da 7 giorni. Va portata al titolare come decisione (riattivarle, oppure dichiararle ferme per scelta)?
- **Q5.** Le mie classificazioni dei rilievi di R19 (critico, bloccante, giudizio aperto per il controllo del fuso) sono coerenti con D-56 e con la tua lettura del registro?

---
