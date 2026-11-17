# Mandato R15 per Gemini (Antigravity)

Preparato il 17/11/2026 sera, dopo l'integrazione di R14 (#96–#104). **Pronto: la corsa dei mutanti sul candidato `8e51ce9` è chiusa** (esecuzione 213/213, simulatore 40/40, DSR 44/44, riconteggio 53/53, controllo della cache 20/20, scaricatore 50/50; 366 test verdi su Python 3.13.18 e 3.9.25 di Claude). Da incollare in Antigravity così com'è.

```
MANDATO R15 PER GEMINI — verifica di R14, taratura del banco su mercati inventati, settimo attacco

CONTESTO
- Il tuo R14 è integrato: tutti i rilievi riprodotti o verificati da Claude e corretti in TDD come #96–#104
  (brain/laboratorio/REGISTRO-DIFETTI.md; sezione R14 in brain/laboratorio/ipotesi/H-002-REVISIONI.md;
  REGISTRO-MODIFICHE v1.49). R14-02 era un difetto dei test di Claude (Python di Apple). Cambi da sapere:
  * nella radice il lanciatore ora rifiuta OGNI cartella con un nome importabile, e pretende -B;
  * versioni_nella_storia rifiuta la storia parziale e legge anche il reflog;
  * esporta_redatto accetta SOLO testo UTF-8 (tutto il resto rifiutato salvo --escludi);
  * il registro canonico è obbligatorio, quindi i tuoi script BANCO-02 e R14 vanno adattati
    (registro = brain/laboratorio/registro_prove.json).
- Decisione del titolare D-24 (brain/governance/DECISIONI.md): i due giri puliti di fila contano i rilievi
  critici o importanti di tipo (E) errore in buona fede e (M) manomissione a costo BASSO. Gli (M) a costo
  medio o alto si registrano e basta. Contatore attuale: 0 su 2. R15 può essere il primo giro pulito.
- CANDIDATO: commit 8e51ce9 (non «l'ultimo»: commit successivi di soli documenti non cambiano il candidato;
  se Claude cambia codice, lo dichiara e il giro si riferisce comunque a 8e51ce9).
- PERIMETRO del candidato (il codice che il sigillo protegge): brain/laboratorio/esecuzione/ (avvio, esegui_h002,
  sigillo, caricatore, criteri, riserva, sintetico), brain/laboratorio/simulatori/orb_londra.py,
  brain/dati/pipeline/dukascopy.py e calendario.py. Strumenti di contorno, valutati ma fuori dal sigillo:
  scarica_cache, controlla_cache, taratura_completezza, riconta, esporta_redatto, potenza_soglia.
- AMBIENTE (parere P6 del DGS, regola per contare i giri): dichiara nel rapporto commit esatto (git rev-parse
  HEAD), python3 --version, sys.version, platform.platform(), sys.flags e sys.pycache_prefix con e senza -I.
  Claude ha verificato su Linux con Python 3.13.18 e 3.9.25; tu verifichi sul Mac con l'Apple Python 3.9.

REGOLE (una violazione invalida il giro)
1. NESSUN DATO VERO: niente brain/dati/reali/, niente caricatore.carica o esegui_h002 su percorsi reali,
   niente rete (HTTPS_PROXY=http://127.0.0.1:9 in ogni comando, con la prova che è attivo). Solo dati inventati
   in cartelle temporanee.
2. Non toccare ~/Downloads/tb-riconta (da lì girano gli scaricamenti BID e ASK), ~/scarica_storico.log,
   ~/scarica_ask.log, i processi attivi, né gli altri worktree.
3. Worktree nuovo:
     cd ~/Downloads/trading-brain-core && git fetch origin feat/esecutore-h002
     git worktree add ../tb-r15 -b rev/gemini-r15 8e51ce9
   Prima dei test: find brain -name __pycache__ -prune -exec rm -rf {} +
   File d'attacco SOLO in copie dentro cartelle temporanee. Scrivi SOLO in brain/collaborazione/da-gemini/.
   Commit con la tua identità: git -c user.name="Gemini (Antigravity)" -c user.email=gemini@invalid commit ...
4. Non modificare il codice del laboratorio né proporre modifiche a criteri o verdetti di H-002: si misura,
   non si cambia. Elenco completo dei comandi nel rapporto. Mai compiacente: ogni «chiuso» con una prova.

COMPITI
A. Verifica di R14 (#96–#104), rilievo per rilievo (chiuso / chiuso in parte / aperto, con la prova):
   rilancia le tue sonde S1–S6 e i tuoi script BANCO-02, adattati al registro canonico; ognuno deve stampare
   «ATTACCO RESPINTO». I 4 mutanti che erano vivi sono negli script ufficiali come N68, N69 e X25–X27
   (gli ultimi tre fatti a mano da Claude, vedi REGISTRO-DIFETTI #103): verifica che muoiano.
B. TARATURA DEL BANCO SU MERCATI INVENTATI (compito nuovo e più importante: errori di tipo E). Domanda:
   il banco promuove una strategia che non vale niente, e riconosce una che funziona? Usa solo funzioni del
   repository (brain/laboratorio/esecuzione/sintetico.py: mercato, scrivi_cache; esegui_h002.esegui_sviluppo)
   in cartelle temporanee, senza modificare il codice:
   B1. NULLO: almeno 20 mercati inventati senza vantaggio (semi diversi, deriva e spinta nulle) sul periodo
       dello sviluppo; quante volte lo screening promuove V-T o V-S? Atteso: raramente. Riporta il numero
       e l'intervallo di confidenza.
   B2. VANTAGGIO PIANTATO: mercati inventati con una spinta dopo la rottura del range di Londra (parametro
       `spinta` di sintetico.mercato) a 2–3 intensità; quante volte lo screening promuove? Riporta la potenza
       per intensità.
   B3. Se B1 promuove spesso o B2 quasi mai, è un rilievo (E): descrivi dove si perde il segnale (costi,
       veto, robustezza, confronto casuale) SENZA proporre soglie nuove.
   Limita il tempo: se 20 semi richiedono troppo, dichiara quanti ne hai fatti e perché.
C. Settimo attacco, con priorità agli errori in buona fede (E): calcoli di criteri.py (DSR, percentili,
   copertura, ultimi 5 anni), caricatore (BID/ASK disallineati, giorni corti, ora legale), costi del
   simulatore orb_londra (spread, commissione, slippage). Almeno 5 sonde e 5 mutanti nuovi.
D. Test e mutanti ufficiali (stampa l'output; rete bloccata; sul tuo Python 3.9 di Apple):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002 brain.laboratorio.tests.test_riserva brain.laboratorio.tests.test_potenza_soglia brain.laboratorio.tests.test_taratura_completezza brain.dati.tests.test_scarica_cache brain.dati.tests.test_dukascopy brain.dati.tests.test_controlla_cache brain.governance.censimento.test_riconta brain.governance.test_esporta_redatto
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_controlla_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/governance/censimento/mutazioni_riconta.py <cartella fuori dal repository> 2

CLASSIFICAZIONE DI OGNI RILIEVO (D-24)
Colonne obbligatorie: gravità (critica/importante/minore), tipo (E oppure M), costo per l'attaccante
(basso/medio/alto). Nei casi dubbi scrivi «dubbio» e il motivo: decide il titolare.

CONSEGNA
brain/collaborazione/da-gemini/G-<data>-R15.md: tabella dei rilievi, esito di A rilievo per rilievo, risultati
di B (numeri, intervalli, semi usati, tempo impiegato), C e D con gli output, elenco completo dei comandi, e
la frase finale esplicita: «R15: nessun difetto critico o importante che conti per D-24» oppure l'elenco.
Commit con la tua identità e push su rev/gemini-r15. Se una regola ti impedisce un compito, fermati su
quel compito e scrivilo.
```
