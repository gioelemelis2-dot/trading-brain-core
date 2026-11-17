# Procedura del consuntivo dello storico XAUUSD (BID e ASK)

Preparata da Claude il 17/11/2026. **Si usa solo a scaricamenti finiti.** Ogni comando legge la cache e stampa **solo conteggi, percentuali e date, mai prezzi**. Le soglie di idoneità **non** sono decise: i risultati servono al titolare per deciderle, guardando anche l'effetto dei buchi su segnali ed esiti (DGS-05, addendum §4).

## 0. Prima di cominciare
Gli scaricamenti devono essere finiti. Questo comando non deve stampare nessun processo:
```
pgrep -fl scarica_cache
```
Le ultime righe dei log devono essere un «FINITO» o un riepilogo finale, non un errore:
```
tail -5 ~/scarica_storico.log; tail -5 ~/scarica_ask.log
```
Il codice va aggiornato all'ultima versione:
```
git -C ~/Downloads/trading-brain-core fetch origin feat/esecutore-h002
git -C ~/Downloads/tb-riconta checkout --detach origin/feat/esecutore-h002
git -C ~/Downloads/tb-riconta log --oneline -1
```
Annotare il commit stampato: va dichiarato nel consuntivo.

## 1. Controllo della cache per lato, sulla riserva
```
cd ~/Downloads/tb-riconta
C=~/Downloads/trading-brain-core/brain/dati/reali/cache_dukascopy
python3 -s -B -m brain.dati.pipeline.controlla_cache $C/XAUUSD --inizio 2005-01-01 --fine 2023-10-31 > ~/Downloads/consuntivo_1_bid.txt; echo "codice $?"
python3 -s -B -m brain.dati.pipeline.controlla_cache $C/XAUUSD_ASK --inizio 2005-01-01 --fine 2023-10-31 > ~/Downloads/consuntivo_1_ask.txt; echo "codice $?"
```

## 2. Confronto BID/ASK per giorno
```
python3 -s -B -m brain.dati.pipeline.controlla_cache $C/XAUUSD --ask $C/XAUUSD_ASK --inizio 2005-01-01 --fine 2023-10-31 > ~/Downloads/consuntivo_2_confronto.txt; echo "codice $?"
```

## 3. Intersezione al minuto e buchi (richiesta del DGS)
```
python3 -s -B -m brain.laboratorio.studi.intersezione_bid_ask --cache $C --inizio 2005-01-01 --fine 2023-10-31 --json ~/Downloads/consuntivo_3_intersezione.json > ~/Downloads/consuntivo_3_intersezione.txt; echo "codice $?"
```

## 4. Taratura per lato (griglia diagnostica delle soglie attuali)
```
python3 -s -B -m brain.laboratorio.studi.taratura_completezza --cache $C/XAUUSD --inizio 2005-01-01 --fine 2023-10-31 > ~/Downloads/consuntivo_4_taratura_bid.txt
python3 -s -B -m brain.laboratorio.studi.taratura_completezza --cache $C/XAUUSD_ASK --inizio 2005-01-01 --fine 2023-10-31 > ~/Downloads/consuntivo_4_taratura_ask.txt
```

## 5. Stessi controlli sullo sviluppo (15/11/2023 → 12/11/2026)
Si ripetono i passi 1–4 con `--inizio 2023-11-15 --fine 2026-11-12`, cambiando il nome dei file in `..._sviluppo_...`.

## 6. Cosa mandare
Tutti i file `consuntivo_*`, più il commit annotato al passo 0. Prima di mandarli a ChatGPT, Claude li ricontrolla: devono contenere solo conteggi, percentuali e date.

**Cosa NON si fa in questa fase:** nessuna esecuzione della strategia, nessuna lettura di prezzi, nessuna soglia scelta guardando i numeri «a occhio». Le soglie si decidono con uno studio dichiarato dell'effetto dei buchi.
