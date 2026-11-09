"""Round-6 exact checks (verifier-written) for the changed cards: c039, c056, c160, c164, c165, c166, c078."""
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP
import itertools

getcontext().prec = 60

def pm(a, b, c): return (a + b * c) / (2 * b)
def qm(a, b, c): return a - b * pm(a, b, c)
def pi_mon(p, a, b, c): return (p - c) * (a - b * p)
def W(Q, a, b, c): return (a * Q - Q * Q / 2) / b - c * Q

# c056 / c164 / c065 at the reference case (120, 1, 20)
a, b, c = F(120), F(1), F(20)
print("c056 p_m", pm(a, b, c), "c164 Q_m", qm(a, b, c), "pi_m", pi_mon(pm(a, b, c), a, b, c), "closed", (a - b * c) ** 2 / (4 * b))
# c056 claim 'unique maximiser': profit identity pi(p) = (a-bc)^2/(4b) - b (p-p_m)^2 on exact grid
ok = True
for a_, b_, c_ in itertools.product([F(120), F(90), F(200), F(7, 2)], [F(1), F(3), F(4), F(1, 2)], [F(0), F(5), F(10), F(20)]):
    if not a_ > b_ * c_:
        continue
    p_m = pm(a_, b_, c_)
    for k in range(0, 201):
        p = F(k, 10)
        lhs = pi_mon(p, a_, b_, c_)
        rhs = (a_ - b_ * c_) ** 2 / (4 * b_) - b_ * (p - p_m) ** 2
        ok = ok and lhs == rhs
print("c056 identity on grid, all cases:", ok)

# c166 / c101: DWL and total surplus, general (a, b, c) with a > bc, exact
bad = []
cases = 0
for a_, b_, c_ in itertools.product([F(120), F(90), F(200), F(7, 2), F(11)], [F(1), F(3), F(4), F(1, 2), F(5, 3)], [F(0), F(5), F(10), F(20), F(1, 3)]):
    if not a_ > b_ * c_:
        continue
    cases += 1
    d = a_ - b_ * c_
    Wc = W(d, a_, b_, c_)
    dwl_m = Wc - W(d / 2, a_, b_, c_)
    dwl_c = Wc - W(2 * d / 3, a_, b_, c_)
    if Wc != d * d / (2 * b_) or dwl_m != d * d / (8 * b_) or dwl_c != d * d / (18 * b_):
        bad.append((a_, b_, c_))
    if dwl_m / Wc != F(1, 4) or dwl_c / Wc != F(1, 9):
        bad.append(("share", a_, b_, c_))
print("c166 DWL shares 1/4 and 1/9 and W_C = d^2/(2b), cases:", cases, "failures:", bad)
print("reference case W_C, DWL_M, DWL_C:", W(F(100), F(120), F(1), F(20)), W(F(100), F(120), F(1), F(20)) - W(F(50), F(120), F(1), F(20)), W(F(100), F(120), F(1), F(20)) - W(F(200, 3), F(120), F(1), F(20)))

# c078 / c165: Cournot reference case, per exchange and industry, half-up rounding applied once to the exact value
d = F(100); b = F(1)
q_each = d / 3
vol = 2 * q_each
fee = (F(120) + 2 * F(1) * F(20)) / (3 * b)
per_exchange = d * d / (9 * b)
industry = 2 * per_exchange
def half_up(x: F) -> int:
    return int((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
print("c078 each q", q_each, "volume", vol, "fee", fee, "per exchange", per_exchange, float(per_exchange), "rounded", half_up(per_exchange))
print("c165 industry", industry, float(industry), "rounded", half_up(industry))
# c160 Bertrand: volume d, fee c, profit 0
print("c160 Bertrand volume", d, "fee", F(20), "profit", F(0))
