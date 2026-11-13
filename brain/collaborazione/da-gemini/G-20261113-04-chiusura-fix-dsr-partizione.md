---
id: G-20261113-04
autore: gemini
data: 2026-11-13
tipo: verifica-chiusura
oggetto: Verifica di chiusura delle correzioni G3-01…G3-06 su fix/dsr-e-partizione-date (commit 6a55e9a)
commit_esaminato: 6a55e9a
file_esaminati:
  - brain/laboratorio/backtester/dsr.py
  - brain/laboratorio/tests/test_dsr_scala.py
  - brain/dati/pipeline/partizione_date.py
  - brain/dati/tests/test_partizione_date.py
  - brain/dati/pipeline/dukascopy.py
  - brain/dati/tests/test_dukascopy.py
  - brain/dati/tests/mutazioni_dsr_partizione.py
  - brain/collaborazione/da-claude/ESITI.md
richiesta_di_origine: "Richiesta utente 2026-11-13: verifica di chiusura breve e dura sulle correzioni 6a55e9a + verdetto esplicito merge sì/no"
---

# Rapporto G-20261113-04 — Verifica di chiusura di `fix/dsr-e-partizione-date` (`6a55e9a`)

## 1. Sintesi (max 5 righe)

Verificate sul worktree `../tb-revisione-claude` (`6a55e9a`) tutte le correzioni ai rilievi `G3-01…G3-04` e `G3-06`. Tutti i probe d'attacco precedenti e i nuovi tentativi di bypass crittografico su `partizione_date.verifica()` **falliscono**. Suite verdi in locale su Python `3.9.6` (**73/73** `dati+laboratorio`, **77/77** `guardian`) e **40/40 mutanti uccisi**. **Verdetto: MERGE SÌ** (con autorizzazione dell'utente), mantenendo aperti solo `G3-05` (`DA-19`/`DA-28`) e `G3-07` come concordato.

---

## 2. Metodo

1. Aggiornato il worktree separato `../tb-revisione-claude` a `origin/fix/dsr-e-partizione-date` (`6a55e9a`), senza modificare alcun file di Claude né toccare la cartella principale del repo.
2. Eseguiti i probe riproduttivi per `G3-01…G3-04` e `G3-06`, verificando che ogni input/attacco venga ora respinto o bloccato.
3. Tentati nuovi bypass su `partizione_date.verifica(cartella, file_nonce, partizione, partizione_sha256)` (rimozione `commitment_hash`, sostituzione `verifica.jsonl` ← `sviluppo.jsonl` anche col nonce reale, duplicazione blocchi, iniezione di tipi spuri in `comm["blocchi"]`, `embargo_giorni=true` vs `1`, alterazione metadati descrittivi `status`/`candele`).
4. Eseguite le suite `unittest` (`-s -B -W error`) e `mutazioni_dsr_partizione.py`.

---

## 3. Rilievi

| ID | Gravità | Stato su `6a55e9a` | Esito della verifica empirica |
|---|---|---|---|
| G3-01 | ALTO | **CHIUSO** | `NaN`, `+inf` su `SR`/`skew`/`kurt`/`benchmark` e `N=0`, `N=-3`, `bool` su `N`/`T` sollevano tutti `ValueError`. Nota `N=1` corretta. |
| G3-02 | ALTO | **CHIUSO** | Downgrade `"ruolo": "sviluppo"` in `commitment.json` con dati alterati e nonce finto dà `valido=False, partizione=False`. Nessun bypass dei dati/sigilli riuscito nei nuovi test `2a, 2b, 2f` (tutti `False`). |
| G3-03 | MEDIO-ALTO | **CHIUSO** | Buco diurno mer `10:00→12:15` ora dà `anomali=1` (`ANOMALO (chiusura lunga in orario di mercato)`); picco intra-candela `2650→9999` solleva `ErroreDati`. Nota residua: chiusure `>2h` con `fine.hour >= 17` restano in `buchi_da_verificare` (scelta intenzionale per le 22 chiusure festive reali). |
| G3-04 | MEDIO | **CHIUSO** | Con `sealed_nonce.secret` già presente, `esegui(..., partizione=...)` solleva `FileExistsError` **prima** di scaricare/scrivere; `XAUUSD_15m.csv` preesistente resta intatto (`SENTINEL`). |
| G3-05 | MEDIO | APERTO (concordato) | Invariato e rinviato a `DA-19`/`DA-28` (`V = max(1/(T-1), V_emp)`). |
| G3-06 | BASSO | **CHIUSO** | `sec=-1`, `sec=86400`, `vol=NaN`, `lo=0` sollevano tutti `ErroreDati` in `decodifica()`. |
| G4-01 | BASSO (nuovo) | Non bloccante | Nel nuovo `verifica()` (`partizione_date.py:173-193`), tre anomalie di schema in `commitment.json` restano tollerate se si possiede il nonce reale e i `.jsonl` sono intatti: (1) elementi non-`dict` in `comm["blocchi"]` vengono ignorati dal filtro `isinstance(d, dict)`; (2) `embargo_giorni: true` in JSON passa se la partizione ha `1` (`True == 1` in Python); (3) campi descrittivi non hashati (`status`, `candele`) non sono coperti da `ok_part`. **Nessuno di questi consente di falsificare candele o aggirare un sigillo** senza il nonce segreto. |

