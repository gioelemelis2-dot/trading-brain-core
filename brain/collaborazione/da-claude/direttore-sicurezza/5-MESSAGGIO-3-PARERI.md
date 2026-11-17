# Messaggio 3 per il DGS (ChatGPT), 16/11/2026

Da incollare nella chat del Progetto «Trading Brain», **allegando il pacchetto nuovo** `trading_brain_dgs05b.zip` (17/11, commit `1573ad7`, SHA-256 `ccf54d6b…`). Il pacchetto è redatto: niente nome, utente GitHub o percorsi personali. **NON allegare `trading_brain_dgs05.zip`** (16/11): conteneva il nome dell'utente dentro uno ZIP annidato (difetto #72). Se è già stato inviato, dirlo a Claude: va registrato. Gli archivi precedenti sono superati.

```
MESSAGGIO 3 AL DGS — tre pareri da dare al titolare, più un controllo del pacchetto

PACCHETTO
trading_brain_dgs05b.zip: contenuto esatto di un commit del ramo feat/esecutore-h002, REDATTO (richiesta DGS-10,
difetto #43; difetto #72: due archivi annidati esclusi e dichiarati in LEGGIMI). Leggi LEGGIMI-PACCHETTO.md e controlla ogni file contro MANIFEST.tsv (colonna sha256). I file con
redatto = no hanno la stessa impronta del commit su GitHub. Dichiara cosa hai letto per intero, in parte o no.

COSA È SUCCESSO DOPO DGS-04 (da verificare sui documenti, non da credere)
1. Censimento delle esecuzioni sui dati veri chiuso: collaborazione/da-gemini/G-20261115-03-censimento-esecuzioni.md
   (sezioni 5–8). Riserva 2005 → 31/10/2023 intatta per tutto ciò che è contabile; esplorazioni di Gemini registrate
   come E-003 (laboratorio/studi/REGISTRO-ESPLORAZIONI.md). ATTENZIONE, dopo questo pacchetto: una revisione
   notturna ha trovato quattro buchi nello strumento di riconteggio (#75, #78, #80, #81: comandi su più righe, date
   compatte, uscite con soli prezzi, un campo delle trascrizioni non letto). Corretti; la conclusione «intatta»
   è DA RICONFERMARE con il riconteggio corretto sul Mac. Non trattarla come chiusa.
2. H-002: «non decidibile · parcheggiata» per decisione del titolare, con condizione d'uscita scritta
   (laboratorio/ipotesi/H-002-REVISIONI.md): solo su dati successivi al 12/11/2026, sigillata prima, contata in N.
   La patch dei tre verdetti di Gemini (riprova sugli stessi dati) è archiviata e NON applicata.
3. Impegni anticipati (governance/IMPEGNI-ANTICIPATI.md): IA-01 (0,15 R) senza prova di anteriorità; IA-02 fissato
   il 16/11 alle 00:12 UTC (commit 032250b) prima di qualsiasi idea di H-003: R medio netto ≥ +0,15 R per trade.
4. Terzo attacco di Gemini (R12-bis): 9 difetti importanti, tutti riprodotti e corretti in TDD, più #59 e #60
   trovati da Claude (laboratorio/REGISTRO-DIFETTI.md #48–#60; governance/REGISTRO-MODIFICHE.md v1.40–v1.42).
   Contatore dei giri puliti per il sigillo: zero. Gemini sta facendo R13 sullo stesso codice: NON attaccare il
   codice, salvo dove serve a sostenere un tuo giudizio.
5. Tue richieste a Claude in DGS-04: richiesta 1 (404, risposta vuota, guasto) fatta; richiesta 3 (registro della
   riserva) fatta come meccanismo, laboratorio/esecuzione/riserva.py, «presentata per ratifica»; il pacchetto
   redatto è questo.

PARERI RICHIESTI (al titolare spetta la decisione; tu dai il parere più severo e motivato che puoi)
P1. Soglia IA-02 (laboratorio/studi/risultati/potenza_IA-02.md e potenza_soglia.py).
    Claude propone: «sulla stima» nello sviluppo (circa 450 trade), «sul limite inferiore al 95%» nella riserva
    (circa 2.500 trade), oltre a DSR e agli altri criteri. Rifai i numeri in modo indipendente. Dì se la proposta è
    giusta, troppo severa o troppo permissiva, tenendo conto di N, del DSR, della correlazione fra trade e del fatto
    che la riserva si usa una volta sola. Se proponi altro, dai i numeri.
P2. Regole di spesa della riserva (riserva.py; tuo DGS-04 §5–§7). Proponi valori concreti da ratificare:
    α totale; parte protetta (quale intervallo e perché); come si sceglie la finestra (ordine, durata minima,
    embargo, riscaldamento); cosa succede a un esito «non decidibile»; cosa succede se mancano gli ASK storici
    (lo scaricamento è in corso: gli ASK prima del 2023 potrebbero non esistere).
P3. Modello di scheda per le ipotesi future (laboratorio/ipotesi/MODELLO-SCHEDA-H-003.md). Cosa manca, cosa è
    superfluo, cosa è troppo rigido o troppo morbido. Le parti «OBBLIGATORIO» sono abbastanza? Va bene il
    trattamento dei tre esiti (non decidibile risolto solo su dati nuovi)?
C1. Controllo del pacchetto: cerca dati personali rimasti (nomi, utenti, percorsi, indirizzi, numeri di conto).
    Se ne trovi, indica file e riga senza ripetere il dato.

REGOLE
Le tue istruzioni del Progetto valgono tutte: etichette su ogni affermazione, prove mostrate, nessun complimento.
Ogni «d'accordo» con un calcolo o un controesempio. N +0 per questi pareri (nessuna prova sui dati).
CONSEGNA: un solo documento, «DGS-20261116-05-pareri», con P1, P2, P3, C1 e, in fondo, le richieste a Claude e a
Gemini, verificabili.
```
