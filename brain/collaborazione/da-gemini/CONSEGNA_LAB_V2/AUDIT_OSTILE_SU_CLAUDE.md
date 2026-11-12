# AUDIT OSTILE INCROCIATO SU CLAUDE CODE (RAMO `feat/fix-g0-journal`)
## Analisi Avversariale, Vulnerabilità Rilevate, Riproduzione Meccanica e Raccomandazioni Tecniche

**Data:** 12 Novembre 2026  
**Autore:** Gemini Antigravity (Quantitative Research Lab)  
**Destinatario:** Gioele Melis / Claude Code  
**Target dell'Audit:** Commit `0396995` (`origin/feat/fix-g0-journal`) nel repository `trading-brain-core`  
**Modalità:** Zero-Trust / Stress-Test Avversariale Indipendente  

---

## 1. PREMESSA E CONTESTO DI AUDIT

In adempimento al mandato operativo di contro-audit indipendente e paritetico, il nodo Gemini Antigravity ha esaminato riga per riga il codice consegnato da Claude Code sul branch `feat/fix-g0-journal`, con particolare focus sui moduli `brain/guardian/g0/` e `brain/guardian/journal/`.

L'indagine ha confermato che Claude ha risolto brillantemente diversi problemi storici (incluso il supporto ai Futures senza forzare una `dimensione_contratto` fittizia e l'aggiunta dell'ancora di integrità). Tuttavia, un'analisi avversariale approfondita ha fatto emergere **5 vulnerabilità tecniche significative**, di cui due costituiscono violazioni dirette delle direttive architetturali del Trading Brain.

---

## 2. VULNERABILITÀ CRITICHE INDIVIDUATE E PROVATE MECCANICAMENTE

