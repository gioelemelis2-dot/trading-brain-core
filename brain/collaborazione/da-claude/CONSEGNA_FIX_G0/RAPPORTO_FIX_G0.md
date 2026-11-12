# Rapporto: repository canonico e correzioni di G0 e journal (Binario A)

**Data:** 12/11/2026 · **Autore:** Claude · **Mandato:** «Binario A: repo canonico & fix G0/Journal»
**Repository:** `gioelemelis2-dot/trading-brain-core` (privato) · **Ramo di lavoro:** `feat/fix-g0-journal`

## 1. Esito
| Passo | Esito |
|---|---|
| 1. Migrazione (D-19) | **Completata.** `main` contiene la storia della sola `brain/`, con albero identico all'origine |
| 2. Correzioni in TDD | **Completate.** 5 test scritti prima (5 rossi), poi 5 correzioni: **29/29 verdi** |
| 3. Auto-audit e consegna | Questo rapporto, `diff_fix_g0.patch`, `log_test_29.txt`, `MANIFEST.sha256` |

Vincoli rispettati:
- nessuna operatività reale;
- G0 resta consultivo (nessun blocco, nessun kill switch);
- V3.3 non toccata (i suoi file non sono nemmeno in questo repository);
- nessuna cartella creata in `brain/laboratorio/` né in `brain/dati/reali/`;
- modifiche al codice solo in `brain/guardian/`;
- fuori da `guardian/`, solo la configurazione del repository (`README.md` e `.gitignore` alla radice) e questa cartella di consegna, richiesta dal mandato.

## 2. Passo 1: migrazione
- **Origine:** repository `l-Altro`, ramo `claude/vibrant-cannon-5uunho`, commit `f6a2824` (24 commit).
- **Metodo:** clone del solo ramo in una cartella temporanea, poi `git filter-branch --index-filter` che rimuove ogni file fuori da `brain/`, con `--prune-empty`.
  - L'unico commit con file estranei, il commit iniziale di `l-Altro` (il suo `README.md` e il suo `.gitignore`), è diventato vuoto ed è stato eliminato.
  - Risultato: **23 commit**, nessun file fuori da `brain/` nella storia.
- **Verifica:** l'albero `brain/` del nuovo `main` ha lo stesso hash git dell'origine: `7422e1fc346bdcc12c2b37a184acd345db04845b`. I file sono quindi identici bit per bit.
- **Commit di configurazione** (`0a1f860`): `README.md` alla radice (provenienza della migrazione) e `.gitignore` (`__pycache__/`, `*.pyc`).
- **Pubblicazione:** `main` → `0a1f860` (24 commit). Ramo di lavoro `feat/fix-g0-journal` creato da `main`.
- **Nota:** i commit migrati hanno hash nuovi, per effetto della riscrittura. La corrispondenza con l'origine è data dall'hash dell'albero e dai messaggi. Il repository `l-Altro` non è stato modificato.

## 3. Passo 2: correzioni (TDD)
**Commit:**
- `9ff30e2`: solo i 5 test. Fase rossa: **2 fallimenti e 3 errori**, ciascuno per il motivo atteso (`log_test_29.txt`, sezione 1).
- `7e56023`: correzioni e documentazione di `guardian/`. Fase verde: **29/29**, anche con gli avvisi di Python trattati come errori (`-W error`).

