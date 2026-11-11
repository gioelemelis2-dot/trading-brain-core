# 05 · Proposta di architettura: Strategy Discovery Lab e Trading Guardian

Audit AUDIT-ARCH-20261111 · **PROPOSTA, non implementata.** Richiede l'approvazione dell'utente (D-07) prima di qualsiasi codice o modifica dell'architettura del Brain.

> **Premessa sul Trading Guardian.** Il termine non compare in nessun documento del Brain né nei materiali di Gemini che ho ricevuto. Quella che segue è la **mia ipotesi di funzione**, ricavata dalle regole del v1 (0.7, 0.8, 0.21: aderenza, regole non negoziabili, kill switch, tilt) e dal lavoro sulle prop firm. Se il Master Mission o Antigravity ne danno un'altra definizione, prevale quella e questa proposta va riallineata.

---

## 1. Dove si collocano nel Brain

Oggi l'architettura è solo didattica (Moduli 0–9 + tracce 10.x). Propongo **uno strato separato**, senza toccare i moduli:

```
brain/
├── moduli/ …            ← formazione (invariata)
├── laboratori/          ← PROPOSTA: sistemi di ricerca e controllo
│   ├── discovery-lab/   ← Strategy Discovery Lab
│   ├── guardian/        ← Trading Guardian
│   └── comuni/          ← componenti condivise (motore di rischio, calcolo esatto, rulebook, dati)
└── …
```

Motivo: i sistemi software hanno un ciclo di vita diverso dalle lezioni (versioni, test, rilasci) e non devono mescolarsi ai contenuti formativi. Ogni sistema rimanda alle lezioni che ne spiegano i principi (Modulo 6 rischio, Modulo 8 ricerca, Modulo 9 operatività).

**Questa è una modifica strutturale:** serve l'approvazione dell'utente, ed è da coordinare con la migrazione sospesa (D-02).

---

## 2. Strategy Discovery Lab

### 2.1 Scopo
Trasformare un'idea in un risultato **verificabile o confutato**, contando ogni prova e separando nettamente esplorazione e validazione. Il Lab non produce strategie "pronte": produce **ipotesi con un esito documentato**, positivo o negativo.

### 2.2 Ciclo di vita di un'ipotesi
```
idea ──► ipotesi registrata ──► esplorazione (in campione) ──► validazione (fuori campione, una volta sola)
                                                                     │
                     ┌───────────────────────────────────────────────┼──────────────────────┐
                 confutata                                    non conclusiva            validata
             (archiviata, resta nel registro)            (dati o potenza insufficienti)      │
                                                                                   revisione incrociata Claude–Gemini
                                                                                             │
                                                                                     paper trading (Guardian attivo)
                                                                                             │
                                                                   operatività reale SOLO con autorizzazione scritta dell'utente
```

### 2.3 Componenti
| # | Componente | Funzione | Regole di qualità | Riuso dell'esistente |
|---|---|---|---|---|
| 1 | **Registro delle ipotesi** | Una scheda per ipotesi: ragione economica, dati, regole, parametri ammessi (griglia dichiarata), metriche, criterio di successo, criterio di abbandono, data di registrazione | Immutabile dopo la registrazione; le modifiche creano una nuova versione | v1 0.3 (5 domande), 0.4 (protocollo) |
| 2 | **Strato dati** | Grezzi (immutabili, con hash) → validati (controlli) → viste point-in-time | Metadati obbligatori; licenza dichiarata; nessun dato simulato senza etichetta | `dati/README.md`; controlli di `riproduci_017.py` |
| 3 | **Libreria di segnali** | Funzioni pure che usano solo dati disponibili al momento della decisione | Test automatico contro il look-ahead (spostando i dati futuri il segnale non deve cambiare) | — |
| 4 | **Modello di esecuzione** | Riempimenti (stop, limite, gap oltre il livello, tocco intraday), costi, slippage, finanziamento, sessioni | Separato dalla logica della strategia; parametri giustificati da dati o dichiarati come ipotesi | Contestazione C-15; seconda revisione §5.C |
| 5 | **Motore di backtest** | Motore di riferimento a eventi, lento ma semplice; eventuale motore veloce validato contro il riferimento | Casi di prova con soluzione esatta; test di mutazione | Metodo della seconda revisione (calcolo esatto, mutazioni) |
| 6 | **Suite di validazione** | Fuori campione bloccato, walk-forward, CPCV con purging, DSR, PBO, Reality Check/SPA, bootstrap a blocchi | **Contatore delle prove**: ogni esecuzione conta nella correzione per test multipli | v1 0.18; bibliografia M |
| 7 | **Registro dei risultati** | Ogni esecuzione: hash di codice, dati e parametri, esito, anche negativo | Nessun risultato senza riga di registro | Manifest SHA-256 già in uso |
| 8 | **Revisione** | Ogni ipotesi "validata" passa la checklist di revisione e la revisione dell'altro sistema | Integrazione solo dopo il controllo di qualità | `CHECKLIST-REVISIONE.md`, protocollo |

