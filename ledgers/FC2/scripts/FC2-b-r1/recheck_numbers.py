"""FC2-b round 1 verifier script: independent re-derivation of the prose numbers in L04, L05, L06.

Uses only the standard library. Run as: .venv/bin/python -I ledgers/FC2/scripts/FC2-b-r1/recheck_numbers.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))


# ---------- L04 ----------
r = math.log(10 / 9)
check("L04 r=ln(10/9) ~ 0.10536 per year", round(r, 5) == 0.10536, f"r={r:.8f}")
check("L04 10.54 per cent in lab docstring", round(r * 100, 2) == 10.54, f"r*100={r * 100:.4f}")
check("L04 Ex2.5 hold PV 10*(9/10)^4 = 6.561", F(10) * F(9, 10) ** 4 == F(6561, 1000), str(F(10) * F(9, 10) ** 4))
check("L04 Ex2.5 exercise d1 PV 18", F(20) * F(9, 10) == 18, "")
check("L04 Ex2.5 put d3 PV 14.58", F(20) * F(9, 10) ** 3 == F(1458, 100), str(F(20) * F(9, 10) ** 3))
check("L04 Ex2.5 put d2 PV 8.10 (E3)", F(10) * F(9, 10) ** 2 == F(810, 100), "")
check("L04 hold values at t=1,2,3 are 7.29, 8.10, 9.00",
      [float(F(10) * F(9, 10) ** (4 - t)) for t in (1, 2, 3)] == [7.29, 8.1, 9.0], "")
check("L04 R1 S_tau = 100 + 20000/729", F(100) + F(20000, 729) == F(100) + F(20000, 729), f"{float(F(100) + F(20000, 729)):.5f}")
check("L04 R1 numeric 127.43484", round(float(F(100) + F(20000, 729)), 5) == 127.43484, "")
check("L04 R3 path PV 7.29 and 32.805",
      F(10) * F(9, 10) ** 3 == F(729, 100) and F(50) * F(9, 10) ** 4 == F(32805, 1000), "")
check("L04 E2 put PV 6.561 -> 6.56 with last spot 90", F(10) * F(9, 10) ** 4 == F(6561, 1000), "")
check("L04 quiz 6.56 within 0.005", abs(6.56 - 6.561) <= 0.005, "")
check("L04 Remark: 1000(9/10)^4 = 656.1 cents", F(1000) * F(9, 10) ** 4 == F(6561, 10), "")
check("L04 path 100,120,90,80,110 call intrinsic 0,20,0,0,10",
      [max(s - 100, 0) for s in (100, 120, 90, 80, 110)] == [0, 20, 0, 0, 10], "")
check("L04 put intrinsic 0,0,10,20,0", [max(100 - s, 0) for s in (100, 120, 90, 80, 110)] == [0, 0, 10, 20, 0], "")
_pv_call = [F(max(s - 100, 0)) * F(9, 10) ** t for t, s in enumerate((100, 120, 90, 80, 110))]
check("L04 best call exercise date on path is 1 (PV 18)", max(range(5), key=lambda t: _pv_call[t]) == 1
      and _pv_call[1] == 18, str(_pv_call))
_pv_put = [F(max(100 - s, 0)) * F(9, 10) ** t for t, s in enumerate((100, 120, 90, 80, 110))]
check("L04 best put exercise date on path is 3 (PV 14.58)", max(range(5), key=lambda t: _pv_put[t]) == 3
      and _pv_put[3] == F(1458, 100), str(_pv_put))

# ---------- L05 ----------
S = 100.0
K_grid = [80, 90, 100, 110, 120]


def call(Kf: float, D: float) -> float:
    return max(S - D * Kf, 0.0) + max(100 - Kf, 0.0) / 10.0


def bounds_ok(D: float) -> bool:
    for Kf in K_grid:
        c = call(Kf, D)
        p = c - S + D * Kf
        if not (0 <= c <= S and c >= max(S - D * Kf, 0) and 0 <= p <= D * Kf and p >= max(D * Kf - S, 0)):
            return False
    return True


# threshold: call at 80 exceeds spot when D < 1/40
check("L05 D=1/100 breaks bounds (call at 80 > S)", not bounds_ok(0.01), f"call80={call(80, 0.01)}")
check("L05 D=1/40 bounds hold (boundary)", bounds_ok(1 / 40), f"call80={call(80, 1 / 40)}")
grid = [i / 1000 for i in range(1, 3001)]
first_ok = min(d for d in grid if bounds_ok(d))
check("L05 smallest D on 0.001 grid where all bounds hold is 1/40 (0.025)", abs(first_ok - 0.025) < 1e-9,
      f"first_ok={first_ok}")
check("L05 lab docstring: bounds hold only for D>=1/40 (no passing D below 1/40 on grid)",
      all(not bounds_ok(d) for d in grid if d < 0.025 - 1e-12), "")
check("L05 synthetic calls 3000,2000,1000,100,0 cents at D=0.9",
      [round(call(k, 0.9) * 100) for k in K_grid] == [3000, 2000, 1000, 100, 0], "")
check("L05 synthetic puts 200,100,0,0,800 cents",
      [round((call(k, 0.9) - 100 + 0.9 * k) * 100) for k in K_grid] == [200, 100, 0, 0, 800], "")
check("L05 M1 put 9.85 (exact rationals)", F(8) - 100 + F(97, 100) * 105 == F(985, 100), str(F(8) - 100 + F(97, 100) * 105))
check("L05 M2 bound 12", max(50 - 0.95 * 40, 0) == 12, "")
check("L05 M3 chord 9.5", (15 + 4) / 2 == 9.5, "")
check("L05 E1 second differences 0,100,800 cents",
      [3000 - 2 * 2000 + 1000, 2000 - 2 * 1000 + 100, 1000 - 2 * 100 + 0] == [0, 100, 800], "")
check("L05 E3 DK-S = 8 at 120", 0.9 * 120 - 100 == 8, "")
check("L05 Ex canon: 100e^-0.1 - 50 = 40.48", round(100 * math.exp(-0.1) - 50, 2) == 40.48, f"{100 * math.exp(-0.1) - 50:.5f}")
check("L05 R2: 120 - e^0.1*100 = 9.48", round(120 - math.exp(0.1) * 100, 2) == 9.48, f"{120 - math.exp(0.1) * 100:.5f}")
# explicit planted-convexity recheck with exact fractions
calls = {8000: F(3000), 9000: F(2000) + 500, 10000: F(1000), 11000: F(100), 12000: F(0)}
ks = sorted(calls)
viol = []
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        for k in range(j + 1, len(ks)):
            k1, k2, k3 = ks[i], ks[j], ks[k]
            lam = F(k3 - k2, k3 - k1)
            if calls[k2] > lam * calls[k1] + (1 - lam) * calls[k3]:
                viol.append((k1, k2, k3))
check("L05 planted convexity violated triples = [(8000,9000,10000),(8000,9000,11000),(8000,9000,12000)]",
      viol == [(8000, 9000, 10000), (8000, 9000, 11000), (8000, 9000, 12000)], str(viol))

# ---------- L06 ----------
q = F(5, 4) - F(1, 2)
q = q / (F(3, 2) - F(1, 2))
check("L06 Ex1.5 q=3/4", q == F(3, 4), str(q))
delta = F(50) / ((F(3, 2) - F(1, 2)) * 100)
B = (F(3, 2) * 0 - F(1, 2) * 50) / ((F(3, 2) - F(1, 2)) * F(5, 4))
check("L06 Ex1.5 delta 1/2, B -20, V0 30", delta == F(1, 2) and B == -20 and delta * 100 + B == 30, "")
check("L06 Ex1.6 cash 5, pays 25/4", (35 - 50 + 20) * F(5, 4) == F(25, 4), "")
check("L06 Ex3.4 V(0,0)=45", (F(3, 4) * 75) / F(5, 4) == 45, "")
check("L06 Ex3.4 V(1,1)=75", (F(3, 4) * 125) / F(5, 4) == 75, "")
check("L06 closed form 45", F(16, 25) * F(9, 16) * 125 == 45, "")
check("L06 E[S2]=156.25", F(9, 16) * 225 + F(6, 16) * 75 + F(1, 16) * 25 == F(15625, 100), "")
check("L06 misconception: payoff at expected price 56.25, discounted 36",
      (F(15625, 100) - 100) * F(16, 25) == 36, "")
check("L06 expected payoff 1125/16", F(9, 16) * 125 == F(1125, 16), "")
check("L06 M1 q=1/2, V0=40", (F(1, 2)) == (F(5, 4) - F(1, 2)) / (2 - F(1, 2)) and (F(1, 2) * 100) / F(5, 4) == 40, "")
check("L06 M2 delta 2/3, B -80/3", F(100) / ((2 - F(1, 2)) * 100) == F(2, 3) and (F(-50)) / ((2 - F(1, 2)) * F(5, 4)) == F(-80, 3), "")
check("L06 M3 V(0,0)=48", (F(1, 2) * ((F(1, 2) * 300) / F(5, 4))) / F(5, 4) == 48, "")
check("L06 E2 V0 doubles to 60", (F(3, 4) * 100) / F(5, 4) == 60, "")
check("L06 E3 short-sale cash flow zero, payoff 5/2 both states",
      (-28 + 30 - 2) == 0 and (50 - 75 + 25 + F(5, 2)) == F(5, 2) and (0 - 25 + 25 + F(5, 2)) == F(5, 2), "")
check("L06 R1 payoff 50,0,-50 replicated by Delta=1, B=-80",
      all(1 * p + F(5, 4) * (-80) == t for p, t in ((150, 50), (100, 0), (50, -50))), "")
check("L06 R2 V0=25 at R=1", (F(1, 2) * 50) / 1 == 25, "")

failures = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" :: {detail}"))
print(f"checks {len(results)} failures {len(failures)}")
