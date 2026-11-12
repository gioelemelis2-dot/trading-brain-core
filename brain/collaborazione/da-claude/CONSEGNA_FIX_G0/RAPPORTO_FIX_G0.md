# Rapporto: repository canonico e correzioni di G0 e journal (Binario A)

**Data:** 12/11/2026 · **Autore:** Claude · **Mandati:** «Binario A: repo canonico & fix G0/Journal» «Contro-audit indipendente su feat/fix-g0-journal» (§4) e «Mandato notturno zero-trust e anti-frode» (§5)
**Repository:** `gioelemelis2-dot/trading-brain-core` (privato) · **Ramo di lavoro:** `feat/fix-g0-journal`

## 1. Esito
| Passo | Esito |
|---|---|
| 1. Migrazione (D-19) | **Completata.** `main` contiene la storia della sola `brain/`, con albero identico all'origine |
| 2. Correzioni in TDD | **Completate.** 5 test scritti prima (5 rossi), poi 5 correzioni: **29/29 verdi** |
| 3. Auto-audit e consegna | Questo rapporto, `AUDIT_OSTILE_SU_GEMINI.md`, `diff_fix_g0.patch`, `log_test_40_e_mutazioni_24.txt`, `MANIFEST.sha256` |
| 4. Contro-audit (7 rilievi bloccanti) | **Risolti.** 7 test scritti prima (7 rossi), poi le correzioni: **36/36 verdi** con `-W error` |
| 5. Mandato notturno | **Completato.** 4 difetti richiesti più 1 trovato in auto-audit: 5 test rossi, poi le correzioni (41/41). Mutation testing: **44/44 mutanti non equivalenti uccisi** (erano 30/44, servivano 11 test in più). Suite finale **52/52 verdi** con `-W error`. Audit su Gemini consegnato |

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
- `9ff30e2`: solo i 5 test. Fase rossa: **2 fallimenti e 3 errori**, ciascuno per il motivo atteso (`log_test_40_e_mutazioni_24.txt`, sezione 1).
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
- `2dcb9aa`: solo i 7 test. Fase rossa: **6 fallimenti e 1 errore**, ciascuno per il motivo atteso (`log_test_40_e_mutazioni_24.txt`, sezione 2).
- `357e48d`: correzioni e documentazione. Fase verde: **36/36**, con `-W error`. Questi 36 test sono compresi nelle fasi verdi del log attuale (sezioni 4 e 6).
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

Diff del solo contro-audit (`7e56023..357e48d`): 11 file, 291 righe aggiunte, 47 rimosse.

**Nota sui file di consegna:** il log è stato rinominato due volte: `log_test_29.txt` → `log_test_36.txt` (contro-audit) → `log_test_40_e_mutazioni_24.txt` (nome richiesto dal mandato notturno).

## 5. Mandato notturno zero-trust e anti-frode

### 5.1 Task 1: difetti residui (TDD)
**Commit:**
- `9170ecf`: solo i test. Fase rossa: **5 fallimenti**, ciascuno per il motivo atteso (log, sezione 3).
- `ab0e48f`: correzioni e documentazione. Fase verde: **41/41** con `-W error` (log, sezione 4).

