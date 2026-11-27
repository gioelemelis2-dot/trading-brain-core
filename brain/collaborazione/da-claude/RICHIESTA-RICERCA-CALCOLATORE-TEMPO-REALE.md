# Richiesta di ricerca al DGS · calcolatore del rischio in tempo reale e stop adattivo · 27/11/2026

**Come si manda:** si incolla il testo fra le due righe di trattini nella conversazione del DGS. Nessun allegato con dati personali.

---

RICHIESTA DI RICERCA E PIANO · CALCOLATORE DEL RISCHIO IN TEMPO REALE ACCANTO A METATRADER, E STOP ADATTIVO

Per ogni affermazione indica [CALCOLATO], [DEDOTTO], [NON VERIFICATO] o [FATTO · fonte con data]. Sono informazioni per decidere, non decisioni prese: le decisioni spettano al titolare.

**CONTESTO**

- Il Guardian G0 (`guardian/g0`) è **consultivo** per D-16: calcola, avvisa e registra; non blocca, non intercetta, non scrive sul conto. Il suo uso per decidere è **non autorizzato** finché non è riconciliato con il broker.
- Oggi calcola solo la perdita allo stop, da prezzi inseriti a mano: |ingresso − stop| × contratto × lotti, convertita nella valuta del conto, più le commissioni se gliele si passano. Calcola anche i limiti FTMO e lo scenario di stress.
- **Non calcola** il margine del broker: la sua funzione «margine» è la distanza dal limite di drawdown.
- La prova D2 (D-57, tolleranze D-60) è in corso su una demo FP Markets MT4 Raw, XAUUSD.cy: contratto 100, margine 5%, server a UTC+2 [DEDOTTO].
  - Sulla prima operazione (S1) profitto e margine coincidono al centesimo con le formule congelate.
  - All'apertura non risulta addebitata alcuna commissione: lo stato del conto (Raw o Standard) è da verificare.
- Ambiente del titolare: Mac. L'app MT4 in uso **sembra la versione per iPad** eseguita su Mac [DEDOTTO dall'interfaccia, da verificare]. In quella versione non girano programmi MQL4.
- Il titolare lavora e ha poco tempo davanti allo schermo.

**CHE COSA CHIEDE IL TITOLARE (parole sue, riassunte)**

Un'applicazione accanto alla piattaforma che calcoli istantaneamente, secondo per secondo, e che **sposti contemporaneamente gli stop adattandosi al prezzo**.

**RICHIESTA A · RICERCA**

1. **Opzioni tecniche su Mac** per un calcolatore in tempo reale accanto a MetaTrader:
   - un indicatore o pannello MQL4 su MT4 desktop (installatore MetaQuotes per macOS, basato su Wine) o MQL5 su MT5;
   - i server MCP ufficiali di MT5 (terminal, marketdata) in **sola lettura**;
   - un'app esterna che legge un file scritto dal terminale;
   - le API dei broker o di FP Markets, se esistono.

   Per ciascuna: che cosa legge (prezzi BID/ASK, posizioni, margine), con che ritardo, se gira sulla versione iPad o desktop, permessi, possibilità di imporre la **sola lettura**, costi, manutenzione, rischi (credenziali, invio di ordini non voluto).
2. **Stop adattivo (trailing o regole dinamiche).** Quali tipi esistono:
   - trailing stop nativo della piattaforma (su MT4 lavora lato terminale e richiede il terminale acceso [da verificare]);
   - EA che modifica gli ordini;
   - ordini lato server del broker.

   Che cosa succede se il terminale o il Mac si spengono, la connessione cade, il mercato fa un gap, o si superano i limiti di modifica del broker.
3. **Regole della prop firm (FTMO)** su EA, copy-trading e modifiche automatiche degli ordini, con la fonte ufficiale e la data.
4. **Compatibilità con il progetto:**
   - con D-16 (Guardian consultivo);
   - con il gate di riconciliazione del Guardian;
   - con il principio per cui **una regola di gestione dello stop è parte della strategia**, e quindi va provata nel laboratorio (scheda H-003, screening, verifica sulla riserva) prima di usarla.

**RICHIESTA B · PIANO**

Proponi un piano a tappe con un criterio d'accettazione per ciascuna. Separa:

- **Fase 1, sola lettura:** calcolatore in tempo reale, cioè il Guardian «dal vivo». Mostra la perdita allo stop, il margine e i limiti, senza toccare il conto. Specifica che cosa deve provare il collaudo (stessi numeri del Guardian G0 e del broker, entro le tolleranze di D-60) e come si dimostra che non può inviare ordini.
- **Fase 2, solo un avviso suggerito:** il calcolatore propone dove spostare lo stop secondo una regola scritta; il titolare decide e agisce.
- **Fase 3, automatico, solo in demo:** lo stop si sposta da solo, ma solo se la regola è stata provata nel laboratorio e il titolare ha deciso di cambiare D-16. Indica quali prove servono: interruzioni, ripresa, duplicazioni, latenza, limiti del broker.

Per ogni fase: costo una tantum e mensile, tempo del titolare, dipendenze (MT4 o MT5, desktop o iPad), il **risultato che farebbe abbandonare** la fase e le decisioni del titolare necessarie.

**CHE COSA NON FARE**

- Non suggerire l'uso su un conto reale.
- Non proporre parametri di stop come raccomandazione di trading.
- Niente credenziali o dati personali nella risposta.

**CONSEGNA**

1. Un verdetto in dieci righe.
2. La matrice: opzione | che cosa risolve | fatto verificato e fonte | che cosa resta da provare | costo | rischio | decisione proposta.
3. Il piano a tappe.
4. L'obiezione più forte alla tua raccomandazione.

---
