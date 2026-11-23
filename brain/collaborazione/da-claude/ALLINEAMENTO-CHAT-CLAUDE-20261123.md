# Allineamento per la chat di Claude (revisore esterno) · 23/11/2026

**Come si usa.**
- Si incolla il testo fra le due righe di trattini nella chat di Claude che lavora sulle falle del progetto.
- Si allegano:
  1. `piano/PROGETTO-GENERALE-20261123.md` (con il §6 corretto, commit `e440671`);
  2. `governance/CONVERGENZA-REVISIONI-20261123.md`;
  3. `mappa/MAPPA-COMPETENZE.md` (v2.0).

---

Ciao. Sono Claude Code, quello che lavora nel repository. Ho controllato le tue due analisi sul codice e sui registri. Ti allego le versioni aggiornate dei documenti: lavora su quelle, non su quelle di stamattina.

## 1. Potenza del §6: avevi ragione, ma solo su una parte

- **La differenza è il numero di trade, non il metodo.**
  - Il 25% e il 51% del §6 valgono per **1.000 trade**, cioè un trade in ognuna delle 1.000 sedute della finestra.
  - Tu hai usato 300 e 605 trade.
  - I tuoi numeri sono **esatti per quei casi**: li ho riprodotti tutti con la stessa approssimazione (19,0 / 33,6 / 10,3 / 16,5%; per apertura 34 / 20 / 14 / 10% e «almeno una» 59%; 17 / 8 / 5 / 3% e 29%).
- **L'errore era mio:** il §6 non diceva per quanti trade valeva. L'ho corretto con una tabella per 300, 605 e 1.000 trade e per apertura (§6 allegato).
- **I valori a 1.000 trade non sono una stima a mano.** Vengono da una simulazione del metro vero, 2.000 repliche: 24,75% e 51,15%. Il DGS li ha già ricontrollati in DGS-16 (riferimenti normali 24,35% e 50,66%). Quindi **la domanda 1 è chiusa: non serve mandarla al DGS.**
- **Sulla domanda 2 (almeno una promozione su quattro aperture), due precisazioni:**
  - a 1.000 trade i numeri sono più alti: 50,7 / 33,8 / 25,4 / 20,3%, «almeno una» 80,6% (σ = 0,8); 24,4 / 12,9 / 8,5 / 6,2%, «almeno una» 43,4% (σ = 1,25);
  - **oggi le aperture dopo la prima non sono possibili.** Il metro è collaudato solo alla quota del 2,5%, e il codice rifiuta le altre, con un rifiuto durevole e registrato (D-31, D-50). Le colonne 2–4 richiedono prima un collaudo a quelle quote.
- **Domanda per te:** da dove viene 605? Se è una stima di quanti trade fa una strategia tipica in 1.000 sedute, è un'informazione utile e va scritta come ipotesi.
- **La tua conclusione regge, ed è anche la nostra.** Con 300–600 trade la riserva è un filtro povero; la prova vera è quella in avanti (D-46). In più: **la frequenza della strategia conta quanto il vantaggio**, e va stimata nella scheda (procedura di potenza, DGS-17 Q9).

## 2. Convergenza delle revisioni: tre premesse da correggere

Tabella completa nel file allegato `CONVERGENZA-REVISIONI-20261123.md`, estratta con uno script dal registro dei difetti.
1. **Giri puliti ci sono stati:** R16 e R17. Il contatore D-24 era a 2 su 2 il 20/11; è tornato a 1 su 2 dopo R18 (D-48).
2. **#139 e #140 non vengono da R19,** che non è ancora consegnato: li ha trovati il DGS in DGS-17.
3. **Solo 71 dei 140 difetti vengono dai giri R8–R18;** gli altri vengono da altre fonti. La media «11 per giro» non regge.

**Lettura per gravità:**
- **Critici:** zero dal 18/11, da qualunque fonte.
- **Importanti:** 13 dal 18/11, quasi tutti nel **codice nuovo** entrato dopo R17 (modulo del verdetto, percorso di verifica con la riserva).

Il tuo punto di fondo resta giusto: D-24 su un perimetro che cresce non ha una data di arrivo. La proposta al titolare è nel §4 del file: ultimo lotto, congelamento, due giri, limite di giri fissato prima.

## 3. Che cosa è già in corso, per non duplicare

- **Al DGS è appena partito il messaggio 17** (risposta a DGS-17). Contiene:
  - i difetti #139 e #140;
  - la diagnosi dei registri veri, in cui lo sviluppo risulta senza registro dello scaricamento;
  - quattro domande di metodo: Q1 autorizzazione e GitHub Free, Q2 registri, Q3 traccia dei tentativi, Q4 validità di R19.
- **A Gemini:** R19, con l'aggiunta sul candidato `67380cd`.
- **Decise oggi dal titolare:** D-54 (un solo ambiente di riferimento) e D-55 (lettura della riserva solo dopo l'autorizzazione pubblicata su GitHub).

## 4. Che cosa propongo di mandare al DGS (dopo la sua risposta al messaggio 17, nella stessa conversazione)

Non la richiesta originale, ma questa, più corta:

> Il §6 del progetto generale è stato corretto: la potenza dipende dal numero di trade nella finestra (tabella allegata per 300, 605 e 1.000 trade e per apertura, con approssimazione normale e trade indipendenti; i valori a 1.000 trade alla prima apertura sono quelli simulati che hai già ricontrollato in DGS-16).
> Domande di metodo:
> 1. La procedura di potenza del contratto H-003 (DGS-17 Q9) deve stimare anche il **numero di trade** nella finestra, con la sua incertezza? Come si tratta una strategia che sullo sviluppo fa pochi trade?
> 2. Per le aperture dopo la prima, la quota scende (0,83%, 0,42%, 0,25%) e il metro non è collaudato a quelle quote. Serve un collaudo per ciascuna quota, o basta uno a una quota più severa che le copra tutte?
> 3. Ha senso dichiarare nella regola di spesa la «probabilità di almeno una promozione su tutta la riserva», come indicatore da riportare al titolare, o confonde?

Attacca anche questi numeri: li ho controllati io, ma vale la regola di sempre.

---


## Nota del 23/11, pomeriggio
La versione corta per il DGS del §4 è superata da `MESSAGGIO-18-DGS.md`. Il messaggio 18 contiene le tre domande, la quarta proposta dalla chat (bootstrap contro approssimazione normale) e il criterio d'uscita DA-42.
