# Protocollo · Analizzare un movimento di mercato senza raccontarsi storie

Versione 0.1 · 11/11/2026 · Strumento trasversale (Aree S, T, A, C). Usato da L2.3 e da tutti i moduli successivi.

Risponde alla domanda "**Perché questo mercato si sta muovendo?**" costruendo un quadro **prima** di qualsiasi previsione. Si compila per iscritto. Le sezioni marcate ✱ sono obbligatorie.

## 0 · Regole
- Non partire dalla direzione futura. La previsione, se c'è, viene per ultima e con una probabilità.
- Distingui sempre: **osservato** (dato) · **inferito** (deduzione dal dato) · **ipotizzato** (da verificare).
- Se non sai, scrivi "non lo so" e quale dato servirebbe.

## 1 · Descrizione ✱
| Campo | Risposta |
|---|---|
| Mercato e strumento | |
| Finestra (da–a, fuso orario) | |
| Ampiezza del movimento in % e in multipli di volatilità (ATR o σ giornaliera) | |
| È statisticamente anomalo? (z-score rispetto alla distribuzione recente; ricorda le code grasse, Modulo 0.17) | |
| Base rate: quante volte negli ultimi N anni si è visto un movimento simile, e cosa è seguito? (solo descrittivo) | |

## 2 · Eventi nella finestra ✱
| Ora | Evento (dato macro, banca centrale, utili, geopolitica, flusso noto) | Attesa (consensus / futures) | Esito | Sorpresa |
|---|---|---|---|---|

## 3 · Contesto macro e tassi
- Cosa hanno fatto 2 anni, 10 anni, inflazione attesa (breakeven), dollaro, spread di credito nella stessa finestra?
- Coerenza: il movimento va nella direzione che la catena (L2.3) suggerirebbe? Quale anello è attivato?
- Segno del co-movimento tassi–azioni (shock di policy o informativo? L2.2).

## 4 · Volatilità e liquidità
- Volatilità implicita (es. VIX, MOVE, vol FX) e struttura a termine: contango o backwardation?
- Spread, profondità, gap: la liquidità era normale?

## 5 · Partecipanti e flussi (con livello di evidenza)
- Chi potrebbe essere coinvolto (fondi sistematici, opzioni/coperture, ribilanciamenti di fine mese, buyback, retail, liquidazioni)?
- Quale dato osservabile lo confermerebbe (volumi, open interest, flussi ETF, funding rate, dati COT)? Se nessun dato è disponibile: **E5/E6, ipotesi**.

## 6 · Microstruttura (se intraday)
- Il movimento è avvenuto con volume alto o basso? In apertura, chiusura, durante un dato?
- Osservabile vs interpretato: separa cosa dice il book/tape da cosa *si pensa* che significhi (Modulo 4).

## 7 · Spiegazioni concorrenti ✱
| # | Spiegazione | Dato che la conferma | Dato che la smentisce | Esito della verifica |
|---|---|---|---|---|
| H1 | | | | |
| H2 | | | | |
| H0 | Rumore / nessuna causa specifica | Movimento entro ±2σ, nessun evento | Evento con sorpresa grande nella finestra | |

Almeno **due** ipotesi più H0. Si cerca attivamente il dato che smentisce la preferita.

## 8 · Ipotesi testabile (facoltativa, livello L5)
"Se H1 è vera, allora in eventi simili (definiti così: …) mi aspetto … misurato da … su un campione di … eventi, con criterio di successo …." → va in `glossario/DOMANDE-APERTE.md` o diventa un progetto del Modulo 8.

## 9 · Rischi di interpretazione ✱
- Hindsight / narrativa a posteriori · Confirmation bias · Campione piccolo · Eventi multipli nella stessa finestra · Dati rivisti · Correlazione scambiata per causa.

## 10 · Conseguenze per il rischio (non per la direzione) ✱
- Volatilità attesa → effetti su stop e size (L2.3, esempio 4).
- Correlazioni tra posizioni aperte: sono aumentate?
- Eventi programmati imminenti.

## 11 · Sintesi in tre righe ✱
1. Cosa è successo (osservato).
2. La spiegazione più supportata, con livello di confidenza (es. "probabile, 60%") e le alternative ancora aperte.
3. Cosa cambia per il rischio.

---
*Esempio compilato*: da produrre nel lab S3 su un evento reale con dati scaricati e allegati (non inventati).
