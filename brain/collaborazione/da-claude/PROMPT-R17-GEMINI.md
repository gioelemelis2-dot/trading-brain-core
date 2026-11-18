# Mandato R17 per Gemini (Antigravity)

**Stato: PRONTO** (18/11/2026). Si consegna quando lo decide il titolare.

```
MANDATO R17 PER GEMINI — secondo giro per la regola d'uscita (D-24)

CONTESTO
- R16 integrato: è il PRIMO giro pulito (D-26: #112 era fuori perimetro e non conta). Contatore 1 su 2.
  R16-01 → #113 (test di K15c, corretto in 40253cc) e #114 (iteratore `anni` in criteri.verifica). R16-03 →
  #115 (tre test deboli negli strumenti di contorno, corretti in 807c978: mutanti IX19, CO12, PI26).
- #114 corretto per decisione del titolare (D-27): NUOVO CANDIDATO e476a9a. Rispetto a 303890b, nel perimetro
  cambia solo laboratorio/esecuzione/criteri.py (2 righe). Per P6, R17 rifà le prove toccate (criteri).
- Fatto anche: collaudo del metodo IA-02 secondo il protocollo DGS-07 (pilota_ia02.py, protocollo_ia02.py).
  Esito: bootstrap con margine 0,05 R, CONFERMATO NEL DOMINIO DEL PILOTA (laboratorio/studi/risultati/ia02/).
- CANDIDATO: commit e476a9a. Perimetro: laboratorio/esecuzione/, simulatori/orb_londra.py,
  dati/pipeline/dukascopy.py, dati/pipeline/calendario.py. Lavora sulla punta del ramo feat/esecutore-h002 e
  verifica con git diff e476a9a HEAD -- <perimetro> che sia vuoto. Dichiara commit, ambiente e perimetro (P6).

REGOLE: quelle di R16 (nessun dato vero, rete bloccata, worktree nuovo ../tb-r17 sulla punta del ramo,
scrivere solo in da-gemini, non modificare il codice, mai compiacente).
- NON toccare ~/Downloads/tb-riconta, brain/dati/reali/ né i processi scarica_cache (scaricamento ASK in corso).
- NOVITÀ (D-28): nei rapporti scrivi i percorsi locali con ~ (per esempio ~/Downloads/tb-r17), mai il percorso
  completo con il nome dell'utente.

COMPITI
A. Sul Mac (Apple Python 3.9): suite ufficiale completa, aggiungendo brain.laboratorio.tests.test_protocollo_ia02:
   atteso 0 errori (1 saltato per #106). Corsa COMPLETA di mutazioni_esecuzione.py: atteso 100%, salvo N63
   (equivalente su Apple Python) e PI10 (dichiarato equivalente nello script dopo #112): verificalo.
   Sonde su #114 (anni da generatore, da range, da lista: stesso esito) e su K15c (anni vuoti → messaggio).
B. Riproducibilità del collaudo IA-02 (solo dati inventati, nessuna rete):
   - decomprimi laboratorio/studi/risultati/ia02/limiti_fase2.json.gz e confronta il suo SHA-256 con quello
     registrato in laboratorio/studi/IMPEGNO-PROTOCOLLO-IA02.md §7;
   - rilancia protocollo_ia02 --fase 2 --candidato bootstrap:0.05 su quel file: stesso verdetto e stessi conteggi
     di risultati/ia02/verdetto_fase2.md;
   - rigenera con pilota_ia02 (fase 2, solo bootstrap) le prime 200 repliche delle celle 2 e 11 su Apple
     Python 3.9 e confronta i limiti con quelli archiviati: dichiara se coincidono bit per bit o no (DGS-07
     vieta di sommare repliche di Python diversi: qui è solo un controllo di riproducibilità).
C. Nono attacco, SOLO errori in buona fede (E):
   - laboratorio/studi/protocollo_ia02.py: Clopper–Pearson unilaterale (valori del DGS: 60/3.000 e 248/12.000),
     conteggi E/P/B/I con le uguaglianze alle soglie, classifica e spareggi, completezza del file, verdetto della
     fase 2, banda della diagnostica dei flussi, inventario dei semi;
   - pilota_ia02.py dopo #112: contratto dell'intervallo (non finito, invertito, ampiezza nulla = errore),
     file dei limiti (versione, ordine, null per gli errori).
   Almeno 5 sonde e 5 mutanti nuovi.
D. Tabella dei rilievi con gravità, tipo (E/M) e costo; frase finale esplicita:
   «R17: nessun difetto critico o importante che conti per D-24» oppure l'elenco.

CONSEGNA: brain/collaborazione/da-gemini/G-<data>-R17.md, commit con la tua identità, push su rev/gemini-r17.
```
