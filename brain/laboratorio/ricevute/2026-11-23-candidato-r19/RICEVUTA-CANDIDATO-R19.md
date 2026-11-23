# Candidato proposto per R19 · `1431190` · 23/11/2026

Tutte le corse sono state fatte in un worktree **bloccato sul commit `1431190`**, su Python 3.13.18 e 3.9.25, con la rete bloccata. Log in `log/`.

| Corsa | 3.13.18 | 3.9.25 | Vivi |
|---|---|---|---|
| Suite complete (`esegui_test.py`) | TUTTO VERDE | TUTTO VERDE | — |
| Mutanti del perimetro (`mutazioni_esecuzione.py`, 299, in 4 gruppi per prefisso: N+K 96, V+E+S+TA+MG+MR 71, C+IX+R+Q 62, P 70) | **299/299** | **299/299** | nessuno |
| Mutanti del verdetto (`mutazioni_verdetto.py`, 132) | 131/132 | 131/132 | VD13, equivalente dichiarato: l'assegnazione `s, k = c` solleva comunque `ValueError` |
| Mutanti del percorso ordinario (`mutazioni_percorso.py`, 58) | 57/58 | 57/58 | MF09, equivalente dichiarato: l'insieme atteso è già generato in ordine |

**Che cosa contiene il candidato rispetto a R18**
- Correzioni di R18: #125, #126, #128, #131–#135. Poi #136, #137, #138 e #124 (in due parti, con decisioni in frazioni esatte).
- Percorso ordinario di verifica `esegui_verifica.py`, con lo schema `riserva/2` (D-50), il manifesto dei dati e i byte verificati. Le protezioni di PIANO-D51 §3:
  - registri canonici e ancorati, storia completa, prenotazione consumata altrove rifiutata, j e N che non scendono;
  - dati di sviluppo legati al registro dello scaricamento;
  - lanciatore `avvio.py verifica` e ambiente ricontrollato;
  - una sola verifica per ipotesi e variante.
- D-51: la verifica di `esegui_h002` è disattivata, con rifiuto immediato. Le protezioni comuni sono provate sullo sviluppo e sul percorso nuovo.
- `test_mutanti_applicabili` nella suite.

**Durante la corsa del candidato sono emersi mutanti vivi, tutti corretti con test nuovi prima di questa corsa definitiva:**
- EV26: test troppo generico;
- N38, N41, N65: i loro test passavano dalla verifica disattivata;
- R05: stesso motivo.

È la perdita di protezioni da cui il DGS aveva messo in guardia in DGS-16 Q7: la corsa completa dei mutanti l'ha trovata.

**A chi spettano le decisioni:**
- che questo sia il candidato di R19 e l'avvio del giro di Gemini (D-48: R19 è un giro ordinario completo più le manomissioni): **al titolare**;
- la chiusura del punto 5 di D-34: **al titolare**.
