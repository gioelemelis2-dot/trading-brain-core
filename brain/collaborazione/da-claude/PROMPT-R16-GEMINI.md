# Bozza del mandato R16 per Gemini (Antigravity)

**Stato: PRONTO, variante B** (17/11/2026 sera). Scelte fatte da Claude su delega del titolare («fai quello che ritieni più utile»), reversibili:
1. **R15 NON conta come primo giro pulito.** È la lettura stretta di D-24: #106 era un mio errore in un test, e dichiararlo innocuo andrebbe a mio vantaggio. Quindi R16 può essere al massimo il primo giro pulito.
2. **Minori #107, #110 e #111 applicati** in `303890b` (variante B). Per il parere P6 del DGS, R16 rifà sul candidato nuovo le prove toccate (criteri, decodifica).

Si consegna a Gemini quando il titolare lo decide. I commit dopo `303890b` toccano solo strumenti di contorno (`laboratorio/studi/`), test, script dei mutanti e documenti: il perimetro resta quello di `303890b`.

```
MANDATO R16 PER GEMINI — secondo giro per la regola d'uscita (D-24)

CONTESTO
- R15 integrato (#106–#111). #106 (test del -B sul Python di Apple) corretto nei test: il caso si salta,
  dichiarandolo, dove -I implica -B. #108 è misurabile: il rendiconto dell'intersezione conta gli estremi
  incrociati. #107, #110, #111 corretti nel commit 303890b (#109 resta registrato: scelta di metodo).
- R15 NON conta come primo giro pulito (scelta stretta, dichiarata). R16 può essere il primo.
- CANDIDATO: commit 303890b (perimetro: laboratorio/esecuzione/, simulatori/orb_londra.py,
  dati/pipeline/dukascopy.py, dati/pipeline/calendario.py). Lavora sulla punta del ramo feat/esecutore-h002 e
  verifica con git diff 303890b HEAD -- <perimetro> che il perimetro sia identico. Dichiara commit, ambiente e
  perimetro (P6).

REGOLE: quelle di R15 (nessun dato vero, rete bloccata, worktree nuovo ../tb-r16 sul candidato, scrivere solo
in da-gemini, non modificare il codice, mai compiacente).

COMPITI
A. Sul Mac (Apple Python 3.9): suite ufficiale completa CON i nuovi moduli di test
   (aggiungere brain.laboratorio.tests.test_intersezione_bid_ask, brain.laboratorio.tests.test_collaudo_ia02 e
   brain.laboratorio.tests.test_pilota_ia02):
   atteso 0 errori. Corsa COMPLETA di mutazioni_esecuzione.py: atteso 100%, salvo N63, che sul Python di
   Apple è equivalente (lì -B non può mancare): dichiaralo.
   Rifai le sonde C1, C2 e S5 di R15 sul candidato nuovo: devono dare errore pulito o valore corretto.
B. Taratura estesa: ripeti B1 (NULLO) con 100 semi (1..100) per stringere l'intervallo (oggi 0–16%). Ripeti
   B2 a spinta 0,005 e 0,01 con 50 semi. Stessi parametri di R15, stessi tempi dichiarati.
C. Ottavo attacco, SOLO errori in buona fede (E): strumenti di contorno nuovi:
   - laboratorio/studi/intersezione_bid_ask.py: conteggi giusti su casi limite (ora legale, vigilie,
     file vuoti da un lato, minuti fuori sessione), nessun prezzo nell'uscita né nel JSON;
   - laboratorio/studi/collaudo_ia02.py: riferimenti analitici (F di AR(1), Clopper–Pearson), generatore
     stazionario, quantile del bootstrap;
   - laboratorio/studi/pilota_ia02.py (disegno del DGS a 12 celle): generatori delle celle (stazionarietà,
     conteggi, perdite rare), HAC (pesi, ritardi, K medio), bootstrap circolare basic (ranghi, ΣK = 0),
     semi SHA-256 (indipendenza dei componenti), classificazione e copertura.
   Almeno 5 sonde e 5 mutanti nuovi.
D. Tabella dei rilievi con gravità, tipo (E/M) e costo; frase finale esplicita:
   «R16: nessun difetto critico o importante che conti per D-24» oppure l'elenco.

CONSEGNA: brain/collaborazione/da-gemini/G-<data>-R16.md, commit con la tua identità, push su rev/gemini-r16.
```
