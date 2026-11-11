# Piano di migrazione · il Trading Brain diventa un progetto autonomo

Versione 1.0 · 11/11/2026 · Stato: **PROPOSTA SOSPESA** (D-02 sospesa da D-10): non si esegue finché l'utente non riapre la questione
Nulla di quanto descritto qui è stato eseguito.

## 1. Situazione di partenza (fotografata il 11/11/2026)

| Elemento | Valore |
|---|---|
| Repository attuale | `gioelemelis2-dot/l-Altro` |
| Branch del Brain | `claude/vibrant-cannon-5uunho` (pubblicato su GitHub) |
| Branch principale di l-Altro | contiene solo il commit iniziale `4c180bf`: **il Brain non è mai stato unito a l-Altro** |
| Cartella | `brain/` (tutto il Brain sta qui; nessun file del Brain fuori da questa cartella) |
| Commit che toccano `brain/` | vedi `git log --oneline -- brain` al momento della migrazione |
| Collegamenti interni | tutti **relativi** e interni a `brain/` (verificati: nessun link rotto) |
| Riferimenti testuali a `brain/`, `l-Altro` o al branch | 5 righe in `CONTINUITA.md`, `piano/PIANO-ESPANSIONE.md`, `governance/STANDARD.md`, `governance/DECISIONI.md` (elenco generato con `grep -rn "brain/\|l-Altro\|vibrant-cannon"`) |
| Manuale v1 | artifact `https://claude.ai/artifact/T4xESphh3BmonZPoprQBtb` (indipendente dal repository) + copia in `brain/originale/` |

Conseguenza importante: **l-Altro non va "ripulito"**. Il suo branch principale non contiene il Brain.

## 2. Che cosa serve dall'utente prima di iniziare

1. **Nome del nuovo repository** (proposta: `trading-brain`) e visibilità (privato consigliato: contiene appunti personali e, in futuro, dati con licenze restrittive).
2. **Creare il repository vuoto su GitHub** (senza README, licenza o .gitignore, così non ci sono conflitti con la cronologia importata). In questa sessione Claude non può creare repository.
3. **Aggiungere il nuovo repository alla sessione** con permesso di scrittura (Claude lo chiederà con lo strumento dedicato quando approvi).
4. Decidere che cosa fare del branch in l-Altro dopo la migrazione (§6).

## 3. Metodo proposto: `git subtree split`

Estrae dalla cronologia di l-Altro **solo i commit che toccano `brain/`**, riscrivendoli in modo che `brain/` diventi la radice del nuovo repository.

| Che cosa si conserva | Che cosa cambia |
|---|---|
| Autori, date, messaggi di commit, ordine dei commit, contenuto dei file byte per byte | Gli **hash** dei commit (inevitabile: cambia il percorso dei file) |
| Collegamenti relativi tra file | I percorsi perdono il prefisso `brain/` (es. `brain/audit/01-DIAGNOSI.md` → `audit/01-DIAGNOSI.md`) |

Alternative valutate:

| Metodo | Pro | Contro | Esito |
|---|---|---|---|
| **A. `git subtree split --prefix=brain`** | Incluso in git; conserva la cronologia di `brain/` | Hash diversi | **Proposto** |
| B. `git filter-repo --subdirectory-filter brain` | Più veloce su grandi repository | Strumento esterno da installare; stesso risultato | Equivalente, di riserva |
| C. Copiare tutto il repository e cancellare i file di l-Altro | Hash identici | Porta nel nuovo progetto la cronologia di l-Altro (commit iniziale, README) | Scartato |
| D. Copiare i file senza cronologia | Semplice | **Perde la cronologia** | Scartato (contrario alla richiesta) |

## 4. Procedura passo per passo

