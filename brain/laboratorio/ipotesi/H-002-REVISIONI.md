# H-002 · Revisioni della bozza (commit 417094c) e verifica di Claude

## R1 · DeepSeek, 14/11/2026 (revisore esterno)
**Nota di attribuzione:** per un errore di invio, DeepSeek ha ricevuto il prompt destinato a Gemini e si è firmato «Gemini». La revisione è di **DeepSeek**, non di Gemini, quindi non va salvata in `da-gemini/`.
- DeepSeek ha dichiarato correttamente di non avere accesso al repository e non ha inventato commit.
- Ha lavorato sul testo della bozza incollato dall'utente.
- Testo originale: nella conversazione dell'utente con DeepSeek.

**Giudizio complessivo di Claude:** revisione seria e utile. Molte ambiguità vere, sei proposte sbagliate o da ridimensionare (sotto, con il motivo).

| Rilievo di DeepSeek | Esito | Verifica e motivo di Claude |
|---|---|---|
| A1: quali minuti compongono il range di apertura | **accolto** | Va scritto come intervallo [08:00, 08:30): 30 minuti, dal minuto delle 08:00 a quello delle 08:29 |
| A2: nei giorni di cambio dell'ora la sessione dura 7,5 o 9,5 ore | **respinto** | Le sessioni sono definite nell'ora locale della borsa e il cambio d'ora avviene di notte: la sessione dura sempre 8,5 ore (Londra) e 6,5 ore (New York). Lo sfasamento USA–Europa cambia solo la relazione fra le due in UTC, ed è già gestito dai fusi |
| A3: minuti mancanti nel range | **accolto** | In Dukascopy un minuto mancante è un minuto senza scambi. Il range usa i minuti presenti; giorno valido solo con almeno l'80% dei minuti |
| A4: 20 giorni di calendario o di trading | **accolto** | Si usano le 20 sessioni valide precedenti della stessa sessione |
| A6, A8: prezzi per acquisti e vendite, e scatto degli stop | **accolto** | Convenzione da scrivere:<br>• acquisto: entra all'ASK, esce al BID, stop quando il BID tocca RA basso;<br>• vendita: entra al BID, esce all'ASK, stop quando l'ASK (BID + spread) tocca RA alto |
| A7: salto di prezzo all'apertura della candela d'ingresso | **accolto** | Se il prezzo d'ingresso è già oltre lo stop, o il rischio è minore del 25% dell'ampiezza del range, il trade non si fa |
| A9: prezzo dell'uscita a fine sessione | **accolto** | Uscita all'apertura del primo minuto dopo la fine della sessione, dal lato giusto (BID o ASK), con slittamento |
| A10: lo spread contato due volte nella dimensione | **accolto come chiarimento** | Distanza = prezzo d'ingresso eseguito meno prezzo d'uscita allo stop, dai lati giusti (lo spread è già dentro); poi si aggiungono commissione e slittamento, una volta sola |
| A11: slittamento sulle uscite | **accolto** | Target come ordine limite: nessuno slittamento. Uscita a fine sessione e stop: slittamento |
| Costi: spread 0,35 troppo ottimistico «all'apertura» | **accolto in parte** | Gli ingressi NON avvengono all'apertura della sessione: il primo possibile è alle 08:45 di Londra e alle 10:15 di New York, a 45 minuti dall'apertura. Senza spread misurati, però, la scelta prudente è giusta: **riferimento 0,50** finché non avremo gli spread di FP Markets per ora del giorno |
| Slittamento 0,10 troppo basso sugli stop | **accolto** | 0,20 USD sugli stop e sulle uscite a mercato; 0,10 sugli ingressi a mercato |
| Esempio numerico con stop di 2,50 USD | **respinto come esempio** | Lo stop di H-002 è il lato opposto del range di apertura. Con candele mediane da circa 2 USD a 1 minuto (Studio 1), un range di 30 minuti è largo molti dollari, quindi i costi pesano molto meno in R. Il principio (contare tutti i costi) resta valido |
| N = 32: contare nel DSR anche le 24 prove di robustezza | **respinto in parte** | Il DSR corregge la scelta della migliore fra N alternative. Le prove di robustezza non possono essere scelte, possono solo bocciare: non aumentano i falsi positivi, li riducono. Contarle anche in N punirebbe due volte.<br>Si registrano tutte nel registro, con ruolo «robustezza», ma restano fuori da N (da confermare in DA-19 e DA-28).<br>Per riferimento, con 600 trade la soglia di Sharpe per trade sale da 0,043 (N = 4) a 0,086 (N = 32) |
| Contare il filtro notizie come prove | **accolto** | Diventerà una variante selezionabile: si pre-registrano 4 prove in più (N = 8 quando ci sarà) |
| Scenari di spread e slittamento come prove | **respinto** | Il riferimento è unico e fissato prima; gli altri scenari si riportano soltanto. Nessuna scelta, quindi nessuna prova in più |
| «Crolla» non definito | **accolto** | Una variante è bocciata se in una qualsiasi prova di robustezza l'aspettativa diventa ≤ 0 o perde più del 50% rispetto alla base |
| Robustezza decisa dopo aver visto il risultato (sguardo al futuro di secondo livello) | **accolto** | Le 6 prove di robustezza per variante si eseguono sempre, comunque vada la base; la soglia è quella sopra |
| Benchmark direzionale contro la tendenza 2023–2026 | **accolto** | La strategia deve battere «sempre acquisto» e «sempre vendita» negli stessi orari di ingresso e con le stesse uscite. Acquisti e vendite si riportano separati, e il confronto entra fra i criteri |
| Criterio di drawdown | **accolto** | Il drawdown massimo in sviluppo deve stare sotto 12R (60% del limite totale FTMO di 20R a rischio 0,5%) |
| Mediana R > −0,1R e asimmetria < 3 | **respinto** | Sbagliato per questa strategia: con target a 1,5R e meno del 50% di vincite, la mediana è per costruzione −1R anche se la strategia guadagna. Un'asimmetria positiva è normale per chi taglia le perdite e lascia correre |
| Dichiarare che i giorni con meno dell'80% dei minuti sono esclusi anche dal vivo | **accolto in parte** | Dal vivo un minuto mancante è un minuto senza scambi, lo stesso fenomeno; va scritto che la regola si applica allo stesso modo |
| Contare in anticipo i trade possibili per verificare il minimo di 300 | **respinto** | Contarli vuol dire far girare i segnali sui dati di sviluppo prima del sigillo. Stima senza dati: circa 750 giorni in 3 anni, quasi sempre con rottura, quindi ben sopra 300 per sessione |
| Saltare i giorni del cambio d'ora | **respinto** | Non serve (vedi A2) |

## R2 · Gemini (Antigravity)
In attesa. Rivede la stessa bozza, commit 417094c.

## Prossimo passo
Quando arriva R2: versione 2 della scheda con le correzioni accolte, e l'elenco delle scelte che restano all'utente (sessione, uscita, stop, numero di prove). Solo dopo, il sigillo.
