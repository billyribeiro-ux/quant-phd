"""Round-2 independent checks for AC2 L04: exact-fraction identities on random states, and the
printed statistics recomputed from the twin's generator (data only; statistics computed here)."""
import contextlib
import io
import random
import runpy
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(root / "tests/labs/AC2/lab-AC2-L04-1.py"), run_name="twin")
build_panel = g["build_panel"]

rng = random.Random(11)
def r():
    return F(rng.randint(-2000, 2000), rng.randint(1, 60))

# Prop 2.2 under A1-A4 (no STD). Generate states; define flows by the assumptions; check identity exactly.
def check_prop22(with_std):
    cash0, cash1 = r(), r()
    cao0, cao1 = r(), r()
    ppe0 = r(); capex = r(); da = r()
    ppe1 = ppe0 + capex - da                     # A2
    onca0, onca1, oncl0, oncl1 = r(), r(), r(), r()
    cl0, cl1 = r(), r()
    ltd0, ltd1 = r(), r()
    std0, std1 = (r(), r()) if with_std else (F(0), F(0))
    # balance sheets: L = CL + LTD + ONCL, CL includes STD when with_std (A3 relaxed)
    ta0 = cash0 + cao0 + ppe0 + onca0
    ta1 = cash1 + cao1 + ppe1 + onca1
    L0 = (cl0 + std0) + ltd0 + oncl0
    L1 = (cl1 + std1) + ltd1 + oncl1
    E0 = ta0 - L0; E1 = ta1 - L1
    D = r()                                       # distributions
    NI = (E1 - E0) + D                            # A1 clean surplus
    # A4: dCash = CFO + CFI + CFF, CFI = -capex, CFF = dLTD + dSTD - D (STD term only if with_std)
    dLTD = ltd1 - ltd0; dSTD = std1 - std0
    CFF = dLTD + dSTD - D
    CFI = -capex
    CFO = (cash1 - cash0) - CFI - CFF
    lhs = NI - CFO
    dCA = (cao1 + cash1) - (cao0 + cash0)
    dCash = cash1 - cash0
    dCL = (cl1 + std1) - (cl0 + std0)
    dONCA = onca1 - onca0; dONCL = oncl1 - oncl0
    rhs_prop22 = (dCA - dCash) - dCL - da + (dONCA - dONCL) + dSTD
    return lhs == rhs_prop22, lhs - rhs_prop22, rhs_prop22 - (rhs_prop22 - dSTD) if with_std else None, lhs, rhs_prop22

ok = 0
for _ in range(3000):
    res = check_prop22(False)
    ok += res[0]
print("Prop 2.2 (A1-A4, no STD) exact identity holds in", ok, "of 3000")

ok = 0
for _ in range(3000):
    res = check_prop22(True)
    ok += res[0]
print("STD-in-CL identity (dSTD term included, exact) holds in", ok, "of 3000")
# The remark's claimed formula: AC^CF - AC^BS = (dSTD + dONCA - dONCL)/TA  with AC^BS = (dCA - dCash - dCL - DA)/TA
# Equivalent exact check: lhs - (dCA - dCash - dCL - da) == dSTD + dONCA - dONCL  (STD in CL)
def check_gap():
    rng2 = random.Random(3)
    bad = 0
    for _ in range(2000):
        cash0, cash1, cao0, cao1 = (F(rng2.randint(-900, 900), rng2.randint(1, 30)) for _ in range(4))
        ppe0, capex, da = (F(rng2.randint(-900, 900), rng2.randint(1, 30)) for _ in range(3))
        ppe1 = ppe0 + capex - da
        onca0, onca1, oncl0, oncl1, cl0, cl1, ltd0, ltd1, std0, std1, D = (F(rng2.randint(-900, 900), rng2.randint(1, 30)) for _ in range(11))
        ta0 = cash0 + cao0 + ppe0 + onca0; ta1 = cash1 + cao1 + ppe1 + onca1
        E0 = ta0 - ((cl0 + std0) + ltd0 + oncl0); E1 = ta1 - ((cl1 + std1) + ltd1 + oncl1)
        NI = E1 - E0 + D
        CFF = (ltd1 - ltd0) + (std1 - std0) - D
        CFO = (cash1 - cash0) + capex - CFF
        lhs = NI - CFO
        bs = (cao1 - cao0) - ((cl1 + std1) - (cl0 + std0)) - da  # (dCA - dCash) - dCL - DA
        bad += (lhs - bs) != (std1 - std0) + (onca1 - onca0) - (oncl1 - oncl0)
    return bad
