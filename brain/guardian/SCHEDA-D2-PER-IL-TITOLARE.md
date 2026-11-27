# Prova D2 · scheda per il titolare, da leggere prima di aprire la demo · 27/11/2026

**Base:** D-57 (prova approvata), DGS-21 §B, DGS-22 §D2. Tutto ciò che segue sul Guardian l'ho verificato nel codice, al commit di questa scheda.

## 1. Che cosa il Guardian sa prevedere davvero

| Voce | Funzione del Guardian | Che cosa calcola, e in quale unità | Si confronta con |
|---|---|---|---|
| **Perdita lorda allo stop** | `g0/strumenti.perdita_allo_stop`, **senza** commissioni | \|ingresso − stop\| × dimensione del contratto × lotti, nella valuta del conto (con un cambio misurato, se il conto non è in USD). Tipo DERIVATO, condizionato a «stop eseguito al prezzo». Esempio illustrativo dimostrato: 0,01 lotti, 5 USD di distanza → **5,0000 USD** | Il **profitto lordo** del broker (OrderProfit in MT4, che **esclude** commissioni e swap) |
| **P&L lordo al prezzo eseguito** | La stessa funzione, con il prezzo di chiusura al posto dello stop | Il valore **assoluto**. **Il segno non lo calcola il Guardian**: lo applico io dalla direzione (acquisto/vendita), e lo dichiaro | Il profitto lordo del broker, con il segno |
| **Commissione** | **Nessuna.** Il Guardian la riceve come dato e la somma alla perdita | Non la prevede. La previsione è la **convenzione tariffaria** scritta prima: oggi «6 USD per lotto, all'ingresso», letta su **MT5** (18/11). Non sappiamo se è per lato o per il giro completo | La commissione del ticket nell'estratto |
| **Margine richiesto dal broker** | **Nessuna.** La funzione `limiti.margine` del Guardian è un'altra cosa: la distanza dell'equity dal limite di drawdown della prop firm | Il Guardian **non lo prevede**. Si può solo registrare il valore osservato, oppure un calcolo esterno attribuito al profilo demo (non al Guardian) | Il margine del conto (AccountMargin) |

**Conseguenza:** la prova può riconciliare **solo la perdita lorda allo stop** e la sua formula al prezzo eseguito. La voce «Guardian riconciliato sul margine» resta **aperta** comunque (DGS-22). Sulla commissione la prova verifica la convenzione tariffaria, non un calcolo del Guardian.

## 2. Prima di operare: da fotografare e mandarmi

1. **Specifiche di XAUUSD sulla demo MT4 Raw:** nome esatto del simbolo, cifre decimali, dimensione del contratto, passo e valore del tick, commissione (e la scritta che spiega quando si addebita), margine o leva, swap, orari. Le specifiche che abbiamo sono di **MT5**, non della demo.
2. **Conto:** valuta, leva, saldo, equity, margine usato (deve essere 0: conto piatto, nessuna posizione), margine libero.

Con questi dati preparo e **salvo nel repository, con data e ora, prima della prima operazione**, la previsione per ogni operazione prevista: la perdita lorda allo stop e la commissione secondo la convenzione dichiarata.

## 3. Durante la prova: una posizione alla volta, 0,01 lotti, stop inserito all'apertura

| Momento | Da fotografare |
|---|---|
| **Subito prima di aprire** | Finestra del conto: saldo, equity, **margine usato** (0) e margine libero. Ora del server |
| **Subito dopo l'apertura** | Riga dell'ordine nel terminale: ticket, tipo, volume, **prezzo d'apertura**, **S/L**, prezzo attuale, **commissione** (se compare già), swap, profitto. Finestra del conto: **margine usato** e margine libero. Ora del server |
| **Se cambi lo stop** | La riga dell'ordine con il nuovo S/L e l'ora. Ogni modifica va annotata |
| **Dopo la chiusura** | La cronologia: prezzo e ora di chiusura, commissione, swap, profitto |
| **Alla fine** | L'**estratto dettagliato** della cronologia del conto (in MT4: cronologia → salva come rapporto) |

Una chiusura avvenuta non allo stop verifica la **formula al prezzo eseguito**. La perdita *realizzata allo stop* resta però non osservata.

## 4. Tolleranze che devi ancora approvare (proposta di DGS-21, confermata da DGS-22)

*u* è il più piccolo importo che il broker mostra nella valuta del conto (per esempio 0,01).

| Voce | Tolleranza proposta | Esempio con u = 0,01 |
|---|---|---|
| P&L lordo / perdita allo stop | **assoluta, 1u** | previsto 0,10, osservato 0,11: concorde (confine incluso) |
| Commissione | **esatta, 0u**, dopo l'arrotondamento documentato | previsto 0,03, osservato 0,06: discordante |
| Margine usato | **1u** sul valore diretto della posizione, **2u** se calcolato come differenza di due letture (prima e dopo) | 35,18 contro 35,20: ammesso per differenza; 35,21 no |

**Regole comuni proposte:**
- concorde se |scarto| ≤ T;
- un errore di segno, lato, valuta, volume o unità è «discordante» anche se piccolo;
- una voce senza previsione o senza osservazione confrontabile è «non osservabile».
- Se una voce obbligatoria resta non osservabile, l'esito è **«parziale»** e `riconciliato` resta **falso**.
- Una spiegazione trovata dopo aver visto l'estratto non cambia l'esito della previsione originaria.

**Testo da approvare (DGS-21):** «Per la prova D2 sulla demo FP Markets MT4 Raw approvo la tabella delle tolleranze del DGS-21, con valuta e precisione documentate prima delle operazioni, confronto per voce ed esito parziale quando manca un'osservazione obbligatoria».

**Una nota mia, che non tocca le tolleranze:** per il margine il Guardian non ha una previsione. Se approvi la tolleranza del margine, essa si applicherà a un calcolo esterno attribuito al profilo demo, non al Guardian.