| # | Difetto | Test (fase rossa) | Correzione |
|---|---|---|---|
| 1 | `perdita_allo_stop` accettava commissioni negative o non finite: `perdita += commissioni` **riduceva** la perdita | `TestNotte1Commissioni`: `-200` accettato | `g0/strumenti.py`: commissioni finite e `>= 0` (0 ammesso per i conti solo spread), altrimenti `ValueError` |
| 2 | P-05: con margine personale negativo, l'`else` sopprimeva gli avvisi su trade e stress | `TestNotte2P05MarginePersonaleNegativo`: equity 99.900, margine personale −100: c'era solo «già superato» | `g0/scheda.py`: i tre avvisi sono controlli indipendenti |
| 3 | Journal: `corregge` e `chiude` controllati solo come «id esistente» | `TestNotte3SemanticaJournal`: un esito che correggeva una previsione era accettato | `journal/journal.py`, nuova `controlla_riferimenti`, chiamata da `aggiungi` **e da `verifica`**, quindi rileva anche un file scritto a mano:<br>• (a) `corregge` collega record della stessa natura;<br>• (b) `chiude` punta solo all'id radice di una previsione;<br>• (c) nessun secondo esito senza `corregge`, e una correzione di esito chiude la stessa previsione dell'esito corretto |
| 4 | Soglie e dati di sessione: booleani, negativi, NaN e infiniti non rifiutati. Una soglia NaN mandava in errore il confronto (`InvalidOperation`) | `TestNotte4DatiSessione`: `ore_sonno = true` dava «non numerico» invece di «non valido». Verificato a parte sullo stesso commit `9170ecf`: con `ore_sonno = NaN` o una soglia NaN la scheda andava in errore (`InvalidOperation`); con −5 minuti segnalava una violazione di P-11 basata su un dato non valido | `g0/scheda.py`: `_numero` allineata a `journal._decimale` (rifiuta booleani, NaN e infiniti), più `_soglia_valida` e `_dato_sessione_valido`. Validi sono:<br>• soglie positive, frazioni sotto 1, sonno ≤ 24, perdite consecutive intere;<br>• dati di sessione non negativi, sonno ≤ 24, perdite intere.<br>Un dato non valido produce «non valido: regola non verificata» |
| 5 | (auto-audit) In Python `True == 1`: `probabilita: true`, `esito: true` e `aderenza: true` passavano la validazione del journal | `TestNotte5BooleaniJournal`: `probabilita=True` accettata | `journal/journal.py`: booleani rifiutati (`type(x) is int` per `esito` e `aderenza`) |

Scelte da segnalare:
- **Punto 3.** Una correzione di esito non può spostare la chiusura su un'altra previsione: per farlo andrebbe corretto l'esito e chiusa l'altra previsione con un nuovo esito.
- **Punto 3 in `verifica`.** Un record che viola le regole viene segnalato e non entra fra i record di riferimento: i record successivi che lo citano risultano anch'essi segnalati, a cascata.
- **Punto 1.** Nel journal le commissioni restano solo «numero finito», anche negative. Il journal registra le misure come le dà il broker (un rimborso può essere negativo), mentre il G0 calcola il rischio e non accetta che le commissioni lo riducano.

### 5.2 Task 2: mutation testing (`guardian/test/mutazioni_g0_journal.py`)
- **Metodo**, modellato su `mutazioni_v3_3.py`:
  - una copia isolata di `guardian/` per ogni mutante, più i 3 documenti di continuità letti da `TestAudit7`: senza, ogni mutante morirebbe per il motivo sbagliato;
  - controllo che la copia **non mutata** superi la suite;
  - ogni sostituzione presente una sola volta nell'originale;
  - modulo importato **dalla copia** e contenente la mutazione (percorso e testo controllati);
  - suite eseguita con `-W error`.
- **Mutanti:** 44 non equivalenti sui 6 file operativi (`valori.py` 4, `strumenti.py` 7, `limiti.py` 6, `scheda.py` 11, `journal.py` 12, `indicatori.py` 4), più 1 equivalente dichiarato (E01).
- **Primo giro, commit `1d1c4f1` con i 41 test: 30/44.** I 14 sopravvissuti riguardavano:
  - i casi limite delle regole (`<` contro `<=`);
  - i valori infiniti;
  - le riserve nello scenario di stress;
  - le correzioni a catena;
  - i fusi orari diversi da UTC;
  - R1 al limite e i pareggi.
  - Il dato è in sé un risultato: i 41 test non presidiavano i confini delle regole.
- **Test aggiunti** (`test/test_mutanti_g0_journal.py`, commit `ac8fe15`): 11 test, verdi sul codice esistente perché servono a uccidere mutanti, non a correggere difetti. I valori attesi vengono dalle regole, non dal codice; per esempio FTMO considera violazione l'equity **sotto** il limite, quindi l'equity esattamente al limite non lo è.
- **Giro finale, commit `4eb79e0`: 44/44** (log, sezioni 5 e 7).
- **E01 (equivalente):** rimuovere il confronto del numero di righe dall'ancora non cambia l'esito di `verifica()`.
  - Se l'ultima riga coincide con quella ancorata, il suo `prec_hash` fissa tutta la catena fino alla genesi.
  - Controllato anche sperimentalmente: 3.000 manomissioni casuali di 8 tipi (duplicazioni, troncamenti, rimozioni, scambi, ripetizioni) non hanno mai dato un esito diverso fra originale e mutante.