```bash
# 0. Partire da una copia aggiornata
git fetch origin claude/vibrant-cannon-5uunho
git checkout claude/vibrant-cannon-5uunho

# 1. Fotografia "prima": elenco e hash di tutti i file
(cd brain && find . -type f -print0 | sort -z | xargs -0 sha256sum) > /tmp/prima.sha256
git log --format='%an|%ad|%s' -- brain > /tmp/prima.log

# 2. Estrazione della cronologia
git subtree split --prefix=brain -b esportazione-brain

# 3. Fotografia "dopo" e confronto (deve risultare IDENTICO)
git worktree add /tmp/verifica esportazione-brain
(cd /tmp/verifica && find . -type f -not -path './.git*' -print0 | sort -z | xargs -0 sha256sum) > /tmp/dopo.sha256
diff /tmp/prima.sha256 /tmp/dopo.sha256
git log --format='%an|%ad|%s' esportazione-brain > /tmp/dopo.log
diff /tmp/prima.log /tmp/dopo.log

# 4. Controlli funzionali sulla copia estratta
cd /tmp/verifica
python3 strumenti/verifica_m0.py
python3 strumenti/sorpresa_monetaria.py
python3 strumenti/riproduci_017.py --test
# + controllo dei link relativi (script usato nell'audit)

# 5. Pubblicazione nel nuovo repository
git remote add trading-brain https://github.com/<utente>/<nuovo-repo>.git
git push trading-brain esportazione-brain:main
```

## 5. Aggiornamenti dopo la migrazione (primo commit nel nuovo repository)

1. Aggiornare le 5 righe che citano `brain/`, `l-Altro` o il vecchio branch.
2. Aggiungere un `.gitignore` adatto (Python, dati locali non conservabili per licenza).
3. Aggiornare `CONTINUITA.md` (nuovo repository, branch di lavoro, convenzioni) e `collaborazione/HANDOFF-GEMINI.md` (nuovo indirizzo per Gemini).
4. Registrare la migrazione in `governance/REGISTRO-MODIFICHE.md` con la tabella di corrispondenza **hash vecchio → hash nuovo** dei commit (generata con `git log` sui due branch), così ogni riferimento storico resta rintracciabile.
5. Aggiornare D-02 in `governance/DECISIONI.md` a "eseguita".

## 6. Che cosa fare con l-Altro

| Opzione | Descrizione | Raccomandazione |
|---|---|---|
| **6a. Lasciare il branch com'è e marcarlo come archivio** | Si aggiunge un tag `archivio/brain-pre-migrazione` sul commit finale; il branch non viene mai unito a l-Altro | **Consigliata** per i primi mesi: rollback immediato possibile |
| 6b. Cancellare il branch del Brain da l-Altro | l-Altro torna esattamente com'era | Solo dopo che il nuovo repository è stato usato senza problemi; richiede approvazione separata |
| 6c. Lasciare in l-Altro un file che rimanda al nuovo repository | Utile solo se l-Altro deve sapere dell'esistenza del Brain | Non necessaria: il branch principale di l-Altro non ha mai contenuto il Brain |

## 7. Rischi e rollback

| Rischio | Prevenzione | Rollback |
|---|---|---|
| File mancanti o alterati | Confronto SHA-256 prima/dopo (§4 passo 3) | Il branch originale resta intatto in l-Altro |
| Cronologia incompleta | Confronto dei log (autore, data, messaggio) | Ripetere lo split |
| Link rotti | Controllo automatico dei link | Correzione nel primo commit |
| Gemini lavora sul vecchio percorso durante la migrazione | **Congelamento**: nessuna scrittura né da Claude né da Gemini dall'inizio della migrazione fino al nuovo `HANDOFF` (vedi `collaborazione/PROTOCOLLO-OPERATIVO.md` §4) | — |
| Lavoro fatto nel frattempo sul branch vecchio | Migrare solo con l'albero di lavoro pulito e nessun branch di Gemini aperto | Ripetere lo split dopo aver integrato |

## 8. Tempi e ordine consigliato

Conviene migrare **prima** che Gemini inizi a scrivere (le letture possono iniziare subito): così nessun riferimento di Gemini cita percorsi che poi cambiano. Durata stimata: una sessione breve, di cui la maggior parte in verifiche.

## 9. Approvazione

Per procedere servono, per iscritto: nome e visibilità del repository · conferma che è stato creato vuoto · scelta per l-Altro (6a/6b/6c) · via libera all'esecuzione.
