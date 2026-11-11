"""[CLAUDE · VERIFICA] (a) V1 ricostruita vs V2, esatto; (b) sensibilità al limite di giorni per fase."""
import sys; sys.path.insert(0, sys.argv[1])
from c1_esatto_challenge import challenge, fase
tab_gemini_v1 = {(0.005,2,60): (0.4903,0.0463,0.0), (0.01,2,60): (0.6726,0.2787,0.0),
                 (0.005,6,25): (0.6048,0.0587,0.0), (0.01,6,25): (0.3725,0.0565,0.5696)}
print("(a) V1 (ricostruita) e V2: valori ESATTI · confronto con la tabella V1 dichiarata da Gemini")
print(f"{'config':16s} {'V2 pass':>8s} {'V1 pass':>8s} {'diff':>7s} | {'V1 Gemini pass':>14s} {'z vs V1 esatto':>14s} | V1 DL esatto / Gemini")
import math
for (r,tpd,md),(gp,gml,gdl) in tab_gemini_v1.items():
    v2 = challenge(0.40, r, 2.0, 0.05, tpd, md, "v2"); v1 = challenge(0.40, r, 2.0, 0.05, tpd, md, "v1")
    z = (gp - v1["pass"]) / math.sqrt(v1["pass"]*(1-v1["pass"])/10000)
    print(f"r={r:.3f} tpd={tpd} {v2['pass']:8.4f} {v1['pass']:8.4f} {v2['pass']-v1['pass']:+7.4f} | {gp:14.4f} {z:14.2f} | {v1['daily_loss']:.4f} / {gdl:.4f}")
    if (r,tpd)==(0.01,6):
        print(f"   fallimenti attesi in più per V1 su 10.000 sfide: {10000*(v2['pass']-v1['pass']):.0f} (Gemini dichiara 470)")
        # sola fase 1 e sola fase 2
        for t in (0.10,0.05):
            a=fase(0.40,r,2.0,0.05,tpd,md,t,versione='v2')['pass']; b=fase(0.40,r,2.0,0.05,tpd,md,t,versione='v1')['pass']
            print(f"   fase con target {t:.2f}: V2 {a:.4f}  V1 {b:.4f}  diff {a-b:+.4f}")
print()
print("(b) Probabilità di superare le DUE fasi al variare del limite di giorni per fase (V2, esatto)")
print(f"{'config':18s}" + "".join(f"{d:>9d}" for d in (25,60,120,250,1000)))
for r,tpd in [(0.0025,2),(0.005,2),(0.0075,2),(0.01,2),(0.005,6),(0.01,6)]:
    print(f"r={r:.4f} tpd={tpd}  " + "".join(f"{challenge(0.40,r,2.0,0.05,tpd,d)['pass']:9.4f}" for d in (25,60,120,250,1000)))
