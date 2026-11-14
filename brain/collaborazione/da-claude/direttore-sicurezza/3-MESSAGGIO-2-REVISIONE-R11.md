# Messaggio 2 per ChatGPT: revisione tecnica R11 di H-002

Da incollare **dopo** la risposta al messaggio 1, nella stessa chat. Non servono allegati nuovi: il codice è nell'archivio `trading_brain_completo.zip` (commit indicato nel MANIFEST).

```
Secondo compito da DGS: la revisione tecnica R11 di H-002, la prima strategia. Usa l'archivio che hai già.
Hai già dato un «NON SIGILLABILE» (rilievi F-01…F-10), ma sullo stato precedente.

Da leggere per primi:
- brain/laboratorio/ipotesi/H-002-REVISIONI.md: sezioni R9 (risposta ai tuoi F-01…F-10) e R10 (8 difetti trovati da Gemini nel programma dei criteri, corretti);
- brain/laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md: decisioni A1–A21, 16 casi d'oro, regola d'uscita per il sigillo;
- brain/laboratorio/REGISTRO-DIFETTI.md;
- codice: brain/laboratorio/simulatori/orb_londra.py e brain/laboratorio/esecuzione/; test in brain/laboratorio/tests/.

DOPPIA REVISIONE. Il giudizio deve venire solo da cose eseguite o calcolate da te.

REVISIONE 1 — ESECUZIONE (dalla cartella che contiene brain/; usa una tua cartella di lavoro, non /tmp/mutanti_h002)
1. python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   (attesi 119 test verdi)
2. Mutanti, anche a blocchi; riporta l'output di ogni blocco:
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py ./lavoro/mo                       (atteso 40/40)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 S,C          (atteso 19/19)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 K            (atteso 28/28)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 E,M          (atteso 23/23)
3. Ricalcola a mano almeno 3 casi d'oro della proposta v3.2 (§B) e confrontali con i test.
Se un passo non si può eseguire, scrivi quale e perché. Non attribuire esiti che non hai visto.

REVISIONE 2 — LETTURA CRITICA E ATTACCO
1. F-01…F-10: la risposta in R9 li chiude, li chiude in parte o no? Con il motivo.
2. A1–A21: d'accordo con la proposta, oppure proposta diversa con il motivo. Sii particolarmente severo su A15 (buchi nei minuti) e A17 (spread di riferimento).
3. Il programma dei criteri ha avuto 5 difetti critici al primo giro, tutti nei collegamenti fra sigillo, registro, sviluppo, verifica e riga di comando. Attacca soprattutto lì: falsi positivi, accessi al periodo sigillato, doppia verifica, N e V del DSR.
4. Almeno 5 test tuoi che provano a far sbagliare il codice: eseguili e riporta l'esito.
5. Almeno 5 mutanti che gli script non hanno: di' se i test li uccidono.
6. La regola d'uscita per il sigillo (proposta v3.2, §C) è sufficiente? Cosa manca?

CONSEGNA: documento «DGS-20261115-02-revisione-R11», con:
- la tabella dei rilievi (gravità critica / importante / minore, file, riga, prova);
- l'output dei comandi;
- i tuoi test e mutanti con l'esito;
- la posizione su F-01…F-10 e su A1–A21;
- l'autocritica;
- UNA di queste formule finali:
  «nessun difetto critico o importante: sigillabile dopo le decisioni A1–A21» /
  «sigillabile dopo le decisioni e queste correzioni: …» /
  «non sigillabile, perché: …».
Il sigillo fissa le regole PRIMA dei risultati; la verifica storica viene dopo e richiede gli ASK storici. Non confondere i due traguardi.
```
