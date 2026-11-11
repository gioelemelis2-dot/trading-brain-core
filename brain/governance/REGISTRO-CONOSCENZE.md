# Registro delle conoscenze

Stato di ogni blocco di conoscenza. **"Scritto" non significa "acquisito"**: la colonna *Padronanza* si aggiorna solo con un cancello superato, dichiarato dall'utente con data.

Legenda contenuto: `v1` (manuale originale) · `bozza` · `verificata` · `da aggiornare` · `da correggere`.
Legenda padronanza: — (non verificata) · L1…L5 con data.

## Moduli e lezioni

| Blocco | Contenuto | Fonti (stato prevalente) | Controverso? | Obsolescenza | Padronanza |
|---|---|---|---|---|---|
| M0 · 0.1 Onestà sull'obiettivo (L1–4) | v1 · **da correggere** (A4, A7, A9) | V-sec per 6 fonti chiave | Ampiezza dei fattori sopravvissuti | Bassa | — |
| M0 · 0.2 Modello mentale (L5–8) | v1 | C | No | Bassa | — |
| M0 · 0.3 Ancora statistica (L9–18) | v1 · numeri **verificati** (B1–B6) | Calcolo esatto | No | Bassa | — |
| M0 · 0.4 Fattore umano (L19–24) | v1 · **da correggere** (A12–A14, C6) | C / V-sec | Sì: neuroscienze divulgative, entità della loss aversion | Media | — |
| M1 · 1.1 Mercati e motori | v1 · **da correggere** (A15) | C / V-sec | Correlazioni instabili | Media (orari, correlazioni) | — |
| M1 · 1.2 Strumenti | v1 · **da aggiornare** (A16–A18) | C | No | **Alta** (fiscalità, leve, specifiche) | — |
| M1 · 1.3 Cripto | v1 | C | Sì (valutazione) | Alta | — |
| M1 · 1.4 Orizzonti | v1 · nota C3 | E5 | No | Bassa | — |
| M1 · 1.5 Microstruttura essenziale | v1 · numeri verificati (B11) | C | No | Bassa | — |
| M2 · L2.1 Banche centrali | **bozza v0.1** | V-sec (Fed, BCE), C (Taylor, BoE, BoJ) | r*, efficacia del QE | **Alta** (strumenti, livelli) · revisione entro 2027-05-11 | — |
| M2 · L2.2 Aspettative e sorprese | **bozza v0.1** | V-sec (Kuttner, Bernanke-Kuttner, GSS, J-K, CME) | Sì: effetto informativo | Bassa | — |
| M2 · L2.3 Trasmissione | **bozza v0.1** | V-sec + C | Sì: ruolo del posizionamento | Media | — |
| M2 · Protocollo analisi movimento | **bozza v0.1** | — (metodo) | — | Bassa | — |

## Strumenti

| Strumento | Verifica | Data |
|---|---|---|
| `strumenti/verifica_m0.py` | Eseguito; riproduce B1–B9 | 2026-11-11 |
| `strumenti/sorpresa_monetaria.py` | Eseguito; esempi di L2.2 coincidono | 2026-11-11 |

## Affermazioni controverse tracciate
| Affermazione | Posizioni | Dove |
|---|---|---|
| Effetto informativo delle banche centrali | Nakamura-Steinsson 2018 (forte) vs Bauer-Swanson 2023 (la Fed reagisce a notizie pubbliche) | L2.2 §5.4 |
| Entità della loss aversion | λ ≈ 2,25 (Tversky-Kahneman 1992) vs critiche (Gal-Rucker 2018) | 0.19 (da aggiornare) |
| "Winner effect" ormonale nei trader | Ipotesi su campioni piccoli (Coates-Herbert 2008) | 0.19 (da aggiornare) |
| Superiorità dei modelli ML complessi | Kelly-Malamud-Zhou 2024 vs letteratura sull'overfitting | traccia 10.4 (futura) |

## Contenuti con scadenza
| Contenuto | Rivedere entro |
|---|---|
| L2.1 strumenti e livelli dei tassi | 2027-05-11 |
| 1.13 fiscalità italiana | a ogni Legge di Bilancio (prossima verifica: gennaio 2027) |
| 1.10 leve ESMA/CFD | 2027-11-11 |
