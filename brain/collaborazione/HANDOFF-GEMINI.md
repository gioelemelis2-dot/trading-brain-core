# Documento di consegna per Gemini

Versione 1.0 · 11/11/2026 · Autore: Claude · Destinatario: Gemini (Antigravity)
Da leggere per intero prima di qualsiasi attività. Le regole di lavoro sono in [`PROTOCOLLO-OPERATIVO.md`](PROTOCOLLO-OPERATIVO.md).

> **Avvertenza.** L'utente ha predisposto un *Master Mission* e un *Protocollo comune di collaborazione*. Nella sessione in cui Claude ha scritto questo documento **quei testi non erano disponibili**. Se li hai, prevalgono su questo documento: segnala all'utente ogni differenza nel tuo primo rapporto.

## 0. In una frase
Il Trading Brain è **una** base di conoscenza modulare, versionata e verificabile sui mercati finanziari, costruita a partire dal *Manuale del Brain v1* dell'utente. Claude ne cura lo sviluppo e la coerenza architetturale; a te chiediamo **ricerca indipendente, verifica e revisione critica**, con integrazione dopo un controllo di qualità. Non esiste un secondo Brain.

## 1. Dove si trova
| Elemento | Valore |
|---|---|
| Repository | GitHub `gioelemelis2-dot/l-Altro`, cartella `brain/` |
| Branch di lavoro di Claude | `claude/vibrant-cannon-5uunho` (non unito al branch principale di l-Altro) |
| Migrazione | È previsto lo spostamento in un repository autonomo ([`../piano/PIANO-MIGRAZIONE.md`](../piano/PIANO-MIGRAZIONE.md)), **non ancora approvato**. Tutti i percorsi in questo documento sono **relativi a `brain/`**: restano validi dopo la migrazione |
| Manuale originale | artifact `https://claude.ai/artifact/T4xESphh3BmonZPoprQBtb`; copia identica in `originale/manuale-v1.html` (sha256 `931685e6…6634`) + testo estratto `originale/manuale-v1.txt` |

L'utente deve concederti l'accesso in lettura al repository e, per consegnare i rapporti, la possibilità di aprire branch `gemini/<argomento>`.

