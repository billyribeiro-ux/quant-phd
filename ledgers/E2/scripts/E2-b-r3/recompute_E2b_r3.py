"""E2 slice b (L04-L06), round 3: independent recomputation of every prose number and the
variant predictions in the problem sets. Exact Fractions only. Run as: python3 -I <this file>.
Variant twins are run from a scratch copy under /tmp, never from the checkout."""

import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

F = Fraction
ROOT = Path(__file__).resolve().parents[4]
TWINS = ROOT / "tests" / "labs" / "E2"
ok = []


def check(name, value, expected):
    assert value == expected, (name, value, expected)
    ok.append(f"PASS {name} = {value}")


def run_variant(twin, subs, tag):
    src = (TWINS / twin).read_text(encoding="utf-8")
    for old, new in subs:
        assert src.count(old) == 1, (tag, old)
        src = src.replace(old, new)
    path = Path(tempfile.mkdtemp(prefix="e2b_r3_")) / "variant.py"
    path.write_text(src, encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True)
    assert out.returncode == 0, (tag, out.stderr)
    return out.stdout


# ---------- L04 base case, lesson prose ----------
YL, YH, CL, CH = 4_000_000, 6_000_000, 1_000_000, 500_000
D = YH - YL
check("L04 Delta cents", D, 2_000_000)
check("L04 lower bound Delta/c_L", F(D, CL), 2)
check("L04 upper bound Delta/c_H", F(D, CH), 4)


def wage(e, t):
    return YH if e >= t else YL


def util(c, e, t):
    return wage(e, t) - c * e


def classify(t, cl=CL, ch=CH, yh=YH, yl=YL):
    w = lambda e: yh if e >= t else yl  # noqa: E731
    u = lambda c, e: w(e) - c * e  # noqa: E731
    uh = u(ch, t)
    bh = max(u(ch, e) for e in range(7))
    ul = u(cl, 0)
    bl = max(u(cl, e) for e in range(7))
    if t == 0:
        return "shared"
    if uh == bh and ul == bl:
        return "separating"
    if ul != bl:
        return "mimic"
    return "high-prefers-other"


labels = {t: classify(t) for t in range(7)}
check(
    "L04 Lab1 B labels",
    labels,
    {
        0: "shared",
        1: "mimic",
        2: "separating",
        3: "separating",
        4: "separating",
        5: "high-prefers-other",
        6: "high-prefers-other",
    },
)
check("L04 high net utility t=2 (cents)", util(CH, 2, 2), 5_000_000)
check("L04 high net utility t=3 (cents)", util(CH, 3, 3), 4_500_000)
check("L04 high net utility t=4 (cents)", util(CH, 4, 4), 4_000_000)
check("L04 low utility e=1 under t=1 (cents)", util(CL, 1, 1), 5_000_000)
check("L04 low utility e=0 (cents)", util(CL, 0, 1), 4_000_000)
check("L04 wage gain Delta, cost at t=2", (D, 2 * CH), (2_000_000, 1_000_000))
# problem-set variants (closed forms)
check("L04 m1 bounds c_H=250000", (F(D, CL), F(D, 250_000)), (2, 8))
check("L04 m1 whole-number count 2..8", len(range(2, 9)), 7)
check("L04 m2 high utility t=3 c_H=250000", YH - 250_000 * 3, 5_250_000)
check("L04 m2 low at e=3 (wage y_H)", YH - CL * 3, 3_000_000)
check("L04 m3 bounds Delta=1.5M", (F(1_500_000, CL), F(1_500_000, CH)), (F(3, 2), 3))
check("L04 e1 bounds c_H=400000", (F(D, CL), F(D, 400_000)), (2, 5))
check("L04 e2 bounds y_H=5M", (F(1_000_000, CL), F(1_000_000, CH)), (1, 2))
check("L04 e2 high utility t=1 (y_H=5M)", 5_000_000 - CH, 4_500_000)
check("L04 e2 low utility e=1 t=1 (y_H=5M)", 5_000_000 - CL, 4_000_000)
check("L04 e3 utilities t=2,3,4", [YH - CH * t for t in (2, 3, 4)], [5_000_000, 4_500_000, 4_000_000])

