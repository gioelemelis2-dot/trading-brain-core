# Proposte di correzione per la V3.3 (errata, da eseguire da Antigravity dopo l'approvazione dell'utente)

Riferimento: [`CLAUDE_FINAL_REVIEW_V3_3.md`](CLAUDE_FINAL_REVIEW_V3_3.md). **Nessuna proposta è stata applicata.** Nessuna è bloccante e nessuna cambia un risultato numerico.
Consiglio di applicarle come **errata** all'inizio della fase successiva, senza un nuovo ciclo di revisione completo. La mia verifica si limiterebbe a: script di mutazione, due test, ricerca testuale.

## T-01 · Analisi di mutazione riproducibile · Media
- **Modifica:**
  1. includere nel pacchetto lo script di mutazione effettivamente usato, oppure adottare `v33_d_mutazioni.py` (stesse definizioni pubblicate da Claude) e allegarne l'uscita;
  2. se si usano definizioni proprie, rinumerarle o dichiararne la differenza;
  3. togliere «uccisi determinatamente» per V22, oppure aggiungere un test deterministico che lo uccida davvero. Per esempio: μ = 0,05, R:R 2, u fissato a 0,5; confrontare `-sample_brownian_mae_given_win(Fisso(0.5), 2.0, 0.05)` con l'inversione esatta calcolata nel test (tolleranza 10⁻¹²). A soglia 0,1 il mutante usa la formula a deriva nulla e il valore cambia alla terza cifra.
- **Test di accettazione:** l'uscita dello script allegato coincide con la tabella del report; con `v33_d_mutazioni.py` sopravvivono solo V01 (e V22, se non si aggiunge il test).

## T-02 · Precisione dei valori esatti · Bassa
- **Modifica:** riportare 0,77998 / 0,85717 / 0,66858 (oppure 4 cifre senza zeri finali), etichettati «esatti (programmazione dinamica in avanti sul reticolo, `c1_esatto_challenge.fase` della revisione V2 di Claude)». Rimuovere «backward induction» e «verifiche matematiche indipendenti» dalla sezione 1, oppure includere il codice usato.
- **Test di accettazione:** ricerca testuale di 0,780000, 0,857200 e 0,668616: nessuna occorrenza.

## T-03 · Attribuzione nel README · Media
- **Modifica:** `README.md:4` → «Proposte di correzione: Claude Code (revisione V3.2). Revisione indipendente della V3.3: Claude Code, `CLAUDE_FINAL_REVIEW_V3_3.md`, esito: validata con riserve». Usare sempre lo stato effettivo, mai un ruolo al futuro.
- **Test di accettazione:** ricerca di «Revisione Indipendente: Claude» solo accanto a un riferimento a un documento esistente e al suo esito.

## T-04 · Copertura dei test · Bassa
- **Modifica:** aggiungere due test:
  1. **configurazione irraggiungibile:** `PropSimulationScenarioV3_3("x", 0.40, 0.001, use_brownian_mae=True)` solleva `ValueError` (uccide V16);
  2. **deriva negativa:** WR 0,05 / R:R 0,1 e WR 0,90 / R:R 0,02. |P_win(μ) − WR| < 10⁻¹², calcolato nel test con la formula indipendente (1 − e^{2μ})/(e^{−2μ·R:R} − e^{2μ}) senza le funzioni del motore (uccide V24).
- **Test di accettazione:** con `v33_d_mutazioni.py`, V16 e V24 uccisi; la suite resta verde.

## T-05 · Dettagli · Minima
- Completare l'espressione di §3.1 del documento matematico.
- Allineare §5, il commento della riga 145 e il limite effettivo `high = min(15.0, 345.0)`: dichiarare 15, oppure portare la ricerca a 345.
- `LEGGIMI_V1.md`: percorsi relativi alla cartella del pacchetto; import citato come blocco multilinea.
- Rimuovere `V3_3_MANIFEST.sha256` o includerlo nel manifest.
