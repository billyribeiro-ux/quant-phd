"""Round-3 verifier: L04 identities with exact fractions, and the lab's printed numbers recomputed independently.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L03-L04-r3/l04_exact.py <checkout>
Exact part: random rational balance sheets. Each state is built from the balance-sheet items and the
assumptions named in the page; the cash-flow items are then derived by the page's own A1/A2/A4 wording.
Lab part: the twin's build_panel is exec'd (its final main() call removed) and the statistics are recomputed here.
"""

from __future__ import annotations

import random
import re
import sys
import types
from fractions import Fraction as F
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
rng = random.Random(2026_10_27)


def r() -> F:
    return F(rng.randint(1, 900), rng.randint(1, 40))


def signed() -> F:
    return F(rng.randint(-900, 900), rng.randint(1, 40))


def state(std_in_cl: bool) -> dict[str, F]:
    """Two year-ends, A1 and A2 built in; STD inside CL when std_in_cl (A3'), otherwise STD = 0 (A3)."""
    s: dict[str, F] = {}
    for suf in ("0", "1"):
        s["cash" + suf] = r()
        s["cao" + suf] = r()
        s["ppe" + suf] = r()
        s["onca" + suf] = r()
        s["cl" + suf] = r()
        s["ltd" + suf] = r()
        s["oncl" + suf] = r()
        s["std" + suf] = r() if std_in_cl else F(0)
        # CL includes STD (A3'); when A3 holds STD = 0 so CL carries no debt.
        s["cl" + suf] = s["cl" + suf] + s["std" + suf]
    s["capex"] = r()
    s["da"] = r()
    s["D"] = signed()
    # A2: PPE roll-forward with no disposals, impairments or acquisitions.
    s["ppe1"] = s["ppe0"] + s["capex"] - s["da"]
    return s


def ta(s: dict[str, F], suf: str) -> F:
    return s["cash" + suf] + s["cao" + suf] + s["ppe" + suf] + s["onca" + suf]


def liab(s: dict[str, F], suf: str) -> F:
    return s["cl" + suf] + s["ltd" + suf] + s["oncl" + suf]


def equity(s: dict[str, F], suf: str) -> F:
    return ta(s, suf) - liab(s, suf)


def ni_clean_surplus(s: dict[str, F]) -> F:
    # A1: E_t = E_{t-1} + NI_t - D_t  =>  NI_t = E_t - E_{t-1} + D_t
    return equity(s, "1") - equity(s, "0") + s["D"]


def run(label: str, n: int, cfi_offset: bool, std_in_cl: bool, cff_with_std: bool) -> dict[str, int]:
    """Check NI - CFO against the page's formula in each assumption set. Returns failure counts."""
    fails = {"prop22_form": 0, "section5_form": 0, "gap_has_no_std": 0}
    for _ in range(n):
        s = state(std_in_cl)
        ni = ni_clean_surplus(s)
        dcash = s["cash1"] - s["cash0"]
        dltd = s["ltd1"] - s["ltd0"]
        dstd = s["std1"] - s["std0"]
        # A4: dCash = CFO + CFI + CFF; CFI = -capex (+ offset if the test perturbs CFI)
        cfi = -s["capex"] + (F(1) if cfi_offset else F(0))
        cff = (dltd + dstd - s["D"]) if cff_with_std else (dltd - s["D"])
        cfo = dcash - cfi - cff
        dca = (s["cao1"] - s["cao0"]) + dcash  # current assets = cash + other current assets
        dcl = s["cl1"] - s["cl0"]
        donca = s["onca1"] - s["onca0"]
        doncl = s["oncl1"] - s["oncl0"]
        avg_ta = (ta(s, "0") + ta(s, "1")) / 2
        da = s["da"]
        lhs = ni - cfo
        # Page's Section 5 formula (with STD term) and Proposition 2.2 form (without).
        form_p22 = (dca - dcash) - dcl - da + donca - doncl
        form_s5 = form_p22 + dstd
        if lhs != form_p22:
            fails["prop22_form"] += 1
        if lhs != form_s5:
            fails["section5_form"] += 1
        cf_measure = lhs / avg_ta
        bs_measure = ((dca - dcash) - dcl - da) / avg_ta
        if cf_measure - bs_measure != (donca - doncl) / avg_ta:
            fails["gap_has_no_std"] += 1
    print(f"{label}: n={n} failures {fails}")
    return fails


