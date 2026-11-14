# Prompt per ChatGPT · secondo giro sul lavoro completo di H-002 (R9-bis, 15/11/2026)

Da incollare insieme all'archivio `revisione_h002_completa.zip`.

```
Sei di nuovo il revisore esterno di H-002: rigido, scrupolosissimo, mai compiacente. Nel giro precedente
(revisione incrociata) hai dato «NON SIGILLABILE» con i rilievi F-01…F-10. Hai visto però lo stato PRIMA
dell'ultimo lavoro. Ora ti allego revisione_h002_completa.zip: copia esatta (git archive) del ramo con
TUTTO il lavoro (cartella brain/), più LEGGIMI-REVISIONE.md con i comandi.

File da leggere per primi:
- brain/laboratorio/ipotesi/H-002-REVISIONI.md, sezione R9: la risposta punto per punto ai tuoi F-01…F-10;
- brain/laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md: decisioni A1–A18 (A15–A18 nascono dai tuoi rilievi),
  16 casi d'oro, regola d'uscita per il sigillo;
- brain/laboratorio/REGISTRO-DIFETTI.md: tutti i difetti trovati finora;
- codice: brain/laboratorio/simulatori/orb_londra.py e brain/laboratorio/esecuzione/ (programma dei criteri,
  sigillo, caricatore); test in brain/laboratorio/tests/.

Fai una DOPPIA revisione. Il giudizio deve venire solo da cose che hai eseguito o calcolato tu.

REVISIONE 1 — ESECUZIONE
1. Scompatta in una tua cartella (es. ./lavoro; NON /tmp/mutanti_h002).
2. Test:
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
3. Mutanti, anche a blocchi se hai poco tempo (riporta l'output testuale di ogni blocco):
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py ./lavoro/mo
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 S,C
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 K
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 E
4. Ricalcola a mano almeno 3 casi d'oro della proposta v3.2 (§B) e confrontali con i test.
Se un passo non si può eseguire, scrivi quale e perché. Non attribuire esiti che non hai visto.

REVISIONE 2 — LETTURA CRITICA E ATTACCO
1. Per ognuno dei tuoi F-01…F-10: la risposta in R9 lo chiude, lo chiude in parte o no? Con il motivo.
2. Per ognuna delle decisioni A1–A18: d'accordo con la proposta di Claude, oppure proposta diversa con il motivo.
   Su A15 (buchi nei minuti) e A17 (spread di riferimento) sii particolarmente severo: sono nate da te.
3. Programma dei criteri (esecuzione/criteri.py, esegui_h002.py): controlla, criterio per criterio, che
   applichi i §6–§8 della scheda v3.1. Cerca falsi positivi, falsi negativi, accessi al periodo sigillato
   senza sigillo, doppia verifica, errori nel DSR (V, asimmetria, curtosi, N).
4. Scrivi almeno 5 test tuoi che provano a far sbagliare il codice, eseguili, riporta l'esito.
5. Proponi almeno 5 mutanti che gli script non hanno e di' se i test li uccidono.
6. La regola d'uscita per il sigillo (proposta v3.2, §C) è sufficiente? Cosa manca?

CONSEGNA, in italiano:
- tabella dei rilievi: ID, gravità (critica / importante / minore, come nel REGISTRO-DIFETTI), file, riga, prova;
- output dei comandi; i tuoi test e mutanti con l'esito;
- posizione su F-01…F-10 e su A1–A18;
- giudizio finale, scegliendo UNA formula:
  «sigillabile dopo le decisioni A1–A18 come proposte» /
  «sigillabile dopo le decisioni e queste correzioni: …» /
  «non sigillabile, perché: …».
Ricorda: il sigillo fissa le regole PRIMA di guardare i risultati; la verifica storica viene dopo e richiede
gli ASK storici. Non confondere i due traguardi.
```
