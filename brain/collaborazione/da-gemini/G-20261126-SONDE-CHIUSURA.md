# Sonde indipendenti di chiusura per i rilievi aperti di R19 (`#143`–`#149`) e serie `#124` (`D1`–`D6`)

- **Autore**: Gemini (Antigravity)
- **Data**: 2026-11-26
- **Mandato**: Sonde di chiusura per i rilievi aperti di R19 (`D-56`, `DGS-20`) — preparazione indipendente per il giro sul candidato congelato (non è un giro di revisione e non dà credito al contatore `D-24`)
- **Commit esaminato**: `7f35740975f9823d3082c2785299eaabea2918c2` (`7f35740`, ramo `feat/esecutore-h002`)
- **Worktree e ramo di consegna**: `~/Downloads/tb-sonde`, ramo `rev/gemini-sonde-chiusura`
- **Ambiente**: Apple Python `3.9.6`, `macOS-14.8.9-arm64-arm-64bit`
- **Indipendenza e vincoli**: nessuna correzione successiva a `7f35740` è stata letta; solo dati sintetici in copie temporanee rimosse a fine sonda; rete bloccata (`HTTPS_PROXY=http://127.0.0.1:9 HTTP_PROXY=http://127.0.0.1:9`); nessuna cartella protetta toccata; 1 solo processo; `df -h ~` = `8.7 GiB` liberi prima e dopo (soglia di arresto `3 GB`); nessun percorso utente nei file consegnati (`D-28`).
- **File consegnati**:
  - Script delle sonde: `brain/collaborazione/da-gemini/r20_sonde_chiusura.py`
  - Output integrale JSONL su `7f35740` (26 righe JSON): `brain/collaborazione/da-gemini/r20_sonde_chiusura_7f35740.jsonl`
  - Questo rapporto: `brain/collaborazione/da-gemini/G-20261126-SONDE-CHIUSURA.md`

---

## 1. Struttura e criteri delle sonde (`r20_sonde_chiusura.py`)

