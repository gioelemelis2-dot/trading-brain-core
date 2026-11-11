"""[CLAUDE · VERIFICA] Catena di Markov a due stati usata da prop_risk_engine_v2.py.
(1) algebra della stazionarietà; (2) comportamento del ramo di codice di Gemini, replicato riga per riga
    (righe 83-94 del motore) con un generatore dichiarato; (3) casi limite."""
import random, statistics, math

def p_l_dopo_w(p, pll):                 # formula del motore (riga 88), senza clamp
    q = 1 - p
    return (q - pll * q) / p

def sequenza(p, pll, n, seme, stato_iniziale_perdita=False):
    rng = random.Random(seme); last_loss = stato_iniziale_perdita; out = []
    for _ in range(n):
        prob_loss = pll if last_loss else max(0.0, min(1.0, p_l_dopo_w(p, pll)))
        is_win = rng.random() >= prob_loss
        last_loss = not is_win; out.append(0 if last_loss else 1)
    return out

def stat(seq):
    p = statistics.fmean(seq)
    ww = sum(1 for a, b in zip(seq, seq[1:]) if a == 1 and b == 1) / max(1, sum(seq[:-1]))
    m = p; num = sum((a - m) * (b - m) for a, b in zip(seq, seq[1:])); den = sum((a - m) ** 2 for a in seq)
    runs, cur = [], 1
    for a, b in zip(seq, seq[1:]):
        if a == b: cur += 1
        else: runs.append((a, cur)); cur = 1
    runs.append((seq[-1], cur))
    lw = statistics.fmean([c for a, c in runs if a == 1]); ll = statistics.fmean([c for a, c in runs if a == 0])
    return p, ww, num / den, lw, ll

print("(1) Algebra: p=0.40, P(L|L)=0.80")
plw = p_l_dopo_w(0.40, 0.80); print(f"   P(L|W) = {plw:.4f} -> P(W|W) = {1-plw:.4f}; rho1 = P(L|L)-P(L|W) = {0.80-plw:.4f}")
print(f"   durata media serie vincenti 1/(1-P(W|W)) = {1/plw:.3f}; serie perdenti 1/(1-P(L|L)) = {1/0.2:.3f}")
p, ww, rho, lw, ll = stat(sequenza(0.40, 0.80, 1_000_000, 2026))
print(f"(2) [SIMULATO] 1.000.000 esiti col ramo di Gemini: WR {p:.4f}, P(W|W) {ww:.4f}, rho1 {rho:.4f}, serie W {lw:.2f}, serie L {ll:.2f}")
print("(3a) Stato iniziale: il motore parte da last_outcome_was_loss=False (come dopo una VINCITA)")
first = [sequenza(0.40, 0.80, 1, s)[0] for s in range(200_000)]
print(f"   [SIMULATO] P(primo trade vincente) = {statistics.fmean(first):.4f} (stazionaria 0.40; teorica 1-P(L|W) = {1-plw:.2f})")
for k in (1, 3, 5, 10):
    # probabilità esatta di vincita al trade k partendo da W: p_k = p + (1-p0... ) lambda^(k-1)
    lam = 0.80 - plw; pk = 0.40 + (0.70 - 0.40) * lam ** (k - 1)
    print(f"   P(vincita al trade {k:2d} di ogni fase) = {pk:.4f}")
print("(3b) Vincolo di ammissibilità: P(L|W) <= 1  <=>  P(L|L) >= 1 - p/(1-p)")
for p_, pll in [(0.40, 0.80), (0.40, 0.40), (0.40, 0.30), (0.40, 0.20), (0.60, 0.10)]:
    raw = p_l_dopo_w(p_, pll); seq = sequenza(p_, pll, 400_000, 7)
    print(f"   p={p_:.2f} P(L|L)={pll:.2f}: P(L|W) calcolata {raw:.3f}{' -> TAGLIATA a 1' if raw>1 else ''}; "
          f"[SIMULATO] WR effettivo {statistics.fmean(seq):.4f} (atteso {p_:.2f}); soglia minima P(L|L) = {max(0,1-p_/(1-p_)):.3f}")
