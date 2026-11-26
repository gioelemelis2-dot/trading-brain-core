# Messaggio 20 al DGS (27/11/2026): casi d'accettazione per l'ultimo lotto e tolleranze della prova D2

**Come si manda.**
- Nella stessa conversazione di DGS-20 si incolla il testo fra le due righe di trattini.
- Si allega **un solo file**, `consegna-dgs20.zip`, con l'indice `SHA256SUMS`.
- Modello: Astra con ragionamento esteso; strumento di esecuzione del codice e plugin di verifica attivi.

---

MESSAGGIO 20 AL DGS — risposta a DGS-20 e richiesta di lavoro. Solo metodo; nessuna decisione riservata al titolare.

**RICHIESTA DI LAVORO.** Per ogni numero dichiara [CALCOLATO], [NON VERIFICATO] o [DEDOTTO].

1. CHE COSA HO FATTO SU DGS-20
- Applicate e verificate sui file le tue correzioni:
  - nell'audit: 1 critico, 5 importanti, 1 minore; 15 requisiti su 18; la tua formula del banco; 0/100 = 2,95% al 95%; «nessuna strategia provata» circoscritto alla riserva;
  - nella verifica R19: le sonde #124 sono solo D1, D2, D3, D6a e D6b;
  - su D-56: 0 giri e 0 tentativi prima del congelamento;
  - riesame di #145 aperto;
  - nei requisiti 15–17: i tuoi criteri di chiusura;
  - al congelamento: indice unico.
- **Decisioni del titolare del 26/11:**
  - **D-57:** prova D2 sul Guardian (la farà sulla demo FP Markets MT4 Raw);
  - **D-58:** nome del titolare sostituito nei file attuali del repository. I manifest delle consegne passate **non** sono stati modificati: gli originali si verificano dalla storia git, e la verifica su 9 file e 5 manifest è riuscita.

2. RICHIESTA A · CASI D'ACCETTAZIONE PER L'ULTIMO LOTTO (allegato `REQUISITI-ULTIMO-LOTTO.md`)
Prima che io scriva le correzioni, ti chiedo i **casi d'accettazione a risposta esatta** per i requisiti **1** (D-55) e **12–18** (#143–#149), come facesti per la prova generale (DGS-12). Mi servono casi scritti da te, che non conosci il codice nuovo: riducono il rischio che i test provino solo ciò che ho immaginato io.

Per ogni caso:
- **ingresso:** scheda, prenotazione, registri, file, argomenti del comando;
- **esito atteso:** codice d'uscita, esito tecnico, eventi nel registro della riserva (tipo e consumo), voci nel registro delle prove, chiamate al caricatore (sviluppo, verifica);
- **almeno un caso positivo** in cui il percorso valido resta esercitabile (D-56).

In particolare:
- **#143:** come rendere **una sola** l'identità fra lanciatore ed esecutore (argomenti e codice sigillato). Quali forme di argomenti vanno rifiutate e quali accettate?
- **#144:** quale esito vuoi per una finestra con feriali vuoti inattesi: «non decidibile», un rifiuto prima dell'autorizzazione, oppure uno stato distinto delle sedute?
- **#145:** l'unicità va controllata su tutte le versioni del registro delle prove nella storia, con α fissato a D-38 e la testa del registro della riserva identica fra le versioni. Bastano queste tre condizioni?
- **D-55:** quale **testimone** è accettabile con il piano GitHub Free?
  - (i) solo la conferma sul riferimento remoto;
  - (ii) come (i), più una ricevuta stampata dall'esecutore che il titolare conserva fuori dal repository e deve fornire per autorizzare la lettura;
  - (iii) come (ii), più un tag firmato.

  Che cosa deve provare il collaudo per ciascuna?

3. RICHIESTA B · TOLLERANZE DELLA PROVA D2 (allegato `PROCEDURA-D2-RICONCILIAZIONE-DEMO.md`)
- In DGS-20 hai scritto «applicare le tolleranze già previste da DA-25». **Ho cercato e non esistono:** né in DA-25 né nei documenti del Guardian compare una tolleranza.
- Proponi una convenzione per voce (perdita allo stop, commissione, margine), assoluta, relativa o mista, con il ragionamento.
- La decisione sarà del titolare, **prima** di aprire le operazioni domani.

4. NON SERVE ORA
- Il giudizio sulla redazione del pacchetto V3.3 congelato (D-17): è un'eccezione aperta. Te lo chiederò solo se il titolare vorrà rifarlo.

---
