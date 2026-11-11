# Richiesta dati · riproduzione della lezione 0.17 (statistica descrittiva e base rate)

Versione 1.0 · 11/11/2026 · Stato: **in attesa dei dati dell'utente**
Script pronto: [`strumenti/riproduci_017.py`](../strumenti/riproduci_017.py) (testato solo su dati **simulati**, vedi §6).

## 1. Che cosa va riprodotto (testo integrale del v1)

| # | Statistica | S&P 500 | Nasdaq 100 | Bitcoin |
|---|---|---|---|---|
| S1 | Rendimento giornaliero medio / dev. std | +0,06% / 1,14% | +0,08% / 1,44% | +0,20% / 3,49% |
| S2 | Curtosi in eccesso | +15,8 | +7,6 | +8,1 |
| S3 | Giorni oltre ±3σ rispetto alla normale | 5,2× | 4,6× | 6,2× |
| S4 | Range giornaliero mediano | 0,88% | 1,21% | 3,49% |
| S5 | P(giorno positivo) | 54,7% | 56,4% | 52,3% |
| S6 | P(positivo \| 3 giorni positivi) | 51,3% | 57,4% | 51,2% |
| S7 | P(positivo \| 3 giorni negativi) | 58,4% | 64,4% | 58,3% |
| S8 | Gap di apertura, in multipli del range mediano: chiusi in giornata se < 0,25× | 72% | — | — |
| S9 | Gap > 1× chiusi in giornata | 23% | — | — |
| S10 | P(su \| 3 giù) con prezzo sotto la media a 200 giorni: "da circa 65% a circa 47%" | **strumento non specificato** | | |

Periodo dichiarato: "settembre 2016 – settembre 2026", 10 anni di dati giornalieri.

## 2. Dati indispensabili

Senza questi la tabella **non** è riproducibile:

| # | Dato | Perché è indispensabile |
|---|---|---|
| D1 | **Serie OHLC giornaliere** (apertura, massimo, minimo, chiusura) per i tre strumenti | S1–S3, S5–S7 usano la chiusura; S4 usa massimo e minimo; S8–S9 usano l'apertura e il massimo/minimo della giornata |
| D2 | **Identità esatta di ogni strumento** (es. indice cash `^GSPC`/`SPX`, ETF `SPY`, future `ES` continuo; `NDX`/`QQQ`/`NQ`; per Bitcoin: exchange o indice e coppia, es. BTC/USD) | Indice, ETF e future hanno aperture, orari e gap diversi: i risultati cambiano |
| D3 | **Fonte e data di download** (provider, eventuale export da piattaforma) | Provider diversi hanno errori diversi (vedi §4) |
| D4 | **Data di inizio e di fine esatte** | "settembre 2016 – settembre 2026" lascia fino a ~40 giorni di ambiguità per serie |
| D5 | **Per Bitcoin: orario di chiusura della "giornata"** (es. 00:00 UTC) e se sono inclusi i fine settimana | Cambia numero di giorni, sequenze di 3 giorni e range |

## 3. Informazioni indispensabili sui calcoli (dal vault: note, formule, script o fogli)

Il testo del v1 lascia aperte queste scelte. Ognuna può spostare i numeri. Lo script le rende **parametri espliciti**; servono quelle usate nel vault.

| # | Scelta | Opzioni plausibili | Default dello script (provvisorio) |
|---|---|---|---|
| C1 | Tipo di rendimento | semplice (C/C₋₁ − 1) o logaritmico | semplice |
| C2 | Curtosi | in eccesso con o senza correzione per il campione | in eccesso, stimatore campionario corretto (come pandas `kurt`) |
| C3 | ±3σ | σ dell'intero campione o mobile; soglia "rispetto alla normale" = frequenza osservata / 0,27% | σ dell'intero campione; normale bilaterale 0,2700% |
| C4 | Range giornaliero | (H − L)/C₋₁, (H − L)/O oppure (H − L)/C | (H − L)/C₋₁ |
| C5 | Giorno positivo | C > C₋₁ (strettamente) o ≥ | strettamente maggiore |
| C6 | "3 giorni positivi" | sequenze **sovrapposte** (ogni giorno dopo 3 rialzi conta) o **non sovrapposte**; esattamente 3 o almeno 3 | sovrapposte, almeno gli ultimi 3 |
| C7 | Gap | (O − C₋₁)/C₋₁, diviso per il range mediano (in %) | come indicato |
| C8 | Gap "chiuso in giornata" | gap su: L ≤ C₋₁; gap giù: H ≥ C₋₁ | come indicato |
| C9 | Classi di gap | < 0,25× e > 1× del range mediano; gap nulli esclusi? | esclusi i gap esattamente nulli |
| C10 | Media a 200 giorni | semplice sulle chiusure, inclusa o esclusa la chiusura del giorno; "sotto" valutato al giorno del segnale | semplice, inclusa la chiusura del giorno del segnale |
| C11 | Strumento di S10 | 65% è vicino a 64,4% (Nasdaq 100), non a 58,4% (S&P 500) | da chiarire |

