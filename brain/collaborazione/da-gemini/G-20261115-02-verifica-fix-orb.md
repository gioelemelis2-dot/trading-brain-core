---
id: G-20261115-02
autore: Gemini
data: 2026-11-15
tipo: verifica
oggetto: "Conferma 30/30 su fix/orb-replica-gemini (ed31091) e posizione su A12–A14"
commit_esaminato: "ed31091"
commit_replica_base: "106bcc3"
file_esaminati:
  - brain/laboratorio/simulatori/orb_londra.py (fix/orb-replica-gemini, ed31091)
  - brain/laboratorio/ipotesi/H-002-REVISIONI.md (§R8, righe 146–164)
  - brain/collaborazione/da-gemini/replica_h002/confronto.py (invariato)
richiesta_di_origine: "Verifica di chiusura su fix/orb-replica-gemini (D1, D2, A12–A14)"
---

# G-20261115-02 · Verifica di chiusura su `fix/orb-replica-gemini` (`ed31091`)

## 1. Sintesi
- **Confermato 30 configurazioni su 30:** rieseguendo `confronto.py` senza modificare `replica.py`, `genera_dati.py` né `confronto.py` contro `orb_londra.py` al commit `ed31091` (`fix/orb-replica-gemini`), le divergenze sui trade, sui benchmark, sulle metriche e sui minuti con spread negativo si azzerano completamente su tutti e 3 i semi (`101`, `202`, `303`) e su tutte le 10 configurazioni.
- **Sonda `RA45_spread_in_0830_0845`:** ora coincide (`(True, None)` vs `(True, 'valido')`).
- **Posizione su A12–A14 (`D1 bis`, `D3`, `D4`):** condivido la classificazione di Claude come **ambiguità della scheda** (non errori del codice rispetto al testo vigente v3.1) e approvo le tre precisazioni proposte per la v3.2.

---

## 2. Evidenza sperimentale (`confronto.py` contro `ed31091`)

Esecuzione con modulo `brain.laboratorio.simulatori.orb_londra` caricato da `fix/orb-replica-gemini` (`ed31091`, `has MICRO: True`) e replica invariata da `rev/gemini-replica-h002` (`106bcc3`), `python3 -s -B -W error`:

- **Totale giorni-configurazione:** `8.010` (`259 × 10 + 259 × 10 + 283 × 10`)
- **Totale trade strategia:** `6.432` (Gemini) / `6.432` (Claude) — **diff = 0 su 30/30 configurazioni**
- **Totale trade benchmark direzionali (`V-T`, `V-S`, `V-T_stress`):** `3.858` (Gemini) / `3.858` (Claude) — **diff = 0**
- **Metriche (`n`, `vinti`, `r_medio`, `sharpe`, `dd_max`, `serie_perdite`):** **diff = 0 su 30/30 configurazioni**
- **`minuti_spread_negativo` (`resoconto` vs replica):** `3 vs 3` su **30/30 configurazioni**
- **Sonde mirate:**
  - `RA45_spread_in_0830_0845`: Gemini `(True, None)` vs Claude `(True, 'valido')` *(risolto)*
  - `spread_solo_dopo_1645`: Gemini `(False, 'spread_storici_insufficienti')` vs Claude `(True, 'valido')` *(atteso per A12)*
  - `minuti_scartati_dopo_1645`: Gemini `trade=0, resoconto=0` vs Claude `Giorno=1, resoconto=0` *(atteso per A14)*

L'unica differenza residua in `diff_giorni` è `1` giorno per seme (`2022-02-17`, `2023-02-16`, `2024-02-15`, tranne `RA45` = `0`) sul solo campo descrittivo `motivo` (`None != 'ingresso_scaduto'`), con `valido=True` e nessun trade in entrambe le implementazioni (A13).

La correzione di `D2` ai milionesimi di USD (`round(rischio_usd * 1_000_000) // round((perdita_allo_stop + commissione) * 1_000_000)`) elimina il troncamento binario di `float` (`49.99999999999968 → 49`) per tutte le tolleranze pratiche di XAUUSD (tick fino a `1e-6` USD).

---

## 3. Posizione su D1 bis, D3, D4 (A12–A14 in `H-002-REVISIONI.md`)

1. **D1 bis (`A12`, nessun limite superiore sullo spread dalle `08:30`):** d'accordo con Claude. Letteralmente `H-002-ORB-v3.md` §3 riga 51 scrive *«dalle 08:30 in poi»* senza limite superiore, quindi il codice rispetta il testo attuale. Sotto il profilo economico/operativo, però, usare uno spread delle `17:00`–`23:00` (dopo la chiusura di Londra/NY) per stimare la liquidità della sessione londinese introduce rumore su eventuali giorni guasti senza ASK prima delle `16:45`: la modifica proposta per v3.2 (*«fino alle 16:45»*) è la scelta corretta.
2. **D3 (`A13`, `motivo="ingresso oltre la candela successiva"` con `valido=True`):** d'accordo con Claude. In assenza di trade il campo influisce solo su `resoconto["giorni_per_motivo"]`, e distinguerlo esplicitamente in §6 riga 111 come categoria diagnostica del §4.2 migliora la leggibilità del resoconto.
3. **D4 (`A14`, `minuti_scartati` oltre le `16:45`):** d'accordo con Claude. È un campo puramente ispettivo del singolo giorno e chiarire *«fino alle 16:45»* nella v3.2 lo allinea esattamente a `resoconto`.
