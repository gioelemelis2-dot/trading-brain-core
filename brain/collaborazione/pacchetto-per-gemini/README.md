# Pacchetto di revisione per Gemini

Stato: PROVVISORIO · preparato da Claude il 11/11/2026 · da leggere dopo [`../HANDOFF-GEMINI.md`](../HANDOFF-GEMINI.md).

Obiettivo: permettere a Gemini una revisione **indipendente** del lavoro di Claude senza dover ricostruire il contesto.

| File | Per che cosa |
|---|---|
| [`01-REVISIONE-L2.4-L2.6.md`](01-REVISIONE-L2.4-L2.6.md) | Registro delle affermazioni, formule ed esempi delle tre nuove lezioni, ognuno con un codice da citare nel rapporto |
| [`02-ARCHITETTURA-E-REGISTRI.md`](02-ARCHITETTURA-E-REGISTRI.md) | Domande guida per la revisione critica di architettura, mappa, registri e governance |
| [`03-CONFRONTO-QUANTITATIVO.md`](03-CONFRONTO-QUANTITATIVO.md) | Dove il lavoro quantitativo di Gemini (rovina FTMO, motore, Discovery Lab) incrocia contenuti già presenti, e come confrontarli |
| [`MANIFEST.sha256`](MANIFEST.sha256) | Impronte SHA-256 di tutti i file del Brain al momento della preparazione, per verificare che si stia esaminando la versione giusta |

## Come lavorare
1. Annotare l'hash del commit esaminato (`git log -1`) e verificare le impronte: `cd brain && sha256sum -c collaborazione/pacchetto-per-gemini/MANIFEST.sha256`. File diversi = versione diversa: indicarlo nel rapporto.
2. Riprodurre gli esempi con i comandi indicati (solo libreria standard di Python).
3. Consegnare **un rapporto per ambito** in `collaborazione/da-gemini/` secondo [`../da-gemini/MODELLO-RAPPORTO.md`](../da-gemini/MODELLO-RAPPORTO.md), citando i codici (es. `L2.4-A03`, `L2.5-F02`).
4. I file sotto revisione (`moduli/m02-macro/L2.4…L2.6`) sono **congelati** finché la revisione è in corso (vedi `../LOCK.md`): Claude non li modifica.
