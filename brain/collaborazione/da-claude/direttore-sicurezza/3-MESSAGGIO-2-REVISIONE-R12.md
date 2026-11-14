# Messaggio 2 per ChatGPT: revisione tecnica R12 di H-002

Da incollare **dopo** la risposta al messaggio 1, nella stessa chat, **allegando l'archivio nuovo `trading_brain_r12.zip`**. Il codice è cambiato dopo il secondo attacco di Gemini (R11): l'archivio del messaggio 1 è superato per la parte tecnica.

```
Secondo compito da DGS: la revisione tecnica di H-002, la prima strategia, sul codice NUOVO.
Ti allego trading_brain_r12.zip: stessa struttura del primo archivio (con MANIFEST.tsv e commit in testa), aggiornato
dopo il secondo attacco di Gemini. Controlla prima il MANIFEST e dimmi cosa è cambiato rispetto all'archivio del
messaggio 1 (file aggiunti, tolti, modificati).

Hai già dato un «NON SIGILLABILE» (F-01…F-10) sullo stato vecchio. Da allora Gemini ha fatto due attacchi (R10: 8
difetti; R11: 8 difetti), tutti corretti, e Claude ha cambiato approccio: la riga di comando non lascia scelte libere
(periodi, ripetizioni e seme sono costanti del codice) e il sigillo registra l'impronta del codice che esegue la scheda.

Da leggere per primi:
- brain/laboratorio/ipotesi/H-002-REVISIONI.md: sezioni R9 (risposta ai tuoi F-01…F-10), R10 e R11 (difetti trovati
  da Gemini e correzioni);
- brain/laboratorio/ipotesi/H-002-v3.2-PROPOSTA.md: decisioni A1–A25, 16 casi d'oro, regola d'uscita per il sigillo;
- brain/laboratorio/REGISTRO-DIFETTI.md (40 difetti);
- codice: brain/laboratorio/simulatori/orb_londra.py e brain/laboratorio/esecuzione/; test in brain/laboratorio/tests/;
  rapporti di Gemini in brain/collaborazione/da-gemini/ (anche R11).

DOPPIA REVISIONE. Il giudizio deve venire solo da cose eseguite o calcolate da te.

REVISIONE 1 — ESECUZIONE (dalla cartella che contiene brain/; usa una tua cartella di lavoro)
1. python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   (attesi 138 test verdi)
2. Mutanti, anche a blocchi; riporta l'output di ogni blocco:
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py ./lavoro/mo                       (atteso 40/40)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 S,C          (atteso 19/19)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 K            (atteso 28/28)
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py ./lavoro/me 2 E,M,R        (atteso 42/42)
3. Ricalcola a mano almeno 3 casi d'oro della proposta v3.2 (§B) e confrontali con i test.
4. Riesegui le sonde di Gemini (brain/collaborazione/da-gemini/prove_r7_esecutore.py e prove_r11.py): i difetti che
   dimostravano devono risultare bloccati. Se una sonda non gira più perché l'interfaccia è cambiata, dillo e
   riproduci il caso a modo tuo.
Se un passo non si può eseguire, scrivi quale e perché. Non attribuire esiti che non hai visto.

REVISIONE 2 — LETTURA CRITICA E ATTACCO
1. F-01…F-10: le risposte (R9) e le correzioni successive li chiudono, li chiudono in parte o no? Con il motivo.
2. A1–A25: d'accordo con la proposta, oppure proposta diversa con il motivo. Severità massima su A15 (buchi nei
   minuti), A17 (spread di riferimento), A22–A25 (nuove).
3. Il programma dei criteri ha avuto 8 difetti critici in due giri, TUTTI nei collegamenti fra sigillo, registro,
   caricatore, sviluppo, verifica e riga di comando. Attacca lì, con l'approccio nuovo in mente: esiste ancora una
   scelta libera? Si può eseguire codice diverso da quello sigillato? Si può far promuovere una strategia senza
   vantaggio, guardare il periodo sigillato, ripetere la verifica, sbagliare N o V del DSR?
4. Almeno 5 test tuoi e almeno 5 mutanti nuovi, con l'esito.
5. La regola d'uscita per il sigillo (v3.2, §C) è sufficiente? Cosa manca?

CONSEGNA: documento «DGS-20261115-02-revisione-R12», con:
- la tabella dei rilievi (gravità critica / importante / minore, file, riga, prova);
- l'output dei comandi;
- i tuoi test e mutanti con l'esito;
- la posizione su F-01…F-10 e su A1–A25;
- l'autocritica;
- UNA di queste formule finali:
  «nessun difetto critico o importante: sigillabile dopo le decisioni A1–A25» /
  «sigillabile dopo le decisioni e queste correzioni: …» /
  «non sigillabile, perché: …».
Il sigillo fissa le regole PRIMA dei risultati; la verifica storica viene dopo e richiede gli ASK storici.
```
