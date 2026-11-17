# Messaggio 4 per il DGS (ChatGPT): riallineamento, 17/11/2026

Da incollare nella chat del Progetto «Trading Brain», allegando `trading_brain_dgs06.zip`:
- commit `c5ca93d`;
- SHA-256 `58d294292ffdceb9b931b64a5bb75bdcc0408d9efc0699fca78791a9e29af9a5`.

**Sostituisce il messaggio 3**, che non è mai stato inviato. Il DGS si era fermato a DGS-04, con l'archivio del commit `83c8956`.

```
MESSAGGIO 4 AL DGS — riallineamento dopo DGS-04 (sostituisce il messaggio 3, mai inviato)

PACCHETTO
trading_brain_dgs06.zip: contenuto esatto del commit c5ca93d del ramo feat/esecutore-h002, REDATTO (nome,
utente GitHub, email e percorsi personali sostituiti da segnaposto). Leggi LEGGIMI-PACCHETTO.md e controlla
ogni file contro MANIFEST.tsv (colonna sha256). Due vecchi zip sono esclusi e dichiarati.
ORDINE DI LETTURA: 1) brain/governance/STATO-PROGETTO.md (una pagina: dove siamo, contatori, cosa manca);
2) brain/governance/REGISTRO-MODIFICHE.md da v1.38 a v1.49; 3) brain/laboratorio/REGISTRO-DIFETTI.md da #41;
4) i documenti citati sotto. La scheda di stato è la fonte unica: d'ora in poi ogni ripresa parte da lì.

COSA È SUCCESSO DOPO DGS-04 (da verificare sui documenti, non da credere)
1. Revisione tecnica (la tua domanda su R11 e 83c8956): dopo R11 ci sono stati R12-bis, R13, BANCO-02 e R14
   di Gemini e due revisioni con revisori separati di Claude. Difetti registrati: 104 (24 critici). Il banco
   NON è sigillabile: giri puliti di fila 0 su 2; R14 (oggi) ha trovato ancora un critico, corretto. Il codice
   non è più 83c8956: vale c5ca93d.
2. Decisioni del titolare dopo DGS-04:
   - H-002 «non decidibile · parcheggiata», con condizione d'uscita scritta (laboratorio/ipotesi/H-002-REVISIONI.md);
   - IA-02 = R medio netto ≥ +0,15 R, fissato prima di ogni idea H-003 (commit 032250b, governance/IMPEGNI-ANTICIPATI.md);
   - emendamento su N in DA-19;
   - D-24 (oggi): modello di minaccia della regola d'uscita. I due giri puliti contano gli errori in buona fede
     e le manomissioni facili; prima della verifica, un giro su TUTTE le manomissioni e la decisione sulla
     protezione del ramo su GitHub (governance/DECISIONI.md).
3. Riserva (2005-01-01 → 2023-10-31, il tuo Gate 4): MAI aperta dal sistema. Il censimento delle esecuzioni
   passate (collaborazione/da-gemini/G-20261115-03-censimento-esecuzioni.md) è stato RICONFERMATO oggi con
   lo strumento di riconteggio corretto (governance/censimento/RICONTEGGIO-20261117.md): nessuna uscita dalla
   cache vera. Limite dichiarato: ciò che una persona ha guardato a mano non si conta.
4. Storico XAUUSD (il consuntivo che aspettavi): sviluppo 15/11/2023 → 12/11/2026 completo BID e ASK. Storico
   BID completo fino all'11/02/2020, in scaricamento dal 12/02/2020 (si era fermato per un riavvio del Mac);
   ASK storico ESISTE dal 2005, in scaricamento. Il consuntivo (copertura, buchi, integrità, BID e ASK
   allineati) NON è ancora pronto: arriva a scaricamento finito, con dati/pipeline/controlla_cache.py (anche
   --ask) e laboratorio/studi/taratura_completezza.py (solo conteggi, mai prezzi).
5. Errori e incidenti da conoscere: #41 (14/11, un'esecuzione sui dati veri prima del sigillo: esplorazione
   E-003, conta in N); #72 (un pacchetto per te conteneva un dato personale dentro uno zip annidato: scoperto
   prima dell'invio, non ti è mai arrivato; lo strumento ora accetta solo testo).

PARERI RICHIESTI (decide il titolare; tu dai il parere più severo e motivato che puoi)
P1. IA-02: la soglia +0,15 R si applica alla stima o al limite inferiore dell'intervallo, nello sviluppo e
    nella verifica? (laboratorio/studi/risultati/potenza_IA-02.md: potenza e correlazione fra trade misurata da Gemini)
P2. Regole di spesa della riserva: α totale, scelta delle finestre, parte protetta
    (laboratorio/esecuzione/riserva.py è il meccanismo, presentato per ratifica, senza valori decisi).
P3. Modello di scheda per H-003 (laboratorio/ipotesi/MODELLO-SCHEDA-H-003.md): manca qualcosa per evitare
    l'autoinganno?
P4. DA-31 (governance/DECISIONI-APERTE.md): verdetto della verifica a due stati o a tre (con «non decidibile»).
P5. Consuntivo dello storico: scrivi ORA, prima di vedere i numeri, i criteri con cui lo accetterai
    (copertura minima per anno, buchi ammessi, BID/ASK allineati, soglie di completezza). Così il criterio
    non si adatta ai dati.
P6. D-24 è già decisa: dimmi solo se vedi un rischio che il titolare non ha considerato. Non riaprirla.

COSA NON FARE
- Non attaccare il codice: lo fa Gemini (R15 dopo la corsa dei mutanti di Claude).
- Non proporre modifiche ai criteri o ai verdetti di H-002.
- Non chiedere accesso a repository, worktree o cartelle di dati: leggi solo il pacchetto redatto.
- Sulla fase «grafici» con il titolare (dopo la baseline): solo dati dal 15/11/2023 in poi; ogni lettura
  si scrive con data e periodo guardato PRIMA di provarla; l'autore delle idee è il titolare. Tu le metti
  alla prova, ma non le scrivi tu: chi giudica non deve essere l'autore.

CONSEGNA
DGS-05: per ogni punto da 1 a 5 «verificato / non verificabile / in disaccordo», con il file letto; i pareri
P1–P6; cosa hai letto per intero, in parte o no. Mai compiacente.
```
