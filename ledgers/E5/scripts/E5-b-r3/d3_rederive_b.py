"""Round 3 verifier re-derivation (E5-b): L04-L06 numbers recomputed with Fractions, independent of the lab twins.

Formulas come from the page definitions (L04 Definition 2.1, Derivation 2.2, Proposition 3.2, 4.2, 4.3; L05 A1-A3,
Propositions 2.1, 2.2, 3.1; L06 A1-A3, Proposition 2.1, Corollary 3.2). The L06 seeded path is regenerated here with
random.Random(20261028).randint(-100, 100), one draw per period, and checked against the identity of Corollary 3.2.
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r3/d3_rederive_b.py
"""

from __future__ import annotations

import random
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E5 = ROOT / "course" / "modules" / "E" / "E5"
fails: list[str] = []


def check(label: str, ok: bool) -> None:
    print(("OK   " if ok else "FAIL ") + label)
    if not ok:
        fails.append(label)


def r6(x: F) -> str:
    """Six decimals, rounded half to even, as the twins print them."""
    scaled = round(x * 10**6)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**6)
    return f"{sign}{whole}.{frac:06d}"


# ---- L04: IS-LM, inputs from the Lab 1 hypothesis ----
c, c0, b0, b, d, h, tax, g, mbar = F(3, 4), F(1), F(1), F(2), F(1, 2), F(1), F(0), F(1), F(2)


def is_lm(g_: F, m_: F, b_: F) -> tuple[F, F, F]:
    A = c0 - c * tax + b0 + g_
    D = h * (1 - c) + b_ * d
    Y = (h * A + b_ * m_) / D
    i = (d * A - (1 - c) * m_) / D
    return Y, i, D


y0, i0, D0 = is_lm(g, mbar, b)
check("L04 A: D = 5/4", D0 == F(5, 4))
check("L04 A: Y* = 28/5", y0 == F(28, 5))
check("L04 A: i* = 4/5", i0 == F(4, 5))
A0 = c0 - c * tax + b0 + g
check("L04 A: IS residual 0 at (Y*, i*)", y0 - (c0 + c * (y0 - tax) + b0 - b * i0 + g) == 0)
check("L04 A: LM residual 0 at (Y*, i*)", d * y0 - h * i0 - mbar == 0)
y1, i1, _ = is_lm(F(11, 10), mbar, b)
y2, i2, _ = is_lm(F(2), mbar, b)
check("L04 B: dY for G 1->11/10 is 2/25", y1 - y0 == F(2, 25))
check("L04 B: di for G 1->11/10 is 1/25", i1 - i0 == F(1, 25))
check("L04 B: multiplier 4/5 for step to 11/10", (y1 - y0) / (F(11, 10) - g) == F(4, 5))
check("L04 B: dY for G 1->2 is 4/5", y2 - y0 == F(4, 5))
check("L04 B: di for G 1->2 is 2/5", i2 - i0 == F(2, 5))
check("L04 B: h/D = 4/5 and 4/5 < 1/(1-c)=4", h / D0 == F(4, 5) and F(4, 5) < 1 / (1 - c))
y3, i3, _ = is_lm(g, F(5, 2), b)
check("L04 C: dY for mbar 2->5/2 is 4/5", y3 - y0 == F(4, 5))
check("L04 C: monetary multiplier 8/5", (y3 - y0) / (F(5, 2) - mbar) == F(8, 5))
check("L04 C: di per unit of money is -1/5", (i3 - i0) / (F(5, 2) - mbar) == F(-1, 5))
check("L04 C: b/D = 8/5", b / D0 == F(8, 5))
check("L04 C: -(1-c)/D = -1/5", -(1 - c) / D0 == F(-1, 5))
yd0, _, _ = is_lm(g, mbar, F(0))
yd1, _, _ = is_lm(F(2), mbar, F(0))
check("L04 D: b=0 spending multiplier equals 4 = 1/(1-c)", (yd1 - yd0) / F(1) == 4 and 1 / (1 - c) == 4)
# Prop 4.3 bound: h/D <= 1/(1-c) iff bd >= 0, with equality iff bd = 0
for bb in (F(0), F(1, 3), F(2), F(7)):
    _, _, Dd = is_lm(g, mbar, bb)
    check(f"L04 Prop 4.3 at b={bb}: h/D <= 1/(1-c) iff bd>=0", (h / Dd <= 1 / (1 - c)) == (bb * d >= 0))
    check(f"L04 Prop 4.3 at b={bb}: equality iff bd=0", (h / Dd == 1 / (1 - c)) == (bb * d == 0))
