# Relazione dell'audit architetturale · AUDIT-ARCH-20261111

Autore: Claude · Data: 11/11/2026 · Base esaminata: commit `a764e61` · Vincoli rispettati: nessuna lezione, nessun materiale di Antigravity e nessuna struttura modificati; nessuna migrazione; nessuna strategia o backtest nuovi.

## 1. In sintesi
1. **Il Brain è solido nel ragionamento sul rischio e nella verifica, debole nella ricerca empirica.** Statistica operativa, rovina, Kelly e controllo dei Monte Carlo sono verificati con calcoli esatti. Dati reali, modello di esecuzione, backtest e registro delle ipotesi sono assenti.
2. **Nessuna lezione è ancora `verificata` e nessun cancello è stato superato.** Le 6 lezioni nuove sono strutturalmente complete (20/20 sezioni); nessuna fonte è letta nel testo integrale; in bibliografia l'84% delle voci è citato da memoria.
3. **L'architettura è solo didattica.** Non ha un posto per Strategy Discovery Lab, Trading Guardian, motore di rischio e dati. Propongo uno strato `laboratori/` separato dalla formazione (da approvare).
4. **Il Trading Guardian non è definito in nessun documento.** Ne propongo una funzione (protezione di capitale e processo, livelli G0 consultivo → G1 paper → G2 reale con autorizzazione), da confermare.
5. **14 incoerenze, 5 duplicazioni e 6 lacune trasversali.** Le più gravi:
   - i materiali V2 di Gemini **non sono archiviati** nel Brain;
   - l'architettura non prevede i sistemi software;
   - i dati reali sono assenti;
   - le regole FTMO non sono verificate su fonti ufficiali.
6. **Priorità per tre mesi:**
   - mese 1: consolidamento (chiusura V2, verifica delle lezioni, specifica del Guardian, rulebook con fonti, statistica);
   - mese 2: metodo di ricerca e dati (Modulo 8, registro delle ipotesi, prime serie reali, motore di rischio unico, Guardian consultivo);
   - mese 3: primo ciclo di ricerca completo, per collaudare la catena e non per cercare un edge.

## 2. Documenti dell'audit
| File | Contenuto |
|---|---|
| [`00-CHECKPOINT.md`](00-CHECKPOINT.md) | Stato delle tappe, per la ripresa |
| [`01-INVENTARIO-E-QUALITA.md`](01-INVENTARIO-E-QUALITA.md) | Che cosa c'è, qualità dei moduli, indicatori |
| [`02-INCOERENZE-E-DUPLICAZIONI.md`](02-INCOERENZE-E-DUPLICAZIONI.md) | I-01…I-14, D-01…D-05, L-01…L-06 |
| [`03-COMPETENZE-QUANT-MANCANTI.md`](03-COMPETENZE-QUANT-MANCANTI.md) | Mappa delle competenze dal discrezionale al sistematico |
| [`04-DIPENDENZE.md`](04-DIPENDENZE.md) | Grafo, percorso critico, lavori paralleli |
| [`05-ARCHITETTURA-SDL-E-GUARDIAN.md`](05-ARCHITETTURA-SDL-E-GUARDIAN.md) | Proposta per Strategy Discovery Lab e Trading Guardian |
| [`06-FONTI-E-VALIDAZIONE.md`](06-FONTI-E-VALIDAZIONE.md) | Qualità delle fonti e delle procedure |
| [`07-PRIORITA-TRE-MESI.md`](07-PRIORITA-TRE-MESI.md) | Piano a 12 settimane con cancelli e rischi |
| `strumenti/misure_brain.py`, `strumenti/misure_20261111.txt` | Misure automatiche riproducibili |

## 3. Rischi principali
| Rischio | Gravità | Proposta |
|---|---|---|
| Perdita della versione congelata V2 (non archiviata) | alta | Decidere l'archivio delle consegne |
| Discovery Lab senza contatore delle prove | alta | Registro delle ipotesi prima di qualsiasi backtest |
| Guardian costruito su regole non verificate | alta | Rulebook con fonti ufficiali e test per regola |
| Lezioni ferme `in_verifica` | media | Piano C → V per priorità d'uso |
| Due definizioni di Guardian tra Claude e Gemini | media | Specifica unica approvata |
| Dati reali inaccessibili | alta | Decisione sull'accesso |

## 4. Proposte operative immediate (non strutturali, eseguibili da Claude dopo il via libera)
1. Aggiornare registri, domande aperte e conteggi (I-02, I-03, I-06).
2. Correggere il rimando C-04 → C-06 nella contestazione, con nota di modifica.
3. Nuova versione datata della matrice delle lacune (I-04), senza sovrascrivere la precedente.
4. Bozza della specifica del Guardian G0, da sottoporre a Gemini e all'utente.

## 5. Decisioni richieste all'utente
| # | Decisione | Perché ora |
|---|---|---|
| 1 | Funzione e nome del **Trading Guardian** | Evita che Claude e Gemini costruiscano due cose diverse |
| 2 | Strato **`laboratori/`** nell'architettura | Serve un posto per i sistemi software prima di scriverli |
| 3 | **Archivio delle consegne** di Gemini | La V2 congelata oggi esiste solo sul Mac e nelle copie in chat |
| 4 | **Accesso ai dati reali** | Blocca mesi 2–3 |
| 5 | Approvazione del **piano a tre mesi** e sblocco dei cantieri sospesi | La roadmap attuale è sospesa |
| 6 | Testi del **Master Mission** e del **Protocollo comune** | Ancora provvisori (D-09) |
| 7 | Conferma di **D-08** | Pendente dal 11/11 |

## 6. Che cosa non è stato verificato in questo audit
- Le fonti della bibliografia (nessuna lettura nuova: l'audit misura lo stato, non lo migliora).
- I contenuti del v1 oltre a quanto già verificato nell'audit iniziale.
- Il rulebook e lo Studio 01 originale di Gemini (non consegnati).
- Le regole FTMO su fonti ufficiali.
