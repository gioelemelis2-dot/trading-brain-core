# Bozza del mandato R16 per Gemini (Antigravity)

**Stato: BOZZA** (17/11/2026 pomeriggio). Da completare dopo le decisioni del titolare:
1. se R15 conta come primo giro pulito (casi «dubbio» #106 e #108);
2. se applicare prima i minori #107, #110 e #111 (`collaborazione/da-claude/PROPOSTA-MINORI-R15.md`).

Due varianti del candidato:
- **Variante A (minori non applicati):** codice del perimetro identico a `8e51ce9`, con i test corretti per #106 (commit `db81dbb` o successivo, dichiarato da Claude).
- **Variante B (minori applicati):** nuovo commit dichiarato da Claude. Per il parere P6 del DGS, R16 rifà sul candidato nuovo le prove toccate (criteri, decodifica).

```
MANDATO R16 PER GEMINI — secondo giro per la regola d'uscita (D-24)

CONTESTO
- R15 integrato (#106–#111). #106 (test del -B sul Python di Apple) corretto nei test: il caso si salta,
  dichiarandolo, dove -I implica -B. #108 è misurabile: il rendiconto dell'intersezione conta gli estremi
  incrociati. [VARIANTE A: minori #107, #109–#111 non applicati, registrati] [VARIANTE B: #107, #110, #111
  corretti nel commit <...>]
- CANDIDATO: commit <...>. Perimetro come in R15. Dichiara commit, ambiente e perimetro (P6).

REGOLE: quelle di R15 (nessun dato vero, rete bloccata, worktree nuovo ../tb-r16 sul candidato, scrivere solo
in da-gemini, non modificare il codice, mai compiacente).

COMPITI
A. Sul Mac (Apple Python 3.9): suite ufficiale completa CON i nuovi moduli di test
   (aggiungere brain.laboratorio.tests.test_intersezione_bid_ask e brain.laboratorio.tests.test_collaudo_ia02):
   atteso 0 errori. Corsa COMPLETA di mutazioni_esecuzione.py: atteso 100%, salvo N63, che sul Python di
   Apple è equivalente (lì -B non può mancare): dichiaralo.
   [VARIANTE B] Rifai le sonde C1, C2 e S5 di R15 sul candidato nuovo: devono dare errore pulito o valore corretto.
B. Taratura estesa: ripeti B1 (NULLO) con 100 semi (1..100) per stringere l'intervallo (oggi 0–16%). Ripeti
   B2 a spinta 0,005 e 0,01 con 50 semi. Stessi parametri di R15, stessi tempi dichiarati.
C. Ottavo attacco, SOLO errori in buona fede (E): strumenti di contorno nuovi:
   - laboratorio/studi/intersezione_bid_ask.py: conteggi giusti su casi limite (ora legale, vigilie,
     file vuoti da un lato, minuti fuori sessione), nessun prezzo nell'uscita né nel JSON;
   - laboratorio/studi/collaudo_ia02.py: riferimenti analitici (F di AR(1), Clopper–Pearson), generatore
     stazionario, quantile del bootstrap.
   Almeno 5 sonde e 5 mutanti nuovi.
D. Tabella dei rilievi con gravità, tipo (E/M) e costo; frase finale esplicita:
   «R16: nessun difetto critico o importante che conti per D-24» oppure l'elenco.

CONSEGNA: brain/collaborazione/da-gemini/G-<data>-R16.md, commit con la tua identità, push su rev/gemini-r16.
```