---

## 4. Contenuti nuovi proposti

### 4.1 Tabella risultati osservati su `6a55e9a` (Python `3.9.6`)

| Controllo | Esito osservato |
|---|---|
| `unittest` 6 moduli (`test_pipeline`, `test_dukascopy`, `test_partizione_date`, `test_backtester`, `test_anti_frode_statico`, `test_dsr_scala`) con `-s -B -W error` | **73/73 OK** (`0.564s`) |
| `unittest discover -s brain/guardian/test -p "test_*.py"` con `-s -B -W error` | **77/77 OK** (`6.280s`) |
| `mutazioni_dsr_partizione.py` | **40/40 mutanti uccisi** (`exit 0`) |
| Probe `G3-01…G3-04`, `G3-06` + bypass `2a, 2b, 2f` su `verifica()` | **Tutti bloccati** |

### 4.2 Verdetto esplicito sul merge in `main`

**VERDETTO: MERGE SÌ** (con autorizzazione esplicita dell'utente).

**Motivazione:**
1. Tutti i difetti critici/alti/medi di correttezza e integrità sollevati in `G-20261113-01` e `G-20261113-03` (`G3-01`, `G3-02`, `G3-03`, `G3-04`, `G3-06`) sono stati risolti in TDD e hanno retto sia ai probe di attacco diretti sia ai tentativi aggiuntivi di bypass su `verifica()`.
2. La copertura di verifica locale su Python `3.9.6` è completa (**73/73** `dati+laboratorio`, **77/77** `guardian`, **40/40** mutanti uccisi) senza regressioni.
3. I soli punti aperti (`G3-05` registro unico/`N_eff`, `G3-07` integrale `E[max]` per piccoli `N`, e il dettaglio igienico non sfruttabile `G4-01`) sono tracciati, non compromettono la correttezza del filtro DSR né l'integrità dei sigilli `partizione_date`, e appartengono correttamente a iterazioni successive (`DA-19`/`DA-28`).

---

## 5. Lacune, duplicazioni, contraddizioni trovate

- Solo il dettaglio di pulizia `G4-01` su `partizione_date.verifica()` (`bool` vs `int` per `embargo_giorni`, elementi non-`dict` in `comm["blocchi"]`, campo `status`); impatto sulla sicurezza **nullo** finché il nonce segreto è protetto.

---

## 6. Fonti consultate

1. Worktree `origin/fix/dsr-e-partizione-date` al commit `6a55e9a` (`/Users/gioele/Downloads/tb-revisione-claude`).
2. `brain/collaborazione/da-claude/ESITI.md` su `6a55e9a`.
3. Output diretti di probe Python, `unittest` e `mutazioni_dsr_partizione.py` eseguiti il 2026-11-13 su Python `3.9.6`.

---

## 7. Limiti del rapporto

- Verificato su Python `3.9.6` (`python3.13` non disponibile in questa macchina).
- Nessun file del ramo di Claude modificato; nessuna operazione sulla cartella principale eccetto la creazione di questo rapporto sul ramo `rev/vettori-dsr-gemini`.
