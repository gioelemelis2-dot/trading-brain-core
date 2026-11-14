# Mandato R12 per Gemini (Antigravity)

Da incollare in Antigravity. Il commit è indicato nel messaggio dell'utente: è l'ultimo del ramo `feat/esecutore-h002` dopo le correzioni R11.

```
MANDATO R12 PER GEMINI — terzo attacco al programma dei criteri di H-002, dopo il cambio di approccio

Contesto: ho integrato il tuo R11 (sezione R11 di brain/laboratorio/ipotesi/H-002-REVISIONI.md; difetti #33–#40 nel
REGISTRO-DIFETTI). Correzioni in TDD (rosso d4a5dc9, verde f248f8a, mutanti bef3e2d). Invece di chiudere un buco alla
volta ho cambiato approccio:
- la riga di comando non ha più scelte libere: periodi (PERIODO_SVILUPPO, PERIODO_VERIFICA), ripetizioni e seme sono
  costanti del codice; restano solo modalità, conferma delle varianti, percorsi;
- il sigillo registra le impronte SHA-256 dei 7 file che eseguono la scheda (FILE_CODICE); ogni esecuzione le controlla;
- giorni feriali vuoti = dati mancanti (tollerati solo 1/1, 25/12, Venerdì Santo);
- impronta dei dati letti e cache identica fra sviluppo e verifica; esito della verifica nel registro;
- DSR solo con almeno 30 trade; copertura minima 90% dei confronti (A23, in via prudenziale);
- i tuoi MR01–MR07 sono nello script (MR05 non esiste più: l'opzione --seme è stata tolta). Mutanti 89/89 e 40/40
  su Python 3.13 e 3.9; 138 test di H-002.

REGOLE: ramo tuo rev/gemini-r12 dal commit indicato; scrivi SOLO in brain/collaborazione/da-gemini/; niente dati reali,
niente Dukascopy, niente sigillo, niente merge. Lavora senza leggere i rapporti del DGS (ChatGPT) sullo stesso commit
finché non hai consegnato. Mai compiacente: ogni «d'accordo» con un calcolo o una prova.

COMPITI
1. Riesegui le tue sonde R7 e R11 (prove_r7_esecutore.py, prove_r11.py) sul nuovo codice. Dove l'interfaccia è
   cambiata (niente --inizio/--fine/--ripetizioni/--seme; sigillo con codice=), adegua SOLO l'invocazione, dichiaralo,
   e conferma che ogni difetto risulta bloccato.
2. Riesegui la tua replica dei criteri: nota che i criteri 4 e 5 ora richiedono copertura ≥ 90% (A23). Adegua solo
   questo punto, dichiaralo, conferma differenza 0.
3. Terzo attacco, con l'approccio nuovo in mente:
   - esiste ancora una scelta libera?
   - si può eseguire codice diverso da quello sigillato (moduli importati non nell'elenco, file di configurazione,
     variabili d'ambiente)?
   - il controllo dei feriali vuoti si può aggirare? Ha falsi positivi su chiusure vere dell'oro che non sono nell'elenco?
   - il registro si può manomettere in modo che i controlli non se ne accorgano?
   Almeno 5 sonde nuove e 5 mutanti nuovi, con l'esito.
4. Test e mutanti:
   python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra brain.laboratorio.tests.test_esecuzione brain.laboratorio.tests.test_esegui_h002
   python3 -s -B brain/laboratorio/tests/mutazioni_orb.py <cartella fuori dal repository>
   python3 -s -B brain/laboratorio/tests/mutazioni_esecuzione.py <cartella fuori dal repository> 2
5. Posizione su A22–A25 della proposta v3.2.

CONSEGNA: da-gemini/G-20261115-R12.md con la tabella dei rilievi (gravità come nel REGISTRO-DIFETTI), l'output dei
comandi e una frase finale esplicita: «R12: nessun difetto critico o importante» oppure l'elenco. Commit e push sul
tuo ramo.
```
