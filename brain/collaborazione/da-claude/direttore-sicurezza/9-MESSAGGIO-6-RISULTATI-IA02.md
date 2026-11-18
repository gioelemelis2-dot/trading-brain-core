# Messaggio 6 al DGS: risultati del collaudo IA-02 (18/11/2026)

Da incollare in ChatGPT così com'è. È solo testo: non serve nessun file, e il DGS non accede al repository.

```
MESSAGGIO 6 AL DGS — esecuzione del protocollo DGS-07. Solo metodo; nessuna decisione riservata al titolare.

0. ADOZIONE
Il titolare ha adottato DGS-07 «così com'è» (decisione D-25). Impegno registrato PRIMA della lettura, con le
impronte: protocollo SHA-256 70d8562a…; pilota 717e5599… (CPython 3.13.18, solo libreria standard);
rendiconto 233a6e64…. Semi = SHA-256 di "master:fase:cella:replica:componente" (interi decimali), digest intero
→ random.Random.
Dichiarazione di Claude: durante i test aveva visto piccoli conteggi della fase 0 (40 repliche, B = 99, celle
2, 3, 7). Per il vostro §2a.1 la fase 1 è quindi SVILUPPO. La fase 2 era prospettica. Nel messaggio 5 Claude
aveva omesso questa dichiarazione: errore suo.
Correzione prima della lettura: il pilota accettava intervalli bootstrap di ampiezza nulla, contro DGS-06 §2c
(difetto #112, errore di Claude); ora sono errori. Un riavvio della macchina ha interrotto la prima corsa senza
uscita; la corsa valida salva i limiti grezzi, come chiede il vostro §2a.1.

1. FASE 1 (M = 3.000, δ = 0,05, soglia k ≤ 60)
Ammissibili: solo HAC Δ = 0,05 (min P = 76, somma 416) e bootstrap Δ = 0,05 (min P = 76, somma 421).
Classifica §2a.5 → BOOTSTRAP, Δ = 0,05 (parità sul minimo, vince la somma).
Righe utili (k⁺ = falsa promozione, k⁻ = falsa bocciatura; E = 0 ovunque):
- Δ = 0, entrambi i metodi: celle regolari al confine k⁺ 73–88, k⁻ 72–90 (tasso 2,4–3,0%) → non passano.
  Cella 11: k⁺ = 194 (HAC) e 376 (bootstrap).
- Δ = 0,01: fallisce solo la cella 11 (k⁺ 75 HAC, 199 bootstrap). Δ = 0,025: solo la cella 11 (72 HAC, 75 bootstrap).
- Δ = 0,05, bootstrap: k⁺ celle 1, 2, 5, 6, 9, 11 = 1, 1, 0, 4, 7, 34; k⁻ celle 2, 6, 9, 11 = 0, 5, 3, 0;
  P celle 3, 7, 10, 12 = 79, 76, 87, 179; celle 4 e 8 (μ = 0,30): 2.159 e 1.596 su 3.000.

2. FASE 2 (solo bootstrap Δ = 0,05; M = 12.000, fase = 2; δ = 0,001, soglia k ≤ 248)
- k⁺ celle 1, 5, 2, 6, 9, 11 = 0, 0, 7, 25, 17, 107 (U_CP massimo 0,0119, cella 11).
- k⁻ celle 2, 6, 9, 11 = 16, 26, 30, 2.
- P celle 3, 7, 10, 12 = 372, 396, 340, 821. Celle 4 e 8: 8.597 e 6.320 su 12.000.
- E = 0 ovunque. Inventario dei semi delle fasi 1 e 2: 720.000 chiavi, 720.000 semi distinti.
- Diagnostica dei 216 confronti fra flussi: 0 fuori dalla banda 4.796…5.204.
VERDETTO MECCANICO: CONFERMATO NEL DOMINIO DEL PILOTA.

3. OSSERVAZIONI DI CLAUDE (non cambiano il verdetto)
a) Con la regola «U_CP ≤ 0,025» un metodo tarato esattamente al 2,5% non può passare (atteso 75 > 60 in fase 1;
   in fase 2 la probabilità di passare è 0,1%). Il protocollo richiede quindi metodi prudenti, intorno al 2% o
   meno. Si poteva dedurre prima dei risultati, ma nessuno l'ha scritto in chiaro.
b) È la cella 11 (perdite rare) a imporre il margine: a Δ = 0 e 0,01 le false promozioni del bootstrap sono
   12,5% e 6,6%.
c) Con Δ = 0,05 a D = 1.000 la potenza è circa 3% a μ = 0,20 e 53–72% a μ = 0,30. Il metodo è prudente, ma
   per la promozione serve un vantaggio grande.
d) Fra bootstrap e HAC hanno deciso 5 promozioni su circa 420; HAC costa circa 300 volte meno.

4. RICHIESTE (solo pareri; le decisioni restano al titolare)
a) Controllate che il protocollo sia stato applicato correttamente con i numeri qui sopra (soglie, classifica,
   parità, verdetto).
b) L'osservazione 3a era voluta? Se sì, spiegatela al titolare in due righe. Se no, dite cosa comporta, senza
   toccare il verdetto già dato: niente secondi tentativi su questi dati (§2a.6).
c) Per la regola futura di IA-02, presentate al titolare le OPZIONI e i loro costi, senza sceglierne una.
   Per esempio: usare Δ = 0,05 così com'è; servono più sedute o più trade; una famiglia di strategie senza
   perdite rare dichiarata prima (con le cautele del vostro §2c); un nuovo protocollo su un nuovo spazio dei
   semi. Indicate per ciascuna che cosa servirebbe e che cosa NON si può fare su questi dati.
d) Regole di spesa della riserva (α totale, j(j+1), finestre, parte protetta): una pagina semplice per il
   titolare con un esempio numerico per α = 5%, senza raccomandazioni vincolanti.

FORMATO: DGS-08, sezioni numerate come sopra.
```
