# Quaderno delle ipotesi (Claude, notte del 14–15/11/2026)

**Stato:** idee iniziali, NON schede da sigillare. Nessuna è stata provata.
- Scritto **solo da conoscenze e letteratura**, senza guardare dati: né quelli di sviluppo né quelli sigillati, né grafici, né TradingView.
- **Contaminazione dichiarata (DA-17):** Claude conosce gli esiti di E-001 (nessuna direzione per sessione) e di E-002 (micro-range: circa +3 punti di ritorno verso la media, troppo poco contro i costi). Dove contano, sono scritti nella scheda.
- **Fonti:** la verifica bibliografica è stata fatta con ricerche web sui record degli editori (RePEc/EconPapers, repository universitari). Per molti lavori **solo l'abstract**: i numeri specifici sull'oro NON sono verificati e sono segnati «da verificare sul testo».
- **Ogni prova costa:** il DSR della verifica usa N = **tutte** le prove nel registro, di tutte le ipotesi. Ogni variante dichiarata alza la soglia anche per le altre. Per questo ogni scheda propone 1–2 varianti al massimo.

## Come sono ordinate
Il punteggio è a giudizio, ed è dichiarato:
1. forza delle prove per l'oro, o almeno per i future su materie prime;
2. compatibilità con le regole personali: niente weekend; overnight non deciso; demo; rischio fisso per trade;
3. possibilità di avere **almeno 300 trade nei 3 anni di sviluppo**. Senza, lo screening del tipo H-002 non si può fare;
4. peso dei costi rispetto al movimento atteso sull'orizzonte del trade;
5. indipendenza da H-002: una prova molto simile a H-002 aggiunge poco e costa N.

**Il costo di riferimento è quello di H-002:** spread vero + 0,07 commissione + 0,10 in ingresso + 0,20 in uscita a mercato, circa 0,6–0,8 USD per oncia andata e ritorno.
- Il movimento tipico cresce come la radice dell'orizzonte: a parità di costo, un orizzonte 4 volte più lungo dimezza il peso relativo dei costi.
- I numeri veri si misurano solo sui dati di sviluppo, dopo il sigillo della scheda. Qui non ce ne sono.

| # | idea | prove | regole personali | trade in 3 anni | costi | voto |
|---|---|---|---|---|---|---|
| Q-01 | momento intraday: l'inizio della giornata predice la fine | medie (molti future; oro solo in Cina e ETF) | compatibile | ~700 | medi | **1°** |
| Q-02 | tendenza giornaliera (incrocio di medie / momento di serie storica) | forti (decenni, molte materie prime) | **conflitto overnight/weekend** | **~30–60** | bassi | 2° (prove), non testabile così |
| Q-03 | prosecuzione dopo i dati macro USA delle 08:30 di New York | buone sulla reazione, deboli sulla prosecuzione | compatibile | ~250–400 | alti | 3° |
| Q-04 | pomeriggio dei giorni di panico azionario (bene rifugio) | buone sul legame contemporaneo, nessuna sulla previsione | compatibile | ~100–200 | medi | 4° |
| Q-05 | movimento prima del fixing LBMA delle 15:00 | una pubblicazione, regime cambiato nel 2015 | compatibile | ~700 | alti | 5° |
| Q-06 | rottura dopo la compressione (NR7) | da praticanti, contraddetta dal raggruppamento della volatilità | compatibile | ~100 | medi | 6° |
| Q-07 | ritorno in tendenza su EMA/VWAP (incrocio di indicatori) | deboli | compatibile | ~300–500 | medi | 7° |
| Q-08 | RSI(2) con filtro di tendenza | deboli (azioni USA, libri da praticanti) | conflitto overnight | ~100 | bassi | 8° |
| Q-09 | ritorno verso la media dopo gli eccessi della notte asiatica | deboli, e E-002 contro | compatibile | ~400 | alti | 9° |
| Q-10 | stagionalità dell'oro («effetto autunno») | da un solo lavoro, rischio di dati cercati | conflitto overnight | **~3** | trascurabili | 10° |

