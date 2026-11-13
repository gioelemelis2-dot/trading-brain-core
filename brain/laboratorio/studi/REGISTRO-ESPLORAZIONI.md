# Registro delle esplorazioni sui dati di sviluppo

Rilievo di Gemini G-20261113-01: ogni sguardo ai dati che orienta le idee deve essere scritto, altrimenti le prove implicite sfuggono al conteggio (DA-19, DA-28). Qui si annota ogni analisi esplorativa: cosa, quando, su quale periodo, con quali parametri. Le esplorazioni non sono prove e non dimostrano nulla. Generano ipotesi, che vanno scritte, sigillate e verificate sul periodo sigillato.

**Regola:** solo periodo di sviluppo (dal 15/11/2023, DA-26). Gli script rifiutano date precedenti.

| # | Data | Chi | Script / commit | Periodo | Parametri decisi prima | Note |
|---|---|---|---|---|---|---|
| E-001 | 2026-11-14 | Claude (eseguito dall'utente sul Mac) | `studi/studio_sessioni.py` | 2025-11-13 → 2026-11-12 | Sessioni come in `tb_sessioni.pine`. Compressioni: 12 candele da 5 minuti sotto 0,5 × la mediana dei 20 giorni precedenti, esito nelle 12 candele dopo. Spread: scenari 0,20 / 0,35 / 0,50 USD (ipotesi, non misure) | Richiesta dell'utente: ore e sessioni che spingono o scaricano, scalping a 1, 5 e 15 minuti, piccoli range. Ogni tabella è confrontata con gli stessi dati a direzioni casuali. Londra e New York si sovrappongono: la «stessa direzione» fra loro è gonfiata anche nel confronto casuale. **Esito (commit `9f47272`, lettura di Claude):**
- la volatilità è concentrata fra le 14 e le 17 italiane;
- nessuna struttura direzionale chiaramente diversa dal caso;
- due indizi deboli, circa 2σ, con molti confronti fatti, quindi non significativi:
  - Londra nella stessa direzione di Tokyo: 56,2% contro 50,4% casuale;
  - dopo la chiusura di Londra, New York resta dentro il range di Londra: 47% contro 38%.
- Candela mediana: circa 1,9–2,2 USD a 1 minuto, 4,5–5 USD a 5 minuti, 8–9 USD a 15 minuti.
- Le compressioni di un'ora si rompono quasi sempre entro l'ora successiva; false rotture come nel caso (30–41%). |
