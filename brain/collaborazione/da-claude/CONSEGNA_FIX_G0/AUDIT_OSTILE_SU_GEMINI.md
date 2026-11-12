# Audit ostile e verifica materiale sul lavoro di Gemini Antigravity

**Data:** 12/11/2026, 21:14–21:25 UTC · **Autore:** Claude · **Mandato:** «Mandato notturno zero-trust», Task 3
**Regola applicata:** ogni affermazione è legata a un comando ripetibile; ciò che non ho potuto controllare è dichiarato «non verificabile», non attribuito a Gemini. Nessun file di Gemini è stato modificato e nessun suo codice è stato eseguito: gli ZIP sono stati letti in memoria.

## 1. Esito in breve
| # | Affermazione del mandato | Esito | Prova |
|---|---|---|---|
| 1 | Ramo `origin/feat/lab-dati-backtester` da ispezionare | **Assente su GitHub.** Test ostili su `brain/dati/pipeline/` e `brain/laboratorio/backtester/` non eseguibili | §2 |
| 2 | Gemini ha scritto l'hash `6fb9d76e73fbf…fec97638` per lo ZIP V3.3 | **Non verificabile nei materiali disponibili.** L'hash falso non compare in nessun materiale di Gemini a mia disposizione; nella continuità V3.3 Gemini dichiara l'hash **corretto** | §3 |
| 3 | `float` in `dsr.py` | **Non verificabile:** `dsr.py` non esiste in nessuna fonte accessibile | §2, §5 |
| 4 | Slippage nascosto con `slippage_fixed = 0` nei test | **Non verificabile** per il codice nuovo (assente). Nel codice V3–V3.3 disponibile, `slippage_fixed` non esiste e gli slippage a zero nei test sono test di **rifiuto** | §5 |
| 5 | (mio controllo aggiuntivo) Integrità di tutti i materiali di Gemini ricevuti | **138/138 coppie (file, hash) dichiarate coincidono** con i byte reali | §4 |

Conclusione: allo stato delle prove, **nessuno dei tre errori attribuiti a Gemini è dimostrabile**. Il punto 2, così come formulato («nel suo ultimo turno»), riguarda un testo che non mi è stato consegnato.

Il §3 mostra però che l'hash falso è quasi certamente stato **ricostruito da una forma abbreviata** usata nei documenti del Brain, compresi i miei: è un difetto di processo reale, con un rimedio (§6).

## 2. Ramo remoto e codice del Binario B
- `git fetch --all --prune` (il remoto è configurato per un solo ramo) e poi `git ls-remote --heads origin`, alle 21:14:10Z, restituiscono solo due rami:
  ```
  0396995161409b71d75925ba47b79db6939cdbf4  refs/heads/feat/fix-g0-journal
  0a1f8604514ca2ec39da7cc836c63392a1d82d8e  refs/heads/main
  ```
- `brain/laboratorio/` non esiste in nessun ramo. `brain/dati/` contiene solo `README.md`, `RICHIESTA-DATI-0.17.md`, `reali/README.md` e `simulati/README.md`, invariati dal commit `8bf9460` (sprint S2, di Claude). Non c'è codice di Gemini.
- Ricerca di `dsr.py`, `slippage_fixed`, `feat/lab-dati-backtester`, `pipeline` e `backtester` in tre fonti, sempre senza risultati:
  - i due repository (`trading-brain-core`, `l-Altro`);
  - la loro intera storia (`git log --all`);
  - i 6 ZIP e i file ricevuti da Gemini in questa sessione.
- **Conseguenza:** nessun test ostile eseguibile sul Binario B. Una lista pronta per quando il ramo sarà pubblicato è nel §7.

## 3. L'hash del pacchetto V3.3
**Hash reale, ricalcolato ora dal file ricevuto** (`57ea5ce6-TRADING_BRAIN_V3_3_PACKAGE.zip`, 62.513 byte):
```
6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638
```

| Dove | Hash | Corretto? |
|---|---|---|
| `CONTINUITA_V3_3_PASSAGGIO_A_CLAUDE.md` di Gemini, righe 17 e 69 | `6fb9d76e54da…627638` | **sì** |
| `R-CLAUDE-20261112-05-V33/output/hash_v33_ricevuti.txt` (mio) | `6fb9d76e54da…627638` | sì |
| `CLAUDE_FINAL_REVIEW_V3_3.md` riga 38 (mio) | `6fb9d76e54da…627638` | sì |
| `ERRATA_V3_3.md` riga 4, `CLAUDE_FINAL_REVIEW_V3_3.md` riga 3 (miei) | `6fb9d76e…7638` (abbreviato) | non controllabile da solo |
| `CONTINUITA.md` riga 35, `REGISTRO-MODIFICHE.md` riga 119 | `6fb9d76e…` (abbreviato) | non controllabile da solo |