---

## Q-01 · Momento intraday: la prima parte della giornata predice l'ultima mezz'ora
- **Motivo economico:**
  - le coperture dei market maker di opzioni con gamma negativo comprano quando il prezzo sale e vendono quando scende, soprattutto vicino alla chiusura;
  - si aggiungono i ribilanciamenti a fine giornata (ETF a leva, fondi) e gli investitori che si muovono tardi.
  - Il flusso va nella direzione della giornata e si concentra alla fine.
- **Letteratura:**
  - Gao, Han, Li & Zhou (2018), *Market intraday momentum*, Journal of Financial Economics 129(2), 394–414: sull'ETF S&P 500 (1993–2013) il rendimento della prima mezz'ora predice quello dell'ultima.
  - Baltussen, Da, Lammers & Martens (2021), *Hedging demand and market intraday momentum*, JFE 142(1), 377–403: oltre 60 future (azioni, obbligazioni, **materie prime**, valute) dal 1974 al 2020; l'ultima mezz'ora segue il resto della giornata; legato alla copertura gamma. **L'effetto si inverte nei giorni successivi.**
  - Oro: studi sui future cinesi sui metalli e sugli ETF (ricerca web: abstract in [ACFR AUT](https://acfr.aut.ac.nz/__data/assets/pdf_file/0008/686816/4a-Z-Ivy-Zhou.pdf), [J. Futures Markets 40(4) 2020](https://ideas.repec.org/a/wly/jfutmk/v40y2020i4p632-650.html)). La prevedibilità dipende dalla sessione ed è più forte nei giorni volatili. **Nessuno studio diretto sul COMEX o sull'XAUUSD trovato.**
- **Regole proposte (da fissare prima del sigillo):**
  - giornata = sessione COMEX, dalle 08:20 alle 13:30 di New York (orario della vecchia contrattazione alle grida, ancora punto di riferimento della liquidità);
  - segnale = segno del rendimento BID da 08:20 a 13:00 di New York;
  - ingresso all'apertura del primo minuto eseguibile dalle 13:00, uscita alle 13:30 a mercato. Nessuno stop di prezzo oltre a uno stop di emergenza a 3 × l'ampiezza media di 30 minuti delle 20 sessioni precedenti;
  - un trade al giorno; si salta se |rendimento del segnale| < 2 × costo;
  - **alternativa da scegliere PRIMA** (non da provare tutte e due): fine alle 17:00 di New York (chiusura elettronica). Il segnale va dalle 08:20 alle 16:30 e l'ingresso alle 16:30 è più vicino all'ultima mezz'ora del lavoro di Baltussen et al.
- **Parametri e prove:** 1 variante principale (N +1). Robustezza fuori da N: finestra del segnale con inizio 09:30 invece di 08:20, e uscita a 13:45.
- **Costi rispetto all'orizzonte:** **critici**. 30 minuti di tenuta sono pochi: se l'effetto vale pochi punti base, i 0,6–0,8 USD lo mangiano. Il filtro del segnale minimo aiuta solo in parte.
- **Perché potrebbe NON funzionare:**
  - sull'oro spot (OTC, 24 ore) non esiste una «chiusura» unica: il ribilanciamento potrebbe concentrarsi altrove, per esempio al fixing o alla chiusura di New York;
  - il meccanismo gamma è documentato sugli indici azionari, molto meno sull'oro;
  - pubblicato nel 2018 e 2021: l'effetto può essersi ridotto dopo la pubblicazione.
- **Regole personali:** nessun conflitto (intraday, chiuso entro le 13:30 o le 17:00 di New York). **Nessuna sovrapposizione con H-002**: orari diversi, posizione chiusa.
- **Perché è prima:** è l'unica idea con un meccanismo documentato su molti future, compresi quelli sulle materie prime, che è intraday, testabile con ~700 trade e costa 1 prova.

## Q-02 · Tendenza giornaliera (incrocio di medie / momento di serie storica)
- **Motivo economico:**
  - reazione lenta alle informazioni, poi eccesso (gregge, coperture);
  - premio per il rischio di chi fornisce copertura ai produttori (pressione di copertura).
- **Letteratura:**
  - Moskowitz, Ooi & Pedersen (2012), *Time series momentum*, JFE 104(2), 228–250: 58 future, rendimento degli ultimi 12 mesi predice il mese successivo;
  - Hurst, Ooi & Pedersen (2017), *A century of evidence on trend-following investing*, Journal of Portfolio Management 44(1);
  - Szakmary, Shen & Sharma (2010), *Trend-following trading strategies in commodity futures: A re-examination*, Journal of Banking & Finance 34(2), 409–426: 28 future, 48 anni, profitti positivi per la grande maggioranza dei contratti. **Il dato specifico sull'oro va verificato sul testo** (DOI 10.1016/j.jbankfin.2009.08.004);
  - contro: Marshall, Cahan & Cahan (2008), JBF 32(9), nessun profitto dopo la correzione per la ricerca di dati su 15 future; Bajgrowicz & Scaillet (2012), JFE 106(3), le regole tecniche non sopravvivono a costi e scoperte false (azioni USA).
- **Regole proposte:**
  - posizione lunga se la media mobile semplice a 50 giorni della chiusura delle 17:00 di New York è sopra quella a 200, corta se è sotto;
  - controllo una volta al giorno; stop di emergenza a 3 × ATR(20);
  - **in alternativa** (una sola delle due): segno del rendimento a 12 mesi, ribilanciamento mensile.
- **Parametri e prove:** 1 variante (N +1). Robustezza: 20/100 e 100/300.
- **Costi rispetto all'orizzonte:** trascurabili sulla commissione; **il problema è lo swap**: il finanziamento overnight del CFD sull'oro su settimane o mesi, da misurare sulla scheda dello strumento di FP Markets.
- **Perché potrebbe NON funzionare:**
  - pochissimi trade (un incrocio ogni pochi mesi): ~30–60 operazioni in 3 anni, troppo poche per lo screening (≥300). **Lo schema H-002 non si applica:** servirebbe una scheda con la sola verifica lunga, dal 2005 al 2023, e criteri diversi, da decidere;
  - i profitti della tendenza sulle materie prime vengono soprattutto da pochi grandi movimenti; su un solo strumento la varianza è enorme.
- **Regole personali:** **conflitto diretto** con «niente weekend» e con l'overnight (non deciso). È incompatibile anche con le regole di molte prove FTMO standard (le posizioni nel weekend sono ammesse solo sui conti «swing»).
- **Perché è seconda e non prima:** ha le prove migliori di tutto il quaderno, ma oggi non si può né testare con le regole di screening né fare con le regole personali. **Serve una decisione dell'utente** sull'overnight prima di qualunque scheda.

## Q-03 · Prosecuzione dopo i dati macro USA delle 08:30 di New York
- **Motivo economico:** la sorpresa del dato sposta il prezzo in pochi secondi. Se una parte degli operatori reagisce in ritardo (ribilanciamenti, interpretazione), il movimento può continuare nei minuti successivi.
- **Letteratura:**
  - Andersen, Bollerslev, Diebold & Vega (2003), *Micro effects of macro announcements*, American Economic Review 93(1), 38–62: sui cambi il salto è quasi immediato;
  - Elder, Miao & Ramchander (2012), *Impact of macroeconomic news on metal futures*, JBF 36(1), 51–65: oro, argento e rame 2002–2008, reazione **rapida e significativa**; dati delle 08:30 (occupazione non agricola, ordini di beni durevoli) i più forti; dati migliori del previsto → oro giù;
  - Christie-David, Chaudhry & Koch (2000), *Do macroeconomics news releases affect gold and silver prices?*, Journal of Economics and Business 52(5).
  - **Nessuna di queste fonti mostra una prosecuzione sfruttabile dopo i primi minuti**: le prove riguardano la reazione, non la previsione.
- **Regole proposte:**
  - solo nei giorni con un dato di livello alto alle 08:30 di New York (occupazione, inflazione dei prezzi al consumo, vendite al dettaglio), dal calendario P-08;
  - segnale = direzione del BID fra le 08:30 e le 08:35;
  - ingresso alle 08:35, uscita alle 09:30 o allo stop al lato opposto della candela 08:30–08:35.
- **Parametri e prove:** 1 variante (N +1). Robustezza: segnale fino alle 08:32 o alle 08:40.
- **Costi rispetto all'orizzonte:** **alti**. Spread larghi e slittamenti veri nei minuti dopo il dato; lo slittamento di 0,10 di H-002 qui è ottimista e andrebbe alzato prima del sigillo.
- **Perché potrebbe NON funzionare:**
  - l'efficienza documentata: la reazione si completa in secondi o minuti;
  - dati Dukascopy al minuto senza la profondità del libro;
  - **manca un calendario affidabile e storico** (P-08, ancora aperto);
  - pochi giorni: circa 2–4 dati forti al mese, circa 70–150 l'anno.
- **Regole personali:** compatibile. Richiede il calendario delle notizie.

## Q-04 · Pomeriggio dei giorni di panico azionario (oro bene rifugio)
- **Motivo economico:** nei giorni di forti cadute azionarie i fondi cercano attività sicure; se lo spostamento avviene in più ore, l'oro sale anche dopo la caduta iniziale.
- **Letteratura:**
  - Baur & Lucey (2010), *Is gold a hedge or a safe haven?*, The Financial Review 45(2), 217–229;
  - Baur & McDermott (2010), *Is gold a safe haven? International evidence*, JBF 34(8), 1886–1898.
  - Il legame è **contemporaneo** (nei giorni estremi, all'incirca, l'oro non scende o sale) e dura poco: non è una previsione intraday.
  - **Nessuna fonte trovata su una prosecuzione intraday** dopo la caduta delle azioni: da cercare prima della scheda.
- **Regole proposte:**
  - se l'S&P 500 (future o ETF) perde più di 1,5% fra l'apertura delle 09:30 di New York e le 11:00, acquisto oro alle 11:00;
  - uscita alle 15:30 di New York o allo stop a 1 × ATR(20) dei 30 minuti.
- **Parametri e prove:** 1 variante (N +1). Robustezza: soglie dell'1% e del 2%.
- **Costi rispetto all'orizzonte:** medi (4,5 ore di tenuta, movimenti ampi nei giorni volatili).
- **Perché potrebbe NON funzionare:**
  - nelle crisi di liquidità l'oro viene **venduto** per coprire margini (per esempio marzo 2020, ottobre 2008: noto in letteratura e dalla cronaca, non da dati guardati);
  - servono dati dell'indice azionario: una fonte nuova da validare;
  - pochi giorni: ~30–70 l'anno.
- **Regole personali:** compatibile (intraday). Risponde alla domanda dell'utente sull'oro come bene rifugio.

## Q-05 · Movimento prima del fixing LBMA delle 15:00 di Londra
- **Motivo economico:** chi partecipa al fixing conosce prima lo squilibrio fra domanda e offerta. Se l'informazione trapela, il prezzo si muove nella direzione del fixing prima della pubblicazione.
- **Letteratura:**
  - Caminschi & Heaney (2014), *Fixing a leaky fixing: short-term market reactions to the London PM gold price fixing*, Journal of Futures Markets 34(11), 1003–1039 ([RePEc](https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html)): sui future GC e sull'ETF GLD, segni che l'informazione trapelava prima della pubblicazione del fixing;
  - critica: P. Fertig nell'*Alchemist* della LBMA (la fuga si spiega senza manipolazione).
  - **Marzo 2015:** il fixing telefonico è sostituito dall'asta elettronica dell'ICE (LBMA Gold Price).
- **Regole proposte:**
  - segnale = direzione del BID fra le 14:45 e le 15:00 di Londra;
  - ingresso alle 15:00, uscita alle 15:30.
- **Parametri e prove:** 1 variante (N +1).
- **Costi rispetto all'orizzonte:** **alti** (30 minuti).
- **Perché potrebbe NON funzionare:**
  - il meccanismo dell'effetto pubblicato (fuga dal fixing telefonico) **è stato abolito nel 2015**;
  - lo sviluppo (2023–2026) è tutto dopo, ma la verifica (2005–2023) mescola i due regimi: un buon risultato in verifica potrebbe venire solo dal periodo prima del 2015, ed è inutile per oggi;
  - la scheda H-002 v3.1 lo nomina come «variante esclusa in questo giro».
- **Regole personali:** compatibile. **Sovrapposizione con H-002**: la sessione di H-002 è ancora aperta alle 15:00.

## Q-06 · Rottura dopo la compressione (NR7)
- **Motivo economico (dichiarato dai praticanti):** dopo un periodo di range stretti la volatilità «si espande» e la rottura del giorno ha seguito.
- **Letteratura:**
  - Crabel (1990), *Day Trading with Short Term Price Patterns and Opening Range Breakout*: libro da praticante, senza verifica statistica indipendente;
  - **contro:** la volatilità si raggruppa (Engle 1982, *Econometrica*; Bollerslev 1986, *Journal of Econometrics*). Dopo giorni calmi il giorno dopo è più spesso calmo: l'«espansione» non è la norma.
- **Regole proposte:**
  - giorno D con range (massimo − minimo, sessione 24 ore fino alle 17:00 di New York) il più stretto dei 7 precedenti;
  - il giorno D+1, ordine stop al massimo e al minimo di D;
  - uscita a fine sessione di Londra o di New York (da scegliere prima), stop al lato opposto.
- **Parametri e prove:** 1 variante (N +1).
- **Costi rispetto all'orizzonte:** medi (range stretti = stop vicini = costi pesanti in R).
- **Perché potrebbe NON funzionare:** le prove sono aneddotiche; la teoria della volatilità va contro; ~1 giorno ogni 7, ~100 trade in 3 anni (sotto lo screening).
- **Regole personali:** compatibile. **Simile a H-002** (rottura di un range): poca informazione nuova per una prova in più.

## Q-07 · Ritorno in tendenza su EMA/VWAP (incrocio di indicatori)
- **Motivo economico:** in una giornata di tendenza i ritorni verso il prezzo medio della giornata (VWAP) sono occasioni d'ingresso usate dagli esecutori istituzionali, quindi supporti «autorealizzati».
- **Letteratura:** debole. Nessuno studio indipendente trovato per l'oro.
  - Il VWAP è un riferimento di esecuzione documentato (Berkowitz, Logue & Noser 1988, *Journal of Finance*), ma non una prova di prevedibilità;
  - le regole tecniche in genere non sopravvivono alla correzione per la ricerca di dati (Sullivan, Timmermann & White 1999, *Journal of Finance* 54(5); Bajgrowicz & Scaillet 2012).
  - **Il VWAP sull'XAUUSD spot non ha volume vero**: Dukascopy dà un volume di tick, non scambi.
- **Regole proposte:**
  - tendenza = EMA(20) a 15 minuti sopra (sotto) l'EMA(50) e prezzo sopra (sotto) l'apertura delle 08:00 di Londra;
  - ingresso al primo tocco dell'EMA(20) dopo le 09:00, stop sotto il minimo del ritracciamento, target 1,5R;
  - un trade al giorno, fine alle 16:30.
- **Parametri e prove:** almeno 4 numeri scelti a mano. **Rischio di ricerca di dati alto**: va dichiarata 1 sola combinazione (N +1).
- **Costi rispetto all'orizzonte:** medi.
- **Perché potrebbe NON funzionare:** l'incrocio di indicatori non ha un meccanismo economico verificabile; molti gradi di libertà.
- **Regole personali:** compatibile. In parte simile a H-002 (giorni di tendenza a Londra).

## Q-08 · RSI(2) con filtro di tendenza
- **Motivo economico:** eccessi a brevissimo termine (vendite forzate, liquidità) che rientrano in pochi giorni dentro una tendenza di fondo.
- **Letteratura:** Connors & Alvarez (2008), *Short Term Trading Strategies That Work*: libro da praticanti, sugli indici azionari USA. **Nessuna prova sull'oro**; l'effetto di ritorno a breve è documentato soprattutto sulle azioni (Lehmann 1990, *Quarterly Journal of Economics*; Jegadeesh 1990, *Journal of Finance*), non sulle materie prime.
- **Regole proposte:** acquisto alla chiusura se RSI(2) < 10 e prezzo sopra la media a 200 giorni; uscita alla chiusura in cui RSI(2) > 70; solo acquisti.
- **Parametri e prove:** 1 variante (N +1).
- **Costi rispetto all'orizzonte:** bassi (giorni).
- **Perché potrebbe NON funzionare:** prove nate su un'altra classe di attività; solo acquisti = dipendenza dalla tendenza (criterio 6 di H-002 contro); pochi trade.
- **Regole personali:** **conflitto con l'overnight e il weekend.**

## Q-09 · Ritorno verso la media dopo gli eccessi della notte asiatica
- **Motivo economico:** di notte la liquidità è bassa e gli ordini grandi spostano il prezzo; all'arrivo di Londra i market maker riportano il prezzo indietro.
- **Letteratura:** sulle azioni, i rendimenti notturni e diurni si comportano in modo diverso (Lou, Polk & Skouras 2019, *A tug of war: Overnight versus intraday expected returns*, JFE 134(1)). Per l'oro spot **nessuna prova diretta trovata**.
- **Contro, dai nostri studi:** E-002 ha trovato al minuto solo +3 punti percentuali di ritorno verso la media, circa 0,02 USD lordi contro 0,07–0,40 di costi.
- **Regole proposte:** se il movimento fra le 00:00 e le 07:00 di Londra supera 2 × la mediana delle 20 notti precedenti, all'apertura delle 08:00 posizione contraria; uscita alle 12:00 o allo stop a 1 × il movimento notturno.
- **Parametri e prove:** 1 variante (N +1).
- **Costi rispetto all'orizzonte:** alti.
- **Perché potrebbe NON funzionare:** gli eccessi notturni dell'oro sono spesso **notizie vere** (Asia, banche centrali), non rumore; l'E-002 è un indizio contrario.
- **Regole personali:** compatibile.

## Q-10 · Stagionalità dell'oro («effetto autunno»)
- **Letteratura:** Baur (2013), *The autumn effect of gold*, Research in International Business and Finance 27(1): rendimenti più alti a settembre e novembre (gioielleria indiana, stagione dei matrimoni, festività).
- **Regole proposte:** acquisto all'inizio di settembre, uscita a fine novembre.
- **Parametri e prove:** 1 (N +1).
- **Perché potrebbe NON funzionare:**
  - 1 trade l'anno: 3 trade nello sviluppo e ~18 in verifica, statisticamente inutile;
  - un solo lavoro e un'anomalia di calendario: il rischio di ricerca di dati è il più alto di tutti.
- **Regole personali:** **conflitto pieno** (mesi di overnight e di weekend, swap).
- **Perché è ultima:** si può scrivere, ma nessun test con questi dati può dire qualcosa.

---

## Cosa NON è nel quaderno, e perché
- **Fibonacci:** l'utente ha chiesto di non parlarne per ora.
- **Combinazioni di più idee in una strategia:** moltiplicano le prove e i gradi di libertà. Prima si prova una idea alla volta.
- **Apprendimento automatico:** con 3 anni di sviluppo e uno strumento, il rischio di adattarsi al rumore è altissimo e il DSR lo punirebbe.

## Decisioni che servono all'utente
1. **Overnight e weekend:** senza una decisione, Q-02, Q-08 e Q-10 restano bloccate.
2. **Quale idea scrivere come scheda dopo H-002.** Proposta di Claude: Q-01, con la sola variante «fine alle 13:30 di New York».
3. **Calendario delle notizie (P-08):** senza, Q-03 non si può scrivere.
4. **Dati azionari** per Q-04: fonte nuova, da validare come Dukascopy.
