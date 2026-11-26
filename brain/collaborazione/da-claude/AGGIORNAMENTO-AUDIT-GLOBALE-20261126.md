# Aggiornamento dell'audit globale del 19/11 · 26/11/2026 (una pagina)

**Fonti:**
- `governance/STATO-PROGETTO.md`, aggiornato oggi;
- l'audit originale (`AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`, 19/11) e la sua controverifica (DGS-11);
- DGS-19 (25/11);
- i registri e la storia git del ramo `feat/esecutore-h002`.

Ho usato solo documentazione del repository. La riserva non è stata toccata e il lavoro tecnico in corso non è stato modificato.

**Etichette:** [VERIFICATO: fonte], [DEDOTTO], [OPINIONE].

| Pilastro | Che cosa è cambiato dal 19/11 | Evidenza datata | Che cosa resta aperto e perché |
|---|---|---|---|
| **Conoscenza** (manuale, moduli, formazione) | **Nessuna evidenza nuova.** | [VERIFICATO: git] Nessun commit dal 19/11 in `moduli`, `glossario`, `bibliografia`, `architettura`, `REGISTRO-CONOSCENZE.md`; l'ultimo è dell'11/11 | **Esiste:** Modulo 2, lezioni L2.1–L2.6 «in_verifica», nessuna «verificata». **Usato dal titolare:** nessun cancello superato registrato. **Rinviato** per D-10, D-12, D-20 e D-33 («prima la macchina»). **Riparte** con una revoca mirata del titolare (era la decisione 4 dell'audit, mai presa) |
| **Ricerca** (dati, laboratorio, macchina) | Il verdetto D-31 è nel codice; c'è un percorso ordinario di verifica con la riserva/2; dal 23/11 una corsa intera dal lanciatore riesce; criterio d'uscita deciso (D-56); dati custoditi su due cloud | [VERIFICATO] Ricevuta `2026-11-23-candidato-7191156` (perimetro 299/299, lanciatore superato, 26/11); DGS-19: parere favorevole sulla prova sintetica positiva (D-34 punto 5); D-39 (23/11) | **R19 consegnato il 26/11 su `1431190`: NON pulito.** 2 critici e 4 importanti. Claude li ha riprodotti rieseguendo le sonde di Gemini sul candidato `7191156` e sul codice attuale: 7 rilievi su 9 si riproducono, i 2 restanti erano già chiusi (#140, #142). Nuovi difetti #143–#149 (`ricevute/2026-11-26-verifica-r19/`). Il candidato effettivo `7191156` **non è valido**. Restano 15 dei 18 requisiti dell'ultimo lotto (correzione da DGS-20: «8 su 11» era l'elenco precedente). I registri dello scaricamento sono incompleti, quindi oggi lo screening si fermerebbe (diagnosi del 23/11). È collaudata una sola quota (DGS-19). La potenza non è calcolata dalla macchina. Nessuna strategia candidata |
| **Protezione** (Guardian G0, regole, diario) | **Nessuna evidenza nuova.** | [VERIFICATO: git] Nessun commit dal 19/11 in `guardian`, `dati/costi`, `dati/reali`. `demo_broker_mt5_50k_xauusd.toml`: `riconciliato = false`. `TEMPLATE_RICONCILIAZIONE_DA25.toml` esiste ma non è compilato | **Esiste:** il G0 consultivo (77 test), le regole personali (14 su 15), il diario a catena con il punteggio di Brier. **Usato dal titolare:** nessuno. La cartella `journal/dati` contiene solo `.gitignore`, e il G0 dichiara «uso per decidere NON AUTORIZZATO». **Riconciliazione demo: non fatta.** Manca l'estratto conto di 2–3 micro-operazioni (DA-25). **Riparte** quando il titolare fa quelle operazioni sulla demo FP Markets |
| **Governance** (decisioni, registri, revisori) | 15 decisioni nuove (D-42…D-56); ciclo DGS-12…DGS-19; regola d'uscita riscritta prima della consegna di R19; convergenza misurata | [VERIFICATO] `DECISIONI.md` (D-56, 26/11); `CONVERGENZA-REVISIONI-20261123.md`; DGS-19 Q5/Q6 | Le gravità le assegnano chi scrive e chi rivede: con D-56 il dissenso va al DGS e decide il titolare. **Protezione del ramo non applicabile** con il piano Free (DA-39 aperta), quindi oggi la difesa è la storia git. Ramo non unito a `main`. **Consulto:** solo proposto (DA-12 aperta), mai avviato |

**Quale conclusione dell'audit originale va corretta oggi.** «Il banco fa bene ciò che promette».
- [VERIFICATO] Il giudizio poggiava su prove **a pezzi**. R19 (26/11) lo conferma: aperti **1 critico** (#143, esecuzione di codice non sigillato prima dei controlli), **5 importanti** (#144–#148) e **1 minore** (#149); 6 sono bloccanti per D-56. (Correzione da DGS-20: avevo scritto «sei importanti».) Fino al 23/11 la verifica vera dal lanciatore **non poteva arrivare in fondo** (#142).
- Il manifesto non era mai stato provato sui registri veri, che sono incompleti (diagnosi del 23/11).
- Anche «nessun critico» era più debole del dichiarato (#126).
- [DEDOTTO, riformulato secondo DGS-20] La formula corretta è: **«Sul caso sintetico valido di riferimento il percorso ordinario termina, e il verdetto si riconcilia con il record. Su altri casi sintetici R19 documenta violazioni del sigillo, dell'integrità dei dati e della gestione della riserva. Il gate resta aperto.»** Anche la mia prima riformulazione («giudica correttamente sui dati sintetici») era troppo larga.
- **Falsi positivi** (DGS-20): «0 su 100 mercati senza vantaggio promossi» dà un limite superiore unilaterale al 95% di **2,95%** [CALCOLATO: 1 − 0,05^(1/100) = 0,0295]. Non è una garanzia per una strategia futura: va citato con scenario, quota e procedura del collaudo.
- **Formulazioni da circoscrivere** (DGS-20): «nessuna strategia provata» vale per la **verifica in riserva**, perché H-002 ha prodotto osservazioni sullo sviluppo. «Riserva mai letta» va inteso come «nessuna verifica di strategia documentata sulla riserva»: le operazioni di copia, inventario e consuntivo sono un'altra cosa.
- Vanno aggiornate anche due affermazioni:
  - «i dati su un solo Mac» è superata, ora ci sono due copie verificate (D-39);
  - «la riserva basta per circa 4 verifiche» va letta come capacità; la quota collaudata oggi è **una** (DGS-19).

**La prossima prova senza strategia che riduce di più l'incertezza sull'utilità per il titolare.** [OPINIONE] **D2 dell'audit: la riconciliazione del G0** con 2–3 micro-operazioni (0,01 lotti, con stop) sulla demo FP Markets, confrontate con l'estratto conto.
- È l'unico pilastro che può aiutare il titolare **subito**, prima di qualunque strategia.
- Costa circa un'ora e nessun denaro, e risponde a una domanda binaria: i numeri del Guardian coincidono con il broker?
- Sblocca l'uso del diario.
- Non tocca la riserva né il lavoro sulla macchina.
- **Alternativa più costosa:** misurare frequenza e dispersione realistiche sullo sviluppo con strategie nulle dichiarate prima. Richiede però prima B1 (registri dello sviluppo) e una regola sul conteggio in N.

**Da far controverificare al DGS:**
1. la correzione della conclusione «il banco fa bene ciò che promette», e se ne vanno corrette altre;
2. la scelta di D2 come prova più utile senza strategia, rispetto alla misura sullo sviluppo con strategie nulle;
3. la verifica di R19 (`VERIFICA-R19.md`): riproduzioni, classificazioni secondo D-56 e la scelta di **non** chiudere R19 su `7191156`, ma di rivedere il candidato congelato dopo il lotto;
4. se la mancanza di evidenze nuove su conoscenza e protezione, da 7 giorni, sia un rischio da portare al titolare come decisione: riattivarle, oppure dichiararle ferme per scelta.
