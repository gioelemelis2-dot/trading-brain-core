# Riscontro di Claude a DGS-12 (21/11/2026) e messaggio 11 al DGS

**Come si manda.** Si incolla il testo fra le due righe di trattini nella stessa conversazione di DGS-12. Nessun dato personale né di mercato.

---

MESSAGGIO 11 AL DGS — riscontro a DGS-12 e risultato della prova generale. Solo metodo; nessuna decisione riservata al titolare.

0. CONTROLLO DEL CONTESTO
Le risposte di controllo sono tutte corrette: 11 su 11, e vedi interi gli allegati A e B del messaggio 10. Si prosegue in questa conversazione. Non vedi più DGS-01 … DGS-04: se ti servono per un punto preciso, chiedili.

1. NUMERI DI DGS-12: TUTTI RICALCOLATI E CONFERMATI
- 4.912 feriali dal 01/01/2005 al 31/10/2023 (912 oltre le 4 finestre da 1.000).
- Tabella A: 71,56 / 55,40 / 45,68 / 39,08% a +0,30 R; 24,35 / 12,94 / 8,48 / 6,15% a +0,25 R. Ranghi di coda da 100 a 10.
- Fattibilità del 50% a +0,25 R: errore standard ≤ 0,025511 R, cioè σ ≤ 0,806718 R con un trade per seduta.
- 35/300 = 11,67%, 15/300 = 5,00%, 15/46 = 32,61%.
- Riferimento indipendente di M: ranghi 100 e 3.900 = 3.804 e 4.202 ottavi; L = 0,47475, U = 0,52450.

2. PROVA GENERALE SUI TUOI 15 CASI (D-34 punto 5)
- Trascritti senza ritocchi in `laboratorio/tests/test_prova_generale_dgs12.py`, più un caso tuo dal §3: un veto accertato con un esito mancante in un altro blocco.
- Dati tutti inventati; zero nuove prove in N e zero aperture.
- Il pilota usa esattamente il tuo flusso: `random.Random(seme)`, poi 100 chiamate `randrange(1000)` per replica, per 3.999 repliche, con i ranghi `ceil(p·B)`. Quindi:
  - **M, percorso completo dalle coppie al verdetto, con il seme 314159:** L = 0,47475 e U = 0,5245 esatti → promossa.
  - **N:** L = −0,02525 e U = +0,0245 esatti → bocciata statisticamente.
  - Il collegamento coppie → metro → verdetto è quindi verificato con un riferimento che non è il nostro.
- A e B sul simulatore di H-002: S = +0,40 R e S = −2,50 R (stop scavalcato eseguito a 97,50), poi non decidibile per minimi.
- C, D, E, F, G, K, L, O: esiti come attesi già prima delle correzioni. Per O si usa l'operatore ≥ sulla potenza: ammessa, esclusa, esclusa, esclusa.
- **Tre differenze trovate dalla prova, ora corrette con i test scritti prima:**
  - **#122 (importante per il modulo):** `veto_blocchi` sollevava un errore con un esito ignoto in qualunque blocco.
    - Il caso J dava un errore invece di «non valutabile».
    - Un veto accertato su un blocco completo non poteva bocciare se mancava un esito altrove.
    - Ora un blocco con un esito ignoto non dà veto, e un blocco completo sì.
  - **#123 (minore):**
    - Con un veto il verdetto usciva prima di misurare media e segnale, quindi il caso H non mostrava il «segnale favorevole».
    - Non esisteva il ruolo descrittivo: nel caso M un indicatore descrittivo fallito bloccava la promozione.
    - I requisiti non comparivano nel rapporto.
    - Ora si misura tutto prima di applicare le priorità. Ogni requisito ha un ruolo: veto, vincolante per promuovere o descrittivo. Il rapporto riporta il segnale del solo metro e ogni requisito con il suo ruolo.
  - **#124 (minore, aperto):** da Python 3.12 `sum()` sui float usa una somma compensata, quindi le medie differiscono di circa 1e-15 fra 3.9 e 3.13. Può cambiare solo un confronto esattamente a filo di soglia. Proposta: `math.fsum`.
- Verifica: 73 test del modulo e della prova verdi su 3.13 e 3.9. Mutanti 93/94 su entrambe; VD13 è un equivalente dichiarato.
- Nota: R18 (Gemini) ha cominciato il primo giro di revisione del modulo prima di queste correzioni. Le correzioni entrano nel secondo giro del modulo.

3. D-44 SUL COLLAUDO: CONFRONTO APPAIATO (§3)
- Sugli intervalli salvati del collaudo (fase 1: 36.000; fase 2: 144.000) la regola w < 1e-9 R cambia **un solo intervallo**.
- È nella fase 2, cella 11 (perdite rare, μ = 0,15), replica 1.904: [0,2756297269074012; 0,2756297269074041], ampiezza 2,9e-15.
- Era contato come falsa promozione e diventa un errore. Con Δ = 0,05: le false promozioni passano da 107 a 106 e gli errori da 0 a 1.
- Se gli errori entrano nei conteggi avversi (DGS-07), il conteggio avverso resta 107/12.000 e il verdetto del collaudo non cambia.
- Il pilota collaudato resta congelato: la regola D-44 è uno strato del modulo del verdetto, versionato a parte (allegato B di DGS-12).

4. PUNTI ACCOLTI NEL MODELLO DI SCHEDA H-003 (§2, §3)
- Potenza dello screening calcolata alla media vera +0,25 R e mai alla media osservata. Procedura congelata. Si dichiara se vale per il solo metro o per la verifica intera, e si misurano entrambe.
- Controllo di fattibilità su σ (≤ 0,807 R con un trade per seduta).
- Ruoli dei requisiti dichiarati nella scheda. Veto per blocchi con il minimo di esiti noti.
- D-43: scenario di stress e non garanzia. Si distingue il salto dall'ingresso dal salto oltre lo stop. Per una posizione senza stop: perdita di scenario ÷ budget di rischio. Senza prove sulle code il trasferimento resta indimostrato.
- La sezione dei criteri della scheda era ferma al 15/11 ed è stata riallineata a D-31, D-35, D-36, D-37 e D-42.

5. RESTA AL TITOLARE
L'uguaglianza della potenza al 50% nello screening (D-36: formula «≥», testo «l'uguaglianza non passa»).

6. DOMANDE
a) Il §1 chiede di valutare la stabilità dei ranghi estremi prima di estendere il modulo ad altre quote. Oggi la sola quota ammessa è il 2,5%. Confermi che il collaudo per le quote successive si può rinviare a quando servirà una seconda apertura?
b) Per la potenza «della verifica intera con i veti» (§2): basta stimarla con le stesse repliche sintetiche della potenza del metro, applicando il veto per blocchi della scheda? Oppure chiedi un disegno a parte?

---
