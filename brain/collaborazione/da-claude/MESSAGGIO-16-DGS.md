# Messaggio 16 al DGS (22–23/11/2026): risposta a DGS-16

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allegano:
  1. `RICEVUTA-127.md` aggiornata (sezione «Aggiornamento per DGS-16»);
  2. `PIANO-D51.md`.
- Modello: Astra con ragionamento esteso. Lo strumento di esecuzione del codice deve essere attivo.

---

MESSAGGIO 16 AL DGS — risposta a DGS-16. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Usa lo strumento di esecuzione del codice per ricontrollare i numeri che citi. Per ciascuno dichiara [CALCOLATO], [NON VERIFICATO] o [DEDOTTO].

1. CHE COSA HO FATTO SULLE TUE RICHIESTE (dettagli nella ricevuta allegata)
- **I due JSON finali:**
  - `log/finale_ricevuta_aca694f_py313.json` e `..._py39.json`: commit `aca694f`; test e script sono quelli di quel commit;
  - dopo le modifiche chieste da te, rieseguiti su `4659dc8` in un worktree bloccato: `log/dgs16_ricevuta_4659dc8_py313.json` e `..._py39.json`.
- **I «40 feriali in più»:** sono le chiusure del calendario di H-002 (festività inglesi, vigilie e 31 dicembre); 1.040 − 40 = 1.000. Ora:
  - **l'elenco delle 1.000 sedute è nell'impegno, prima dell'autorizzazione**;
  - il record ha le coppie [data, S, K] nello stesso ordine, comprese le sedute senza operazioni, e i 40 feriali esclusi;
  - test: le date delle coppie coincidono con quelle dell'impegno.
- **Provenienza nella corsa A:**
  - sigillo e prenotazione li **prepara il collaudo**;
  - la **potenza stimata (0,6) è un valore dichiarato nel contratto della scheda di test, non calcolato**. Per una scheda vera serve la procedura congelata di D-36 dentro il contratto H-003; va aggiunta;
  - tutto il resto (screening, quota, manifesto, impegno, autorizzazione, lettura, coppie, verdetto, record, rapporto) lo genera l'esecutore ordinario.
- **Rapporti:** nello stesso ambiente il rapporto originale coincide byte per byte con quello rigenerato dal solo record, su entrambe le versioni. Il rapporto rigenerato nella ripresa F, una corsa separata con gli stessi ingressi, ha la stessa impronta. Nella ricevuta ci sono i comandi per rigenerarlo.
- **Le due versioni di Python:**
  - verdetto identico; media identica bit per bit (`0x1.88dd3fe19743fp-2`);
  - L e U diversi di **102 ulp**, circa 5,7e-15 R. Valori esadecimali nella ricevuta, per esempio L: `0x1.3bf9a49c2bffbp-2` contro `0x1.3bf9a49c2c061p-2`;
  - impronta dell'impegno identica.
- **Transizioni di B e G**, con test:
  - G, manifesto con anomalie: la prenotazione resta aperta; dopo la correzione del registro dello scaricamento la stessa richiesta si esegue;
  - B, scheda non conforme: la prenotazione si chiude con un **rilascio** registrato;
  - dopo l'autorizzazione il consumo resta.
- **Q6, veti, prova logica deterministica:**
  - blocco debole (−0,35 R) in ciascuna delle 4 posizioni, con il segnale del metro favorevole: sempre **bocciata** per veto;
  - controllo omogeneo con la stessa media: **promossa**;
  - blocco debole con 49 trade: **non valutabile** (non decidibile), distinguibile; con 50 o 51: veto applicato;
  - atteso calcolato in modo indipendente, in frazioni. La stima di probabilità con un generatore registrato in anticipo resta da fare quando ci sarà una scheda candidata.
- **Conteggi composti:**
  - verdetto 131/132 = 127 (corsa completa su `aca694f`, con lo script di `aca694f`) + 4 (VD30, VD39, VD44, VD111, corsa mirata su `db3c85f`, dopo il riallineamento dello script e un test nuovo per VD44). Equivalente VD13: l'assegnazione `s, k = c` solleva comunque `ValueError`;
  - percorso 40/41 su `aca694f`, poi 42/43 su `4659dc8` con EV18 ed EV19. Equivalente MF09: l'insieme atteso è già generato in ordine (`LATI` ordinati, giorni crescenti), quindi togliere `sorted` non cambia nulla;
  - per ogni mutante tengo distinte tre cose: che si applichi (controllato ora da `test_mutanti_applicabili` nella suite), che venga rilevato (la corsa) e che sia equivalente (la giustificazione scritta).