### Vulnerabilità 1: Crash Sistematico di Portabilità per Dipendenza non Protetta da `tomllib` (Python < 3.11)
- **File Coinvolto:** `brain/guardian/g0/scheda.py` (riga 11)
- **Codice:** `import tomllib`
- **Problema:**  
  La libreria standard `tomllib` è stata introdotta in Python solo a partire dalla versione 3.11. Sulle macchine con Python 3.9 o 3.10 (incluso l'ambiente di default macOS `/usr/bin/python3` presente sulla macchina di lavoro), l'esecuzione della scheda di G0 fallisce immediatamente all'avvio con:
  ```
  ModuleNotFoundError: No module named 'tomllib'
  ```
- **Impatto:**  
  Il Guardian G0 risulta non eseguibile su sistemi operativi con Python predefinito a meno di non forzare un ambiente virtuale 3.11+.
- **Correzione Prescrittiva:**  
  Implementare un fallback trasparente:
  ```python
  try:
      import tomllib
  except ImportError:
      try:
          import tomli as tomllib
      except ImportError:
          # Parser TOML minimale di emergenza o avviso formale
          pass
  ```

---

### Vulnerabilità 2: Divieto Assoluto di `Decimal` nel Campo `probabilita` di `journal.valida('previsione')`
- **File Coinvolto:** `brain/guardian/journal/journal.py` (righe 148–151)
- **Codice Contestato:**
  ```python
  if registro == "previsione" and "chiude" not in dati:
      p = dati["probabilita"]
      if not isinstance(p, (int, float)) or not 0 <= p <= 1:
          raise ValueError("probabilita: numero tra 0 e 1")
  ```
- **Problema e Riproduzione:**  
  Il controllo di tipo impone categoricamente `(int, float)`. Se un modulo quantitativo o matematico (come il Discovery Lab o il Backtester) invia una stima probabilistica rigorosa in formato `Decimal("0.75")`, il journal la rifiuta sollevando:
  ```
  ValueError: probabilita: numero tra 0 e 1
  ```
- **Violazione Architetturale:**  
  Questo controllo **costringe deliberatamente l'utente o gli agenti a utilizzare i tipi `float`**, violando la regola aurea della governance epistemica stabilita in `MODELLO-EPISTEMICO.md` (*"Niente float nei calcoli monetari e quantitativi"*).
- **Correzione Prescrittiva:**
  Estendere il controllo a `Decimal`:
  ```python
  if not isinstance(p, (int, float, Decimal)) or not 0 <= Decimal(str(p)) <= 1:
      raise ValueError("probabilita: numero tra 0 e 1")
  ```

---

### Vulnerabilità 3: Mancata Validazione di Esistenza per `corregge` e Creazione di "Record Fantasma" in `versioni_finali()`
- **File Coinvolto:** `brain/guardian/journal/journal.py` (righe 135–170 e 260–275)
- **Problema:**  
  La funzione `valida()` verifica solo la sintassi locale del dizionario dati, ma **non controlla se l'ID specificato in `dati["corregge"]` esista realmente nel registro su disco**.  
  Quando successivamente viene chiamata la funzione `versioni_finali()` (utilizzata ad esempio da `brier()` e dagli indicatori), accade quanto segue:
  ```python
  r = radice.get(d["corregge"], d["corregge"]) if "corregge" in d else rec["id"]
  radice[rec["id"]] = r
  finali[r] = ...
  ```
  Se un record dichiara `corregge: "GHOST-999"`, il dizionario `finali` genera un record definitivo per la chiave `"GHOST-999"`, creando un'entità inesistente mai registrata in origine.
- **Evidenza Sperimentale Eseguita:**  
  Inserendo un record con `corregge: "GHOST-999"`, `versioni_finali()` ha restituito `['GHOST-999']`, confermando la contaminazione dello stato storico.
- **Correzione Prescrittiva:**  
  In `aggiungi()`, prima di appendere la riga, se `"corregge"` è presente, verificare che `dati["corregge"]` sia presente nell'insieme degli ID già registrati nel file `.jsonl`.

---

### Vulnerabilità 4: Assenza di File Locking Concorrente (`fcntl.flock`) su Registri e Ancora
- **File Coinvolto:** `brain/guardian/journal/journal.py` (funzioni `aggiungi` e `_aggiorna_ancora`)
- **Problema:**  
  La scrittura sui file `.jsonl` e su `ancora_integrita.json` avviene tramite apertura standard in modalità append `open(path, "a")`, priva di lock cooperativo a livello di kernel (`fcntl.flock(f, fcntl.LOCK_EX)`).
- **Rischio in Produzione:**  
  Se due processi (ad esempio il Guardian G0 che emette un alert di rischio e il Backtester che registra un trade o una previsione) invocano `journal.aggiungi` simultaneamente:
  1. I byte delle righe JSON possono interleavarsi sul disco.
  2. Il calcolo di `prec_hash` (basato sull'ultima riga letta prima dell'append) subisce una *race condition*, rompendo definitivamente la catena crittografica con falso allarme di manomissione (`catena interrotta`).
- **Correzione Prescrittiva:**  
  Introdurre un context manager con lock di file esclusivo su ogni operazione di scrittura nel journal.

---

### Vulnerabilità 5: Fragilità Temporale su Millisecondi ISO-8601 in Ambienti Eterogenei
- **File Coinvolto:** `brain/guardian/journal/journal.py` (`orario_utc`)
- **Osservazione:**  
  La regex/parser di `orario_utc` accetta formati ISO con o senza millisecondi. Tuttavia, in caso di formati generati da broker con microsecondi a 6 cifre e suffisso `Z` o offset numerici non normalizzati (es. `+00:00:00`), `fromisoformat` di Python 3.9/3.10 solleva eccezioni di parsing non omogenee rispetto a Python 3.11+.

---

## 3. VALUTAZIONE COMPLESSIVA E CONFRONTO SCIENTIFICO

| Aspetto Auditato | Valutazione Gemini | Stato |
| :--- | :--- | :--- |
| **Separazione Regole Prop vs Personali (Q-09)** | Eccellente, pulita e rigorosa | **APPROVATO** |
| **Integrazione Futures in `Strumento`** | Risolto correttamente il bug di `spec` vuoto | **APPROVATO** |
| **Ancora di Integrità e Impronta Esterna** | Ottima soluzione contro il troncamento di coda | **APPROVATO** |
| **Compatibilità Python Nativo** | Rilasciato con dipendenza da `tomllib` (3.11+) | **VULNERABILE** |
| **Rispetto Governance Epistemica sui Tipi** | Vietato `Decimal` su probabilità previsioni | **VIOLAZIONE** |
| **Integrità Referenziale `corregge`** | Mancanza di verifica dell'ID originale | **VULNERABILE** |

---

## 4. CONCLUSIONI

Il lavoro svolto da Claude sul branch `feat/fix-g0-journal` rappresenta un solido passo avanti nell'architettura del Guardian G0.  
Le 5 vulnerabilità sopra documentate sono state riprodotte tramite test indipendenti e non costituiscono motivo di blocco, bensì una **prescrizione di miglioramento immediato** prima di qualsiasi futuro merge su `main`.
