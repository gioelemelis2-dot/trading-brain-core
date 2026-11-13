# Richieste di revisione R7: programma dei criteri e sigillo di H-002 (15/11/2026)

**Oggetto:** ramo `feat/esecutore-h002` (NON unito a main), cartella `brain/laboratorio/esecuzione/`.
**Pacchetto eseguibile** per i revisori senza accesso al repository: `revisione_esecutore_h002.zip`, preparato da Claude e consegnato dall'utente.

Testi pronti da incollare, uno per revisore.

---

## 1. Gemini (Antigravity): replica indipendente e revisione

```
MANDATO PER GEMINI (Antigravity) — R7: replica indipendente e revisione del programma dei criteri di H-002

Contesto: Claude ha scritto sul ramo feat/esecutore-h002 il programma che applica i §6–§8 della scheda
brain/laboratorio/ipotesi/H-002-ORB-v3.md (v3.1) e lo strumento di sigillo. Codice in brain/laboratorio/esecuzione/,
test in brain/laboratorio/tests/test_esecuzione.py e test_esegui_h002.py, mutanti in mutazioni_esecuzione.py.
Ambiguità della scheda trovate da Claude: sezione «Programma dei criteri e sigillo» di H-002-REVISIONI.md (A1–A11).

REGOLE
- Lavora su un ramo tuo: rev/gemini-esecutore-h002, partendo da feat/esecutore-h002. Scrivi SOLO in
  brain/collaborazione/da-gemini/. Non modificare file di Claude.
- Niente dati reali, niente richieste a Dukascopy, niente sigillo, niente merge su main.
- Sii critico e mai compiacente. Se sei d'accordo su un punto, dimostralo con un calcolo o un test, non con una frase.

COMPITO A — REPLICA INDIPENDENTE (prima di leggere esecuzione/criteri.py ed esecuzione/esegui_h002.py)
1. Leggi SOLO la scheda v3.1 (§6–§8) e il simulatore già revisionato (simulatori/orb_londra.py).
2. Scrivi in un file tuo (da-gemini/replica_criteri_h002.py) il TUO programma dello screening: confronto casuale
   (1.000 ripetizioni, seme fisso, 95° percentile), benchmark sui giorni comuni, scenario di stress (+0,20),
   robustezza sempre eseguita (range 20 e 45 minuti; target 1,2 e 2,0 solo V-T; tetto 1,6 e 2,5) con il veto,
   verdetto sui 9 criteri.
3. Fallo girare sui tre mercati inventati di esecuzione/sintetico.py (è solo un generatore di dati: puoi usarlo):
   SN.mercato(date(2024,1,1), 800, seme=3, sd=0.7) — casuale; con spinta=0.01 — vantaggio noto; con deriva=0.01 —
   sola tendenza.
4. Confronta con i numeri di Claude (esegui E.esegui_sviluppo sugli stessi mercati DOPO aver scritto il tuo):
   per ogni mercato e variante n, R medio, Sharpe, drawdown, R delle vendite, benchmark, stress, robustezza, verdetto.
   Tolleranza: identici per i valori deterministici; per il 95° percentile casuale ±0,01 (dipende dal generatore
   casuale). Ogni differenza va spiegata: errore tuo, errore di Claude o ambiguità della scheda.

COMPITO B — REVISIONE DEL RAMO
1. Fai girare i test su Python 3.13 e 3.9 e il mutation testing:
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
2. Cerca soprattutto:
   - strade per cui il programma promuove una strategia che non dovrebbe (falsi positivi);
   - strade per leggere il periodo sigillato (prima del 15/11/2023) senza sigillo, o per rifare la verifica;
   - differenze fra codice e scheda v3.1;
   - mutanti mancanti: proponi almeno 5 mutanti nuovi e di' se i test li uccidono.
3. Prendi posizione su ogni ambiguità A1–A11, con il motivo.

CONSEGNA: da-gemini/G-20261115-R7-esecutore-h002.md con le tabelle della replica, i rilievi (gravità, file, riga,
prova riproducibile) e la posizione su A1–A11. Commit e push sul tuo ramo; l'utente lo porterà a Claude.
```

---

## 2. DeepSeek: revisione del codice e delle ambiguità

