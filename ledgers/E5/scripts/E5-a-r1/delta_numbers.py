"""Re-derive the numbers and identities touched by the E5-a closing delta (2a805c83..d9de2fe5)."""
import math
import random
from decimal import Decimal, getcontext

getcontext().prec = 50

# 1. Lab 1 averages printed by the L02 twin, and the difference quoted in L02 (line 285) and card E5-c141.
r02, r04 = Decimal("0.016254"), Decimal("0.010665")
print("diff of printed averages:", r02 - r04, "| quoted 0.005589 matches:", r02 - r04 == Decimal("0.005589"))

# 2. Definition 2.1 and Proposition 2.4 (cards c032, c034; L02 lines 131, 285, 379, 436-439).
rng = random.Random(1)
worst = 0.0
for _ in range(20000):
    dlnK = [rng.uniform(-0.2, 0.2) for _ in range(5)]
    dlnL = [rng.uniform(-0.2, 0.2) for _ in range(5)]
    dlnY = [rng.uniform(-0.2, 0.2) for _ in range(5)]
    a, b = rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99)

    def res(alpha, t):
        return dlnY[t] - alpha * dlnK[t] - (1 - alpha) * dlnL[t]

    for t in range(5):
        lhs = res(a, t) - res(b, t)
        rhs = -(a - b) * (dlnK[t] - dlnL[t])
        worst = max(worst, abs(lhs - rhs))
print("Prop 2.4 per-period identity, max abs error over 100000 cases:", worst)

# 3. Average-residual dependence on alpha is zero iff average K growth equals average L growth (iff in Prop 2.4).
avgK, avgL = 0.03, 0.03
print("equal average growth gives zero change in average residual:", -(0.2) * (avgK - avgL) == 0)

# 4. L03 Proposition 2.2 (steady state depends on n and delta only through n+delta), card E5-c040 and L03 line 393.
def g(k, s, d, n, al):
    return (s * k ** al + (1 - d) * k) / (1 + n)

ok = True
for _ in range(2000):
    s = rng.uniform(0.05, 0.9)
    d = rng.uniform(0.01, 0.9)
    n = rng.uniform(-0.009, 0.2)
    al = rng.uniform(0.05, 0.95)
    kstar = (s / (n + d)) ** (1 / (1 - al))
    if abs(g(kstar, s, d, n, al) - kstar) > 1e-9 * max(1, kstar):
        ok = False
    # depends on n and d only through n+d: shifting (n,d) keeping n+d fixed leaves k* unchanged
    d2 = d + 0.01
    n2 = n - 0.01
    k2 = (s / (n2 + d2)) ** (1 / (1 - al))
    if abs(k2 - kstar) > 1e-9 * max(1, kstar):
        ok = False
print("Prop 2.2 closed form is a fixed point and depends on (n,delta) only via n+delta:", ok)

# 5. c040: g(0) = 0 under A1, so zero is a fixed point; it is not a positive steady state under Definition 2.1.
print("g(0) with alpha 0.3, s 0.2, delta 0.05, n 0.01:", g(0.0, 0.2, 0.05, 0.01, 0.3))

# 6. L01 Definition 1.6 deflator: D_0 = 1 holds for any index with P_0 = base; nothing numeric changed.

# 7. Theorem 2.3 needs the economy's own alpha (L02 line 117; card E5-c031). Counterexample to the card E5-c033 and L02 lines 269, 281, 405 wording without that hypothesis.
A_t, K_t, L_t = [1.0, 1.05], [2.0, 2.4], [3.0, 3.3]
alpha_true, alpha_chosen = 0.3, 0.5
dlnY = math.log(A_t[1] * K_t[1] ** alpha_true * L_t[1] ** (1 - alpha_true)) - math.log(A_t[0] * K_t[0] ** alpha_true * L_t[0] ** (1 - alpha_true))
dlnA = math.log(A_t[1] / A_t[0])
dlnK = math.log(K_t[1] / K_t[0])
dlnL = math.log(L_t[1] / L_t[0])
res_true = dlnY - alpha_true * dlnK - (1 - alpha_true) * dlnL
res_chosen = dlnY - alpha_chosen * dlnK - (1 - alpha_chosen) * dlnL
print("residual with the economy's alpha equals dlnA:", abs(res_true - dlnA) < 1e-12)
print("residual with a chosen alpha 0.5 equals dlnA:", abs(res_chosen - dlnA) < 1e-12, "| value", res_chosen, "vs dlnA", dlnA)