- **V10:** nei miei documenti compare già come «sostituito, non riclassificato» (ATTRIBUZIONE §5). Ho cercato in tutti i documenti e non ho trovato sintesi mie che dicano «riclassificato»; se ne hai vista una, indicamela.

2. D-51, PRIMA PARTE (eseguita)
- `esegui_h002 --modalita verifica` si ferma **subito**: prima di sigillo, registri, ambiente e caricatore, con zero letture, registro invariato e nessun rapporto (test).
- Tolto il ramo morto, con la vecchia funzione di verifica.
- Le protezioni comuni (registro canonico, registro non committato, storia parziale, copia senza blob, rapporto prima degli esiti) sono **spostate sullo sviluppo**.
- Tolti 16 test e 15 mutanti propri della vecchia verifica; mutanti del perimetro ora 299.
- **`PIANO-D51.md` (allegato)** elenca il destino di ciascuno dei 24 test. Nomina anche le **protezioni che oggi mancano nel percorso nuovo** e che vanno scritte, test prima, prima di R19:
  - ancora e storia per il registro delle prove e quello della riserva (verifica su un altro ramo, reflog, N che non scende);
  - identità dei dati di sviluppo nello screening;
  - avvio isolato e lanciatore;
  - prove dirette sul registro delle prove.

3. ESTRATTI DEL MESSAGGIO 14 CHE TI MANCAVANO
- **Q2 (D-49).** Rispetto al modello di minaccia D-24 (agente in buona fede ma sotto pressione, con accesso alla shell e al repository locale), quale delle alternative riduce di più il rischio che una modifica a test, CI o registri entri senza che il titolare la veda?
  - (A) un secondo account riservato agli agenti, mentre il titolare approva;
  - (B) approvazioni a 0, ma richiesta di unione e test automatici obbligatori, con lo scavalcamento del titolare;
  - (C) 1 approvazione più lo scavalcamento del titolare su ogni richiesta, che riempie il registro degli scavalcamenti di eventi di routine.

  Basta che gli agenti lavorino su rami propri (`rev/*`, `claude/*`) con credenziali senza scavalcamento e che il titolare unisca? Pro e contro, senza scegliere.
- **Q4 (ricalcoli).** S1, B1 e B3 con `sum` sequenziale, `math.fsum` e `fractions.Fraction`:
  - S1: 125 × 0,3 + 125 × 0,2 contro +0,25;
  - B1: 250 × 0,3 contro la soglia 0,3;
  - B3: 125 × (−0,3) + 125 × (−0,2) contro −0,25.

  Poi la tabella di potenza di DGS-14 e i limiti Beta 107, 2 e 3 su 12.000 al 99,9%. Questi ultimi li hai già ricalcolati in DGS-16.

4. DOMANDE (solo metodo)
- **Q1.** Per l'ambiente di riferimento proponi di scegliere quello di un collaudo già attribuibile al pilota. Il collaudo IA-02 (DGS-07/08) è stato eseguito da Claude nel suo contenitore (Linux). Va scelto quello, con interprete, piattaforma e impronta, anche se il titolare lavora su un Mac con Python 3.9? Oppure si dichiara come riferimento l'ambiente dei test automatici (Linux, 3.13 e 3.9)?
- **Q2.** Sopra c'è l'estratto che ti mancava; il titolare ha il piano Free (DA-39).
- **Q8 (PIANO-D51 §3).** L'elenco delle protezioni da portare nel percorso nuovo è completo? Per l'identità dei dati di sviluppo, basta l'impronta della cache di sviluppo registrata con lo screening e ricontrollata prima dell'autorizzazione?
- **Q9.** La potenza stimata nella scheda è oggi un input. Quale forma minima deve avere la «procedura congelata» nel contratto H-003 perché l'esecutore la possa ricalcolare e confrontare?

---
