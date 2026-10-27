"""Round-2: exact random-state checks of L03 propositions, plus the printed table entries."""
import contextlib
import io
import random
import runpy
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(root / "tests/labs/AC2/lab-AC2-L03-1.py"), run_name="twin")
st = g["standardize"](g["make_filer"]())
for e, row in st.items():
    print(e, {k: round(v / 1e6, 1) for k, v in row.items() if k in ("equity", "long_term_debt", "cash", "operating_income", "net_income")})

rng = random.Random(7)
def rq():
    return F(rng.randint(-500, 500), rng.randint(1, 40))

# Proposition 2.2: ROIC(t2)/ROIC(t1) = (1-t2)/(1-t1) for random positive-average states
bad = 0
for _ in range(20000):
    oi = rq() * 100
    avg = F(rng.randint(1, 1000), rng.randint(1, 50))
    t1 = F(rng.randint(0, 99), 100); t2 = F(rng.randint(0, 99), 100)
    r1 = oi * (1 - t1) / avg; r2 = oi * (1 - t2) / avg
    if r1 != 0 and r2 / r1 != (1 - t2) / (1 - t1):
        bad += 1
print("Prop 2.2 counterexamples in 20000:", bad)

# Proposition 3.2: average of sum
bad = 0
for _ in range(20000):
    E0, E1, D0, D1, C0, C1 = (rq() for _ in range(6))
    lhs = ((E1 + D1 - C1) + (E0 + D0 - C0)) / 2
    rhs = (E1 + E0) / 2 + (D1 + D0) / 2 - (C1 + C0) / 2
    bad += lhs != rhs
print("Prop 3.2 failures in 20000:", bad)

# Remark 2.3: 1 - NI/OI = 1 - (1 - I/OI)(1 - tau) when NI=(OI-I)(1-tau)
bad = 0
for _ in range(20000):
    OI = F(rng.randint(1, 999), 7); I = F(rng.randint(0, 99), 3); tau = F(rng.randint(0, 99), 100)
    NI = (OI - I) * (1 - tau)
    bad += (1 - NI / OI) != 1 - (1 - I / OI) * (1 - tau)
print("Remark 2.3 algebra failures:", bad)

# Proposition 3.4 as printed: 'If IC_t > IC_{t-1} and NOPAT_t > 0, ROIC on average > ROIC on year-end. If IC_t < IC_{t-1} the inequality reverses.'
def compare(ict, icp, nopat):
    avg = (ict + icp) / 2
    return nopat / avg, nopat / ict if ict != 0 else None
# case 1: rising, positive
print("rising case, random:", end=" ")
bad = 0; n = 0
for _ in range(20000):
    icp = F(rng.randint(1, 999)); ict = icp + F(rng.randint(1, 999))
    N = F(rng.randint(1, 999))
    a, y = compare(ict, icp, N)
    n += 1; bad += not (a > y)
print("violations", bad, "of", n)
# case 2: falling, the claim 'the inequality reverses' (ROIC_avg < ROIC_ye)
print("falling case, positive year-end IC: ", end="")
bad = 0; n = 0; ex = None
for _ in range(20000):
    icp = F(rng.randint(2, 999)); ict = F(rng.randint(1, int(icp) - 1)) if int(icp) > 1 else F(1, 2)
    N = F(rng.randint(1, 999))
    a, y = compare(ict, icp, N)
    n += 1; bad += not (a < y)
print("violations", bad, "of", n)
print("falling case, non-positive year-end IC (ict <= 0 < avg):", end=" ")
ict, icp, N = F(-5), F(10), F(1)
a, _ = compare(ict, icp, N)
print("avg ROIC", a, "year-end ROIC", N / ict, "avg > year-end:", a > N / ict)
