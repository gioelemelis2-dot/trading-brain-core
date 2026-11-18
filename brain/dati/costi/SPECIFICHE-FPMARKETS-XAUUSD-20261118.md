# Specifiche di XAUUSD presso il broker (rilevate il 18/11/2026)

**Fonte:** schermata «Specifiche» dell'app MetaTrader 5, conto **Raw** della società europea del broker (FP Markets, server di Cipro), simbolo **XAUUSD.cyr**. Lette dal titolare con saldo 0. **Nessun dato del conto è registrato qui.** Valori da ricontrollare prima di ogni uso, perché il broker può cambiarli.

| Voce | Valore | Nota |
|---|---|---|
| Cifre decimali | 2 | 1 punto = 0,01 USD per oncia |
| Dimensione del contratto | 100 | 1 lotto = 100 once |
| Spread | fluttuante | misura istantanea vista dal titolare il 18/11: 40 punti = 0,40 USD |
| Livello degli stop | 0 | nessuna distanza minima dichiarata |
| Valuta del margine e del profitto | USD | |
| Calcolo | Contratti | |
| Grandezza e valore del tick | mostrati «0.00» e «0» | arrotondamento dell'app; in pratica 0,01 USD = 1 USD per lotto |
| Grafico | per prezzo BID | come i dati Dukascopy del progetto |
| Esecuzione | a mercato; riempimento FOK/IOC | |
| Volume | min 0,01, max 20, passo 0,01 | |
| Swap | in punti: long −54,02, short +32,3; mercoledì triplo | conta solo per le posizioni tenute la notte |
| **Commissione** | **6 USD per lotto**, «istantaneo per volume, deals in ingresso» | addebitata all'ingresso: probabilmente l'intero giro (6 USD per 100 once = 0,06 USD/oncia). **Da confermare con un estratto conto** |
| Sessione quotazioni | lun–ven 01:00–24:00 (ora del server) | |
| Sessione trade | lun–gio 01:01–23:59, ven 01:01–23:58 (ora del server) | il server non è in UTC: il fuso va confermato |
| Margine | valore nozionale; circa 18.846 USD per lotto a circa 3.769 | equivale a una leva 1:20 sull'oro (non 1:30) |

**Confronto con la scheda G0 attuale:** la scheda usa 7,00 USD per lotto andata e ritorno; qui sono 6 USD, se l'interpretazione è giusta.

**Costo di un trade in R (esempio, IPOTESI):** spread 0,40 + commissione 0,06 = circa 0,46 USD per oncia.
- Con lo stop a 5 USD: circa 0,09 R a trade.
- Con lo stop a 15 USD: circa 0,03 R.
- Stop più larghi rendono i costi più leggeri in R. Lo spread vero varia con l'ora e va misurato dai tick.
