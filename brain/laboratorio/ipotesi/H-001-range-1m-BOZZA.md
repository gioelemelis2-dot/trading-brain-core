# H-001 · Scalping nei micro-range a 1 minuto (BOZZA, NON sigillata)

**Stato:** bozza di Claude sull'idea grezza dell'utente (14/11/2026). Mancano le risposte dell'utente (domande in fondo), i dati dello Studio 1 (E-001) e gli spread misurati. **Non si testa finché non è sigillata.**

## Idea dell'utente (testuale)
«Range di accumulo che durano anche 5 minuti… entrare al top e vendere al bottom, sono movimenti brevi, in cui si mette uno stop loss strettissimo e un tp stretto sempre rispettando il rapporto rischio rendimento.»

Lettura di Claude, da confermare: **contro-tendenza ai bordi del range.** Vendita al massimo del range e acquisto al minimo, con stop appena fuori e target dentro il range.

## Inefficienze e rischi (critica di Claude)
1. **«Range» non è definito:** durata, ampiezza massima, quanti tocchi, se contano le ombre o le chiusure. Senza definizione ogni grafico «mostra» range a posteriori.
2. **Un range si riconosce solo dopo.** Al momento dell'ingresso si conoscono solo i minuti passati: il backtest deve usare solo quelli, altrimenti vede il futuro.
3. **Costi enormi rispetto al movimento.** Con un range di W USD, stop al 25% di W oltre il bordo e target a metà range (rischio/rendimento 1:2 lordo), la percentuale di vincite minima per andare in pari è:

   | Costo per operazione (spread + commissione) | W = 1 | W = 2 | W = 3 | W = 4 | W = 6 |
   |---|---|---|---|---|---|
   | 0,20 USD | 60% | 47% | 42% | 40% | 38% |
   | 0,35 USD | 80% | 57% | 49% | 45% | 41% |
   | 0,50 USD | 100% | 67% | 56% | 50% | 44% |

   Senza costi basterebbe il 33%. Nei range piccoli i costi decidono tutto.
   - **Dati reali (Studio 1, E-001):** la candela mediana a 1 minuto si muove di circa 1,9–2,2 USD e quella a 5 minuti di 4,5–5 USD. Un range di 5 minuti sull'oro di oggi è largo tipicamente qualche dollaro. Con 0,35 USD di costo servono circa il 45–50% di vincite: non impossibile, ma senza margine per stop eseguiti male.
4. **Si vende proprio dove avvengono le rotture.** Ogni range finisce con una rottura, e la rottura parte dal bordo dove si entra. Lo stop stretto viene preso esattamente lì, spesso con slittamento (lo slippage dei movimenti veloci).
5. **Gli ordini limite si riempiono soprattutto quando il prezzo sfonda** (selezione avversa). Toccare il livello sul grafico non vuol dire essere eseguiti.
6. **Dentro una candela da 1 minuto non si sa se è arrivato prima lo stop o il target.** Ipotesi prudente: prima lo stop.
7. **I dati sono solo BID:** gli acquisti si fanno all'ASK, quindi serve lo spread vero, minuto per minuto.
8. **Conflitto con le regole personali:** P-12 (60 secondi fra «vedo» e «clicco») è incompatibile con lo scalping a 1 minuto. Anche P-11 e P-08 pesano. A mano, questa idea è in contrasto con le regole che l'utente si è dato contro l'impulsività. Strade possibili: automatizzarla, oppure cambiare le regole per iscritto (DA-23).
9. **«Rispettare il rapporto rischio/rendimento» non basta:** conta l'aspettativa = p × vincita − (1 − p) × perdita − costi. Un rapporto 1:2 con il 30% di vincite perde.
10. **Troppi parametri liberi** (durata, ampiezza, tocchi, stop, target, sessione, uscita a tempo): ogni combinazione è una prova (DA-19). Vanno fissati prima.
11. **Notizie:** i range prima dei dati USA finiscono con scatti violenti. Serve il filtro di P-08, quindi un calendario storico, che ancora non abbiamo.
12. **FTMO:** lo scalping ordinario dovrebbe essere ammesso, ma le «pratiche vietate» vanno verificate sulle fonti.

## Versione strutturata proposta (da confermare)
- **Dati:** candele BID da 1 minuto (Dukascopy), solo periodo di sviluppo per lo sviluppo.
- **Range (solo minuti passati):** ultimi W minuti.
  - Varianti dichiarate: W = 5 (come dice l'utente) e W = 10, cioè **2 prove**.
  - Ampiezza A = massimo − minimo.
  - Valido se A ≤ 2,5 × ATR(60) da 1 minuto (è un range, non una tendenza)
  - **e** A ≥ 6 × costo per operazione (*filtro di Claude: solo range abbastanza larghi da pagare i costi*).
- **Ingresso:** ordine limite di vendita al massimo del range e di acquisto al minimo, valido 5 minuti; un solo trade alla volta.
  - Esecuzione solo se il prezzo **supera** il livello: BID ≥ livello per la vendita, ASK ≤ livello per l'acquisto.
- **Stop:** 0,25 × A oltre il bordo.
- **Target:** metà del range (rischio/rendimento lordo 1:2).
- **Uscita a tempo:** 10 minuti.
- **Filtri:**
  - sessione scelta dopo lo Studio 1, prima del test;
  - niente trade da 15 minuti prima a 15 minuti dopo i dati USA ad alto impatto (serve il calendario);
  - niente trade nella pausa giornaliera.
- **Costi:** spread misurato sui conti demo per ora del giorno, più la commissione del broker; slippage di 0,05 USD sugli stop (*ipotesi*).
- **Candela ambigua:** se tocca sia lo stop sia il target, conta lo stop.
- **Criterio di fallimento, scritto prima:** aspettativa netta ≤ 0 sullo sviluppo, oppure DSR < 0,95 con tutte le prove contate, oppure risultato che non regge con lo spread peggiore dei tre scenari.

## Domande all'utente
1. «Entrare al top e vendere al bottom»: vendi al massimo del range e compri al minimo (contro-tendenza)? Oppure entri quando il prezzo esce dal range (rottura)?
2. Come riconosci il range sul grafico: dalle ombre o dalle chiusure? Quanti tocchi per lato?
3. Dove metti il target: lato opposto del range, metà del range, o un rapporto fisso?
4. A che ore lo fai di solito?
