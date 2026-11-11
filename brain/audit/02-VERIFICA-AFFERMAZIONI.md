# 2 · Verifica delle affermazioni del manuale v1

Data: 11/11/2026. Metodo: ricerca web delle fonti primarie (abstract, pagine istituzionali) + ricalcolo esatto dei numeri con `strumenti/verifica_m0.py`.
Legenda esito: ✅ confermato · ⚠️ impreciso o da qualificare · ❌ errato · ❓ non verificabile ora.
Stato fonte: V / V-sec / C / X (vedi `governance/STANDARD.md` §3).

> Le correzioni **non** sono state applicate all'artifact originale. Sono elencate qui e verranno integrate nella v2 della lezione corrispondente, con nota di modifica.

## A. Citazioni e dati empirici

| # | Lezione v1 | Affermazione | Esito | Cosa dice la fonte | Stato |
|---|---|---|---|---|---|
| A1 | 0.1 | Barber, Lee, Liu, Odean (2014): < 1% dei day trader di Taiwan batte il mercato netto di costi in modo affidabile; top 500 +37,9 bps/giorno, peggiori −28,9 | ✅ con nota | *J. Financial Markets* 18, 2014, pp. 1–24. "< 1%" è nel testo pubblicato. I valori 61,3 (lordo) / **37,9 (netto)** bps/giorno per i top 500 e −28,9 per i peggiori vengono dall'abstract del working paper. Specificare: **netti di commissioni, nell'anno successivo al ranking**. | V-sec |
| A2 | 0.1 | Chague, De-Losso, Giovannetti (2020): 97% dei persistenti oltre 300 giorni ha perso; 1,1% sopra il salario minimo; nessun apprendimento | ✅ con nota | Corretto. Precisare che riguarda **1.551 persone su 19.646** che hanno iniziato (7,9%): il 97% è sul sottogruppo dei persistenti. Working paper SSRN (rev. 2020), non articolo su rivista. | V-sec |
| A3 | 0.1 | Barber, Odean (2000): il quintile più attivo sottoperforma di ~6,5% l'anno | ✅ | Coerente con quanto noto; nel paper la causa principale sono i **costi di negoziazione**. "Cattivo timing" va attenuato. | C |
| A4 | 0.1 | ESMA: 70–80% dei conti CFD retail perde | ⚠️ | La comunicazione ESMA del marzo 2018 riporta **74–89%** dei conti, con perdita media 1.600–29.000 € per cliente. Le avvertenze attuali dei singoli broker hanno percentuali proprie, che cambiano nel tempo. Correggere in "74–89% (ESMA, 2018)". | V |
| A5 | 0.3 | Hou, Xue, Zhang (2020): 452 anomalie; 65% non supera \|t\| > 1,96; 82% fallisce con \|t\| > 2,78 | ✅ | *Review of Financial Studies* 33(5), 2020, pp. 2019–2133. Precisare il setup: **breakpoint NYSE e rendimenti value-weighted** (per neutralizzare le microcap). | V-sec |
| A6 | 0.3 | Harvey, Liu, Zhu (2016): 316 fattori; 27–53% false scoperte; proposta t > 3 | ⚠️ | *RFS* 29(1), 2016, pp. 5–68. Confermati 316 fattori e soglia **t > 3,0**. L'intervallo "27–53%" **non è stato trovato** nelle fonti consultate: rimuoverlo o verificarlo sul testo. | V-sec / X per 27–53% |
| A7 | 0.3 | McLean, Pontiff (2016): "calano del 26% rispetto all'in-sample, e del 58% rispetto al periodo pre-pubblicazione fuori campione" | ❌ | *Journal of Finance* 71(1), 2016, 97 predittori. Abstract: i rendimenti sono **26% più bassi fuori campione (prima della pubblicazione)** e **58% più bassi dopo la pubblicazione**, entrambi rispetto all'in-sample. La differenza (≈ 32%) è attribuita al trading informato dalla pubblicazione; il 26% è un **limite superiore** dell'effetto data mining. Rendimenti mensili medi: 0,582% in-sample → 0,402% OOS → 0,264% post-pubblicazione. | V-sec |
| A8 | 0.3 | Hurst, Ooi, Pedersen (2017): un secolo, 67 mercati | ✅ | *Journal of Portfolio Management*, 2017; 67 mercati (29 commodity, 11 indici, 15 bond, 12 valute), dal 1880. Fonte F5 (autori AQR): **conflitto d'interesse da dichiarare**. | V-sec |
| A9 | 0.3 | Quality: "Novy-Marx (2013), fattore RMW" | ❌ | Novy-Marx (2013, *JFE*) introduce la **gross profitability**. Il fattore **RMW** è di **Fama e French (2015)**, five-factor model, con una misura diversa (operating profitability). Correggere separando le due fonti. | V-sec |
| A10 | 0.3 | Frazzini, Pedersen (2014) low-vol/BAB; Koijen et al. (2018) carry; Jegadeesh-Titman (1993) | ✅ | Citazioni corrette (riviste: *JFE* 2014; *JFE* 2018; *JF* 1993). | C |
| A11 | 0.3 | Grossman-Stiglitz (1980); Lo, *Adaptive Markets* (2017) | ✅ | Corretto. Aggiungere Lo (2004, *JPM*) come fonte originale dell'Adaptive Markets Hypothesis. | C |
| A12 | 0.4 | Venkatraman et al. (2011): "anche una sola notte scarsa" sposta da difesa delle perdite a ricerca dei guadagni | ⚠️ | *J. Neuroscience* 31(10):3712–3718. Lo studio è su **una notte di privazione totale di sonno**, 29 giovani adulti. "Notte scarsa" è un'estensione non testata: riformulare. Effetto non replicato in modo esteso (E3). | V-sec |
| A13 | 0.4 | Kahneman-Tversky (1979, 1992): λ ≈ 2,25 | ⚠️ | λ = 2,25 è la stima mediana di **Tversky e Kahneman (1992)**, non del 1979. Studi successivi trovano stime molto variabili (alcune vicine a 1): indicare E2 con dibattito. | C |
| A14 | 0.4 | Testosterone sale dopo serie di vincite ("winner effect", Coates) | ⚠️ | Coates e Herbert (2008, *PNAS*) misurano su ~17 trader di Londra che il testosterone mattutino **predice** il P/L della giornata; il "winner effect" sui trader è un'**ipotesi** dell'autore, ricavata anche da studi animali. Livello E3/E4. | C |
| A15 | 1.1 | Volmageddon: "in due ore il VIX sale del 115%"; "XIV perde il 96% in una seduta" | ⚠️ | Il +115% del VIX è **close-to-close** del 5/2/2018 (≈ 17 → 37). Per XIV le fonti divergono: −84% nella giornata (BIS), −90/−96% del valore indicativo **after-hours**; terminato da Credit Suisse il 6/2 per "acceleration event". Riformulare: "il VIX chiude a +115%; il valore indicativo di XIV crolla oltre l'80–90% tra seduta e after-hours". | V-sec (SEC, BIS) |
| A16 | 1.2 | Fiscalità cripto: 33% dal 2026 | ✅ con nota | Aumento dal 26% al 33% per le plusvalenze realizzate dal 1/1/2026 (L. 207/2024; alcune fonti citano conferme nella L. 199/2025). Stablecoin in euro conformi MiCAR: 26%. **Da confermare su fonte ufficiale** (Agenzia delle Entrate / Gazzetta Ufficiale). Dal 2026 è operativa la DAC8. | V-sec (fonti secondarie) |
| A17 | 1.2 | ETF: guadagni = redditi di capitale; minus = redditi diversi | ✅ | Coerente con la normativa nota; manca data e fonte (TUIR artt. 44, 67): aggiungere. | C |
| A18 | 1.1 | Sessione cash USA alle 15:30 italiane | ⚠️ | Vero per gran parte dell'anno; per ~2–3 settimane in marzo e ~1 settimana tra fine ottobre e inizio novembre (cambio d'ora sfasato USA/UE) l'apertura è alle **14:30**. | C |

