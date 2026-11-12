# Rapporto: repository canonico e correzioni di G0 e journal (Binario A)

**Data:** 12/11/2026 · **Autore:** Claude · **Mandati:** «Binario A: repo canonico & fix G0/Journal» e «Contro-audit indipendente su feat/fix-g0-journal» (§4)
**Repository:** `gioelemelis2-dot/trading-brain-core` (privato) · **Ramo di lavoro:** `feat/fix-g0-journal`

## 1. Esito
| Passo | Esito |
|---|---|
| 1. Migrazione (D-19) | **Completata.** `main` contiene la storia della sola `brain/`, con albero identico all'origine |
| 2. Correzioni in TDD | **Completate.** 5 test scritti prima (5 rossi), poi 5 correzioni: **29/29 verdi** |
| 3. Auto-audit e consegna | Questo rapporto, `diff_fix_g0.patch`, `log_test_36.txt`, `MANIFEST.sha256` |
| 4. Contro-audit (7 rilievi bloccanti) | **Risolti.** 7 test scritti prima (7 rossi), poi le correzioni: **36/36 verdi** con `-W error` |

Vincoli rispettati:
- nessuna operatività reale;
- G0 resta consultivo (nessun blocco, nessun kill switch);
- V3.3 non toccata (i suoi file non sono nemmeno in questo repository);
- nessuna cartella creata in `brain/laboratorio/` né in `brain/dati/reali/`;
- modifiche al codice solo in `brain/guardian/`;
- fuori da `guardian/`, solo la configurazione del repository (`README.md` e `.gitignore` alla radice), questa cartella di consegna (richiesta dal mandato) e, con il contro-audit, i tre documenti di continuità autorizzati (`CONTINUITA.md`, `governance/REGISTRO-MODIFICHE.md`, `governance/DECISIONI-APERTE.md`).

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
- `9ff30e2`: solo i 5 test. Fase rossa: **2 fallimenti e 3 errori**, ciascuno per il motivo atteso (`log_test_36.txt`, sezione 1).
- `7e56023`: correzioni e documentazione di `guardian/`. Fase verde: **29/29**, anche con gli avvisi di Python trattati come errori (`-W error`).

| # | Difetto | Test (fase rossa) | Correzione |
|---|---|---|---|
| 1 | Lo scenario di stress era confrontato solo con il margine **giornaliero** | `TestFix1StressMargineTotale`: conto a 91.500 USD con margine totale di 1.500 e stress di 1.510,50 → il margine totale dopo lo stress (−10,50) non era né mostrato né segnalato | `g0/scheda.py`: riga «margine totale dopo lo scenario» e avviso «Nello scenario di stress il limite totale viene violato.» Aggiunto anche l'avviso per il trade previsto che supera il margine totale |
| 2 | Ai futures veniva assegnata una dimensione del contratto «1» come REGOLA con stato di verifica, anche se il calcolo usa solo il tick | `TestFix2MetadatiFutures`: future senza dimensione → errore di costruzione; FX senza dimensione accettato | `g0/strumenti.py`: `dimensione_contratto` facoltativa per i futures e obbligatoria per FX e CFD; tra gli input della perdita entrano **solo** le specifiche usate (passo e valore del tick per i futures). `g0/scheda.py`: nessun valore predefinito «1» |
| 3 | Le regole personali erano una stringa fissa: le regole confermate non si applicavano | `TestFix3RegolePersonali`: con P-01 confermata a 0,5%, il trade da 682 USD su 100.000 (0,682%) non produceva avvisi | `g0/scheda.py` legge `regole/regole_personali.toml` e applica **solo** `confermata = true`: P-01 rischio per trade; P-05 limite personale giornaliero; P-11 pausa dopo perdita; P-14 ore di sonno; P-15 perdite consecutive. Le altre confermate sono domande della checklist; i dati di sessione mancanti sono dichiarati; una regola confermata senza valore numerico produce un avviso |
| 4 | La catena di hash non rilevava modifica dell'ultima riga, troncamento e riscrittura completa | `TestFix4AncoraEsterna`: i tre casi passavano come «integri» | `journal/journal.py`: `ancora_integrita.json` (righe e SHA-256 dell'ultima riga per registro), scritta in modo atomico da `aggiungi()` e controllata da `verifica()`. Percorso separabile con `TRADING_JOURNAL_ANCHOR`; comando `ancora` che stampa l'impronta da annotare fuori dal journal |
| 5 | Gli indicatori usavano `float` e accettavano solo `…:SSZ` | `TestFix5IndicatoriDecimal`: errore con `09:33:00.120Z`; 0,3/0,1 in float vale 2,9999… | `journal/indicatori.py`: tutto in `Decimal`, con durate esatte da giorni, secondi e microsecondi; orari ISO-8601 in UTC con o senza frazioni di secondo, o con `+00:00`; orari senza fuso o non UTC rifiutati |

