# Mandato R13 per Gemini (Antigravity), 16/11/2026

Da incollare in Antigravity così com'è.

```
MANDATO R13 PER GEMINI — verifica delle correzioni R12-bis e primo attacco a riserva e potenza

CONTESTO
- Ho integrato il tuo R12-bis (brain/laboratorio/ipotesi/H-002-REVISIONI.md, sezione R12-bis; difetti #48–#59 in
  brain/laboratorio/REGISTRO-DIFETTI.md). Tutte le tue sonde sono state riprodotte con la rete bloccata: risultati
  identici. B-04 è respinto con motivo (leggilo e, se non sei d'accordo, controbatti con una prova).
- Correzioni in TDD: scaricatore b0525a9, riconteggio b8c211e, programma dei criteri 774573d; registri af2914d.
- Trovato anche da me: #59, due mutanti con sintassi rotta contati come uccisi (R06 e W08). Ora gli script
  segnalano «NON VALIDO».
- Commit di partenza: l'ultimo di origin/feat/esecutore-h002 (af2914d o successivo).

REGOLE (le stesse di R12-bis; una violazione invalida il giro)
1. NESSUN DATO VERO: niente in brain/dati/reali/, niente caricatore.carica o esegui_h002 su percorsi reali,
   niente Dukascopy né rete. Solo dati inventati in cartelle temporanee.
2. Sul Mac può girare lo scaricamento storico (~/Downloads/tb-scarica, ~/scarica_storico.log): non toccarlo.
3. Worktree nuovo:
     cd ~/Downloads/trading-brain-core && git fetch origin feat/esecutore-h002
     git worktree add ../tb-r13 -b rev/gemini-r13 origin/feat/esecutore-h002
   Scrivi SOLO in brain/collaborazione/da-gemini/. Non modificare file di Claude.
4. Commit con la tua identità: git -c user.name="Gemini (Antigravity)" -c user.email=gemini@invalid commit ...
5. Per ogni sonda che tocca dukascopy.richiesta_http: ora `attesa` e `apri` si risolvono alla chiamata, quindi
   basta sostituire urllib.request.urlopen e time.sleep nel modulo. Prima di ogni sonda controlla di non poter
   uscire in rete (per esempio HTTPS_PROXY=http://127.0.0.1:9).
6. Niente proposte su criteri o verdetti di H-002. Non leggere i rapporti del DGS su questo commit prima di
   consegnare. Elenco completo dei comandi eseguiti nel rapporto. Mai compiacente.

COMPITI
A. Verifica delle correzioni: rilancia le TUE sonde R12-bis (A3, B, C) sul codice nuovo e dimmi, una per una,
   se il difetto è chiuso, chiuso in parte o ancora aperto. Rilancia MC05 (deve morire).
B. Attacco alle correzioni nuove:
   - #48 impronte dalla chiusura degli import (esegui_h002.moduli_brain): import dinamici (importlib,
     __import__, exec), pacchetti senza __init__.py, file .pth, sitecustomize, variabili d'ambiente (PYTHONPATH):
     si può eseguire codice non coperto dalle impronte?
   - #49 completezza: la soglia di metà sessione si aggira? Ha falsi positivi su giornate vere (mezze giornate,
     cambio dell'ora legale, minuti senza scambi)?
   - #50 calendario: festività mancanti o tollerate per errore, 2005–2023.
   - #51 aggancio a git (sigillo.controlla_ancora): si manomette il registro senza che se ne accorga?
     (collegamenti simbolici, commit riscritti, file non ancora committato, HEAD staccata, registro in un altro ramo)
C. Primo attacco a due moduli mai rivisti:
   - brain/laboratorio/esecuzione/riserva.py (registro della riserva, richiesta 3 del DGS-04): due autorizzazioni
     sullo stesso perimetro, j o quota falsificati, ripetizione tecnica abusata, parte protetta aggirata,
     manomissione del file che la ricostruzione non vede, concorrenza fra processi (non solo thread).
   - brain/laboratorio/studi/potenza_soglia.py e il documento studi/risultati/potenza_IA-02.md: le formule e le
     conclusioni sono giuste? Rifai i numeri in modo indipendente (anche con una simulazione tua).
   Almeno 5 sonde e 5 mutanti nuovi per ciascuno dei due.
D. Test e mutanti (stampa l'output; tutti con la rete bloccata):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002 brain.laboratorio.tests.test_riserva brain.laboratorio.tests.test_potenza_soglia brain.dati.tests.test_scarica_cache brain.dati.tests.test_dukascopy brain.dati.tests.test_controlla_cache brain.governance.censimento.test_riconta
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/governance/censimento/mutazioni_riconta.py <cartella fuori dal repository> 2

CONSEGNA
brain/collaborazione/da-gemini/G-20261116-R13.md: tabella dei rilievi (critica, importante, minore), esito di A
rilievo per rilievo, output dei comandi, elenco completo dei comandi eseguiti, frase finale esplicita:
«R13: nessun difetto critico o importante» oppure l'elenco. Commit con la tua identità e push su rev/gemini-r13.
Se una regola ti impedisce un compito, fermati su quel compito e scrivilo.
```
