# Decisioni da prendere per finire la macchina (19/11/2026)

**Per il titolare.**
- Questo documento raccoglie in un posto solo le decisioni aperte che bloccano la macchina di valutazione.
- Per ogni decisione trovi: la domanda, perché conta, le opzioni con i costi, il **consiglio di Claude** (dichiarato come tale) e che cosa si sblocca.
- **La scelta è tua.** Rispondi con il codice dell'opzione (per esempio «1-A, 2-B…»), oppure scrivi «rinvio» o «altro: …».

**Fonti:**
- DGS-10 §4–§6;
- DA-26, DA-29 e DA-31;
- `laboratorio/esecuzione/riserva.py`;
- l'audit globale del 19/11 (`collaborazione/da-claude/AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`).

**Che cosa conviene decidere oggi:** le decisioni 1, 2, 3 e 4 (circa 40 minuti). La 5 e la 6 dipendono dal consuntivo dell'ASK e dalla risposta del DGS all'audit, quindi si possono solo impostare. La 7 e la 8 sono semplici.

---

## Un fatto nuovo, che pesa su tutte le decisioni: la riserva basta per circa 4 verifiche in tutto

**L'audit non lo diceva: è una mia omissione.**
- Il registro della riserva consuma le date **per calendario e per tutti i mercati insieme**. Una data letta per una verifica è spesa per sempre, anche per GBPJPY o qualunque altro mercato (`riserva.py`, intestazione).
- La riserva va dal 2005 a circa il 31/10/2023: sono **4.912 giorni feriali**, meno festivi, embargo e giorni scartati per qualità.
- Una verifica collaudata usa **1.000 sedute**, cioè circa 4 anni di calendario.
- **Conclusione: la riserva permette circa 4 verifiche in tutto il progetto**, comprese le eventuali verifiche di altri mercati sulle stesse date.

**Per di più, ogni apertura successiva è più severa** (regola α_j = 5% / [j(j+1)]), e la potenza scende:

| Apertura j | Quota | Promossa se vale +0,25 R | +0,30 R | +0,35 R | +0,40 R |
|---|---|---|---|---|---|
| 1ª | 2,5% | 24% | 72% | 97% | 100% |
| 2ª | 0,83% | 13% | 55% | 92% | 100% |
| 3ª | 0,42% | 9% | 46% | 88% | 99% |
| 4ª | 0,25% | 6% | 39% | 84% | 99% |

La tabella è una **stima** (IPOTESI): approssimazione normale, σ = 1,25 R, 1 trade per seduta, D = 1.000, una sola variante (m = 1). Le quote dalla 2ª apertura in poi **non sono state collaudate**: il collaudo IA-02 riguarda il 2,5%, e il DGS lo ha già segnalato (DGS-10 §6).

**Che cosa vuol dire in pratica:**
- la riserva è una risorsa **molto scarsa**: va spesa solo su ipotesi con buone probabilità;
- per idee da +0,30 R o meno il test finale vero sarà comunque la **demo**.

---

## Decisione 1 · «Definizione di fatto» della macchina, e dove mettere il criterio D-31

**Domanda.** Che cosa deve esistere perché tu possa dire «la macchina è finita»? E il nuovo codice del criterio D-31 entra nel perimetro sigillato (R17) oppure in un modulo nuovo, rivisto a parte?

**Perché conta.**
- Il codice che oggi dà il verdetto (`criteri.verifica`) controlla «R medio netto > 0», non il limite D-31.
- Se il criterio D-31 entra nel perimetro di R17, il candidato cambia, e il contatore D-24 (oggi 1 su 2) deve ripartire sul nuovo candidato.
- Senza un elenco chiuso, ogni strumento nuovo apre nuovi giri di revisione.

| Opzione | Che cosa significa | Costo | Rischio |
|---|---|---|---|
| **1-A** | Si chiude il contatore sul perimetro attuale (R17 più il giro su tutte le manomissioni). Il criterio D-31 e il registro unico di N diventano un **modulo nuovo**, con 2 giri di revisione propri, limitati a quel modulo, più un collegamento testato con l'esecutore | Medio: circa 1 settimana | Un'interfaccia fra i due pezzi da collaudare |
| **1-B** | Si mette D-31 dentro il perimetro adesso; nuovo candidato, contatore da 0 su tutto | Alto: altri 2 giri completi | Ciclo di revisioni più lungo |
| **1-C** | D-31 lo applica a mano un revisore sul file dei risultati, senza codice | Basso | Errore manuale; meno ripetibile |

**Elenco chiuso proposto** (vale con 1-A o 1-B):
1. il criterio D-31 nel codice;
2. il registro unico delle prove (N);
3. la clausola sulle code (stop obbligatorio e perdita massima per trade dichiarata);
4. i rapporti con tipo e incertezza su ogni numero;
5. la prova generale a vuoto superata;
6. R17 e il giro su tutte le manomissioni;
7. l'unione in `main` con la protezione del ramo.

**Tutto ciò che non è in elenco va a lotti e non riapre il contatore.**