# Remark 4.5: dI/dG = -b d/D
check("L04 Remark 4.5: dI/dG = -bd/D = -1/(5/4) = -4/5", -b * d / D0 == F(-4, 5))
# misconception 2 numbers: rise in Y 4/5 for G 1->2; per unit 4/5
check("L04 misc 2: per-unit output rise 4/5 for G 1->2", (y2 - y0) / (F(2) - g) == F(4, 5))
# E1: interest per output = d/h = 1/2
check("L04 E1: (1/25)/(2/25) = d/h = 1/2", (F(1, 25) / F(2, 25)) == d / h == F(1, 2))
# E3: share 1/5 of benchmark, closed form h(1-c)/D
check("L04 E3: 0.8/4 = 1/5 and h(1-c)/D = 1/5", F(4, 5) / 4 == F(1, 5) == h * (1 - c) / D0)
# M1..M3, R1..R3 at the page parameters
cM, bM, dM, hM, AM, mM = F(1, 2), F(2), F(1), F(2), F(4), F(3)
DM = hM * (1 - cM) + bM * dM
check("L04 M1: D=3, Y*=14/3, i*=5/6", DM == 3 and (hM * AM + bM * mM) / DM == F(14, 3) and (dM * AM - (1 - cM) * mM) / DM == F(5, 6))
check("L04 M1: IS check = 4 and LM check = 3", (1 - cM) * F(14, 3) + bM * F(5, 6) == 4 and dM * F(14, 3) - hM * F(5, 6) == 3)
check("L04 M2: h/D = 2/3 and benchmark 2", hM / DM == F(2, 3) and 1 / (1 - cM) == 2)
check("L04 M3: b/D = 2/3 and -(1-c)/D = -1/6", bM / DM == F(2, 3) and -(1 - cM) / DM == F(-1, 6))
check("L04 R1: d=0 gives D=h(1-c), dY/dG = 1/(1-c)", h * (1 - c) == F(1, 4) and h / (h * (1 - c)) == 1 / (1 - c))

# ---- L05: AD-AS, inputs from the Lab 1 hypothesis ----
a, eta, ybar, nu, pe = F(1160), F(100), F(1000), F(200), F(1)


def sr(a_: F, nu_: F) -> tuple[F, F]:
    p = (a_ - ybar + nu_ * pe) / (eta + nu_)
    return p, a_ - eta * p


p0, y0s = sr(a, nu)
p1, y1s = sr(a + 30, nu)
check("L05 A: P*=6/5, Y*=1040", p0 == F(6, 5) and y0s == 1040)
check("L05 A: Y*-Ybar = nu(P*-Pe) = 40", y0s - ybar == nu * (p0 - pe) == 40)
check("L05 B: dP = 1/10, dY = 20", p1 - p0 == F(1, 10) and y1s - y0s == 20)
check("L05 B: P=1.3, Y=1060 after the shift", p1 == F(13, 10) and y1s == 1060)
check("L05 B: output share 2/3, price share 1/300", nu / (eta + nu) == F(2, 3) and 1 / (eta + nu) == F(1, 300))
lr0 = (a - ybar) / eta
lr1 = (a + 30 - ybar) / eta
check("L05 C: LR price 1.6 and 1.9", lr0 == F(8, 5) and lr1 == F(19, 10))
check("L05 C: LR price change 0.3 = 30/100", lr1 - lr0 == F(3, 10) == F(30, 100))
check("L05 C: LR output a - eta*P_LR equals 1000 in both states", a - eta * lr0 == ybar and (a + 30) - eta * lr1 == ybar)
# Prop 2.1 with Pe = lr1 must return lr1
p_fp2 = (a + 30 - ybar + nu * lr1) / (eta + nu)
check("L05 C: short-run price with Pe = LR price equals LR price", p_fp2 == lr1)
for slope in (F(50), F(100), F(200), F(400), F(800)):
    share = slope / (eta + slope)
    pa, ya = sr(a, slope)
    pb, yb = sr(a + 30, slope)
    check(f"L05 D nu={slope}: share {r6(share)} price change {r6(pb - pa)} output change {r6(yb - ya)}",
          (yb - ya) == share * 30 and (pb - pa) == F(30) / (eta + slope))
