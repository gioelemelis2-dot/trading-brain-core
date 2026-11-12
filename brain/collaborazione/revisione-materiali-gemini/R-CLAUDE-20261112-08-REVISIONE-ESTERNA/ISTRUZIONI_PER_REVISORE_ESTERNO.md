# Istruzioni per il revisore esterno

## Contesto
Il **Trading Brain** è un progetto di ricerca quantitativa sul trading, in italiano. Il proprietario umano prende tutte le decisioni; due modelli di intelligenza artificiale lavorano come centri di ricerca indipendenti.

In questo pacchetto c'è un ciclo completo di revisione reciproca:
1. **Gemini** ha scritto un'architettura e una roadmap pluriennale (`01-gemini-architettura-v2/`).
2. **Claude** ne ha fatto un audit indipendente (`02-claude-audit/`).
3. **Gemini** ha controverificato l'audit (`03-gemini-controverifica/`).
4. **Claude** ha valutato la controverifica e corretto alcuni propri errori (`04-claude-valutazione/`).
5. In `05-fonti-primarie/` ci sono i file del progetto citati dalle due parti: rulebook, schede di strategia, motore V3.3, standard di qualità del Brain, estratto del manuale.

Ti chiediamo una **verifica esterna**: i due modelli hanno prodotto molta convergenza e pochi disaccordi, e non possono escludere di condividere gli stessi errori.

## Che cosa chiediamo
1. **Fatti.** Controlla a campione le affermazioni fattuali di entrambi sui file in `05-fonti-primarie/` e tra i documenti (citazioni, conteggi, numeri di riga, che cosa ha scritto chi). Segnala ogni discrepanza.
2. **Matematica.** Verifica in modo indipendente almeno:
   - il calcolo di potenza (594 trade a potenza 80%, test unilaterale con α 5%; 1.417 con soglia t > 3; ipotesi WR 0,40, R:R 2, costo 0,05R, i.i.d.);
   - l'affermazione che il caso peggiore di un portafoglio con stop sia «tutti gli stop colpiti insieme» e non «correlazione ρ = 1»;
   - la critica alle stime sigillate con hash senza sale.
3. **Fonti.** Dove puoi, verifica le citazioni bibliografiche contestate:
   - Lo, Repin e Steenbarger 2005;
   - Almgren e Chriss (DOI);
   - Lou, Polk e Skouras 2019;
   - Bouchaud, Farmer e Lillo;
   - Branch e Ma 2012;
   - Pine Script v6.

   Indica se hai letto la fonte o solo una scheda bibliografica.
4. **Metodo.** Valuta se le proposte principali sono solide:
   - modello epistemico a più assi;
   - Guardian G0 consultivo;
   - criterio «NON STIMABILE»;
   - rischio di contaminazione delle ipotesi generate da LLM;
   - indicatori comportamentali validati sui dati di una sola persona.
5. **Errori comuni.** Cerca gli errori o le assunzioni **condivisi da entrambi** i modelli, che nessuno dei due ha visto. È la parte più importante.
6. **Decisioni.** In `DECISIONI-APERTE.md` ci sono le decisioni riservate all'utente. Segnala se ne manca qualcuna, se qualcuna è mal posta o se una raccomandazione è debole. **Non prendere decisioni al posto dell'utente.**

## Regole
- Non scegliere un vincitore tra Claude e Gemini: interessa solo che cosa è corretto.
- Distingui sempre tra fatto verificato, calcolo, inferenza, ipotesi e scelta progettuale.
- Non inventare fonti, DOI, dati o risultati. Se non puoi verificare qualcosa, scrivilo.
- Indica per ogni conclusione il grado di certezza.

## Formato della risposta richiesto
1. Sintesi (al massimo 10 righe).
2. Tabella dei rilievi: id, documento e punto, affermazione esaminata, verifica eseguita, esito (corretta / parzialmente corretta / errata / non verificabile), gravità.
3. Errori condivisi da entrambi i modelli.
4. Osservazioni sulle decisioni aperte.
5. Limiti della tua verifica (che cosa non hai potuto controllare).
