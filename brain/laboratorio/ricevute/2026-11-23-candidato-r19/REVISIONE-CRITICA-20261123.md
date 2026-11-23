# Revisione critica di Claude sul percorso di verifica · 23/11/2026

Richiesta dal titolare dopo DGS-17 («siamo in una fase molto importante»). Ho cercato i punti deboli che test e mutanti non vedono: quelli del flusso operativo, delle decisioni non ancora prese e dei confini fra sintetico e reale.

## A. Corretti oggi (con test scritti prima)

| # | Che cosa | Come si è visto |
|---|---|---|
| #139 | Due prenotazioni della stessa domanda potevano superare entrambe il controllo «una verifica sola» (#138), che gira prima dell'autorizzazione; la seconda la fermava solo la quota non collaudata. Ora l'unicità è garantita **dal registro della riserva**, sotto il blocco e alla ricostruzione | DGS-17 Q8, riprodotto |
| #140 | Con una caduta fra l'esito scritto nella riserva e quello nel registro delle prove, la ripresa non riconciliava i due registri | DGS-17 Q8, riprodotto |
| — | Una seduta con i dati completi ma senza operazioni (K = 0) non era mai esercitata: ora c'è un test con il 25% di giornate neutre e la media ricalcolata come somma degli S diviso somma dei K | DGS-17 |
| — | **Lacune dei MIEI test, trovate in questa revisione:** #139 non era provato dopo l'esito della prima verifica (il mutante PR14 sopravviveva); la ripresa tecnica dopo una caduta durante la lettura non era provata attraverso l'esecutore. Test aggiunti, codice invariato (`67380cd`) | Rilettura del codice e mutante a mano |
| — | Il controllo veloce dei mutanti ora verifica anche che il file mutato resti Python valido: PR12 ed EV33 erano «non validi» e si sarebbero visti solo nella corsa lunga | Corsa mirata |

## B. Punti critici ancora aperti (in ordine di gravità)

1. **L'autorizzazione è scritta in locale prima della lettura, ma non è ancora su GitHub. — RISCHIO PRINCIPALE.**
   - Oggi l'esecutore scrive l'autorizzazione nel file della riserva e subito dopo legge i dati.
   - Se dopo la lettura il file venisse ripristinato in locale (`git checkout`, copia di riserva) prima del commit, il consumo sparirebbe. La finestra si potrebbe allora leggere di nuovo, con un'altra scheda, senza traccia. È il limite già dichiarato #90/#98 (registri locali prima del push), che vale anche per il percorso nuovo; la protezione del ramo (D-49) non è attiva.
   - **Proposta (DA-41):** l'esecutore si ferma dopo aver scritto l'autorizzazione e chiede commit e push. Legge i dati solo quando l'ancora conferma che quell'autorizzazione è già sulla versione remota. Tecnicamente è una ripresa con lo stesso impegno, e il controllo c'è già (`controlla_ancora` più la storia). Costa un passo in più per verifica, ma chiude il buco più serio.
