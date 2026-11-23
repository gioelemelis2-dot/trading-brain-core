# Ricevuta del candidato `67380cd` per R19 · 23/11/2026 (parziale: mutanti in corso)

**Commit:** `67380cd5ff7d1f0b5f0e250fb79742de5493687a`, ramo `feat/esecutore-h002`.
**Dove:** worktree bloccato sul commit, nel contenitore di Claude, con la rete bloccata. Python 3.13.18 e 3.9.25.

## Che cosa cambia rispetto a `1431190` (candidato di partenza di R19)
- `b9ec2f4`:
  - **#139:** una sola autorizzazione per domanda nel registro della riserva;
  - **#140:** la ripresa riconcilia i due registri;
  - giornate K = 0 nel mercato sintetico;
  - `riconcilia_record.py`;
  - il controllo dei mutanti verifica anche la sintassi.
- `67380cd`, **solo test e mutanti** (lacune dei test di Claude trovate nella revisione critica):
  - #139 anche dopo l'esito della prima verifica (mutante PR14, che sopravviveva);
  - ripresa tecnica identica dopo una caduta durante la lettura;
  - il rifiuto non rilascia la prenotazione (caso B).
- **Il codice del perimetro è identico a `b9ec2f4`:** `git diff b9ec2f4 67380cd` su `esecuzione`, `verdetto` e `dati/pipeline` è vuoto. La ricevuta lo conferma con `perimetro_modificato_rispetto_al_commit: false`.

## Esiti

| Prova | 3.13.18 | 3.9.25 | Log |
|---|---|---|---|
| Suite complete | **TUTTO VERDE**, 757 test | **TUTTO VERDE**, 757 test | `log/67380cd_suite_py*.log` |
| Prove A–G del percorso ordinario (`ricevuta_127.py`) | osservato = atteso in tutte e 7 | uguale | `log/67380cd_ricevuta_py*.json` |
| Riconciliazione dal record, corsa A (`riconcilia_record.py`) | **5/5, «tutti»: true** | **5/5, «tutti»: true** | `log/67380cd_riconcilia_py*.json` |
| Mutanti del percorso (62) | **61/62** (MF09 equivalente) | **61/62** (MF09 equivalente) | `log/67380cd_mutanti_percorso_py*.log` |
| Mutanti del verdetto (132) | **131/132** (VD13 equivalente) | non eseguita | `log/67380cd_mutanti_verdetto_py313.log` |
| Mutanti del perimetro (299, in 4 gruppi) | non eseguita | non eseguita | — |
| **Prova positiva completa dal lanciatore** (`prova_lanciatore.py`) | **FALLITA: difetto #142** | — | `log/67380cd_prova_lanciatore_py313_FALLITA_142.json` |

**Riconciliazione, corsa A** (uguale sulle due versioni):
- esito promossa, causa «L > +0,20 R e requisiti superati»;
- 1.000 sedute, tutte con trade;
- media `0x1.88dd3fe19743fp-2` ≈ 0,3836565 R.

La corsa A non ha giornate con K = 0: quel caso è provato dal test con le giornate neutre (`test_coppie_zero_e_riconciliazione_dal_record`).

**Su `b9ec2f4`** (stesso perimetro): suite verdi, 746 test, e riconciliazione 5/5 su entrambe le versioni (`log/b9ec2f4_*`).

## Esito: `67380cd` NON è un candidato valido (difetto #142)

- La prova positiva completa dal lanciatore, chiesta da DGS-18, ha trovato che il percorso ordinario **non può arrivare in fondo**.
- Il lanciatore `avvio.py` non è nel codice sigillato, quindi il controllo dell'ambiente lo trova caricato e ferma la verifica: codice d'uscita 2, «avvio.py: modulo brain non sigillato».
- La correzione, con i test scritti prima (incluso un test positivo completo dal lanciatore nella suite), fa nascere un candidato nuovo: ricevuta in `../2026-11-23-candidato-<nuovo>/`.
- I mutanti del verdetto restano validi per il modulo del verdetto, che non cambia.

## Da completare (superato)
I mutanti dei tre script su entrambe le versioni. Questa ricevuta si aggiorna con i conteggi e gli equivalenti dichiarati (MF09, VD13).
