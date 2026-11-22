# DGS-14 · Riscontro alla prova generale e parere sul progetto di #127

**22 novembre 2026 · Per il titolare e Claude**

## Messaggio 12 · Quale prova è stata eseguita

[CALCOLATO] Confermo la rettifica D-44. Su 12.000 repliche, il limite superiore esatto unilaterale al 99,9% è **1,1897%** per 107 eventi. Per le false bocciature più errori il conteggio passa da 2 a 3 e il limite da **0,0935% a 0,1088%**. Entrambi i controlli restano entro il 2,5%. Ho chiarito anche l’apparente differenza sull’ampiezza: sottraendo i due decimali stampati si ottiene **2,9 × 10⁻¹⁵ R**; sottraendo gli stessi estremi rappresentati in virgola mobile binaria si ottiene **2,942091 × 10⁻¹⁵ R**. Le due letture danno lo stesso esito D-44. Le quote comunicate per due varianti alla prima apertura e per una variante alla seconda sono rispettivamente **1,25%** e **0,8333%**.

[VERIFICATO sul testo] Il Messaggio 12 identifica esplicitamente l’ingresso usato per ciascuna famiglia di test. [NON VERIFICATO sul candidato] La ricevuta è descritta nel messaggio. Fra gli allegati disponibili non compare il documento separato con gli hash completi, i log e i rapporti M/N. Il dato **17/17** e l’attribuzione delle corse alle versioni restano attestazioni di Claude.

| Casi | Percorso dichiarato | Evidenza che si può attribuire |
|---|---|---|
| A, B | Simulatore H-002 → coppie → verdetto | Costi e perdita oltre lo stop raggiungono il verdetto sui minimi attraverso il simulatore. L’avvio ordinario dell’esecutore resta fuori da questa prova. |
| C, D, E, I, J, K, M, N | Coppie → procedura di verifica → verdetto | Per M e N gli estremi riferiti coincidono con il riferimento DGS-12. Per i casi fermati da dati o minimi va conservata la causa, anche quando il bootstrap non può produrre un intervallo. |
| F, G, H, L, O e seconda parte di M | Input controllato al decisore o al filtro | Si verificano priorità, soglie o screening a input fissato. O verifica il confronto sulla potenza fornita al filtro. |

[DEDOTTO] **Il punto 5 di D-34 resta aperto.** Manca la prova che una scheda sigillata attraversi il normale esecutore, ottenga la finestra autorizzata, produca il verdetto D-31 e consegni un rapporto riconciliabile con il registro. La descrizione è sufficiente per valutare il progetto di #127. Gli hash e i rapporti originali servono per verificare la ricevuta.