# L04 variant twins
out = run_variant("lab-E2-L04-1.py", [("COST_HIGH = 500_000", "COST_HIGH = 400_000")], "L04e1")
assert "separating thresholds on the grid by enumeration: [2, 3, 4, 5]" in out, out
assert "the two lists agree: True" in out, out
check("L04 e1 twin prints [2,3,4,5] and agree True", True, True)
out = run_variant("lab-E2-L04-1.py", [("Y_HIGH = 6_000_000", "Y_HIGH = 5_000_000")], "L04e2")
assert "separating thresholds on the grid by enumeration: [1, 2]" in out, out
assert "the two lists agree: True" in out, out
check("L04 e2 twin prints [1,2] and agree True", True, True)

# ---------- L05 base case ----------
TL, TH, PL, PH = 3000, 6000, F(3, 4), F(1, 4)


def cost(q):
    return F(q) * F(q) / 2


q_low = TL - PH / PL * (TH - TL)
check("L05 q_L*", q_low, 2000)
q_high = TH
m_low = TL * q_low
m_high = TH * q_high - (TH - TL) * q_low
check("L05 m_L cents", m_low, 6_000_000)
check("L05 m_H cents", m_high, 30_000_000)
u_high = TH * q_high - m_high
check("L05 U_H = (theta_H-theta_L) q_L*", (u_high, (TH - TL) * q_low), (6_000_000, 6_000_000))
check("L05 U_L = 0", TL * q_low - m_low, 0)
prof = PL * (m_low - cost(q_low)) + PH * (m_high - cost(q_high))
check("L05 menu profit cents", prof, 6_000_000)
fb = PL * (TL * 3000 - cost(3000)) + PH * (TH * 6000 - cost(6000))
check("L05 first-best profit cents", fb, 7_875_000)
check("L05 gap cents", fb - prof, 1_875_000)
check("L05 Remark2.1 low surplus loss weighted", PL * ((TL * 3000 - cost(3000)) - (TL * 2000 - cost(2000))), 375_000)
check("L05 Remark2.1 rent share", PH * u_high, 1_500_000)
check("L05 FOC balance p_L(theta_L-q_L)=p_H(theta_H-theta_L)", (PL * (TL - q_low), PH * (TH - TL)), (750, 750))
check("L05 m2 transfers q_L=1000", (TL * 1000, TH * 6000 - (TH - TL) * 1000), (3_000_000, 33_000_000))
check("L05 m2 U_H", TH * 6000 - (TH * 6000 - (TH - TL) * 1000), 3_000_000)
check("L05 m2 IC-L slack side", TL * 6000 - (TH * 6000 - (TH - TL) * 1000), -15_000_000)
prof_m2 = PL * (3_000_000 - cost(1000)) + PH * (33_000_000 - cost(6000))
check("L05 m3 profit at m2 menu", prof_m2, 5_625_000)
check("L05 m1 q_L* at p_H=1/2", TL - F(1, 2) / F(1, 2) * (TH - TL), 0)
check("L05 m1 profit (0,6000) p_H=1/2", F(1, 2) * (36_000_000 - cost(6000)), 9_000_000)
check("L05 e3 loss percent of first best is 23.81 (rounded)", round(F(1_875_000, 7_875_000) * 100, 2), F(2381, 100))
check("L05 e3 first best above menu percent", F(7_875_000, 6_000_000) - 1, F(3125, 10000))

# L05 variant e1: p_H = 1/3, p_L = 2/3 (prose predictions)
PL2, PH2 = F(2, 3), F(1, 3)
q_star2 = TL - PH2 / PL2 * (TH - TL)
check("L05 e1 q_L* at p_H=1/3", q_star2, 1500)
prof_1500 = PL2 * (TL * 1500 - cost(1500)) + PH2 * (TH * 6000 - (TH - TL) * 1500 - cost(6000))
check("L05 e1 profit at 1500 (cents)", prof_1500, 6_750_000)
fb2 = PL2 * (4_500_000) + PH2 * (18_000_000)
check("L05 e1 first best (cents)", fb2, 9_000_000)
prof_2000 = PL2 * (TL * 2000 - cost(2000)) + PH2 * (TH * 6000 - (TH - TL) * 2000 - cost(6000))
check("L05 e1 menu profit at 2000 rounded half up", int(prof_2000 + F(1, 2)), 6_666_667)
check("L05 e1 gap at 2000 (exact floor of 2.333...)", int((fb2 - prof_2000) + F(1, 2)), 2_333_333)
check("L05 e2 rent p_H=1/3", (TH - TL) * q_star2, 4_500_000)