### 2.4 Ripartizione Claude / Gemini (proposta)
| Parte | Gemini | Claude |
|---|---|---|
| Codice del motore, dello strato dati e del modello di esecuzione | sviluppa | revisiona; scrive i casi di prova con soluzione esatta |
| Registro delle ipotesi, protocollo, suite di validazione (metodo) | revisiona | specifica e scrive le lezioni |
| Ogni ipotesi | chi la propone la registra | l'altro la revisiona prima della validazione |

### 2.5 Che cosa il Lab non fa
- Non ottimizza senza contare le prove.
- Non usa il fuori campione più di una volta.
- Non promuove una strategia a operatività reale.
- Non presenta come "verificato" un risultato su dati simulati.

---

## 3. Trading Guardian (ipotesi di funzione)

### 3.1 Scopo
Proteggere **capitale e processo** dell'operatore, discrezionale o sistematico, facendo rispettare regole scritte prima dell'operatività. **Non genera segnali e non opera da solo.**

### 3.2 Livelli di intervento (si sale solo con autorizzazione esplicita)
| Livello | Che cosa fa | Requisiti |
|---|---|---|
| **G0 · Consultivo** | Calcola lo stato di rischio, avvisa, registra; non blocca nulla | Rulebook verificato; inserimento manuale o export dei dati del conto |
| **G1 · Vincolante in paper** | Blocca gli ordini simulati che violano le regole | G0 stabile; test per ogni regola |
| **G2 · Vincolante sul conto reale** | Blocca o chiude ordini reali tramite API del broker | Autorizzazione scritta dell'utente; verifica dei termini del broker o della prop firm; procedura di emergenza |

### 3.3 Componenti
| # | Componente | Funzione | Riuso |
|---|---|---|---|
| 1 | **Rulebook versionato** (YAML con schema) | Regole del conto (prop firm o broker) e regole personali; per ciascuna: fonte, data, tipo di conto, test | Rulebook di Gemini (da consegnare e verificare); checklist C1–C7; v1 0.8 |
| 2 | **Motore dello stato di rischio** | Saldo, equity, pavimento giornaliero (con orario di reset), max loss, esposizione, posizioni correlate | Motore V2 dopo le correzioni C-01…C-04 |
| 3 | **Proiezione del rischio** | Data la situazione attuale e la size prevista: probabilità di violare il limite giornaliero o il max loss, quante perdite consecutive restano | Calcolo esatto (`c1`/`riferimento_rovina`), con parametri dichiarati |
| 4 | **Controllo pre-trade** | Checklist del v1 0.8: setup del playbook, stop definito, size entro il budget, nessuna condizione proibita (notizie, stanchezza, tilt) | v1 0.8, 0.21, 0.22 |
| 5 | **Monitor e allarmi** | Soglie di avviso prima delle soglie di violazione | — |
| 6 | **Kill switch** | G0: invito a fermarsi e blocco della sessione nel journal · G1/G2: blocco effettivo | v1 0.8 regola 5 |
| 7 | **Journal e aderenza** | Registrazione di ogni trade con voto di aderenza, stato emotivo, ore di sonno; statistiche aderenza/risultato | v1 0.7, 0.19, 0.22 |
| 8 | **Rapporti** | Riepilogo giornaliero e settimanale; nessuna promessa di rendimento | Modulo 9.6 |

### 3.4 Che cosa il Guardian non fa
- Non decide trade.
- Non aumenta il rischio.
- Non opera sul conto reale senza autorizzazione esplicita.
- Non sostituisce le regole del broker o della prop firm: le **anticipa**.

---

## 4. Componenti comuni e archivio delle consegne
| Componente | Proposta |
|---|---|
| Motore di rischio | Una sola versione canonica (oggi: V2 di Gemini + calcolo esatto di Claude, duplicato D-01), con suite di test comune (test di Gemini + gruppo A/B di Claude) |
| Rulebook | Un solo file per tipo di conto, con le fonti ufficiali |
| Archivio delle consegne di Gemini | Cartella dedicata, intoccabile, con i file congelati e il loro manifest (oggi i materiali V2 non sono archiviati: rischio di perdita, I-08) |
| Esecutore dei test | Un comando unico che esegue tutti i test degli strumenti e ne registra l'esito |

---

## 5. Decisioni richieste all'utente
1. Confermare o correggere la **funzione del Trading Guardian** (§3) e il suo nome.
2. Approvare lo **strato `laboratori/`** (modifica strutturale) o indicare un'alternativa.
3. Decidere **dove archiviare le consegne di Gemini** (nel Brain, nel repository dedicato alle consegne, o altrove).
4. Autorizzare, quando opportuno, l'accesso a **dati reali** (abilitazione di rete per i provider, oppure file forniti dall'utente).
5. Confermare la **ripartizione Claude/Gemini** del §2.4.