| ID | File | Mutazione | 1° giro (`1d1c4f1`, 41 test) | Finale (`4eb79e0`, 52 test) | Test che lo uccidono |
|---|---|---|---|---|---|
| V01 | `g0/valori.py` | tipo del risultato = il PIÙ FORTE fra gli input | ucciso | **ucciso** | `test_limite_e_derivato_dalla_regola_verificata`, `test_fx_conto_nella_valuta_quotata`, `test_propagazione_del_tipo_piu_debole_e_delle_condizioni` |
| V02 | `g0/valori.py` | NON STIMABILE non più contagioso | ucciso | **ucciso** | `test_non_stimabile_contagioso_e_incertezza_obbligatoria`, `test_le_riserve_entrano_nello_scenario` |
| V03 | `g0/valori.py` | restringi può allargare il limite | ucciso | **ucciso** | `test_una_stima_non_allarga_mai_un_limite` |
| V04 | `g0/valori.py` | stato di verifica = il PIÙ FORTE | ucciso | **ucciso** | `test_propagazione_del_tipo_piu_debole_e_delle_condizioni` |
| V05 | `g0/strumenti.py` | commissioni omesse dalla perdita | ucciso | **ucciso** | `test_avviso_se_lo_stress_viola_il_limite_totale`, `test_commissioni_negative_o_non_finite_rifiutate`, `test_vendita_allo_scoperto_e_commissioni`, `test_esempio_end_to_end`, `test_equity_esattamente_al_limite_non_e_violazione` |
| V06 | `g0/strumenti.py` | commissioni negative ammesse | ucciso | **ucciso** | `test_commissioni_negative_o_non_finite_rifiutate` |
| V07 | `g0/strumenti.py` | cambio FX: * invece di / | ucciso | **ucciso** | `test_fx_terza_valuta_richiede_cambio_misurato` |
| V08 | `g0/strumenti.py` | valuta base convertita al prezzo d'ingresso invece che allo stop | ucciso | **ucciso** | `test_fx_conto_nella_valuta_base_converte_al_prezzo_dello_stop`, `test_esempio_end_to_end` |
| V09 | `g0/strumenti.py` | controllo is_finite() rimosso su prezzi, quantità e cambio | sopravvissuto | **ucciso** | `test_prezzi_quantita_e_cambi_infiniti_rifiutati` |
| V10 | `g0/strumenti.py` | distanza non multipla del tick ammessa | ucciso | **ucciso** | `test_future_tick` |
| V11 | `g0/strumenti.py` | stop uguale all'ingresso ammesso | ucciso | **ucciso** | `test_valori_non_positivi_rifiutati` |
| V12 | `g0/limiti.py` | limite giornaliero: frazione applicata al saldo invece che al capitale iniziale | ucciso | **ucciso** | `test_1step_giornaliero_e_trailing`, `test_2step_giornaliero_esempio_ufficiale`, `test_instant_esempio_ufficiale`, `test_equity_esattamente_al_limite_non_e_violazione` |
| V13 | `g0/limiti.py` | frazioni FTMO scambiate (giornaliero con la frazione totale) | ucciso | **ucciso** | `test_1step_giornaliero_e_trailing`, `test_2step_giornaliero_esempio_ufficiale`, `test_instant_esempio_ufficiale`, `test_equity_esattamente_al_limite_non_e_violazione` |
| V14 | `g0/limiti.py` | trailing 1-Step/Instant ignorato | ucciso | **ucciso** | `test_1step_giornaliero_e_trailing`, `test_instant_esempio_ufficiale` |
| V15 | `g0/limiti.py` | 2-Step trattato come trailing | ucciso | **ucciso** | `test_2step_totale_statico` |
| V16 | `g0/limiti.py` | capitale iniziale non positivo ammesso | ucciso | **ucciso** | `test_valori_non_positivi_rifiutati` |
| V17 | `g0/limiti.py` | scenario di stress senza le riserve dichiarate | sopravvissuto | **ucciso** | `test_le_riserve_entrano_nello_scenario` |
| V18 | `g0/scheda.py` | P-05 regola aurea: >= diventa > (limite personale UGUALE a quello FTMO accettato) | sopravvissuto | **ucciso** | `test_p05_uguale_al_limite_della_prop_non_e_piu_stretto` |
| V19 | `g0/scheda.py` | P-01: > diventa >= (rischio uguale alla soglia segnalato) | sopravvissuto | **ucciso** | `test_p01_rischio_uguale_alla_soglia_non_la_supera` |
| V20 | `g0/scheda.py` | P-11/P-14: < diventa <= (valore uguale alla soglia = violazione) | sopravvissuto | **ucciso** | `test_p11_e_p14_valore_uguale_alla_soglia_rispetta_la_regola` |
| V21 | `g0/scheda.py` | P-15: >= diventa > (raggiunto il massimo di perdite: nessun avviso) | sopravvissuto | **ucciso** | `test_p15_raggiunto_il_massimo_di_perdite_consecutive` |
| V22 | `g0/scheda.py` | P-05: avvisi su trade soppressi a margine personale negativo (difetto reintrodotto) | ucciso | **ucciso** | `test_avvisi_trade_e_stress_anche_a_limite_personale_superato` |
| V23 | `g0/scheda.py` | trade previsto: > diventa >= sul margine giornaliero (equity AL limite = violazione) | sopravvissuto | **ucciso** | `test_equity_esattamente_al_limite_non_e_violazione` |
| V24 | `g0/scheda.py` | posizione aperta misurata dal prezzo d'ingresso | ucciso | **ucciso** | `test_esempio_end_to_end`, `test_equity_esattamente_al_limite_non_e_violazione` |
| V25 | `g0/scheda.py` | dati di sessione negativi ammessi | ucciso | **ucciso** | `test_dati_di_sessione_e_soglie_non_validi` |
| V26 | `g0/scheda.py` | _numero accetta NaN e infiniti | ucciso | **ucciso** | `test_dati_di_sessione_e_soglie_non_validi` |
| V27 | `g0/scheda.py` | stress: < diventa <= sul margine giornaliero dopo lo scenario | sopravvissuto | **ucciso** | `test_equity_esattamente_al_limite_non_e_violazione` |
| V28 | `g0/scheda.py` | stress: margine totale dopo lo scenario non controllato | ucciso | **ucciso** | `test_avviso_se_lo_stress_viola_il_limite_totale` |
| V29 | `journal/journal.py` | versioni_finali: catene di correzioni non risolte | sopravvissuto | **ucciso** | `test_brier_e_indicatori_con_correzione_di_una_correzione` |
| V30 | `journal/journal.py` | impronta esterna non controllata | ucciso | **ucciso** | `test_verifica_con_impronta_rileva_cancellazione_totale` |
| V31 | `journal/journal.py` | doppia chiusura di una previsione ammessa | ucciso | **ucciso** | `test_corregge_e_chiude_coerenti_e_nessuna_doppia_chiusura` |
| V32 | `journal/journal.py` | chiude verso una correzione ammesso | ucciso | **ucciso** | `test_corregge_e_chiude_coerenti_e_nessuna_doppia_chiusura` |
| V33 | `journal/journal.py` | corregge fra record di natura diversa ammesso | ucciso | **ucciso** | `test_corregge_e_chiude_coerenti_e_nessuna_doppia_chiusura` |
| V34 | `journal/journal.py` | catena di hash non controllata | ucciso | **ucciso** | `test_catena_integra_e_manomissione_scoperta` |
| V35 | `journal/journal.py` | Brier: errore assoluto invece del quadrato | ucciso | **ucciso** | `test_brier_applica_le_correzioni`, `test_brier`, `test_brier_e_indicatori_con_correzione_di_una_correzione` |
| V36 | `journal/journal.py` | journal: orari non UTC ammessi | sopravvissuto | **ucciso** | `test_journal_rifiuta_fusi_diversi_da_utc_e_ammette_apertura_uguale_a_chiusura` |
| V37 | `journal/journal.py` | journal: chiusura nello stesso istante dell'apertura rifiutata (< diventa <=) | sopravvissuto | **ucciso** | `test_journal_rifiuta_fusi_diversi_da_utc_e_ammette_apertura_uguale_a_chiusura` |
| V38 | `journal/journal.py` | journal: probabilità booleana ammessa | ucciso | **ucciso** | `test_booleani_rifiutati_come_numeri` |
| V39 | `journal/journal.py` | sigillo verificato senza nonce | ucciso | **ucciso** | `test_sigillo` |
| V40 | `journal/journal.py` | ancora non controllata da verifica() | ucciso | **ucciso** | `test_ancora_rileva_ultima_riga_troncamento_e_riscrittura` |
| V41 | `journal/indicatori.py` | indicatori: microsecondi ignorati nelle durate | ucciso | **ucciso** | `test_decimal_e_frazioni_di_secondo` |
| V42 | `journal/indicatori.py` | indicatori: orari non UTC ammessi | sopravvissuto | **ucciso** | `test_indicatori_rifiutano_fusi_diversi_da_utc` |
| V43 | `journal/indicatori.py` | R1: < invece di <= sui minuti (rientro esattamente al limite escluso) | sopravvissuto | **ucciso** | `test_r1_rientro_esattamente_al_limite_e_pareggio` |
| V44 | `journal/indicatori.py` | indicatori: un pareggio conta come perdita | sopravvissuto | **ucciso** | `test_r1_rientro_esattamente_al_limite_e_pareggio` |
| E01 | `journal/journal.py` | ancora: confronto del numero di righe rimosso (EQUIVALENTE) | equivalente | **equivalente** | — |

