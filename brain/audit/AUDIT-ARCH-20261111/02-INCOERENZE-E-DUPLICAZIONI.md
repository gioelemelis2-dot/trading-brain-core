# 02 · Incoerenze, duplicazioni e lacune tra documenti

Audit AUDIT-ARCH-20261111 · Nessuna correzione è stata applicata: ogni voce indica la proposta e chi può eseguirla, previa approvazione dove richiesto (D-07).

## 1. Incoerenze

| Id | Dove | Problema | Proposta | Gravità |
|---|---|---|---|---|
| I-01 | `CONTINUITA.md`, `collaborazione/LOCK.md` | Dicono "sviluppo sospeso, Claude non avvia attività"; l'utente ha poi assegnato questo audit | Aggiornate in questa tappa (sezione "audit in corso") | media |
| I-02 | `governance/REGISTRO-CONOSCENZE.md` | Fermo alla preparazione della prima revisione: non registra la seconda revisione V2, i difetti C-01…C-17, lo stato dello Studio 01 | Aggiornare in un commit di registro | media |
| I-03 | `glossario/DOMANDE-APERTE.md` | Non contiene le questioni aperte Q-01…Q-07 della seconda revisione | Aggiungerle | bassa |
| I-04 | `audit/03-MATRICE-LACUNE.md` | Scritta prima di L2.4–L2.6 e del lavoro quantitativo: Area A e Area L/M sottostimate, Area F parzialmente coperta dagli strumenti di revisione | Nuova versione datata (non sovrascrivere la precedente) | media |
| I-05 | `architettura/ARCHITETTURA.md` | Architettura solo didattica: non prevede Strategy Discovery Lab, Trading Guardian, motore di rischio, dati | Proposta di uno strato "Laboratori e sistemi" (documento 05); **modifica strutturale → serve approvazione** | **alta** |
| I-06 | `bibliografia/BIBLIOGRAFIA.md`, `REGISTRO-MODIFICHE.md` | Il registro dice "185 voci"; il conteggio attuale è ≈ 190 righe dopo le aggiunte S2 | Aggiornare il conteggio con metodo dichiarato | bassa |
| I-07 | `STANDARD.md` §8 vs L2.1–L2.3 | Regola delle etichette di classe non applicata alle prime tre lezioni | Allineare alla prima revisione delle lezioni (sviluppo oggi sospeso) | media |
| I-08 | `collaborazione/da-gemini/consegne/README.md` | Prevede consegne nel repository; in pratica i materiali V2 sono arrivati come allegati in chat e **non sono archiviati** nel Brain | Decidere dove archiviare le consegne di Gemini (documento 05 §4) | **alta** (rischio di perdita) |
| I-09 | `ANTIGRAVITY_V2_REVIEW_PACKAGE.md` (Gemini) | Due manifest con hash diversi | Già contestato (C-16) | alta, in carico a Gemini |
| I-10 | `MANIFEST_REVISIONE_CLAUDE.sha256` | Riferito al commit `3bbe137`; `LEGGIMI.md` è cambiato dopo | Già dichiarato nel `LEGGIMI`; rigenerare al prossimo commit della cartella | bassa |
| I-11 | `governance/DECISIONI.md` | D-08 ancora "da confermare"; D-12 (sospensione) è parzialmente superata dall'incarico di audit | Chiedere all'utente; registrare D-13 per l'audit | media |
| I-12 | `collaborazione/PROTOCOLLO-OPERATIVO.md` | Provvisorio; Master Mission e Protocollo comune ancora assenti (D-09) | In attesa dell'utente | media |
| I-13 | `piano/PIANO-ESPANSIONE.md` | Sprint S3–S7 sospesi; la roadmap non include il lavoro quantitativo di Gemini, lo Strategy Discovery Lab o il Guardian | Sostituire con la pianificazione a tre mesi (documento 07), dopo approvazione | media |
| I-14 | `audit/02-VERIFICA-AFFERMAZIONI.md`, voce C1 (rischio di rovina "praticamente escluso") | Ora è quantificabile con strumenti verificati: con edge noto e rischio fisso la rovina è bassa, ma dipende da costi, limite giornaliero, clustering e incertezza sull'edge (seconda revisione, §5.D) | Aggiungere un rimando nella prossima correzione del v1 (S5) | bassa |

## 2. Duplicazioni

| Id | Elementi | Natura | Proposta |
|---|---|---|---|
| D-01 | `collaborazione/revisione-materiali-gemini/strumenti/riferimento_rovina.py` e `R-CLAUDE-20261111-01-V2/verifiche/c1_esatto_challenge.py` | Due calcoli esatti di challenge con modelli quasi uguali (barriere, limite giornaliero, giorni) | Un solo modulo canonico `strumenti/rischio/` con test, quando lo sviluppo riapre; i due originali restano come documenti storici della revisione |
| D-02 | Tre descrizioni del processo di ricerca: v1 lezione 0.4, `CHECKLIST-REVISIONE.md` sez. G, Modulo 8 in `ARCHITETTURA.md` | Stesse regole (pre-registrazione, OOS, test multipli) con formulazioni diverse | Un unico "Protocollo di ricerca" canonico (Modulo 8.1) a cui le altre parti rimandano |
| D-03 | Tre elenchi di questioni aperte: `glossario/DOMANDE-APERTE.md`, §10 della seconda revisione, §7 della contestazione | Sovrapposizione parziale | Un solo registro (`DOMANDE-APERTE.md`); gli altri documenti rimandano ai codici |
| D-04 | Regole FTMO descritte in `CHECKLIST-REVISIONE.md` (sez. C) e nel rulebook di Gemini (non consegnato) | Due fonti per lo stesso contenuto | Il rulebook, una volta verificato su fonti ufficiali, diventa l'unica fonte; la checklist rimanda |
| D-05 | Bibliografia: "Cripto-attività" compare due volte (MiCAR e Circolare 30/E) | **Falso duplicato**: fonti diverse con lo stesso tema | Nessuna azione; segnalato per completezza |

## 3. Lacune trasversali (non di contenuto)

| Id | Lacuna | Conseguenza |
|---|---|---|
| L-01 | Nessun dato reale nel Brain | Nessuna affermazione empirica può essere verificata internamente; lab S3 e riproduzione 0.17 bloccati |
| L-02 | Nessun esecutore unico dei test degli strumenti | La verificabilità dipende dal ricordare quali script eseguire |
| L-03 | Nessun archivio delle consegne di Gemini | Rischio di perdita della versione congelata; le revisioni restano senza oggetto conservato |
| L-04 | Nessuna definizione scritta di "Trading Guardian" | Rischio che Claude e Gemini costruiscano due cose diverse con lo stesso nome |
| L-05 | Regole FTMO non verificate su fonti ufficiali | Ogni risultato dello Studio 01 è condizionato a regole non confermate |
| L-06 | Nessun registro delle ipotesi di ricerca (pre-registrazione) fuori dai documenti | Rischio di HARKing e test multipli non contati nel Discovery Lab |
