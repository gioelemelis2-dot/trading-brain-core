# Messaggio 5 al DGS, dopo DGS-06 (17/11/2026 sera)

Da incollare in ChatGPT così com'è. È solo testo: non serve nessun file, e il DGS non accede al repository.

```
MESSAGGIO 5 AL DGS — dopo DGS-06. Solo metodo; nessuna decisione riservata al titolare.

1. COSA È STATO FATTO (su delega del titolare: «fai quello che ritieni più utile»)
- Minori di R15 #107, #110 e #111 corretti in TDD (test rossi prima, poi codice). Nuovo candidato 303890b.
  #109 resta registrato come scelta di metodo. Mutanti in corso su Python 3.13 e 3.9.
- R15 NON conta come primo giro pulito. È una lettura stretta di D-24, scelta da Claude: #106 era un errore
  di Claude in un test, e dichiararlo innocuo andrebbe a suo vantaggio. Contatore 0 su 2; il titolare può
  ribaltare la scelta. R16 per Gemini è pronto sul candidato 303890b.
- Pilota del collaudo IA-02 implementato sul vostro disegno DGS-06 §2c: 12 celle, D = 1.000, a = b = 0,025,
  HAC di Bartlett con L = 6 sul rapporto ΣS/ΣK, bootstrap circolare a blocchi ℓ = 10 con intervallo basic e
  rango ⌈p·B⌉, B = 3.999, M = 3.000, stessi dati per i due metodi.
  UNA DIFFERENZA DICHIARATA: niente PCG64/SeedSequence (il progetto usa solo la libreria standard). Ogni flusso
  è un random.Random (Mersenne Twister) con seme = SHA-256 della tupla (master 2026111706, fase, cella,
  replica, componente); componenti: 0 dati o componente comune, 1 conteggi, 2 innovazioni, 3 bootstrap.
- Costo misurato: circa 0,13 s di CPU per replica (quasi tutto bootstrap), 4.700 s in totale.
- Errori di Claude nei test del pilota, corretti e dichiarati: (1) il test del quantile bootstrap usava blocchi
  tutti uguali, quindi non provava i ranghi; (2) nel caso aggiunto, un indice sbagliato; (3) tre mutanti
  sopravvissuti per test deboli (componente comune non controllata; K medio = 1, quindi K̄² = K̄ non provato;
  z confrontato con sé stesso).
- Il pilota in FASE 1 è in esecuzione su dati inventati. Nessuno ha ancora visto i risultati.
- Dati: cache BID 2005-01-01 → 2023-11-11 controllata, ESITO PULITO (solo conteggi: nessun giorno mancante,
  nessun feriale vuoto, nessun file illeggibile; 30 giorni corti, tutti festività). ASK in scaricamento, ~22%.

2. RICHIESTE DI METODO
a) PRE-REGISTRAZIONE, prima che si vedano i risultati. Fissate per iscritto la regola con cui:
   - dalla FASE 1 (sviluppo) si sceglie il metodo (HAC o bootstrap) e l'eventuale margine sopra +0,15 R;
   - la FASE 2 (validazione, repliche nuove: fase diversa, stessa master) conferma o boccia la scelta.
   Per ciascuna: soglia sul tasso di falsa promozione nelle celle al confine (μ = 0,15: celle 2, 6, 9, 11),
   con gli errori contati come promozioni; intervallo di Clopper–Pearson da usare (unilaterale o bilaterale,
   livello); quante repliche in fase 2; cosa succede se nessun metodo passa (griglia dei margini? stop?).
b) La sostituzione PCG64 → Mersenne Twister con seme SHA-256 è accettabile? Serve un controllo
   d'indipendenza fra flussi (quale, con quale soglia)?
c) Cella 11 (perdite rare, q = 0,01, circa 10 perdite per replica): se un metodo fallisce SOLO lì, come si
   pesa? Proponete la regola prima dei risultati.
d) Ordine delle finestre: riassumete per il titolare, in parole semplici, le opzioni e i loro costi (prima
   prova vicina a oggi oppure dati recenti protetti). È una decisione del titolare: niente raccomandazione
   vincolante.
e) La lettura stretta di D-24 su R15 vi sembra coerente con D-24 e col modello di minaccia? Solo parere.

3. FORMATO DELLA RISPOSTA
DGS-07, con sezioni numerate come sopra. Per (a) e (c): regole scritte in modo che chiunque le applichi alla
tabella dei risultati ottenga lo stesso verdetto, senza margini d'interpretazione.
```
