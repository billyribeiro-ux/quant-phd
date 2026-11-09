"""Verifier round 5: independent exact recomputation of the L07 numbers (own script, Fractions and math only)."""
import math
from fractions import Fraction as F

def half_up(x):
    return math.floor(x + F(1, 2))

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name)

for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5)]:
    d = F(a - b * c)
    CS = lambda Q: Q * Q / (2 * b)
    PS = lambda Q, fee: (fee - c) * Q
    W = lambda Q: CS(Q) + (d - Q) * Q / b          # Theorem 1.2 closed form
    Ws = W(d)
    cases = {
        "mono": (d / 2, F(a + b * c, 2 * b)),
        "cour": (2 * d / 3, F(a + 2 * b * c, 3 * b)),
        "bert": (d, F(c)),
    }
    dwl = {}
    for k, (Q, fee) in cases.items():
        # Theorem 1.2 closed form versus direct integral of (P - c)
        integ = (F(a) * Q - Q * Q / 2) / b - c * Q
        check(f"{a},{b},{c} {k}: W closed form equals integral of P-c", W(Q) == integ)
        check(f"{a},{b},{c} {k}: CS+PS=W", CS(Q) + PS(Q, fee) == W(Q))
        dwl[k] = Ws - W(Q)
        check(f"{a},{b},{c} {k}: DWL=(d-Q)^2/(2b)", dwl[k] == (d - Q) ** 2 / (2 * b))
    check(f"{a},{b},{c}: loss shares 1/4 and 1/9", dwl["mono"] / Ws == F(1, 4) and dwl["cour"] / Ws == F(1, 9))
    check(f"{a},{b},{c}: DWL_M/DWL_C = 9/4", dwl["mono"] / dwl["cour"] == F(9, 4))
    check(f"{a},{b},{c}: monopoly DWL = d^2/(8b), Cournot = d^2/(18b)", dwl["mono"] == d * d / (8 * b) and dwl["cour"] == d * d / (18 * b))
    pm = PS(cases["mono"][0], cases["mono"][1]); pc = PS(cases["cour"][0], cases["cour"][1])
    check(f"{a},{b},{c}: profit monopoly > Cournot two exchanges", pm > pc)
    check(f"{a},{b},{c}: Cournot CS=2d^2/(9b), PS=2d^2/(9b)", CS(2*d/3) == 2*d*d/(9*b) and PS(2*d/3, cases['cour'][1]) == 2*d*d/(9*b))

# Reference-case cents (Example 2.2, Part B)
a, b, c = 120, 1, 20
d = F(100)
check("ref: Cournot DWL 5000/9 rounds half up to 556", F(5000, 9) == F(10000, 18) and half_up(F(5000, 9)) == 556)
check("ref: Cournot total 40000/9 rounds to 4444", half_up(F(40000, 9)) == 4444)
check("ref: Cournot CS and PS 20000/9 round to 2222", half_up(F(20000, 9)) == 2222)
check("ref: Cournot fee 160/3 rounds to 53 and volume 200/3 rounds to 67", half_up(F(160, 3)) == 53 and half_up(F(200, 3)) == 67)
check("ref: monopoly profit 2500 minus loss 1250 (misconception bullet)", F(2500) - F(1250) == 1250)

# M1, M2, M3, P3 exact values
check("M1 (90,3,10): loss 150, total 450, CS 150, PS 300", (F(30*30, 3) == 300) and (F(900, 6) == 150) and (F(3600, 6) == 600) and (600 - 450 == 150) and (F(3600, 24) == 150))
check("M2 (90,3,10): Cournot loss 200/3 = 20^2/6 = 3600/54", F(20**2, 6) == F(200, 3) == F(3600, 54) and half_up(F(200, 3)) == 67)
check("M3: midpoint two steps of int_0^50 (120-x) dx = 4750", (F(107, 1) + F(1, 2) - 0 == F(215, 2)) and ((F(215, 2) + F(165, 2)) * 25 == 4750) and (120 * 50 - F(50 * 50, 2) == 4750))
check("P3: (d^2/(8b))/(d^2/(18b)) = 9/4", (F(1, 8) / F(1, 18)) == F(9, 4))

# R1: volume at half the monopoly loss
s2 = math.sqrt(2)
Qroot = 1 - s2 / 4
check("R1: (sqrt2/4) squared is 1/8 (exact), so (d-Q)^2 = d^2/8 with d-Q = d/(2 sqrt2)", abs((s2 / 4) ** 2 - 1 / 8) < 1e-15 and abs(1 / (2 * s2) - s2 / 4) < 1e-15)
check("R1: root 1 - sqrt2/4 = 0.646447.. (page: 0.64645)", abs(Qroot - 0.64645) < 5e-6)
check("R1: 0.64645 lies between 1/2 and 2/3", 0.5 < Qroot < 2 / 3)
check("R1: Cournot loss / monopoly loss = 4/9 (<1/2)", F(4, 9) == (F(1, 18)) / (F(1, 8)) and F(4, 9) < F(1, 2))
# exact check of the boundary: 1 + sqrt2/4 <= 1 + bc/d  <=> d <= 4bc/sqrt2 = 2 sqrt2 bc
for bc_over_d in [0.3, 0.35355, 0.36, 1.0]:
    inside = (1 + s2 / 4) <= 1 + bc_over_d
    expected = (1 / bc_over_d) <= 2 * s2  # d <= 2 sqrt2 bc, with a = d + bc, Q <= a iff sqrt2/4 <= bc/d
    check(f"R1 boundary: bc/d={bc_over_d}: inside [0,a] iff d <= 2 sqrt2 bc", inside == expected)
check("R1: other root exceeds d (so it is not the asked root below d)", 1 + s2 / 4 > 1)

# R3 difference (units d^2/b)
for lam in [F(0), F(2, 7), F(1), F(3)]:
    wm = lam * F(1, 8) + F(1, 4)
    wc = lam * F(2, 9) + F(2, 9)
    check(f"R3 lambda={lam}: difference equals (7 lambda - 2)/72", wc - wm == (7 * lam - 2) / 72)
print("ALL_OK" if ok else "SOME_FAIL")
