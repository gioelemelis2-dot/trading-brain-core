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

## 4. Aggiunta prima della lettura (17/11, notte, dopo il riavvio del contenitore)

- La corsa avviata alle 22:51 da `fc0c639` **si è interrotta per il riavvio del contenitore senza scrivere nulla**: il file d'uscita è vuoto (0 byte), e nessuno ha visto risultati.
- **La corsa della fase 1 è quindi quella avviata alle 23:3x da `4d0c904`**: `pilota_ia02.py` del commit `4883dd9`, SHA-256 `717e55996b23a4954d69c97722458e30c2499000b5055fdcca4cba29f864b0ee` (contratto di #112 applicato, limiti grezzi salvati). Il rendiconto usa `protocollo_ia02.py`, SHA-256 `233a6e64ed634f8b95e9a8c8c90fa78b13acdbc5289e9c44cd3b2c17d9f09827`.
- Non c'è più una corsa «a conteggi soli» da confrontare: il confronto di §3 cade. Semi, generatori e metodi sono gli stessi dell'impegno.

## 5. Corsa della fase 1 finita, impronte registrate PRIMA dell'apertura

- Uscita 0, nessun messaggio d'errore. File dei limiti grezzi: 3.142.109 byte, SHA-256 `8ed698a9d6699caf8fd787a4f84b308573109127e1a127bdb525200d191d0edf`. Archiviato compresso (gzip -9 -n) in `laboratorio/studi/risultati/ia02/limiti_fase1.json.gz`.
- Tabella descrittiva del pilota (non aperta), SHA-256 `2c4fd7abad53c2c6729f91a9f05d85f845dbd44011f02556cd038b7c417119d4`.
- Intestazione del file (non sono risultati): versione `717e5599…`, fase 1, 3.000 repliche, B = 3.999, master 2026111706, celle 1–12, due metodi.
- Prossimo passo, meccanico: `protocollo_ia02 --limiti … --fase 1`, poi la classifica di DGS-07 §2a.5 così com'è.

## 6. Esito meccanico della fase 1 e congelamento (17/11, 23:5x)

- Rendiconto: `laboratorio/studi/risultati/ia02/rendiconto_fase1.md` (`protocollo_ia02`, versione `233a6e64…`).
- **Ammissibili:** HAC Δ = 0,05 (min P = 76, somma 416) e bootstrap Δ = 0,05 (min P = 76, somma 421). Tutti gli altri sei candidati falliscono almeno un controllo.
- **Candidato scelto dalla classifica §2a.5:** **bootstrap circolare a blocchi, ℓ = 10, B = 3.999, intervallo basic, Δ = 0,05 R** (parità sul minimo, vince la somma). Versione congelata: `pilota_ia02.py` SHA-256 `717e5599…`, CPython 3.13.18.
- **Fase 2:** solo questo candidato, fase = 2, repliche 1…12.000, tutte e 12 le celle, master 2026111706. Nessuna lettura intermedia.
- **Osservazioni di Claude (non cambiano nulla, servono al titolare e al DGS):**
  1. A margine 0 entrambi i metodi sono ben tarati nelle celle regolari (falsa promozione al confine 2,4–2,9%). La regola «U_CP ≤ 0,025» richiede un tasso vero intorno al 2% o meno, quindi un metodo tarato esattamente non può passare. Era deducibile prima dei risultati; nessuno dei due l'ha scritto in chiaro.
  2. La cella 11 (perdite rare) è quella che impone il margine: a Δ = 0 le false promozioni sono 12,5% con il bootstrap e 6,5% con HAC.
  3. Con Δ = 0,05 la promozione richiede L > 0,20 R. A D = 1.000 la potenza descrittiva è circa 2,5% a μ = 0,20, 72% (iid) e 53% (AR) a μ = 0,30. Il metodo è prudente, ma con molte sedute serve un vantaggio grande. Se usarlo davvero resta una decisione del titolare (DGS-07 §2a.6).
  4. La scelta fra bootstrap e HAC si è decisa per 5 promozioni su circa 420 (spareggio sulla somma). HAC costa molto meno da calcolare.
