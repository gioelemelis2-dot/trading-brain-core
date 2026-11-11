# Documento di continuità

Ultimo aggiornamento: **2026-11-11**, fine sprint **S1**. Leggere questo file per primo all'inizio di ogni sessione.

## Dove siamo
- Fasi completate: **1 Audit · 2 Ricerca (prima passata) · 3 Progettazione**. Fase **4 Sviluppo** avviata con l'unità 2.1 del Modulo 2.
- Il manuale v1 è intatto (artifact `https://claude.ai/artifact/T4xESphh3BmonZPoprQBtb` e copia in `originale/`).
- Nessuna correzione è stata ancora applicata al v1: sono in `audit/02-VERIFICA-AFFERMAZIONI.md`.

## Prossima azione esatta (sprint S2)
1. Leggere `glossario/DOMANDE-APERTE.md` Q4 e verificare sui siti ufficiali le ultime note di implementazione Fed e i tassi BCE; aggiornare L2.1 §8 se utile.
2. Scrivere **L2.4 Tassi nominali, reali e inflazione attesa** (Fisher, TIPS/BTP€i, breakeven, tassi reali e oro, legame con Gordon), **L2.5 Bilancio della banca centrale** (QE/QT, riserve, taper tantrum 2013 con numeri verificati), **L2.6 Fed/BCE/BoJ/BoE** (mandati, strumenti, calendari; verificare BoE e BoJ).
3. Per ogni lezione: modello a 20 sezioni (`governance/STANDARD.md` §4), fonti con stato, esempi numerici ricalcolati con uno script in `strumenti/`.
4. Aggiornare `REGISTRO-CONOSCENZE.md`, `REGISTRO-MODIFICHE.md`, `GLOSSARIO.md`, `moduli/m02-macro/README.md` e questo file.

## Sprint successivi (vedi `piano/PIANO-ESPANSIONE.md`)
S3 lab event study (richiede accesso di rete a dati FRED/BCE) · S4 traccia 10.1 statistica · S5 correzioni v1 → lezioni v2 · S6 unità 2.2–2.3 · S7 serie storiche + pipeline dati.

## Convenzioni da mantenere
- Lingua: italiano. Riquadri del v1: Definizione · Esempio · Errori tipici · Sintesi · Oltre il vault.
- File lezione: `moduli/mXX-nome/L<m>.<n>-titolo.md` con intestazione YAML (id, versione, data, stato, revisione_entro).
- Mai segnare una fonte come V senza averla letta. Mai segnare una padronanza senza cancello superato dichiarato dall'utente.
- Commit sul branch `claude/vibrant-cannon-5uunho` del repository `l-Altro`, cartella `brain/`.

## Domande per l'utente ancora aperte
- I dati del vault Obsidian (per rigenerare la tabella 0.17) sono disponibili?
- Si preferisce che il Brain resti in questo repository (`l-Altro/brain/`) o in un repository dedicato?
- Rigenerare in futuro un manuale HTML (stile v1) a partire dai file Markdown?
