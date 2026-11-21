# Riscontro di Claude a DGS-13 (21/11/2026): messaggio 12 al DGS

**Come si manda.** Si incolla il testo fra le due righe di trattini, nella stessa conversazione, e si allega `RICEVUTA-PROVA-GENERALE-20261121.md`.

---

MESSAGGIO 12 AL DGS — riscontro a DGS-13. Solo metodo; nessuna decisione riservata al titolare.

1. NUMERI DI DGS-13: RICALCOLATI E CONFERMATI
- Limiti superiori esatti unilaterali al 99,9%, quantile Beta(0,999; k+1, 12.000−k): 1,1897% (k = 107), 0,0935% (k = 2), 0,1088% (k = 3).
- Ampiezza dell'intervallo della replica 1.904: 2,94e-15 R.
- Quote: 1,25% (due varianti alla prima apertura) e 0,8333% (seconda apertura).

2. RETTIFICA ACCOLTA (errore di Claude)
- Nel messaggio 11 ho riportato solo il controllo delle false promozioni. Con D-44 cambia anche quello delle false bocciature della cella 11: da 2 + 0 = 2 a 2 + 1 = 3, con limite da 0,0935% a 0,1088%.
- Entrambi restano sotto il 2,5% e il verdetto del collaudo non cambia.
- Registrato così nel registro delle modifiche.

3. RICEVUTA DELLA PROVA GENERALE (allegata)
- **Candidato del modulo e impronte:**
  - commit del codice eseguito e SHA-256 di `verdetto_d31.py` e del pilota nella ricevuta;
  - 17/17 test su Python 3.13 e 3.9, con l'elenco per caso;
  - rapporti finali tipizzati di M e N.
- **Percorso realmente eseguito:**
  - A e B: `orb_londra.simula` → coppie → verdetto (non l'esecutore `esegui_h002`);
  - C, D, E, I, J, K, M, N: coppie → metro collaudato → verdetto;
  - F, G, H, L, O e la seconda parte di M: decisore con l'intervallo fornito.
- **Ha ragione: il percorso intero non è stato eseguito, perché oggi non esiste.**
  - L'esecutore non usa né il modulo D-31 né il registro della riserva: è il difetto #127, trovato da Gemini in R18.
  - In più, la sua verifica userebbe tutto il periodo 2005–2023.
  - **Il punto 5 di D-34 resta aperto per il percorso intero:** scheda, sigillo, screening, prenotazione sintetica, verdetto e rapporto.
  - Lo preparo insieme alla correzione di #127. Il controllo della quota (§A) andrà **prima** dell'autorizzazione e della lettura dei dati, e il motivo del rifiuto resterà registrato.

4. ATTRIBUZIONE DELLE EVIDENZE DI R18 ALLE VERSIONI
- **R18 di Gemini** (punta `efcfcbc`, perimetro identico a `e476a9a`): tutto, compreso il primo giro del modulo del verdetto, **precede** #122 e #123 (`f0ee358`) e le correzioni di R18 (`f338381`).
- **Riproduzioni di Claude:**
  - R18-07, R18-08 e R18-09 sono rieseguiti sul modulo **dopo** #122 e #123 (`f0ee358`), e sono ancora presenti;
  - R18-01 è riprodotto sul codice del perimetro identico a `e476a9a`.
- **Dopo le correzioni** (test `e72af87`, codice `f338381`, mutanti `8f175b6`), rieseguiti da Claude:
  - 27/27 suite su 3.13 e 3.9;
  - mutanti del verdetto 117/118 su entrambe (VD13 equivalente);
  - mutanti nuovi del perimetro Q01–Q11: 11/11 su entrambe;
  - la corsa completa dei mutanti del perimetro è in corso.
- Il prossimo giro (R19) avverrà su un candidato nuovo, dichiarato con il suo commit.

5. ALTRI PUNTI
- **#123:** accolta la tua proposta. La parte in cui un indicatore descrittivo bloccava la promozione è riclassificata **importante** per il modulo; l'omissione nel rapporto resta minore.
- **#124:** per i casi di uguaglianza e quelli adiacenti farò un confronto con un riferimento in aritmetica esatta (frazioni), su 3.9 e 3.13. Se si adotta `math.fsum`, sarà su un candidato versionato.
- **§B (potenza con i veti):** recepito nel modello di scheda. Sugli stessi percorsi si contano F e P e si riportano la perdita (F−P)/M con gli intervalli binomiali e le cause fra i percorsi favorevoli. Una discordanza P > F è un difetto.
- **Uguaglianza al 50%:** resta al titolare (DA-34).

---
