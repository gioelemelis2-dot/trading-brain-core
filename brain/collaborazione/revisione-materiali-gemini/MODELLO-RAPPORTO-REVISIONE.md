---
id: R-CLAUDE-AAAAMMGG-NN
revisore: Claude
data: AAAA-MM-GG
consegna_esaminata: "collaborazione/da-gemini/consegne/<ID>/"
commit_esaminato: "hash"
manifest_verificato: si | no | parzialmente
materiali: [G-MAT-1, G-MAT-2, ...]
ambiente: "Python x.y, sistema, dipendenze installate"
esito_complessivo: integrabile | integrabile con correzioni | non integrabile ora | non valutabile
---

# Rapporto di revisione · <titolo della consegna>

## 0. Sintesi (max 8 righe)
Che cosa è stato esaminato, che cosa regge, che cosa no, che cosa serve per decidere.

## 1. Che cosa è stato fatto
- Comandi eseguiti (con output essenziale), test lanciati, fonti lette, calcoli ripetuti.
- Che cosa **non** è stato possibile fare e perché.

## 2. Risultati confermati
| # | Materiale · file · riga/sezione | Risultato di Gemini | Come è stato confermato | Valore ricalcolato da Claude | Classe |
|---|---|---|---|---|---|

## 3. Errori individuati
| # | Dove | Errore | Prova (riproduzione minima) | Impatto sui risultati | Gravità (alta/media/bassa) |
|---|---|---|---|---|---|

## 4. Ipotesi discutibili
| # | Ipotesi | Dove compare | Perché è discutibile | Alternativa ragionevole | Effetto stimato se cambiata |
|---|---|---|---|---|---|

## 5. Dati mancanti
| # | Dato o informazione mancante | Perché serve | Chi può fornirlo | Blocca la valutazione? |
|---|---|---|---|---|

## 6. Differenze metodologiche
Confronto tra l'approccio di Gemini e quello già presente nel Brain o nel riferimento indipendente di Claude. Una differenza **non è un errore**: si descrive, si quantifica dove possibile e si indica quale scelta è più adatta a quale domanda.
| # | Aspetto | Gemini | Brain / Claude | Effetto sul risultato | Valutazione |
|---|---|---|---|---|---|

## 7. Proposte di correzione e di integrazione
| # | Proposta | Tipo (correzione / test aggiuntivo / documentazione / integrazione nel Brain) | File interessati | Chi la esegue | Priorità |
|---|---|---|---|---|---|

Ogni proposta che tocca file di Gemini è **eseguita da Gemini**; ogni proposta che tocca file canonici del Brain è eseguita da Claude **dopo** l'approvazione dell'utente se strutturale (D-07).

## 8. Checklist compilata
Copiare qui la tabella di `CHECKLIST-REVISIONE.md` con l'esito di ogni voce.

## 9. Domande per Gemini
Domande precise a cui serve una risposta prima della decisione.

## 10. Domande per l'utente
Solo le decisioni che spettano all'utente.

## 11. Limiti di questa revisione
Che cosa potrebbe essere sfuggito; quali parti non sono state esaminate.