### 5.3 Task 3: audit su Gemini
Dettaglio in `AUDIT_OSTILE_SU_GEMINI.md`. In sintesi:
- il ramo `feat/lab-dati-backtester` **non è su GitHub**: test ostili sul Binario B non eseguibili;
- `dsr.py` e `slippage_fixed` non esistono in nessuna fonte accessibile;
- **138/138** coppie (file, hash) dichiarate da Gemini nei materiali ricevuti coincidono con i byte reali;
- l'hash falso del V3.3 **non compare** in nessun materiale disponibile, e la continuità V3.3 di Gemini riporta quello corretto;
- l'hash falso coincide con il vero esattamente su prefisso e suffisso dell'abbreviazione `6fb9d76e…7638`, che usano anche i miei documenti: quasi certamente è stato ricostruito da lì. È un difetto di processo; il rimedio è proposto nell'audit.

Diff del mandato notturno (`0396995..4eb79e0`, cartella di consegna esclusa): 10 file, 606 righe aggiunte, 27 rimosse.

**Patch consegnata** (`diff_fix_g0.patch`): `git diff main..HEAD` sull'intero repository, esclusa solo la cartella di consegna, che conterrebbe sé stessa: 13 file, 1.212 righe aggiunte, 65 rimosse. A parte la consegna, `HEAD` coincide con `4eb79e0`.

