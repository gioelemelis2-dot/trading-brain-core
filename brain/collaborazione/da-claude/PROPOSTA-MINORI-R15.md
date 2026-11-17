# Proposta per i minori di R15 nel codice sigillato (#107, #109, #110, #111) e per #108

**Stato: PROPOSTA, NON APPLICATA** (17/11/2026). Toccano il perimetro del candidato `8e51ce9`: se si applicano, il candidato cambia, e per il parere P6 del DGS il prossimo giro (R16) deve rifare sul candidato nuovo le prove toccate.

| Difetto | Correzione proposta | Effetto sui risultati | Costo |
|---|---|---|---|
| #107 copertura 1,0 con confronto casuale vuoto | valore predefinito 0,0, come per il benchmark | nessuno (il criterio fallisce già): cambia solo il valore registrato | minimo |
| #110 `verifica` con `anni` vuoto o `sharpe_prove` con None; `percentile` con q fuori da (0, 1] | `ValueError` con un messaggio chiaro | nessuno sui chiamanti attuali | minimo |
| #111 record in ordine non crescente | `decodifica` li rifiuta come errore di dati (come per #89) | nessuno sui dati di Dukascopy, che sono in ordine; sui file anomali un errore invece di un'accettazione | minimo |
| #109 giorni senza minuti nel range d'apertura accettati come completi | **da decidere con le soglie definitive**: oggi `orb_londra` li scarta comunque | dipende dalle soglie | — |
| #108 ASK ≥ BID solo su apertura e chiusura | **scelta di metodo:** decidere dopo aver visto, con il rendiconto dell'intersezione, quanti minuti dei dati veri hanno estremi incrociati | cambia quali minuti sono eseguibili | — |

**Raccomandazione di Claude:**
- **#107, #110, #111** in un solo commit con i test prima, prima di R16, così R16 lavora sul candidato definitivo.
- **#108 e #109** dopo il consuntivo dello storico, insieme alle soglie.

Decide il titolare.
