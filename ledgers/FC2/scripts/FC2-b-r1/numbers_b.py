"""Recompute the displayed numbers of FC2 L04-L06 (slice b) from their inputs, exactly where possible.

Usage: .venv/bin/python -I ledgers/FC2/scripts/FC2-b-r1/numbers_b.py   (from the checkout root)
Prints one line per check: the displayed value from the page, the recomputed value, and OK or MISMATCH.
"""
from __future__ import annotations

import math
from fractions import Fraction as F

fails: list[str] = []


def check(label: str, shown: str, value: float, digits: int) -> None:
    got = f"{float(value):.{digits}f}"
    ok = got == shown
    print(f"{'OK' if ok else 'MISMATCH'} {label}: page={shown} recomputed={float(value):.10f} rounded={got}")
    if not ok:
        fails.append(label)


e = math.exp
check("L04 ex2.5 call hold at 0", "6.70", 10 * e(-0.4), 2)
check("L04 ex2.5 call exercise at 1, PV at 0", "18.10", 20 * e(-0.1), 2)
check("L04 ex2.5 put exercise at 3, PV at 0", "14.82", 20 * e(-0.3), 2)
check("L04 lab table call hold at date 1", "7.41", 10 * e(-0.3), 2)
check("L04 lab table call hold at date 2", "8.19", 10 * e(-0.2), 2)
check("L04 lab table call hold at date 3", "9.05", 10 * e(-0.1), 2)
check("L04 lab 1000e^-0.4 cents", "670.32", 1000 * e(-0.4), 2)
check("L04 R1 expiry spot 100+20e^0.3", "126.99718", 100 + 20 * e(0.3), 5)
check("L04 R3 call hold 50e^-0.4", "33.52", 50 * e(-0.4), 2)
check("L04 R3 exercise at 3, PV", "7.41", 10 * e(-0.3), 2)
check("L04 canon 25 USD call minus 8 USD premium", "17.00", 25 - 8, 2)
check("L05 canon 100e^-0.1-50", "40.48", 100 * e(-0.1) - 50, 2)
check("L05 R2 bound 120 - e^0.1*100", "9.48", 120 - e(0.1) * 100, 2)
check("L05 M1 put 8-100+0.97*105", "9.85", 8 - 100 + F(97, 100) * 105, 2)
check("L05 E3 put bound 0.9*120-100", "8.00", F(9, 10) * 120 - 100, 2)
D = F(9, 10)
strikes = (8000, 9000, 10000, 11000, 12000)
calls = [max(10000 - D * k, 0) + F(max(10000 - k, 0), 10) for k in strikes]
puts = [c - 10000 + D * k for c, k in zip(calls, strikes)]
print("L05 synthetic calls (cents):", [int(c) for c in calls], "puts (cents):", [int(p) for p in puts])
assert [int(c) for c in calls] == [3000, 2000, 1000, 100, 0]
assert [int(p) for p in puts] == [200, 100, 0, 0, 800]
check("L05 E1 second difference at 90 USD (cents)", "0", float(calls[0] - 2 * calls[1] + calls[2]), 0)
check("L05 E1 second difference at 100 USD (cents)", "100", float(calls[1] - 2 * calls[2] + calls[3]), 0)
check("L05 E1 second difference at 110 USD (cents)", "800", float(calls[2] - 2 * calls[3] + calls[4]), 0)
check("L05 key-result second difference 20-2*10+1", "1", 20 - 2 * 10 + 1, 0)
check("L05 M3 second difference 15-18+4", "1", 15 - 2 * 9 + 4, 0)
check("L05 M3 chord (15+4)/2", "9.50", F(15 + 4, 2), 2)
S0, K, u, d, R = F(100), F(100), F(3, 2), F(1, 2), F(5, 4)
Vu, Vd = max(u * S0 - K, 0), max(d * S0 - K, 0)
Delta = (Vu - Vd) / ((u - d) * S0)
B = (u * Vd - d * Vu) / ((u - d) * R)
q = (R - d) / (u - d)
V0 = Delta * S0 + B
print("L06 ex1.5 Delta", Delta, "B", B, "q", q, "V0", V0)
check("L06 ex1.5 (3/4*50)/(5/4)", "30.00", q * Vu / R, 2)
shown_expr = F(50, 2) - 20
print(f"L06 ex1.5 page expression '50/2 - 20' evaluates to {shown_expr} (page claims 30); Delta*S0 = {Delta * S0}")
if shown_expr != 30:
    fails.append("L06 ex1.5 displayed expression 50/2 - 20 = 30")
cash = 35 - 50 + 20
print("L06 ex1.6 cash today", cash, "lent at R gives", F(cash) * R, "(page 25/4)")
assert F(cash) * R == F(25, 4)
Vuu, Vud, Vdd = max(S0 * u * u - K, 0), max(S0 * u * d - K, 0), max(S0 * d * d - K, 0)
V11 = (q * Vuu + (1 - q) * Vud) / R
V10 = (q * Vud + (1 - q) * Vdd) / R
V00 = (q * V11 + (1 - q) * V10) / R
closed = sum(math.comb(2, k) * q**k * (1 - q) ** (2 - k) * max(S0 * u**k * d ** (2 - k) - K, 0) for k in range(3)) / R**2
print("L06 ex3.4 V11", V11, "V10", V10, "V00", V00, "closed", closed)
assert V11 == 75 and V00 == 45 and closed == 45
EQS2 = q * q * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25
print("L06 quiz E^Q[S2]", EQS2, "R^2 S0", R * R * S0)
assert EQS2 == F(3125, 20) and R * R * S0 == F(3125, 20)
EPAY = q * q * 125
print("L06 misconception E^Q[payoff] before discounting", float(EPAY), "page 70.3125")
assert EPAY == F(703125, 10000)
print("L06 misconception payoff at 156.25 discounted", float(max(F(15625, 100) - 100, 0) * F(16, 25)), "page 36")
print("L06 E2 V0 with spot and strike 200", float((q * max(F(3, 2) * 200 - 200, 0)) / R), "page 60")
assert (q * max(F(3, 2) * 200 - 200, 0)) / R == 60
M1q = (F(5, 4) - F(1, 2)) / (2 - F(1, 2))
M1V0 = M1q * 100 / F(5, 4)
M2D = (100 - 0) / ((2 - F(1, 2)) * 100)
M2B = (2 * 0 - F(1, 2) * 100) / ((2 - F(1, 2)) * F(5, 4))
print("L06 M1 q", M1q, "V0", M1V0, "M2 Delta", M2D, "B", M2B, "check", M2D * 100 + M2B)
assert M1q == F(1, 2) and M1V0 == 40 and M2D == F(2, 3) and M2B == F(-80, 3) and M2D * 100 + M2B == 40
M3 = (F(1, 2) * 300) / F(5, 4)
M3b = (F(1, 2) * M3) / F(5, 4)
print("L06 M3 V(1,1)", M3, "V(0,0)", M3b)
assert M3 == 120 and M3b == 48
print("L06 R1 payoffs", [1 * s + (-80) * R for s in (150, 100, 50)])
assert [1 * s + (-80) * R for s in (150, 100, 50)] == [50, 0, -50]
R2q = (1 - d) / (u - d)
print("L06 R2 q", R2q, "V0", R2q * 50, "B", (u * 0 - d * 50) / ((u - d) * 1))
assert R2q == F(1, 2) and R2q * 50 == 25
print("RESULT", "ALL OK (except the flagged displayed expression)" if fails == ["L06 ex1.5 displayed expression 50/2 - 20 = 30"] else f"MISMATCHES: {fails}")