**Consiglio di Claude: 1-A con l'elenco chiuso.** Tiene il valore dei giri già fatti e limita le nuove revisioni al codice nuovo.

**Sblocca:** il lavoro tecnico dei prossimi giorni, cioè il criterio D-31 in TDD e poi la prova generale a vuoto.

---

## Decisione 2 · Esiti della verifica: due stati o tre (DA-31), e cosa fare dei «non decidibili»

**Domanda.** Quando la verifica non promuove, vuoi distinguere «bocciata» (evidenza contraria) da «non decidibile» (prova insufficiente)?

**Perché conta.** Con la potenza del nostro metro, **molti esiti saranno «inconclusivi»**: per esempio, a +0,25 R tre volte su quattro. Se li chiamiamo tutti «bocciata», nel registro una strategia scarsa e una buona ma non dimostrabile sembrano uguali.

| Opzione | Testo in breve (dal DGS-10 §4) | Pro | Contro |
|---|---|---|---|
| **2-A** due stati | Avanza solo con L > +0,20 R e tutti i requisiti; altrimenti si chiude, **con la causa scritta** (sfavorevole, veto, inconclusiva, prova invalida) | Semplice | La parola «bocciata» confonde i casi |
| **2-B** tre stati | Promossa / bocciata (U < +0,10 R o veto) / non decidibile, con la tabella delle priorità del DGS | Distingue l'evidenza contraria dalla prova insufficiente | Bisogna fissare prima la priorità dei veti |

**E per i «non decidibili»:**
- **2-x** archiviazione definitiva;
- **2-y** riesame **solo con dati nuovi** (la demo futura), come prova nuova contata in N, senza un'altra spesa di riserva storica.

**Consiglio di Claude: 2-B con 2-y.** Un «non decidibile» ha poi una strada sola: la demo. È coerente con il fatto che la riserva basta per circa 4 verifiche.

**Sblocca:** il codice del criterio D-31 (Decisione 1), che deve sapere quali esiti produrre.

---

## Decisione 3 · Regola dello screening sullo sviluppo (quando una variante merita di spendere la riserva)

**Domanda.** Sullo sviluppo (dal 15/11/2023, circa 780 sedute), che cosa deve mostrare una variante per poter chiedere una verifica sulla riserva?

**Perché conta.**
- Ogni verifica spende circa un quarto della riserva.
- Lo screening **non** è una prova: il risultato migliore fra più varianti è gonfiato dalla selezione. Serve solo a non sprecare la riserva.

| Opzione | Regola | Effetto |
|---|---|---|
| **3-A** solo stima | R medio netto sullo sviluppo **> r_min** | Semplice. Con r_min basso passa quasi tutto |
| **3-B** solo limite | Limite inferiore dell'intervallo (lo stesso bootstrap) **> 0** | Esclude il puro caso, ma lascia passare medie da +0,10 R che poi in verifica sarebbero quasi sempre inconclusive |
| **3-C** stima e limite | R medio netto **> r_min** **e** limite inferiore **> 0**, più una **potenza stimata ≥ 50%** per la verifica, calcolata con la procedura congelata nella scheda | Spende la riserva solo dove c'è una possibilità concreta |

**Valore di r_min da scegliere:** +0,20 / **+0,25** / +0,30 R. L'uguaglianza esatta non passa (confronto stretto «>», come in verifica).

**Consiglio di Claude: 3-C con r_min = +0,25 R.** Motivo: sotto +0,25 R la potenza della prima verifica è sotto il 25%, cioè si spenderebbe un quarto della riserva con tre probabilità su quattro di non concludere nulla.

**Sblocca:** il §8 del modello H-003 (DGS-10 testo I, ultima riga) e la prova generale a vuoto.

---

## Decisione 4 · Minimi e anni valutabili (clausola D del modello)

**Domanda.** Quali minimi deve avere una verifica, e cosa fare dei criteri annuali (60% di anni positivi, ultimi 5 anni positivi)?

**Perché conta: c'è un'incoerenza da risolvere.**
- 1.000 sedute sono circa **4 anni**: «ultimi 5 anni positivi» non si può valutare senza contare anni parziali (DGS-10 §6 lo segnala).
- Inoltre, ogni criterio aggiunto **abbassa ancora la potenza**.

| Opzione | Che cosa significa |
|---|---|
| **4-A** | Il verdetto lo dà **solo D-31**. Gli anni (o blocchi da 250 sedute) si riportano come descrizione, e diventano un **veto** solo se un blocco è molto negativo, con soglia fissata prima (per esempio media del blocco < −0,25 R) |
| **4-B** | Si tengono i criteri annuali come requisiti vincolanti, ridefiniti su blocchi da 250 sedute (60% dei blocchi positivi; nessun requisito sugli «ultimi 5») |
| **4-C** | Si tiene tutto com'era e si allunga la verifica a 5 anni (circa 1.250 sedute): fuori dal dominio collaudato, quindi serve un nuovo collaudo, e la riserva scende a circa 3 verifiche |

**Minimi tecnici proposti (per tutte le opzioni):**
- D = 1.000 sedute esatte, scelte per calendario prima di aprire;
- almeno **300 trade**;
- almeno 200 sedute con trade.