In conformità al mandato e alle osservazioni di `VERIFICA-R19.md`:
1. **Stato effettivo, nessuna scritta fissa**: ogni sonda costruisce il caso in una cartella temporanea isolata, legge lo stato reale (`rc` / eccezione, `esito_tecnico`, `esito`, eventi e contatori di `registro_riserva.json`, voci di `registro_prove.json`, chiamate a `caricatore.carica` per modalità, file creati o temporanei orfani, file spia per l'import pre-controllo) ed emette su `stdout` una sola riga JSON con le cinque chiavi `{"sonda", "rilievo", "atteso_dopo_la_correzione", "osservato", "difetto_presente"}`.
2. **Condizioni separate (`DGS-20`)**:
   - in `S-148` (`#148`), `--rapporto` puntato a una cartella esistente è provato con `--ora` valida (`2026-11-22T12:00:00Z`);
   - in `S-146c` (`#146c`), `--ora` invalida (`NON-UNA-DATA`) è provata con `--rapporto` file regolare valido;
   - in `S-147a` e `S-147b` (`#147`), provenienza URL e formato `sha256` sono provati con `--rapporto` file regolare valido e `--ora` valida;
   - la cache sintetica valida riempie con sedute neutre complete anche i feriali inglesi in `orb_londra.esclusi` fuori da `calendario.chiusure_note`, così `feriali_vuoti` e `feriali_incompleti` sono vuoti nel caso pulito indipendentemente dal calendario usato dal controllo.
3. **Riesecuzione sul candidato congelato**: lo script accetta l'opzione `--esigi-zero-difetti`, che restituisce codice d'uscita `0` se e solo se tutti i 26 valori `"difetto_presente"` sono `false` (`1` altrimenti):
   ```bash
   HTTPS_PROXY=http://127.0.0.1:9 HTTP_PROXY=http://127.0.0.1:9 \
     python3 -u -s -B brain/collaborazione/da-gemini/r20_sonde_chiusura.py --esigi-zero-difetti
   ```

---

## 2. Esito su `7f35740` — Parte I: Rilievi aperti (`#143`–`#149`, 12 sonde)

Su `7f35740` **tutte e 12 le sonde dei rilievi aperti risultano `"difetto_presente": true`**, come atteso.

| Sonda | Rilievo | Caso provato (isolato) | Stato effettivo osservato su `7f35740` | `difetto_presente` |
|---|---|---|---|---|
| `S-143` | `#143` (`R19-02`) | (a) Doppio `--scheda` (`esca_H002` + `H-T143`) con `esegui_verifica.py` manomesso; (b) singolo `--scheda` il cui sigillo omette `esegui_verifica.py`; (c) `--scheda=<file>` su codice integro | (a) `codice_manomesso_importato=true`; (b) `codice_manomesso_importato=true`; (c) `rc=2` con falso `['manca --scheda']` | **`true`** |
| `S-144` | `#144` (`R19-03`) | (a) 20 sedute feriali vuote (`vuoto-200` coerente col CSV); (b) 5 sedute feriali incomplete (1 solo minuto alle `08:00` Londra, `dati` coerente col CSV) | (a) `esito="promossa"`, `trade=980`, `20` coppie `(0, 0)` sui giorni vuoti, `1489` gg consumati; (b) `esito="promossa"`, `trade=995`, `5` coppie `(0, 0)` sugli incompleti | **`true`** |
| `S-145` | `#145` (`R19-04`) | Ramo git divergente `ramo_b` con stesso `j=1` dopo che `H-R145 V-T` è già verificata su `principale`: (a) `alfa_tot=0.75, m=5`; (b) `alfa_tot=0.05, m=1` (D-38) | (a) seconda verifica completata `esito="promossa"`, letture `1/1`, `2` eventi aggiunti; (b) non solleva `ValueError` sulla storia di `registro_prove`, scrive `1` evento `rifiuto` al passo 5 | **`true`** |
| `S-146a` | `#146a` (`R19-06a`) | Stesso mercato sintetico a doppio confine orario (`07:00` e `08:00` UTC d'estate) con `Europe/London` vs `O.LONDRA = timezone.utc` vs `TZ=America/New_York` | Con `timezone.utc`: stessa `finestra`, stesse `1000` sedute, **stessa `impronta_impegno`** (`8b9edc36...`), `1489` gg consumati, ma **esito invertito da `"promossa"` (`+0.5363 R`) a `"bocciata"` (`-0.2796 R`)** | **`true`** |
| `S-146b` | `#146b` (`R19-06b`) | (a) Modulo estraneo caricato in `sys.modules` durante la lettura di verifica (prima dell'esito); (b) modulo estraneo in `sys.modules` alla ripresa (`CONTROLLO_AMBIENTE=True`) | (a) completa `esito="promossa"` e scrive l'esito in entrambi i registri; (b) rigenera il rapporto (`rapporto rigenerato`) senza fermarsi | **`true`** |
| `S-146c` | `#146c` (`R19-06c`) | `--ora "NON-UNA-DATA"` con `--rapporto` file regolare valido | `eccezione=null`, `esito="promossa"`, `1489` gg consumati, `3` voci scritte nel registro delle prove | **`true`** |
| `S-146d` | `#146d` (`R19-06d`) | `veto_blocchi.soglia` pari a `-Infinity`, `+Infinity`, `NaN` nel contratto H-003 | Tutte e tre accettate da `leggi_contratto`; su `-Infinity`, `esegui` legge `sviluppo` (`1`) e scrive `1` voce in `registro_prove` prima di fallire per JSON non conforme | **`true`** |
| `S-146e` | `#146e` (`R19-06e`) | Campo `"ipotesi"` uguale a `""` e a `"   "` nel contratto H-003 | Entrambe accettate da `leggi_contratto` (`eccezione=null`) | **`true`** |
| `S-147a` | `#147a` (`R19-07a`) | CSV con (a) dominio falso `evil.invalid` e (b) dominio Dukascopy vero ma data di un altro anno (`2019-05-06` su `2010-02-08`), con `--rapporto` regolare | In entrambi `anomalie_manifesto=[]`, `esito="promossa"`, `1489` gg di riserva consumati | **`true`** |
| `S-147b` | `#147b` (`R19-07b`) | Riga `esito="dati"` con (a) `sha256=""` e (b) `sha256="ZZZ_NON_ESADECIMALE"`, con `--rapporto` regolare | In entrambi `anomalie_manifesto=[]`, autorizza e brucia `1489` gg di riserva prima di `esito_tecnico="file difforme"` | **`true`** |
| `S-148` | `#148` (`R19-08`) | `--rapporto` puntato a una cartella esistente, con `--ora` valida (`2026-11-22T12:00:00Z`) | Consuma `1489` gg di riserva, scrive apertura ed `esito="promossa"` nei due registri, poi solleva `IsADirectoryError` lasciando `.destinazione_e_cartella.*` orfano | **`true`** |
| `S-149` | `#149` (`R19-09`) | `RV.quota(0.15, 2, 1)` ed esecuzione su riserva `alfa_tot=0.15` a `j=2, m=1` | `quota_015_2_1 = 0.024999999999999998` (`!= 0.025`), `esito_tecnico="rifiutata per quota"` durevole | **`true`** |

### Nota di merito su `#146a` (`DGS-20`, giudizio aperto sull'impatto del fuso)

`VERIFICA-R19.md` lasciava aperto il giudizio su `#146a` (*«impatto incerto: da misurare»*) e `REQUISITI-ULTIMO-LOTTO.md` (requisito 15) chiedeva di confrontare sullo stesso caso sintetico, con un confine di seduta e di ora legale, **date, sedute, impegno ed esito**. La sonda `S-146a` misura direttamente i tre regimi:
- **Variabile d'ambiente locale `TZ=America/New_York`** (con `ZoneInfo("Europe/London")` integro): nessun effetto (`impronta_impegno`, `1000` trade, media `+0.5363 R` ed esito `"promossa"` identici al riferimento).
- **Dati del fuso `Europe/London` privi di ora legale europea (`O.LONDRA = timezone.utc`)**: nei ~7 mesi estivi (fine marzo – fine ottobre) l'apertura letta slitta dalle `07:00 UTC` alle `08:00 UTC`. Poiché `impronta_impegno` non copre `tzdata` del sistema, **la finestra (`2010-01-04 → 2014-01-31`), il numero di sedute (`1000`), il numero di trade (`1000`) e l'`impronta_impegno` (`8b9edc3675aaaa5a18e01a5936f4795f18d35421fae12357f05552957a71757d`) restano identici**, ma il verdetto passa da **`"promossa"` (`+0.5363 R`)** a **`"bocciata"` (`-0.2796 R`)** consumando i `1489` giorni della riserva.
- **Conclusione empirica**: il controllo `controlla_fuso()` contro la regola europea dell'ora legale (`#94d`) è necessario prima dell'autorizzazione.

---

## 3. Esito su `7f35740` — Parte II: Percorsi validi (`V-143`–`V-149`, 7 sonde)

Tutte e 7 le sonde del percorso valido risultano **`"difetto_presente": false`** su `7f35740` e dovranno restare `false` dopo il lotto.

| Sonda | Rilievo coperto | Percorso valido verificato | Stato osservato su `7f35740` | `difetto_presente` |
|---|---|---|---|---|
| `V-143` | `#143` | Corsa completa dal lanciatore `avvio.py verifica` con `--scheda <file>` nella forma normale (`ANCORA_GIT=True`, `CONTROLLO_AMBIENTE=True`) | `rc=0`, `completata / promossa`, letture `1/1`, `ruoli=['sviluppo','verifica','esito']`, rapporto creato | **`false`** |
| `V-144` | `#144` | Finestra con tutti i feriali completi e ~25% di sedute neutre senza segnali (`K=0` legittimo: `244` sedute neutre, `756` trade su `1000` sedute) | `completata / promossa`, `sedute=1000`, `trade=756` | **`false`** |
| `V-145` | `#145` | Una sola verifica sul ramo `principale` (`alfa_tot=0.05`, `j=1`), commit/push e successiva ripresa identica dal lanciatore | Prima corsa `rc=0, promossa`; ripresa `rc=0, rapporto rigenerato` con `0` letture, `1` sola apertura | **`false`** |
| `V-146` | `#146` | Ambiente isolato pulito, fuso `Europe/London` regolare, `--ora` ISO-8601 UTC valida, contratto con `ipotesi` valida e `soglia=-0.25` finita (verifica + ripresa dal lanciatore) | `verifica_rc=0` (`promossa`), `ripresa_rc=0` (`rapporto rigenerato`) | **`false`** |
| `V-147` | `#147` | Manifesto con URL Dukascopy canonici (`DK.url_giorno`) e `sha256` esadecimali di 64 cifre (`2978` voci) + corsa completa | `anomalie_manifesto=[]`, `completata / promossa` | **`false`** |
| `V-148` | `#148` | `--rapporto` file regolare in sottocartella nuova, poi rigenerazione atomica su file esistente | `promossa` poi `rapporto rigenerato`, testo identico a `rapporto_da_record`, `0` file temporanei orfani | **`false`** |
| `V-149` | `#149` | Quota esatta `D-38` (`alfa_tot=0.05, j=1, m=1` → `0.025`) | `quota_005_1_1=0.025`, `completata / promossa`, `aperture=[("P1", 1, 0.025, "promossa")]`, `rifiuti=[]` | **`false`** |

---

## 4. Esito su `7f35740` — Parte III: Serie completa `#124` (`D1`–`D6`, incluse `D4` e `D5`)

Tutte e 7 le sonde `#124` (comprese `D4` e `D5`, che mancavano nello script di R19) risultano **`"difetto_presente": false`** su `7f35740`.

| Sonda | Caso `#124` | Stato osservato su `7f35740` | `difetto_presente` |
|---|---|---|---|
| `S-124-D1` | `screening()` `k=300`, somma esatta `75 + 2^-48 > 75` | `ammessa=true`, `cause=[]`, `media=0.25` | **`false`** |
| `S-124-D2` | `veto_blocchi()` `k=250`, somma esatta `-62.5 - 2^-49 < -62.5` | `esito="fallito"` | **`false`** |
| `S-124-D3` | `veto_blocchi()` serie costante `[(x,1)]*k` uguale alla soglia (`k=3, x=-0.4` + scansione di tutti i 242 casi con `fsum/k < x`) | `k3_x_meno_04_esito="superato"`, `falsi_veti_nella_scansione=0` | **`false`** |
| `S-124-D4` | **(Aggiunta)** `verdetto()` media descrittiva su `k=1000` (`250 + 2^-46` e `250 + 2^-42`), `k=3` (`-0.4`) e `k=300` (`0.1, 0.2, 0.45`) contro `float(somma_Fraction / trade)` | `divergenze=0` (`uguale=true` in tutti e 4 i casi) | **`false`** |
| `S-124-D5` | **(Aggiunta)** Bordi `±1e-9`: `L_vicino_a_zero` su `±1e-9` (`false`), `nextafter(±1e-9, 0)` (`true` + clausola `#124` nel rapporto), `0` trade (`false`), intervallo invalido (`false`); `vicini(lo, hi)` su `0.20±1e-9` e `0.10±1e-9` | Tutti i bordi e le clausole coincidono col riferimento esatto | **`false`** |
| `S-124-D6a` | `controlla_coppie([(1.5e308, 1), (-1.5e308, 1), (1.5e308, 1)])` | `ValueError: la somma dei risultati non è un numero finito` | **`false`** |
| `S-124-D6b` | `controlla_coppie([(1.5e308, 1), (1.5e308, 1), (-1.5e308, 1)])` | `ValueError: la somma dei risultati non è un numero finito` | **`false`** |
