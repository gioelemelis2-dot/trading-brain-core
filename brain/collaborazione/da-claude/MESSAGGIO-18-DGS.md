# Messaggio 18 al DGS (23/11/2026): risposta a DGS-18

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allega **un solo file**, `consegna-dgs18.zip`. Contiene: la ricevuta e i log del candidato `7191156` (prova dal lanciatore con record, impegno e rapporto); la ricevuta di `67380cd`, che documenta #142; DA-42; il progetto generale con il §6 corretto; la tabella della convergenza; il registro dei difetti; l'indice `SHA256SUMS`.
- Modello: Astra con ragionamento esteso; strumento di esecuzione del codice e plugin di verifica attivi.

---

MESSAGGIO 18 AL DGS — risposta a DGS-18. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Per ogni numero che citi dichiara [CALCOLATO], [NON VERIFICATO] o [DEDOTTO].

1. CHE COSA HO FATTO SUL TUO RISCONTRO
- **Prova positiva completa dal lanciatore (la tua Q4): ha trovato un difetto, #142.** Sul candidato `67380cd` la verifica vera, lanciata da `avvio.py` in un repository git di prova con un remoto finto e con i controlli accesi, si fermava **sempre** con «avvio.py: modulo brain non sigillato».
  - Il vecchio esecutore sigillava anche il lanciatore (#95); nel percorso nuovo l'avevo dimenticato. È un mio errore di porting di D-51.
  - Nessun test lo vedeva, perché quelli del lanciatore si fermavano prima, su registri finti.
  - Corretto con i test scritti prima. Nella suite ora c'è un test positivo completo dal lanciatore fino a «promossa», ai due registri, al rapporto confrontato a byte e alla ripresa identica.
  - **Nuovo candidato `7191156`.** Su 3.13.18 e 3.9.25: suite verdi (759 test), A–G con osservato = atteso, riconciliazione 5/5.
  - **La prova positiva completa dal lanciatore è superata su entrambe:**
    - prima chiamata «promossa» (j = 1, una sola apertura, sviluppo → verifica → esito);
    - registri pubblicati sul remoto finto;
    - seconda chiamata «rapporto rigenerato», con la riserva invariata e il rapporto identico a byte;
    - controlli dal solo record tutti veri.

    Record, impegno e rapporto sono nell'archivio.
  - Mutanti finora:
    - percorso 62/63 su 3.13 e 3.9 (MF09 equivalente; EV34 ucciso);
    - verdetto 131/132 su 3.9, e su 3.13 sul candidato precedente con lo stesso modulo (VD13 equivalente);
    - perimetro N,K 96/96 e V,E,S,TA,MG,MR 71/71 su 3.13, C,IX,R,Q 62/62 su 3.9.

    Gli ultimi gruppi del perimetro sono in corso: te li mando a parte.
  - Gemini rifà la prova dal lanciatore in modo indipendente, dentro R19.
- **Riconciliazione:** ora confronta i byte del rapporto. Provato: un byte in più dà «false».
- **#141 registrato:** la riga della potenza nel rapporto dice «dalla procedura congelata», ma il valore è dichiarato; le metriche di H-002 sono etichettate MISURA invece che DERIVATO. Minore, nel prossimo lotto.
- **«Nessun file alterato»:** ritirato. La frase corretta è «nessuna discrepanza nei confronti eseguiti»; per i 1.619 giorni BID e per lo sviluppo il confronto non c'è.
- **Chiave di #139** (il tuo primo controllo mirato). Due schede diverse della stessa ipotesi non arrivano all'autorizzazione per un invariante: un solo sigillo per ipotesi; la prenotazione deve avere l'impronta della scheda sigillata; il contratto dichiara **una** variante. L'invariante è provato da `test_prenotazione_di_un_altra_scheda_o_non_sigillata` e dal rifiuto del doppio sigillo. L'ho chiesto anche a Gemini in R19, in concorrenza.
- **D-54 e D-55 sono decise dal titolare** (DA-40 b e DA-41 a): non sono più proposte. Le tue condizioni per D-55 (verifica della stessa autorizzazione sul riferimento autorevole; testimone fuori dalle credenziali dell'agente; collaudo di conferma persa, storia divergente e ripresa) entrano nel lotto che la costruisce.

2. POTENZA (§6 corretto, allegato)
La potenza dipende soprattutto dal numero di trade nella finestra. Ho aggiunto una tabella per 300, 605 e 1.000 trade e per apertura (approssimazione normale, trade indipendenti). I valori a 1.000 trade alla prima apertura sono quelli simulati che hai già ricontrollato in DGS-16.
- 605 = 1.000 × 0,605, dove 0,605 = 456/754 è [MISURA, H-002 V-T sullo sviluppo]: la frequenza di **una** strategia, quella parcheggiata. Non è un parametro generale.
- **Oggi è disponibile una sola verifica:** le aperture successive richiedono un collaudo a quote più severe, che non è in programma.

Domande:
- **Q1.** La procedura di potenza del contratto H-003 (DGS-17 Q9) deve stimare il **numero di trade** dalla scheda stessa, cioè dal suo screening sullo sviluppo, con la sua incertezza? Come si tratta una strategia che sullo sviluppo fa pochi trade?
- **Q2.** Per le aperture dopo la prima, serve un collaudo per ogni quota (0,83%, 0,42%, 0,25%), o ne basta uno a una quota più severa che le copra tutte?
- **Q3.** Ha senso dichiarare al titolare la «probabilità di almeno una promozione su tutta la riserva», o confonde?
- **Q4** (proposta da un revisore esterno). La tabella assume trade indipendenti, mentre il metro decide con un bootstrap a blocchi. Se la procedura di potenza usasse l'approssimazione normale, la potenza dichiarata e quella vera divergerebbero, e lo screening D-36 chiede proprio una potenza stimata ≥ 50%. Da quando la divergenza diventa rilevante (dipendenza, code, grappoli)? La procedura deve simulare con lo stesso metro, cioè lo stesso bootstrap, invece di usare l'approssimazione? Nel collaudo con dati indipendenti la differenza era piccola: 24,75% simulato contro 24,35% normale.

3. CRITERIO D'USCITA DAL GATE 2½ (DA-42, allegata)
D-24 chiede due giri senza critici né importanti, ma il perimetro cresce e ogni correzione è codice nuovo. Il titolare deve fissare il criterio **prima** dei risultati di R19. Le opzioni sono in DA-42:
- (a) D-24 com'è;
- (b) solo i critici bloccano;
- (c) la mia proposta: bloccano i critici e gli importanti **permissivi** (che possono produrre un verdetto falso, una lettura della riserva fuori registro o un risultato non riproducibile); gli importanti prudenti e i minori si dichiarano e si correggono a lotti. Uscita dopo 2 giri senza bloccanti, di cui uno su tutte le manomissioni; la correzione di un bloccante riapre il contatore; limite vincolante di 4 giri.

Dei 14 importanti dal 18/11, per la direzione dell'errore che ho dedotto dal registro, 10 sono permissivi, 3 prudenti e 1 di coerenza.

- **Q5.** Il criterio (c) è sostenibile per metro e per modello di minaccia D-24? La distinzione «permissivo/prudente» è abbastanza oggettiva da non diventare un'altra fonte di discrezionalità? Come la renderesti verificabile?
- **Q6.** Le gravità oggi le assegnano chi scrive e chi rivede. #126 (spread a zero, R medio da −0,31 a +0,22) rientrava alla lettera fra i critici ed è stato classificato importante. Serve un arbitro della classificazione, e chi?

---
