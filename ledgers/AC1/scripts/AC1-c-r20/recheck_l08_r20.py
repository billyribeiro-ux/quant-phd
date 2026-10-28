# Independent recomputation of the L08 Section 2 / why-it-matters exactness claims (cents, integer arithmetic).
import random
from fractions import Fraction as F
rng = random.Random(7)
bad = []
trials = 0
for _ in range(3000):
    L = rng.randint(1, 6)
    C = rng.randint(1, 500) * 10_000
    if (C // L) * L != C or (C // L) % 100 != 0:  # Def 1.1: C/L multiple of 100 cents
        continue
    # tax percentages: integers summing to 100 (non-negative here)
    cuts = sorted(rng.sample(range(0, 101), L - 1))
    p = [b - a for a, b in zip([0] + cuts, cuts + [100])]
    b = C // L
    tau = [C * pt // 100 for pt in p]
    assert all(t % 100 == 0 for t in tau) and b % 100 == 0 and sum(tau) == C
    r = rng.randint(0, 60)
    K = 0; dtl_prev = 0
    for t in range(L):
        d = tau[t] - b
        K += d
        dtl = F(r * K, 100)
        de = dtl - dtl_prev
        dtl_prev = dtl
        trials += 1
        # DE and DTL integral for any P (no P condition)
        if de.denominator != 1 or dtl.denominator != 1:
            bad.append(('DE/DTL', C, L, r, t))
    # CT and TE for random P_t
    for P in [rng.randrange(0, 9_000_001) for _ in range(3)] + [rng.randrange(0, 900_001) * 100]:
        for t in range(L):
            pass
        # CT_t integral iff r*P multiple of 100 (taxable difference multiple of 100)
        Pm = P
        ct = F(r * (Pm - (tau[0] - b)), 100)
        integral = ct.denominator == 1
        if integral != ((r * Pm) % 100 == 0):
            bad.append(('CT iff', P, r))
        if Pm % 100 == 0 and not integral:
            bad.append(('P100 sufficient fails', P, r))
print('trials', trials, 'violations', bad[:5], len(bad))
# Concrete counter-check of the sentence "a multiple of 100 cents is sufficient": P=50,000 r=21, and a P not multiple of 100 with r=25
print('P=50001 r=21 CT', F(21*(50001-20000),100), 'r=100 P=50001 CT integral?', F(100*(50001-20000),100).denominator==1)
