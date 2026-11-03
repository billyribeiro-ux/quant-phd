"""Re-derive the L07 numbers (Example 1.4, Remark 1.6, Prop 2.2, E2, misconception, E3) with decimal precision.

Run: python -I ledgers/E3/scripts/E3-g-r3/l07_numbers.py
"""
import math
from decimal import Decimal, getcontext

getcontext().prec = 50
D = Decimal


def om(p: Decimal) -> Decimal:
    # eta = 1/2 closed form: sqrt(p) / (1 + 2 sqrt(p(1-p)))
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())


w310 = om(D(3) / D(10))
w35 = om(D(3) / D(5))
w12 = om(D("0.5"))
w01 = om(D("0.01"))
w099 = om(D("0.99"))
w14 = om(D(1) / D(4))
print("omega(3/10) =", f"{w310:.12f}")
print("omega(3/5)  =", f"{w35:.12f}")
print("omega(1/2)  =", f"{w12:.12f}", " 1/(2 sqrt2) =", f"{1 / (2 * D(2).sqrt()):.12f}")
print("2*omega(3/10) =", f"{2 * w310:.12f}")
print("ratio omega(3/10)/omega(3/5) =", f"{w310 / w35:.12f}")
print("threshold alpha=1:", f"{D(1) / (1 + D(1) / 2):.12f}", " alpha=1/2:", f"{D(1) / (1 + 1 / D(2).sqrt()):.12f}")
print("quotient of printed values 0.28579088/0.39125077 =", f"{D('0.28579088') / D('0.39125077'):.12f}")
print("omega(0.01) =", f"{w01:.12f}", " omega(0.99) =", f"{w099:.12f}")
print("omega(1/4) =", f"{w14:.12f}", " 2-sqrt3 =", f"{2 - D(3).sqrt():.12f}")

# Part C (lab): Gamma(A), Gamma(B) at alpha = 1 and alpha = 1/2
gA1 = w310 * (D(50) + D(100))
gB1 = w35 * D(100)
gA_half = w310 * (D(50).sqrt() + D(100).sqrt())
gB_half = w35 * D(100).sqrt()
print("Gamma(A) alpha=1 =", f"{gA1:.8f}", " Gamma(B) alpha=1 =", f"{gB1:.8f}")
print("difference alpha=1 =", f"{gA1 - gB1:.10f}", "-> 4 dp", f"{(gA1 - gB1):.4f}")
print("Gamma(A) alpha=1/2 =", f"{gA_half:.8f}", " Gamma(B) alpha=1/2 =", f"{gB_half:.8f}")

# Misconception: L = 100 w.p. 0.01, 50 w.p. 0.99 at alpha = 1
wv = w01 * 100 + w099 * 50
ev = D("0.01") * 100 + D("0.99") * 50
print("weighted value =", f"{wv:.8f}", " EV =", ev)
print("overweight term (w01-0.01)*100 =", f"{(w01 - D('0.01')) * 100:.6f}")
print("underweight term (0.99-w99)*50 =", f"{(D('0.99') - w099) * 50:.6f}")
print("net =", f"{wv - ev:.6f}")

# Remark 2.3 / E3 identity weighting
print("identity: V(A)=0.3*50+0.3*100 =", D("0.3") * 50 + D("0.3") * 100, " V(B)=0.6*100 =", D("0.6") * 100)

# Lab claim: ordering of grid, sign change and crossing; closed form vs general formula at eta = 1 (E3)
grid = [i / 1000 for i in range(1001)]
gen_gap_eta1 = max(abs(p - math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))) for p in grid)
print("E3 claim: max |omega_1(p) - closed(p)| on 1001 grid =", f"{gen_gap_eta1:.6f}", "(page: 3.13e-1)")

# Observation 1.5 sign change on the grid (float, as the lab)
above = [p > 0 and (p**0.5) / (p**0.5 + (1 - p) ** 0.5) ** 2 > p for p in grid[1:-1]]
print("sign changes on interior =", sum(1 for a, b in zip(above, above[1:]) if a != b))
last = max(p for p, a in zip(grid[1:-1], above) if a)
print("last grid point with omega > p =", f"{last:.3f}")
print("omega(0.278) - 0.278 =", f"{float(om(D('0.278')) - D('0.278')):.8f}", " omega(0.279) - 0.279 =", f"{float(om(D('0.279')) - D('0.279')):.8f}")
