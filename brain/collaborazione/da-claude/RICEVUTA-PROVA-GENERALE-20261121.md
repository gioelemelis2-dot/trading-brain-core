# Ricevuta della prova generale sui casi del DGS (DGS-12 allegato C), 21/11/2026

- **Commit del codice eseguito:** `f5d0cad` (ramo `feat/esecutore-h002`); modulo `laboratorio/verdetto/verdetto_d31.py` dopo le correzioni #122, #123 (`f0ee358`) e #131–#134 (`f338381`).
- **Impronta SHA-256 del modulo:** `29ea3eb46df37f584c92a782ff1e63e8fd2d121055141ea739f76b1391038403`; del pilota: `717e55996b23a4954d69c97722458e30c2499000b5055fdcca4cba29f864b0ee`.
- **Percorso realmente eseguito:** A e B: `orb_londra.simula` (non `esegui_h002`) → coppie → `verdetto`; C, D, E, I, J, K, M, N: coppie → `intervallo` (pilota collaudato) → `verdetto`; F, G, H, L, O e M-bis: decisore con l'intervallo fornito. **Non esiste ancora** il percorso intero scheda → sigillo → screening → prenotazione → verdetto → rapporto (vedi #127): il punto 5 di D-34 resta aperto per quella parte.

## Python 3.13.18

```
Long di un'unità: acquisto all'ASK 101, vendita al BID 106, commissione totale 1, budget di rischio 10. ... ok
Long a 100, stop 99, prima vendita eseguibile a 97,50 dopo il salto, budget 1, costi nulli: S = −2,50 R. ... ok
999 coppie (0,40; 1) e una con K = 1 e S mancante: non decidibile per dati inidonei. Sostituirla con zero ... ok
test_d_minimo_trade (brain.laboratorio.tests.test_prova_generale_dgs12.TestDatiEMinimi.test_d_minimo_trade) ... ok
test_e_minimo_sedute_attive (brain.laboratorio.tests.test_prova_generale_dgs12.TestDatiEMinimi.test_e_minimo_sedute_attive) ... ok
test_k_intervallo_degenere (brain.laboratorio.tests.test_prova_generale_dgs12.TestPercorsiCompleti.test_k_intervallo_degenere) ... ok
Riferimento indipendente del DGS (CPython 3.12, random.Random(314159), 100 randrange(1000) per replica, ... ok
Stesso intervallo, un requisito vincolante per promuovere indeterminato: non decidibile. ... ok
test_n_bocciatura_da_coppie (brain.laboratorio.tests.test_prova_generale_dgs12.TestPercorsiCompleti.test_n_bocciatura_da_coppie) ... ok
Con l'operatore ≥ scritto nella formula di D-36 (lettura da far chiarire al titolare): ammessa, esclusa, ... ok
test_f_uguaglianza_di_l (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie.test_f_uguaglianza_di_l) ... ok
test_g_uguaglianza_di_u (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie.test_g_uguaglianza_di_u) ... ok
test_l_confine_d44 (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie.test_l_confine_d44) ... ok
Primo blocco 250 × (−0,50; 1), poi 750 × (1; 1). Media totale +0,625 R, segnale favorevole (estremi ... ok
test_i_veto_valido_con_minimi_globali_mancanti (brain.laboratorio.tests.test_prova_generale_dgs12.TestVeti.test_i_veto_valido_con_minimi_globali_mancanti) ... ok
Come I, ma il risultato del centesimo trade è ignoto: 99 esiti noti, veto non accertato, non decidibile. ... ok
DGS-12 §3: un blocco completo può bocciare anche se manca un'osservazione in un altro blocco. ... ok
Ran 17 tests in 0.608s
OK
```

## Python 3.9.25

