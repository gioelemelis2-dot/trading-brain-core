# Registro delle conoscenze

Aggiornato: 2026-11-11, fine sprint S2.

Stato di ogni blocco di conoscenza. **"Scritto" non significa "acquisito"**: la colonna *Padronanza* si aggiorna solo con un cancello superato, dichiarato dall'utente con data.

Stato del contenuto (STANDARD §9): `v1` (manuale originale) · `bozza` · `in_verifica` · `verificata` · `da_aggiornare` · `da correggere`.
Padronanza: — (non verificata) · L1…L5 con data.

## Moduli e lezioni

| Blocco | Contenuto | Fonti (stato prevalente) | Controverso? | Obsolescenza | Padronanza |
|---|---|---|---|---|---|
| M0 · 0.1 Onestà sull'obiettivo (L1–4) | v1 · **da correggere** (A4, A7, A9) | V-sec per 6 fonti chiave | Ampiezza dei fattori sopravvissuti | Bassa | — |
| M0 · 0.2 Modello mentale (L5–8) | v1 | C | No | Bassa | — |
| M0 · 0.3 Ancora statistica (L9–16, 18) | v1 · numeri **verificati** (B1–B6) | Calcolo esatto | No | Bassa | — |
| M0 · 0.17 Statistica descrittiva | v1 · **non riproducibile** finché non arrivano i dati del vault (C5, Q8, Q9) | Dati dell'utente | — | Bassa | — |
| M0 · 0.4 Fattore umano (L19–24) | v1 · **da correggere** (A12–A14, C6) | C / V-sec | Sì: neuroscienze divulgative, entità della loss aversion | Media | — |
| M1 · 1.1 Mercati e motori | v1 · **da correggere** (A15) | C / V-sec | Correlazioni instabili | Media | — |
| M1 · 1.2 Strumenti | v1 · **da aggiornare** (A16–A18) | C | No | **Alta** (fiscalità, leve, specifiche) | — |
| M1 · 1.3 Cripto | v1 | C | Sì (valutazione) | Alta | — |
| M1 · 1.4 Orizzonti | v1 · nota C3 | E5 | No | Bassa | — |
| M1 · 1.5 Microstruttura essenziale | v1 · numeri verificati (B11) | C | No | Bassa | — |
| M2 · L2.1 Banche centrali | **in_verifica** v0.1 | V-sec (Fed, BCE), C (Taylor) | r*, efficacia del QE | **Alta** · entro 2027-05-11 | — |
| M2 · L2.2 Aspettative e sorprese | **in_verifica** v0.1 | V-sec | Sì: effetto informativo | Bassa | — |
| M2 · L2.3 Trasmissione | **in_verifica** v0.1 | V-sec + C | Sì: ruolo del posizionamento | Media | — |
| M2 · L2.4 Tassi reali e inflazione attesa | **in_verifica** v0.1 | V-sec (D'Amico-Kim-Wei, Erb-Harvey), C (TIPS, BTP) | Sì: legame oro–tassi reali | Bassa | — |
| M2 · L2.5 Bilancio: QE, QT, riserve | **in_verifica** v0.1 | V-sec (Gagnon et al., Fed), C | Sì: entità e persistenza degli effetti | **Alta** · entro 2027-05-11 | — |
| M2 · L2.6 Fed, BCE, BoJ, BoE | **in_verifica** v0.1 | V-sec (BoJ, BoE, Fed, BCE), C (composizione comitati, calendari) | No | **Alta** · entro 2027-05-11 | — |
| M2 · Protocollo analisi movimento | bozza v0.1 (manca un esempio compilato su dati reali) | — (metodo) | — | Bassa | — |

Nessuna lezione è `verificata` al 2026-11-11.

## Strumenti

| Strumento | Verifica | Classe di dati | Data |
|---|---|---|---|
| `strumenti/verifica_m0.py` | Eseguito; riproduce B1–B9 | calcolo esatto | 2026-11-11 |
| `strumenti/sorpresa_monetaria.py` | Eseguito; esempi di L2.2 coincidono | `[ESEMPIO]` | 2026-11-11 |
| `strumenti/tassi_reali.py` | Eseguito; esempi ed esercizi di L2.4 coincidono | `[ESEMPIO]` | 2026-11-11 |
| `strumenti/riproduci_017.py` | Test su casi costruiti a mano + serie GBM | `[SIMULATO]` solo per test; nessun dato reale elaborato | 2026-11-11 |

## Dati

| Dato | Classe | Stato |
|---|---|---|
| Serie OHLC del vault per la lezione 0.17 | `[REALE]` | **richiesti all'utente** (`dati/RICHIESTA-DATI-0.17.md`) |
| GBM-017 | `[SIMULATO]` | generatore documentato in `dati/simulati/README.md` |

## Affermazioni controverse tracciate
| Affermazione | Posizioni | Dove |
|---|---|---|
| Effetto informativo delle banche centrali | Nakamura-Steinsson 2018 (forte) vs Bauer-Swanson 2023 (la Fed reagisce a notizie pubbliche) | L2.2 §5.4 |
| Entità della loss aversion | λ ≈ 2,25 (Tversky-Kahneman 1992) vs critiche (Gal-Rucker 2018) | 0.19 (da aggiornare) |
| "Winner effect" ormonale nei trader | Ipotesi su campioni piccoli (Coates-Herbert 2008) | 0.19 (da aggiornare) |
| Oro e tassi reali | Narrazione diffusa vs Erb-Harvey 2013 | L2.4 §5.4 |
| Entità e persistenza degli effetti del QE | Event study vs persistenza discussa | L2.5 §13 |
| Superiorità dei modelli ML complessi | Kelly-Malamud-Zhou 2024 vs letteratura sull'overfitting | traccia 10.4 (futura) |

## Contenuti con scadenza
| Contenuto | Rivedere entro |
|---|---|
| L2.1, L2.5, L2.6 (strumenti, bilanci, comitati, calendari) | 2027-05-11 |
| 1.13 fiscalità italiana | a ogni Legge di Bilancio (prossima verifica: gennaio 2027) |
| 1.10 leve ESMA/CFD | 2027-11-11 |

## Revisioni esterne (Gemini)
| Rapporto | Oggetto | Esito |
|---|---|---|
| — | Nessun rapporto ricevuto al 2026-11-11 | — |
