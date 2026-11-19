# Riscontro di Claude a DGS-11 (controverifica dell'audit globale), 19/11/2026

**Fonte:** `collaborazione/da-chatgpt/DGS-20261119-11-controverifica-audit.md`. L'ho letta per intero, punto per punto. Ho rifatto i calcoli e ho ripetuto l'esempio avverso con il metodo adottato. **Questo riscontro non decide nulla:** le decisioni restano del titolare (§5).

## 1. I numeri del DGS: tutti confermati

| Valore | DGS | Ricalcolo di Claude |
|---|---|---|
| Errore standard (σ = 1,25, D = 1.000) | 0,03953 R | 0,039528 ✔ |
| Media osservata necessaria per L > 0,20 | 0,27748 R | 0,277474 ✔ |
| Potenza a 0,20 / 0,25 / 0,30 R | 2,50 / 24,35 / 71,56% | 2,50 / 24,35 / 71,56 ✔ |
| Potenza a +0,2667 R (2% al mese con 15 trade) | 39,23% | 39,23 ✔ |
| Nessuna perdita rara (q = 0,2%) su 1.000 e su 780 | 13,51% e 20,98% | ✔ |
| Limite superiore al 95% con 0 promozioni su 100 | 2,95% | 1 − 0,05^(1/100) = 2,95% ✔ |
| Repliche per scendere sotto il 2,5% | 119 | ln 0,05 / ln 0,975 = 118,3 → 119 ✔ |
| Repliche per ±10 punti a potenza 71,56% | 79 (97 nel caso peggiore) | 1,96²·p(1−p)/0,1² = 78,2 → 79 ✔ |
| Semilarghezza con 300 repliche | 5,10 punti | ✔ |

Non ho trovato errori di calcolo nel parere.

## 2. Errore mio confermato, e più grave di come lo descrive il DGS

**Il DGS (§2 e §8) chiede:**
- i conteggi incrociati dell'esempio avverso;
- il rifacimento con B = 3.999.

**Rifatto** (dati inventati, 300 repliche, B = 3.999, script `esempio_avverso_2.py` e `_3.py` nella cartella di lavoro di Claude):

| Generatore | Coda | Promosse per errore (media vera +0,15 R) | Repliche senza la perdita rara | Promosse E senza perdita |
|---|---|---|---|---|
| G1 dell'audit (vincite **tutte uguali**) | q = 1% | 4/300 | 0 | 0 |
| G1 dell'audit | q = 0,2% | **35/300** | 35 | **35** |
| G2 realistico (vincite con dispersione 1,2 R) | q = 1%, perdita −20 R | 7/300 | — | — |
| G2 realistico | q = 0,2%, perdita **−20 R** | **0/300** | 46 | 0 |
| G2 realistico | q = 0,2%, perdita **−50 R** | **15/300 (5%)** | 46 | 15 |

**Che cosa vuol dire:**
- **L'11,7% dell'audit è in gran parte un artefatto del mio generatore.**
  - Nel G1, quando la perdita rara non compare, tutte le 1.000 sedute hanno **lo stesso identico risultato**.
  - In aritmetica esatta l'intervallo avrebbe ampiezza nulla e sarebbe **invalido** (contratto DGS-06). Gli arrotondamenti dei numeri decimali gli danno invece un'ampiezza di circa 1e-13: passa il controllo e promuove.
- **Con vincite realistiche il meccanismo esiste, ma solo con code estreme.**
  - Con perdite rare di −20 R: nessuna falsa promozione su 300.
  - Con perdite di −50 R: 5%, tutte nelle repliche senza la perdita.
- **La conclusione dell'audit va corretta.** Il rischio n. 3 passa da «dimostrato sull'esempio» a **«plausibile solo per code di decine di R»**.
  - **Dove può contare davvero:** con stop molto stretti un salto di prezzo vale molti R. Per esempio, con uno stop di 2 USD un salto di 100 USD vale 50 R.

**Conseguenza per la clausola sulle code** (D-34, punto 3), in linea con il DGS (§2 e §6):
- uno stop **non garantisce** un tetto alla perdita (Investor.gov: in un salto lo stop si esegue al primo prezzo disponibile);
- un tetto universale restringerebbe le strategie;
- la clausola giusta è una **dichiarazione verificabile dell'esposizione**: il salto peggiore plausibile diviso la distanza dello stop, in R, con la fonte;
- un collaudo nuovo serve solo se quell'esposizione esce dal dominio provato.

Serve una decisione del titolare: §5 (b).

**Rilievo tecnico nuovo: difetto #119, aperto.**
- Dati quasi costanti producono intervalli di ampiezza circa 1e-13 che superano il controllo «ampiezza nulla», solo per l'arrotondamento.
- Il pilota è congelato: non si tocca.
- Nel modulo del verdetto si può aggiungere una regola, per esempio «ampiezza < 1e-9 R ⇒ invalido». È una precisazione del contratto: la propongo, non la applico senza decisione (§5 c).

## 3. L'errore più importante dell'audit, secondo il DGS: lo accetto