Sotto questi minimi l'esito è «non decidibile» (con 2-B) o «chiusa per prova insufficiente» (con 2-A). I numeri sono una **proposta**: servono a garantire che l'intervallo sia stimabile.

**Consiglio di Claude: 4-A** con il veto per blocchi e i minimi proposti. Tiene un solo metro collaudato ed evita criteri che non si possono valutare.

**Sblocca:** il codice del criterio (Decisione 1) e la clausola D del modello.

---

## Decisione 5 · Regole di spesa della riserva (da impostare oggi, da confermare dopo il consuntivo ASK)

**Domanda.** Quanto «errore» totale accettiamo su tutte le aperture (α totale), e quale parte della riserva teniamo **protetta** per l'ultima conferma?

| Opzione | α totale | Parte protetta | Effetto |
|---|---|---|---|
| **5-A** | 5% (già nel codice e nel collaudo) | Nessuna | Massima flessibilità: circa 4 verifiche disponibili |
| **5-B** | 5% | Un blocco di circa 1.000 sedute riservato alla **conferma finale di un portafoglio** (per esempio prima della sfida FTMO) | Restano circa 3 verifiche per le singole ipotesi |
| **5-C** | 10% | Nessuna | Quote più alte, quindi più potenza, ma più falsi positivi tollerati. **Fuori dal collaudo**: richiede un nuovo collaudo |

**Consiglio di Claude: 5-A per ora**, con riesame dopo la prima verifica. Con circa 4 verifiche, proteggerne una subito ne lascia troppo poche; il test finale del portafoglio può essere la demo.

**Che cosa resta da fissare dopo il consuntivo ASK** (non decidibile oggi):
- date esatte di inizio e fine;
- embargo prima dello sviluppo (proposta: 10 giorni di borsa);
- quarantena dei giorni con dati scarsi. Proposta: un giorno va in quarantena se nella fascia operativa mancano più del 5% dei minuti su BID o su ASK.

**Sblocca:** la creazione del registro vero della riserva (oggi vietata finché non decidi).

---

## Decisione 6 · Divario fra il metro e i tuoi obiettivi (dopo la risposta del DGS all'audit)

**Domanda.** Gli obiettivi (+0,10/+0,27 R a trade) stanno dove il metro promuove raramente: che cosa facciamo?

| Opzione | In breve | Costo |
|---|---|---|
| **6-A1** | Si tiene D-31 e si portano in verifica solo idee con vantaggio atteso ≥ 0,35 R e potenza calcolata prima | Basso; meno idee candidabili |
| **6-A2** | Verifiche più lunghe (2.000 sedute) | Nuovo collaudo; la riserva scende a circa 2 verifiche |
| **6-A3** | Nuovo collaudo su un dominio ristretto (stop obbligatorio, perdita massima limitata) per ridurre il margine | Medio-alto; può fallire |
| **6-A4** | La prova decisiva diventa la **demo** (test di Wald); la riserva fa da filtro | Mesi di demo |
| **6-A5** | Prima il Brain come strumento di rischio e disciplina (Guardian, diario), poi la ricerca | Rinvia le strategie |

**Consiglio di Claude: aspettare la risposta del DGS al messaggio 9**, che ricalcola la potenza. Se il calcolo regge, la combinazione più realistica sembra **6-A1 più 6-A4**, ma è una scelta di strategia del progetto e spetta a te.

---

## Decisione 7 · Custodia dei dati (semplice)

**Domanda.** Dove teniamo la seconda copia dei dati veri oltre al Mac?

| Opzione | Che cosa significa |
|---|---|
| **7-A** | Chiavetta USB o disco esterno più il cloud già usato, ciascuno con la stessa impronta SHA-256 |
| **7-B** | Solo il cloud |

**Consiglio di Claude: 7-A**, appena l'ASK è finito (copia finale, `PROCEDURA-ASSISTENZA-MAC.md` passo 3).

---

## Decisione 8 · Pilastri fermi (facoltativa)

**Domanda.** Riattiviamo subito il diario e le previsioni, che costano pochi minuti al giorno, oppure li rinviamo con una data?

| Opzione | Che cosa significa |
|---|---|
| **8-A** | Da domani, una previsione al giorno nel registro delle previsioni (per esempio la direzione dell'oro a fine sessione di Londra, con probabilità), solo su dati dal 15/11/2023. Dopo 30 previsioni, il punteggio di Brier contro la base ingenua |
| **8-B** | Rinvio, con riesame alla fine della macchina |

**Consiglio di Claude: 8-A** se hai 5 minuti al giorno. È la prima misura di «utilità per te» che non richiede una strategia.

---

## Come rispondere

Basta una riga, per esempio: «1-A, 2-B-y, 3-C 0,25, 4-A, 5-A, 6 aspetto il DGS, 7-A, 8-B».

Claude poi:
1. registra le scelte in `DECISIONI.md` come D-34 e seguenti, con data;
2. aggiorna il modello H-003 dove serve;
3. comincia in TDD il codice che ne deriva.