Diff di questa fase (`main..7e56023`, solo `brain/guardian/`): 7 file, 349 righe aggiunte, 25 rimosse. La patch consegnata ora copre anche il contro-audit (§4).

## 4. Contro-audit: 7 rilievi bloccanti
**Commit:**
- `2dcb9aa`: solo i 7 test. Fase rossa: **6 fallimenti e 1 errore**, ciascuno per il motivo atteso (`log_test_36.txt`, sezione 2).
- `357e48d`: correzioni e documentazione. Fase verde: **36/36**, con `-W error` (sezione 3).
- I test non sono cambiati tra la fase rossa e la verde: `git diff 2dcb9aa..357e48d -- brain/guardian/test` è vuoto.

| # | Rilievo | Test (fase rossa) | Correzione |
|---|---|---|---|
| 1 | P-05 non controllava che il limite personale fosse più stretto di quello della prop firm; un `elif` sopprimeva l'avviso di stress quando scattava quello del trade | `TestAudit1P05RegolaAurea`: P-05 al 4% su FTMO 1-Step (limite giornaliero 3%) non segnalato. Il test copre anche P-05 allo 0,4%: margine 150 USD, trade 682 e stress 842,50, che richiede entrambi gli avvisi | `g0/scheda.py`: se il limite personale non è più stretto, avviso «vale il limite della prop firm; correggere la regola». Altrimenti gli avvisi del trade e dello stress sono due controlli indipendenti |
| 2 | P-01 controllava solo il rischio per trade; la seconda parte («size maggiore del trade precedente dopo una perdita») era ignorata | `TestAudit2P01SecondaParte`: nessuna riga sulla seconda parte né con i dati né senza | `[sessione]` accetta `ultima_operazione_in_perdita` (vero/falso) e `size_precedente`:<br>• dati mancanti → «P-01 (seconda parte) non verificata: servono …»;<br>• dati non validi → avviso;<br>• in perdita e size maggiore → avviso «size maggiore della precedente dopo una perdita»;<br>• altrimenti → «verificata, nessuna violazione» |
| 3 | `journal.valida()` accettava testo al posto dei numeri, valori nulli o negativi, orari non ISO e chiusure prima dell'apertura. Un record malformato non si toglie più dalla catena | `TestAudit3ValidazioneJournal`: `aperto_utc="ieri"` accettato (primo caso del test) | `journal/journal.py`, all'ingresso:<br>• numeri `Decimal` finiti;<br>• `ingresso`, `stop`, `quantita`, `uscita` e `target` maggiori di zero;<br>• orari ISO-8601 in UTC, compresi `scadenza_utc` ed `esito_utc`;<br>• `chiuso_utc` non prima di `aperto_utc`;<br>• `data` come data ISO;<br>• `ore_sonno` tra 0 e 24;<br>• `corregge` e `chiude` puntano a un record esistente |
| 4 | `brier()` ignorava `corregge` | `TestAudit4BrierCorrezioni`: risultato 0,04 (previsione originale 0,8) invece di 0,16 (previsione corretta 0,6) | Nuova `versioni_finali()`: applica le correzioni, anche a catena, e riconduce `chiude` all'originale. La usano `brier()` e, per coerenza, `indicatori.trade_da_journal()` |
| 5 | `verifica()` dava «integro» se dati e ancora erano stati cancellati insieme | `TestAudit5ImprontaEsterna`: `verifica()` non accettava un'impronta attesa | `verifica(cartella, impronta_attesa)` e CLI `verifica --impronta <sha256>`: errore se l'ancora manca o se la sua impronta non coincide. Smoke test: journal cancellato → «ancora assente ma impronta attesa fornita…», uscita 1 |
| 6 | G0 accettava capitale, prezzi, quantità, cambi e specifiche nulli o negativi, e stop uguale all'ingresso | `TestAudit6Positivita`: 9 casi; il primo (capitale iniziale zero) accettato senza errore | `g0/strumenti.py`: rifiutati `dimensione_contratto`, `passo_tick` e `valore_tick` non positivi o non finiti, e così `ingresso`, `stop`, `quantita` e `cambio`; rifiutato `ingresso == stop`. `g0/limiti.py`: `capitale_iniziale` deve essere positivo |
| 7 | Documenti di continuità fermi a prima della migrazione | `TestAudit7Continuita`: `trading-brain-core` assente da `CONTINUITA.md` | Aggiornati `CONTINUITA.md` (repository canonico e stato), `DECISIONI-APERTE.md` (DA-01 eseguita) e `REGISTRO-MODIFICHE.md` (voce v1.12: migrazione e correzioni) |