| # | Difetto | Test (fase rossa) | Correzione |
|---|---|---|---|
| 1 | Lo scenario di stress era confrontato solo con il margine **giornaliero** | `TestFix1StressMargineTotale`: conto a 91.500 USD con margine totale di 1.500 e stress di 1.510,50 → il margine totale dopo lo stress (−10,50) non era né mostrato né segnalato | `g0/scheda.py`: riga «margine totale dopo lo scenario» e avviso «Nello scenario di stress il limite totale viene violato.» Aggiunto anche l'avviso per il trade previsto che supera il margine totale |
| 2 | Ai futures veniva assegnata una dimensione del contratto «1» come REGOLA con stato di verifica, anche se il calcolo usa solo il tick | `TestFix2MetadatiFutures`: future senza dimensione → errore di costruzione; FX senza dimensione accettato | `g0/strumenti.py`: `dimensione_contratto` facoltativa per i futures e obbligatoria per FX e CFD; tra gli input della perdita entrano **solo** le specifiche usate (passo e valore del tick per i futures). `g0/scheda.py`: nessun valore predefinito «1» |
| 3 | Le regole personali erano una stringa fissa: le regole confermate non si applicavano | `TestFix3RegolePersonali`: con P-01 confermata a 0,5%, il trade da 682 USD su 100.000 (0,682%) non produceva avvisi | `g0/scheda.py` legge `regole/regole_personali.toml` e applica **solo** `confermata = true`: P-01 rischio per trade; P-05 limite personale giornaliero; P-11 pausa dopo perdita; P-14 ore di sonno; P-15 perdite consecutive. Le altre confermate sono domande della checklist; i dati di sessione mancanti sono dichiarati; una regola confermata senza valore numerico produce un avviso |
| 4 | La catena di hash non rilevava modifica dell'ultima riga, troncamento e riscrittura completa | `TestFix4AncoraEsterna`: i tre casi passavano come «integri» | `journal/journal.py`: `ancora_integrita.json` (righe e SHA-256 dell'ultima riga per registro), scritta in modo atomico da `aggiungi()` e controllata da `verifica()`. Percorso separabile con `TRADING_JOURNAL_ANCHOR`; comando `ancora` che stampa l'impronta da annotare fuori dal journal |
| 5 | Gli indicatori usavano `float` e accettavano solo `…:SSZ` | `TestFix5IndicatoriDecimal`: errore con `09:33:00.120Z`; 0,3/0,1 in float vale 2,9999… | `journal/indicatori.py`: tutto in `Decimal`, con durate esatte da giorni, secondi e microsecondi; orari ISO-8601 in UTC con o senza frazioni di secondo, o con `+00:00`; orari senza fuso o non UTC rifiutati |

**Diff** (`main..7e56023`, solo `brain/guardian/`): 7 file, 349 righe aggiunte, 25 rimosse (`diff_fix_g0.patch`).

## 4. Auto-audit: limiti che restano
1. **Ancora del journal.** Se resta nella cartella dei dati (impostazione predefinita), una riscrittura **deliberata** di dati e ancora non viene rilevata. La protezione richiede l'ancora in un percorso separato e l'impronta annotata altrove. Un'interruzione tra la scrittura della riga e quella dell'ancora produce una segnalazione, che va risolta controllando l'ultima riga. È documentato in `journal/LEGGIMI.md`.
2. **Regole personali.** Il controllo automatico copre 5 regole su 15. Nessuna è confermata oggi, quindi in pratica la sezione dichiara «0 confermate su 15». I dati di sessione (`[sessione]`) li fornisce l'utente.
3. **G0 non validato.** La riconciliazione con un estratto conto reale (DA-25) manca ancora: la scheda continua a dichiarare in prima riga di non usarla per decidere.
4. **Test preesistente:** `test_g0.py` costruisce il future ES con una dimensione di 50, che ora viene semplicemente ignorata. Non l'ho modificato: il mandato chiedeva nuovi test, non la riscrittura dei vecchi.
5. **Documenti di continuità non aggiornati:** `CONTINUITA.md`, `REGISTRO-MODIFICHE.md` e `DECISIONI-APERTE.md` restano allo stato del commit `f6a2824`, perché sono fuori dal perimetro del mandato (`brain/guardian/` e configurazione). Vanno aggiornati con la migrazione (D-19 eseguita) e con questo lavoro, quando autorizzato.
6. **Repository precedente.** `l-Altro` non è stato modificato. Il ramo `claude/vibrant-cannon-5uunho` resta come copia storica: decidere se archiviarlo.

## 5. Come verificare
```bash
git clone https://github.com/gioelemelis2-dot/trading-brain-core && cd trading-brain-core && git checkout feat/fix-g0-journal
```
```bash
cd brain/guardian && python3 -s -B -W error -m unittest discover -s test -v
```
```bash
cd brain/collaborazione/da-claude/CONSEGNA_FIX_G0 && sha256sum -c MANIFEST.sha256
```
Verifica della migrazione: `git rev-parse main:brain` deve restituire `7422e1fc346bdcc12c2b37a184acd345db04845b`.
