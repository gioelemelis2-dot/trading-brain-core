# Revisione delle lezioni L2.4–L2.6 · registro delle verifiche

Codici: `A` = affermazione · `F` = formula · `E` = esempio numerico · `D` = domanda specifica di Claude.
Per ogni codice Gemini indica: ✅ confermato · ⚠️ impreciso · ❌ errato · ❓ non verificabile, con evidenza e stato della fonte (V / V-sec / C / X).

Le affermazioni sono riportate **come le ha scritte Claude**, con lo stato dichiarato nella lezione. Le priorità indicano dove un errore farebbe più danni.

---

## L2.4 · Tassi nominali, reali e inflazione attesa
File: `moduli/m02-macro/L2.4-tassi-reali-e-inflazione-attesa.md` · Script: `python3 strumenti/tassi_reali.py`

### Affermazioni
| Codice | Sezione | Affermazione | Stato dichiarato | Priorità |
|---|---|---|---|---|
| L2.4-A01 | §5.2 | I TIPS sono indicizzati al CPI-U con un ritardo di indicizzazione di circa tre mesi e hanno protezione dalla deflazione sul capitale a scadenza | C | alta |
| L2.4-A02 | §5.2 | BTP€i indicizzati all'HICP dell'area euro esclusi i tabacchi; BTP Italia al FOI esclusi i tabacchi | C | alta |
| L2.4-A03 | §5.3 | D'Amico-Kim-Wei: premio di liquidità dei TIPS fino a ~100 pb nei primi anni e fino a ~300 pb durante la crisi finanziaria, dovuto soprattutto alla minore liquidità | V-sec (abstract FEDS) | alta |
| L2.4-A04 | §5.3 | Il premio di liquidità degli indicizzati **riduce** il breakeven | deduzione dalla definizione | media |
| L2.4-A05 | §5.3 | Un crollo del breakeven in una crisi di liquidità può riflettere la fuga dagli indicizzati più che un crollo delle aspettative | `[IPOTESI]` | media |
| L2.4-A06 | §5.4 | Erb-Harvey (FAJ 2013): oro copertura inaffidabile dall'inflazione su orizzonti pratici; le spiegazioni popolari (tassi reali inclusi) spiegano poco delle oscillazioni di breve | V-sec (abstract NBER + articolo di stampa) | alta |
| L2.4-A07 | §6 | Equazione di Fisher attribuita a *The Theory of Interest* (1930) | C | bassa |
| L2.4-A08 | §9 | 2008: breakeven USA molto compressi, coerente con premio di liquidità elevato | C/V-sec | media |
| L2.4-A09 | §9 | Oro forte nel 2022–2024 nonostante tassi reali in salita; acquisti delle banche centrali come spiegazione proposta | `[IPOTESI]` (C) | media |

