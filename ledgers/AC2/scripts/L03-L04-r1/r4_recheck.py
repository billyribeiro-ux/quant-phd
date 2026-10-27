"""Independent checks for AC2 L04 (run: python -I -W error <this file> <checkout>).

Part A: exact rational (fractions.Fraction) random tests of Proposition 2.2, Corollary 2.3, Proposition 3.1,
        the short-term-debt remark (Section 5), Proposition 4.1 and the printed M1-M4, E1-E3 values.
        Each random state is built from the balance sheet and the stated A1-A4 (or the STD variant), with the
        cash-flow statement derived from A4 and NI from A1; nothing is taken from the lab.
Part B: the lab's own numbers at full precision, and the E3 claim (remaining share of variance is the non-current gap).
"""
import random
import sys
import types
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
rng = random.Random(7)


def r() -> F:
    return F(rng.randint(-400, 400), rng.randint(1, 40))


def state(std: bool):
    """Return (year0, year1, flows) with independent random balance sheets; cash, CL etc. are free draws."""
    s = {}
    for t in (0, 1):
        s[t] = dict(
            cash=F(rng.randint(1, 300)),
            caO=r() + 400,
            ppe=F(rng.randint(100, 900)),
            onca=r() + 100,
            cl_op=r() + 200,
            std=(F(rng.randint(0, 120)) if std else F(0)),
            ltd=F(rng.randint(50, 400)),
            oncl=r() + 60,
        )
    capex = F(rng.randint(0, 200))
    da = F(rng.randint(0, 80))
    dist = r()
    s[1]["ppe"] = s[0]["ppe"] + capex - da  # A2
    # Clean surplus: E1 = E0 + NI - D.  Equity is the balance-sheet residual (A1 and the balance sheet fix NI).
    def ta(x):
        return x["cash"] + x["caO"] + x["ppe"] + x["onca"]

    def liab(x):
        return x["cl_op"] + x["std"] + x["ltd"] + x["oncl"]

    E0 = ta(s[0]) - liab(s[0])
    E1 = ta(s[1]) - liab(s[1])
    NI = E1 - E0 + dist
    # Cash-flow statement (A4): CFO + CFI + CFF = dCash, CFI = -capex, CFF = dLTD + dSTD - D
    dcash = s[1]["cash"] - s[0]["cash"]
    dstd = s[1]["std"] - s[0]["std"]
    cff = (s[1]["ltd"] - s[0]["ltd"]) + dstd - dist
    cfo = dcash + capex - cff
    avg_ta = (ta(s[0]) + ta(s[1])) / 2
    return s, dict(NI=NI, CFO=cfo, capex=capex, da=da, avg_ta=avg_ta, dist=dist, dcash=dcash, dstd=dstd)


def ac_cf(s, f):
    return (f["NI"] - f["CFO"]) / f["avg_ta"]


def ac_bs(s, f):
    d = lambda k: s[1][k] - s[0][k]
    dca = (s[1]["caO"] + s[1]["cash"]) - (s[0]["caO"] + s[0]["cash"])
    dcl = (s[1]["cl_op"] + s[1]["std"]) - (s[0]["cl_op"] + s[0]["std"])
    return ((dca - f["dcash"]) - dcl - f["da"]) / f["avg_ta"]


fails = 0
for trial in range(2000):
    # Part A1: A1-A4 without debt in CL (std=0): identity exact, gap = (dONCA - dONCL)/avgTA exact
    s, f = state(std=False)
    d = lambda k: s[1][k] - s[0][k]
    lhs = f["NI"] - f["CFO"]
    rhs2 = (d("caO") + d("cash") - f["dcash"]) - (d("cl_op")) - f["da"] + (d("onca") - d("oncl"))
    if lhs != rhs2:
        fails += 1
    if ac_cf(s, f) - ac_bs(s, f) != (d("onca") - d("oncl")) / f["avg_ta"]:
        fails += 1
    # Prop 3.1: NI - CFO = dNOA - capex (STD = 0)
    noa = lambda x: x["caO"] + x["ppe"] + x["onca"] - x["cl_op"] - x["oncl"]
    if lhs != (noa(s[1]) - noa(s[0])) - f["capex"]:
        fails += 1
    # Part A2: STD inside CL: gap = (dSTD + dONCA - dONCL)/avgTA
    s2, f2 = state(std=True)
    d2 = lambda k: s2[1][k] - s2[0][k]
    if ac_cf(s2, f2) - ac_bs(s2, f2) != (d2("std") + d2("onca") - d2("oncl")) / f2["avg_ta"]:
        fails += 1
    # Prop 4.1 scale invariance: multiply all money by k
    k = F(rng.randint(2, 50))
    s3 = {t: {kk: vv * k for kk, vv in s[t].items()} for t in (0, 1)}
    f3 = {kk: (vv * k if kk != "x" else vv) for kk, vv in f.items()}
    if ac_cf(s3, f3) != ac_cf(s, f) or ac_bs(s3, f3) != ac_bs(s, f):
        fails += 1
print("Part A exact-arithmetic failures over 2000 random states:", fails)

# M1: AC^BS = 10/1600; M2: AC^CF = -30/1600; M3 gap 20/1600; M4 gap 35/1600
print("M1", F(60 - 20 - 30, 1600), float(F(60 - 20 - 30, 1600)))
print("M2", F(120 - 150, 1600), float(F(120 - 150, 1600)))
print("M3", F(30 - 10, 1600), float(F(30 - 10, 1600)), "AC_CF", float(F(10, 1600) + F(20, 1600)))
print("M4", float(F(15 + 30 - 10, 1600)))

# Part B: lab numbers at full precision
src = (root / "tests/labs/AC2/lab-AC2-L04-1.py").read_text(encoding="utf-8")
src = src[: src.rindex("main()")]
mod = types.ModuleType("twinL04")
sys.modules["twinL04"] = mod
exec(compile(src, "twinL04", "exec"), mod.__dict__)
import numpy as np  # noqa: E402

clean = mod.build_panel(np.random.default_rng(2604), 400, moving=False)
moving = mod.build_panel(np.random.default_rng(2604), 400, moving=True)
cf = mod.accruals_cash_flow(moving)
bs = mod.accruals_balance_sheet(moving)
print("moving means cf, bs, diff:", cf.mean(), bs.mean(), cf.mean() - bs.mean())
print("corr:", np.corrcoef(cf, bs)[0, 1], " r^2:", np.corrcoef(cf, bs)[0, 1] ** 2)
print("share |gap|>0.01:", np.mean(np.abs(cf - bs) > 0.01))
gap = cf - bs
print("var(gap)/var(cf):", gap.var(ddof=1) / cf.var(ddof=1), " var(gap)/var(bs):", gap.var(ddof=1) / bs.var(ddof=1))
# share of var(cf) left unexplained by a linear regression on bs (1 - r^2)
beta = np.cov(cf, bs, ddof=1)[0, 1] / bs.var(ddof=1)
resid = cf - (cf.mean() + beta * (bs - bs.mean()))
print("1-r^2 share (resid var / var(cf)):", resid.var(ddof=1) / cf.var(ddof=1))
print("var(gap)/var(cf) vs 1-r^2 differ? ", abs(gap.var(ddof=1) / cf.var(ddof=1) - resid.var(ddof=1) / cf.var(ddof=1)))
print("clean max |cf-bs|:", np.max(np.abs(mod.accruals_cash_flow(clean) - mod.accruals_balance_sheet(clean))))
