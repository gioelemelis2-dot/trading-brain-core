# Prova D2 · riconciliazione del Guardian sulla demo (DA-25), procedura · 26/11/2026

**Perché.**
- È la prova senza strategia che il DGS preferisce (DGS-20 Q2).
- Risponde a una domanda sola: i numeri del Guardian (perdita allo stop, commissione, margine) coincidono con quelli del broker sul conto demo?
- Non tocca la riserva né il lavoro sulla macchina, e non usa denaro reale.

**Decisione del titolare: presa (D-57, 26/11).** Restano da approvare le tolleranze (DGS-21 §B). Scheda operativa: `SCHEDA-D2-PER-IL-TITOLARE.md`.

## Stato documentale verificato (26/11)
- `dati/reali/demo_broker_mt5_50k_xauusd.toml`: `riconciliato = false`; il broker di quel conto da 50.000 USD non è noto.
- `dati/costi/SPECIFICHE-FPMARKETS-XAUUSD-20261118.md`: le specifiche sono state lette dall'app **MT5**, conto **Raw** reale con saldo 0, simbolo `XAUUSD.cyr`. La commissione è di 6 USD per lotto, ma **da confermare** se per lato o andata e ritorno.
- La demo FP Markets aperta è **MT4 Raw** (roadmap del 17/11).
- **Piattaforma della demo e piattaforma delle specifiche sono diverse.** Prima di interpretare uno scarto vanno identificati piattaforma, tipo di conto, strumento, valuta e condizioni (DGS-20).
- `dati/reali/TEMPLATE_RICONCILIAZIONE_DA25.toml` è un **esempio** (FTMO, EURUSD, ES), non il modulo di questo conto.

## Passi
1. **Profilo del conto.** Il titolare legge dalla demo MT4 Raw: valuta del conto, leva, e per XAUUSD dimensione del contratto, passo, valore del punto, commissione e livello di margine. Manda gli screenshot a Claude.
2. **Scheda del Guardian prima di operare.** Claude prepara la scheda del conto demo con quei valori e calcola **prima**, per ogni operazione prevista, la perdita allo stop, la commissione e il margine. La previsione si salva nel repository con data e ora, **prima** del confronto.
3. **Operazioni.** 2–3 operazioni da 0,01 lotti su XAUUSD, ciascuna con lo stop inserito all'apertura. Si annota l'ora di apertura e, se possibile, uno screenshot del margine usato in quel momento.
4. **Estratto.** Al termine, l'estratto o la cronologia dei conti della demo, con prezzi eseguiti, commissioni e risultato.
5. **Riconciliazione**, una riga per operazione e per voce:

| Voce | Previsione del Guardian | Osservazione del broker | Scarto | Spiegazione | Esito |
|---|---|---|---|---|---|
| volume, stop, prezzi effettivi | | | | | concorde / discordante / non osservabile |
| perdita prevista allo stop | | risultato **riconciliato al prezzo eseguito** (la differenza di esecuzione si mostra a parte) | | | |
| commissione, per lato o totale | | | | | |
| margine all'apertura | **nessuna previsione del Guardian** (verificato: `limiti.margine` è la distanza dal limite di drawdown); al più un calcolo esterno attribuito al profilo demo | screenshot prima e subito dopo, altrimenti «non osservabile» | | | |

- Le tolleranze **non** sono in DA-25 (DGS-21 §B, rettifica). Si usa la convenzione che il titolare approverà prima delle operazioni (proposta di DGS-21, confermata da DGS-22).
- Ogni voce ha un esito: concorde, discordante o non osservabile.

6. **Registrazione.** La prova si scrive nel diario. Il risultato vale **per quel profilo** (demo MT4 Raw). I parametri del profilo di destinazione (MT5, FTMO) restano da verificare.

**Che cosa NON fa:** non autorizza l'uso del Guardian per decidere. Quello segue il suo gate, con `riconciliato = true` solo se tutte le voci osservabili sono concordi.
