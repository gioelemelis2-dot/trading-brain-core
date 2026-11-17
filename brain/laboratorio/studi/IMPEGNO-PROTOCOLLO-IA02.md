# Impegno del protocollo DGS-07 per il collaudo del metodo IA-02

**Data dell'impegno:** 17/11/2026, sera, prima di qualunque lettura dei risultati della fase 1.
**Adottato da:** il titolare, «così com'è» (D-25). Claude registra e applica; non sceglie.

## 1. Identità

| Oggetto | Valore |
|---|---|
| Protocollo | `collaborazione/da-chatgpt/DGS-20261117-07-protocollo-ia02.md`, SHA-256 `70d8562af07a748c9b82a4c9a7b0fa027477effa9937fc5d019b7bfaa3af1af2` (copia senza modifiche del file consegnato) |
| Disegno di riferimento | `collaborazione/da-chatgpt/DGS-20261117-06-riscontro-risposta-7.md` §2c, SHA-256 `b8c37689ca3536c06f7bdce4d0802e2a1eb634e6476cc2265b7c6bdea62a3f41` |
| Versione del pilota della corsa già avviata | `laboratorio/studi/pilota_ia02.py` del commit `e72fc68` (invariato fino a `fc0c639`), SHA-256 `2b9a313634c603a67a3c87e42628c157c0a2fb3623fac58a57a6da23d451cc5a` |
| Ambiente | CPython 3.13.18 su Linux (contenitore di Claude), solo libreria standard. La fase 2 gira nello stesso ambiente. Non si sommano repliche ottenute su Python diversi |
| Semi | `random.Random(int.from_bytes(SHA-256(f"{master}:{fase}:{cella}:{replica}:{componente}".encode()), "big"))`: digest completo, interi decimali separati da «:», nessun `hash()` di processo, nessun orologio. Master 2026111706. Componenti: 0 dati o componente comune, 1 conteggi, 2 innovazioni individuali, 3 bootstrap |
| Matrice | 12 celle di DGS-06 §2c (1–4 iid, 5–8 AR(1) ρ = 0,25, 9–10 conteggi, 11–12 perdite rare), μ come da disegno |
| Candidati | {HAC L = 6; bootstrap circolare ℓ = 10, B = 3.999, basic} × Δ ∈ {0; 0,01; 0,025; 0,05} R |
| Fase 1 | M₁ = 3.000, fase = 1. Controlli: k ≤ 60 (U_CP unilaterale 95% ≤ 0,025) nelle celle 2, 6, 9, 11 (falsa promozione e falsa bocciatura) e 1, 5 (falsa promozione); P ≥ 1 nelle celle 3, 7, 10, 12. Classifica di DGS-07 §2a.5 |
| Fase 2 | solo il vincitore, M₂ = 12.000, fase = 2, repliche 1…12.000. Controlli: k ≤ 248 (U_CP unilaterale 99,9% ≤ 0,025), stesse celle; diagnostica dei flussi di DGS-07 §2b (216 confronti, banda 4.796…5.204); un solo tentativo |

## 2. Chi ha visto che cosa (attestazione di Claude)

- **Fase 1:** nessuno ha visto risultati. La prima corsa (avviata alle 22:3x circa) è stata fermata prima di stampare: il suo file d'uscita è vuoto (0 byte). La seconda corsa, avviata alle 22:51 da `fc0c639`, scrive solo su file; Claude non l'ha aperto e ne registrerà soltanto impronta e numero di righe.
- **Fase 0 (diagnostiche viste da Claude mentre scriveva i test; dichiarate perché DGS-07 §2a.1 lo chiede):**
  - prova di velocità su 5 repliche delle celle 1, 9, 11, solo tempi;
  - test di cella con 6 repliche della cella 1 (B = 99), solo la coerenza dei conteggi;
  - scelta dei casi del test di classificazione: 40 repliche, B = 99, celle 2, 3, 7. Visti i conteggi: cella 2 (μ = 0,15) 0/40 promozioni con entrambi i metodi; cella 3 (μ = 0,20) 8/40 HAC e 11/40 bootstrap; cella 7 (μ = 0,20) 7/40 HAC e 8/40 bootstrap; limiti tra 0,10 e 0,15 in 7–19 casi su 40; poche mancate coperture.
  Sono repliche di fase 0 (semi diversi dalla fase 1), poche e con B = 99. Non bastano a prevedere l'esito dei controlli, ma sono diagnostiche rivelatrici in senso largo: per DGS-07 la fase 1 resta **sviluppo**, e questo impegno **non** si descrive come anteriore a ogni lettura. La fase 2 è prospettica: nessuna sua replica è stata generata.
- Gemini e ChatGPT non hanno visto risultati del pilota.

## 3. Correzioni prima della lettura

- **#112 (errore di Claude):** il bootstrap del pilota restituiva un intervallo di ampiezza nulla come valido, contro DGS-06 §2c («limiti non finiti, invertiti o intervalli di ampiezza nulla sono non stimabilità»). Il test rosso si aspettava `(2.0, 2.0)` su un caso degenere e il codice è stato adattato al test invece che al disegno. Succede solo con dati costanti: nella cella 11, una replica senza perdite (probabilità circa 0,99^1000 ≈ 0,004%). Con i conteggi di DGS-07 (k⁺ = P + E, k⁻ = B + E) non cambia nessun controllo; può solo spostare un caso da P a E.
- **Limiti grezzi:** la corsa avviata registra solo conteggi a margine zero, che per DGS-07 §2a.1 non bastano per gli altri margini. Si prepara una **riproduzione identica** (stessi semi, stessi generatori, stessi metodi) che salva i limiti grezzi (L, U) o l'errore per replica, metodo e cella; il rendiconto del protocollo si calcola su quei limiti. La corsa già avviata non si altera: dopo l'apertura, i suoi conteggi a margine zero devono coincidere con quelli della riproduzione, salvo i casi di #112 (dichiarati uno per uno).
- **Strumenti da costruire in TDD prima della lettura:** salvataggio dei limiti grezzi; rendiconto del protocollo (E, P, B, I, k⁺, k⁻, U_CP, esiti, classifica, verdetto, completezza); inventario dei semi delle fasi 1 e 2 senza duplicati; diagnostica dei 216 confronti; prova che l'ordine dei processi non cambia i risultati.
