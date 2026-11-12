# Affermazioni di Gemini a confronto con i risultati di Claude (V3.2)

**Legenda:**
- **Confermata:** riprodotta.
- **Confermata con precisazione:** riprodotta, ma la formulazione va corretta.
- **Non confermata:** il mio risultato è diverso.
- **Non verificabile:** non controllabile da questo ambiente.

| # | Affermazione di Gemini | Dove | Risultato di Claude | Esito |
|---|---|---|---|---|
| 1 | SHA-256 dello ZIP `989dd288…3d18` | continuità §1 | coincide | Confermata |
| 2 | ZIP di 41.696 byte | continuità, riga 16 | 47.977 byte | Non confermata (S-08) |
| 3 | Manifest 15/15 OK | continuità §1 | 15/15 OK, nessun file non dichiarato | Confermata |
| 4 | File storici intatti, con gli hash originari | registro §1; continuità | identici byte per byte all'archivio V3.1 | Confermata |
| 5 | V2, V3 e V3.1 congelate e intatte nelle rispettive cartelle | checkpoint §1 | copie ricevute intatte; cartelle sul Mac inaccessibili | Non verificabile (copie ricevute: confermata) |
| 6 | 14/14 test superati | continuità §2 | 14/14 OK | Confermata |
| 7 | JSON prodotto dal runner | README; checkpoint §3 | identico byte per byte | Confermata |
| 8 | ±1 SE [+0,0651; +0,2349]; IC 95% [−0,0163; +0,3163]; f* [0,20%; 0,73%] | risposta §2.1 | [+0,0651; +0,2349]; [−0,0163; +0,3163]; [0,201%; 0,726%] | Confermata |
| 9 | Edge non distinguibile da zero al 95%; nessuna size giustificata dal campione | risposta §2.1; JSON | corretto | Confermata |
| 10 | Mutanti V02–V12 uccisi; «11/12, V01 quasi equivalente» | continuità §2; risposta §4 | V02–V12 11/11; V01 sopravvive | Confermata |
| 11 | Test R:R 1 «uccide V03 e V10» | test riga 298; risposta §2.2 | uccide V03; non può rilevare V10 (identico per costruzione). V10 è ucciso dal test delle barriere | Non confermata per V10 (S-02) |
| 12 | Test della fase 2 «uccide V07» | test riga 328; risposta §2.2 | non attraversa `run_full_challenge_v3_2`; V07 è ucciso solo dal Gruppo A | Non confermata (S-02) |
| 13 | Test R:R 1: z = 0,13 | risposta §2.2 | z = −0,13 | Confermata |
| 14 | Gruppo A: valori esatti 0,9108 / 0,7034 / 0,6686 / 0,4406 / 0,3884 | test righe 357–361 | coincidono con il calcolo esatto | Confermata |
| 15 | Gruppo A: «tutti \|z\| ≤ 1,46» | checkpoint, riga 33 | \|z\| massimo 1,67 (Markov) | Non confermata (S-08) |
| 16 | Fase 2 «benchmark analitico» ≈ 85,96%; fase 1 ≈ 77,60% | risposta, riga 65; test righe 332 e 349 | esatti 0,8572 e 0,7800; i valori dichiarati sono simulati | Non confermata (S-01) |
| 17 | F(0,5) = 1/3 e P(daily loss) = 1/6 per WR 0,50 e R:R 1 | test | 0,333333 e 0,166667 | Confermata |
| 18 | E[S] 0,0602; Var[S] 0,0222; E[R netto] 0,1139; Var[R] 2,2609; f* 0,3363% | risposta §2.3; JSON | 0,060169 / 0,022249 / 0,113899 / 2,260861 / 0,3363% | Confermata |
| 19 | Momenti ottenuti per «integrazione esatta» di P(S > s) | risposta §2.3 | equivalente alla forma chiusa | Confermata |
| 20 | Effetto del MAE: simulato −2,39 / +2,57 / −0,17; esatto −2,42 / +2,58 / −0,12; swing −1,53 | risposta §2.4; JSON | coincide | Confermata |
| 21 | Benchmark del MAE «analitici esatti in forma chiusa» | risposta, riga 87; checkpoint, riga 39 | esatti, ma numerici (programmazione dinamica con F(d) in forma chiusa) | Confermata con precisazione (S-08) |
| 22 | 0 sfide «impossibili» (passate solo con il MAE) | continuità §2; JSON | 0, e la proprietà è garantita dalla costruzione CRN | Confermata |
| 23 | Guardia 2\|μ\|·max(1, R:R) < 700; `ValueError` invece di `OverflowError` | risposta §2.7 | confermato su 15 casi estremi; guardia più restrittiva del necessario | Confermata con precisazione (S-05) |
| 24 | Soglia μ ≈ 0 a 10⁻⁷, allineata tra risolutore e campionatore | risposta §2.7 | coerente; F continua alla soglia | Confermata |
| 25 | La deriva riproduce il WR entro 10⁻⁷ | intestazione del motore | errore ≤ 2·10⁻¹⁶ (10⁻⁸ alla soglia) | Confermata |
| 26 | MAE «per qualsiasi (WR, R:R)» `[DIMOSTRATO]` | risposta, riga 155 | valido nel dominio accettato dalla guardia, non per qualsiasi coppia | Confermata con precisazione (S-08) |
| 27 | LEGGIMI_V1: due modalità, hash atteso `a6781b7e…` | risposta §2.6; LEGGIMI | modalità A OK; modalità B fallisce (`main` inesistente); import citato in modo errato | Non confermata per la modalità B (S-03) |
| 28 | Intestazioni e attribuzioni standardizzate | risposta §2.5 | coerenti in tutti i file | Confermata |
| 29 | «Come osservato da Claude, V01 (tolleranza bisezione…)» | risposta, riga 69 | V01 è «la fase 2 riusa i generatori della fase 1» | Non confermata (S-08) |
| 30 | Revisione V3.1 al commit `8544a15` | risposta, riga 7 | `8544a15` è la revisione V3; quella V3.1 è `9ff4514` | Non confermata (S-08) |
| 31 | Regole FTMO: «Regolamento ufficiale FTMO» | risposta, riga 160 | il JSON dello stesso pacchetto dichiara V-SEC; non riverificato in questa sessione | Incoerenza interna (S-08) |
| 32 | Q-07 e Q-09 non modificati | risposta §3 | file d'archivio identici | Confermata |