check("L05 E2: increments 5, 5, 4, 8/3", (F(15) - 10, F(20) - 15, F(24) - 20) == (5, 5, 4) and
      30 * (F(8, 9) - F(4, 5)) == F(8, 3))
check("L05 R2: P*=3/2 and Y*=1040 with Pe=1.3, a=1190", (F(190) + 200 * F(13, 10)) / 300 == F(3, 2) and
      1190 - 100 * F(3, 2) == 1040)
check("L05 R3: output at P=1.3 with Pe=1 is 1060, gap 60", ybar + nu * (F(13, 10) - pe) == 1060 and
      ybar + nu * (F(13, 10) - pe) - ybar == 60)
check("L05 canon: demand at P=1 is 1060 and at P=1.6 is 1000 (a=1160)", 1160 - 100 * 1 == 1060 and 1160 - 100 * F(8, 5) == 1000)
# L05 canon bullet 2: with Pe moving by dPe, dP=(da+nu dPe)/(eta+nu) and dY=nu(da-eta dPe)/(eta+nu)
da, dpe = F(30), F(1, 10)
p_mv = (a + da - ybar + nu * (pe + dpe)) / (eta + nu)
y_mv = (a + da) - eta * p_mv
check("L05 canon: dP=(da+nu dPe)/(eta+nu) with Pe moving", p_mv - p0 == (da + nu * dpe) / (eta + nu))
check("L05 canon: dY=nu(da-eta dPe)/(eta+nu) with Pe moving", y_mv - y0s == nu * (da - eta * dpe) / (eta + nu))
check("L05 canon: dP with Pe fixed reduces to da/(eta+nu)", (p1 - p0) == da / (eta + nu))
p_m1 = (F(1100) - ybar + F(100) * F(11, 10)) / (F(100) + F(100))
check("L05 M1: P*=1.05, Y*=995", p_m1 == F(21, 20) and F(1100) - 100 * p_m1 == 995)
check("L05 M2: share 3/4, dY 30, dP 0.2", F(150, 200) == F(3, 4) and F(3, 4) * 40 == 30 and F(40, 200) == F(1, 5))
check("L05 M3: LR 1 and 1.4, output 1000", F(100, 100) == 1 and F(140, 100) == F(7, 5) and F(1140) - 100 * F(7, 5) == 1000)
check("L05 E1: share 4/5, dY 24, dP 0.06 at nu=400", F(400, 500) == F(4, 5) and F(4, 5) * 30 == 24 and F(30, 500) == F(3, 50))
check("L05 E3: 1.9-1.6 = 0.3 gives da = 30", F(19, 10) - F(8, 5) == F(3, 10) and F(3, 10) * 100 == 30)
check("L05 P2: 1 - nu/(eta+nu) = eta/(eta+nu)", 1 - nu / (eta + nu) == eta / (eta + nu))

# ---- L06: Phillips curve, seeded path ----
Ybar, NU, KAPPA, UN = F(1000), F(200), F(200), F(5, 100)
P_START, PI_START = F(6, 5), F(3, 100)
beta0 = KAPPA / (NU * P_START)
pe_a = P_START * (1 + PI_START)
p_a = pe_a - KAPPA * (F(6, 100) - UN) / NU
pi_a = (p_a - P_START) / P_START
check("L06 A: expected price 1.236, price 1.226", pe_a == F(1236, 1000) and p_a == F(1226, 1000))
check("L06 A: inflation 13/600 = 0.021667", pi_a == F(13, 600) and r6(pi_a) == "0.021667")
check("L06 A: Phillips form equals levels", PI_START - beta0 * (F(6, 100) - UN) == pi_a)
check("L06 beta at P=6/5 is 5/6 and at P=1 is 1", beta0 == F(5, 6) and KAPPA / (NU * 1) == 1)
rng = random.Random(20261028)
price, pi = P_START, PI_START
seen = []
ok_all = True
no_change = 0
zero_gap = 0
for t in range(1, 13):
    draw = rng.randint(-100, 100)
    gap = F(draw, 10000)
    u = UN + gap
    pe_t = price * (1 + pi)
    p_new = pe_t - KAPPA * (u - UN) / NU  # from P - Pe = (Y - Ybar)/nu with Y - Ybar = -kappa (u - un)
    pi_new = (p_new - price) / price
    form = pi - KAPPA / (NU * price) * (u - UN)
    ok_all = ok_all and pi_new == form
    no_change += pi_new == pi
    zero_gap += gap == 0
    seen.append((t, draw, r6(u * 100), r6(pi_new), r6(pi_new - pi)))
    price, pi = p_new, pi_new
