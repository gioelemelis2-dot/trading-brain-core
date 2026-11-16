# Mandato R12-bis per Gemini (Antigravity), 16/11/2026

Sostituisce `PROMPT-R12-GEMINI.md` (sospeso dopo l'incidente del 14/11, difetto #41). Da incollare in Antigravity così com'è.

```
MANDATO R12-bis PER GEMINI — terzo attacco al programma dei criteri e primo attacco ai due strumenti nuovi

CONTESTO
- Il giro R12 era stato sospeso per l'incidente del 14/11 (registro dei difetti, #41): H-002 eseguita sui dati veri
  dello sviluppo prima del sigillo, analisi esplorative, bozza dei 3 verdetti scritta dopo i numeri. Il censimento
  è chiuso (brain/collaborazione/da-gemini/G-20261115-03-censimento-esecuzioni.md): la riserva 2005–2023 risulta
  intatta. H-002 è «non decidibile · parcheggiata» per decisione dell'utente; esce dal parcheggio solo su dati
  successivi al 12/11/2026 (H-002-REVISIONI.md). La patch di tb-proposte NON si applica.
- Commit di partenza: l'ultimo di origin/feat/esecutore-h002 (032250b o successivo).

REGOLE (vincolanti; una violazione invalida il giro)
1. NESSUN DATO VERO. Non leggere, non elencare, non aprire nulla in brain/dati/reali/ (cache_dukascopy, CSV, meta,
   partizioni). Non chiamare caricatore.carica né esegui_h002 su percorsi reali, in nessuna modalità. Non usare
   Dukascopy né la rete per scaricare prezzi. Solo dati inventati (laboratorio/esecuzione/sintetico.py, genera_dati)
   in cartelle temporanee.
2. Stanotte sul Mac gira lo scaricamento storico (worktree ~/Downloads/tb-scarica, log ~/scarica_storico.log):
   NON toccare tb-scarica, la cache, il log, i processi python3 in corso.
3. Lavora in un worktree nuovo:
     cd ~/Downloads/trading-brain-core && git fetch origin feat/esecutore-h002
     git worktree add ../tb-r12bis -b rev/gemini-r12bis origin/feat/esecutore-h002
   Scrivi SOLO in brain/collaborazione/da-gemini/. Non modificare file di Claude, nemmeno sul tuo ramo.
4. Ogni commit con la TUA identità, non quella dell'utente:
     git -c user.name="Gemini (Antigravity)" -c user.email=gemini@invalid commit ...
5. Niente proposte di cambiare i criteri o i verdetti di H-002. Niente merge. Non leggere i rapporti del DGS
   (ChatGPT) su questo commit finché non hai consegnato.
6. Nel rapporto, l'ELENCO COMPLETO dei comandi eseguiti (passo, comando, esito), così si può ricontare.
7. Mai compiacente: ogni «d'accordo» con un calcolo, una prova o un controesempio.

COMPITI
A. Programma dei criteri (come R12 originale)
   1. Riesegui le sonde R7 e R11 (prove_r7_esecutore.py, prove_r11.py) sul codice attuale; adegua SOLO l'invocazione
      dove l'interfaccia è cambiata, dichiaralo, conferma che ogni difetto risulta bloccato.
   2. Riesegui la replica dei criteri (copertura ≥ 90% sui criteri 4 e 5, A23); conferma differenza 0.
   3. Terzo attacco: esiste ancora una scelta libera? Si può eseguire codice diverso da quello sigillato (moduli
      importati fuori da FILE_CODICE, configurazioni, variabili d'ambiente)? Il controllo dei feriali vuoti si aggira
      o ha falsi positivi su chiusure vere dell'oro? Il registro si manomette senza che i controlli se ne accorgano?
      Almeno 5 sonde e 5 mutanti nuovi.
B. Scaricatore solo-cache (brain/dati/pipeline/scarica_cache.py, dukascopy.richiesta_http)
   - Un file a metà o sbagliato può finire in cache? Un giorno può risultare «scaricato» senza esserlo?
   - --continua-su-http: un giorno in errore può essere scambiato per «nessun dato»? Il conteggio di fila si azzera
     quando non deve? I codici d'uscita (0, 2, 3, 4, 5) sono sempre quelli giusti?
   - Il registro CSV resta coerente dopo un'interruzione a metà?
   Solo con risposte finte (nessuna rete). Almeno 3 sonde e 3 mutanti nuovi.
C. Riconteggio (brain/governance/censimento/riconta.py)
   - Trova le forme che NON vede: strumenti con argomenti in campi diversi, esecuzioni scritte in altri modi, date in
     altri formati (03/01/2005, 2005.01.03, timestamp numerici), prezzi con virgola decimale o separatori, uscite
     annidate. Usa trascrizioni FINTE costruite da te, mai le tue trascrizioni vere.
   - Può stampare un contenuto o un prezzo che non dovrebbe?
   Almeno 3 sonde e 3 mutanti nuovi.
D. Test e mutanti (stampa l'output):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002 brain.dati.tests.test_scarica_cache brain.dati.tests.test_dukascopy brain.governance.censimento.test_riconta
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py <cartella fuori dal repository>
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella fuori dal repository> 2

CONSEGNA
brain/collaborazione/da-gemini/G-20261116-R12bis.md con: tabella dei rilievi (gravità come nel REGISTRO-DIFETTI:
critica, importante, minore), output dei comandi, elenco completo dei comandi eseguiti, e una frase finale esplicita:
«R12-bis: nessun difetto critico o importante» oppure l'elenco. Commit con la tua identità e push sul ramo
rev/gemini-r12bis. Se una regola ti impedisce un compito, fermati su quel compito e scrivilo: non aggirarla.
```
