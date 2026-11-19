# Compito per Gemini/Antigravity: operazioni dichiarate della fonte P-001 (19/11/2026)

**Da dare solo dopo la consegna di R17.** Base: D-41 (valutazione della fonte, nessuna scheda né prova sul banco). Il testo da incollare è fra le due righe di trattini.

---

COMPITO P-001 — catalogo delle operazioni dichiarate (Brad Goh). Solo raccolta di informazioni: nessuna strategia, nessuna prova.

CONTESTO
- Leggi `brain/laboratorio/ipotesi/DOSSIER-FONTE-P001.md` (prima parte, di Claude) e `brain/laboratorio/ipotesi/CATALOGO-OPERAZIONI-P001.md` (regole e colonne del catalogo).
- Elenchi dei video: `brain/laboratorio/ipotesi/fonti/p001/elenco_bt_videos.psv` (111 operazioni dal vivo, canale @bradgtrades) e gli episodi «Market Mechanics» in `elenco_tg_videos.psv`.

REGOLE (vincolanti)
1. **Nessun video scaricato.** Si scaricano solo i sottotitoli automatici (testo), con yt-dlp `--skip-download --write-auto-subs`, in `~/Downloads/p001_sottotitoli/`.
2. **Le trascrizioni restano sul Mac.** NON vanno nel repository: sono contenuti dell'autore. Nel repository vanno solo informazioni, link e minuto.
3. **Se puoi analizzare i video direttamente** (immagini del grafico), puoi leggere livelli e risultati mostrati. Se non puoi, dillo e lavora solo sul testo.
4. **Per XAUUSD, GBPJPY ed EURUSD**, un'operazione con candele anteriori al 15/11/2023 si registra senza guardare il grafico («Data ammessa» = no). I video di @bradgtrades dovrebbero essere tutti successivi: controllalo.
5. **Quattro colonne separate:**
   - ciò che l'autore DICE;
   - ciò che si VEDE nel video;
   - la TUA interpretazione;
   - il dato non disponibile, che si scrive «ignoto».
6. **Per ogni motivazione** indica se l'autore la dice PRIMA che l'operazione si chiuda o DOPO.
7. **Ogni dato** ha il link con il minuto (`https://www.youtube.com/watch?v=ID&t=SECONDIs`).
8. **Ordine cronologico completo**, perdite comprese. Nella tabella «Lacune» annota:
   - le operazioni annunciate ma non mostrate;
   - i video montati, con salti nel tempo;
   - i periodi senza video.
9. **Rischio in R:**
   - calcolalo solo se ingresso, stop e dimensione sono letti o detti;
   - R = risultato / (|ingresso − stop| × dimensione × valore del punto);
   - indica sempre da dove viene ciascun numero.
10. **Spazio sul disco:** controlla `df -h ~` prima di iniziare. Se sono liberi meno di 3 GB, fermati e avvisa.

CHE COSA CONSEGNARE
- Il file `P001-CATALOGO-GEMINI.md`, sul ramo `rev/gemini-p001`, nella cartella `brain/collaborazione/da-gemini/`.
  - Contenuto: una riga per operazione, con le colonne di `CATALOGO-OPERAZIONI-P001.md` più «Si vede nel video», «Rischio in R e fonte dei numeri», «Conto o broker mostrato».
- **Prima una prova su 10 video**: i 10 più recenti di @bradgtrades. Consegnali e aspetta il via prima di fare gli altri 101.
- **Un riepilogo:**
  - quanti video hanno ingresso, stop e dimensione leggibili;
  - quante motivazioni sono dette prima dell'esito;
  - le incoerenze fra parole e immagini (per esempio uno stop detto diverso da quello disegnato, o un risultato non compatibile con la dimensione).
- Nei mandati, scrivi `~` al posto dei percorsi completi che contengono il nome utente (D-28).

---