## 6. Auto-audit: limiti che restano
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
7. **Mutation testing:**
   - I mutanti li ho scelti io: 44/44 dice che la suite rileva **questi** difetti, non che il codice sia corretto.
   - I file di regole (`regole/*.toml`) e l'interfaccia a riga di comando non sono mutati.
8. **Binario B:** nessun audit sul codice di Gemini possibile finché il ramo non è pubblicato; i controlli pronti sono nel §7 dell'audit.
9. **Merge su `main`:** sospeso fino a decisione dell'utente.

## 7. Come verificare
```bash
git clone https://github.com/gioelemelis2-dot/trading-brain-core && cd trading-brain-core && git checkout feat/fix-g0-journal
```
```bash
cd brain/guardian && python3 -s -B -W error -m unittest discover -s test -v
```
```bash
cd brain/guardian/test && python3 -s -B mutazioni_g0_journal.py /tmp/mutanti_g0
```
```bash
cd brain/collaborazione/da-claude/CONSEGNA_FIX_G0 && sha256sum -c MANIFEST.sha256
```
Fasi rosse:
- `git checkout 9ff30e2`: attesi 2 fallimenti e 3 errori;
- `git checkout 2dcb9aa`: attesi 6 fallimenti e 1 errore;
- `git checkout 9170ecf`: attesi 5 fallimenti.

Primo giro di mutazioni: `git checkout 1d1c4f1`, poi lo stesso comando delle mutazioni (atteso 30/44).

Tutte le fasi sono riportate per intero in `log_test_40_e_mutazioni_24.txt`.

Verifica della migrazione: `git rev-parse main:brain` deve restituire `7422e1fc346bdcc12c2b37a184acd345db04845b`.
