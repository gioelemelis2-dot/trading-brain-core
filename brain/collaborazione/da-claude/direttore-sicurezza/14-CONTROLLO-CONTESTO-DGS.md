# Controllo del contesto del DGS (21/11/2026)

**Perché.** La conversazione con ChatGPT è lunga e il 19/11 si è fermata per il limite d'uso; il titolare teme che il DGS abbia perso informazioni per strada. Prima di farlo rispondere al messaggio 10, gli si chiede di **dichiarare che cosa vede ancora** e di rispondere a domande di cui Claude conosce la risposta. Così la perdita si misura, invece di supporla.

**Come si usa.**
- Si incolla il testo fra le due righe di trattini **nella stessa conversazione** del messaggio 10.
- **Modello:** lo stesso che risponderà al messaggio 10 (Astra). Conta la finestra di contesto della conversazione, non solo la forza del modello: uno più leggero potrebbe vedere ancora meno.
- La **chiave di correzione** in fondo **NON si incolla**: serve a Claude per valutare.

---

CONTROLLO DEL CONTESTO — prima di rispondere al messaggio 10

La conversazione è lunga e si è interrotta il 19/11 per il limite d'uso. Prima di rispondere al mio ultimo messaggio (il messaggio 10) devo sapere che cosa vedi ancora. NON rispondere ancora al messaggio 10.

Regole:
- Per ogni risposta scrivi una di queste etichette:
  [VISIBILE] = lo leggi ora in un messaggio della conversazione o in un file allegato (indica quale);
  [RICORDO] = non lo ritrovi nel testo visibile, ma lo ricordi;
  [NON SO].
- «Non so» vale più di una risposta indovinata. Non ricostruire per deduzione quello che non vedi.
- Rispondi in modo breve: al massimo una riga per domanda, una pagina in tutto.

PARTE 1 — Che cosa vedi
1. Il mio ultimo messaggio (messaggio 10): citane la prima riga e l'ultima riga che vedi.
2. Vedi l'ALLEGATO A (decisioni D-24 … D-45) e l'ALLEGATO B (specifica del modulo del verdetto)? Per ciascuno: sì / in parte / no. Se sì, cita il numero dell'ultima decisione che vedi nell'ALLEGATO A.
3. Quali tuoi documenti DGS-01 … DGS-11 vedi ancora per intero, quali solo in parte, quali non più?
4. Quali file allegati della conversazione puoi ancora aprire? (elenco dei nomi)

PARTE 2 — Domande di controllo
5. Il criterio D-31: con quale valore di L si promuove e con quale valore di U si boccia?
6. Il metro: tipo di bootstrap, lunghezza del blocco, numero di repliche B, tipo di intervallo, quota per coda.
7. I tre esiti del verdetto (D-35) e l'ordine in cui si applicano.
8. Lo screening sullo sviluppo (D-36): le tre condizioni.
9. I minimi per una verifica (D-37): sedute, trade, sedute attive.
10. Le regole di spesa della riserva (D-38): α totale, formula della quota α_j, parte protetta.
11. Quante verifiche, all'incirca, consente la riserva in tutto il progetto?
12. L'esempio avverso dell'audit con l'11,7% di promozioni false: che cosa si è scoperto?
13. Da quale data si possono guardare grafici e dati di XAUUSD e GBPJPY, e perché?
14. Che cosa chiede D-24 prima della verifica sulla riserva?
15. Che cosa ti è vietato come DGS (accessi e decisioni)?

PARTE 3 — Lacune
16. Elenca le informazioni che ti servirebbero per rispondere bene al messaggio 10 e che non vedi più.

Dopo questa risposta ti dirò se proseguire qui o ripartire in una conversazione nuova con un pacchetto aggiornato.

---

## Chiave di correzione (NON incollare)

| # | Risposta attesa | Fonte |
|---|---|---|
| 1 | Prima riga: «MESSAGGIO 10 AL DGS — solo metodo; nessuna decisione riservata al titolare.» Ultima: la riga «Funzioni: `segnale(iv)` … un equivalente dichiarato)» dell'ALLEGATO B | messaggio 10 |
| 2 | Entrambi sì; ultima decisione D-45. Se manca l'ALLEGATO B, il messaggio è stato diviso e la seconda parte non è arrivata | messaggio 10 |
| 3 | Dovrebbe vedere DGS-01 … DGS-11 (DGS-01 insediamento; 02 addendum governance; 03 gate 4 campione storico; 04 riserva multi-mercato; 05 passaggio a Claude; 06 riscontro risposta 7; 07 protocollo IA-02; 08 riscontro IA-02; 09 idee pubblicate, GBPJPY, ruoli; 10 revisione modello H-003; 11 controverifica audit). Una parte potrebbe essere in un'altra conversazione (dal 18/11 il titolare ne ha aperta una nuova) | `collaborazione/da-chatgpt/` |
| 4 | Libero: serve a sapere che cosa rimandare | — |
| 5 | Promuove se L > +0,20 R; boccia se U < +0,10 R | D-31 |
| 6 | Circolare a blocchi, blocco 10, B = 3.999, intervallo basic, 2,5% per coda | D-31, ALLEGATO B |
| 7 | Promossa / bocciata / non decidibile. Ordine: veto accertato → bocciata; dati inidonei, minimi mancanti o intervallo invalido → non decidibile; U < +0,10 → bocciata; L > +0,20 e requisiti → promossa; altrimenti non decidibile | D-35, ALLEGATO B |
| 8 | Media > +0,25 R, L > 0, potenza stimata ≥ 50% | D-36 |
| 9 | 1.000 sedute, 300 trade, 200 sedute attive | D-37 |
| 10 | α 5%, α_j = α/[j(j+1)]/m, nessuna parte protetta | D-38 |
| 11 | Circa 4 verifiche in tutto il progetto | messaggio 10, richiesta 1 |
| 12 | Era in gran parte un artefatto: vincite identiche, intervallo di ampiezza ~1e-13 accettato; con vincite realistiche 0/300 a −20 R e 15/300 a −50 R. Da qui D-44 (intervallo < 1e-9 R invalido) | DGS-11, messaggio 10 |
| 13 | Dal 15/11/2023: la riserva va dal 2005 a circa fine ottobre 2023 e non si deve contaminare guardandola | regola del progetto |
| 14 | Un giro dedicato a tutte le manomissioni, a qualunque costo, senza difetti critici o importanti, più 2 giri puliti consecutivi e la decisione del titolare sulla protezione del ramo | D-24 |
| 15 | Non accede a repository, worktree e cartelle dei dati; non prende decisioni riservate al titolare (date della riserva, regole di spesa, modelli delle ipotesi) | istruzioni del progetto |

**Regola per decidere (proposta di Claude, la decisione è del titolare):**
- **si prosegue nella stessa conversazione** se l'ALLEGATO A e l'ALLEGATO B sono visibili e al massimo 2 risposte su 11 (5–15) sono sbagliate o «non so», rimandandogli solo quello che dichiara mancante;
- **si riparte in una conversazione nuova** con un pacchetto di ripartenza preparato da Claude (istruzioni del progetto, decisioni aggiornate, DGS-10 e DGS-11, messaggio 10) se manca un allegato del messaggio 10, se gli errori sono 3 o più, o se una risposta sbagliata è data come [VISIBILE] o [RICORDO] invece di «non so».
