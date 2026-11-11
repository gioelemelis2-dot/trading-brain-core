# Protocollo operativo Claude–Gemini

Versione 1.1 · 11/11/2026 · Stato: **PROVVISORIO** — regole pratiche di lavoro in attesa dei documenti fondativi.

> ⚠️ **Questo file NON sostituisce il Master Mission né il Protocollo comune di collaborazione dell'utente (decisione D-09).** Serve solo a lavorare in modo ordinato finché quei testi non sono inseriti in [`fondamenti/`](fondamenti/). Quando ci saranno, prevalgono loro; questo file verrà riallineato e ogni differenza segnalata all'utente.

> **Nota di onestà.** L'utente ha predisposto un *Master Mission* e un *Protocollo comune di collaborazione*. **Questi due testi non sono disponibili nella sessione in cui è stato scritto questo file** (non presenti nella conversazione, né su Google Drive, né tra gli artifact accessibili). Questo protocollo traduce in regole pratiche quanto l'utente ha descritto per iscritto il 11/11/2026. Quando i testi originali saranno copiati in [`fondamenti/`](fondamenti/), **prevalgono loro**: ogni differenza va segnalata all'utente e corretta qui.

## 1. Principi (dalla richiesta dell'utente)

1. **Un solo Brain.** Claude e Gemini lavorano sullo stesso repository e sulla stessa architettura. Nessuno dei due crea una base di conoscenza parallela.
2. **Stessa missione, stessi standard.** Valgono per entrambi `governance/STANDARD.md` (fonti, evidenze, classi di contenuto, ciclo di vita delle lezioni) e le decisioni in `governance/DECISIONI.md`.
3. **Il confronto serve alla qualità**, non è l'obiettivo. Si cercano lacune, contraddizioni, duplicazioni, errori e miglioramenti.
4. **Integrazione solo dopo controllo di qualità.**
5. **Mai due sistemi sullo stesso file nello stesso momento.**
6. **Modifiche strutturali e migrazioni solo con approvazione dell'utente** (D-07).

## 2. Ruoli