out = run_variant(
    "lab-E2-L05-1.py",
    [("P_LOW = Fraction(3, 4)", "P_LOW = Fraction(2, 3)"), ("P_HIGH = Fraction(1, 4)", "P_HIGH = Fraction(1, 3)")],
    "L05e1",
)
for line in [
    "profit maximizing low-type quantity on the grid: 1500",
    "profit at that quantity, rounded to cents: 6750000",
    "menu expected profit: 6666667",
    "first-best expected profit: 9000000",
    "gap, first best minus menu: 2333333",
]:
    assert line in out, (line, out)
check("L05 e1 twin output matches prose (1500, 6750000, 6666667, 9000000, 2333333)", True, True)

# ---------- L06 base case ----------
OUT = 1_000_000
EH = F(3, 4) * OUT
EL = F(1, 4) * OUT
CHe = 100_000
check("L06 E_H", EH, 750_000)
check("L06 E_L", EL, 250_000)
check("L06 Delta_E", EH - EL, 500_000)
check("L06 first best E_H - c_H", EH - CHe, 650_000)
check("L06 beta threshold c_H/Delta_E", F(CHe, 500_000), F(1, 5))
check("L06 optimum profit", EH * (1 - F(1, 5)), 600_000)
check("L06 optimum agent utility", F(1, 5) * EH - CHe, 50_000)
check("L06 agency cost", (EH - CHe) - EH * F(4, 5), 50_000)
check("L06 m1 utilities at 1/4", (F(1, 4) * EH - CHe, F(1, 4) * EL), (87_500, 62_500))
check("L06 m1 profit at 1/4", EH * F(3, 4), 562_500)
check("L06 m2 utility at 2/15 high", F(2, 15) * EH - CHe, 0)
check("L06 m2 low utility at 2/15", F(2, 15) * EL, F(100_000, 3))
check("L06 m3 profit alpha=10000", EH - (10_000 + F(1, 5) * EH), 590_000)
check("L06 p1 counterexample U_H", -1_000_000 + F(1, 2) * EH - CHe, -725_000)
check("L06 p1 counterexample U_L", -1_000_000 + F(1, 2) * EL, -875_000)
check("L06 p2 bound", EH * F(4, 5), 600_000)
check("L06 p3 weighted payment equals alpha + beta E_L", F(3, 4) * 0 + F(1, 4) * OUT - EL, 0)
check("L06 e1 threshold c_H=150k", F(150_000, 500_000), F(3, 10))
check("L06 e1 profit", EH * F(7, 10), 525_000)
check("L06 e1 first best and agency cost", (750_000 - 150_000, 600_000 - 525_000), (600_000, 75_000))
EH2, EL2 = F(800_000), F(200_000)
check("L06 e2 threshold", F(100_000, 600_000), F(1, 6))
check("L06 e2 profit exact", EH2 * F(5, 6), F(2_000_000, 3))
check("L06 e2 profit rounded half up", int(EH2 * F(5, 6) + F(1, 2)), 666_667)
check("L06 e2 first best", EH2 - CHe, 700_000)
check("L06 e3 surplus = sum", (F(1, 5) * EH - CHe + 600_000), 650_000)
check(
    "L06 Remark 1.4 alpha at beta=0.2,0.5,1",
    [CHe - b * EH for b in (F(1, 5), F(1, 2), 1)],
    [-50_000, -275_000, -650_000],
)

# L06 twin: Part A and B and C numbers
out = run_variant("lab-E2-L06-1.py", [], "L06base")
assert "best share on the grid: 0.20, agent takes high effort" in out, out
assert "principal profit at the best share, in cents: 600000" in out, out
assert "agency loss, first best minus best share, in cents: 50000" in out, out
check("L06 base twin Part B output matches prose", True, True)
out = run_variant("lab-E2-L06-1.py", [("COST_HIGH = 100_000", "COST_HIGH = 150_000")], "L06e1")
assert "best share on the grid: 0.30, agent takes high effort" in out, out
assert "principal profit at the best share, in cents: 525000" in out, out
check("L06 e1 twin prints share 0.30 and profit 525000", True, True)

print("\n".join(ok))
print(f"ALL {len(ok)} CHECKS PASSED")