```
Long di un'unità: acquisto all'ASK 101, vendita al BID 106, commissione totale 1, budget di rischio 10. ... ok
Long a 100, stop 99, prima vendita eseguibile a 97,50 dopo il salto, budget 1, costi nulli: S = −2,50 R. ... ok
999 coppie (0,40; 1) e una con K = 1 e S mancante: non decidibile per dati inidonei. Sostituirla con zero ... ok
test_d_minimo_trade (brain.laboratorio.tests.test_prova_generale_dgs12.TestDatiEMinimi) ... ok
test_e_minimo_sedute_attive (brain.laboratorio.tests.test_prova_generale_dgs12.TestDatiEMinimi) ... ok
test_k_intervallo_degenere (brain.laboratorio.tests.test_prova_generale_dgs12.TestPercorsiCompleti) ... ok
Riferimento indipendente del DGS (CPython 3.12, random.Random(314159), 100 randrange(1000) per replica, ... ok
Stesso intervallo, un requisito vincolante per promuovere indeterminato: non decidibile. ... ok
test_n_bocciatura_da_coppie (brain.laboratorio.tests.test_prova_generale_dgs12.TestPercorsiCompleti) ... ok
Con l'operatore ≥ scritto nella formula di D-36 (lettura da far chiarire al titolare): ammessa, esclusa, ... ok
test_f_uguaglianza_di_l (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie) ... ok
test_g_uguaglianza_di_u (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie) ... ok
test_l_confine_d44 (brain.laboratorio.tests.test_prova_generale_dgs12.TestSoglie) ... ok
Primo blocco 250 × (−0,50; 1), poi 750 × (1; 1). Media totale +0,625 R, segnale favorevole (estremi ... ok
test_i_veto_valido_con_minimi_globali_mancanti (brain.laboratorio.tests.test_prova_generale_dgs12.TestVeti) ... ok
Come I, ma il risultato del centesimo trade è ignoto: 99 esiti noti, veto non accertato, non decidibile. ... ok
DGS-12 §3: un blocco completo può bocciare anche se manca un'osservazione in un altro blocco. ... ok
Ran 17 tests in 0.904s
OK
```

## Rapporti finali tipizzati (Python 3.13)

### M (percorso completo, seme 314159, con un indicatore descrittivo fallito)

```
VERDETTO D-31 · promossa · causa: L > +0,20 R e requisiti superati
- sedute: 1000 sedute [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- trade: 1000 trade [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- sedute con trade: 1000 sedute [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- media del campione: 0.5000 R a trade [DERIVATO] · incertezza: esatto (sul campione) · fonte: somma di S / somma di K
- prove nel registro (N): 1 prove [MISURA] · incertezza: esatto · fonte: registro_prove.json, sha256 cdcdcdcdcdcdcdcd…
- soglie del metro: [0.2000; 0.1000] R a trade [REGOLA] · incertezza: esatto · fonte: D-31 (Δ = 0,05 R attorno a +0,15 R)
- quota: 0.0250 per coda [REGOLA] · incertezza: esatto · fonte: D-31, D-38
- vantaggio della strategia: [0.4748; 0.5245] R a trade [STIMA] · incertezza: intervallo bootstrap basic, 2,5% per coda, blocchi da 10, B = 3999, seme 314159; valido nel dominio del collaudo IA-02 · fonte: pilota_ia02 sha256 717e55996b23a495…
- segnale del solo metro: favorevole
- requisito drawdown descrittivo [descrittivo, non cambia l'esito]: fallito
Esito della regola, non una raccomandazione a operare: la decisione resta del titolare (D-14).
```

### N (percorso completo, seme 314159)

```
VERDETTO D-31 · bocciata · causa: statistica: U < +0,10 R
- sedute: 1000 sedute [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- trade: 1000 trade [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- sedute con trade: 1000 sedute [MISURA] · incertezza: esatto · fonte: coppie giornaliere della prova
- media del campione: 0.0000 R a trade [DERIVATO] · incertezza: esatto (sul campione) · fonte: somma di S / somma di K
- prove nel registro (N): — prove [MISURA] · incertezza: NON FORNITO · fonte: nessun registro fornito
- soglie del metro: [0.2000; 0.1000] R a trade [REGOLA] · incertezza: esatto · fonte: D-31 (Δ = 0,05 R attorno a +0,15 R)
- quota: 0.0250 per coda [REGOLA] · incertezza: esatto · fonte: D-31, D-38
- vantaggio della strategia: [-0.0253; 0.0245] R a trade [STIMA] · incertezza: intervallo bootstrap basic, 2,5% per coda, blocchi da 10, B = 3999, seme 314159; valido nel dominio del collaudo IA-02 · fonte: pilota_ia02 sha256 717e55996b23a495…
- segnale del solo metro: sfavorevole
Esito della regola, non una raccomandazione a operare: la decisione resta del titolare (D-14).
```
