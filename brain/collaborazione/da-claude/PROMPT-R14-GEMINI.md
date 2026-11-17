# Mandato R14 per Gemini (Antigravity)

> **BLOCCATO il 17/11 alle 9:30:** la revisione del laboratorio ha trovato tre difetti critici aperti (#86–#88). Non consegnare finché non sono corretti; il mandato andrà riscritto per verificarli.

Preparato la notte del 16–17/11/2026, aggiornato il 17/11 mattina (#72–#85). **Da consegnare solo quando Claude lo conferma** (dopo l'integrazione della revisione del laboratorio, ancora in corso): R14 deve girare su codice fermo. Da incollare in Antigravity così com'è.

```
MANDATO R14 PER GEMINI — verifica delle correzioni R13 e quinto attacco

CONTESTO
- Ho integrato il tuo R13 (sezione R13 di brain/laboratorio/ipotesi/H-002-REVISIONI.md; difetti #61–#71 nel
  REGISTRO-DIFETTI). Nota: sulla tua controprova di B-04 avevi RAGIONE tu e il mio rigetto era sbagliato (#67):
  ora solo un giorno con dati azzera il conteggio degli errori di fila.
- Correzioni in TDD più una revisione notturna con revisori separati (#72–#85); i commit sono nel
  REGISTRO-MODIFICHE (v1.40–v1.46). #72 è un errore di Claude: il pacchetto per il DGS conteneva il nome
  dell'utente dentro uno ZIP annidato.
- Commit di partenza: l'ultimo di origin/feat/esecutore-h002 al momento della consegna. Dichiaralo.

REGOLE (le stesse di R13; una violazione invalida il giro)
1. NESSUN DATO VERO: niente brain/dati/reali/, niente caricatore.carica o esegui_h002 su percorsi reali,
   niente rete (HTTPS_PROXY=http://127.0.0.1:9 in ogni comando, con la prova che è attivo). Solo dati inventati
   in cartelle temporanee.
2. Non toccare ~/Downloads/tb-scarica, ~/scarica_storico.log, i processi attivi, né il tuo worktree tb-banco.
3. Worktree nuovo:
     cd ~/Downloads/trading-brain-core && git fetch origin feat/esecutore-h002
     git worktree add ../tb-r14 -b rev/gemini-r14 origin/feat/esecutore-h002
   Scrivi SOLO in brain/collaborazione/da-gemini/. Commit con la tua identità:
   git -c user.name="Gemini (Antigravity)" -c user.email=gemini@invalid commit ...
4. Niente proposte su criteri o verdetti di H-002. Non leggere i rapporti del DGS su questo commit prima di
   consegnare. Elenco completo dei comandi nel rapporto. Mai compiacente: ogni «chiuso» con una prova mostrata.

COMPITI
A. Verifica delle correzioni R13, rilievo per rilievo (chiuso / chiuso in parte / aperto, con la prova):
   - #61: controlla_ambiente (modalità isolata -I -S, origine dei moduli caricati, impronta del file DAVVERO
     caricato). Attacca ancora: c'è un modo di eseguire codice non sigillato che il controllo non vede?
   - #62 e #64: ancora a GitHub (sigillo.ancora_git, riserva.controlla_ancora): HEAD su un ramo, discendenza
     dalla versione remota, file identico alla HEAD, niente collegamenti simbolici. Attacca: riferimento remoto
     locale riscritto a mano (.git/refs/remotes), repository annidati, worktree, filtri di git.
   - #63: completezza per terzi della sessione (QUOTA_TERZO) e vigilie. Attacca: distribuzioni di minuti che
     passano senza poter generare trade; ora legale (marzo/ottobre); giorni con sessione di Londra vera corta.
   - #65: valori della riserva (m, N globale, impronta, ripetizione dopo l'esito, quarantena su protetta).
   - #66: gli script di mutanti bloccano la rete da soli e segnalano il tempo scaduto come «da guardare».
   - #67: 404 e vuoti non azzerano più il conteggio; riprova la tua controprova dei fine settimana.
   - #69: prove di robustezza dichiarate al sigillo.
   - #71: i 6 mutanti che erano vivi (N06, N07, N15, N24, N26, P12) ora muoiono? Rilanciali.
   - #72–#85 (revisione notturna): per ognuno, la correzione chiude davvero lo scenario del registro? In
     particolare #75/#78/#80/#81 (riconteggio: comandi su più righe, date compatte attaccate a lettere,
     uscite con soli prezzi sotto 1.900 — euristica con un limite dichiarato —, toolUseResult), #83
     (decompressione limitata: stessa semantica di lzma.decompress?) e #85 (minuti distinti).
B. Quinto attacco, su ciò che NON hai ancora attaccato:
   - brain/governance/esporta_redatto.py (pacchetto per i revisori), dopo #72 e #84: riesci ancora a far
     passare un dato personale (codifiche non coperte, archivi senza firma nota, testo dentro PDF o immagini,
     nomi di file, sostituzioni che si sovrappongono)? Usa SOLO dati personali INVENTATI (es. «Mario
     Rossi»), mai quelli veri.
   - riconta.py: un'uscita con dati della riserva che passa ancora senza segnalazione (timestamp attaccati a
     lettere: noto e non corretto; altri formati?).
   - il log dei nuovi tentativi dello scaricatore (dukascopy.richiesta_http con annota): può mentire o
     perdere tentativi?
   - moduli_brain / impronte_codice: chiusura degli import ancora aggirabile (import dentro stringhe eseguite,
     __init__ con logica, plugin per estensione)?
   Almeno 5 sonde e 5 mutanti nuovi.
C. Test e mutanti ufficiali (stampa l'output; tutti con la rete bloccata):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002 brain.laboratorio.tests.test_riserva brain.laboratorio.tests.test_potenza_soglia brain.dati.tests.test_scarica_cache brain.dati.tests.test_dukascopy brain.dati.tests.test_controlla_cache brain.governance.censimento.test_riconta brain.governance.test_esporta_redatto
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/governance/censimento/mutazioni_riconta.py <cartella fuori dal repository> 2

CONSEGNA
brain/collaborazione/da-gemini/G-<data>-R14.md: tabella dei rilievi (critica/importante/minore), esito di A
rilievo per rilievo con le prove, output dei comandi, elenco completo dei comandi eseguiti, e la frase finale
esplicita: «R14: nessun difetto critico o importante» oppure l'elenco. Commit con la tua identità e push su
rev/gemini-r14. Se una regola ti impedisce un compito, fermati su quel compito e scrivilo.
```
