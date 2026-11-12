# Errata V3.3

**Data:** 12/11/2026 · **Autore:** Claude, per D-20 e D-22 («prima l'errata T-01…T-05, poi Q-09, poi il G0 minimo»)
**Oggetto:** pacchetto V3.3 di Gemini (ZIP `6fb9d76e…7638`; motore `prop_risk_engine_v3_3.py` `b20608ca…1a12`; suite `test_prop_risk_v3_3.py` `bb43b359…c0`)
**Principio:** V3.3 resta **congelata e intatta** (D-17). L'errata è un **addendum**: test aggiuntivi, uno script di mutazione e correzioni documentali scritte qui. Nessun file di V3.3 è stato modificato.

## Esito
Le riserve **T-01…T-05 sono chiuse** con l'evidenza seguente, che sottopongo all'accettazione dell'utente.

Risultato delle mutazioni (`output/esecuzione_errata.txt`): suite di Gemini più test dell'errata → **24/24 mutanti non equivalenti uccisi** (V02–V25). Sopravvive solo **V01**, che fa riusare alla fase 2 i generatori della fase 1. È quasi equivalente: cambia l'accoppiamento tra le fasi, non la distribuzione dei risultati. Lo è dalla V3.1 ed è documentato.

| Riserva | Risoluzione | Evidenza |
|---|---|---|
| **T-01** Analisi di mutazione riproducibile e V22 | Script `mutazioni_v3_3.py` (25 mutanti con definizioni pubblicate, verifica che il mutante sia effettivamente caricato); test deterministico `test_t01_v22_campionatore_deriva_piccola`: con μ = 0,05 deve valere F(m(u)) = u entro 10⁻¹², per 3 valori di R:R e 5 di u | V22 ucciso dall'errata |
| **T-02** Precisione dei valori esatti | Valori corretti, sotto | Ricalcolo con `c1_esatto_challenge.fase` (revisione V2 di Claude) |
| **T-03** Attribuzione nel README | Testo corretto, sotto | — |
| **T-04** Test mancanti per V16 e V24 | `test_t04_v16_configurazione_irraggiungibile` (WR 0,40, R:R 0,001 → `ValueError`); `test_t04_v24_deriva_negativa` (3 configurazioni con deriva negativa, \|P_win − WR\| < 10⁻¹² con formula indipendente) | V16 e V24 uccisi |
| **T-05** Dettagli documentali | Correzioni, sotto | — |

## T-02 · Valori esatti della sfida a due fasi (swing 1%, 60 giorni, WR 0,40, R:R 2, costo 0,05R)
| Grandezza | Valore dichiarato in V3.3 | Valore corretto |
|---|---|---|
| Fase 1 isolata | 0,780000 | **0,7799848** |
| Fase 2 isolata | 0,857200 | **0,8571715** |
| Sfida completa (prodotto) | 0,668616 | **0,6685807** |

Metodo: programmazione dinamica **in avanti** sul reticolo dell'equity (`c1_esatto_challenge.fase`), non «backward induction». Arrotondati a 4 cifre (0,7800 / 0,8572 / 0,6686), i valori usati nei test V3.3 restano corretti.

## T-03 · Attribuzione
`README.md`, riga 4, va letto così: «Proposte di correzione: Claude Code (revisione V3.2). Revisione indipendente della V3.3: Claude Code, `CLAUDE_FINAL_REVIEW_V3_3.md`, esito: validata con riserve; errata: `ERRATA-V3_3/`».

## T-05 · Dettagli documentali
1. `V3_3_MATHEMATICAL_VERIFICATION.md` §3.1: l'espressione corretta per deriva nulla, stop a −1 e target a +b è **F(d) = b·(1 − d)/(b + d)**; con b = 1 si ottiene (1 − d)/(1 + d).
2. Stesso documento, §5, e motore riga 145: la ricerca della deriva positiva si ferma a **μ = 15** (`high = min(15.0, 345.0)`, riga 149), non a 345 né a 350. Win rate che richiedono μ > 15 (oltre 1 − e⁻³⁰ circa) sono rifiutati con `ValueError`.
3. `archivio_storico/LEGGIMI_V1.md`: i percorsi assoluti del Mac vanno letti come relativi alla cartella del pacchetto; l'import del runner V1 è un blocco su più righe (righe 13–16).
4. `V3_3_MANIFEST.sha256` è un duplicato di `MANIFEST_SHA256_V3_3.txt`, fuori dal manifest: va ignorato.

## Difetti aggiuntivi dalla revisione esterna (ChatGPT)
- **R-16 · Wilson con zero osservazioni.** `wilson_confidence_interval(0, 0)` restituisce `(0.0, 0.0)`, che si può leggere come certezza che la probabilità sia zero. Il codice congelato non si corregge.
  - Il test `test_r16_wilson_zero_osservazioni` documenta il comportamento corretto (`ValueError` o stato NON STIMABILE) ed è marcato «fallimento atteso».
  - **Il codice nuovo (G0) non riusa questa funzione così com'è.**
- **R-17 · Nome fuorviante.** `calculate_kelly_confidence_interval` non calcola una frazione di Kelly: calcola E[R], il suo errore standard e un intervallo normale (Wald), con payoff fisso. Nel codice nuovo si chiamerà per ciò che fa (intervallo dell'aspettativa).

## Come rieseguire
```bash
PYTHONPATH=<cartella con prop_risk_engine_v3_3.py> python3 -s -B test_errata_v3_3.py -v
```
```bash
python3 -s -B mutazioni_v3_3.py <prop_risk_engine_v3_3.py> <test_prop_risk_v3_3.py> test_errata_v3_3.py <cartella vuota>
```
Tempo indicativo: circa 45 secondi.

## Limiti
- I mutanti sono 25, scelti a mano: un kill rate del 100% su di essi non dimostra l'assenza di altri difetti.
- La revisione esterna non ha potuto riprodurre la suite V3.3 perché non era nel pacchetto. Questa cartella contiene i test dell'errata, mentre la suite di Gemini resta nel pacchetto V3.3, da archiviare nel nuovo repository (D-19).
