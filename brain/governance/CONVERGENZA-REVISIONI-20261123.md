# Convergenza dei giri di revisione · estratto del registro dei difetti (23/11/2026)

**Richiesta del titolare**, a partire da una domanda della chat di Claude sul Gate 2½: «state convergendo?».
**Fonte:** `laboratorio/REGISTRO-DIFETTI.md` (#1…#140), colonne «Gravità» e «Trovato da», estratte con uno script, non a mano.
**Limiti:**
- la riga #124 ha la colonna «Trovato da» rovinata («S») e non è attribuibile;
- R7 e R9 non hanno righe proprie nel registro: i loro rilievi sono in `ipotesi/H-002-REVISIONI.md`.

## 1. Giri di Gemini

| Giro | Data | Difetti | Critici | Importanti | Minori | Limiti | Che cosa rivedeva |
|---|---|---|---|---|---|---|---|
| R7 | 15/11 | — | — | — | — | — | (nessuna riga propria) |
| R8 | 15/11 | 2 | 0 | 1 | 1 | 0 | replica indipendente del simulatore |
| R9 | 15/11 | — | — | — | — | — | (nessuna riga propria) |
| R10 | 15/11 | 9 | **5** | 4 | 0 | 0 | esecutore di H-002 |
| R11 | 15/11 | 8 | **3** | 4 | 1 | 0 | criteri, caricatore, esecutore |
| R12-bis | 16/11 | 11 | 0 | 8 | 3 | 0 | perimetro e scaricatore |
| R13 | 16/11 | 9 | 0 | 6 | 3 | 0 | ambiente, ancora, riserva |
| R14 | 17/11 | 9 | **1** | 4 | 4 | 0 | lanciatore e correzioni del 17/11 |
| R15 | 17/11 | 6 | 0 | 1 | 5 | 0 | candidato `8e51ce9` |
| R16 | 18/11 | 3 | 0 | 0 | 3 | 0 | candidato `303890b` → **pulito** (D-26) |
| R17 | 18–20/11 | 3 | 0 | 0 | 3 | 0 | candidato `e476a9a` → **pulito**, contatore 2 su 2 (20/11) |
| R18 | 21/11 | 11 | 0 | 7 | 3 | 1 | **giro su tutte le manomissioni** più il modulo nuovo del verdetto → contatore 1 su 2 (D-48) |
| R19 | in corso | — | — | — | — | — | candidato `1431190`, poi `67380cd` |

Gli importanti di R18 sono di due gruppi:
- **3 nel perimetro già rivisto:** #125 (copia parziale del repository), #126 (BID e ASK nella stessa cartella), #127 (collegamento fra esecutore e riserva);
- **4 nel codice nuovo:** #131–#133 nel modulo del verdetto D-31, #135 nella CI.

## 2. Difetti trovati fuori dai giri di Gemini

| Fonte | Difetti | Critici | Importanti | Minori |
|---|---|---|---|---|
| Audit di Gemini del 13/11 (prima dei giri numerati) | 6 | 3 | 2 | 1 |
| Giri R2–R3 di Gemini (14/11) | 4 | 1 | 3 | 0 |
| Claude (corse di mutanti, riletture, revisioni proprie) | circa 20 | 4 | circa 9 | circa 7 |
| Revisori separati avviati da Claude (17/11) | 23 | 5 | 12 | 6 |
| DGS (ChatGPT) | 10 | 1 | 7 | 2 |
| DeepSeek | 4 | 0 | 2 | 2 |
| Titolare | 1 | 0 | 1 | 0 |

Totale 140: 71 dai giri numerati R8–R18 (75 con R2 e R3), 68 da altre fonti, #124 non attribuibile.

## 3. Lettura

- **Critici: convergenza netta.** L'ultimo critico, da qualunque fonte, è del **17/11** (#96 in R14; #86–#88 e #95 nello stesso giorno). Dal 18/11 a oggi: **zero critici**, in tutti i giri e da tutte le fonti.
- **Importanti: non convergono, e il motivo si vede.** Dal 18/11 sono 13 (#122–#127, #131–#133, #135, #138–#140). Quasi tutti stanno nel **codice nuovo** entrato dopo R17:
  - il modulo del verdetto (D-34);
  - il percorso ordinario `esegui_verifica` e la riserva/2 (#127, D-50, D-51).

  Sul perimetro già rivisto due volte ne restano 3, tutti trovati da R18, che era un giro di tipo diverso: tutte le manomissioni.
- **Il contatore non è mai stato «impossibile».** R16 e R17 sono stati puliti e il contatore è arrivato a 2 su 2 il 20/11. È tornato a 1 su 2 perché il perimetro è **cresciuto** (D-34, D-51) e perché il giro su tutte le manomissioni ha trovato 3 importanti.
- **#139 e #140 non vengono da R19,** che non è ancora consegnato: li ha trovati il DGS (DGS-17). Se facciano ripartire il contatore è una decisione del titolare; è la domanda Q4 del messaggio 17.

## 4. Il problema vero e un'uscita possibile (proposta, non decisione)

D-24 chiede due giri puliti di fila **su un perimetro che continua a crescere**. Prima del primo accesso reale entrano altre modifiche:
- D-55, la lettura dopo la pubblicazione;
- la procedura di potenza;
- A1, i doppioni identici;
- D-54, l'ambiente di riferimento.

Ognuna, fatta da sola, riaprirebbe il contatore.

**Proposta di Claude:**
1. Un **ultimo lotto** con tutte le modifiche richieste prima del primo accesso reale.
2. Poi il **congelamento del perimetro**: nel candidato entrano solo correzioni di difetti.
3. Poi i due giri.
4. **Limite dichiarato prima:** se dopo N giri (per esempio 4) restano importanti, il titolare decide se dichiararli limiti o se riscrivere D-24. Così il gate ha una fine anche nel caso peggiore.


## Aggiornamento del 23/11, pomeriggio

- **#141 (minore)** e **#142 (importante)**, entrambi nel codice nuovo del percorso ordinario. #142 l'ha trovato Claude con la prova positiva completa dal lanciatore chiesta dal DGS: il percorso non poteva arrivare in fondo.
- Conferma la lettura del §3: **zero critici**; gli importanti nascono dove il codice è nuovo o non è mai stato esercitato davvero.
- Fa capire anche che cosa mancava: **una prova d'insieme del percorso vero**, non solo dei pezzi. Ora è nella suite.
