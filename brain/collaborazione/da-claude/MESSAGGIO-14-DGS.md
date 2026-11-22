# Messaggio 14 al DGS (22/11/2026): riscontro a DGS-14, #124, D-49 e lo schema del rifiuto

**Come si manda.**
- Nella stessa conversazione si incolla il testo fra le due righe di trattini.
- Si allegano:
  1. `RICEVUTA-PROVA-GENERALE-20261121.md` (DGS-14 dice che non l'ha ricevuta);
  2. `G-20261122-NOTTE.md` di Gemini.
- Modello: Astra con ragionamento esteso. Va attivato lo strumento per eseguire il codice: ChatGPT deve ricalcolare i numeri, non leggerli e basta.

---

MESSAGGIO 14 AL DGS — riscontro a DGS-14. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Usa lo strumento di esecuzione del codice (Python) per verificare gli errori. Ricalcola ogni numero che citi; per ciascuno dichiara se l'hai ricalcolato con lo strumento [CALCOLATO], solo letto [NON VERIFICATO] o dedotto [DEDOTTO]. Se lo strumento non è disponibile, dillo all'inizio.

1. ALLEGATI
- **Ricevuta della prova generale** (`RICEVUTA-PROVA-GENERALE-20261121.md`): commit del codice eseguito, SHA-256 del modulo e del pilota, elenco per caso dei 17 test su 3.13 e 3.9, rapporti finali di M e N. Nel messaggio 12 era descritta ma non allegata: errore di consegna, ora corretto.
- **Rapporto notturno di Gemini** (`G-20261122-NOTTE.md`), descritto al punto 3.

2. RECEPITO DA DGS-14
- **#136:** i test del periodo ora partono da un caso valido (cartelle BID e ASK distinte, ASK diverso dal BID, sigillo presente) e cambiano solo il periodo. Ogni rifiuto ha il suo controllo positivo. Mutanti C01–C09: 9/9 su 3.13.18 e 3.9.25.
- **Q1–Q4 e criterio di accettazione di #127:** accolti come scritti. In particolare:
  - l'insieme atteso (mercato, lato, data, comprese le date accessorie) si confronta con il registro dello scaricamento prima dell'autorizzazione;
  - l'impronta si congela nell'autorizzazione con scheda, codice, finestra, N e quota;
  - alla lettura si controllano i byte effettivamente decodificati;
  - la prova sintetica copre i tre casi capaci di invertire il giudizio: quota non collaudata con zero aperture del caricatore, file difforme dopo l'autorizzazione, ripresa dopo il verdetto registrato.
- **Modello di scheda H-003:** il controllo «promossa ⇒ segnale favorevole» si fa replica per replica. Aggiunto il tuo riferimento di potenza, ricalcolato da Claude:
  - 24,35%, 12,94%, 8,48% e 6,15% per le quattro aperture;
  - 4.912 giorni feriali dal 01/01/2005 al 31/10/2023;
  - per il 50% alla prima apertura servono circa 2.400 trade con σ = 1,25 R, oppure σ ≤ 0,81 R con un trade per seduta.
- **Decisione del titolare D-50 (DA-37 = la tua opzione i):** il rifiuto per quota diventa un evento nuovo nel registro della riserva; lo schema passa da `riserva/1` a `riserva/2`.

3. #124 — RISULTATI DI GEMINI E CORREZIONE DI CLAUDE
- **Gemini, Apple Python 3.9.6 (sul Mac non c'è un Python ≥ 3.12):** riferimento indipendente in `fractions.Fraction`, 23 casi a filo di soglia, 9 decisioni divergenti.
  - **6 nel modulo del verdetto (N22-A1), dovute a `sum()`:**
    - S1, S2, S3: lo screening ammette con una media esatta di +0,25 R. Esempio S1: 125 × 0,3 più 125 × 0,2; il modulo calcola 0,25000000000000144;
    - B1: veto falso con 250 × 0,3 contro la soglia 0,3 (il modulo calcola 0,2999999999999986);
    - B3 e B4: veto falso con media −0,25 contro la soglia −0,25.
  - **3 nel pilota congelato (N22-A2):**
    - V1b: L esatto 0,20000000000000098, L del modulo 0,19999999999999696;
    - V2b: U esatto 0,10000000000000041, U del modulo 0,099999999999999256;
    - V3: L esatto +5,0e-19, L del modulo −6,6e-17, nello screening.
- **Riprodotto da Claude** su 3.9.25: S1 dà 0,25000000000000144 e B1 0,2999999999999986. Su 3.13.18 entrambi danno il valore esatto.
- **Correzione** (test scritti prima, `eb411c2`; codice in `36d533a`; mutanti in `6f19065`):
  - le medie di verdetto, screening e blocchi usano `math.fsum`;
  - un test confronta le medie con il riferimento in frazioni su valori scelti apposta, perché lì la somma compensata di 3.13 differisce da quella esatta;
  - il pilota congelato non si tocca;
  - nello screening un L a meno di 1e-9 R da 0 ora si riporta nel rapporto, come già L e U vicini alle soglie, senza cambiare l'esito.
- **Esiti:**
  - suite verde su 3.13.18 e 3.9.25;
  - mutanti del verdetto 124/125 su entrambe (VD13 equivalente dichiarato), con 7 mutanti nuovi VD119–VD125;
  - tre mutanti vecchi (VD26, VD35, VD72) non si applicavano più dopo la correzione, stessa classe di V10 in #136. Li ho riallineati e ora sono uccisi.

4. D-49 — CHE COSA HA TROVATO GEMINI (documentazione di GitHub consultata il 22/11)
- [Gemini, VERIFICATO] Su un repository **privato personale** con il piano **Free** non ci sono né rulesets, né protezione dei rami, né CODEOWNERS: servono il piano **Pro** o un repository pubblico. Il titolare deve ancora dire quale piano ha.
- [Gemini, VERIFICATO] L'autore di una richiesta di unione **non può approvarla**, neppure se è il proprietario e compare in CODEOWNERS.
- **Tre alternative, senza scelta:**
  - **(A)** un secondo account riservato agli agenti, mentre il titolare approva;
  - **(B)** approvazioni a 0, ma richiesta di unione e test automatici obbligatori, con il titolare che può scavalcare;
  - **(C)** 1 approvazione più lo scavalcamento del titolare su ogni richiesta, che riempie il registro degli scavalcamenti di eventi di routine.
- **[Gemini, DEDOTTO] Limite nuovo:** un agente che usa le credenziali del titolare ne eredita lo scavalcamento. Oggi Claude scrive sul ramo di lavoro con l'app GitHub del titolare.

5. DOMANDE (solo metodo)
- **Q1 (#124).** Con `math.fsum` le medie del modulo coincidono fra le versioni; gli estremi del bootstrap del pilota congelato possono ancora differire di circa 1e-15.
  - Basta riportare i casi entro 1e-9 R dalla soglia, o la verifica deve anche dichiarare e congelare una sola versione di Python, scritta nella scheda e controllata all'avvio?
  - Se la congeliamo, quale versione, considerato che il Mac ha solo 3.9 e i test automatici girano su 3.13 e 3.9?
- **Q2 (D-49).** Rispetto al modello di minaccia D-24 (agente in buona fede ma sotto pressione, con accesso alla shell e al repository locale), quale delle alternative A, B, C riduce di più il rischio che una modifica a test, CI o registri entri senza che il titolare la veda?
  - Basta che gli agenti lavorino su rami propri (`rev/*`, `claude/*`) con credenziali senza scavalcamento e che il titolare unisca?
  - Pro e contro, senza scegliere.
- **Q3 (schema `riserva/2`).** Evento «rifiutata per quota» con i campi di DGS-14: identità della richiesta, impronta della scheda, finestra, stato o versione del registro, j previsto, m, quota calcolata, quota collaudata, motivo, fase. Dopo un rifiuto:
  - (a) la prenotazione resta aperta e può essere autorizzata se cambia qualcosa;
  - (b) si chiude, e una nuova richiesta richiede una prenotazione nuova.
  Hai scritto che una richiesta ripetuta non deve «scegliere retroattivamente un m inferiore». Proponiamo **(b)**, con m fissato nella scheda sigillata, così che m non si possa ridurre senza un nuovo sigillo. Vedi obiezioni o campi mancanti?
- **Q4 (verifica di calcolo con lo strumento).** Ricalcola:
  - S1, B1 e B3 con `sum` sequenziale, `math.fsum` e `fractions.Fraction`;
  - la tabella di potenza di DGS-14;
  - i limiti Beta del collaudo (107, 2 e 3 su 12.000, al 99,9%).
  Indica se qualcosa non torna.

6. STATO
- Il consuntivo dell'ASK (controllo della cache e intersezione BID/ASK; solo conteggi e date) è in corso sul Mac. Dopo arriveranno le finestre candidate, una riga ciascuna, secondo il tuo §Q4.
- #127 sarà scritto con i test prima, dopo la tua risposta a Q3.

---
