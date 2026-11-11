# Standard del Brain

Versione 1.0 · 11/11/2026. Regole che valgono per ogni file del Brain.

## 1. Gerarchia delle fonti

| Rango | Tipo | Esempi | Uso |
|---|---|---|---|
| F1 | Paper peer-reviewed originale | Journal of Finance, RFS, JFE, JME, AER | Base per affermazioni empiriche |
| F2 | Manuale universitario / testo specialistico riconosciuto | Hull, Campbell-Lo-MacKinlay, Hasbrouck | Definizioni, teoria, metodi |
| F3 | Istituzione ufficiale | Fed, BCE, BIS, IMF, ESMA, CONSOB, Agenzia Entrate | Fatti istituzionali, norme, dati |
| F4 | Documentazione tecnica di exchange, broker, data provider | CME, Cboe, Eurex | Specifiche di contratto, metodologie |
| F5 | Ricerca di istituzioni finanziarie | AQR, banche, asset manager | Utile, ma con possibile conflitto d'interesse |
| F6 | Corsi universitari, curricula professionali | MIT OCW, CFA, FRM | Copertura e ordine didattico |
| F7 | Divulgazione qualificata | blog accademici, libri divulgativi | Solo di supporto, mai unica fonte |

Le community di trading, i forum e i video promozionali **non sono fonti**: possono essere *oggetto* di studio (cosa si afferma) ma non *prova* (cosa è vero).

## 2. Livelli di evidenza (da indicare accanto alle affermazioni importanti)

| Codice | Significato |
|---|---|
| **E1** Consenso | Accettato dalla letteratura, replicato molte volte |
| **E2** Replicato | Replicato in più campioni o mercati, con dibattito sui dettagli |
| **E3** Preliminare | Pochi studi, campioni limitati, non ancora replicato |
| **E4** Teorico | Conseguenza di un modello, non (ancora) misurata in modo diretto |
| **E5** Opinione professionale | Pratica diffusa tra professionisti, senza prova sistematica |
| **E6** Interpretazione discrezionale | Lettura soggettiva (es. "assorbimento" su un footprint) |
| **E7** Promozionale / non dimostrato | Affermazione senza prova o con incentivo a venderla |

## 3. Stato di verifica di una fonte (nella bibliografia e nel registro)

- **V** — consultata in questa base: almeno abstract o pagina ufficiale letti, con data.
- **V-sec** — confermata solo tramite fonti secondarie o snippet (il testo originale non è stato letto).
- **C** — citata dalla conoscenza dell'autore, **non riletta**: da verificare prima di usarla come prova.
- **X** — tentativo di verifica fallito o fonte non trovata.

Non si dichiara mai **V** per una fonte non letta.

## 4. Modello di lezione (20 sezioni)

1. Titolo · 2. Obiettivi di apprendimento (con livello L1–L5) · 3. Prerequisiti (link) · 4. Definizione ·
5. Spiegazione approfondita · 6. Fondamenti teorici · 7. Formule · 8. Esempi numerici ·
9. Esempi reali e casi storici · 10. Applicazione ai mercati · 11. Connessioni con altre discipline (link) ·
12. Errori comuni · 13. Limiti e controversie · 14. Evidenze scientifiche (con E1–E7) · 15. Fonti (con V/C) ·
16. Sintesi da ricordare · 17. Flashcard · 18. Esercizi · 19. Domande di ragionamento · 20. Checklist di padronanza.

Ogni lezione ha un'intestazione con: `id`, versione, data, stato (`bozza` / `verificata` / `da aggiornare`), data di prossima revisione per i contenuti che invecchiano (tassi, norme, fiscalità).

Le convenzioni grafiche del v1 restano valide: **Definizione · Esempio · Errori tipici · Sintesi · Oltre il vault**.

## 5. I cinque livelli di padronanza

| Livello | Cosa sa fare | Come si verifica |
|---|---|---|
| L1 Conoscenza | Definisce e descrive | Flashcard |
| L2 Comprensione | Spiega il meccanismo | Spiegazione a voce senza note |
| L3 Applicazione | Usa il concetto su dati reali | Esercizi numerici, analisi di grafici e dati |
| L4 Analisi critica | Trova limiti, errori, alternative | Revisione avversariale, confronto tra ipotesi |
| L5 Integrazione e ricerca | Collega discipline, formula e progetta test | Mini-progetto di ricerca pre-registrato |

