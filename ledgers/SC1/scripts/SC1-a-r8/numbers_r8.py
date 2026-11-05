# Round 8 SC1-a number re-derivation (L02 E3 unrounded value; L03 standard-error gaps and z-values).
import math, random, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-a/tests/labs/SC1")
# L02: replicate the twin's RNG draw order exactly
SEED = 20260101
LEVELS = 8
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
sup1 = max(abs(c) for c in coeffs[0]) * 2 ** (-(1 + 1) / 2)
print("L02 level-1 unrounded sup:", repr(sup1), "rounded6:", f"{sup1:.6f}")
print("L02 |xi_11| unrounded:", repr(abs(coeffs[0][0])), "twice sup:", repr(2*sup1), "round6 of 2*sup:", f"{2*sup1:.6f}")
print("L02 bound lambda_1/2:", math.sqrt(4*math.log(2))/2, "sqrt(4log2):", math.sqrt(4*math.log(2)))
# L03: standard-error gaps from the printed 4-decimal values
rows = {
 1: [(1,0.0718),(2,0.0538),(4,0.0373),(8,0.0249),(16,0.0174),(32,0.0131),(64,0.0092),(128,0.0063)],
 2: [(1,0.1601),(2,0.0934),(4,0.0772),(8,0.0475),(16,0.0364),(32,0.0256),(64,0.0190),(128,0.0125)],
}
gaps = []
for H, lst in rows.items():
    for N, se in lst:
        pop = H*math.sqrt(2/N)/20
        g = se/pop - 1
        gaps.append((abs(g), H, N, se, pop, g))
gaps.sort(reverse=True)
for x in gaps[:5]:
    print("gap |%.4f| H=%d N=%d printed=%.4f pop=%.6f signed=%+.4f%%" % (x[0], x[1], x[2], x[3], x[4], 100*x[5]))
print("H=2 N=128 pop exact:", 2*math.sqrt(2/128)/20)
# unrounded L03 sample se for H=2 N=128 cannot be recovered from output; report bounds implied by 4-dec print
for lo, hi in [(0.12745,0.12755)]:
    pass