Precisazioni:
- **Rilievo 4.** Il difetto è reale, ma il meccanismo descritto nel contro-audit va precisato. Senza correzioni applicate, `brier()` usa la versione **vecchia** della previsione: la correzione, priva di `chiude`, veniva contata come una previsione separata ancora aperta. Il doppio conteggio avviene solo se ricevono un esito sia l'originale sia la correzione. Il test copre entrambi i casi (n = 1 in tutti e due).
- **Rilievo 3.** La validazione vale per i record nuovi. Quelli già scritti non vengono riletti con le nuove regole: oggi il journal reale è vuoto, quindi non ci sono record da sanare.

Diff dell'intero lavoro (`main..357e48d`, `brain/guardian/` più i tre documenti di continuità): 11 file, 627 righe aggiunte, 59 rimosse. Solo il contro-audit (`7e56023..357e48d`): 11 file, 291 righe aggiunte, 47 rimosse. Il file è `diff_fix_g0.patch`; la cartella di consegna è esclusa perché conterrebbe sé stessa.

**Nota sui file di consegna:** `log_test_29.txt` è stato rinominato `log_test_36.txt`. Contiene entrambe le fasi rosse, rieseguite sui commit `9ff30e2` e `2dcb9aa` in copie di lavoro separate, e la fase verde su `357e48d`. I quattro file restano quattro.

## 5. Auto-audit: limiti che restano
1. **Ancora del journal.** Se resta nella cartella dei dati (impostazione predefinita), una riscrittura **deliberata** di dati e ancora è rilevata solo con `verifica --impronta`, usando un'impronta annotata altrove.
   - L'impronta cambia a ogni `aggiungi`: va annotata di nuovo, almeno a fine sessione.
   - Chi controlla anche il luogo dove è annotata può sostituire anche quella.
   - Un'interruzione tra la scrittura della riga e quella dell'ancora produce una segnalazione, che va risolta controllando l'ultima riga.
   - Tutto questo è documentato in `journal/LEGGIMI.md`.
2. **Correzioni nel journal.** Una correzione sostituisce **l'intero** record, non solo i campi cambiati, e va scritta completa (lo schema lo impone).
3. **Regole personali.** Il controllo automatico copre 5 regole su 15 (P-01 in entrambe le parti, P-05, P-11, P-14, P-15).
   - Nessuna è confermata oggi: in pratica la sezione dichiara «0 confermate su 15».
   - I dati di sessione (`[sessione]`) li fornisce l'utente.
   - P-05 è confrontata con il limite giornaliero della prop firm espresso come frazione del capitale iniziale: è corretto per FTMO, ma con regole espresse diversamente va rivisto.
4. **G0 non validato.** La riconciliazione con un estratto conto reale (DA-25) manca ancora: la scheda continua a dichiarare in prima riga di non usarla per decidere.
5. **Test preesistente:** `test_g0.py` costruisce il future ES con una dimensione di 50, che ora viene semplicemente ignorata. Non l'ho modificato: entrambi i mandati chiedevano nuovi test, non la riscrittura dei vecchi.
6. **Repository precedente.** `l-Altro` non è stato modificato. Il ramo `claude/vibrant-cannon-5uunho` resta come copia storica: decidere se archiviarlo.
7. **Merge su `main`:** sospeso fino a decisione dell'utente.

## 6. Come verificare
```bash
git clone https://github.com/gioelemelis2-dot/trading-brain-core && cd trading-brain-core && git checkout feat/fix-g0-journal
```
```bash
cd brain/guardian && python3 -s -B -W error -m unittest discover -s test -v
```
```bash
cd brain/collaborazione/da-claude/CONSEGNA_FIX_G0 && sha256sum -c MANIFEST.sha256
```
Fase rossa del contro-audit: `git checkout 2dcb9aa`, poi lo stesso comando dei test (attesi 6 fallimenti e 1 errore).

Verifica della migrazione: `git rev-parse main:brain` deve restituire `7422e1fc346bdcc12c2b37a184acd345db04845b`.
