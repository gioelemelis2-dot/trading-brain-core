# Ricevuta del percorso ordinario di verifica (#127) · DGS-15 punti 2–6 · 22/11/2026

**Solo dati e registri sintetici.** Nessun dato vero, nessuna riserva reale, rete bloccata. Etichette:
- **[ESEGUITO]**: rieseguito per questa ricevuta, con il log;
- **[EVIDENZA PRECEDENTE]**: log salvati in precedenza;
- **[PROPOSTO AL TITOLARE]**: scelte che restano sue.

## Candidato

> **Candidato finale: `aca694f`.** Comprende la seconda revisione (#137, manifesto letto una volta) e la seconda parte di #124, cioè le decisioni a filo in frazioni esatte nel modulo del verdetto.
> - **Rieseguito su `aca694f`**, in un worktree bloccato, su 3.13.18 e 3.9.25:
>   - suite complete verdi (`log/finale_suite_aca694f_*.log`);
>   - prove A–G (`log/finale_ricevuta_aca694f_*.json`): **esiti identici** a quelli di `7c90c90` e fra le due versioni. L'impronta dell'impegno ora è `6b09ce67…`, diversa perché il codice è cambiato ed è legato all'impegno. L e U differiscono ancora di 5,7e-15 R fra le versioni (pilota congelato);
>   - mutanti del verdetto 127/132 (`log/finale_mutanti_verdetto_aca694f_*.log`). VD30, VD39 e VD111 non si applicavano dopo #124 e VD44 era vivo: riallineati, con un test nuovo per VD44, in `db3c85f`; poi 4/4 uccisi su entrambe le versioni. **Totale 131/132**, VD13 equivalente;
>   - mutanti del percorso (`mutazioni_percorso.py`, 41): **40/41 su 3.13.18 e su 3.9.25**; l'unico vivo è MF09, equivalente dichiarato (`log/finale_mutanti_percorso_aca694f_*.log`);
>   - controlli aperti del punto 5, rieseguiti: **risultati identici** a quelli della prima corsa e fra le versioni (`log/finale_controlli_aperti_aca694f_*.json`).
> - **Controllo nuovo nella suite** (`test_mutanti_applicabili`, `db3c85f`): ogni mutante dei tre script deve applicarsi una volta sola. Ha trovato subito anche V07, V17 e V18 del perimetro, rotti da `riserva/2`, e li ha fatti riallineare prima della corsa completa.
>
> Le righe sotto descrivono la prima corsa (`7c90c90`), rimasta come storia.

| Elemento | Valore |
|---|---|
| Commit delle prove | `7c90c90` (ramo `feat/esecutore-h002`), eseguito in una copia bloccata sul commit (worktree separato) |
| Codice eseguibile | 31 file (chiusura degli import di `esegui_verifica`); impronta dell'insieme `175043ce…b57c` |
| Moduli nuovi o cambiati | `esecuzione/esegui_verifica.py` (nuovo), `esecuzione/manifesto.py` (nuovo), `esecuzione/riserva.py` (schema `riserva/2`), `esecuzione/caricatore.py` (byte verificati) |
| Ambienti | Python 3.13.18 e 3.9.25 |
| Log | `log/ricevuta_7c90c90_py313.json`, `log/ricevuta_7c90c90_py39.json`, rapporti in `log/rapporto_*.txt` |
| Test | `test_esegui_verifica` (10), `test_manifesto` (13), `test_riserva` (32), verdi su entrambe le versioni |

## Oggetto sintetico (punto 2)

- **Mercato sintetico** (`tests/mercato_sintetico.py`): ogni seduta di Londra ha un range d'apertura di 5 USD e una rottura al rialzo alle 08:45. Poi la giornata tocca il target («vinta», +1,42236 R) oppure lo stop («persa», −1,08054 R). Il 60% delle giornate è vinto, con il generatore casuale fissato da un seme.
- **Scheda di test conforme a H-003:** blocco `json contratto-h003` con modello, ipotesi, destinazione «test», simulatore `orb_londra`, variante V-T, m = 1, metro D-31, semi, potenza stimata, 35 giorni accessori (storia per le mediane di H-002), 1.000 sedute, veto per blocchi (−0,25 R, minimo 50 trade) e periodo di sviluppo. La scheda è sigillata con le impronte dei 31 file di codice.
- **Finestre:**
  - lettura 04/01/2010 → 31/01/2014 (prenotazione);
  - verifica 08/02/2010 → 31/01/2014, esattamente 1.000 sedute;
  - sviluppo 2024 (da un'altra cache sintetica).

## Le prove (punti 2–4)

Per ogni prova: esito atteso e osservato, registro della riserva prima e dopo (impronta del file, giorni per stato, aperture, rifiuti), chiamate al caricatore e rapporti. Tutto è nei due JSON. Qui il riassunto, **identico su 3.13 e 3.9** salvo dove indicato.

| Prova | Atteso | Osservato | Chiamate al caricatore | Date e quota consumate |
|---|---|---|---|---|
| A · corsa completa | completata, promossa | **completata, promossa**: L = +0,3086, U = +0,4612, media ≈ +0,3836565 R (esadecimale `0x1.88dd3fe19743fp-2`, DGS-17), 1.000 sedute / 1.000 trade / 1.000 attive; screening ammesso; registro delle prove: sviluppo → verifica → esito; il rapporto coincide con quello rigenerato dal record | sviluppo 1, verifica 1 | 1.489 giorni consumati (tutta la prenotazione, date accessorie comprese); j = 1; α_j = 0,025; N = 1 |
| B · vecchia scheda H-002 | rifiutata prima dell'autorizzazione | **rifiutata**: «serve un solo blocco json contratto-h003 (modello H-003)»; registro della riserva invariato (stessa impronta prima e dopo): le 1.489 date restano **prenotate**, non consumate | nessuna | nessuna |
| C · quota non collaudata (m = 2, 1,25%) | rifiuto durevole, nessuna lettura, nessun consumo | **«rifiutata per quota»**: evento `rifiuto` con j previsto 1, m 2, quota calcolata 0,0125 e fase «prima dell'autorizzazione». Riletto dal file: 0 giorni prenotati o consumati, α speso 0. La quota prevista dopo il rifiuto è ancora (1; 0,025), quindi l'indice delle aperture non è avanzato. Nessuna esecuzione nel registro delle prove: N invariato. Il secondo tentativo con la stessa prenotazione è rifiutato («serve una richiesta nuova») | nessuna, anche al primo tentativo | nessuna |
| D · concorrenza | una sola apertura alla quota | B controlla la quota (2,5%), poi, prima della sua autorizzazione, A si autorizza attraverso lo stesso ingresso (j = 1) e cade durante la lettura. Al ricontrollo sotto il blocco **B è rifiutata** (fase «ricontrollo all'autorizzazione», j previsto 2, quota calcolata 0,00833) | B: sviluppo 1, verifica 0. A: sviluppo 1, lettura interrotta alla chiamata (caduta simulata prima di leggere file) | solo le date di A (j = 1, 0,025, N = 2 perché sono sigillate due ipotesi); A resta autorizzata senza esito; nessun consumo per B |
| E · file difforme dopo l'autorizzazione | esito tecnico, consumo mantenuto | **«file difforme»**, esito «non decidibile», causa «ASK 2010-02-18: byte diversi dal manifesto autorizzato», scritta nel record e nel rapporto | sviluppo 1, verifica 1 (interrotta al file difforme) | 1.489 giorni consumati, j = 1: il consumo resta |
| F · caduta dopo il verdetto e prima del rapporto | rapporto rigenerato dal record, senza letture | Prima corsa: verdetto e record scritti, poi caduta prima del rapporto. Ripresa: **«rapporto rigenerato»**, promossa, **nessuna chiamata al caricatore**, registro della riserva invariato. Ripresa con impronte di codice diverse: **rifiutata** («ripresa non identica: scheda, codice, variante, seme o finestra diversi dal record») | prima corsa: sviluppo 1, verifica 1; ripresa: nessuna | quelle della prima corsa (j = 1) |
| G · giorno omesso nel registro dello scaricamento | rifiutata prima dell'autorizzazione | **rifiutata**: «manifesto con anomalie: omesso: XAUUSD ASK 2010-02-08». Il file c'era e aveva l'impronta giusta: mancava la riga nel registro. Registro della riserva invariato; le date restano prenotate | sviluppo 1 (screening), verifica 0 | nessuna |

**Il punto 3 nei test** (`test_manifesto`, [ESEGUITO]):
- un giorno omesso, una voce doppia, una riga dell'altro lato, un indirizzo dell'altro lato o di un altro mercato, un esito HTTP non valido: tutti emergono anche quando i file presenti hanno l'impronta giusta;
- i giorni in quarantena restano nell'elenco con il loro stato e cambiano l'impronta dell'elenco;
- il caricatore decodifica gli **stessi byte** di cui verifica l'impronta (lo prova una spia sul decodificatore). Un file sostituito, sparito o non previsto dal manifesto dà `FileDifforme`.

**Che cosa lega l'autorizzazione (l'impegno):**
- impronta della scheda;
- impronte dei 31 file di codice;
- metro (D-31, impronta del pilota, quota 0,025);
- finestra di lettura e di verifica;
- istantanea dei due registri dello scaricamento (nome e SHA-256);
- elenco ordinato [mercato, lato, giorno, stato, SHA-256] di 2.978 voci e la sua impronta;
- N globale, quota, j, variante, seme e contratto intero.

L'impronta dei dati scritta nel registro è lo SHA-256 della forma canonica dell'impegno; un impegno ritoccato dopo è rifiutato quando il registro viene ricostruito (test).

**Le due versioni di Python:**
- **uguali:** gli esiti di tutte le prove e l'impronta dell'impegno (`88069ac0…5450`);
- **diversi di circa 5,7e-15 R:** gli estremi L e U del bootstrap. La causa è il pilota congelato, che somma con `sum()` (N22-A2). Quella differenza basta a far cambiare l'impronta del registro delle prove e del file della riserva, perché i record contengono quei numeri;
- **diversi solo nell'ultima cifra:** le somme annuali descrittive di H-002;
- **identica:** la media.

Questo è il caso concreto della domanda Q1 del messaggio 14: congelare una sola versione di Python nella verifica.

## Soluzioni di registro provate e scelte di governance

- **Provato [ESEGUITO]:** schema `riserva/2` con l'evento `rifiuto` (D-50), il ricontrollo della quota sotto il blocco del file, l'impegno nell'autorizzazione e il record del verdetto nell'esito.
- **Proposto [PROPOSTO AL TITOLARE]:**
  - **dopo un rifiuto la prenotazione si chiude** e serve una prenotazione nuova (proposta (b) del messaggio 14, senza ancora un parere del DGS);
  - **DA-38:** il vecchio `esegui_h002 --modalita verifica` legge ancora la riserva senza registro. D-37 aveva lasciato quei criteri a H-002, quindi disattivarlo spetta al titolare (consiglio: disattivarlo).
- **Non esercitato nelle prove sintetiche:**
  - l'ancoraggio dei registri alla versione su GitHub (`controlla_ancora`), presente nel vecchio esecutore e non ancora nel nuovo;
  - i controlli dell'ambiente all'avvio (`avvio.py`, isolamento);
  - il lanciatore isolato per il nuovo esecutore.
  Vanno aggiunti prima di qualunque uso reale: sono nel candidato di R19.

## Punto 5 · Controlli aperti [ESEGUITO]

- **Script:** `controlli_aperti.py`, SHA-256 `e706794f…5bbc` (uguale a quello nel commit `7c90c90`).
- **Dove è girato:** worktree bloccato su `8d59885`; il modulo del verdetto è lo stesso di `36d533a`.
- **Ambienti e risultati:** 3.13.18 e 3.9.25; risultati **identici** sulle due versioni. Log: `log/controlli_aperti_8d59885_py313.json` e `..._py39.json`.

| Controllo | Esito |
|---|---|
| **D-47** | Potenza stimata 0,50: **ammessa**. Potenza 0,4999999999999999 (un ulp sotto): **non ammessa**. |
| **#123** | Lo stesso requisito «costi» fallito, sulle stesse coppie (segnale del metro favorevole). Come **descrittivo**: esito **promossa**, e il rapporto lo riporta come «requisito costi [descrittivo, non cambia l'esito]: fallito». È l'omissione informativa, ora corretta. Come **vincolante per promuovere**: esito **non decidibile**. È la parte che poteva cambiare il verdetto, classificata importante. |
| **#124** | 9 casi su 3 confronti (screening 125×0,3 + 125×0,2 contro 0,25; blocco 250×0,3 contro 0,3; blocco 125×(−0,3) + 125×(−0,2) contro −0,25), ciascuno all'uguaglianza, a +1 ulp e a −1 ulp: la decisione del modulo **coincide** con quella in frazioni esatte in tutti i 9 casi, su entrambe le versioni. |
| **D-44** | Limiti superiori esatti unilaterali al 99,9% su 12.000: **1,1897%** (107), **0,0935%** (2), **0,1088%** (3). Entrambi i conteggi avversi corretti sono sotto il 2,5%. |

**Potenza replica per replica** alla media vera +0,25 R: 1.000 sedute, un trade per seduta, veto per blocchi a −0,25 R con minimo 50 trade, N fornito. M = 2.000 repliche per scenario.

| Scenario | M | F (segnale favorevole) | P (promosse) | promosse senza segnale favorevole | invalide | inconclusive | F/M (IC 95%) | P/M (IC 95%) | (F−P)/M (IC 95%) |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| σ = 1,25 R | 2.000 | 495 | 495 | **0** | 0 | 1.505 | 24,75% (22,87–26,70) | 24,75% (22,87–26,70) | 0 (0–0,18%) |
| σ = 0,80 R | 2.000 | 1.023 | 1.023 | **0** | 0 | 977 | 51,15% (48,93–53,36) | 51,15% (48,93–53,36) | 0 (0–0,18%) |

- **Implicazione «promossa ⇒ segnale favorevole»:** controllata su ogni replica, non solo sul totale. 0 discordanze su 4.000.
- **Intervalli:** esatti (Clopper-Pearson). Le repliche invalide e inconclusive restano nel denominatore.
- **Cause fra i percorsi favorevoli:** veto 0, minimi 0, requisito 0. In questi scenari il veto non scatta mai: con media +0,25 R e 250 trade per blocco, la media di un blocco sotto −0,25 R è rarissima. Quindi la perdita di potenza dovuta ai veti **non è messa alla prova** da questi scenari. Serve uno scenario con blocchi deboli, o con meno trade, quando ci sarà una scheda candidata.
- **Confronto con DGS-14:** il riferimento normale di DGS-14 era 24,35% con σ = 1,25 R. Il valore simulato, 24,75%, cade nel suo intervallo. Con σ = 0,80 R la potenza è circa 50%, come previsto (σ ≤ 0,81 R).

## Punto 6 · Scelta futura delle date: che cosa manca

La durata è fissata: 1.000 sedute (D-37). Per preparare una riga per finestra candidata servono:
1. **il consuntivo al minuto** (`controlla_cache` e `intersezione_bid_ask` sul Mac): copertura congiunta BID/ASK per seduta e per fascia operativa, buchi per anno, giorni corti. *Manca: il titolare deve ancora mandare i 4 file di `~/Desktop/consuntivo_ask`.*
2. **i registri dello scaricamento reali** (nomi e impronte): servono per il manifesto di ogni finestra candidata. Per il BID 2005–2009, scaricato con la pipeline completa, va verificato che ogni file abbia una riga; se no, si registra («in-cache-non-registrato») prima di qualunque autorizzazione. *Da controllare sul Mac, senza aprire i file.*
3. **le regole ancora da fissare (D-38):** date esatte della riserva, embargo (proposta: 10 giorni di borsa), quarantena (proposta: oltre il 5% dei minuti mancanti su BID o ASK nella fascia operativa). *Decisioni del titolare.*
4. **la frequenza e la dispersione dei trade di una scheda candidata sullo sviluppo:** servono per la probabilità di raggiungere 300 trade e 200 sedute attive e per la potenza alla quota effettiva. Oggi non c'è nessuna candidata H-003 (DA-35, D-48): la si può stimare solo per scenari sintetici.
5. **le esposizioni pregresse** per domanda e finestra (stato «vista / esposizione incerta / mai vista», D-32), dal registro delle prove e dal quaderno delle ipotesi.

Con questi dati, ogni riga riporterà: confini e date accessorie, sedute con BID e ASK congiunti, buchi, quarantene, embargo, probabilità dei minimi, potenza alla quota effettiva e finestre contigue residue dopo il consumo. Si useranno solo metadati, lo sviluppo ammesso e scenari sintetici.

## Stato di D-49

**Nessuna protezione è attiva oggi.** Gemini ha verificato che su un repository privato personale con il piano Free non ci sono né rulesets, né protezione dei rami, né CODEOWNERS. Il titolare non ha ancora detto se il suo piano è Free o Pro. Claude scrive sul ramo con le credenziali dell'app GitHub del titolare; con una protezione attiva, gli agenti dovranno usare rami propri e credenziali senza scavalcamento.

## Che cosa resta al titolare

- La chiusura del punto 5 di D-34 (prova del percorso intero) e qualunque accesso reale alla riserva.
- DA-38 (vecchio esecutore di H-002), le date e le regole di D-38, il piano GitHub per D-49.

## Aggiornamento per DGS-16 (candidato `4659dc8`, worktree bloccato, 3.13.18 e 3.9.25)

Log: `log/dgs16_ricevuta_4659dc8_py313.json` e `..._py39.json`. File della prova A in `log/dgs16_A_*`.

**1. Provenienza nella corsa A**
- **Sigillo:** lo prepara il collaudo (`S.sigilla` nello script), con le impronte dei 31 file di codice.
- **Prenotazione:** la prepara il collaudo (`RV.prenota`), con l'impronta della scheda.
- **Potenza stimata (0,6):** è un **valore dichiarato nel contratto** della scheda di test. È un input: **non è calcolato** e non viene da una procedura congelata. Per una scheda vera, D-36 chiede la procedura congelata prima del sigillo: va aggiunta al contratto H-003.
- **Generato dall'esecutore ordinario:** screening sullo sviluppo, quota, manifesto, impegno, autorizzazione, lettura, coppie, verdetto, record e rapporto.

**2. Sedute fissate prima dell'apertura e coppie usate**
- L'impegno, scritto **prima** dell'autorizzazione, contiene l'elenco delle 1.000 sedute: il calendario di H-002, cioè i feriali senza `orb_londra.esclusi`.
- Il record contiene le coppie **[data, S, K]** nello stesso ordine, comprese le sedute senza operazioni, e i 40 feriali esclusi.
- Verificato su entrambe le versioni: le date delle coppie coincidono con quelle dell'impegno; 1.040 feriali − 40 esclusi = 1.000.
- Elenchi completi in `log/dgs16_A_sedute_e_coppie_py313.json`.
- I 40 esclusi sono festività inglesi, vigilie e 31 dicembre, per esempio 02/04/2010, 05/04/2010, 03/05/2010, 31/05/2010, 30/08/2010, 24/12/2010 …

**3. Rapporto originale, record e rapporto rigenerato** (stesso ambiente)

| | 3.13.18 | 3.9.25 |
|---|---|---|
| Rapporto originale uguale al rigenerato dal record, byte per byte | **sì** | **sì** |
| SHA-256 del rapporto originale di A | `6a80b0b93f0a…` | `ee589ad4f7ee…` |
| SHA-256 del rapporto rigenerato nella ripresa F (corsa separata, stessi ingressi) | `6a80b0b93f0a…` (uguale ad A) | `ee589ad4f7ee…` (uguale ad A) |
| Impronta dell'impegno | `e8d69883f27f…` | `e8d69883f27f…` (uguale) |

**Comandi per rigenerare** (dalla radice, sul commit `4659dc8`):
```
python3 -s -B brain/laboratorio/ricevute/2026-11-22-percorso-127/ricevuta_127.py <cartella>
python3 -c "import json,sys; sys.path.insert(0,'.'); from brain.laboratorio.esecuzione import esegui_verifica as EV; print(EV.rapporto_da_record(json.load(open('<cartella>/A_corsa_completa/record_P1.json'))), end='')"
```
Il secondo comando ristampa il rapporto dal solo record, senza leggere dati.

**4. Le due versioni di Python: verdetto e numeri separati**
- **Verdetto:** identico, promossa, con lo stesso segnale e la stessa causa.
- **Media:** identica, bit per bit: `0x1.88dd3fe19743fp-2` ≈ 0,3836565 R (il valore esatto del double è 0,3836564999999758…; DGS-17: l’uguaglianza dei bit e l’arrotondamento decimale sono confronti diversi).
- **L e U:** diversi nelle ultime cifre binarie.
  - L: `0x1.3bf9a49c2bffbp-2` (3.13) contro `0x1.3bf9a49c2c061p-2` (3.9);
  - U: `0x1.d850f9ed97262p-2` contro `0x1.d850f9ed972c8p-2`;
  - circa 102 ulp, cioè 5,7e-15 R. La causa è la somma del pilota congelato.
- **Byte dei rapporti:** diversi fra le due versioni. Il motivo sono queste cifre e le impronte dei registri che le contengono.

**5. Transizioni di B e G** (test: `test_dopo_l_anomalia_corretta_la_stessa_prenotazione_riprende`, `test_prenotazione_abbandonata_si_rilascia`)
- **G**, manifesto con anomalie: nessuna autorizzazione, prenotazione ancora aperta. Corretto il registro dello scaricamento, la **stessa** richiesta, con scheda e identità invariate, si esegue fino alla promozione.
- **B**, scheda non conforme: la prenotazione si chiude con un **rilascio registrato** (`RV.rilascia`) prima di qualunque autorizzazione, e le date tornano disponibili.
- **Rifiuto per quota:** chiude la prenotazione (D-50), come concorda il DGS (Q3).
- **Dopo l'autorizzazione:** il consumo resta anche se il processo cade (D, E).

**6. Prova logica dei veti (Q6)**, in `controlli_aperti.py`, sezione 6. Quattro blocchi da 250 sedute, rumore con seme fisso, blocco debole a −0,35 R e gli altri a +0,70 R; veto a −0,25 R con minimo di 50 trade. Il risultato atteso del veto è calcolato indipendentemente, in frazioni. Risultati su `4659dc8`:

| Caso | Segnale del metro | Veto (atteso = osservato) | Esito |
|---|---|---|---|
| Blocco debole in posizione 1, 2, 3 o 4 | favorevole | fallito | **bocciata** (veto) |
| Controllo omogeneo, stessa media | favorevole | superato | **promossa** |
| Blocco debole con 49 trade | favorevole | **non valutabile** | non decidibile |
| Blocco debole con 50 o 51 trade | favorevole | fallito | bocciata |

Un veto **non valutabile** resta distinguibile da uno valutato senza violazione.
