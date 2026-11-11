# Prompt di ripresa automatica (per Claude)

Da usare quando una sessione riparte dopo un'interruzione (limite di utilizzo, nuova sessione, cambio di dispositivo). Si può incollare così com'è, oppure inviare come messaggio programmato.

---

```
Riprendi il lavoro sul Trading Brain senza chiedere conferme intermedie per le attività già autorizzate.

1. Repository gioelemelis2-dot/l-Altro, branch claude/vibrant-cannon-5uunho, cartella brain/.
   Esegui git fetch e verifica di essere allineato; se trovi modifiche non tue, fermati e segnalale.
2. Leggi brain/CONTINUITA.md, poi brain/collaborazione/LOCK.md e governance/DECISIONI.md.
3. Se esiste un checkpoint di un'attività in corso (es. audit/*/00-CHECKPOINT.md con tappe non ✅),
   riprendi dalla prima tappa non completata.
4. Controlla se sono arrivati nuovi materiali di Antigravity (allegati nella conversazione o
   cartelle collaborazione/da-gemini/). Se sì: verifica gli hash e avvia la revisione indipendente
   secondo la procedura in CONTINUITA.md, senza modificare i file di Antigravity.
5. Se non c'è nulla da riprendere e restano solo decisioni dell'utente: NON avviare nuove attività,
   non fare controlli ripetuti; scrivi in due righe che cosa aspetta l'utente e fermati.
6. Regole sempre valide: nessuna modifica a lezioni o materiali di Antigravity senza autorizzazione,
   nessuna migrazione, nessuna strategia o backtest nuovi, mai dichiarare verificato ciò che non hai
   controllato. Salva un checkpoint a ogni tappa e aggiorna CONTINUITA.md prima di fermarti.
```

---

## Note
- Claude non può accorgersi da solo che un limite di utilizzo si è azzerato. Prima di un lavoro lungo programma un messaggio di ripresa con questo prompt (strumento di invio differito), all'orario indicato dal sistema per lo sblocco o, in mancanza, dopo alcune ore.
- Se non c'è un lavoro in corso, nessuna ripresa viene programmata: eviterebbe solo di consumare crediti.
