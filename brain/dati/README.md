# Dati del Brain

Regola: **un dato reale e un dato simulato non stanno mai nello stesso file, nella stessa cartella o nella stessa tabella senza etichetta.**

| Cartella | Contenuto | Etichetta obbligatoria nei testi |
|---|---|---|
| `reali/` | Dati di mercato o economici reali, con file `.meta.yaml` (fonte, data di download, strumento, fuso, rettifiche) e hash SHA-256. Se la licenza non permette di conservarli qui: solo metadati + hash | `[REALE]` |
| `simulati/` | Descrizione dei generatori (seme, modello, parametri). Le serie si rigenerano dagli script, non si conservano | `[SIMULATO]` |
| `derivati/` (quando servirà) | Risultati calcolati da dati reali, con riferimento a script, versione e hash dell'input | `[REALE · derivato]` |

Ogni numero citato in una lezione deve indicare se viene da dati reali (con fonte), da una simulazione (con generatore e seme) o da un esempio didattico costruito a mano (`[ESEMPIO]`).

Richieste di dati aperte:
- [RICHIESTA-DATI-0.17.md](RICHIESTA-DATI-0.17.md) — dati del vault Obsidian per la tabella della lezione 0.17.
