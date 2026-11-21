# Messaggio 10 al DGS: capienza della riserva, decisioni D-24 … D-45, modulo del verdetto, casi a risposta esatta (19/11/2026)

**Come si manda.** Si incolla tutto il testo fra le due righe di trattini; è lungo, quindi se serve si divide in due messaggi alla riga «ALLEGATO A». Nessun dato personale né di mercato.

---

MESSAGGIO 10 AL DGS — solo metodo; nessuna decisione riservata al titolare.

CONTESTO
- AGGIORNAMENTO DEL 21/11 (il messaggio è stato scritto il 19–20/11 e si manda oggi):
  - R17 consegnato da Gemini e verificato da Claude: pulito, contatore D-24 a 2 su 2 sul candidato e476a9a;
    un solo rilievo nuovo, minore e fuori dal perimetro (#121, bordi su input anomali di protocollo_ia02.py).
  - R18 (giro su tutte le manomissioni, più il primo giro di revisione del modulo del verdetto) è in corso con Gemini.
  - D-34 punti 1–4 fatti nel codice (verdetto D-31, N dal registro canonico, clausola sulle code nel modello,
    rapporti con i tipi epistemici); manca il punto 5, la prova generale a vuoto, per cui servono i tuoi casi.
  - Test automatici su GitHub attivi a ogni push (25 suite, Python 3.13 e 3.9, rete bloccata); hanno trovato #120.
- DGS-11 ricevuto, archiviato e verificato: tutti i numeri sono confermati da Claude.
- **Esempio avverso rifatto** come chiesto (B = 3.999, conteggi incrociati), su dati inventati, 300 repliche, media vera +0,15 R:
  - G1 dell'audit: 35/300 promosse, tutte nelle 35 repliche senza perdita rara.
  - Causa: le vincite erano tutte identiche, quindi l'intervallo aveva ampiezza di circa 1e-13 solo per arrotondamento, e veniva accettato.
  - Con vincite gaussiane (sd 1,2 R) e perdita rara di −20 R: 0/300. Con −50 R: 15/300, tutte senza perdita (46 repliche senza perdita).
  - **L'11,7% dell'audit era quindi in gran parte un artefatto.**
- **Errore di metodo dell'audit accettato** (DGS-11 §8): Claude ha giudicato la macchina intera con un solo criterio.
- **Il punto 9 del messaggio 9 non vi era arrivato.** Lo riporto qui sotto (richiesta 1).
- La vostra copia del registro delle decisioni si fermava a D-23: le decisioni D-24 … D-45 sono nell'ALLEGATO A.

RICHIESTE
1. **Capienza della riserva** (omissione dell'audit).
   - Il registro consuma le date per calendario e per tutti i mercati insieme.
   - La riserva 2005 → circa 31/10/2023 ha 4.912 giorni feriali, prima di festivi, embargo e quarantene.
   - Con D = 1.000 sedute bastano circa **4 verifiche in tutto il progetto**.
   - Con α_j = 5%/[j(j+1)] e m = 1 le quote sono 2,5%, 0,8333%, 0,4167% e 0,25%.
   - Nell'approssimazione normale (σ = 1,25, 1 trade per seduta) la potenza a μ = +0,30 R vale 71,6%, 55,4%, 45,7% e 39,1%.
   - Verificate il conteggio e la potenza, e dite se le quote dalla seconda apertura richiedono un collaudo proprio, e di che tipo.
2. **Coerenza delle decisioni D-24 … D-45** (ALLEGATO A) fra loro e con DGS-06 … DGS-11. In particolare:
   - D-36 (screening) con D-42 (obiettivo +0,25 R con potenza 50%);
   - D-37 (verdetto solo dal metro, veto per blocchi) con il vostro §4 di DGS-11;
   - D-43 (esposizione in R al posto dello stop obbligatorio).
3. **Specifica del modulo del verdetto** (ALLEGATO B, testo della specifica, non il codice): ci sono scelte che contraddicono DGS-10 §4 o DGS-11 §6? Per esempio:
   - un veto accertato boccia anche con dati inidonei o minimi mancanti;
   - un requisito non vincolante fallito dà «non decidibile»;
   - un intervallo più stretto di 1e-9 R è invalido (D-44).
4. **Casi a risposta esatta della prova generale a vuoto** (DGS-11 §7). Proponiamo che **li scriviate voi**, perché non avete scritto l'esecutore: 10–15 casi su dati inventati, con le coppie (S_d, K_d) o le operazioni e il verdetto atteso calcolato a mano. Devono includere:
   - costo contato una volta;
   - input mancante;
   - perdita oltre lo stop;
   - uguaglianza alle soglie +0,20 e +0,10;
   - veto accertato con L favorevole;
   - minimi non raggiunti;
   - intervallo degenere.

   Se il bootstrap rende impossibile il calcolo a mano, indicate i casi in cui il verdetto non dipende dal ricampionamento (per esempio dati inidonei, veto, minimi) e quelli per cui serve un riferimento indipendente.

5. **Ruolo di N nel verdetto di H-003** (domanda nuova, 20/11).
   - Con D-37 il verdetto lo dà solo il metro D-31; il DSR non è più un requisito. La molteplicità è governata dalla quota α_j/[j(j+1)]/m della riserva.
   - Il modulo ora legge N **solo** dal registro canonico e lo riporta nel verdetto con l'impronta del file. Rifiuta i registri ereditati e ogni quota diversa dal 2,5%.
   - Domanda: basta riportare N (con un DSR solo descrittivo), oppure N deve entrare in un requisito? In quel caso, quale, e come si raccorda con j e m?

Formato della risposta: un paragrafo per richiesta. I numeri vanno marcati «ricalcolato» o «preso dal messaggio».

ALLEGATO A — Decisioni D-24 … D-45 (testo del registro)

| N. | Data | Chi | Decisione | Fonte | Note | Stato |
|---|---|---|---|---|---|---|
| D-24 | 2026-11-17 | Utente | **Modello di minaccia della regola d'uscita** (proposta di Claude, «A con il giro B prima della verifica»): i due giri di revisione puliti di fila richiesti per il sigillo contano i difetti critici o importanti di tipo **E** (errori in buona fede: comandi sbagliati, file dimenticati, agenti IA fuori protocollo, dati incompleti) e di tipo **M a costo basso** (manomissioni facili). Le manomissioni elaborate (M a costo medio o alto) si registrano lo stesso, si correggono quando costa poco, altrimenti si dichiarano come limiti. **Prima della verifica sulla riserva** serve in più un giro dedicato a TUTTE le manomissioni, senza difetti critici o importanti, e la decisione sulla protezione del ramo su GitHub | Conversazione con Claude del 17/11/2026 | Il rischio concreto sono gli errori e l'autoinganno; la verifica è il solo passo irreversibile, quindi lì la severità è massima. La classificazione E/M e il costo li dà il revisore, il titolare decide i casi dubbi | attiva |
| D-25 | 2026-11-17 | Utente | **Protocollo DGS-07 adottato «così com'è»** per scegliere e validare il metodo del test IA-02 su dati inventati: 8 candidati (HAC o bootstrap × margine 0; 0,01; 0,025; 0,05 R), fase 1 a 3.000 repliche con classifica meccanica, fase 2 a 12.000 repliche nuove solo per il vincitore (limite unilaterale 99,9%), cella 11 con veto, diagnostica dei flussi, un solo tentativo. Impegnato prima della lettura (`laboratorio/studi/IMPEGNO-PROTOCOLLO-IA02.md`, protocollo SHA-256 70d8562a…) | Risposta del titolare a Claude, 17/11/2026 sera | Non cambia IA-02, α, DA-31 né le regole della riserva. Se vince un margine sopra zero, usarlo nella regola futura resta una decisione del titolare. Le diagnostiche di fase 0 viste da Claude sono dichiarate: la fase 1 resta sviluppo | attiva |
| D-26 | 2026-11-18 | Utente | **#112 non conta per D-24**: è un difetto del pilota del collaudo, fuori dal perimetro sigillato. R16 è quindi il **primo giro pulito: contatore 1 su 2** | Risposta del titolare a Claude, 18/11/2026 | Su proposta di Claude, che aveva segnalato il caso come dubbio (D-24: il titolare decide i casi dubbi) | attiva |
| D-27 | 2026-11-18 | Utente | **#114 si corregge subito** (opzione b): nuovo candidato, e R17 rifà le prove toccate (criteri) | idem | Consiglio di Claude: correzione di una riga; meglio arrivare al sigillo senza difetti noti nel perimetro | attiva |
| D-28 | 2026-11-18 | Utente | Nei mandati a Gemini si chiede di scrivere `~` al posto dei percorsi locali completi, che contengono il nome dell'utente | idem | I file già consegnati non si modificano (D-11) | attiva |
| D-29 | 2026-11-14 (trascritta il 18/11) | Utente | **DA-26, partizione dei dati («inversione»):** sviluppo = dal 15/11/2023 in poi (già visto); **verifica sigillata = 2005 → circa 31/10/2023**, date esatte dopo il conteggio dei buchi, con embargo prima dello sviluppo. Nessuno guarda la verifica: dati, grafici, TradingView. Il 13/11 era stato deciso di scaricare XAUUSD dal 2005 | `DECISIONI-APERTE.md` DA-26 (decisione dell'utente del 14/11) | Trascritta su richiesta del titolare (18/11) perché risultava solo fra le decisioni aperte. Restano aperte: date esatte e regole di spesa della riserva | attiva |
| D-30 | 2026-11-13 (trascritta il 18/11) | Utente | **DA-29, obiettivi:** weekend chiuso (nessuna posizione aperta nel weekend, anche nei backtest); obiettivo «essere in positivo», l'1–2% al mese su un futuro conto FTMO da 100.000 va benissimo; sfida FTMO solo dopo più strategie testate; arresto «quando la probabilità non è a nostro favore», da tradurre in numeri | `DECISIONI-APERTE.md` DA-29 (decisione dell'utente del 13/11) | Trascritta come sopra. Le proposte di Claude in DA-29 (obiettivi in R, soglie, arresto in demo con il test di Wald, overnight) restano **proposte** | attiva |
| D-31 | 2026-11-18 | Utente | **Regola di IA-02 in verifica: opzione A di DGS-08 §4c.** Si usa il metro collaudato così com'è: bootstrap circolare a blocchi (ℓ = 10, B = 3.999, basic) con margine Δ = 0,05 R. Promozione solo se il limite inferiore grezzo supera **+0,20 R**, bocciatura se il limite superiore è sotto **+0,10 R**; per il resto restano i requisiti di DA-31. Vale nel perimetro collaudato (circa 1.000 sedute, quota 2,5%); una quota diversa (seconda apertura, più varianti) richiede una giustificazione o un collaudo specifico (DGS-08) | Risposta del titolare a Claude, 18/11/2026 | Il titolare punta a strategie con guadagni più alti, compatibili con un metro severo. La regola dello **screening sullo sviluppo** (orientamento: sulla stima) resta da decidere | attiva |
| D-32 | 2026-11-19 | Utente | **Primo passo del modello H-003 secondo DGS-10 §5:** approvate e applicate al modello in vigore tre parti, nel testo di DGS-10 §3: provenienza dell'idea e regole sul revisore (G, al §0); stato della coppia domanda–finestra con i tre stati vista / esposizione incerta / ammissibile, che ratifica il criterio di accesso proposto in DGS-09 (H, al §2); tracciabilità dei giri di revisione (F, al §11). Il modello nel suo insieme resta da approvare | Risposta del titolare a Claude («procedi»), 19/11/2026 | Restano aperte, prima del sigillo della prima scheda: DA-31 (due o tre esiti) con la politica di riesame, la regola dello screening, minimi e anni valutabili (D), costi (J), unità e confronti (A–C), applicazione di I | attiva |
| D-33 | 2026-11-19 | Utente | **Prima la macchina, poi le strategie.** Il lavoro sulle idee di Market Mechanics (P-001: corso, catalogo delle operazioni dal vivo, adattamenti) è **in pausa** finché l'infrastruttura che valuta le strategie non è finita. I prompt preparati il 19/11 per la chat delle strategie e per Gemini non si inviano | Messaggio del titolare a Claude, 19/11/2026 | Coerente con DGS-09 §0 e §2a (prima la base sull'oro). Claude riconosce di aver anticipato il lavoro sulle strategie contro l'ordine concordato. Il registro della provenienza resta valido per quanto già raccolto | attiva |
| D-34 | 2026-11-19 | Utente | **Definizione di fatto della macchina (opzione 1-A):** il contatore D-24 si chiude sul perimetro attuale: R17 sul candidato e476a9a, poi il giro su tutte le manomissioni. Il criterio D-31 e il registro unico delle prove (N) diventano un **modulo nuovo**, con **2 giri di revisione propri** limitati a quel modulo e un collegamento con l'esecutore coperto da test. **Elenco chiuso di ciò che manca:** (1) criterio D-31 nel codice; (2) registro unico di N; (3) clausola sulle code: stop obbligatorio e perdita massima per trade dichiarata; (4) rapporti con tipo e incertezza su ogni numero; (5) prova generale a vuoto superata; (6) R17 e giro su tutte le manomissioni; (7) unione in `main` con la protezione del ramo. Ciò che non è in elenco si corregge a lotti e non riapre il contatore | `governance/DECISIONI-DA-PRENDERE-20261119.md`, decisione 1; risposta del titolare, 19/11/2026 | Il titolare: «nel caso servissero altre revisioni lo modifichiamo». L'elenco si può cambiare solo con una nuova decisione | attiva |
| D-35 | 2026-11-19 | Utente | **DA-31: tre esiti** (opzione 2 di DGS-10 §4, con la sua tabella delle priorità): bocciata per veto; non decidibile per prova inidonea o minimi mancanti; bocciata statisticamente (U < +0,10 R); promossa (L > +0,20 R e requisiti superati); ogni altro caso non decidibile. **Riesame (opzione y):** una variante «non decidibile» si archivia e può essere riprovata **solo con dati nuovi, cioè la demo futura**, come prova nuova contata in N (DA-19), senza un'altra spesa di riserva storica. Ogni verifica avviata consuma comunque date e quota | idem, decisione 2 | Chiude DA-31 | attiva |
| D-36 | 2026-11-19 | Utente | **Regola dello screening sullo sviluppo (opzione 3-C):** una variante può chiedere la verifica solo se sullo sviluppo vale **R medio netto > +0,25 R** **e** il limite inferiore dello stesso bootstrap è **> 0**, **e** se la potenza stimata della verifica è **≥ 50%**, calcolata con una procedura congelata nella scheda prima del sigillo. Confronti stretti: l'uguaglianza non passa | idem, decisione 3 | Motivo: la riserva basta per circa 4 verifiche; sotto +0,25 R la potenza della prima verifica è sotto il 25% (stima). Completa D-31 e il testo I di DGS-10 | attiva |
| D-37 | 2026-11-19 | Utente | **Minimi e anni (opzione 4-A):** il verdetto lo dà **solo il metro D-31**. Gli anni civili e i blocchi da 250 sedute si riportano come descrizione; un blocco diventa **veto** solo se la sua media è sotto una soglia fissata nella scheda prima del sigillo (proposta: −0,25 R). **Minimi tecnici:** D = 1.000 sedute scelte per calendario prima dell'apertura, almeno 300 trade, almeno 200 sedute con trade. Sotto i minimi l'esito è «non decidibile» | idem, decisione 4 | Risolve l'incoerenza «ultimi 5 anni» con verifiche di circa 4 anni (DGS-10 §6). I criteri annuali di `criteri.verifica` (H-002) restano nel perimetro attuale: valgono per H-002, non per H-003 | attiva |
| D-38 | 2026-11-19 | Utente | **Regole di spesa della riserva (opzione 5-A):** α totale **5%**, quota α_j = α/[j(j+1)]/m, **nessuna parte protetta**, riesame dopo la prima verifica. Restano da fissare dopo il consuntivo dell'ASK: date esatte, embargo (proposta: 10 giorni di borsa), quarantena dei giorni con dati scarsi (proposta: oltre il 5% dei minuti mancanti su BID o ASK nella fascia operativa) | idem, decisione 5 | Il registro vero della riserva si crea solo dopo la decisione sulle date | attiva |
| D-39 | 2026-11-19 | Utente | **Custodia dei dati (opzione 7-A):** a ASK finito, copia finale con impronta su chiavetta o disco esterno più il cloud, con la stessa impronta SHA-256 verificata su ogni copia | idem, decisione 7 | `piano/PROCEDURA-ASSISTENZA-MAC.md`, passi 3–4 | attiva |
| D-40 | 2026-11-19 | Utente | **Niente previsioni giornaliere del titolare per ora** (decisione 8, «no»). **Il divario fra metro e obiettivi (decisione 6) si decide dopo la risposta del DGS al messaggio 9** | idem, decisioni 6 e 8 | Motivo del titolare per la 8: le sue previsioni confonderebbero il lavoro; sta studiando con la chat delle strategie le strategie di trader esterni | attiva |
| D-41 | 2026-11-19 | Utente | **Eccezione limitata a D-33:** dopo la revisione di DGS-11, Claude prepara una **valutazione approfondita della fonte P-001** (Brad Goh): canali, storico dei video, operazioni dichiarate, personalità e stile del canale, modello di business, verificabilità dei risultati. **Non comprende:** schede, varianti, prove sul banco, grafici XAUUSD o GBPJPY anteriori al 15/11/2023 | Messaggio del titolare a Claude, 19/11/2026 | Claude è già contributore di P-001 (non revisore indipendente). Regole del catalogo P-001: nessun video scaricato, solo testo con link e minuto; le dichiarazioni dell'autore non sono prove. La macchina resta la priorità (D-34) | attiva |
| D-42 | 2026-11-19 | Utente | **Metro contro obiettivi (DGS-11 §5; riscontro §5 a): si conferma come obiettivo del progetto l'effetto minimo di +0,25 R a trade con potenza del 50%** (già usato nello screening, D-36). Il metro D-31 resta com'è; si candidano alla verifica solo idee che possono raggiungerlo (opzione A1) | Risposta del titolare a Claude, 19/11/2026: «sì (confido nelle nostre capacità di costruirla insieme tra idee altrui etc.)» | Chiude la decisione 6 (D-40) | attiva |
| D-43 | 2026-11-19 | Utente | **Clausola sulle code (modifica il punto 3 dell'elenco di D-34), proposta del DGS:** ogni scheda dichiara in modo verificabile l'**esposizione massima per trade in R** (salto di prezzo peggiore plausibile diviso la distanza dello stop, con fonte e periodo). Si richiede un collaudo nuovo solo se l'esposizione esce dal dominio provato. Niente tetto universale né «stop obbligatorio» come garanzia | idem («accetto la proposta di chat») | Motivo: uno stop non garantisce il prezzo nei salti (DGS-11 §2); l'esempio rifatto mostra il rischio solo con code di decine di R (riscontro §2) | attiva |
| D-44 | 2026-11-19 | Utente (delegata a Claude) | **#119:** nel modulo del verdetto un intervallo più stretto di **1e-9 R** è invalido; il pilota collaudato resta congelato | idem («decidi tu») | Scelta di Claude: 1e-9 R è la stessa banda dei casi a filo di DGS-10 testo I; nessun dato reale produce intervalli così stretti | attiva |
| D-45 | 2026-11-19 | Utente | **Modo di esecuzione di una strategia certificata (orienta DA-30):**<br>(1) prima, alert sul telefono con ingresso, stop, target, lotto e esito del Guardian; il titolare inserisce l'ordine o salta il trade e annota il motivo;<br>(2) **solo se la demo va bene**, ordine già compilato in MetaTrader da confermare con un tocco;<br>(3) l'esecuzione completamente automatica, senza conferma, **non è autorizzata**: richiederebbe una nuova autorizzazione esplicita | Risposta del titolare a Claude, 19/11/2026 («una volta che la strategia è testata e certificata faremo così», riferito al passaggio citato) | Coerente con D-14 e D-16. Le ore operative dipendono da DA-32 | attiva |

ALLEGATO B — Specifica del modulo del verdetto (`laboratorio/verdetto/verdetto_d31.py`)

Verdetto della verifica secondo D-31, D-35, D-36 e D-37 (19/11/2026). Modulo nuovo fuori dal perimetro sigillato
(D-34): ha i suoi due giri di revisione.

- Metro: l'implementazione di riferimento collaudata (`studi/pilota_ia02.intervallo_bootstrap`), cioè bootstrap circolare
  a blocchi da 10, B = 3.999, intervallo basic, quota 2,5% per coda. Il modulo si rifiuta di calcolare se l'impronta
  del pilota non è quella congelata nell'impegno del collaudo (IMPEGNO-PROTOCOLLO-IA02.md).
- Segnale (D-31): favorevole se L > +0,20 R, sfavorevole se U < +0,10 R, altrimenti inconclusivo; un intervallo
  mancante, non finito, invertito o più stretto di 1e-9 R (#119, D-44) è invalido. L'uguaglianza non attraversa la soglia.
- Esiti (D-35, DGS-10 §4 opzione 2), nell'ordine: veto accertato → bocciata; dati inidonei, minimi mancanti o intervallo
  invalido → non decidibile; U < +0,10 → bocciata; L > +0,20 e requisiti superati → promossa; altrimenti non decidibile.
- Screening sullo sviluppo (D-36): media > +0,25 R, L > 0 e potenza stimata ≥ 50%.
- Veto per blocchi (D-37): soglia e minimo di trade per blocco li fissa la scheda prima del sigillo.

Vale solo per la prima apertura con una variante (quota 2,5%): una quota diversa richiede un collaudo (D-31).

Funzioni: `segnale(iv)`, `vicini(L, U)`, `controlla_coppie`, `minimi_mancanti`, `intervallo(coppie, seme)`, `verdetto(coppie, seme, requisiti)`, `screening(coppie, seme, potenza_stimata)`, `veto_blocchi(coppie, soglia, minimo_trade_blocco, ampiezza=250)`. Verifica: 31 test, mutanti 47/48 su Python 3.13 e 3.9 (un equivalente dichiarato).

---
