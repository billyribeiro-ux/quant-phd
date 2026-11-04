"""Independent re-derivation of the numbers printed or quoted in SC1 slice pages L01-L03 and the hub.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r4/recompute.py
"""
import math
import random
from fractions import Fraction

print("== L02 level-1 coefficient and bounds (seed 20260101, same draw order as the twin)")
rng = random.Random(20260101)
xi0 = rng.gauss(0.0, 1.0)
xi11 = rng.gauss(0.0, 1.0)
print(f"xi0 = {xi0!r}")
print(f"xi_1,1 = {xi11!r}")
sup1 = abs(xi11) * 2 ** (-1)
print(f"level-1 observed sup (unrounded) = {sup1!r} -> 6dp {sup1:.6f}")
print(f"twice the unrounded sup = {2 * sup1:.7f}; 6dp of |xi_1,1| = {abs(xi11):.6f}; 2 * printed(0.116589) = {2 * 0.116589:.6f}")
bound1 = math.sqrt(4 * math.log(2)) * 2 ** (-1)
print(f"lambda_1 = {math.sqrt(4 * math.log(2)):.6f}; bound_1 = lambda_1/2 = {bound1:.6f}")

print("== L02 grid sup |S_8 - S_4| and sum of bounds 5..8")
LEVELS = 8


def hat(m, j, t):
    return max(0.0, 1.0 - 2.0**m * abs(t - (2 * j - 1) / 2.0**m))


rng = random.Random(20260101)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]


def S(levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total


grid = [i / 2**10 for i in range(2**10 + 1)]
gsup = max(abs(S(8, t) - S(4, t)) for t in grid)
bsum = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9))
print(f"grid sup |S_8-S_4| = {gsup:.6f}; sum bounds 5..8 = {bsum:.6f}")

print("== L02 dyadic case count and formula")
total = sum((2**n + 1) * (LEVELS - n + 1) for n in range(5))
print(f"cases = {total}; per depth {[(2**n + 1, LEVELS - n + 1) for n in range(5)]}")

print("== L02 Lemma 2.3 variance bookkeeping (exact)")
for n in range(0, 6):
    c2 = Fraction(1, 2 ** (n + 2))
    varU = Fraction(1, 4) * Fraction(1, 2**n) + c2
    varUV_cov = Fraction(1, 4) * Fraction(1, 2**n) - c2
    assert varU == Fraction(1, 2 ** (n + 1)) and varUV_cov == 0
print("Var(U_j) = 2^-(n+1) and Cov(U_j,V_j) = 0 hold exactly for n=0..5")

print("== L02 Lemma 2.2(d) sanity and Prop 2.4 tail sums")
print("sum_{m>=1} m r^m with r=2^-1/2 =", sum(m * 2 ** (-m / 2) for m in range(1, 200)), " r/(1-r)^2 =",
      (2**-0.5) / (1 - 2**-0.5) ** 2)

print("== L03 gap table: printed sample se vs H*sqrt(2/N)/20 (printed 4dp values from the lab output)")
printed = {
    (1, 1): 0.0718, (1, 2): 0.0538, (1, 4): 0.0373, (1, 8): 0.0249, (1, 16): 0.0174, (1, 32): 0.0131,
    (1, 64): 0.0092, (1, 128): 0.0063,
    (2, 1): 0.1601, (2, 2): 0.0934, (2, 4): 0.0772, (2, 8): 0.0475, (2, 16): 0.0364, (2, 32): 0.0256,
    (2, 64): 0.0190, (2, 128): 0.0125,
}
gaps = {}
for (H, N), se in printed.items():
    pop = H * math.sqrt(2 / N) / 20
    gaps[(H, N)] = se / pop - 1
worst = max(gaps, key=lambda k: abs(gaps[k]))
print(f"largest |gap| at H={worst[0]}, N={worst[1]}: {100 * gaps[worst]:.2f}% ; population at H=2,N=1 = {2 * math.sqrt(2) / 20:.6f}")
print("H=1,N=1 population:", round(math.sqrt(2) / 20, 4), " H=2,N=128 population:", 2 * math.sqrt(2 / 128) / 20)

print("== L03 exact t-squared sums and closed forms")
for H in (Fraction(1), Fraction(2)):
    for N in (1, 2, 4, 8, 16, 32, 64, 128):
        pts = [H * j / N for j in range(N + 1)]
        s = sum(((pts[i + 1] ** 2 - pts[i] ** 2) ** 2 for i in range(N)), Fraction(0))
        cf = H**4 * (4 * N * N - 1) / (3 * N**3)
        assert s == cf, (H, N)
print("exact sums equal H^4(4N^2-1)/(3N^3) for H in {1,2}, N in 1..128 (all 16 levels)")
print("H=2,N=8 exact:", float(Fraction(16) * 255 / 1536), "H=1,N=2:", float(Fraction(15, 24)))
print("E|Z| check: 2/sqrt(2 pi) =", 2 / math.sqrt(2 * math.pi), " sqrt(2/pi) =", math.sqrt(2 / math.pi))
print("L03 canon-break: N * sqrt(2/pi) * sqrt(t/N) at t=1 for N=1,4,16:",
      [round(N * math.sqrt(2 / math.pi) * math.sqrt(1 / N), 6) for N in (1, 4, 16)])

print("== L01 exact numbers (Fraction)")
w = Fraction(3, 4) / 16
print("pieces of [0,3/4] at depth 4:", w, " 16*w =", 16 * w)
print("sd of increment over h=1/4:", Fraction(1, 4) ** Fraction(1, 2), " h=1/100 sd:", Fraction(1, 100) ** Fraction(1, 2))
print("ratio 1/sqrt(1/100):", 1 / math.sqrt(1 / 100))
print("Cov(B_1/2,B_1)=min:", min(Fraction(1, 2), Fraction(1)))
print("Var(3B_1 - B_2) = 9*1 + 2 - 6*min(1,2) =", 9 * 1 + 2 - 6 * min(1, 2))
print("E[B_3^2] = Var(B_3) =", 3)
print("M1 Cov(B_{1/3},B_{2/3}) =", min(Fraction(1, 3), Fraction(2, 3)), " Var(B_{2/3}-B_{1/3}) =", Fraction(2, 3) - Fraction(1, 3))
print("E1 pieces 3/64; 16*3/64 =", 16 * Fraction(3, 64))
print("E2 2*1/8 =", 2 * Fraction(1, 8), " min(1/4,5/8)=", min(Fraction(1, 4), Fraction(5, 8)))
print("ratio 10 check: (1/100)^-0.5 / (1/100)^0 ... h=1/100 sd/h =", (1 / 10) / (1 / 100))
print("L01 quiz 2: P(B_{1/2}) ... Cov =", min(Fraction(1, 2), Fraction(1)))
print("Lab L01 81 ordered pairs of 9 grid times:", 9 * 9, "; depths x times:", 3 * 5)

print("== hub placement arithmetic (nine items, mastery bar 0.8)")
print("7/9 =", round(100 * 7 / 9, 1), "percent; 8/9 =", round(100 * 8 / 9, 1), "percent; 8/9 >= 0.8:", 8 / 9 >= 0.8,
      "; 7/9 >= 0.8:", 7 / 9 >= 0.8)
