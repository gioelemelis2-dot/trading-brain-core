# Attribuzione delle prove già dichiarate (DGS-15, punto 1) · 22/11/2026

Ogni risultato è legato al commit che l'ha prodotto, alla versione di test e script e all'ambiente Python. I log sono in `log/`.
- **[ESEGUITO]**: rieseguito oggi, con il log.
- **[EVIDENZA PRECEDENTE]**: log o ricevuta salvati quando la corsa è stata fatta.
- **[ATTESTATO]**: solo dichiarato nei messaggi, senza log conservato.

Ambienti usati:
- Python 3.13.18 e Python 3.9.25, nel contenitore di Claude (Linux);
- Python 3.9.6 di Apple, sul Mac, per le corse di Gemini.

## 1. Prova generale: 17/17

| Elemento | Valore |
|---|---|
| Codice eseguito | `f5d0cad`. Modulo `verdetto_d31.py` dopo #122, #123 (`f0ee358`) e #131–#134 (`f338381`). SHA-256 del modulo `29ea3eb4…8403`; pilota `717e5599…b0ee` |
| Test | `brain/laboratorio/tests/test_prova_generale_dgs12.py` allo stesso commit |
| Ambienti | 3.13.18 e 3.9.25 |
| Ricevuta | `brain/collaborazione/da-claude/RICEVUTA-PROVA-GENERALE-20261121.md`: esito per caso sulle due versioni e rapporti finali di M e N. **[EVIDENZA PRECEDENTE]** |
| Dopo #124 | Il modulo è cambiato (`math.fsum`, `36d533a`). La suite della prova generale è di nuovo verde su `dfe0227` (`log/att_suite313_dfe0227.log`, `log/att_suite39_dfe0227.log`). **[ESEGUITO]** |

**Quale percorso ha attraversato ciascun caso:**