## 4. Problemi noti da verificare quando arrivano i dati

1. **Apertura dell'indice cash.** Per alcuni provider e periodi, l'"open" dell'S&P 500 cash coincide con la chiusura precedente o è calcolata su prezzi non ancora aggiornati: i gap risulterebbero falsati. *Ipotesi da verificare sui dati*, non un fatto accertato per la serie del vault.
2. **Bitcoin: range mediano (3,49%) identico alla deviazione standard (3,49%).** Può essere una coincidenza o un errore di trascrizione. Solo i dati originali possono dirlo.
3. **Festività e mezze giornate** (es. venerdì dopo il Ringraziamento negli USA): influiscono su range e gap.
4. **Cambi di composizione dell'indice** non toccano il livello dell'indice, ma se si usano ETF o future servono rettifiche (dividendi, roll del future continuo).

## 5. Formato richiesto

Un file CSV per strumento, UTF-8, separatore virgola, punto decimale, una riga per giorno, in ordine cronologico.

```csv
date,open,high,low,close
2016-09-01,2173.15,2173.56,2156.08,2170.86
```
*(La riga d'esempio mostra solo il formato: i valori non sono dati verificati.)*

| Colonna | Obbligatoria | Formato |
|---|---|---|
| `date` | sì | ISO `AAAA-MM-GG` (per Bitcoin, data UTC della chiusura) |
| `open`, `high`, `low`, `close` | sì | numero decimale, prezzo non rettificato per gli indici |
| `volume` | no | numero |
| `adj_close` | no (solo per ETF/azioni) | numero |

Più un file di metadati per serie, `NOME.meta.yaml`:

```yaml
strumento: "S&P 500 indice cash"
ticker_fonte: "^GSPC"
fonte: "nome del provider o della piattaforma"
scaricato_il: "AAAA-MM-GG"
fuso_orario_chiusura: "America/New_York 16:00"
rettifiche: "nessuna"
note: ""
```

Se nel vault ci sono note con le formule o fogli di calcolo, sono utili quanto i dati: anche come screenshot o testo copiato.

## 6. Che cosa è già pronto e che cosa NON è stato fatto

- `strumenti/riproduci_017.py` calcola S1–S10 da CSV nel formato sopra, con tutte le scelte C1–C10 esplicite.
- È stato verificato **solo** su:
  - un caso costruito a mano, con risultati calcolabili a mente (test unitari);
  - una serie **SIMULATA** (moto geometrico browniano, seme fisso 17), generata dalla funzione `serie_simulata()` dello script e descritta in `dati/simulati/README.md`, marcata come tale, usata solo per controllare che il codice funzioni. **Non è una stima dei mercati reali e non sostituisce i dati del vault.**
- Non sono stati scaricati dati di mercato reali: i siti dei provider (FRED, Yahoo, Stooq) sono bloccati dalla rete di questo ambiente.

## 7. Dove vanno i dati

- `dati/reali/` solo se la licenza del provider consente di conservarli in un repository; altrimenti restano in locale e nel repository si registrano metadati e **hash SHA-256** del file, così che il risultato resti verificabile.
- Il risultato della riproduzione verrà registrato in `audit/02-VERIFICA-AFFERMAZIONI.md` (voce C5) con esito per ciascuna statistica: riprodotta / scostamento spiegato / non riprodotta.
