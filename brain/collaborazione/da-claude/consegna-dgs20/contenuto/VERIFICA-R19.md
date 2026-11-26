# Verifica di Claude del giro R19 di Gemini · 26/11/2026

**Che cosa è stato verificato:** il rapporto di Gemini `G-20261126-R19.md`, sul candidato `1431190`, consegnato sul ramo `rev/gemini-r19` (`c3c434d`), letto per intero. I rilievi sono stati **riprodotti** rieseguendo lo script di Gemini (`r19_sonde_manomissioni_d51.py`) su due copie del codice, con rete bloccata e Python 3.13.18:
1. il candidato `7191156`: script invariato; log `log/sonde_gemini_su_7191156_py313.log`, 131 righe;
2. il codice attuale `94b9c92`, con i punti 4, 8 e 9 dell'ultimo lotto: script adattato **solo** nelle due chiamate a `rilascia`, che oggi richiedono autore e motivo; differenza in `log/adattamento_script_per_94b9c92.diff`; log `log/sonde_gemini_su_94b9c92_py313.log`, 131 righe.

**Confronto delle due corse:** identiche riga per riga dopo aver tolto percorsi temporanei e impronte, tranne CONC-2 (r.32). Lì cambia quale dei due processi in gara vince; l'esito è lo stesso: una sola apertura, il secondo processo fermato con «esito di 'P1' già registrato». Comando del confronto: `diff` dei due log normalizzati con `sed` su `/tmp/…` e sulle stringhe esadecimali.

**Come leggere la tabella:** «r.N» è la riga del log sul candidato che prova l'esito. Le scritte dello script non bastano: si legge il dato. Tre scritte non corrispondono al dato e sono segnalate sotto.

## Rilievi, una scheda per difetto (D-56)

| R19 | Registro | Esito su `7191156` e su `94b9c92` | Prova | Caso concreto → atteso / osservato | Conseguenza (D-56) | Proposta |
|---|---|---|---|---|---|---|
| 01 | **#142** | **chiuso** | r.6: dal lanciatore `rc=0`, «completata / promossa»; r.9: manomissione del lanciatore RILEVATA | verifica valida dal lanciatore → attesa completata / osservata completata | — | Gravità: Gemini propone «critico», Claude aveva scritto «importante». **Claude concorda con «critico»:** un lanciatore non sigillato rendeva inutile il controllo del sigillo |
| 02 | **#143** | riprodotto | r.11: `codice_manomesso_eseguito=True` | `--scheda esca-H002 --scheda vera` con `esegui_verifica.py` manomesso → atteso FERMO prima degli import / osservato codice eseguito. Inoltre `--scheda=PATH` → `manca --scheda` (r.10) | Codice non sigillato eseguito prima di ogni controllo: autorizzazione e consumo non più garantiti | **critico, bloccante** |
| 03 | **#144** | riprodotto | r.16: «promossa», 980 trade invece di 1.000 | 20 feriali vuoti, coerenti con il registro → atteso «non decidibile» o seduta mancante / osservato contati come sedute senza operazioni | Il verdetto cambia: dati mancanti confusi con K = 0 (DGS-17) | **importante, bloccante** |
| 04 | **#145** | riprodotto | r.20: con α 0,75 e m 5, «completata / promossa», con letture | Seconda verifica della stessa ipotesi e variante su un ramo divergente con lo stesso j → attesa rifiutata / osservata completata | Doppio consumo, seconda lettura della riserva. Cause: la storia del registro delle prove viene scartata, e l'α totale del registro della riserva è alterabile | **importante, bloccante** |
| 05 | **#140** | **chiuso** | r.17: i ruoli sono `['sviluppo', 'verifica', 'esito']` | caduta fra i due registri → attesi tutti e tre / osservati tutti e tre | — | Già corretto in `b9ec2f4` |
| 06 | **#146** | riprodotto | r.21–26 | (a) controllo del fuso assente; (b) ambiente controllato una volta sola, non prima dell'esito né alla ripresa; (c) `--ora` non validato (r.24: «NON-UNA-DATA» scritto); (d) soglia del veto −∞ accettata, poi fallisce tardi dopo aver letto lo sviluppo e scritto una voce (r.22); (e) ipotesi vuota accettata | (b) protezione #61 persa; (c) registri non riconciliabili nel tempo; (d) registro scritto da un contratto invalido; (e) identità vuota | **importante, bloccante** (b–e). Per (a) l'**impatto è incerto: giudizio aperto** (D-56), da misurare |
| 07 | **#147** | riprodotto | r.27: anomalie `[]` con URL falso; r.28: 1.489 giorni bruciati con `sha256=""` | indirizzo con dominio o data falsi; impronta vuota su «dati» → attesa anomalia prima dell'autorizzazione / osservata nessuna | Identità dei dati non garantita; consumo della riserva per un errore rilevabile prima | Gemini: «media». **Claude: importante, bloccante.** La scala del registro non ha «media»; il dissenso è solo sull'etichetta, non sul blocco |
| 08 | **#148** | riprodotto | r.24: riserva consumata 1.489 giorni, poi `IsADirectoryError` | `--rapporto` che è una cartella → atteso rifiuto prima dell'autorizzazione / osservato consumo | Consumo per un errore rilevabile prima (regressione di R11-S4) | Gemini: «media». **Claude: importante, bloccante** |
| 09 | **#149** | riprodotto | r.18: `RV.quota(0.15, 2, 1) = 0.024999999999999998`, diverso da 0,025 | quota uguale in aritmetica esatta → attesa ammessa / osservata «rifiutata per quota», durevole | Falso rifiuto. **Non si raggiunge con D-38:** con α 0,05, j 1, m 1 la quota è esattamente 0,025 (calcolo nel registro delle modifiche v2.12); solo con α alterato | Gemini: «media». **Claude: minore, latente; si corregge nel lotto** (confronto esatto in frazioni) |

