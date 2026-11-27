# Prova D2 · osservazioni, in ordine di arrivo · 27/11/2026

Le previsioni stanno in `PIANO-ORDINI-D2-20261127.md`, commit `57d2e2e` (16:00 UTC). Qui solo ciò che è stato osservato dopo, con l'ora e la fonte. Le foto originali le conserva il titolare; nel repository non vanno il nome né i numeri di conto.

## Ordine «S1»: vendita aperta FUORI dal piano

**Fonte:** foto della scheda Trade, ricevuta alle 16:2x UTC.

- **Ordine:** sell 0,01 xauusd.cy, alle **18:21 ora del server**, cioè 17:21 in Italia e 16:21 UTC. Il server risulta quindi a UTC+2: è una deduzione, da confermare.
- **Prezzi:** apertura **3.621,35**; **S/L 3.657,86**, cioè **+36,51** sopra l'apertura; T/P nessuno; prezzo corrente 3.622,19.
- **Conto:** saldo 100.000,00, equità 99.999,16, **margine 181,07**, margine libero 99.818,09, profitto −0,84.

**Scostamento dal piano.** Il piano prevedeva come primo ordine O1: **acquisto** con stop a −2,00. La vendita di O2 aveva lo stop a +3,00. Quest'ordine è una vendita con lo stop a +36,51: **non corrisponde a nessun ordine del piano**. Lo registro come **S1, fuori piano**. **Chi l'ha aperto:** il titolare, a mano, «secondo una mia idea» (sua risposta delle 16:3x UTC), non Claude chat. **Concausa di Claude:** in chat avevo scritto che le operazioni si potevano fare «a caso», intendendo il momento dell'ingresso, e subito dopo una tabella di parametri da rispettare esattamente. Il messaggio era ambiguo.

| Voce | Previsione congelata | Osservato | Scarto | Esito provvisorio |
|---|---|---|---|---|
| P&L lordo al prezzo corrente (formula congelata, con il segno della vendita) | (3.621,35 − 3.622,19) × 100 × 0,01 = **−0,84** | **−0,84** | 0,00 | concorde (T = 1u) |
| Margine (formula esterna congelata: apertura × 100 × 0,01 × 5%) | 3.621,35 × 0,05 = **181,07** | **181,07** | 0,00 | concorde (T = 1u); **non è una previsione del Guardian** |
| Commissione all'apertura (H-a: 0,06) | 0,06 | **0,00 finora**: equità = saldo + profitto, al centesimo (100.000 − 0,84 = 99.999,16) | −0,06 | **H-a non confermata all'apertura.** Da rivedere alla chiusura, con lo Storico. Possibili spiegazioni da verificare: commissione addebitata solo alla chiusura (H-b/H-c), oppure conto **Standard** senza commissione (il cancello «Raw o Standard» non è ancora verificato) |
| Perdita lorda allo stop | non pre-registrata per 36,51; la formula congelata dà 36,51 | — | — | lo stop non è stato scritto prima: **non vale come previsione** |

## Errore di Claude, nel piano

Nel commit `57d2e2e` l'**esempio numerico** del margine è sbagliato di un fattore 10:
- «a 3.770,00 vale 18,85 USD»: il valore giusto è **188,50**;
- in chat ho scritto «circa 18,11 USD»: il valore giusto è **181,14**.

La **formula** congelata (apertura × 100 × 0,01 × 5%) era giusta, ed è quella che si confronta. Il numero detto al titolare era sbagliato e lo registro come tale.

## Chiusura di S1

**Fonte:** foto della scheda Storico e dell'orologio del Mac, ricevuta alle 16:3x UTC.

- Chiuso alle **18:33 ora del server**. Il Mac segna «Ven 27 nov 17:33» nella stessa foto: **server a UTC+2 confermato**.
- Prezzo di chiusura **3.625,00**; swap vuoto; profitto **−3,65**.
- Saldo **99.996,35**. Nel riepilogo: deposito 100.000,00, credito 0,00, prelievo 0,00.
- **Lo Storico mostra T/P 3.574,98.** Nella foto della scheda Trade delle 18:21 il T/P era vuoto: **il take profit è stato aggiunto dopo l'apertura**, ed è una modifica dell'ordine. Lo S/L è rimasto 3.657,86.

| Voce | Previsione congelata | Osservato | Scarto | Esito (D-60) |
|---|---|---|---|---|
| P&L lordo alla chiusura (formula congelata, con il segno della vendita) | (3.621,35 − 3.625,00) × 100 × 0,01 = **−3,65** | **−3,65** | 0,00 | **concorde** |
| Commissione totale (H-a: 0,06 all'apertura; alternative H-b 0,12 e H-c 0,06) | 0,06 | **0,00**: saldo = 100.000 − 3,65, al centesimo | −0,06 | **discordante** con la previsione congelata. **Spiegazione da verificare, registrata dopo l'osservazione:** il conto potrebbe essere **Standard** e non Raw, perché il cancello A2 non era stato verificato; oppure la demo non applica commissioni. Per D-60, una spiegazione trovata dopo non cambia l'esito |
| Margine (dall'osservazione all'apertura) | 181,07 | 181,07 | 0,00 | **concorde**. Formula esterna, **non del Guardian** |
| Perdita lorda allo stop | non pre-registrata (stop fuori piano) | stop non scattato | — | **non osservabile** su S1 |

**Stato della prova dopo S1:**
- concordi: la formula del P&L con il segno, all'apertura e alla chiusura, e il margine esterno;
- discordante: la commissione;
- da osservare: **la perdita allo stop (O1)**, cioè l'unica voce che il Guardian prevede davvero.