check("L06 B: identity holds in each of 12 periods (independent path)", ok_all)
check("L06 B: zero gap periods 0 and no-change periods 0", zero_gap == 0 and no_change == 0)
expected_draws = [58, 42, 76, 85, 49, -89, 48, 75, -46, -91, 27, 38]
check("L06 B: gap draws equal the printed unemployment_gap_bp column", [s[1] for s in seen] == expected_draws)
pos = sum(1 for x in expected_draws if x > 0)
neg = sum(1 for x in expected_draws if x < 0)
check("L06 E2: 9 positive and 3 negative gaps", pos == 9 and neg == 3)
check("L06 E3: beta_1 = 5/6 and change -(5/6)(0.0058) prints -0.004833",
      r6(-F(5, 6) * F(58, 10000)) == "-0.004833")
check("L06 E3: 5.5 percent row change -0.004167", r6(-F(5, 6) * F(5, 1000)) == "-0.004167")
check("L06 Part C: 4 percent change 0.008333 and 3 percent 1/60", r6(-F(5, 6) * F(-1, 100)) == "0.008333" and
      -beta0 * F(-2, 100) == F(1, 60))
check("L06 misc 1: gap -0.01 at beta 5/6 changes inflation by 1/120", -F(5, 6) * F(-1, 100) == F(1, 120))
check("L06 R2: u = 0.05 + 0.01/(5/6) = 0.062", UN + F(1, 100) / F(5, 6) == F(31, 500))
check("L06 R1: beta ratio 6/5 equals 1.2/1", (1 / F(5, 6)) == F(6, 5))
check("L06 M1: beta = 0.5, pi = 0.03 (kappa 100, nu 200, P=1)", F(100, 200) == F(1, 2) and F(4, 100) - F(1, 2) * F(2, 100) == F(3, 100))
check("L06 M2: beta = 0.8, pi = 0.048", F(200, 250) == F(4, 5) and F(4, 100) - F(4, 5) * F(-1, 100) == F(48, 1000))
check("L06 M3: pi falls to 0.005 at gap 0.03 (beta 0.5, pi_prev 0.02)", F(2, 100) - F(1, 2) * F(3, 100) == F(5, 1000))
check("L06 Q6: pi = 0.03 - (5/6)(0.01) = 0.021667", r6(F(3, 100) - F(5, 6) * F(1, 100)) == "0.021667")
check("L06 Q9: pi = 0.04 + 0.8*0.01 = 0.048", F(4, 100) - F(4, 5) * F(-1, 100) == F(48, 1000))

# ---- prose and page numbers: compare the printed decimals in the page's expected blocks with these results ----
pages = {"L06": E5 / "L06.html"}
txt = pages["L06"].read_text(encoding="utf-8")
block = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', txt, re.S).group(1)
rows = [ln for ln in block.splitlines() if ln.startswith("t ")]
check("L06 expected block has 12 period lines", len(rows) == 12)
for (t, draw, u6, pi6, ch6), ln in zip(seen, rows):
    want = f"t {t} unemployment_gap_bp {draw} unemployment {u6} percent inflation {pi6} change {ch6} identity True"
    check(f"L06 page line t={t} equals recomputation", ln.strip() == want)

print()
print("FAILS:", len(fails))
for f in fails:
    print("  ", f)
sys.exit(1 if fails else 0)