2. **La potenza stimata della scheda è un input, non un calcolo** (DGS-16, DGS-17 Q9).
   - Oggi chi scrive la scheda può dichiarare 0,6 e superare lo screening (D-36, D-47).
   - Prima di qualunque accesso reale serve la procedura di potenza dentro il contratto H-003 (ricetta sigillata, semi, repliche, evento, ricalcolo prima dell'autorizzazione), come descritta dal DGS.
   - Non è un difetto del codice di oggi, ma è un **requisito bloccante per l'uso reale**.
3. **Ambiente di riferimento non fissato** (DGS-17 Q1).
   - Fra 3.13 e 3.9 i verdetti coincidono, ma gli estremi differiscono di 102 ulp.
   - Va deciso quale ambiente produce il risultato ufficiale, con l'identità registrata nell'impegno.
   - **Proposta (DA-40):** un'immagine Linux riproducibile con Python e versione esatti, qualificata rieseguendo i riferimenti congelati del collaudo IA-02. Il Mac (3.9) e l'altra versione restano prove di portabilità.
4. **R19 è partito su `1431190`, ma il codice è cambiato dopo (#139 e #140 in `b9ec2f4`; più test in `67380cd`).** Per D-24 il giro vale per il candidato che rivede.
   - **Proposta:** a Gemini un'aggiunta al mandato con la differenza `1431190..67380cd`: riserva, esecutore, test, mercato sintetico. Gemini la rivede dentro R19.
   - In alternativa, R19 conta per `1431190` e le correzioni si rivedono a parte. Ma allora il candidato finale non avrebbe un giro pulito.
5. **Il manifesto non è mai stato confrontato con i registri VERI dello scaricamento.**
   - **Verificato (REGISTRO-MODIFICHE v1.33):** il BID fino al 07/06/2009 era già in cache il 15/11, prima che nascesse `scarica_cache` con il registro per giorno. Quei file hanno una riga solo se `scarica_cache` è poi passato su quel periodo, come «in-cache-non-registrato», con l'impronta di quel momento. Altrimenti il manifesto li vede «omessi».
   - **Trovato leggendo il codice:** `--riprova-vuoti` aggiunge una seconda riga valida per lo stesso giorno (prima «vuoto-200», poi «dati»), e il manifesto la tratta come «voce doppia». Una riga del lato o del mercato sbagliato, in qualunque data del registro, compare fra le anomalie di **ogni** finestra.
   - In tutti questi casi il manifesto **blocca**: è il verso giusto, perché non lascia passare niente. Però potrebbe rendere inutilizzabili interi anni di riserva.
   - **Fatto:** `laboratorio/studi/diagnosi_manifesto.py` (`7edcb80`, fuori dal candidato), test scritti prima, mutanti 13/13 su 3.13 e 3.9.
     - Applica lo stesso manifesto al periodo intero e conta le anomalie per tipo, lato e anno, con gli esiti delle voci doppie.
     - Controlla che i byte di ogni file abbiano l'impronta del registro, senza decodificarli.
     - Scrive solo conteggi e date.
   - **Eseguita il 23/11** (`../2026-11-23-diagnosi-manifesto/RICEVUTA-DIAGNOSI.md`). Nessun file è alterato, ma il manifesto blocca in tre casi: BID senza riga fino al 07/06/2009 (1.619 giorni); 236 doppioni identici del 16/11 (#60); **sviluppo interamente senza registro**, quindi oggi lo screening si fermerebbe. Opzioni A1 e B1 al DGS (messaggio 17, Q2).
   - **Era da fare sul Mac:** `dati/PROCEDURA-DIAGNOSI-MANIFESTO.md`, su riserva (confini di D-29) e sviluppo. Se escono anomalie, come trattarle (per esempio: vale l'ultima riga dopo una nuova prova dei vuoti, oppure si rigenera un registro di riconciliazione firmato dal titolare) è una **decisione di metodo**, da portare al DGS prima di cambiare il manifesto.
6. **Un solo simulatore.** `esegui_verifica` accetta solo `orb_londra` con le varianti di H-002. Per una scheda H-003 vera con un'altra strategia servirà un simulatore registrato e sigillato. Il percorso va esteso prima di quella scheda, non adesso.
7. **La prova della storia git usa un remoto finto** (DGS-17).
   - Il permesso reale, la versione autorevole su GitHub e la protezione dei riferimenti restano da provare con il repository vero, prima del primo accesso reale.
   - Con il piano Free (DA-39) una protezione dei riferimenti su GitHub non c'è: oggi la storia locale è l'unica difesa.
8. **Positivo completo dal lanciatore.**
   - Il lanciatore è provato sui rifiuti, e sul passaggio all'esecutore fino ai registri finti.
   - Una corsa positiva completa `avvio.py verifica` → promossa, con registri canonici in un repository git di prova, non c'è ancora.
   - **Proposta:** aggiungerla come prova di ricevuta, oppure chiederla a Gemini in R19.

## C. Che cosa NON è a rischio, per chiarezza

- La riserva reale non è mai stata letta. Il consuntivo ha prodotto solo conteggi e date. La copia estratta per sbaglio da Safari non è stata aperta ed è stata cancellata.
- Le decisioni del verdetto non dipendono dalla versione di Python: è controllato su 9 casi a filo di soglia e sulle prove A–G.
- Le verifiche già fatte sui dati sintetici sono attribuite ai loro commit, con log e impronte.