| Casi | Ingresso | Che cosa provano |
|---|---|---|
| A, B | Simulatore `orb_londra.simula` → coppie → `verdetto` | La contabilità del simulatore (costi, perdita oltre lo stop) arriva fino al verdetto. **Non** passano dall'esecutore ordinario. |
| C, D, E, I, J, K, M, N | Coppie inventate → `intervallo` del pilota collaudato → `verdetto` | Dati inidonei, minimi, veti, intervallo degenere; M e N coincidono con il riferimento indipendente di DGS-12. |
| F, G, H, L, O e la seconda parte di M | Intervallo o potenza forniti direttamente al decisore (`segnale`, `verdetto` con l'intervallo simulato) o al filtro (`screening`) | Priorità, uguaglianze alle soglie (F, G), confine di D-44 (L), potenza esattamente al 50% (O, ora D-47). |

Il percorso **intero** (scheda → esecutore ordinario → riserva → verdetto → rapporto) è nella ricevuta di #127: `../2026-11-22-percorso-127/`.

## 2. Mutanti del perimetro: 314/314

| Elemento | Valore |
|---|---|
| Codice e test | `6ce6388` (correzione di #136: solo test e script dei mutanti); il codice del perimetro è quello di `f338381`. `fc79f5b` cambia solo il registro delle modifiche. |
| Script | `brain/laboratorio/tests/mutazioni_esecuzione.py` a `6ce6388`: 314 mutanti |
| 3.13.18 | 314/314 in una corsa: `log/mutanti_esecuzione_6ce6388_py313.log` **[EVIDENZA PRECEDENTE]** |
| 3.9.25 | Corsa intera fermata al limite di 2 ore dopo 51 mutanti (`log/mutanti_esecuzione_6ce6388_py39_interrotta_limite_2h.log`). Rifatta in due parti per prefisso: A con N, K, V, E, S, TA, 169/169; B con C, IX, MG, MR, R, P, Q, 145/145 (`..._parteA.log`, `..._parteB.log`). 169 + 145 = 314. **[EVIDENZA PRECEDENTE]** |
| Prima della correzione | 311/314 su 3.13 (`log/mutanti_esecuzione_8f175b6_py313_prima_di_136.log`). Vivi C01 e C08; V10 non si applicava. |
| Dopo | I test del periodo sono stati riscritti partendo da casi validi (`84dcb59`). C01–C09: 9/9 su 3.13 e 3.9 (`log/mutanti_C0x_84dcb59_py313_py39.log`) **[EVIDENZA PRECEDENTE]**. Gli altri 305 mutanti non sono stati rieseguiti con questi test: il 314/314 resta attribuito a `6ce6388`. |
| Dopo #127 | Il perimetro è cambiato: caricatore, riserva, manifesto, esecutore ordinario. **Serve una corsa completa nuova sul candidato di R19.** I mutanti nuovi del percorso sono a parte (§ ricevuta di #127). |

## 3. R18: quali evidenze appartengono a quale versione

| Evidenza | Versione |
|---|---|
| Tutto il rapporto R18 di Gemini, compreso il primo giro del modulo del verdetto | Punta `efcfcbc`; perimetro identico a `e476a9a`; **prima** di #122, #123 (`f0ee358`) e delle correzioni R18 (`f338381`) |
| R18-01 (copia parziale) riprodotto da Claude | Codice del perimetro identico a `e476a9a` |
| R18-07, R18-08, R18-09 riprodotti da Claude | Modulo **dopo** `f0ee358`: erano ancora presenti |
| Correzioni | Test rossi `e72af87`, codice `f338381`, mutanti `8f175b6` |
| Riesecuzioni dopo le correzioni | 27/27 suite su 3.13 e 3.9 **[ATTESTATO]**: il log di quella corsa non è stato salvato. Mutanti del verdetto 117/118 su 3.13 e 3.9 (`log/mutanti_verdetto_8f175b6_py313_py39.log`) **[EVIDENZA PRECEDENTE]**. Q01–Q11 11/11 **[ATTESTATO]**, poi compresi nel 314/314 di `6ce6388`. |
| Stato attuale | Suite complete verdi su 3.13.18 e 3.9.25, e mutanti del verdetto 124/125 (VD13 equivalente), nella copia bloccata su `dfe0227` (`log/att_*_dfe0227.log`) **[ESEGUITO]** |

## 4. #136: caso valido e stesso caso con il solo periodo sbagliato

Script `dimostra_136.py`; uscita in `log/dimostra_136.log`, su 3.13.18 e 3.9.25 **[ESEGUITO]**. Precondizioni: cartelle BID e ASK distinte, ASK diverso dal BID, sigillo valido.

| Caso | Esito osservato |
|---|---|
| A1: sviluppo dal 15/11/2023 | accettato |
| A2: sviluppo dal 14/11/2023 (cambia solo l'inizio) | rifiutato: «sviluppo dal 2023-11-15 in poi: 2023-11-14 è nel periodo sigillato (DA-26)» |
| B1: verifica fino al 31/10/2023 | accettato |
| B2: verifica fino al 01/11/2023 (cambia solo la fine) | rifiutato: «la verifica finisce il 2023-10-31 (poi embargo e sviluppo): 2023-11-01 è oltre» |
| C1: sviluppo il 02/01/2024 | accettato |
| C2: 03/01 → 02/01/2024 (cambia solo l'ordine) | rifiutato: «periodo vuoto: 2024-01-03 → 2024-01-02» |

## 5. V10: sostituito, non riclassificato

- **Prima:** V10 («quota non controllata») toglieva la riga `if abs(float(e.get("alfa_j", -1)) - quota(...)) > 1e-15:`.
- **Perché è cambiato:** la correzione di #128 (`f338381`) ha riscritto quella condizione in tre controlli (tipo float, valore finito, distanza dalla quota). La vecchia riga non esisteva più e lo script ha segnalato «la sostituzione compare 0 volte».
- **Dopo (`6ce6388`):** V10 toglie la sola distanza dalla quota (`abs(alfa - quota(...)) > 1e-15` diventa `False`) e lascia i controlli di tipo. Il difetto simulato è lo stesso: una quota sbagliata accettata.
- **Esito:** ucciso nella corsa mirata (`log/mutanti_V10_C0x_dopo_136_py313.log`, 10/10) e nel 314/314. Non è equivalente e non è stato riclassificato.
- La stessa classe di errore si è ripetuta il 22/11 con VD26, VD35 e VD72 dopo #124, ed è stata corretta allo stesso modo (`6f19065`).

## Che cosa resta solo attestato

- 27/27 suite dopo le correzioni di R18 (21/11): il log non è stato salvato. Lo sostituisce la corsa verde su `dfe0227`, che è successiva.
- Q01–Q11 11/11 come corsa separata: compresi nel 314/314 di `6ce6388`.
- Le esecuzioni di Gemini (R18, notte del 22/11) sono attestate dai suoi rapporti, con il commit di partenza dichiarato.
