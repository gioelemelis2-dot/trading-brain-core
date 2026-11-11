# Revisione dei materiali di Gemini (da parte di Claude)

Stato: **PROVVISORIO** (struttura di lavoro della prima fase di collaborazione, non definitiva — decisione D-10).
Aggiornato: 11/11/2026.

## A che cosa serve
Documentare una revisione **indipendente** dei materiali prodotti da Gemini Antigravity, senza dare per scontata la correttezza dei risultati, prima di qualsiasi integrazione nel Brain.

## Materiali attesi (annunciati dall'utente, non ancora ricevuti)
| Codice | Materiale | Stato |
|---|---|---|
| G-MAT-1 | Studio sulla rovina operativa FTMO con 10.000 simulazioni Monte Carlo | atteso |
| G-MAT-2 | Motore quantitativo Python | atteso |
| G-MAT-3 | Test unitari | atteso |
| G-MAT-4 | Rulebook YAML | atteso |
| G-MAT-5 | Primo Strategy Discovery Lab | atteso |

## Flusso
```
Gemini deposita i materiali in  collaborazione/da-gemini/consegne/<ID>/  con MANIFEST (vedi lì il README)
            │   (Claude non modifica nulla in quella cartella)
            ▼
Claude: ricezione e integrità (hash)  →  checklist  →  rapporto di revisione in questa cartella
            ▼
Esiti in collaborazione/da-claude/ESITI.md  ·  disaccordi in DISACCORDI.md  ·  decide l'utente
            ▼
Integrazione nel Brain SOLO dopo il controllo e con proposta documentata
```

## Contenuto
| File | Uso |
|---|---|
| [`CHECKLIST-REVISIONE.md`](CHECKLIST-REVISIONE.md) | Controlli da eseguire, con codice, metodo di verifica ed esito |
| [`MODELLO-RAPPORTO-REVISIONE.md`](MODELLO-RAPPORTO-REVISIONE.md) | Struttura del rapporto: confermati · errori · ipotesi discutibili · dati mancanti · differenze metodologiche · proposte |
| [`strumenti/riferimento_rovina.py`](strumenti/riferimento_rovina.py) | Calcolo **esatto** (catena di Markov) e Monte Carlo indipendente per un modello semplificato di challenge; scritto prima di vedere il codice di Gemini. Test: coincide con la formula chiusa della rovina classica |
| `R-CLAUDE-AAAAMMGG-NN-*.md` | I rapporti di revisione (uno per consegna) |

## Regole
- **Non si modifica nessun file di Gemini.** Le correzioni si propongono nel rapporto; eventuali versioni corrette sono nuovi file con nome diverso, nella cartella di revisione.
- I risultati di Gemini restano attribuiti a Gemini; i risultati del ricalcolo di Claude sono etichettati come tali.
- Ogni numero porta la sua classe: `[REALE]`, `[SIMULATO]`, `[ESEMPIO]`, `[IPOTESI]`.
- Un risultato non riprodotto non è necessariamente sbagliato: si scrive "non riprodotto" con il motivo.
