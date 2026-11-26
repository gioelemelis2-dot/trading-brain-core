# Ricevuta del candidato `7191156` per R19 · 23/11/2026 (completa)

**Commit:** `7191156d1e3f2c42b5d6a6445fbb6df6086e16fd`, ramo `feat/esecutore-h002`.
**Dove:** worktree bloccato sul commit, contenitore di Claude, rete bloccata; Python 3.13.18 e 3.9.25.

## Che cosa cambia rispetto a `67380cd`
- **#142:** `esegui_verifica.impronte_codice` include il lanciatore `avvio.py`, come il #95 nel vecchio esecutore. Senza, la verifica vera dal lanciatore si fermava sempre (ricevuta di `67380cd`).
- **Test nuovi:** `test_il_lanciatore_e_nel_codice_sigillato` e `test_positivo_completo_dal_lanciatore`, che fa la corsa intera in un repository git con un remoto finto, controlli accesi. Mutante nuovo **EV34**.
- Nel perimetro cambia solo `esegui_verifica.py`, 3 righe. Il modulo del verdetto è identico.

## Esiti

| Prova | 3.13.18 | 3.9.25 | Log |
|---|---|---|---|
| Suite complete | **TUTTO VERDE**, 759 test | **TUTTO VERDE** | `log/suite_py*.log` |
| Prove A–G (`ricevuta_127.py`) | osservato = atteso | osservato = atteso | `log/ricevuta127_py*.json` |
| Riconciliazione dal record, corsa A | **5/5** | **5/5** | `log/riconcilia_py*.json` |
| **Prova positiva completa dal lanciatore** (`../2026-11-23-candidato-67380cd/prova_lanciatore.py`) | **superata** | **superata** | `log/prova_lanciatore_py*.json`, `log/lanciatore_py*.log` |
| Mutanti del percorso (63) | **62/63** (MF09 equivalente; EV34 ucciso) | **62/63** (MF09 equivalente) | `log/mutanti_percorso_py*.log` |
| Mutanti del verdetto (132) | 131/132 su `67380cd`, stesso modulo (VD13 equivalente) | **131/132** (VD13 equivalente) | `log/mutanti_verdetto_py39.log`; 3.13 in `../2026-11-23-candidato-67380cd/log/` |
| Mutanti del perimetro (299, 4 gruppi) | **299/299** (N,K 96; V,E,S,TA,MG,MR 71; C,IX,R,Q 62; P 70) | **299/299** (stessi gruppi) | `log/mutanti_perimetro_*` |

## La prova positiva dal lanciatore, in dettaglio (uguale su 3.13 e 3.9)
- **Comando:** `python3 -I -S -B brain/laboratorio/esecuzione/avvio.py verifica --scheda … --registro brain/laboratorio/registro_prove.json --riserva brain/laboratorio/registro_riserva.json --prenotazione P1 …`. Processo separato; ancora git e controllo dell'ambiente accesi come nel codice, senza sostituzioni.
- **Prima chiamata:** codice 0, «completata», **promossa**. Riserva: una sola apertura, P1, j = 1. Registro delle prove: sviluppo → verifica → esito.
- **Storia git del repository di prova:** «sigillo e prenotazione P1», poi «esito della verifica P1», entrambi pubblicati sul remoto finto.
- **Seconda chiamata identica:** codice 0, «rapporto rigenerato», riserva invariata, rapporto identico a byte.
- **Controlli dal solo record:**
  - identità dell'impegno;
  - sedute (le date delle coppie uguali all'elenco impegnato);
  - media esatta;
  - verdetto ricalcolato;
  - rapporto a byte;
  - byte uguali alla ripresa.

  Tutti **veri**.
- **Conservati:** record, impegno e rapporto della prova (`log/record_P1_lanciatore_py*.json`, `log/impegno_P1_lanciatore_py*.json`, `log/rapporto_P1_lanciatore_py*.txt`).
- **Riga della potenza nel rapporto:** «[STIMA] · incertezza: dalla procedura congelata nella scheda prima del sigillo». È il **#141**, ancora aperto: il valore 0,60 è dichiarato nel contratto di test, non calcolato.

## Esito
Su `7191156`, su Python 3.13.18 e 3.9.25:
- suite verdi;
- A–G con osservato = atteso;
- riconciliazione 5/5;
- **prova positiva completa dal lanciatore superata**;
- mutanti: percorso 62/63, verdetto 131/132, perimetro 299/299. Gli unici vivi sono gli equivalenti dichiarati, MF09 e VD13.

Il verdetto su 3.13 è attribuito a `67380cd`, con lo stesso modulo.

**Aperti noti, non in questa ricevuta:**
- #141, minore, nel prossimo lotto;
- il possibile varco R19-04 segnalato da Gemini (α totale del registro della riserva non fissato a D-38). Va riprodotto quando arriva il suo rapporto.