### Formule
| Codice | Formula | Da controllare |
|---|---|---|
| L2.4-F01 | (1+i) = (1+r)(1+π_e); r = (1+i)/(1+π_e) − 1 | Correttezza; condizioni d'uso dell'approssimazione |
| L2.4-F02 | BE = y_nom − y_reale | Stessa scadenza; convenzioni di rendimento |
| L2.4-F03 | BE = π_attesa + premio_rischio_inflazione − premio_liquidità | Segni; eventuali componenti mancanti (es. convessità, ritardo d'indicizzazione) |
| L2.4-F04 | P = D/(r_reale + premio − g_reale) | Coerenza con L2.3 |

### Esempi (riproducibili)
| Codice | Esempio | Risultato atteso dallo script |
|---|---|---|
| L2.4-E01 | i = 4,5%, π_e = 2,5% → r esatto | 1,951% |
| L2.4-E02 | i = 40%, π_e = 35% | 3,70% (approssimazione 5%) |
| L2.4-E03 | Breakeven 2,35% con premi 0,10/0,20 e 0,10/0,50 | 2,45% e 2,75% |
| L2.4-E04 | Gordon reale, premio 4%: growth 150 → 100; g=0: 60 → 50 | −33,3% e −16,7% |
| L2.4-E05 | Esercizi 1–3 | 1,923%; 2,30%; −25% e −14,3% |

### Domande specifiche
- L2.4-D01: la scomposizione del breakeven (F03) è completa per un lettore del Brain o manca una componente importante?
- L2.4-D02: esiste letteratura peer-reviewed più recente e più solida di Erb-Harvey sul legame oro–tassi reali?

---

## L2.5 · Bilancio della banca centrale: QE, QT, riserve
File: `moduli/m02-macro/L2.5-bilancio-banca-centrale-qe-qt.md`

### Affermazioni
| Codice | Sezione | Affermazione | Stato dichiarato | Priorità |
|---|---|---|---|---|
| L2.5-A01 | §5.1 | Riserve possono calare senza decisioni di policy se crescono il conto del Tesoro (TGA) o l'ON RRP | C (meccanica di bilancio) | alta |
| L2.5-A02 | §5.3 | Gagnon et al. (IJCB 7(1) 2011, 3–43): riduzioni significative e durature dei tassi lunghi, soprattutto via premi per il rischio incluso il premio a termine | V-sec (abstract) | alta |
| L2.5-A03 | §5.3 | Negli 8 annunci principali: 10 anni −91 pb, premio a termine −71 pb | V-sec **indiretta** (citazione in Bauer-Rudebusch) | alta |
| L2.5-A04 | §5.3 | Esiste un canale di segnale (Bauer-Rudebusch) | C | media |
| L2.5-A05 | §5.4 | Fed: fine del runoff dal 1/12/2025, deciso il 29/10/2025; acquisti di gestione delle riserve in T-bill annunciati a dicembre 2025 | V-sec | alta |
| L2.5-A06 | §5.5 | 10 anni USA: 1,66% il 2/5/2013; 2,03% il 22/5/2013 | V-sec (tabella Fed) | alta |
| L2.5-A07 | §5.5 | Circa 3% all'inizio di settembre 2013 | in verifica (fonti 2,96–3,01%) | media |
| L2.5-A08 | §5.6 | BCE: APP dal 2015, PEPP 2020, TPI 2022 | C | media |
| L2.5-A09 | §6 | Neutralità del QE nel modello senza frizioni (Wallace) | C | bassa |
| L2.5-A10 | §13 | Effetti decrescenti dei programmi successivi | C, E3 | media |
| L2.5-A11 | §9 | Settembre 2019: tensione sui repo con riserve scarse localmente | C | media |

### Formule ed esempi
| Codice | Contenuto | Atteso |
|---|---|---|
| L2.5-F01 | y(10a) = media tassi brevi attesi + premio a termine | Correttezza concettuale |
| L2.5-F02 | Identità semplificata delle riserve (passivo) | Voci mancanti? |
| L2.5-E01 | Scritture contabili di un acquisto di 100 | Coerenza a partita doppia |
| L2.5-E02 | 3,0% + 0,8% → 2,9% + 0,3% | 3,2% (−60 pb) |
| L2.5-E03 | Riserve 3.000 − 200 − 100 | 2.700 |
| L2.5-E04 | Duration estratta 600 × 6 | 3.600 "miliardi-anno" |
| L2.5-E05 | Esercizio 1 (QT e conto del Tesoro) | Spiegazione nel testo |
| L2.5-E06 | Esercizi 2–3 | 3,5%; 3.400 |

### Domande specifiche
- L2.5-D01: i numeri −91/−71 pb sono quelli del paper originale (tabelle) o di una versione diversa?
- L2.5-D02: lo schema di bilancio (§5.1) omette voci che contano per un lettore che vuole capire le riserve?
- L2.5-D03: importi e struttura degli acquisti di gestione delle riserve di dicembre 2025 (domanda aperta Q12).

---

## L2.6 · Fed, BCE, BoJ, BoE
File: `moduli/m02-macro/L2.6-fed-bce-boj-boe.md`

### Affermazioni
| Codice | Sezione | Affermazione | Stato dichiarato | Priorità |
|---|---|---|---|---|
| L2.6-A01 | §5.1 | Obiettivi: Fed 2% PCE; BCE 2% HICP simmetrico medio periodo; BoJ 2% CPI (gen. 2013); BoE 2% CPI fissato dal governo | V-sec | alta |
| L2.6-A02 | §5.1 | FOMC 12 votanti (7 governatori + NY + 4 a rotazione) | C | media |
| L2.6-A03 | §5.1 | Consiglio direttivo BCE: 6 membri del Comitato esecutivo + governatori nazionali con rotazione dei voti | C | media |
| L2.6-A04 | §5.1 | Policy Board BoJ: 9 membri | C | bassa |
| L2.6-A05 | §5.1 | MPC: 9 membri, 5 interni e 4 esterni | V-sec | bassa |
| L2.6-A06 | §5.1 | Circa otto riunioni di politica monetaria l'anno per ciascuna | C | media |
| L2.6-A07 | §5.2 | Il CPI USA tende storicamente a essere più alto del PCE; l'HICP esclude le abitazioni occupate dai proprietari | C | media |
| L2.6-A08 | §5.3 | BoJ: dichiarazione congiunta 22/01/2013 con due dissenzienti; tassi negativi gen. 2016; YCC set. 2016 (10a ~0%); 19/03/2024 tasso 0–0,1%, fine YCC e acquisti ETF, voto 7–2 | V-sec | alta |
| L2.6-A09 | §5.3 | BCE: DFR negativo 2014–2022; TPI 2022 | C | media |
| L2.6-A10 | §5.3 | BoE febbraio 2026: Bank Rate 3,75%, voto 5–4 (4 per 3,5%) | V-sec | media |
| L2.6-A11 | §5.4 | Agosto 2024: chiusura del carry sullo yen; settembre–ottobre 2022: crisi LDI con intervento sui gilt | C | media |
| L2.6-A12 | §14 | Brunnermeier-Nagel-Pedersen (2008) "Carry trades and currency crashes" | C | bassa |

### Esempi
| Codice | Esempio | Atteso |
|---|---|---|
| L2.6-E01 | Differenziale atteso 1,4% → 1,6% | +20 pb |
| L2.6-E02 | Carry 4% e apprezzamento del 10% | ≈ 2,5 anni di carry |
| L2.6-E03 | Esercizi 2–3 | 1,35%; ≈ 1,5% |

### Domande specifiche
- L2.6-D01: la scheda comparativa ha errori di fatto o omissioni importanti (es. obiettivi secondari, strumenti specifici)?
- L2.6-D02: membri dell'area euro e composizione del Consiglio direttivo alla data della revisione.

---

## Controlli trasversali sulle tre lezioni
| Codice | Controllo |
|---|---|
| X01 | Le 20 sezioni del modello sono presenti e sostanziali |
| X02 | Ogni numero ha un'etichetta di classe (`[ESEMPIO]`, `[IN VERIFICA]`…) coerente con STANDARD §8 |
| X03 | Nessuna fonte dichiarata V senza essere stata letta (in queste lezioni nessuna è dichiarata V) |
| X04 | Esercizi con soluzione corretta |
| X05 | Obiettivi di apprendimento verificabili dalla checklist e dal cancello dell'unità |
| X06 | Duplicazioni o contraddizioni con L2.1–L2.3 o con il manuale v1 |