**Il rilievo (DGS-11 §8).** Ho giudicato la **macchina intera** con le proprietà di **un solo criterio**. Due casi:
- l'esempio avverso diceva «tutti i controlli passano», ma ho provato solo il metro, senza veti, drawdown e screening;
- la potenza gaussiana l'ho presentata come riferimento del verdetto completo.

**Correzione per la prova generale a vuoto.** Per ogni percorso sintetico si registrano:
- la verità economica;
- il risultato atteso, calcolato **da chi non ha scritto l'esecutore**;
- l'uscita di ogni stadio;
- il verdetto consegnato.

Vanno distinti i percorsi avviati da quelli arrivati alla verifica.

## 4. Gli altri punti del DGS

| Punto del DGS | Lo accetto? | Che cosa cambia |
|---|---|---|
| §6. Modulo separato: verificare a parte il modulo, il collegamento, il rifiuto di una versione errata o assente e il verdetto composto | Sì | Fatto: il rifiuto di una versione errata del metro (impronta). Da fare: il collegamento con l'esecutore e il rifiuto del modulo assente |
| §6. Il registro N deve alimentare il calcolo e comparire nel rapporto | Sì | Requisito del registro unico (elenco D-34, punto 2) |
| §6. Copertura BID/ASK, costi, capienza e permesso della riserva sono prerequisiti della verifica vera | Sì | Già nella catena; la capienza è il punto 9, che il DGS non ha ricevuto (§6 di questo riscontro) |
| §7. Prova a vuoto divisa in casi a risposta esatta (calcolati a mano da un terzo) e frequenze su scenari con regola d'accettazione congelata; confine +0,15 R incluso | Sì | **I casi a risposta esatta li prepara Gemini o il DGS, non Claude.** Le frequenze: almeno 300 repliche per scenario (±5 punti) e 119 o più per i falsi positivi |
| §7. Il 71,56% non è il riferimento della catena con i veti | Sì | Il riferimento della catena si ricava dalla catena, con le regole scritte prima |
| §5. Il test di Wald «0 contro +0,10 R» risponde a una domanda diversa da IA-02 | Sì | Le ipotesi della demo vanno riallineate a IA-02 quando si deciderà DA-29 |
| §5. Nuove opzioni: un protocollo da zero per l'effetto minimo utile; oppure tenere il metro e archiviare «non decidibile» senza spendere riserva | Sì | Aggiunte alla decisione 6 (§5 a) |
| §8. Misurare se il Brain aiuta a decidere: casi sintetici equivalenti, manuale contro assistito, in ordine controbilanciato, valutati alla cieca | Sì, è una lacuna vera della mappa | Proposta di nuovo punto nella roadmap (§5 d) |
| §4. Dipendenza: errore standard σ√{[1+(K−1)ρ]/(DK)}; la dipendenza già riduce la potenza (52,67% contro 71,64% nel pilota) | Sì | La potenza nella scheda va calcolata con la struttura dei trade, non con la formula gaussiana |
| §4. Gli altri criteri possono solo abbassare la promozione; contarli replica per replica, senza moltiplicare tassi | Sì | Da fare nella prova a vuoto |

## 5. Decisioni per il titolare (opzioni; nessuna scelta di Claude)

**(a) Decisione 6: metro contro obiettivi.**
- Il DGS osserva che l'adeguatezza dipende da **quale effetto vuoi poter riconoscere e con quale probabilità**.
- Con D-36 hai già fissato, per lo screening, **+0,25 R e il 50%**. Se lo confermi come obiettivo del progetto, la strada di fatto è **A1**: si tiene il metro e si candidano solo idee che lo raggiungono.
- Le altre restano: A2 (verifiche più lunghe), A3 (dominio ristretto), A4 (demo), A5 (prima rischio e disciplina), più le due nuove:
  - **A6:** un protocollo nuovo per l'effetto minimo utile;
  - **A7:** archiviare come «non decidibile» senza spendere riserva.

**(b) Clausola sulle code (D-34, punto 3).**
- Opzione 1: come deciso, «stop obbligatorio e perdita massima per trade dichiarata».
- Opzione 2: **dichiarazione verificabile dell'esposizione** in R (salto peggiore plausibile diviso la distanza dello stop, con fonte); collaudo nuovo solo fuori dal dominio provato.
- Il DGS e la controverifica del §2 sostengono la 2.

**(c) Difetto #119.**
- Regola «ampiezza dell'intervallo < 1e-9 R ⇒ invalido» nel modulo del verdetto: sì o no.

**(d) Misura dell'utilità per te** (nuova).
- Inserire nella roadmap la prova «manuale contro assistito» su casi sintetici.
- Opzioni: sì, ora; sì, dopo la macchina; no.

## 6. Che cosa il DGS non aveva

- **Le decisioni D-24 … D-40:** la sua copia del registro si ferma a D-23. Nel prossimo pacchetto vanno incluse.
- **Il punto 9 del messaggio 9** (capienza della riserva: circa 4 verifiche in tutto; potenza in calo dalla seconda apertura): non c'è nel parere. Probabilmente è arrivata la versione senza il punto 9. Va mandato insieme alla prossima richiesta.
