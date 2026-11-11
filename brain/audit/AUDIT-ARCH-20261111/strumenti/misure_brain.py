"""[CLAUDE · AUDIT] Misure automatiche sullo stato del Brain (sola lettura).
Uso: python3 -I misure_brain.py <cartella brain> > misure.txt"""
import os, re, sys, collections, hashlib
B = sys.argv[1]
def md(p): return open(p, encoding="utf8").read()

print("== 1. File per area")
cnt = collections.Counter()
for root, _, files in os.walk(B):
    if "/originale" in root: continue
    for f in files: cnt[os.path.relpath(root, B).split(os.sep)[0]] += 1
for k, v in sorted(cnt.items()): print(f"  {k:16s} {v}")

print("\n== 2. Lezioni nuove: conformità al modello a 20 sezioni, fonti, etichette")
SEZ = ["Titolo","Obiettivi","Prerequisiti","Definizione","Spiegazione","Fondamenti","Formule","Esempi numerici",
       "Esempi reali","Applicazione","Connessioni","Errori","Limiti","Evidenze","Fonti","Sintesi","Flashcard",
       "Esercizi","Domande di ragionamento","Checklist"]
for f in sorted(os.listdir(f"{B}/moduli/m02-macro")):
    if not re.match(r"L2\.\d", f): continue
    t = md(f"{B}/moduli/m02-macro/{f}")
    heads = re.findall(r"^## (\d+)\. ", t, re.M)
    stato = re.search(r"^stato: (\S+)", t, re.M).group(1)
    fonti = t[t.find("## 15."):t.find("## 16.")]
    v = len(re.findall(r"\|\s*V\s*\|", fonti)); vs = len(re.findall(r"V-sec", fonti)); c = len(re.findall(r"\|\s*C[ (|]", fonti))
    etich = {e: len(re.findall(re.escape(e), t)) for e in ("[VERIFICATO]","[IN VERIFICA]","[IPOTESI]","[ESEMPIO]","[ESERCIZIO]","[SIMULATO]","[REALE]")}
    flash = t[t.find("## 17."):t.find("## 18.")].count("\n|") - 2
    eser = len(re.findall(r"^\d\. ", t[t.find("## 18."):t.find("## 19.")], re.M))
    print(f"  {f[:40]:40s} sezioni {len(heads):2d}/20 · stato {stato:12s} · fonti V {v} V-sec {vs} C {c} · flashcard {flash} · esercizi {eser} · etichette {sum(etich.values())} {'' if sum(etich.values()) else '(nessuna)'}")

print("\n== 3. Manuale v1: lezioni per modulo")
t = md(f"{B}/originale/manuale-v1.txt")
print("  lezioni:", len(re.findall(r"^Lezione \d+", t, re.M)), "· cancelli:", t.count("Cancello per il Modulo"))

print("\n== 4. Bibliografia: stato delle voci e duplicati")
t = md(f"{B}/bibliografia/BIBLIOGRAFIA.md")
rows = [r for r in t.split("\n") if r.startswith("| ") and not r.startswith("| ---") and not re.match(r"\| (Autori|Fonte|Corso) ", r)]
st = collections.Counter()
for r in rows:
    last = r.rstrip(" |").split("|")[-1].strip()
    st[last.split(" ")[0]] += 1
print("  voci:", len(rows), "· stato:", dict(st.most_common(8)))
tit = collections.Counter()
for r in rows:
    cells = [c.strip() for c in r.split("|")]
    if len(cells) > 3: tit[re.sub(r"\W+", " ", cells[2].lower())[:60]] += 1
d = [k for k, v in tit.items() if v > 1 and k]
print("  titoli ripetuti:", d if d else "nessuno")

print("\n== 5. Riferimenti a stati e numeri che possono essere superati")
for p, pat in [("CONTINUITA.md", r"SVILUPPO SOSPESO|in attesa"), ("collaborazione/LOCK.md", r"SOSPESO|congelat"),
               ("governance/REGISTRO-CONOSCENZE.md", r"Aggiornato: .*"), ("collaborazione/HANDOFF-GEMINI.md", r"Versione \S+"),
               ("README.md", r"L2\.1–L2\.\d"), ("audit/03-MATRICE-LACUNE.md", r"in sviluppo")]:
    tt = md(f"{B}/{p}"); m = re.findall(pat, tt)
    print(f"  {p:38s} {len(m)} occorrenze: {m[:3]}")

print("\n== 6. Termini richiesti dall'incarico presenti nel Brain")
for term in ("Strategy Discovery Lab", "Trading Guardian", "Guardian", "rulebook", "walk-forward", "point-in-time", "CPCV", "Deflated Sharpe", "kill switch"):
    hits = []
    for root, _, files in os.walk(B):
        if "/originale" in root or "AUDIT-ARCH" in root: continue
        for f in files:
            if f.endswith(".md") and term.lower() in md(os.path.join(root, f)).lower(): hits.append(os.path.relpath(os.path.join(root, f), B))
    print(f"  {term:24s} {len(hits)} file: {hits[:4]}")

print("\n== 7. Coerenza manifest della revisione (atteso: superato dopo l'errata)")
D = f"{B}/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261111-01-V2"
ok = bad = 0
for line in open(f"{D}/MANIFEST_REVISIONE_CLAUDE.sha256"):
    h, f = line.split(None, 1); f = f.strip()
    p = os.path.join(D, f)
    if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == h: ok += 1
    else: bad += 1; print("   diverso o assente:", f)
print(f"  OK {ok} · diversi {bad}")
