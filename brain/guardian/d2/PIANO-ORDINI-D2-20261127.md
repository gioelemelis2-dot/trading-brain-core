# Prova D2 · piano degli ordini e previsioni, scritti PRIMA delle operazioni · 27/11/2026, 17:00 italiane

**Regole:** li prepara Claude, li **esegue il titolare**, solo sul conto con l'etichetta **Demo** (server FirstPrudentialMarketsCY-Demo, valuta USD). Le previsioni valgono dall'ora del commit che contiene questo file. Numeri di conto e nome del titolare non si scrivono qui.

## Cancelli: niente ordini finché non sono tutti chiusi

1. Nell'app restano **solo conti demo**: quello senza «Demo» va rimosso dall'app.
2. **Tolleranze approvate** dal titolare (scheda D2, §4).
3. **Specifiche MT4 di XAUUSD lette e mandate a Claude.** Se la dimensione del contratto non è 100, o se la commissione è descritta diversamente da qui sotto, **Claude rifà le previsioni con un nuovo commit, prima di operare**.
4. Conto piatto: margine usato 0,00 (osservato alle 16:5x italiane: saldo ed equity 100.000,00 USD).

**Stato dei cancelli (27/11, dopo il commit delle previsioni):**
- 1: dichiarato dal titolare, da confermare con la foto dell'elenco dei conti;
- 2: approvato (D-60);
- 3: **chiuso** con le specifiche MT4 di **XAUUSD.cy** lette dal titolare (foto delle 17:1x):
  - cifre 2; livello degli stop 0; dimensione del contratto **100**;
  - calcolo del profitto CFD; calcolo del margine «Contracts»; margine hedge 0,00; **percentuale del margine 5,0%**;
  - swap in punti: long −54,02, short 32,30; spread fluttuante.

  Le previsioni sono **confermate senza modifiche**: contratto 100 e margine al 5%, come ipotizzato. **La commissione non compare nella finestra di MT4**, quindi resta valida l'ipotesi congelata H-a e si verifica sul primo ordine. Biglietto osservato prima di O1: Bid 3.622,52, Ask 3.622,71 (spread 0,19); conto piatto;
- 4: osservato.

## Versione ridotta (27/11, 16:4x UTC, su richiesta del titolare che ha poco tempo)

- **S1**, la vendita fuori piano aperta dal titolare: si chiude a mano entro la chiusura di venerdì, **senza modificare lo stop**; poi la foto dello Storico. Serve per la commissione.
- **O1** si fa quando il titolare ha tempo, anche nei giorni successivi, in modalità «imposta e dimentica»: Buy 0,01, S/L = Ask − 2,00, nessun T/P. Lo stop la chiude da solo; se non scatta, chiusura manuale quando capita. Le foto sono tre: biglietto, riga subito dopo l'apertura, Storico.
- **O2 e O3 sono annullati.** La vendita è coperta da S1, per P&L e margine. Le previsioni di O1 restano quelle del commit `57d2e2e`.
- Il limite «entro le 19:30» vale solo per S1. Per O1 basta non lasciarla aperta nel weekend.

## Gli ordini

Uno alla volta, **XAUUSD, 0,01 lotti**, a mercato, nessun take profit. Lo stop si inserisce nel biglietto prima di inviare l'ordine.

| Ordine | Lato | Stop (S/L) da scrivere nel biglietto | Come si chiude |
|---|---|---|---|
| **O1** | Acquisto (Buy) | prezzo **Ask** mostrato meno **2,00** | si lascia toccare lo stop; se dopo 30 minuti non è scattato, chiusura manuale |
| **O2** | Vendita (Sell) | prezzo **Bid** mostrato più **3,00** | chiusura manuale dopo circa 10 minuti |
| **O3** | Acquisto (Buy) | prezzo **Ask** mostrato meno **5,00** | chiusura manuale dopo circa 10 minuti, oppure allo stop se scatta prima |

Esempio con Ask a 3.770,40: lo stop di O1 è 3.768,40.

Tutto va chiuso **entro le 19:30 italiane**. È il venerdì dopo il Thanksgiving americano: la liquidità potrebbe ridursi prima della chiusura del weekend. Gli orari esatti si leggono nelle specifiche.

## Previsioni congelate

**Perdita lorda allo stop: del Guardian.** Calcolata con `g0.strumenti.perdita_allo_stop`, senza commissioni; script `d2/previsioni_d2.py`, output qui sotto.

```
O1 acquisto 0.01 lotti, stop a 2.00 USD: perdita lorda allo stop (Guardian) = 2.0000 USD [DERIVATO]
O2 vendita 0.01 lotti, stop a 3.00 USD: perdita lorda allo stop (Guardian) = 3.0000 USD [DERIVATO]
O3 acquisto 0.01 lotti, stop a 5.00 USD: perdita lorda allo stop (Guardian) = 5.0000 USD [DERIVATO]
```

- Al confronto si usa la **stessa formula** sui prezzi effettivi: |prezzo d'apertura eseguito − prezzo di chiusura eseguito| × 100 × 0,01.
- Il segno lo dà il lato. **Lo applica Claude, non il Guardian.**
- Se lo stop non è esattamente alla distanza prevista dal prezzo eseguito, conta la distanza **effettiva** fra apertura e S/L.
- La perdita *realizzata allo stop* si osserva solo se lo stop scatta. Una chiusura manuale verifica la formula al prezzo eseguito.

**Commissione: non è del Guardian.** È un'ipotesi del profilo demo, dalla specifica MT5 del 18/11: «6 USD per lotto, istantaneo per volume, deals in ingresso».

| Ipotesi | Previsione per ordine da 0,01 lotti | Stato |
|---|---|---|
| **H-a (congelata)** | **0,06 USD**, addebitati **all'apertura**, una sola volta | previsione |
| H-b | 0,06 all'apertura **e** 0,06 alla chiusura (0,12 in tutto) | alternativa dichiarata |
| H-c | 0,03 all'apertura e 0,03 alla chiusura (0,06 in tutto) | alternativa dichiarata |

**Margine usato: non è del Guardian.** Calcolo esterno attribuito al profilo demo: **5% del nozionale**, cioè leva 1:20 sull'oro (specifica MT5 del 18/11). Margine = prezzo d'apertura × 100 × 0,01 × 0,05. Esempio: a 3.770,00 vale **18,85 USD**.

Il valore va confermato con la specifica MT4, perché la leva della demo potrebbe essere diversa. La voce «Guardian riconciliato sul margine» resta comunque aperta.

## Che cosa fotografare per ogni ordine

| Momento | Foto |
|---|---|
| Subito prima di aprire | Riga del conto: saldo, equity, margine, margine libero. Deve comparire l'etichetta Demo |
| Biglietto dell'ordine, prima di inviare | Simbolo, volume 0,01, S/L |
| Subito dopo l'apertura | Riga dell'ordine (prezzo, S/L, commissione, swap, profitto) e riga del conto (margine) |
| Dopo la chiusura | Storico: prezzo e ora di chiusura, commissione, swap, profitto |

Alla fine, se possibile, l'estratto dall'area clienti di FP Markets.