**Ricerca dell'hash falso `6fb9d76e73fbf509938ca9e28bf6152ef3225883ef5fbe8e1bb3f7a1fec97638`:**
- file di lavoro di `trading-brain-core` e di `l-Altro`: **0** occorrenze;
- storia completa dei due repository (`git log --all -S 6fb9d76e73fbf`): **0**;
- materiali ricevuti da Gemini: **0**;
- unica occorrenza: il testo del mandato stesso, nella trascrizione di questa sessione.

**Analisi dell'hash falso.**
- È formalmente valido: 64 caratteri esadecimali.
- Coincide con quello vero **esattamente** nei primi 8 caratteri (`6fb9d76e`) e negli ultimi 4 (`7638`): cioè proprio nella forma abbreviata `6fb9d76e…7638` dei documenti del Brain.
- Per caso, la probabilità che un hash casuale coincida su quei 12 caratteri è 16⁻¹² ≈ 3,6 × 10⁻¹⁵.
- **Conclusione (IPOTESI ben fondata, non una prova d'autore):** l'hash falso è stato prodotto **riempiendo un'abbreviazione**, non copiando né ricalcolando l'hash. Chi l'abbia fatto non lo posso stabilire: il turno citato dal mandato non è fra i materiali che ho ricevuto.

## 4. Integrità di tutti i materiali di Gemini ricevuti
Lo script in Appendice A legge le dichiarazioni (file, hash) e le confronta con i byte reali dei file e dei membri degli ZIP. Le dichiarazioni vengono da 12 fonti:
- le continuità V3.1, V3.2 e V3.3;
- i manifest interni agli ZIP (V3, V3.1, V3.2, V3.3 con due copie, architettura V2, controverifica);
- i manifest esterni (pacchetto V2, risposta all'audit).

Esito:
```
Coppie dichiarate verificate: 138 OK, 0 discrepanze, 0 file non disponibili (fra 138 uniche)
```
Gli hash degli ZIP dichiarati nelle continuità, cioè V3.1 `99e8f0bd…`, V3.2 `989dd288…` e V3.3 `6fb9d76e54da…`, coincidono con i file ricevuti.

**Limite:** per gli ZIP V3, architettura V2 e controverifica, i materiali che ho non contengono un hash dichiarato dello ZIP. Se è stato dato in chat, non l'ho verificato qui.

## 5. Controlli sul codice di Gemini disponibile (V3–V3.3, congelato)
- **`dsr` o «deflated» nel codice Python degli ZIP:** nessuna occorrenza.
- **`slippage_fixed`:** nessuna occorrenza.
  - Le uniche assegnazioni di slippage a zero sono in `test_prop_risk_v3_3.py`, righe 630 e 634 (`slippage_tail_alpha=0.0`, `slippage_cap_r=0.0`), dentro `with self.assertRaises(ValueError)`: verificano che quei valori siano **rifiutati**.
  - Gli scenari con slippage (`"Slip"`, `"Balanced_Pareto_Slip"`) hanno parametri non nulli.
  - Nessuna neutralizzazione nascosta.
- **`float`:** il motore Monte Carlo V3.x usa `float`; era noto e già esaminato nelle revisioni V3.2 e V3.3. Non viola nessuna regola: l'obbligo di `Decimal` vale per gli importi monetari di G0 e del journal, non per le simulazioni statistiche.
  - Lo stesso vale per un eventuale `dsr.py`: l'uso di `float` in un Deflated Sharpe Ratio **non è di per sé un errore**.
  - Andrebbe giudicato con un test di tolleranza contro un valore di riferimento pubblicato, da reperire sulla fonte primaria: non lo invento qui.

## 6. Difetto di processo e rimedio
Un hash abbreviato (`6fb9d76e…7638`) è comodo da leggere, ma è anche un invito a «ricostruirlo». Rimedio proposto, da decidere dall'utente; non l'ho applicato ai documenti esistenti:
1. Nei documenti, ogni hash abbreviato deve essere accompagnato dal percorso del file che contiene l'hash completo, per esempio `hash_v33_ricevuti.txt`.
2. Ogni hash citato in un rapporto si copia da un file di output o si ricalcola con `sha256sum`; non si trascrive a memoria né si completa.
3. Nei controlli incrociati si confronta sempre l'hash **completo**: la sola coincidenza di prefisso e suffisso non prova nulla (vedi §3).

## 7. Controlli ostili pronti per il ramo `feat/lab-dati-backtester`
Da eseguire in una cartella temporanea, senza modificare i file di Gemini:
1. Ogni artefatto confrontato con il manifest (lo script dell'Appendice A, esteso al ramo).
2. Suite di Gemini eseguita con `-W error`, più mutation testing sul calcolo dello slippage e dei costi: per esempio slippage ignorato, tetto rimosso, segno invertito.
3. Ogni test che azzera costi o slippage deve avere un gemello con valori non nulli che ne verifichi l'effetto; altrimenti, segnalazione.
4. Importi monetari: `Decimal` o tolleranza dichiarata. Statistiche (per esempio il DSR): confronto con un valore di riferimento pubblicato, con la fonte.
5. Dati: ogni serie in `brain/dati/reali/` con fonte, data di download e hash; dati simulati etichettati come tali.

## Appendice A — `verifica_hash_gemini.py`
Comando: `python3 -I verifica_hash_gemini.py <cartella dei materiali ricevuti>`. SHA-256 dello script, eseguito come riportato sopra: `4726e467c538bf4ed1ee9d6e81a00911266ed9ff47dbd87d1c299e87560cd4e8`.
```python
"""Verifica materiale degli hash dichiarati da Gemini nei materiali ricevuti (sola lettura, ZIP letti in memoria,
nessun codice eseguito). Uso: python3 -I verifica_hash_gemini.py <cartella upload>"""
import hashlib, re, sys, zipfile
from pathlib import Path
U = Path(sys.argv[1]); H = re.compile(r"\b[0-9a-f]{64}\b")
sha = lambda b: hashlib.sha256(b).hexdigest()
reali = {}                                   # nome (relativo e base) -> {hash reali}
def reg(nome, b):
    for k in {nome, nome.split("/")[-1]}:
        reali.setdefault(k, set()).add(sha(b))
for f in sorted(U.iterdir()):
    if f.name.startswith(".") or f.is_dir(): continue
    b = f.read_bytes(); nome = re.sub(r"^[0-9a-f]{8}-", "", f.name); reg(nome, b)
    if f.suffix == ".zip":
        with zipfile.ZipFile(f) as z:
            for i in z.infolist():
                if not i.is_dir():
                    n = i.filename.split("/", 1)[1] if "/" in i.filename and not i.filename.startswith("archivio") else i.filename
                    reg(i.filename, z.read(i)); reg(n, z.read(i))
dichiarati = []                               # (sorgente, file, hash)
def da_testo(sorgente, testo):
    for riga in testo.splitlines():
        hs = H.findall(riga)
        if len(hs) != 1: continue
        v = re.search(r"CONTINUITA_(V[0-9_]+)_PASSAGGIO", sorgente)
        if v and "SHA-256 ZIP" in riga:                 # riga senza nome del file: è lo ZIP della stessa versione
            dichiarati.append((sorgente, f"TRADING_BRAIN_{v.group(1)}_PACKAGE.zip", hs[0])); continue
        m = re.search(r"([\w./-]+\.(?:py|json|md|txt|yaml|zip|sha256))", riga.replace(hs[0], ""))
        if m: dichiarati.append((sorgente, m.group(1), hs[0]))
for f in sorted(U.iterdir()):
    if f.suffix in (".md", ".txt") and ("CONTINUITA" in f.name or "MANIFEST" in f.name):
        da_testo(f.name, f.read_text(encoding="utf-8", errors="replace"))
    if f.suffix == ".zip":
        with zipfile.ZipFile(f) as z:
            for i in z.infolist():
                if re.search(r"(MANIFEST|\.sha256$)", i.filename, re.I) and not i.is_dir():
                    da_testo(f"{f.name}::{i.filename}", z.read(i).decode("utf-8", "replace"))
ok = ko = na = 0; visti = set()
for src, nome, h in dichiarati:
    if (src, nome, h) in visti: continue
    visti.add((src, nome, h)); base = nome.split("/")[-1]
    cand = reali.get(nome) or reali.get(base)
    if cand is None: na += 1; esito = "NON DISPONIBILE"
    elif h in cand: ok += 1; esito = "OK"
    else: ko += 1; esito = "DISCREPANZA (reale: " + ", ".join(sorted(x[:16] + "…" for x in cand)) + ")"
    if esito != "OK": print(f"{esito:16s} {src} -> {nome} {h[:16]}…")
print(f"\nCoppie dichiarate verificate: {ok} OK, {ko} discrepanze, {na} file non disponibili (fra {len(visti)} uniche)")
```