Un modulo è "superato" solo quando il suo **cancello** (che richiede almeno L3, e L4 dal Modulo 3 in poi) è passato. Il passaggio si registra nel REGISTRO-CONOSCENZE con data.

## 6. Regole di sicurezza e di rigore

- Nessuna promessa di rendimento, nessuna strategia presentata come sicura, nessun incoraggiamento alla leva.
- Un backtest non è una garanzia; una simulazione non autorizza a rischiare denaro reale.
- Non si inventano dati, citazioni, autori, link. Se una fonte non è stata letta, lo si dichiara.
- Non si nascondono risultati negativi: vanno nel registro come i positivi.
- Correlazione ≠ causalità: ogni catena causale indica il livello di evidenza di **ogni anello**.
- Nessuna automazione di ordini reali senza autorizzazione esplicita, scritta, e un piano di rischio approvato.
- Contenuti fiscali e normativi: sempre **giurisdizione + data + fonte ufficiale**, e il limite "non è consulenza".
- Quattro ambienti separati: **studio → ricerca offline → simulazione/paper → reale**. Il passaggio da uno all'altro richiede un cancello esplicito (Modulo 9).

## 7. Distinguere ciò che si sa da ciò che si deduce

Nei testi si usano tre marcatori:
- *Documentato:* segue una fonte.
- *Deduzione:* ragionamento dell'autore a partire da fonti, senza prova diretta.
- *Ipotesi testabile:* formulata in modo da poter essere confutata, con i dati che servirebbero.

## 8. Classi di contenuto (da tenere sempre separate)

Introdotte il 11/11/2026 su decisione dell'utente (D-05 in `DECISIONI.md`).

| Classe | Etichetta nel testo | Che cosa significa | Dove vive |
|---|---|---|---|
| Verificato | `[VERIFICATO]` | Affermazione con fonte letta (stato V) o calcolo ricontrollato da un secondo controllo | Lezioni con stato `verificata` |
| In verifica | `[IN VERIFICA]` | Fonte confermata solo indirettamente (V-sec) o non ancora letta (C), oppure esempio non ancora ricontrollato | Lezioni `bozza` / `in_verifica` |
| Ipotesi | `[IPOTESI]` | Deduzione o congettura formulata in modo testabile | Lezioni (riquadro "Ipotesi") e `glossario/DOMANDE-APERTE.md` |
| Esercitazione | `[ESERCIZIO]` / `[ESEMPIO]` | Numeri costruiti a mano per insegnare: non descrivono il mercato | Sezioni 8 e 18 delle lezioni |
| Dato simulato | `[SIMULATO]` | Prodotto da un generatore con seme dichiarato | `dati/simulati/`, output degli script |
| Dato reale | `[REALE]` | Osservazione di mercato o economica con fonte, data e hash | `dati/reali/`, `dati/derivati/` |

Regola: nelle sezioni 8 (esempi numerici) e 9 (casi reali) di ogni lezione, ogni numero porta una di queste etichette. Le lezioni scritte prima di questa regola (L2.1–L2.3) usano già "Esempio" e "Stato V/V-sec/C": vanno allineate alla prima revisione.

## 9. Ciclo di vita di una lezione

```
bozza ──► in_verifica ──► verificata ──► (da_aggiornare) ──► verificata
                │
                └── padronanza dell'utente: separata, registrata solo col cancello superato
```

| Stato | Condizione per entrarci |
|---|---|
| `bozza` | Struttura a 20 sezioni presente, ancora incompleta o non riletta |
| `in_verifica` | Completa; fonti con stato dichiarato; restano fonti C/V-sec o esempi non ricontrollati |
| `verificata` | Tutte le fonti usate come prova sono V; esempi ricalcolati da script o da un secondo revisore (Claude o Gemini, non l'autore) |
| `da_aggiornare` | Data `revisione_entro` superata o fonte superata |

**Una lezione non è "completata" perché è scritta.** È completa per il Brain quando è `verificata`; è acquisita dall'utente solo quando il cancello è superato.

## 10. Sorgente e versione generata

I file Markdown in `brain/` sono la **fonte primaria** della conoscenza. Il manuale HTML (stile v1) sarà **generato** da questi file con uno script e non si modificherà mai a mano (decisione D-03). Il v1 originale resta in `originale/` come documento storico.
