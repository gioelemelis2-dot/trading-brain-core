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

## 7. Corsa della fase 2 finita, impronte registrate PRIMA del verdetto

- Lanciata da `7ac484e` con `pilota_ia02.py` `717e5599…`, `--fase 2 --repliche 12000 --metodi bootstrap`. Uscita 0, nessun messaggio d'errore.
- File dei limiti: 6.284.691 byte, SHA-256 `564eba71ab2ad0ef49ab37eff2022d02fbdf10c843c4f460f4097f6ddc0f7b1b`. Archiviato compresso in `risultati/ia02/limiti_fase2.json.gz`. Tabella descrittiva, SHA-256 `21f419d6b3d3bc2f9f41c416f23da2187be62da18703c7e0bc612bb779de34bd`.
- Intestazione: fase 2, 12.000 repliche, B = 3.999, master 2026111706, 12 celle, solo bootstrap.
- Prossimo passo, meccanico: `protocollo_ia02 --fase 2 --candidato bootstrap:0.05`, con inventario dei semi e 216 confronti. Un solo tentativo.

## 8. Verdetto meccanico della fase 2 (18/11, notte)

**CONFERMATO NEL DOMINIO DEL PILOTA** (`risultati/ia02/verdetto_fase2.md`), per il bootstrap circolare a blocchi (ℓ = 10, B = 3.999, basic) con margine Δ = 0,05 R, a D = 1.000 sedute e a = b = 0,025.
- **Controlli:** tutti e 10 passano (soglia k ≤ 248 su 12.000). Il più vicino alla soglia è la falsa promozione della cella 11 (perdite rare): k = 107, U_CP = 0,0119.
- **Inventario dei semi delle fasi 1 e 2:** 720.000 chiavi, 720.000 semi distinti.
- **Diagnostica dei flussi:** 216 confronti, nessuno fuori dalla banda 4.796…5.204.
- **Potenza descrittiva (P/M)** a μ = 0,20: 3,1% (iid), 3,3% (AR), 2,8% (conteggi), 6,8% (perdite rare). A μ = 0,30: 71,6% (iid) e 52,7% (AR).
- **Che cosa NON dice** (DGS-07 §2a.6):
  - non certifica altri processi, altre numerosità o una strategia reale;
  - non dà al metodo una potenza utile: con Δ = 0,05 e 1.000 sedute serve un vantaggio vero intorno a +0,30 R per essere promossi con buona probabilità.
  - Usarlo nella regola futura, e con quale margine, resta una decisione del titolare.

## 9. Riscontro del DGS (DGS-08, 18/11) ed errata di Claude

- **DGS-08 concorda con la selezione e con il verdetto meccanico** sui numeri comunicati. Ha ricalcolato in modo indipendente i limiti 60/61 e 248/249, lo spareggio, i dieci limiti della fase 2 e le potenze. Restano **attestazioni di Claude**:
  - ammissibilità completa di HAC a Δ = 0,05;
  - anteriorità;
  - riconciliazione E + P + B + I = M per riga;
  - isolamento degli stati e indifferenza all'ordine dei processi (coperta da un test; la riproducibilità è chiesta a Gemini in R17, compito B).
- **Errata di Claude sull'osservazione 1 di §6 (e 3a del messaggio 6):**
  - «un metodo tarato esattamente **non può** passare» è **sbagliato**. Al 2,5% vero il singolo controllo passa con probabilità 4,14% in fase 1 e 0,099% in fase 2: è improbabile, non impossibile. È lo stesso tipo di errore del «non passa mai» già corretto dal DGS-06;
  - «nessuno l'ha scritto in chiaro» è **falso**: DGS-07 §2a.7 riportava la probabilità di passare al 2,5% (0,0993%), e DGS-06 §1.2 trattava il caso p = a. La prudenza del criterio era voluta e documentata.
- **Osservazione nuova del DGS (3c):** nella cella 12 (perdite rare, μ = +0,20) il limite inferiore grezzo supera la media vera nel 6,84% dei casi, invece del 2,5% nominale. Il limite grezzo, preso da solo, è ottimista in quello scenario. Il verdetto riguarda invece gli attraversamenti con margine.
- **Per DGS-08, il DGS-07 ha esaurito il suo unico tentativo confermativo.** Scegliere HAC, togliere la cella 11 o cambiare Δ, soglia o numerosità **su queste repliche** violerebbe §2a.6. Ogni opzione futura richiede un protocollo nuovo.