## Scritte dello script che non corrispondono al dato (da segnalare a Gemini)
1. **r.17:** «(manca 'esito'!)» è stampato sempre (riga 282 dello script), ma il dato contiene 'esito'.
2. **r.19:** «BYPASS §3.4!» con α 0,15, ma l'esito osservato è «rifiutata per quota». Lì R19-09 ferma la seconda verifica, per caso.
3. **Sezione 6, «file extra non nel registro»:** segnato «NON RILEVATO!», ma Gemini stesso nel rapporto lo classifica come comportamento previsto. Il manifesto legge solo il registro; il caricatore solo le date attese.

## Che cosa regge di R19
- L'esito «non pulito» è corretto.
- **7 rilievi su 9 sono riprodotti** sul codice attuale; gli altri 2 sono già chiusi (#140, #142).
- Superati sul candidato e sul codice attuale (r.31–40):
  - concorrenza reale con due processi (CONC-1, 2, 3);
  - sonde #124 **D1, D2, D3, D6a, D6b**. Correzione da DGS-20: lo script non esegue D4 e D5 [VERIFICATO: righe 35–40 dei log e sezione 4 dello script], quindi la serie completa D1–D6 su questi commit non è attestata qui.
- Tutte le protezioni della matrice D-51 sono superate, tranne R19-04.
- I mutanti di Gemini su `1431190` (Apple Python 3.9.6) coincidono con quelli di Claude su quel candidato. N63 è equivalente di piattaforma (#106).

## Conseguenza per il percorso
- R19 non avanza il contatore. Per D-56 non avrebbe comunque contato: il perimetro non era congelato.
- I sei difetti aperti (#143–#148) e #149 entrano nell'**ultimo lotto**, come requisiti 12–18 di `piano/REQUISITI-ULTIMO-LOTTO.md`.
- Il prossimo giro di Gemini sarà sul candidato congelato dopo il lotto: è il primo dei due che contano.
