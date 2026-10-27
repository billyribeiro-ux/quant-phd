"""Round-4 independent check of the L04 lab numbers, the Remark 2.4 and Section 5 algebra, and the E2/E3 figures."""
import sys
import types
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
mod = types.ModuleType("lab_l04")
sys.modules["lab_l04"] = mod
ns = mod.__dict__
src = (root / "tests/labs/AC2/lab-AC2-L04-1.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
exec(compile(src, "lab-AC2-L04-1-nomain", "exec"), ns)
build_panel = ns["build_panel"]
acf = ns["accruals_cash_flow"]
abs_ = ns["accruals_balance_sheet"]

n = 400
mv = build_panel(np.random.default_rng(2604), n, moving=True)
cf = acf(mv)
bs = abs_(mv)
r = np.corrcoef(cf, bs)[0, 1]
print("r moving 2604 unrounded", r, "r^2", r * r, "1-r^2", 1 - r * r)
gap = cf - bs
print("var(gap)/var(cf) (ddof=1 both ratio)", np.var(gap, ddof=1) / np.var(cf, ddof=1), "ddof0", np.var(gap) / np.var(cf))
print("means cf, bs, diff", cf.mean(), bs.mean(), cf.mean() - bs.mean())
print("sd cf, bs (ddof1)", cf.std(ddof=1), bs.std(ddof=1))
for s in (2604, 2605, 2606):
    p = build_panel(np.random.default_rng(s), n, moving=True)
    g = acf(p) - abs_(p)
    print("seed", s, "share gap>0.01", float(np.mean(np.abs(g) > 0.01)))
print("gap mean over firms", gap.mean())

# Section 5 and Remark 2.4 algebra, tested on a random articulated panel with STD in CL.
rng = np.random.default_rng(7)
ok = {"A3p_A4lit": [], "A3p_A4p": [], "A3p_A4p_CFIwrong": [], "A3_A4lit": []}
for trial in range(300):
    m = 50
    size = np.exp(rng.normal(np.log(1000.0), 0.6, m))
    ca0 = size * rng.uniform(0.15, 0.3, m)
    ppe0 = size * rng.uniform(0.25, 0.5, m)
    onca0 = size * rng.uniform(0.05, 0.15, m)
    std0 = size * rng.uniform(0.01, 0.06, m)
    cl0 = size * rng.uniform(0.10, 0.20, m) + std0  # current liabilities include short-term debt
    ltd0 = size * rng.uniform(0.02, 0.12, m)
    oncl0 = size * rng.uniform(0.01, 0.04, m)
    cash0 = size * rng.uniform(0.05, 0.15, m)
    dep = ppe0 * rng.uniform(0.06, 0.12, m)
    capex = ppe0 * rng.uniform(0.05, 0.15, m)
    ppe1 = ppe0 + capex - dep
    cash1 = cash0 * np.exp(rng.normal(0.03, 0.15, m))
    ca1 = ca0 * (1 + rng.normal(0.08, 0.10, m))
    std1 = std0 * (1 + rng.normal(0, 0.3, m))
    cl1 = cl0 * (1 + rng.normal(0.05, 0.10, m))  # includes std1 below
    cl1 = cl1 - std0 + std1  # keep the non-debt part and replace debt by std1
    onca1 = onca0 * (1 + rng.normal(0, 0.2, m))
    oncl1 = oncl0 * (1 + rng.normal(0, 0.25, m))
    ltd1 = ltd0 * (1 + rng.normal(0.02, 0.10, m))
    payout = size * rng.normal(0.01, 0.02, m)
    eq0 = (cash0 + ca0 + ppe0 + onca0) - (cl0 + ltd0 + oncl0)
    eq1 = (cash1 + ca1 + ppe1 + onca1) - (cl1 + ltd1 + oncl1)
    ni = eq1 - eq0 + payout  # clean surplus A1
    # CFI and CFF choices
    for label, cfi_fn, cff in (
        ("A3p_A4lit", lambda: -capex, ltd1 - ltd0 - payout),
        ("A3p_A4p", lambda: -capex, (ltd1 - ltd0) + (std1 - std0) - payout),
        ("A3p_A4p_CFIwrong", lambda: -capex + 1.0, (ltd1 - ltd0) + (std1 - std0) - payout),
    ):
        cfi = cfi_fn()
        dcash = cash1 - cash0
        cfo = dcash - cfi - cff  # cash identity solved for CFO
        lhs = ni - cfo
        # Proposition 2.2 form (no STD term) and Section 5 form (with STD term)
        prop22 = (ca1 - ca0) - (cl1 - cl0) - dep + ((onca1 - onca0) - (oncl1 - oncl0))
        sec5 = (ca1 - ca0) - (cl1 - cl0) - dep + (((std1 - std0) + (onca1 - onca0) - (oncl1 - oncl0)))
        key = label
        ok.setdefault(key + "_prop22_fail", []).append(float(np.max(np.abs(lhs - prop22))) > 1e-6)
        ok.setdefault(key + "_sec5_fail", []).append(float(np.max(np.abs(lhs - sec5))) > 1e-6)
for k, v in ok.items():
    if k.endswith("_fail"):
        print(k, "draws failing", sum(v), "of", len(v))
for k in ("A3p_A4lit_prop22_fail", "A3p_A4p_sec5_fail", "A3p_A4p_CFIwrong_sec5_fail", "A3p_A4lit_sec5_fail"):
    if k in ok:
        print(k, "failures", sum(ok[k]), "of", len(ok[k]))
