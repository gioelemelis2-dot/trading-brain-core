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
| **Ricerca** (dati, laboratorio, macchina) | Il verdetto D-31 è nel codice; c'è un percorso ordinario di verifica con la riserva/2; dal 23/11 una corsa intera dal lanciatore riesce; criterio d'uscita deciso (D-56); dati custoditi su due cloud | [VERIFICATO] Ricevuta `2026-11-23-candidato-7191156` (perimetro 299/299, lanciatore superato, 26/11); DGS-19: parere favorevole sulla prova sintetica positiva (D-34 punto 5); D-39 (23/11) | **R19 in attesa:** il candidato effettivo è `7191156`, ma Gemini lavora ancora su `1431190`. L'ultimo esito indipendente consegnato è **R18 (21/11), non pulito**. Restano 8 degli 11 requisiti dell'ultimo lotto. I registri dello scaricamento sono incompleti, quindi oggi lo screening si fermerebbe (diagnosi del 23/11). È collaudata una sola quota (DGS-19). La potenza non è calcolata dalla macchina. Nessuna strategia candidata |
| **Protezione** (Guardian G0, regole, diario) | **Nessuna evidenza nuova.** | [VERIFICATO: git] Nessun commit dal 19/11 in `guardian`, `dati/costi`, `dati/reali`. `demo_broker_mt5_50k_xauusd.toml`: `riconciliato = false`. `TEMPLATE_RICONCILIAZIONE_DA25.toml` esiste ma non è compilato | **Esiste:** il G0 consultivo (77 test), le regole personali (14 su 15), il diario a catena con il punteggio di Brier. **Usato dal titolare:** nessuno. La cartella `journal/dati` contiene solo `.gitignore`, e il G0 dichiara «uso per decidere NON AUTORIZZATO». **Riconciliazione demo: non fatta.** Manca l'estratto conto di 2–3 micro-operazioni (DA-25). **Riparte** quando il titolare fa quelle operazioni sulla demo FP Markets |
| **Governance** (decisioni, registri, revisori) | 15 decisioni nuove (D-42…D-56); ciclo DGS-12…DGS-19; regola d'uscita riscritta prima della consegna di R19; convergenza misurata | [VERIFICATO] `DECISIONI.md` (D-56, 26/11); `CONVERGENZA-REVISIONI-20261123.md`; DGS-19 Q5/Q6 | Le gravità le assegnano chi scrive e chi rivede: con D-56 il dissenso va al DGS e decide il titolare. **Protezione del ramo non applicabile** con il piano Free (DA-39 aperta), quindi oggi la difesa è la storia git. Ramo non unito a `main`. **Consulto:** solo proposto (DA-12 aperta), mai avviato |

**Quale conclusione dell'audit originale va corretta oggi.** «Il banco fa bene ciò che promette».
- [VERIFICATO] Il giudizio poggiava su prove **a pezzi**. Fino al 23/11 la verifica vera dal lanciatore **non poteva arrivare in fondo** (#142).
- Il manifesto non era mai stato provato sui registri veri, che sono incompleti (diagnosi del 23/11).
- Anche «nessun critico» era più debole del dichiarato (#126).
- [DEDOTTO] La formula corretta è: **il banco giudica correttamente sui dati sintetici, da un capo all'altro, solo dal 23/11; sui dati veri non è ancora pronto a partire.**
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
3. che lo stato «R19 in attesa» e il candidato effettivo `7191156` siano descritti correttamente, alla luce della sua regola sulle prove trasferite (DGS-18 Q4);
4. se la mancanza di evidenze nuove su conoscenza e protezione, da 7 giorni, sia un rischio da portare al titolare come decisione: riattivarle, oppure dichiararle ferme per scelta.
