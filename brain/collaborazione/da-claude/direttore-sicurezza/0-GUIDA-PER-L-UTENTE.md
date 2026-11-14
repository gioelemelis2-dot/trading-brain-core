# Guida: insediare ChatGPT come Direttore generale della sicurezza (DGS)

## 1. Prepara ChatGPT (una volta sola)
1. **Crea un Progetto** chiamato «Trading Brain». Con il piano Plus i Progetti tengono insieme istruzioni, file e chat; se il nome nel menu è diverso, cerca «Progetti» nella barra laterale.
2. **Istruzioni del Progetto:** incolla il blocco di `1-ISTRUZIONI-DEL-PROGETTO.md` (5.053 caratteri). Valgono per ogni chat del Progetto, così ChatGPT non le dimentica.
3. **File del Progetto:** carica
   - `trading_brain_completo.zip` (tutto il materiale);
   - i file sciolti: `INDICE-PER-IL-DGS.md`, `PROGETTO-GENERALE-20261115.md`, `CONTINUITA.md`, `REGISTRO-DIFETTI.md`, `H-002-REVISIONI.md`, `H-002-v3.2-PROPOSTA.md`, `DECISIONI.md`, `DECISIONI-APERTE.md`.
   Se c'è un limite al numero di file, basta lo ZIP più l'INDICE: dentro c'è tutto.
4. **Modello:** scegli quello di **ragionamento** più forte del tuo piano (quello che «pensa» più a lungo) e controlla che possa eseguire codice Python. Serve per scompattare l'archivio, verificare il MANIFEST e far girare test e mutanti.
5. **Memoria:** se ChatGPT ha la memoria fra le chat, conviene limitarla al Progetto. Così le abitudini «gentili» delle altre chat non entrano qui.

## 2. Si può «spegnere» la compiacenza?
**No, non esiste un interruttore**, né nel codice né nelle impostazioni: la tendenza a dare ragione nasce da come questi modelli sono addestrati. Si può però limitare molto:
1. **Istruzioni vincolanti:** etichette su ogni affermazione e niente complimenti. È già nelle istruzioni.
2. **Prove obbligatorie:** un «d'accordo» senza un controllo mostrato non vale.
3. **Controllo incrociato:**
   - DeepSeek rilegge la prima relazione del DGS (`4-PROMPT-DEEPSEEK-CONTROLLO-DEL-DGS.md`);
   - Claude verifica i suoi rilievi sul codice prima di applicarli, come per Gemini.
4. **Il tuo atteggiamento:** non premiare l'accordo. Quando ti dà ragione, chiedi «dimostralo». Quando ti piace una risposta, chiedi «qual è il punto più debole di quello che hai scritto?».

## 3. In che ordine
1. **Messaggio 1** (`2-MESSAGGIO-1-MANDATO.md`), in una chat nuova del Progetto: insediamento, inventario, mandato, roadmap, limiti, aspettative, bias, viabilità, proposte.
2. Portami la sua risposta. La archivio così com'è in `brain/collaborazione/da-chatgpt/` e verifico i rilievi sul codice e sui documenti.
3. In parallelo puoi mandarla a **DeepSeek** con `4-PROMPT-DEEPSEEK-CONTROLLO-DEL-DGS.md`.
4. **Messaggio 2** (`3-MESSAGGIO-2-REVISIONE-R11.md`), nella stessa chat: revisione tecnica R11 di H-002. È lo stesso giro che sta facendo Gemini.

## 4. Cosa NON mandare
Stipendio, budget, numeri del conto, journal dei trade, nonce, dati di mercato scaricati. Il pacchetto è già pulito: l'ho controllato prima di prepararlo.

## 5. Cosa serve sapere da te (rispondimi quando puoi)
1. **Il profilo che ChatGPT riceve** dice: circa 2 anni di trading, risultati altalenanti, «emotivo e impulsivo», obiettivo 1–2% al mese. È già nel documento «Progetto generale» che hai mandato a DeepSeek. Va bene, o vuoi togliere qualcosa?
2. **Tempo:** quante ore alla settimana dedichi al progetto, adesso e quando partirà la demo? Senza questo il DGS non può giudicare se la roadmap è realistica.
3. **Capitale:** vuoi dirgli almeno l'ordine di grandezza di quanto pensi di investire (sfide, abbonamenti), senza dati personali? Facoltativo, ma rende concreto il giudizio sulle aspettative.
4. **Strumenti:** il tuo ChatGPT Plus ha i Progetti e l'esecuzione del codice? Se no, adatto le istruzioni.
