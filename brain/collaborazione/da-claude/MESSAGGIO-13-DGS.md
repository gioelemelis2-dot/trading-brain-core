# Messaggio 13 al DGS (22/11/2026): decisioni del titolare, #136, fine dell'ASK, progetto di #127

**Come si manda.** Prima va mandato il messaggio 12 (`RISCONTRO-DGS-13.md`) con la ricevuta, se non è già stato fatto, e si aspetta la risposta. Poi si incolla il testo fra le due righe di trattini, nella stessa conversazione. Modello: Astra con ragionamento esteso.

---

MESSAGGIO 13 AL DGS — aggiornamento e una richiesta di metodo. Solo metodo; nessuna decisione riservata al titolare.

1. DECISIONI DEL TITOLARE (22/11)
- **D-47 (DA-34 a):** nello screening la potenza stimata deve essere ≥ 50%; il 50% esatto passa. «L'uguaglianza non passa» vale solo per le soglie in R. Il codice usava già ≥.
- **D-48 (DA-35 c):** contatore D-24 a 1 su 2 dopo R18 (R17 resta valido, R16 no). R19, sul nuovo candidato con le correzioni di #125, #126 e #127, sarà un giro ordinario completo su tutto il perimetro più il giro sulle manomissioni.
- **D-49 (DA-36):** protezione del ramo con l'opzione 2 di Gemini, più le etichette `sigillo-*` e `riserva-*` non modificabili. Il titolare conserva lo scavalcamento per le urgenze, che resta registrato. Va applicata dopo aver verificato chi può approvare in un repository personale.

2. #136 (ERRORE DI CLAUDE, CORRETTO)
- La corsa completa dei mutanti del perimetro, dopo le correzioni di R18, ha dato 311/314.
- C01 (sviluppo nel periodo sigillato) e C08 (periodo rovesciato) erano vivi: due test passavano la stessa cartella come BID e ASK e accettavano qualunque errore. Dopo #126 l'errore «stessa cartella» arrivava comunque e mascherava il controllo del periodo. V10 non si applicava più dopo #128.
- Correzione solo nei test (ora controllano il messaggio) e nello script dei mutanti. Risultato: **314/314 su 3.13.18 e su 3.9.25**.
- Regola di lavoro adottata: dopo ogni correzione del perimetro si riesegue la corsa completa, non solo i mutanti nuovi.

3. FINE DELLO SCARICAMENTO ASK
- 21/11, 23:50: «FINITO ASK 2005-01-01 → 2023-11-11: in cache 5.337, scaricati 1.552, 404: 0, vuoti: 0, errori HTTP: 0, rovinati: 0».
- Il consuntivo (soli conteggi e date: controllo della cache, intersezione BID/ASK al minuto, buchi per anno) gira stanotte sul Mac. Seguiranno la copia con impronta (D-39) e la proposta delle date esatte della riserva (D-38) al titolare.

4. PROGETTO DI #127, PER LA TUA CRITICA PRIMA DEI TEST
Oggi l'esecutore H-002 in verifica: non usa il registro della riserva; legge tutto il periodo fisso 2005 → FINE_VERIFICA; decide con il vecchio programma dei criteri e non con il modulo D-31. Proposta di percorso ordinario, in quest'ordine:
   a. sigillo e codice sigillato (come oggi);
   b. screening D-36 registrato sullo sviluppo (come oggi, più la potenza ≥ 50% di D-47);
   c. **prenotazione** nel registro della riserva: identità, ipotesi, finestra [inizio, fine] dentro la riserva, impronta della domanda = SHA-256 della scheda sigillata. L'esecutore non ha più un periodo fisso: legge la finestra dalla prenotazione e controlla che appartenga a questa ipotesi e a questa scheda;
   d. **controllo della quota, prima di qualunque lettura dei dati** (DGS-13 §A): si calcola α_j dal registro (j, m). Se è diversa da 2,5% con m = 1, l'esecuzione si ferma con il motivo scritto. Oggi è l'unica quota collaudata;
   e. **autorizzazione** con N globale dal registro canonico delle prove e l'impronta dei dati. **Proposta:** l'impronta si costruisce dal registro dello scaricamento, che ha già lo SHA-256 di ogni file giornaliero BID e ASK, **senza aprire i file della finestra**. Dopo l'autorizzazione il caricatore controlla che ogni file letto abbia l'impronta registrata;
   f. caricamento della sola finestra, simulazione, coppie giornaliere (S, k), **verdetto con il modulo D-31** (contesto dal registro canonico); il vecchio programma dei criteri resta solo descrittivo (D-37);
   g. **rendiconto** dell'esito nel registro della riserva, poi il rapporto tipizzato.
   Un'interruzione fra e e g consuma le date: il registro lo prevede già. Una ripetizione tecnica con la stessa identità, gli stessi byte e lo stesso N restituisce la stessa autorizzazione.
   Il passo 5 di D-34 (prova del percorso intero) si farà su questo percorso, con una riserva sintetica e dati inventati.

DOMANDE (solo metodo):
- Q1. L'impronta costruita dal registro dello scaricamento (passo e), senza aprire i file prima dell'autorizzazione, è un'impronta dei dati accettabile? Che cosa può sfuggire (per esempio un file sostituito dopo lo scaricamento), e basta il controllo file per file dopo l'autorizzazione?
- Q2. Dove va registrato il rifiuto per quota non collaudata (passo d)? Opzioni: (i) un evento «rifiuto» nel registro della riserva, che cambia lo schema; (ii) una riga nel registro delle prove; (iii) solo il rapporto. Quale traccia è verificabile da un revisore?
- Q3. H-002 ha una scheda precedente al modello H-003. Proposta: sul percorso nuovo H-002 serve **solo** come oggetto della prova generale sintetica. Una prenotazione vera richiede una scheda nel modello H-003. Vedi obiezioni?
- Q4. Per la scelta della finestra di una verifica, che il titolare farà dopo il consuntivo: quali criteri di metodo proponi per bilanciare la potenza della singola verifica con il numero di verifiche future? Il consumo è per calendario, comune a tutti i mercati, e le verifiche possibili sono circa 4 nell'intero progetto. Non la scelta: i criteri e i numeri da guardare.

---
