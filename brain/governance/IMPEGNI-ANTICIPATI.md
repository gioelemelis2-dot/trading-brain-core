# Registro degli impegni anticipati

**Scopo:** fissare per iscritto cosa l'utente (o un collaboratore) si aspetta o sceglierebbe **prima** di vedere un risultato, per poterlo confrontare dopo con la scelta effettiva. Serve contro l'autoinganno: aiuta a vedere quanto un risultato ha spostato una scelta.

**Cosa NON è:**
- non è una regola operativa;
- non cambia schede, codice o criteri: valgono solo le schede sigillate;
- non è un sigillo nel senso del registro delle prove: non ha impronta SHA-256 e non entra in N.

**Come si usa:**
- ogni voce dice chi la dichiara, quando, prima di cosa e in che forma esiste l'originale;
- quando arriva la scelta effettiva, si aggiunge il confronto nella stessa riga. Le voci non si modificano: si aggiunge.

| # | Dichiarato da | Data dichiarata | Prima di | Impegno | Stato operativo | Registrato | Confronto con la scelta effettiva |
|---|---|---|---|---|---|---|---|
| IA-01 | Utente | 14/11/2026 | aver visto il «banco di taratura del motore» | Il vantaggio minimo che sceglierebbe oggi è **0,15 R per trade** | **Nessuno.** La soglia nel codice resta quella della scheda H-002 v3.1 (criterio 1 dello screening: R medio netto ≥ +0,05 R) | da Claude il 15/11/2026, su dichiarazione scritta dell'utente in chat | da fare quando l'utente sceglierà il numero dopo il banco |

**Note su IA-01:**
- **La data e il «prima di» sono dichiarati dall'utente:** Claude non può verificarli. Se esiste l'originale scritto il 14/11 (file, messaggio, nota con data), va archiviato qui o citato con dove si trova e la sua data.
- **La revisione esterna del 15/11** (`collaborazione/da-revisori-esterni/2026-11-15-nucleo-statistico-e-incidente.md`) la chiama «numero sigillato il 14/11». In questo registro è un **impegno anticipato**, non un sigillo: niente impronta e niente N.
- **Il «banco di taratura del motore»** non è ancora documentato nel repository: va descritto (cos'è, chi l'ha fatto, quando) per poter fare il confronto.
- **15/11, dal censimento di Gemini:** il «banco» è con ogni probabilità la taratura di Gemini su mercati inventati (passi 2862–2997 del 14/11), la cui esecuzione completa si è interrotta con log vuoto. Da confermare dall'utente, insieme all'ora della nota rispetto ai piloti.
- **16/11, risposta dell'utente:** non sa quando ha scritto lo 0,15 R né a cosa si riferisse il «banco di taratura del motore». Quindi IA-01 resta una **dichiarazione senza prova di anteriorità**: vale come indicazione di preferenza, **non** come impegno preso prima di vedere un risultato. Il «banco» resta non identificato (l'ipotesi di Claude, la taratura di Gemini su dati inventati, non è confermata).
- **Rimedio proposto da Claude:** fissare oggi, prima di qualsiasi idea per H-003, la soglia minima per le ipotesi future come nuova voce (IA-02). La data del commit nel repository sarà la prova di anteriorità che a IA-01 manca.

