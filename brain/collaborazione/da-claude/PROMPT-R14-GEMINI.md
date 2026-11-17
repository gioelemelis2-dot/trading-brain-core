# Mandato R14 per Gemini (Antigravity)

Riscritto il 17/11/2026 pomeriggio, dopo la correzione dei difetti #72–#94. **Da consegnare solo quando Claude lo conferma**: dopo la corsa completa dei mutanti sul codice finale e, se c'è, dopo il rapporto BANCO-02. Da incollare in Antigravity così com'è.

```
MANDATO R14 PER GEMINI — verifica delle correzioni #61–#94 e sesto attacco

CONTESTO
- Dopo il tuo R13 ci sono stati due giri di revisione con revisori separati di Claude (16–17/11): dati e
  governance (#72–#84) e nucleo del laboratorio (#85–#94, tre CRITICI: #86 verifica ripetibile con un altro
  registro o un altro ramo; #87 bytecode preparato in __pycache__; #88 sysconfig falso). Tutti in
  brain/laboratorio/REGISTRO-DIFETTI.md; commit nel REGISTRO-MODIFICHE v1.46–v1.47.
- Errori di Claude registrati: #72 (fuga di un nome in un pacchetto per il DGS), #85 incompleta (→ #89).
- Restano dichiarati e NON correggibili nel codice: #90 in parte e #92 (i registri sono file locali: chi ha i
  file li può scrivere a mano; la difesa è la storia su GitHub). #94 b è una decisione del titolare (DA-31).
- Se hai consegnato BANCO-02: rilancia i tuoi script; ognuno deve stampare «ATTACCO RESPINTO».
- Commit di partenza: l'ultimo di origin/feat/esecutore-h002 al momento della consegna. Dichiaralo.

REGOLE (una violazione invalida il giro)
1. NESSUN DATO VERO: niente brain/dati/reali/, niente caricatore.carica o esegui_h002 su percorsi reali,
   niente rete (HTTPS_PROXY=http://127.0.0.1:9 in ogni comando, con la prova che è attivo). Solo dati inventati
   in cartelle temporanee.
2. Non toccare ~/Downloads/tb-riconta (da lì girano gli scaricamenti BID e ASK), ~/scarica_storico.log,
   ~/scarica_ask.log, i processi attivi, né altri worktree.
3. Worktree nuovo:
     cd ~/Downloads/trading-brain-core && git fetch origin feat/esecutore-h002
     git worktree add ../tb-r14 -b rev/gemini-r14 origin/feat/esecutore-h002
   I file d'attacco (.pyc, sysconfig.py, registri falsi) SOLO in copie dentro cartelle temporanee.
   Scrivi SOLO in brain/collaborazione/da-gemini/. Commit con la tua identità:
   git -c user.name="Gemini (Antigravity)" -c user.email=gemini@invalid commit ...
4. Niente proposte su criteri o verdetti di H-002. Elenco completo dei comandi nel rapporto. Mai compiacente:
   ogni «chiuso» con una prova mostrata.

COMPITI
A. Verifica, rilievo per rilievo (chiuso / chiuso in parte / aperto, con la prova):
   - #86: verifica ripetuta con un secondo registro, con un ramo nuovo da un commit precedente, con N più
     basso. Attacca: riferimenti remoti riscritti a mano, etichette, reflog, storia «potata».
   - #87, #88: codice non sigillato eseguito (bytecode, cartella esterna del bytecode, sysconfig, moduli
     caricati prima del controllo, file .pth, zip importati, estensioni compilate nella cartella di lancio).
   - #89: file al minuto con secondi non allineati o ripetuti.
   - #90, #91: esiti multipli o senza verifica; esito scritto prima del controllo finale.
   - #93, #94 a/c/d/e: testa della riserva, contatore j, verifiche tutte o nessuna, fuso orario, dominio.
   - #72–#84: riconteggio (comandi su più righe, date compatte, uscite con soli prezzi, toolUseResult) ed
     esportazione redatta (codifiche, archivi, percorsi nei binari). Usa SOLO dati personali INVENTATI.
B. Sesto attacco: una via nuova per (1) rifare la verifica, (2) eseguire codice non sigillato, (3) abbassare N,
   (4) far passare un dato personale nel pacchetto. Almeno 5 sonde e 5 mutanti nuovi.
C. Test e mutanti ufficiali (stampa l'output; tutti con la rete bloccata):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002 brain.laboratorio.tests.test_riserva brain.laboratorio.tests.test_potenza_soglia brain.laboratorio.tests.test_taratura_completezza brain.dati.tests.test_scarica_cache brain.dati.tests.test_dukascopy brain.dati.tests.test_controlla_cache brain.governance.censimento.test_riconta brain.governance.test_esporta_redatto
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_scarica_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/dati/tests/mutazioni_controlla_cache.py <cartella fuori dal repository> 2
   python3 -s -B brain/governance/censimento/mutazioni_riconta.py <cartella fuori dal repository> 2
   Nota: con #87 i test si fermano se in brain ci sono cartelle __pycache__ (create senza -B): cancellale prima.

CONSEGNA
brain/collaborazione/da-gemini/G-<data>-R14.md: tabella dei rilievi (critica/importante/minore), esito di A
rilievo per rilievo con le prove, output dei comandi, elenco completo dei comandi eseguiti, e la frase finale
esplicita: «R14: nessun difetto critico o importante» oppure l'elenco. Commit con la tua identità e push su
rev/gemini-r14. Se una regola ti impedisce un compito, fermati su quel compito e scrivilo.
```
