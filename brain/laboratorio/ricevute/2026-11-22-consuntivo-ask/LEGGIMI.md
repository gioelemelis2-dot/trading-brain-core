# Consuntivo dell'ASK (fine scaricamento) · 22/11/2026

- **Prodotto sul Mac del titolare** il 22/11/2026 tra le 05:48 e le 05:53. Comandi:
  - `controlla_cache` su BID e ASK, con il confronto fra i due;
  - `intersezione_bid_ask` dal 01/01/2005 all'11/11/2023.
- **Codice:** quello della punta di `feat/esecutore-h002` dopo il `git pull` di quella sera.
- **Contenuto:** solo conteggi e date, **nessun prezzo** (DA-26). File copiati com'erano, con le impronte in `SHA256SUMS`.

## In sintesi
- **Cache BID e ASK pulite:** 6.889 giorni di calendario, ogni giorno ha il file su entrambi i lati (`ALLINEATI`).
  - nessun file mancante, nessun feriale vuoto, nessun file illeggibile, nessun file temporaneo;
  - 30 giorni «corti» per lato, quasi tutti festività e vigilie (1/1, Venerdì Santo, 25/12, 26/12).
- **Sedute di Londra nel periodo:** 4.823 (4.803 sedute più 20 vigilie). In ogni seduta ci sono entrambi i file.
- **Qualità al minuto, cioè la quota di minuti comuni validi della sessione, al 1° percentile:**
  - più bassa nei primi anni: 2005 0,44 (buco massimo 158 minuti); 2006 0,74; 2007 0,89; 2008 0,97;
  - dal 2009 in poi ≥ 0,97, quasi sempre 1,00;
  - buchi isolati più lunghi: 106 minuti nel 2012, 63 nel 2015.
- **Nessun minuto con quotazioni incrociate** (ASK sotto BID agli estremi): il rilievo #108 sui dati veri è nullo.
- **Griglia diagnostica** (le soglie non sono decise qui):

| quota seduta | quota per terzo | buco massimo | sedute ammissibili |
|---|---|---|---|
| 0,98 | 0,95 | 5 | 4.423 su 4.823 |
| 0,95 | 0,90 | 15 | 4.578 su 4.823 |
| 0,90 | 0,80 | 30 | 4.683 su 4.823 |
| 0,50 | 0,25 | 525 | 4.819 su 4.823 |

## Che cosa ne segue (da decidere dal titolare, D-38)
- Con 1.000 sedute per verifica (D-37) e circa 4.400–4.800 sedute ammissibili, le finestre disgiunte sono **al massimo 4**, prima dell'embargo e delle date accessorie.
- La quarantena proposta (oltre il 5% dei minuti mancanti nella fascia operativa) toglierebbe soprattutto giorni del 2005–2007.
- La proposta delle date esatte arriverà come documento a parte, con una riga per finestra candidata (DGS-14 Q4).
