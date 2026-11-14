# Giro di revisione R11 · H-002 dopo le correzioni R10 (15/11/2026)

**Oggetto:** ramo `feat/esecutore-h002` (NON unito a main), commit indicato nel messaggio dell'utente. Contiene:
- simulatore corretto (D1, D2) e test strutturali;
- programma dei criteri corretto (P1–P8 di Gemini);
- proposta v3.2 con A1–A21;
- registro dei difetti.

**Regola d'uscita per il sigillo** (proposta v3.2, §C): servono **due giri di fila** senza difetti critici o importanti. R11 è il primo giro dopo le correzioni.

---

## 1. Gemini (Antigravity)

```
MANDATO R11 PER GEMINI — verifica delle correzioni e secondo attacco al programma dei criteri di H-002

Contesto: ho integrato la tua revisione R7 (sezione R10 di brain/laboratorio/ipotesi/H-002-REVISIONI.md).
Correzioni in TDD sul ramo feat/esecutore-h002 (rosso 6a29aa2, poi verde): P1–P8 accolti tutti, i tuoi
mutanti MG01, MG03, MG04, MG06, MG07 sono nello script e muoiono. Registro dei difetti aggiornato
(brain/laboratorio/REGISTRO-DIFETTI.md: i tuoi rilievi sono #23–#31).

REGOLE: ramo tuo rev/gemini-r11 da feat/esecutore-h002; scrivi SOLO in brain/collaborazione/da-gemini/; niente
dati reali, niente Dukascopy, niente sigillo, niente merge. Mai compiacente: ogni «d'accordo» con un calcolo o
una prova.

COMPITI
1. Riesegui le tue sonde (prove_r7_esecutore.py) sul nuovo codice: P1–P7 devono risultare bloccate. Se una
   non lo è, è un difetto.
2. Riesegui la tua replica dei criteri (replica_criteri_h002.py). Nota: il confronto casuale ora usa l'R della
   strategia sugli STESSI giorni del casuale (A2 in via prudenziale), e la verifica passa tutti gli anni del
   periodo (A3). Adegua la replica SOLO su questi due punti, dichiarandolo, e conferma differenza 0.
3. Secondo attacco: cerca difetti NUOVI, soprattutto nei collegamenti fra sigillo, registro, sviluppo, verifica
   e riga di comando (dove stavano i 5 difetti critici del primo giro). Almeno 5 sonde nuove e 5 mutanti nuovi,
   con l'esito.
4. Test e mutanti, su Python 3.9 (e 3.13 se riesci a installarlo):
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py <cartella fuori dal repository>
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
5. Posizione su A12–A21 della proposta v3.2 (A1–A11 li hai già dati), con il motivo.

CONSEGNA: da-gemini/G-20261115-R11.md con la tabella dei rilievi (gravità come nel REGISTRO-DIFETTI:
critica / importante / minore), l'output dei comandi e una frase finale esplicita: «R11: nessun difetto critico o
importante» oppure l'elenco. Commit e push sul tuo ramo.
```

---

## 2. ChatGPT

Da incollare insieme all'archivio `revisione_h002_r11.zip`.

```
Sei di nuovo il revisore esterno di H-002: rigido, scrupolosissimo, mai compiacente. Nel giro precedente
(revisione incrociata) hai dato «NON SIGILLABILE» con i rilievi F-01…F-10, ma avevi lo stato PRIMA dell'ultimo
lavoro. Ti allego revisione_h002_r11.zip: copia esatta (git archive) del ramo con tutto il lavoro (cartella
brain/), più LEGGIMI-REVISIONE.md con i comandi.

Da leggere per primi:
- brain/laboratorio/ipotesi/H-002-REVISIONI.md: sezione R9 (risposta punto per punto ai tuoi F-01…F-10) e R10
  (difetti trovati da Gemini nel programma dei criteri e corretti);
- brain/laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md: decisioni A1–A21 (A15–A18 nascono dai tuoi rilievi), 16 casi
  d'oro, regola d'uscita per il sigillo;
- brain/laboratorio/REGISTRO-DIFETTI.md: tutti i 32 difetti trovati finora, con gravità e lettura;
- codice: brain/laboratorio/simulatori/orb_londra.py e brain/laboratorio/esecuzione/; test in brain/laboratorio/tests/.

Fai una DOPPIA revisione. Il giudizio deve venire solo da cose che hai eseguito o calcolato tu.

REVISIONE 1 — ESECUZIONE
1. Scompatta in una tua cartella (es. ./lavoro; NON /tmp/mutanti_h002).
2. python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
3. Mutanti, anche a blocchi (riporta l'output di ogni blocco):
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py ./lavoro/mo
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 S,C
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 K
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 E,M
4. Ricalcola a mano almeno 3 casi d'oro (proposta v3.2, §B) e confrontali con i test.
Se un passo non si può eseguire, scrivi quale e perché. Non attribuire esiti che non hai visto.

REVISIONE 2 — LETTURA CRITICA E ATTACCO
1. Per ognuno dei tuoi F-01…F-10: la risposta in R9 lo chiude, lo chiude in parte o no? Con il motivo.
2. Per ognuna delle decisioni A1–A21: d'accordo con la proposta, oppure proposta diversa con il motivo. Su A15
   (buchi nei minuti) e A17 (spread di riferimento) sii particolarmente severo.
3. Il programma dei criteri ha avuto 5 difetti critici al primo giro, tutti nei collegamenti fra sigillo,
   registro, sviluppo, verifica e riga di comando. Attacca soprattutto lì: falsi positivi, accessi al periodo
   sigillato, doppia verifica, N e V del DSR sbagliati.
4. Scrivi almeno 5 test tuoi che provano a far sbagliare il codice, eseguili, riporta l'esito.
5. Proponi almeno 5 mutanti che gli script non hanno e di' se i test li uccidono.
6. La regola d'uscita per il sigillo (proposta v3.2, §C) è sufficiente? Cosa manca?

CONSEGNA, in italiano:
- tabella dei rilievi: ID, gravità (critica / importante / minore, come nel REGISTRO-DIFETTI), file, riga, prova;
- output dei comandi; i tuoi test e mutanti con l'esito;
- posizione su F-01…F-10 e su A1–A21;
- giudizio finale, scegliendo UNA formula:
  «nessun difetto critico o importante: sigillabile dopo le decisioni A1–A21» /
  «sigillabile dopo le decisioni e queste correzioni: …» /
  «non sigillabile, perché: …».
Ricorda: il sigillo fissa le regole PRIMA di guardare i risultati; la verifica storica viene dopo e richiede gli ASK
storici. Non confondere i due traguardi.
```
