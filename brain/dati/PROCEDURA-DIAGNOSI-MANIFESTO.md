# Diagnosi del manifesto sui registri veri (sul Mac del titolare) · 23/11/2026

**Perché.**
- Il manifesto blocca ogni finestra con anche una sola anomalia nei registri dello scaricamento.
- Non è mai stato provato sui registri veri. Il BID fino al 07/06/2009 è precedente al registro per giorno, e `--riprova-vuoti` crea voci doppie (revisione critica del 23/11, punto B.5).
- Questa diagnosi dice **prima** se ci sono anni inutilizzabili.

**Che cosa legge.**
- Solo i due registri e le impronte dei file. I file della riserva non si decodificano.
- Scrive **solo conteggi e date**: mai impronte, mai prezzi.
- Va eseguita dal titolare. Gemini non tocca `brain/dati/reali/`.

## 0. Codice aggiornato in una copia separata
```
git -C ~/Downloads/trading-brain-core fetch origin feat/esecutore-h002
git -C ~/Downloads/tb-riconta checkout --detach origin/feat/esecutore-h002
git -C ~/Downloads/tb-riconta log --oneline -1
```
Annotare il commit stampato.

## 1. Riserva e sviluppo
```
cd ~/Downloads/tb-riconta
C=~/Downloads/trading-brain-core/brain/dati/reali/cache_dukascopy
python3 -s -B -m brain.laboratorio.studi.diagnosi_manifesto --cache $C --inizio 2005-01-01 --fine 2023-10-31 --json ~/Downloads/diagnosi_riserva.json > ~/Downloads/diagnosi_riserva.txt; echo "codice $?"
python3 -s -B -m brain.laboratorio.studi.diagnosi_manifesto --cache $C --inizio 2023-11-15 --fine 2026-11-12 --json ~/Downloads/diagnosi_sviluppo.json > ~/Downloads/diagnosi_sviluppo.txt; echo "codice $?"
```

**Come leggere i codici:**
- **0:** nessuna anomalia;
- **1:** anomalie, contate nel file `.txt`;
- **2:** argomenti o cartella sbagliati;
- un errore «registro dello scaricamento mancante»: i registri stanno in un'altra cartella, e va detto a Claude.

## 2. Che cosa mandare
I quattro file `diagnosi_*` e il commit annotato, a Claude. Claude li ricontrolla prima di girarli al DGS: solo conteggi e date.

**Cosa NON si fa:** non si corregge a mano nessun registro. Se escono anomalie, il modo di trattarle è una decisione di metodo, da portare al DGS prima di toccare il manifesto o i registri.
