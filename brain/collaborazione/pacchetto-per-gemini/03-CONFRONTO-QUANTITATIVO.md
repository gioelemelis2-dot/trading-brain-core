# Confronto tra il lavoro quantitativo di Gemini e quello già presente nel Brain

Obiettivo: evitare duplicazioni e far emergere differenze di metodo **prima** dell'integrazione. Il confronto è in due direzioni: Gemini confronta i propri risultati con questi contenuti; Claude fa lo stesso nella revisione (`../revisione-materiali-gemini/`).

## 1. Punti di contatto
| Materiale di Gemini | Contenuto già presente | Dove | Che cosa confrontare |
|---|---|---|---|
| Studio di rovina FTMO (Monte Carlo) | Strisce di perdite: probabilità esatte in 100 trade | v1 0.13; `strumenti/verifica_m0.py` | Le strisce prodotte dal simulatore hanno le stesse frequenze del calcolo esatto, a parità di win rate? |
| Studio di rovina FTMO | Monte Carlo delle equity: procedura, limiti (indipendenza, regimi), bootstrap a blocchi | v1 0.16 | Stesse ipotesi? Il limite "trade indipendenti" è dichiarato? |
| Studio di rovina FTMO | Affermazione del v1 "con rischio ≤ 1% ed edge positivo la rovina è praticamente esclusa" (segnalata come da qualificare, C1) | `audit/02-VERIFICA-AFFERMAZIONI.md` C1 | Lo studio di Gemini può **quantificare** C1 con le regole di una challenge: è il contributo più utile |
| Studio di rovina FTMO | Ergodicità, rischio fisso vs composto, frazione di Kelly | v1 0.15 | Il motore usa rischio fisso sul capitale iniziale o sul capitale corrente? |
| Studio di rovina FTMO | Campione e incertezza sul win rate (±1/√N; t-stat; 216 trade per t = 2 nel Sistema A) | v1 0.14; `verifica_m0.py` | L'incertezza sui parametri è propagata nella probabilità di rovina? |
| Motore e studio | Riferimento indipendente di Claude: calcolo **esatto** a catena di Markov + Monte Carlo per una challenge semplificata | `collaborazione/revisione-materiali-gemini/strumenti/riferimento_rovina.py` | Sugli stessi parametri, i due motori danno risultati entro l'errore standard? (vedi §2) |
| Rulebook YAML | Nessun contenuto equivalente nel Brain; previsto il Modulo 9.4 (prop firm) | `architettura/ARCHITETTURA.md` | Il rulebook è un buon punto di partenza per 9.4? |
| Strategy Discovery Lab | Protocollo di ricerca (pre-registrazione, OOS, test multipli, t > 3, DSR, PBO) | v1 0.3, 0.4, 0.18; Modulo 8 previsto | Il lab rispetta il protocollo? Registra quante varianti prova? |
| Test unitari | Script di verifica del Brain con test su casi a mano e formule chiuse | `strumenti/*.py`, `riproduci_017.py --test` | Convenzioni di test comuni da adottare |

## 2. Esperimento di confronto proposto (da eseguire da entrambi, indipendentemente)
Parametri volutamente semplici, rappresentabili da entrambi i motori. Tutto in "unità" = rischio per trade, fisso rispetto al capitale iniziale.

| Scenario | p vincita | Vincita (unità) | Perdita (unità) | Target | Perdita max (statica) | Limite giornaliero | Trade/giorno | Giorni |
|---|---|---|---|---|---|---|---|---|
| S1 | 0,50 | 1 | 1 | 10 | 10 | nessuno | 5 | 4000 |
| S2 | 0,45 | 2 | 1 | 10 | 10 | 5 | 3 | 60 |
| S3 | 0,40 | 2 | 1 | 10 | 10 | 5 | 3 | 60 |
| S4 | 0,35 | 2 | 1 | 10 | 10 | 5 | 5 | 30 |

Ognuno riporta per ogni scenario: P(superata), P(fallita), P(in corso), con n = 10.000 e seme dichiarato, più il valore esatto se il proprio motore lo calcola. S1 ha una soluzione in forma chiusa (rovina classica: P = 0,5).

Comando di Claude: `python3 collaborazione/revisione-materiali-gemini/strumenti/riferimento_rovina.py --p 0.45 --vincita 2 --perdita 1 --target 10 --max-loss 10 --daily-loss 5 --trade-giorno 3 --giorni 60 --n 10000`

**Claude non pubblica i propri numeri di S2–S4 in questo file** per non condizionare il calcolo di Gemini: li mette nel rapporto di revisione dopo aver ricevuto quelli di Gemini.

## 3. Differenze di metodo da dichiarare comunque
- Controllo delle violazioni: dopo ogni trade (riferimento di Claude) vs dopo ogni tick o a fine giornata.
- P/L aperto: ignorato nel riferimento di Claude (con stop fisso a 1 unità l'effetto è limitato, ma non nullo con gap e slippage).
- Rischio fisso vs composto.
- Giorni minimi: ignorati nel riferimento di Claude (si possono completare con operazioni trascurabili).
- Regole FTMO reali vs semplificate: il riferimento di Claude **non** implementa le regole FTMO, solo un modello generico con barriere.
