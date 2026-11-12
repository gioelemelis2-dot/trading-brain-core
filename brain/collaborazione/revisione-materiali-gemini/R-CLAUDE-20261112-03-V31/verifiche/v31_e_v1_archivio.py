"""[CLAUDE · VERIFICA V3.1] (E) Motore V1 d'archivio: confronto dei suoi risultati (JSON V1, riprodotto byte per byte)
con il calcolo ESATTO in modalità V1 (target valido solo da min_days) e V2/V3.1. Chiude C-11 sul piano quantitativo."""
import sys, json, math; sys.path.insert(0, sys.argv[1])
from c1_esatto_challenge import challenge
d = json.load(open(sys.argv[2])); N = 10000
scen = {"A_Asymmetric_Swing": (0.35, 2.5), "B_Balanced_Swing": (0.40, 2.0), "C_High_WinRate_Scalp": (0.60, 1.0), "Z_Null_Control": (0.50, 1.0)}
zs = []
for nome, (p, rr) in scen.items():
    for r in ("0.0025", "0.0050", "0.0075", "0.0100", "0.0150", "0.0200"):
        v = d["sensitivity"][nome][r]["pass"]["rate"]
        ex1 = challenge(p, float(r), rr, 0.05, 2, 60, "v1")["pass"]; ex2 = challenge(p, float(r), rr, 0.05, 2, 60, "v2")["pass"]
        z = (v - ex1) / math.sqrt(max(ex1*(1-ex1), 1e-12)/N); zs.append(z)
        print(f"{nome:22s} {r}: V1 json {v:.4f} · esatto V1 {ex1:.4f} (z {z:+.2f}) · esatto V2/V3.1 {ex2:.4f} · bug min_days {100*(ex2-ex1):+.2f} punti")
print(f"max |z| sul confronto V1 json / esatto V1: {max(abs(x) for x in zs):.2f} su {len(zs)} configurazioni")
print("Intraday 1% (B, 6 trade/giorno, 25 giorni): esatto V1 {:.4f}, esatto V2 {:.4f}, differenza {:+.2f} punti".format(
    challenge(0.40, 0.01, 2.0, 0.05, 6, 25, "v1")["pass"], challenge(0.40, 0.01, 2.0, 0.05, 6, 25, "v2")["pass"],
    100*(challenge(0.40, 0.01, 2.0, 0.05, 6, 25, "v2")["pass"] - challenge(0.40, 0.01, 2.0, 0.05, 6, 25, "v1")["pass"])))
