# Bozza di aggiornamento del modello di scheda H-003 (integrazioni P3 del DGS e DA-31)

**Stato: BOZZA, NON APPLICATA.** Preparata da Claude il 17/11/2026 pomeriggio su richiesta del titolare (decisione 5 della risposta 7). Il modello in vigore resta `MODELLO-SCHEDA-H-003.md`. Si applica solo con il via del titolare, e la parte sugli esiti solo dopo la ratifica di DA-31.

Per ogni punto: **[DOC]** è un aggiornamento documentale, cioè rende esplicito ciò che H-002 già fa; **[METODO]** è un cambio di metodo, che serve una decisione.

---

## A. Nuovo §5-bis «Unità e misura del risultato» [DOC]

> **R di un'operazione.** R_i = P/L netto dell'operazione i ÷ B_i, dove B_i è il budget di rischio in USD fissato **prima** dell'ingresso (in H-002: 500 USD, §5). Il denominatore non cambia dopo il risultato.
> - **Operazione** = un ingresso con tutte le sue uscite, parziali comprese, fino alla chiusura completa. Reingressi e aumenti di posizione: [DA COMPILARE] (vietati, oppure regola scritta).
> - **Numeratore:** comprende spread (già nei prezzi del lato eseguibile, da non sottrarre due volte), commissione [fonte], slittamento [modello dichiarato], eventuali costi di finanziamento. Uno stop con salto può costare più di 1 R.
> - **Estimando:** media di R per operazione della regola congelata, sulle opportunità del calendario. I giorni senza operazioni non sono trade a zero R; si contano a parte (frequenza, esposizione).
> - **Unità statistica:** la seduta. Per ogni seduta d si registrano S_d (somma degli R delle operazioni attribuite alla seduta d'ingresso) e K_d (numero di operazioni). Media per trade = ΣS_d / ΣK_d.

## B. §4 «Regole», nuova voce obbligatoria «Ambiguità sulla barra al minuto» [DOC]

> Il primo istante in cui ogni informazione è disponibile: [DA COMPILARE per ingresso, stop, target, uscita a orario].
> - Se nella stessa barra al minuto sono compatibili più percorsi (per esempio stop e target toccati), vale la regola **conservativa**, cioè lo stop prima del target, come in H-002 (`H-002-ORB-v3.md` riga 85; `orb_londra.py` righe 231–239, dove nel minuto d'ingresso conta solo lo stop). I casi si **contano** e si riportano.
> - Stessa regola scritta per ingressi e uscite vicini a un buco nei dati.
> - Ogni regola di ambiguità ha almeno un caso d'oro (§10).

## C. §6 «Metriche» e §7 «Prove e N»: confronti e gradi di libertà [DOC]

> - **Primario:** media di R netto per trade (A). Benchmark («compro sempre», «vendo sempre», confronto casuale) **sulle stesse date eleggibili**, con la stessa esecuzione e lo stesso rischio.
> - **Elenco chiuso** di ogni via di promozione: varianti, tagli ereditati (§0), veti, N e m (promozioni possibili nella stessa apertura). Una diagnostica usata per scegliere diventa una prova selezionabile e entra in N.

## D. §8 «Criteri»: coerenza del campione [METODO]

> - **Metodo dell'intervallo** per IA-02 in verifica: [DA SCEGLIERE dopo il pilota del collaudo: HAC con regola dei ritardi fissata, oppure bootstrap a blocchi delle coppie giornaliere (S_d, K_d)]. Quota unilaterale = quota della variante (P2).
> - **Minimo tecnico** (per calcolare le statistiche) e **minimo informativo** (trade necessari per la potenza dichiarata, con la dipendenza stimata nello sviluppo), entrambi scritti prima. Il minimo informativo si calcola dalla frequenza osservata nello sviluppo e dall'effetto minimo plausibile **motivato prima**.
> - **Anni:** definire gli anni parziali e gli «ultimi cinque anni». Una finestra senza cinque anni valutabili non può soddisfare il criterio 4 della verifica: va dichiarato prima se il criterio cade o se la finestra va allungata.

## E. §8 «Esiti» a tre stati (sostituisce il blocco «Esiti») [METODO, dipende da DA-31]

> | Esito | Regola scritta prima |
> |---|---|
> | **Promossa** | dati idonei; minimi raggiunti; **limite inferiore > +0,15 R**; tutti i requisiti vincolanti passati |
> | **Bocciata** | su una prova valida, **limite superiore < +0,15 R** (metodo: [DA SCEGLIERE]), oppure un veto terminale accertato su misure valide |
> | **Non decidibile** | dati insufficienti, statistica non stimabile, o intervallo che contiene +0,15 R, senza veto terminale |
>
> - Solo «promossa» fa avanzare.
> - «Non decidibile» **consuma le date e la quota della riserva** (non le restituisce).
> - **Riesame:** solo con dati **nuovi**, successivi all'ultima data vista, con la regola **congelata**, una prenotazione nuova e una prova in più in N.
> - Se cambia la regola o il disegno per recuperare l'esito, è un'**ipotesi nuova**.
> - **Conflitto da risolvere** (rilevato dal DGS): l'attuale frase «se nessuna variante passa, H-003 è chiusa» vale per «bocciata». Per «non decidibile» l'ipotesi resta **sospesa** fino al riesame preregistrato, oppure chiusa per scelta del titolare.

## F. §11 «Sigillo», tracciabilità dei giri di revisione [DOC, già in vigore per R15]

> Ogni giro di revisione che conta per la regola d'uscita dichiara: commit esatto, ambiente (sistema, versione e opzioni di Python), perimetro verificato e prove eseguite. Se tra due giri cambia il codice del perimetro, le prove toccate si rifanno sul candidato finale prima di contare entrambi i giri (D-24, parere P6 del DGS).

---

**Cosa NON cambia:** IA-02 (+0,15 R), il §0 sulla contaminazione, il divieto di eseguire prima del sigillo, la verifica una volta sola.

---

## Aggiornamento del 18/11/2026: decisioni D-31, DGS-07, DGS-08 e DGS-09

Anche queste voci sono **BOZZA, NON APPLICATA**: si applicano con il via del titolare, come il resto.

## G. Nuovo §0 «Provenienza dell'idea» [METODO, DGS-09 §1]
> - **Riga di provenienza** in `laboratorio/ipotesi/PROVENIENZA-IDEE.md`, compilata **prima** di questa scheda: fonte e versione, regola disponibile a quella data, informazioni dell'autore, selezione da parte nostra, destinazione.
> - **Che cosa viene dalla fonte e che cosa aggiungiamo noi**: due elenchi separati.
> - **Chi ha contribuito al disegno**: persone e chat, compresa la chat delle strategie. Serve a scegliere un revisore indipendente (DGS-09 §3).

## H. §9 «Verifica»: stato della finestra candidata [METODO, DGS-09 §1b e §2b]
> Per ogni finestra candidata della riserva: **vista per questa domanda / esposizione incerta / ammissibile in linea di principio**, con la motivazione e il rimando al censimento del mercato (per esempio `governance/censimento/CENSIMENTO-GBPJPY.md`). Si prenota solo una finestra ammissibile.

## I. §8 «Criteri»: regola di verifica di D-31 e dominio collaudato [METODO, DGS-08 §4c, DGS-09 §2c]
> - **Verifica:** bootstrap circolare a blocchi (ℓ = 10, B = 3.999, intervallo basic) con Δ = 0,05 R. Promozione se il limite inferiore grezzo supera **+0,20 R**, bocciatura se il limite superiore è sotto **+0,10 R** (D-31).
> - **Corrispondenza al dominio collaudato**, da motivare con le sole informazioni ammesse dello sviluppo:
>   - numero di sedute vicino a 1.000;
>   - quota del 2,5% per coda;
>   - operazioni per seduta, dipendenza, dispersione e perdite rare comparabili con le 12 celle del pilota.
>   Se una condizione materiale cambia (per esempio la quota scende all'1,25% per una seconda variante o una seconda apertura), serve una giustificazione specifica o un collaudo preregistrato su repliche nuove **prima** dell'uso.
> - **Pareggi alle soglie** (#116): limiti a meno di 1e-9 dalla soglia vanno contati e dichiarati nel rendiconto, con la regola di pareggio fissata prima.
> - **Screening sullo sviluppo:** regola da decidere (orientamento del titolare: sulla stima).

## J. §5 «Costi» [DOC, Gate 1]
> Commissione e spread **fissati prima dei dati** da `dati/costi/` (specifiche del broker rilevate e spread per ora UTC misurato con `dati/pipeline/costi_tick.py` sullo sviluppo). Il costo in R dipende dalla distanza dello stop: va riportato per la distanza tipica della regola.