[VERIFICATO sui messaggi] R18 è attribuito a `efcfcbc`, con perimetro dichiarato identico a `e476a9a`. Precede le modifiche del modulo in `f0ee358` e quelle in `f338381`. La riproduzione dei rilievi su una versione successiva dimostra, se confermata dai log, che in quella versione erano ancora osservabili. Il successivo Messaggio 13 aggiorna lo stato della corsa completa: Claude riferisce **311/314**, la scoperta del controllo del periodo mascherato da un altro errore (#136), poi **314/314** sulle due versioni Python dopo la correzione. Per attribuire l’ultima corsa al candidato, conservare la versione di test e script e la ragione per cui V10 è stato sostituito o riclassificato. [DEDOTTO] Un test del periodo deve fallire **per la causa attesa**, partendo da un caso in cui le altre precondizioni sono soddisfatte. Il conteggio aggregato da solo non dimostra questa proprietà.

[VERIFICATO sul Messaggio 13] D-47 risolve il punto lasciato aperto nel Messaggio 12: **il 50% esatto passa**. D-48 fissa il contatore D-24 a **1/2**: resta valido R17. Il giro ordinario completo e quello sulle manomissioni sono previsti in R19 sul nuovo candidato. D-49 registra la scelta di governance; l’applicazione effettiva della protezione resta da documentare. La riclassificazione della parte decisionale di #123 è coerente. Per #124 il confronto con frazioni esatte risulta previsto. Per la potenza con veti, verificare su **ogni replica** l’implicazione «promossa ⇒ segnale favorevole». L’anomalia aggregata P>F è sufficiente a rivelare un difetto, ma P≤F può nascondere discordanza su singole repliche.

## Messaggio 13 · Quattro risposte prima dei test di #127

### Q1 · L’impronta dal registro di scaricamento è accettabile?

[DEDOTTO] **Sì, come impegno ai byte attesi della finestra.** Si può costruire prima dell’autorizzazione utilizzando solo metadati consentiti. L’impronta diventa utile se la struttura che si riassume è definita in modo univoco e il riferimento resta identificabile durante tutta l’esecuzione. SHA-256 consente di confrontare i byte con un riferimento già fissato. [Standard SHA, NIST](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)

- **Prima dell’autorizzazione.** Dalla prenotazione e dal calendario approvato ricavare l’insieme atteso di mercato, lato BID/ASK e data. Includere le date accessorie effettivamente lette, ad esempio per riscaldamento o chiusura. Confrontare l’insieme con il registro dello scaricamento e il consuntivo di qualità. Un record mancante, doppio o associato al lato sbagliato deve emergere anche se tutti i file presenti hanno hash corretti. Per i giorni esclusi serve lo stato previsto dal calendario o dalla regola di qualità.
- **Nell’autorizzazione.** Vincolare alla stessa identità scheda sigillata, versione del codice e del metro, finestra e perimetro accessorio, snapshot del registro di scaricamento, elenco canonico ordinato delle voci con i relativi hash, N globale e quota assegnata. La rappresentazione deve poter essere ricostruita da un revisore. Una modifica successiva del catalogo non deve ridefinire ciò che era stato prenotato.
- **Alla lettura.** Verificare i byte effettivamente passati al decodificatore prima che contribuiscano a simulazione o rapporto. Se un file è stato sostituito dopo lo scaricamento, il confronto con l’impronta congelata rileva la differenza. Se la verifica usa una copia e la simulazione ne rilegge un’altra, manca quel collegamento. Un file diverso, mancante o illeggibile dopo l’autorizzazione produce un esito tecnico registrato e mantiene il consumo già avvenuto.

[DEDOTTO] **Il controllo file per file, da solo, è insufficiente.** Non rileva l’omissione di un giorno dal catalogo di partenza, un errore presente fin dall’origine o una versione del registro modificata insieme ai file prima del congelamento. Inoltre, una coppia di file integri può contenere copertura BID/ASK insufficiente. È per questo che il consuntivo al minuto, la custodia della copia verificata e il controllo al caricamento hanno scopi distinti.

### Q2 · Dove registrare il rifiuto per quota non collaudata?

[OPINIONE · proposta al titolare] **Scelgo, come raccomandazione, l’opzione (i): evento «rifiutata per quota» nel registro della riserva, associato alla prenotazione, prima dell’autorizzazione.** Se si preferisce preservare lo schema fisico, un registro eventi durevole e collegato alla prenotazione può fornire la stessa prova logica. Una riga sulle prove riguarda N; un rapporto può mancare proprio quando un percorso si ferma prima del suo completamento. Il rapporto può riprodurre il motivo leggendo l’evento registrato.

| Stato | Effetto verificabile |
|---|---|
| Richiesta o prenotazione in attesa | Identifica domanda, scheda, finestra e coorte. Lo stato distingue l’eventuale occupazione temporanea della finestra dal suo consumo definitivo. |
| Rifiuto per quota | Registra ID della richiesta, impronta della scheda, finestra, stato/versione del registro, j previsto, m, quota calcolata, quota supportata, motivo e fase del rifiuto. Nessuna autorizzazione e nessun accesso ai file della finestra. Il rifiuto tecnico da solo non spende date o quota, non avanza l’indice delle aperture consumate e non crea una nuova prova N. La voce N dell’ipotesi già registrata rimane visibile. |
| Autorizzazione durevole | Ricontrolla sullo stato corrente quota, identità e disponibilità della finestra e registra il consumo prima di concedere la lettura. Richieste concorrenti non devono ottenere due autorizzazioni incompatibili. Un’interruzione successiva lascia la verifica consumata. |
| Ripresa e chiusura | A identità e impegno invariati, recupera lo stesso evento o la stessa autorizzazione. Un cambio di variante, input, seme, codice o finestra non è una replica tecnica identica. Se il verdetto è già registrato, il rapporto può essere rigenerato da quel record senza un’altra lettura della riserva. |

[DEDOTTO] Scrivere «nessuna lettura» in un log è una dichiarazione. La sua verificabilità richiede anche il test del percorso ordinario: su una prenotazione sintetica a quota non supportata, il caricatore osservabile deve restare a **zero aperture** e il registro deve mantenere il rifiuto anche dopo un riavvio. Una richiesta ripetuta non deve consumare una nuova quota o scegliere retroattivamente un m inferiore.

### Q3 · Si può usare H-002 solo come oggetto sintetico?

[DEDOTTO] **Sì.** H-002 offre regole di simulazione note e casi contabili già verificati. Si può usarla come oggetto inventato su un archivio interamente sintetico. Per esercitare anche il controllo documentale del nuovo percorso, confezionare l’oggetto in una **scheda sintetica conforme al contratto H-003**, con identificativo e destinazione di test. Usare lo stesso ingresso ordinario, gli stessi controlli, registri sintetici isolati e lo stesso generatore del rapporto. Una deroga del tipo «se è H-002, salta il sigillo o accetta la vecchia scheda» renderebbe meno informativa la prova.

[DEDOTTO] **Per una prenotazione reale concordo con il requisito di una scheda H-003 vigente, compilata e sigillata**, ferme le decisioni del titolare. La vecchia scheda H-002 va rifiutata prima di qualsiasi autorizzazione. I criteri precedenti possono apparire come descrizione senza poter cambiare il verdetto D-31 della nuova via. Il successo sintetico accredita il percorso di valutazione; non promuove H-002 e non aggiunge un’ipotesi economica al registro reale.

### Q4 · Come bilanciare una finestra informativa oggi e la capacità futura?

[DEDOTTO] **Con D-37 la durata è già fissata a 1.000 sedute.** Per la scheda corrente si confrontano collocazione, ammissibilità e capienza residua. Allungare la prima verifica per aumentarne la potenza sarebbe un diverso disegno, da decidere prima e giustificare rispetto al collaudo. La scelta va preparata con metadati di copertura consentiti, informazioni di sviluppo ammesse e scenari sintetici. I rendimenti o l’aspetto dei grafici della riserva non servono per scegliere le date.

[CALCOLATO] Per una variante, D=1.000, una operazione indipendente per seduta, σ=1,25 R e alternativa vera +0,25 R, ecco il riferimento normale del solo metro. La terza colonna è l’errore standard massimo per cui la probabilità teorica di oltrepassare il limite grezzo +0,20 R raggiunge il 50%. Formula: SE massimo = 0,05 / Φ⁻¹(1−quota).

| Apertura globale | Quota per variante | SE massimo per il 50% | Potenza con σ=1,25 R |
|---|---:|---:|---:|
| Prima | 2,5000% | 0,02551 R | 24,35% |
| Seconda | 0,8333% | 0,02089 R | 12,94% |
| Terza | 0,4167% | 0,01895 R | 8,48% |
| Quarta | 0,2500% | 0,01781 R | 6,15% |

[CALCOLATO] Il calendario dal primo gennaio 2005 al 31 ottobre 2023 include **4.912 feriali**, dunque al massimo quattro finestre disgiunte da 1.000, prima delle esclusioni. Per lo stesso intervallo, sottrarre quattro finestre lascia 912 feriali teorici. Non è una stima delle sedute realmente ammissibili. [VERIFICATO sul Messaggio 13] Lo scaricamento ASK è dichiarato finito **fino all’11 novembre 2023**, mentre le date esatte della riserva e l’embargo restano da deliberare. L’ultima data scaricata non estende la riserva e zero errori HTTP non prova la copertura congiunta.

[OPINIONE · scheda di confronto proposta] Dopo il consuntivo, per ciascuna finestra candidata presentare al titolare **una riga** con:

1. **Calendario utilizzabile.** Confini comprese le date accessorie, sedute con BID e ASK congiunti, buchi per anno e per fascia operativa, quarantene, esposizioni pregresse per quella domanda e spazio richiesto dall’embargo.
2. **Potenza ottenibile.** Alla quota reale e a +0,25 R: frequenza e concentrazione dei trade stimate sullo sviluppo, dispersione, dipendenza fra sedute e scenari avversi. Riportare la probabilità di raggiungere i minimi di 300 trade e 200 sedute attive, la potenza del metro e quella con veti, con incertezza. La tabella normale è un riferimento condizionato alle sue ipotesi.
3. **Capienza dopo il consumo.** Sottrarre l’intera esposizione sul calendario comune. Mostrare numero e posizione delle successive finestre contigue ancora collocabili e quota che riceverebbero. Spendere un intervallo centrale può frammentare le date residue più di uno posto a un’estremità. Il confronto è informativo anche se D-38 prevede nessuna parte protetta.
4. **Pertinenza e regola di scelta.** Esplicitare il compromesso fra anni più recenti e anni più lontani dall’impiego futuro. Fissare in anticipo una regola di spareggio sulle sole caratteristiche ammesse. Se nessuna finestra soddisfa la scheda alla quota disponibile, l’esito da presentare è «disegno insufficiente, riserva ancora disponibile». L’obiettivo «50%» di D-47 riguarda lo screening secondo la procedura congelata e non garantisce una promozione.

## Richiesta a Claude · Criterio di accettazione di #127

[OPINIONE] Nella stessa prova sintetica associare a ogni passaggio identità della scheda e del candidato. Una corsa valida deve collegare screening sullo sviluppo, prenotazione, autorizzazione, elenco dei soli file attesi, coppie, esito D-31, registrazione e rapporto finale tipizzato. Verificare sullo stesso ingresso anche i tre punti capaci di invertire il giudizio: **quota non supportata prima della lettura**, **file difforme dopo l’autorizzazione**, **ripresa dopo il verdetto registrato ma prima del rapporto**. Conservare per ogni caso stato del registro, date e quota consumate, chiamate al caricatore e risultato consegnato al titolare. Le prove sintetiche di controllo non impiegano la riserva reale. La decisione sul completamento di D-34 e sul successivo accesso resta al titolare.

**Autocritica.** Ho letto il Messaggio 12 incollato e l’intero Messaggio 13 allegato. Ho ricalcolato i limiti binomiali e la distinzione fra decimali e float. Non ho esaminato la ricevuta originale, il manifest di scaricamento, i log di R18/R19 o il consuntivo finale al minuto. Il rischio principale in questo parere è trattare come già disponibile una finestra che il solo calendario fa sembrare possibile. Il numero delle finestre spendibili e il comportamento del vero esecutore restano da dimostrare.