| | Claude | Gemini |
|---|---|---|
| Ruolo principale | Sviluppo dei contenuti canonici e **coerenza architetturale** | **Ricerca indipendente**, approfondimenti, verifiche, revisione critica |
| Scrive nei file canonici (`moduli/`, `architettura/`, `audit/`, `mappa/`, `bibliografia/`, `governance/`, `piano/`, `glossario/`, `strumenti/`, `dati/`, `CONTINUITA.md`, `README.md`) | Sì | **No** (propone modifiche tramite rapporto) |
| Scrive in `collaborazione/da-gemini/` (incluse le consegne in `da-gemini/consegne/`) | **No, mai** (solo lettura; D-11) | Sì |
| Scrive in `collaborazione/revisione-materiali-gemini/` (revisione dei materiali di Gemini) | Sì | No (solo lettura) |
| Scrive in `collaborazione/pacchetto-per-gemini/` (materiale per la revisione del lavoro di Claude) | Sì | No (solo lettura) |
| Scrive in `collaborazione/da-claude/` | Sì (risposte, esiti dell'integrazione, richieste a Gemini) | No (solo lettura) |
| Revisiona il lavoro dell'altro | Sì: esamina ogni rapporto di Gemini e risponde | Sì: può revisionare qualsiasi file canonico |
| Aggiorna registri e continuità | Sì | No (Claude registra anche il contributo di Gemini, citandolo) |

L'asimmetria sulla scrittura serve solo a evitare conflitti e a mantenere un unico responsabile della coerenza. Il **giudizio** è simmetrico: un rilievo di Gemini vale quanto uno di Claude e va accolto o respinto con motivazione scritta. L'utente può cambiare questa ripartizione in qualsiasi momento (ad esempio affidando a Gemini interi file o aree): la modifica va in `governance/DECISIONI.md`.

## 3. Branch e file

| Chi | Branch | Dove scrive |
|---|---|---|
| Claude | branch di lavoro indicato in `CONTINUITA.md` | file canonici, `collaborazione/da-claude/` |
| Gemini | `gemini/<argomento>` (uno per attività), creato dall'ultimo stato del branch di Claude | solo `collaborazione/da-gemini/` |

- Un branch di Gemini non tocca file fuori da `collaborazione/da-gemini/`. Se lo fa, Claude non lo unisce e lo segnala.
- I rapporti indicano sempre l'**hash del commit** che hanno esaminato: se il file è cambiato nel frattempo, Claude riconcilia.

## 4. Coordinamento: la bacheca `LOCK.md`

[`LOCK.md`](LOCK.md) elenca chi sta lavorando su cosa. Prima di iniziare un'attività:
1. leggere `LOCK.md`;
2. aggiungere una riga (attività, file coinvolti, chi, inizio, fine prevista);
3. al termine, spostare la riga in "Concluse".

Gemini non scrive nei file canonici, quindi i suoi lock servono a evitare **lavori doppi** (due ricerche sulla stessa fonte), non conflitti di scrittura. Se Gemini non può aggiornare `LOCK.md` (è un file condiviso), dichiara l'attività nell'intestazione del rapporto e Claude la registra.

**Congelamento:** durante una migrazione o una modifica strutturale approvata, `LOCK.md` riporta in alto "CONGELATO" con data: nessuno scrive finché non viene rimosso.

## 5. Ciclo di una verifica o ricerca di Gemini

```
Claude o utente apre una richiesta (da-claude/RICHIESTE.md)  ─┐
Gemini sceglie un'attività dall'elenco in HANDOFF §7          ├─► Gemini lavora su gemini/<argomento>
                                                              ─┘          │
                                    rapporto G-AAAAMMGG-NN in da-gemini/ ◄┘
                                                │
                     Claude esegue il controllo di qualità (§6)
                                                │
           ┌──────────────────────┬─────────────┴───────────┬─────────────────────┐
       accolto               accolto in parte            respinto              disaccordo
     (integrato nei      (integrato ciò che passa      (motivazione           (va in DISACCORDI.md;
      file canonici)        il controllo)                scritta)              decide l'utente)
           └──────────────────────┴──────────┬──────────────┴─────────────────────┘
                     esito in da-claude/ESITI.md + REGISTRO-MODIFICHE con citazione "rapporto G-…"
```

## 6. Controllo di qualità prima dell'integrazione

Un rilievo o un contenuto entra nel Brain solo se:

| # | Criterio |
|---|---|
| Q1 | Ogni affermazione empirica ha una fonte con stato dichiarato (V / V-sec / C / X) |
| Q2 | Le fonti dichiarate **V** sono state lette davvero (almeno abstract o pagina ufficiale) e sono rintracciabili (titolo, anno, sede, link o DOI) |
| Q3 | Nessuna citazione, dato o link inventato; nessun dato simulato presentato come reale |
| Q4 | Formule ed esempi numerici ricalcolati (script o calcolo indipendente) |
| Q5 | Classe del contenuto esplicita (verificato / in verifica / ipotesi / esercitazione / simulato / reale) |
| Q6 | Coerente con l'architettura; se non lo è, la proposta di cambio architettura va all'utente (D-07) |
| Q7 | Non duplica contenuti esistenti; se li migliora, indica che cosa sostituisce |
| Q8 | Limiti e controversie dichiarati |

Il controllo vale anche al contrario: Gemini applica gli stessi criteri quando revisiona il lavoro di Claude.

## 7. Disaccordi

Registrati in [`DISACCORDI.md`](DISACCORDI.md) con le due posizioni, le fonti di ciascuna e che cosa risolverebbe la questione. Nessuno dei due sistemi "vince" per insistenza: se le fonti non bastano, decide l'utente, oppure la questione resta aperta e il Brain la presenta come **controversa**.

## 8. Che cosa nessuno dei due fa

- Sovrascrivere il lavoro dell'altro senza passare dal ciclo §5.
- Dichiarare letta una fonte non letta.
- Considerare una lezione completata perché è scritta.
- Spostare, rinominare o cancellare file canonici senza approvazione (D-07).
- Collegare il Brain a operatività reale.