print("Section 5 gap formula failures (exact, 2000 states):", check_gap())

# A3-violating case with A4 unchanged (CFF without dSTD): does the page's (A4) statement hold? Show mismatch.
def check_a4_as_written():
    cash0, cash1, cao0, cao1, ppe0, capex, da, onca0, onca1, oncl0, oncl1, cl0, cl1, ltd0, ltd1, std0, std1, D = (F(x) for x in (100, 130, 50, 60, 200, 30, 20, 40, 45, 10, 12, 80, 90, 150, 160, 25, 40, 5))
    ppe1 = ppe0 + capex - da
    ta0 = cash0 + cao0 + ppe0 + onca0; ta1 = cash1 + cao1 + ppe1 + onca1
    E0 = ta0 - ((cl0 + std0) + ltd0 + oncl0); E1 = ta1 - ((cl1 + std1) + ltd1 + oncl1)
    NI = E1 - E0 + D
    CFF_as_written = (ltd1 - ltd0) - D            # A4 as written on the page (no dSTD)
    CFO_as_written = (cash1 - cash0) + capex - CFF_as_written
    return NI - CFO_as_written, (cash1 - cash0) + capex - (ltd1 - ltd0) + D
v = check_a4_as_written()
print("NI-CFO under A4-as-written:", v[0], "; its implied CFO:", v[1])

# Statistics of the lab's moving panel, computed here from the twin's build_panel output
def stats(p):
    ta0 = p.cash0 + p.ca_other0 + p.ppe0 + p.onca0
    ta1 = p.cash1 + p.ca_other1 + p.ppe1 + p.onca1
    avg = (ta0 + ta1) / 2
    cfo = (p.cash1 - p.cash0) + p.capex - (p.ltd1 - p.ltd0) + p.payout
    cf = (p.ni - cfo) / avg
    bs = ((p.ca_other1 - p.ca_other0) - (p.cl1 - p.cl0) - p.dep) / avg
    return cf, bs

for label, moving in (("moving", True), ("clean", False)):
    p = build_panel(np.random.default_rng(2604), 400, moving=moving)
    cf, bs = stats(p)
    print(label, "cf mean %+.6f sd %.6f | bs mean %+.6f sd %.6f" % (cf.mean(), cf.std(ddof=1), bs.mean(), bs.std(ddof=1)))
    if moving:
        r = np.corrcoef(cf, bs)[0, 1]
        print("correlation %.8f  r^2 %.8f  1-r^2 %.8f" % (r, r * r, 1 - r * r))
        gap = cf - bs
        print("var(gap)/var(cf) ddof=1 %.8f ; ddof=0 %.8f" % (np.var(gap, ddof=1) / np.var(cf, ddof=1), np.var(gap) / np.var(cf)))
        print("share |gap|>0.01: %.8f" % np.mean(np.abs(gap) > 0.01))
        print("mean(cf)-mean(bs) %.8f" % (cf.mean() - bs.mean()))
        # regression residual share of var(cf) on bs (should equal 1 - r^2)
        X = np.column_stack([np.ones_like(bs), bs]); b = np.linalg.lstsq(X, cf, rcond=None)[0]
        res = cf - X @ b
        print("residual var share of cf on bs (lstsq with intercept): %.8f" % (np.var(res) / np.var(cf)))
        # identity from the formula: gap = (dONCA - dONCL)/TA
        ta0 = p.cash0 + p.ca_other0 + p.ppe0 + p.onca0; ta1 = p.cash1 + p.ca_other1 + p.ppe1 + p.onca1
        avg = (ta0 + ta1) / 2
        print("max |gap - (dONCA-dONCL)/avg| = %.3e" % np.max(np.abs(gap - ((p.onca1 - p.onca0) - (p.oncl1 - p.oncl0)) / avg)))