## 2. Architettura attuale
- **Spina dorsale**: Moduli 0–9 (fondamenta → mercati → macro → tecnica → order flow → fondamentale → rischio → strategie → ricerca e automazione → operatività reale).
- **Modulo 10**: tracce specialistiche parallele (matematica, serie storiche, ML, derivati, fixed income, asset pricing e storia, psicologia, causalità e previsione, sistemi complessi), alcune obbligatorie prima di certi moduli.
- **Aree di conoscenza** A–S (richieste dall'utente) + T–Z (aggiunte: inferenza causale e forecasting, plumbing finanziario, storia delle crisi, asset pricing, fixed income avanzato, sistemi complessi, gestione della conoscenza).
- Dettagli: [`../architettura/ARCHITETTURA.md`](../architettura/ARCHITETTURA.md), [`../mappa/MAPPA-COMPETENZE.md`](../mappa/MAPPA-COMPETENZE.md), [`../mappa/DIPENDENZE.md`](../mappa/DIPENDENZE.md).

```
brain/
├── README.md, CONTINUITA.md        ← punto d'ingresso e stato esatto del lavoro
├── governance/                     ← STANDARD, DECISIONI, registri conoscenze e modifiche
├── audit/                          ← diagnosi del v1, verifica delle affermazioni, matrice lacune
├── mappa/  architettura/  piano/   ← competenze, dipendenze, moduli, roadmap, migrazione
├── bibliografia/                   ← 185 voci con stato di verifica
├── moduli/m02-macro/               ← lezioni L2.1–L2.6 + protocollo di analisi
├── strumenti/                      ← script Python riproducibili
├── dati/                           ← regole e richieste dati (reali / simulati separati)
├── glossario/                      ← glossario, domande aperte
├── collaborazione/                 ← questo documento, protocollo, LOCK, richieste, esiti, rapporti
└── originale/                      ← manuale v1, intoccabile
```

## 3. Lavoro completato

| Sprint | Contenuto | Stato |
|---|---|---|
| S1 | Governance; audit del v1 (verificate 18 citazioni e 11 calcoli: **2 errori**, 8 imprecisioni, tutti i numeri corretti); matrice delle lacune per 17 aree; mappa A–Z; catene causali con livelli di evidenza; architettura con corrispondenza v1 → v2; bibliografia; piano; lezioni L2.1–L2.3; protocollo di analisi di un movimento; 2 script | completato |
| S2 | Lezioni L2.4–L2.6; classi di contenuto e ciclo di vita delle lezioni; registro delle decisioni; piano di migrazione; specifica dei dati per la lezione 0.17 + script di riproduzione; questo materiale di collaborazione | completato |

**Nessuna lezione è `verificata`.** L2.1–L2.6 sono `in_verifica`: la maggior parte delle fonti è confermata solo tramite abstract o fonti secondarie (V-sec) o non ancora letta (C). È qui che il tuo contributo vale di più.

## 4. Decisioni prese
Registro completo: [`../governance/DECISIONI.md`](../governance/DECISIONI.md). Le essenziali:
- D-01 Architettura "spina 0–9 + tracce".
- D-02 Il Brain diventerà un progetto autonomo — **solo dopo approvazione** del piano.
- D-03 I Markdown sono la fonte primaria; l'HTML sarà generato.
- D-04 Mai sostituire dati mancanti con dati inventati o simulati non dichiarati.
- D-05 Separare sempre: verificato · in verifica · ipotesi · esercitazione · dato simulato · dato reale.
- D-06 Collaborazione sullo stesso Brain, integrazione dopo controllo di qualità, mai modifiche simultanee agli stessi file.
- D-07 Migrazioni e modifiche strutturali importanti solo con approvazione dell'utente.

## 5. Criteri di qualità
Sono gli stessi per entrambi: [`../governance/STANDARD.md`](../governance/STANDARD.md).
- Fonti F1–F7 (paper peer-reviewed → divulgazione), **stato** V / V-sec / C / X: *V solo se letta davvero*.
- Livelli di evidenza E1 (consenso) → E7 (promozionale).
- Classi di contenuto con etichette `[VERIFICATO]` `[IN VERIFICA]` `[IPOTESI]` `[ESERCIZIO]/[ESEMPIO]` `[SIMULATO]` `[REALE]`.
- Lezione a 20 sezioni; livelli di padronanza L1–L5; cancelli.
- Controllo di qualità Q1–Q8 prima di integrare qualsiasi contenuto: [`PROTOCOLLO-OPERATIVO.md`](PROTOCOLLO-OPERATIVO.md) §6.

## 6. File da consultare
| Priorità | File | Perché |
|---|---|---|
| 1 | `CONTINUITA.md`, questo documento, `collaborazione/PROTOCOLLO-OPERATIVO.md`, `collaborazione/LOCK.md` | Stato e regole |
| 1 | `governance/STANDARD.md`, `governance/DECISIONI.md` | Standard e decisioni |
| 2 | `audit/01-DIAGNOSI.md`, `audit/02-VERIFICA-AFFERMAZIONI.md`, `audit/03-MATRICE-LACUNE.md` | Che cosa è stato verificato e che cosa manca |
| 2 | `moduli/m02-macro/*` | Le lezioni da verificare |
| 2 | `bibliografia/BIBLIOGRAFIA.md` | Fonti e loro stato |
| 3 | `mappa/*`, `architettura/ARCHITETTURA.md`, `piano/*` | Per la revisione critica dell'impianto |
| 3 | `glossario/DOMANDE-APERTE.md`, `collaborazione/da-claude/RICHIESTE.md` | Domande aperte e richieste esplicite |
| 3 | `originale/manuale-v1.txt` | Il testo di partenza |
| — | `strumenti/*.py` | Ogni esempio numerico è riproducibile: `python3 strumenti/<nome>.py` (`riproduci_017.py --test`) |

## 7. Dove una verifica indipendente è particolarmente utile
In ordine di valore atteso:

| # | Attività | Perché proprio tu | Richiesta |
|---|---|---|---|
| 1 | **Verificare le lezioni L2.1–L2.6**: portare le fonti da V-sec/C a V, ricontrollare gli esempi, segnalare affermazioni sbagliate o sopravvalutate | Seconda lettura indipendente; nessuna lezione può diventare `verificata` senza un revisore diverso dall'autore | R-001 |
| 2 | **Seconda opinione sull'audit del v1** (soprattutto gli errori A7 McLean-Pontiff e A9 Novy-Marx/RMW, e le imprecisioni A4–A18) | Un errore nell'audit si propagherebbe nelle correzioni del v1 | R-002 |
| 3 | **Fiscalità italiana 2026** su fonti ufficiali (Agenzia delle Entrate, Gazzetta Ufficiale, MEF) | Alta probabilità di errori e di cambi normativi | R-003, Q7 |
| 4 | **Harvey-Liu-Zhu 2016**: esiste nel testo l'intervallo "27–53%"? | Verifica puntuale su testo integrale | R-004, Q5 |
| 5 | **Dati e cifre storiche** in verifica: Gagnon et al. (Q10), taper tantrum (Q11), acquisti Fed dicembre 2025 (Q12), note di implementazione 2026 (Q4) | Richiedono testi originali o serie ufficiali | Q4, Q10–Q12 |
| 6 | **Revisione critica di mappa e architettura**: aree mancanti, prerequisiti errati, duplicazioni, ordine didattico | Un secondo punto di vista sull'impianto | R-005 |
| 7 | **Bibliografia da C a V**, partendo dalle fonti citate nelle lezioni | Lavoro lungo e parallelizzabile | R-006 |
| 8 | **Controversie** già tracciate (effetto informativo delle banche centrali; entità della loss aversion; neuroscienze divulgative nel Modulo 0.4): stato attuale della letteratura | Ricerca bibliografica approfondita | — |
| 9 | Se il tuo ambiente può scaricare dati pubblici (es. FRED): **riproduzione indipendente** delle statistiche della lezione 0.17 calcolabili con le sole chiusure (S1–S3, S5–S7, S10), con fonte e data, etichettata `[REALE]` e dichiarata come **dataset diverso** da quello del vault | Qui la rete è bloccata; un dataset indipendente misura quanto i numeri dipendono dalla fonte | — |

## 8. Che cosa puoi fare senza sovrapporti al lavoro di Claude
- **Sì**: ricerche, verifiche, revisioni, proposte di testo, analisi su dati reali pubblici, controlli di calcolo, critiche all'architettura — tutto consegnato come rapporto in `collaborazione/da-gemini/`.
- **Sì, previo accordo** (riga in `LOCK.md` o richiesta in `da-claude/RICHIESTE.md`): bozze di nuove lezioni in aree che Claude non ha in corso, consegnate come rapporto di tipo "proposta" e poi integrate da Claude.
- **No**: modificare file fuori da `collaborazione/da-gemini/`; avviare lavori su attività riservate a Claude in `LOCK.md` (stesura del Modulo 2 da L2.7 in poi, traccia 10.1, generatore HTML) senza accordo; spostare o rinominare file; segnare fonti come V senza averle lette.

## 9. Come restituire i risultati
1. Crea il branch `gemini/<argomento>` dall'ultimo commit del branch di lavoro di Claude.
2. Scrivi un rapporto `collaborazione/da-gemini/G-AAAAMMGG-NN-argomento.md` secondo [`da-gemini/MODELLO-RAPPORTO.md`](da-gemini/MODELLO-RAPPORTO.md): hash del commit esaminato, metodo, tabella dei rilievi (esito ✅ ⚠️ ❌ ❓, evidenza, stato della fonte, proposta concreta), fonti **effettivamente lette**, limiti.
3. Pubblica il branch e avvisa l'utente.
4. Claude esegue il controllo di qualità, integra o motiva il rifiuto in `da-claude/ESITI.md` e cita il rapporto in `governance/REGISTRO-MODIFICHE.md`. I disaccordi vanno in `DISACCORDI.md` e li decide l'utente se le fonti non bastano.

## 10. Attività aperte (sintesi)
- Approvazione utente: piano di migrazione; conferma D-08 (le aggiunte non distruttive non sono "modifiche strutturali").
- Dati del vault per la lezione 0.17 ([`../dati/RICHIESTA-DATI-0.17.md`](../dati/RICHIESTA-DATI-0.17.md)).
- Testi del Master Mission e del Protocollo comune in `collaborazione/fondamenti/`.
- Roadmap di Claude: traccia 10.1 (statistica), generatore HTML, correzioni del v1, unità 2.2–2.3, lab event study (bloccato in attesa di dati reali).
