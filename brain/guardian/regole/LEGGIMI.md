# Rulebook del Guardian (Q-09)

Due file separati, perché le regole hanno origini diverse (Q-09; DA-13 alternativa A):
- `prop_firm_ftmo.toml`: regole **della prop firm**, ciascuna con citazione testuale della pagina ufficiale, data di consultazione e stato di verifica. Fonti: `fonti/FTMO_REGOLE_ESTRATTO_20261112.txt` (estratto delle pagine ufficiali e SHA-256 delle pagine scaricate il 12/11/2026).
- `regole_personali.toml`: regole **dell'utente**. Sono una **proposta**: nessuna è attiva finché l'utente non la conferma. Ogni regola indica se viene dal Manuale v1 dell'utente o dal vecchio rulebook di Gemini. Le soglie che non sono nel Manuale restano «DA DEFINIRE».

Il vecchio `rulebook.yaml` (archivio V3.3) resta intatto come documento storico.

## Che cosa è cambiato rispetto alle ipotesi del progetto (verifica del 12/11/2026)
1. **Il limite giornaliero ha come base il SALDO alle 00:00 CE(S)T**, non l'equity: limite = saldo a mezzanotte − 5% del capitale iniziale (2-Step). Il controllo durante la giornata invece riguarda l'**equity**, incluse posizioni aperte, swap e commissioni.
   - I simulatori V2–V3.3 erano coerenti con questa regola solo grazie all'ipotesi «nessuna posizione aperta a mezzanotte» (S-09).
   - Con posizioni tenute oltre la notte il G0 deve usare la regola esatta.
2. **Esistono tre prodotti con regole diverse:**
   - 2-Step: 5% giornaliero, 10% statico, 4 giorni minimi, periodo illimitato;
   - 1-Step: 3% giornaliero, 10% trailing sul saldo di fine giornata, regola di consistenza dal 12/10/2026;
   - Instant: 3% giornaliero, 10% trailing intraday, consistenza 30%.
3. **Tipo di conto Standard o Swing:** le restrizioni su notizie e posizioni overnight/weekend valgono solo per il tipo Standard. I dettagli non sono ancora verificati (FAQ non lette).

## Informazioni necessarie dall'utente (per completare il G0)
1. **Prodotto** FTMO in uso o previsto (2-Step, 1-Step, Instant), oppure un'altra prop firm o un broker.
2. **Tipo di conto** (Standard o Swing), **dimensione** e **valuta del conto**.
3. **Piattaforma** (MT4, MT5, cTrader, DXtrade…) e **strumenti** che operi (simboli esatti).
4. **Specifiche dei contratti** del broker per quegli strumenti (dimensione del contratto, valore del tick o del pip, valuta del profitto, orari, swap). Basta una schermata o un'esportazione della scheda del simbolo.
5. **Conferma o modifica** delle regole personali P-01…P-15 e dei valori «DA DEFINIRE».
6. Un **estratto conto** (anche di un conto demo) per la riconciliazione del G0: senza riconciliazione il G0 non va usato per decidere.
