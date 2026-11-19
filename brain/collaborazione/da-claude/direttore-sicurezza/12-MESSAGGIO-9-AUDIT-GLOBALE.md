# Messaggio 9 al DGS: controverifica dell'audit globale (19/11/2026)

**Come si manda.** Si incolla il testo qui sotto, fra le due righe di trattini. Insieme si carica il file `AUDIT-GLOBALE-TRADING-BRAIN-E-ROADMAP.md`. Se il caricamento non riesce, si incolla l'audit in due messaggi: il primo fino a «## 3.» esclusa, il secondo da lì alla fine. Nessun dato personale né di mercato.

---

MESSAGGIO 9 AL DGS — solo metodo; nessuna decisione riservata al titolare.

CONTESTO
- Il titolare ha chiesto a Claude un audit complessivo del Trading Brain e della roadmap, in sola lettura. L'audit è allegato (o incollato in due parti).
- D-33 (19/11): prima si finisce la macchina di valutazione, poi le strategie. Il lavoro sull'idea esterna P-001 è in pausa.
- Banco di prova: contatore 1 su 2 (D-26). R17 di Gemini è in corso sul candidato e476a9a.
- Claude ha scritto gran parte del codice e delle specifiche che giudica: il conflitto d'interessi è dichiarato nell'audit.

RICHIESTA
Per ciascuno dei sei punti della sezione finale «Controverifica richiesta al DGS»:
1. Rifate il calcolo o il passaggio indicato **in autonomia**. In particolare:
   - la potenza del §3.1: P = 1 − Φ((0,20 + 1,96·σ/√D − μ)/(σ/√D)), con σ = 1,25 R e D = 1.000. Claude ottiene 2,5%, 24,3% e 71,6% per μ = 0,20, 0,25 e 0,30. Il pilota aveva misurato 71,64% a μ = 0,30 nella cella gaussiana;
   - la probabilità di nessuna perdita rara del §3.2: 0,998^1000 ≈ 0,135 e 0,998^780 ≈ 0,21.
2. Dite se la conclusione provvisoria regge, oppure se regge la spiegazione alternativa più forte.
3. Dite quale decisione cambierebbe se Claude avesse torto.

Inoltre:
4. **Potenza (rischio 1).** L'approssimazione con un trade per seduta, risultati indipendenti e σ = 1,25 è adeguata per un ordine di grandezza? Come cambierebbe con K > 1 trade per seduta e dipendenza fra sedute? L'aggiunta degli altri criteri della verifica (DSR, anni positivi, ultimi 5 anni, drawdown) abbassa la potenza in modo rilevante?
5. **Alternative A1–A5 del §4.4 A** (metro contro obiettivi): sono complete e corrette? Mancano alternative realistiche? Presentatele come opzioni per il titolare, **senza sceglierne una**.
6. **«Definizione di fatto» della macchina** (§4.4 B): l'elenco chiuso proposto è sufficiente e non eccessivo? Va chiarito se il criterio D-31 debba entrare nel perimetro sigillato, con un nuovo candidato e nuovi giri, oppure stare in un modulo separato. Indicate le conseguenze di ciascuna strada sul contatore D-24, senza decidere.
7. **Prova generale a vuoto** (D1, §4.1): le condizioni di successo e di arresto proposte bastano? La tolleranza di ±10 punti sulla potenza attesa è adeguata al numero di repliche che servirebbe?
8. **Seconda lettura.** Qual è, secondo voi, l'errore più importante dell'audit? Che cosa manca nella mappa o nel registro dei rischi?

Formato della risposta: un paragrafo per ciascun punto (1–8). Ogni numero va contrassegnato come «ricalcolato» oppure «preso dall'audit».

---
