# Risposta di Claude al dossier del DGS (DGS-05, addendum, specifica di collaudo IA-02)

17/11/2026 sera. Per il titolare e il DGS. Le proposte numeriche del DGS restano **proposte** finché il titolare non le ratifica. Anche le mie lo sono.

## 1. Stato corrente

| Voce | Completato | In corso | Da verificare |
|---|---|---|---|
| **Candidato del banco** | Commit `8e51ce9`: #96–#105 corretti; 366 test verdi su Python 3.13.18 e 3.9.25 (Linux, Claude) | | Sull'Apple Python 3.9 del Mac: R15 |
| **Mutanti sul candidato** | Esecuzione 213/213, simulatore 40/40, DSR 44/44, riconteggio 53/53, controllo della cache 20/20, scaricatore 50/50, su entrambe le versioni. N57 dichiarato equivalente; 8 rifatti a parte dopo la corsa completa (#105, errore mio) | | |
| **Antigravity** | R14 integrato (#96–#104) | **R15** sul candidato `8e51ce9`, con commit, ambiente e perimetro dichiarati (P6). Mandato attivo: `collaborazione/da-claude/PROMPT-R15-GEMINI.md` | Giri puliti: **0 su 2** |
| **Scaricamenti** (solo metadati) | BID 2005 → 11/02/2020; sviluppo BID e ASK | BID dal 12/02/2020; ASK dal 2005 (esiste) | Consuntivo per lato e per intersezione: lo strumento dell'intersezione manca (sotto, punto 3) |
| **Riserva** | Mai aperta; censimento riconfermato il 17/11 sulle trascrizioni | | #92: il meccanismo `riserva.py` non è collegato al caricatore (custodia ≠ contabilità) |

Correzione per il DGS: l'arresto del BID all'11/02/2020 è attestato da «Last login: Tue Nov 17 01:10:13» nel Terminale e dal log senza messaggio finale (riavvio del Mac). L'episodio dei «venti giorni» (#47 → #60) è un altro evento.

## 2. Esito di ogni proposta del DGS

| Proposta | Esito | Motivo |
|---|---|---|
| **P1:** stima nello screening, limite inferiore unilaterale in verifica | **Accolta** (il titolare conferma l'orientamento) | I numeri del DGS sono corretti, li ho ricalcolati (4.906 e 6.544 trade). **Correggo una mia affermazione:** «la riserva è lunga, quindi i trade ci sono» era sbagliata. Con σ = 1,25 R, potenza 80% e quota 2,5%, i trade necessari sono: **545** per +0,30 R; **1.226** per +0,25 R; **4.906** per +0,20 R. Con la dipendenza del riferimento AR(1) ρ = 0,25 (F ≈ 1,66) diventano 905, 2.036 e 8.143. A circa un trade per seduta, 2005–2023 offre circa 4.700 sedute, prima di togliere la parte protetta. Quindi **solo vantaggi veri dell'ordine di +0,25 R o più sono verificabili nella riserva**; per gli altri l'esito atteso è «non decidibile». È da calcolare nella scheda di ogni ipotesi. |
| **P2:** α totale 5%, α_j = 0,05/[j(j+1)], ripartizione α_j/m | **Accolta in parte:** la formula è già in `riserva.py`, il valore spetta al titolare | Il 5% resta una scelta di governance. Osservazione: con j = 2 la quota è già 0,83%, quindi la seconda apertura richiede circa il 33% di trade in più a parità di effetto. |
| **P2:** finestre cronologiche minime, parte protetta = ultimo intervallo contiguo | **Da decidere** (confronto sotto, punto 5) | Il DGS propone «vecchi prima, recenti protetti»; io avevo suggerito il contrario. Nessuno dei due è dimostrato: è una scelta. |
| **P2:** condizione di apertura (custodia) | **Accolta. Serve prima della verifica**, non prima del sigillo | Coincide con #92 aperto: il caricatore deve leggere solo il perimetro prenotato e registrare il consumo prima della lettura, con un impegno datato esterno, cioè un commit spinto. È lavoro di codice. |
| **P3:** quattro integrazioni al modello H-003 | **Accolte**, come aggiornamento documentale del modello | (1) Ambiguità sulla barra al minuto: H-002 ha già una regola conservativa (stop prima del target nella stessa barra) da riportare come obbligo del modello. (2) Formula di R e denominatore: la convenzione dell'addendum coincide con H-002 §5, da rendere esplicita. (3) Coerenza del campione: va nel modello. (4) Esito incompleto: dipende da DA-31. |
| **P4:** DA-31 a tre stati, con minimo tecnico e minimo informativo distinti, e limite superiore per «bocciata» | **Accolta nel principio** | Il titolare conferma. Va completata con il metodo del limite superiore e la regola del riesame. È una **modifica di metodo**, da ratificare. |
| **P5:** soglie 99/98/95% e 5 minuti | **Ritirata dal DGS** | Non approvate. Le soglie attuali (50% e 25%) restano provvisorie. Lo strumento dell'intersezione si costruisce comunque: è un rendiconto, non una soglia. |
| **P6:** ogni giro dichiara commit, ambiente e perimetro | **Accolta, già applicata a R15** | Il candidato è fissato a `8e51ce9`, con l'ambiente da dichiarare. Il perimetro del sigillo è separato dagli strumenti di contorno (dati, riconteggio, esportazione). |
| **Addendum §4:** prova che i buchi selettivi distorcono il risultato | **Accolta** | Il controesempio è giusto. Conferma che la soglia sui buchi va scelta guardando l'effetto su segnali ed esiti, non solo le percentuali. |
| **Specifica di collaudo:** limiti Clopper–Pearson e regola U ≤ a | **Accolta in parte** | Corretta matematicamente; ho verificato le formule e il fattore F. **Costi calcolati** (punto 4): la versione completa è fattibile per l'intervallo da solo, non per l'intera procedura. |
| **Specifica:** γ = 1%, p* = a/2, 90% per cella | **Da ridiscutere** | Con p* = a/2 il metodo deve essere molto conservativo (falsa promozione vera ≤ metà della quota), e così perde potenza proprio dove i trade scarseggiano (vedi P1). L'alternativa motivata è nel punto 4. |

**Errori matematici trovati nel dossier:** nessuno nei calcoli che ho ricontrollato (F di AR(1), tassi 6,44% e 12,86%, trade necessari, limiti binomiali esatti, linearizzazione per il rapporto S_d/K_d). Una precisazione: per la sola certificazione (U ≤ a) basta la coda superiore. Usare δ = γ/(2K) su entrambe le code è prudente, ma costa repliche.

**Duplicazioni:** R15 di Gemini (compito B) misura falsi positivi e potenza dello **screening attuale di H-002** su mercati inventati. La specifica del DGS riguarda invece il **test di verifica sul limite inferiore**. Sono vicini ma distinti. B sarà un primo dato sulla «procedura intera», da non confondere con il collaudo dell'intervallo.

## 3. Cosa è già coperto e quando serve il resto

| Quando | Cosa |
|---|---|
| **Prima della chiusura della baseline** (adesso) | R15 e R16 di Gemini; strumento dell'intersezione BID/ASK e dei buchi (solo rendiconto); consuntivo dello storico a scaricamento finito |
| **Prima del sigillo di H-003** | Convenzione di R ed estimando (addendum §1); metodo dell'intervallo **scelto e collaudato**; DA-31 completata; P3 nel modello; minimo informativo calcolato sulla frequenza stimata nello sviluppo |
| **Prima della verifica sulla riserva** | #92 (custodia: il caricatore legge solo il perimetro prenotato); giro su tutte le manomissioni e protezione del ramo (D-24); valori di P2 ratificati; soglie di idoneità dello storico decise con lo studio dei buchi |
| **Può aspettare** | Collaudo della procedura completa di selezione su più ipotesi; cambi di regime oltre la dichiarazione dei limiti |

## 4. Il passo metodologico più piccolo, con i costi

**Costi della specifica come proposta.** Repliche per cella per avere il 90% di probabilità di ottenere U ≤ a con γ = 1%:

| Quota a | p* = a/2, K = 20 | p* = a/2, K = 60 | p* = a/1,5, K = 20 |
|---|---|---|---|
| 2,5% | 3.068 | 3.529 | 7.102 |
| 0,833% | 9.394 | 10.804 | 21.733 |
| 0,417% | 18.898 | 21.733 | 43.715 |

- **Per l'intervallo da solo:** una replica è una serie inventata di qualche migliaio di trade più un intervallo HAC o bootstrap. Costa da millisecondi a un secondo, quindi 60 celle × 10.000 repliche si fanno in ore. **Fattibile.**
- **Per la procedura intera** (simulatore, screening, veti) una replica costa da secondi a minuti. Migliaia di repliche per cella sono **sproporzionate**. Qui propongo di **stimare** i tassi con il loro intervallo su poche celle, senza certificare.
- **Sul margine richiesto da U ≤ a:** un metodo esattamente al livello nominale (p = a) non passa mai. Con p* = a/2 si chiede un metodo «doppiamente prudente», e la potenza persa va pagata in trade (punto P1). Propongo di **decidere il margine dopo un pilota**, non prima e non dopo la verifica finale.

**Passo minimo proposto (pilota), costo circa mezza giornata di lavoro e qualche ora di calcolo, solo dati inventati:**
1. Due candidati: HAC con regola dei ritardi fissata, e bootstrap a blocchi giornalieri sulle coppie (S_d, K_d).
2. Quattro celle: gaussiano indipendente e AR(1) con ρ = 0,25, ciascuno al confine μ = 0,15 e a +0,30, con n = 1.000 e quota 2,5%.
3. 3.000 repliche per cella, semi impegnati prima.

**Evidenza di accettazione del pilota:** il tasso di falsa promozione stimato al confine, con il suo intervallo, per ciascun metodo. Serve a scegliere il metodo e il margine **prima** di scrivere la matrice completa con K e M definitivi. Il pilota non certifica nulla: va dichiarato come sviluppo del metodo.

## 5. Decisioni richieste al titolare

1. **P2, valore di α totale** (proposta del DGS: 5%).
2. **P2, ordine delle finestre:**
   - **vecchi prima, recenti protetti** (DGS): la prima verifica, quella con la quota più grande, si fa su un mercato più lontano da oggi; la seconda verifica conserva gli anni più vicini all'oggi;
   - **recenti prima, vecchi protetti** (Claude, prima): la prima verifica si fa sugli anni più simili allo sviluppo; un'eventuale seconda verifica cadrebbe su 2005–2010, con prezzi, liquidità e forse qualità dei dati molto diversi.

   In entrambi i casi la scelta va fatta **prima** dell'apertura, usando solo la copertura per anno: nessun prezzo.
3. **DA-31:** tre stati con la regola del DGS. Da completare con il limite superiore e il riesame.
4. **Collaudo:** autorizzare il pilota del punto 4 (dopo R15 o in parallelo: solo dati inventati, non tocca il candidato), e rinviare γ, p* e il 90% a dopo il pilota.
5. **P3:** autorizzare l'aggiornamento documentale del modello H-003 con le quattro integrazioni.

Nessun valore numerico del DGS è stato applicato al codice o ai documenti normativi.