```
Sei un revisore esterno, rigoroso e scettico, di un progetto di ricerca quantitativa (nessun denaro reale).
Ti allego: la scheda della strategia H-002 v3.1 (H-002-ORB-v3.md), il registro delle revisioni (H-002-REVISIONI.md,
leggi la sezione «Programma dei criteri e sigillo» con le ambiguità A1–A11), e il codice nuovo:
sigillo.py, criteri.py, caricatore.py, esegui_h002.py, sintetico.py, con i test test_esecuzione.py e
test_esegui_h002.py.

Cosa fa il codice: applica i criteri scritti prima della scheda (§6–§8) ai risultati del simulatore già revisionato;
gestisce il registro delle prove e il sigillo (impronta SHA-256 della scheda, N per il DSR, verifica una volta sola);
carica i dati BID/ASK rifiutando il periodo sigillato in sviluppo.

Fai DUE passate e tienile separate.
PASSATA 1 — conformità: per ogni criterio dei §6–§8 indica la funzione e le righe che lo applicano e se coincidono
alla lettera con la scheda. Ogni scostamento: gravità (bloccante / importante / minore), riga, esempio numerico.
PASSATA 2 — attacco: cerca come il programma potrebbe
  a) promuovere una strategia senza vantaggio (falso positivo);
  b) bocciare una strategia buona per un errore (falso negativo);
  c) permettere di guardare il periodo sigillato o di ripetere la verifica;
  d) dare un DSR sbagliato (controlla V, asimmetria, curtosi, N).
Per ogni punto: scenario concreto, righe di codice, test che lo dimostrerebbe.

Poi prendi posizione su ciascuna ambiguità A1–A11 (d'accordo con la proposta di Claude / proposta diversa, motivo).

Regole: non dire «sembra corretto» senza aver ricostruito il calcolo; se non puoi eseguire il codice dillo, e
calcola a mano almeno: il percentile a rango più vicino di 1.000 medie, il veto con la base a 0,10 e una prova a
0,05, il DSR di test_criteri_di_verifica. Rispondi in italiano, con tabelle.
```

---

## 3. ChatGPT: doppia revisione con il pacchetto eseguibile

```
Sei un revisore esterno, rigido e scrupolosissimo, di un progetto di ricerca quantitativa (solo demo, nessun denaro
reale). Ti allego revisione_esecutore_h002.zip: una copia eseguibile del codice (cartella brain/) con la scheda
della strategia H-002 v3.1, il registro delle revisioni e il programma nuovo dei criteri in
brain/laboratorio/esecuzione/. Le istruzioni sono in LEGGIMI-REVISIONE.md dentro l'archivio.

Devi fare una DOPPIA revisione, e il giudizio finale deve venire SOLO da prove che hai eseguito o calcolato.

REVISIONE 1 — ESECUZIONE (riproduci, non fidarti)
1. Scompatta in una cartella tua (NON /tmp/mutanti_h002: l'altra volta ha dato errore di permessi; usa ./lavoro).
2. Esegui con Python 3:
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   Attesi: 49 test verdi in circa 35 secondi.
3. Mutation testing (56 mutanti). Se hai poco tempo, a blocchi per prefisso:
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/mut 2 S,C
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/mut 2 K
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/mut 2 E
   Atteso: tutti uccisi. Riporta l'output testuale.
4. Riproduci la tabella dei tre mercati inventati (sezione «Programma dei criteri e sigillo» di H-002-REVISIONI.md).
Se un passo non si può eseguire, scrivi quale e perché; non attribuire esiti che non hai visto.

REVISIONE 2 — LETTURA CRITICA E ATTACCO
1. Confronta il codice con i §6–§8 della scheda, criterio per criterio.
2. Scrivi tu almeno 5 test nuovi che provano a far sbagliare il programma: falsi positivi, falsi negativi,
   accessi al periodo sigillato, doppia verifica, DSR. Eseguili e riporta l'esito.
3. Proponi almeno 5 mutanti che lo script non ha e di' se i test esistenti li uccidono.
4. Prendi posizione sulle ambiguità A1–A11.

CONSEGNA in italiano: tabella dei rilievi (gravità, file, riga, prova), output dei comandi, test e mutanti nuovi
con l'esito, posizione su A1–A11, e un giudizio finale: «pronto per il sigillo» / «pronto con correzioni» /
«non pronto», con il motivo.
```