N = 3000
# Proposition 2.2 under A1 to A4 (STD = 0): the Proposition 2.2 form must hold exactly.
run("A1-A4 (STD=0), CFF = dLTD - D, CFI = -capex", N, False, False, False)
# Section 5 with STD inside CL, the page's A3' and A4' (CFF includes dSTD); CFI = -capex kept from A4.
run("A1,A2,A3',A4' (CFF includes dSTD), CFI = -capex", N, False, True, True)
# Same but A4 as literally written (CFF without dSTD) while STD sits in CL.
run("A3' with A4 literal (CFF = dLTD - D)", N, False, True, False)
# Perturbation: CFI not equal to -capex (the page's A4' wording does not state CFI = -capex).
run("A3',A4' with CFI = -capex + 1 (perturbed)", 200, True, True, True)

# Scale invariance (Proposition 4.1) on a random state: multiply all money items by k.
bad41 = 0
for _ in range(2000):
    s = state(True)
    k = F(rng.randint(1, 50), rng.randint(1, 9))
    s2 = {key: v * k for key, v in s.items()}
    a1 = (ta(s, "0") + ta(s, "1")) / 2
    a2 = (ta(s2, "0") + ta(s2, "1")) / 2
    ni1, ni2 = ni_clean_surplus(s), ni_clean_surplus(s2)
    if ni1 / a1 != ni2 / a2:
        bad41 += 1
print("Prop 4.1 scale failures (ratio NI/avgTA, 2000 draws):", bad41)

# Proposition 3.1 under A1 to A4: NI - CFO = dNOA - capex with STD = 0.
bad31 = 0
for _ in range(3000):
    s = state(False)
    ni = ni_clean_surplus(s)
    dcash = s["cash1"] - s["cash0"]
    cfo = dcash + s["capex"] - (s["ltd1"] - s["ltd0"]) + s["D"]
    noa = lambda suf: s["cao" + suf] + s["ppe" + suf] + s["onca" + suf] - s["cl" + suf] - s["oncl" + suf]
    if ni - cfo != (noa("1") - noa("0")) - s["capex"]:
        bad31 += 1
print("Prop 3.1 failures (3000 draws):", bad31)

# Lab recomputation with numpy (independent statistics on the twin's panel).
src = (root / "tests/labs/AC2/lab-AC2-L04-1.py").read_text(encoding="utf-8")
src = re.sub(r"^main\(\)\s*$", "", src, flags=re.M)
mod = types.ModuleType("twin_L04")
sys.modules["twin_L04"] = mod
exec(compile(src, "lab-AC2-L04-1.py", "exec"), mod.__dict__)
build_panel = mod.__dict__["build_panel"]
average_total_assets = mod.__dict__["average_total_assets"]
cfo_from_balance_sheet = mod.__dict__["cfo_from_balance_sheet"]

gen = np.random.default_rng(2604)
moving = build_panel(gen, 400, moving=True)
cf = (moving.ni - cfo_from_balance_sheet(moving)) / average_total_assets(moving)
ta_avg = average_total_assets(moving)
bs = ((moving.ca_other1 - moving.ca_other0) - (moving.cl1 - moving.cl0) - moving.dep) / ta_avg
print(f"cash-flow mean {cf.mean():+.6f} sd(ddof1) {cf.std(ddof=1):.6f}")
print(f"balance-sheet mean {bs.mean():+.6f} sd(ddof1) {bs.std(ddof=1):.6f}")
print(f"mean difference cf-bs {cf.mean() - bs.mean():+.6f}")
r_ = float(np.corrcoef(cf, bs)[0, 1])
print(f"correlation {r_:.8f}  r^2 {r_**2:.8f}  1-r^2 {1 - r_**2:.8f}")
gap = cf - bs
print(f"share |gap|>0.01: {float(np.mean(np.abs(gap) > 0.01)):.7f}")
print(f"var(gap)/var(cf) ddof1 {float(np.var(gap, ddof=1) / np.var(cf, ddof=1)):.8f}  ddof0 {float(np.var(gap) / np.var(cf)):.8f}")
# Residual share of cf regressed on bs (least squares with intercept)
X = np.column_stack([np.ones_like(bs), bs])
beta, *_ = np.linalg.lstsq(X, cf, rcond=None)
res = cf - X @ beta
print(f"residual variance share of cf on bs: {float(np.var(res) / np.var(cf)):.8f}")
ident = (cf - bs) * ta_avg - ((moving.onca1 - moving.onca0) - (moving.oncl1 - moving.oncl0))
print(f"max |identity residual| {float(np.max(np.abs(ident))):.3e}")
