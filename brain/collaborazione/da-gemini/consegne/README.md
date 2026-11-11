# Consegne di materiali da parte di Gemini

Stato: PROVVISORIO (prima fase di collaborazione).

Qui Gemini deposita codice, dati, risultati e studi da sottoporre a revisione. **Claude non modifica nulla in questa cartella.**

## Struttura di una consegna
```
consegne/
└── G-CONS-AAAAMMGG-NN-<argomento>/
    ├── MANIFEST.md          ← obbligatorio
    ├── LEGGIMI.md           ← obiettivo, metodo, risultati principali, limiti
    ├── codice/              ← motore, script
    ├── test/                ← test unitari
    ├── config/              ← rulebook YAML e altri parametri
    ├── risultati/           ← tabelle e grafici prodotti, con il seme usato
    └── dati/                ← solo se la licenza lo consente; altrimenti metadati + hash
```

## MANIFEST.md (obbligatorio)
| Voce | Contenuto |
|---|---|
| Id e data | `G-CONS-…`, data di consegna |
| Commit di origine | hash nel repository di lavoro di Gemini, se esiste |
| Elenco dei file | percorso, dimensione, **SHA-256** |
| Ambiente | versione di Python, sistema operativo, dipendenze con versione esatta |
| Come si esegue | comandi per test e per riprodurre ogni risultato citato |
| Semi casuali | per ogni risultato simulato |
| Dati | per ciascun dato: `[REALE]` (fonte, data, licenza) o `[SIMULATO]` (generatore, parametri) o `[IPOTESI]` |
| Regole esterne | per il rulebook: fonte ufficiale e data di consultazione di ogni regola |
| Risultati principali | i numeri che Gemini chiede di verificare, con riferimento al file che li produce |
| Limiti noti | ciò che Gemini sa essere semplificato o non verificato |

## Consegne attese
| Id previsto | Contenuto | Stato |
|---|---|---|
| G-CONS-…-ftmo | Studio di rovina operativa FTMO (10.000 simulazioni Monte Carlo), motore Python, test unitari, rulebook YAML, Strategy Discovery Lab | in attesa |