## B. Numeri e formule (ricalcolo esatto)

Eseguito `python3 strumenti/verifica_m0.py` il 11/11/2026.

| # | Lezione | Affermazione | Esito | Valore esatto |
|---|---|---|---|---|
| B1 | 0.13 | Strisce di perdite in 100 trade (tabella da simulazione) | ✅ | 50%/6 → 0,546 · 50%/8 → 0,170 · 40%/6 → 0,873 · 40%/8 → 0,490 · 40%/10 → 0,205 · 33%/10 → 0,449 |
| B2 | 0.13 | Recupero = 1/(1−perdita) − 1 | ✅ | — |
| B3 | 0.14 | Sistema A: σ ≈ 1,47R; t = 0,75 / 1,36 / 2,36 con 30 / 100 / 300 trade | ✅ | Aggiunta utile: servono **≈ 216 trade per t = 2** e **≈ 486 per t = 3** |
| B4 | 0.14 | Errore sul win rate ≈ ±1/√N (95%, p ≈ 0,5) | ✅ | 1,96 × 0,5/√N ≈ 0,98/√N |
| B5 | 0.15 | Gioco di Peters: 1,05 vs √0,9 ≈ 0,949 | ✅ | 1,050 / 0,9487 |
| B6 | 0.15 | Geometrico ≈ aritmetico − σ²/2 | ✅ | Approssimazione valida per rendimenti piccoli |
| B7 | 1.2 | 100 € a 10 anni: 67,6 → 61,4 (−9%) | ✅ | 67,56 → 61,39 (−9,1%) |
| B8 | 1.4 | Contango 80 → 81: ~1,2% al mese | ✅ | 1,25% |
| B9 | 1.7 | ETF 2×: 100 → 120 → 98,2 | ✅ | 98,18 |
| B10 | 1.8 | ES 50 $/pt, MES 5 $, NQ 20 $, MNQ 2 $ | ✅ | Specifiche CME note (verificare su CME prima dell'uso operativo) |
| B11 | 1.18 | Spread effettivo 4, realizzato 1, selezione avversa 3 | ✅ | Coerente con le definizioni standard |

## C. Affermazioni da qualificare (non errate, ma oltre l'evidenza)

| # | Lezione | Affermazione | Problema | Proposta |
|---|---|---|---|---|
| C1 | 0.13 | "Con rischio ≤ 1% per trade ed edge positivo, la rovina è praticamente esclusa" | Vero per la rovina **totale** con trade indipendenti e edge **noto**; falso se l'edge è stimato male, se c'è correlazione tra trade o gap oltre lo stop | Definire "rovina" (es. −50%) e calcolare il rischio di rovina con incertezza sull'edge |
| C2 | 1.9 | "Comprare opzioni con IV bassa, venderle con IV alta" | Conta il confronto IV vs **volatilità realizzata futura** e il variance risk premium, non il livello assoluto | Rimandare al Modulo 10 (volatilità) |
| C3 | 1.17 | Multi-timeframe: "meno falsi segnali" | Plausibile, nessuna evidenza citata | Marcare E5 e trasformarlo in ipotesi testabile (Modulo 8) |
| C4 | 0.23 | Fondo d'emergenza 6–12 mesi, capitale di rischio 5–10% | Convenzioni di finanza personale | Marcare E5 |
| C5 | 0.17 | Tabella statistiche 2016–2026 "dal vault" | Non riproducibile senza dati e script; due anomalie da chiarire (Q8 range = dev. std per Bitcoin; Q9 strumento di S10) | Specifica dei dati e script pronti: `dati/RICHIESTA-DATI-0.17.md`, `strumenti/riproduci_017.py` (in attesa dei dati del vault) |
| C6 | 0.19 | Ruoli di amigdala, insula, dopamina "nel trading" | Semplificazioni divulgative di risultati di laboratorio | Aggiungere livelli di evidenza e la distinzione neuroscienze vs divulgazione (Area P) |

## Sintesi

- **2 errori** da correggere (A7 McLean-Pontiff, A9 Novy-Marx/RMW).
- **8 imprecisioni** da qualificare (A4, A6, A12, A13, A14, A15, A18, più la nota su A3).
- **Tutti i numeri ricalcolati sono corretti** (B1–B11).
- **6 affermazioni** da etichettare con un livello di evidenza (C1–C6).

Sources consultate in questa verifica: vedi `bibliografia/BIBLIOGRAFIA.md`, sezione "Fonti verificate il 11/11/2026".
