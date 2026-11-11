# Proposte di correzione per la V3 (da eseguire da Antigravity, dopo l'approvazione dell'utente)

Riferimento: `CLAUDE_FINAL_REVIEW_V3.md`. **Nessuna proposta è stata applicata.** La V3 consegnata resta congelata; le correzioni andrebbero in una V3.1 separata, con un nuovo manifest.

| # | Problema | Proposta | Test che dimostra la correzione |
|---|---|---|---|
| P-01 | N-01 CRN non accoppiati tra sfide | In `run_full_challenge_v3`, creare i tre generatori **per ogni sfida** da un seed derivato (es. `seed * 10**6 + i` più offset per MAE e slippage), oppure pre-generare le sequenze per sfida | Confronto base/MAE sullo stesso seed: **zero** sfide che passano solo con il MAE (oggi 2.275 su 10.000) |
| P-02 | N-02 MAE con parametri fissi | Calcolare μ dallo scenario (risolvere P(+R:R prima di −1) = win_rate) e passare le barriere reali al campionatore; in alternativa sollevare `ValueError` se `use_brownian_mae` è usato con WR ≠ 0,40 o R:R ≠ 2 | WR 0,50 / R:R 1: P(MAE ≤ −0,5R \| vincita) campionata ≈ 0,333 |
| P-03 | N-03 documentazione | Correggere Var[R] (2,16) e f* (0,4636%) in risposta e checkpoint; dichiarare la convenzione dello z (test score); separare i numeri di Claude da quelli della V3 | Numeri dei documenti uguali all'uscita di `verify_claude_17_points.py` |
| P-04 | N-04 attribuzione | Intestazione del motore: "Autore: Gemini Antigravity. Revisione indipendente: Claude (CLAUDE_FINAL_REVIEW_V3.md)" | Lettura |
| P-05 | N-05 ordine di classificazione | Stesso ordine (max loss, poi daily loss) nei due controlli, o dichiarare la regola | Caso costruito con violazione simultanea |
| P-06 | N-06 test | Integrare i test di concordanza con il calcolo esatto (gruppo A di Claude), un test di accoppiamento tra sfide e un test MAE con scenario diverso; rieseguire i test di mutazione | Suite che uccide i mutanti non equivalenti, adattati al codice V3 |
| P-07 | N-07 manifest | Includere checkpoint e README nel manifest | `sha256sum -c` su tutti i file consegnati |
| P-08 | C-13 ipotesi | Scrivere nei metadati del JSON e nelle uscite: edge supposto, i.i.d. o Markov, parametri di MAE e slippage dichiarati illustrativi, regole e loro fonte | Metadati presenti |
| P-09 | N-09 raccomandazione | Riformulare "0,25–0,45%" come euristica condizionata all'edge supposto, con la sensibilità all'incertezza dell'edge e allo slippage | Testo con etichetta `[EDGE SUPPOSTO]` |
| P-10 | C-11, C-15, C-17 materiali | Consegnare motore V1, rulebook YAML, schede STR-001/002, con manifest | File consegnati e verificabili |
| P-11 | N-08 governance | Fornire all'utente il testo del Master Mission citato (§0–§25), da inserire in `collaborazione/fondamenti/` | Testo presente nel Brain |
