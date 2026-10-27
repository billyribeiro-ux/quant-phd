"""Round-3 verifier: exact-fraction re-derivation of every L03 number and proposition.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L03-L04-r3/l03_exact.py <checkout>
The twin's standardizer and filer are loaded by exec of the twin source with its final main() call removed;
every ROIC, invested capital, growth and rate figure below is then computed here with fractions.Fraction.
"""

from __future__ import annotations

import random
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "tests/labs/AC2/lab-AC2-L03-1.py").read_text(encoding="utf-8")
src = re.sub(r"^main\(\)\s*$", "", src, flags=re.M)
import types

mod = types.ModuleType("twin_L03")
sys.modules["twin_L03"] = mod
exec(compile(src, "lab-AC2-L03-1.py", "exec"), mod.__dict__)
ns = mod.__dict__
standardize = ns["standardize"]
make_filer = ns["make_filer"]
SEED = ns["SEED"]

table = standardize(make_filer(SEED))  # type: ignore[operator]
years = sorted(table)
print("period ends:", years)


def q(x: float | int | str) -> F:
    return F(str(x)) if isinstance(x, str) else F(x)


def ic(row: dict[str, float]) -> F:
    return F(row["equity"]) + F(row["long_term_debt"]) - F(row["cash"])


def r4(x: F) -> str:
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return str(d)


ICs: dict[str, F] = {}
for y in years:
    row = table[y]
    if "long_term_debt" in row:
        ICs[y] = ic(row)
    print(y, {k: row[k] for k in ("equity", "long_term_debt", "cash", "operating_income", "net_income") if k in row})
for y in years:
    if y in ICs:
        print(f"IC {y}: {float(ICs[y]):.4f}")

# Average IC and ROIC grid, exact.
rates = ["0", "0.15", "0.21", "0.25", "0.30"]
grid: dict[str, dict[str, F]] = {}
for i, y in enumerate(years):
    if i == 0 or years[i - 1] not in ICs or y not in ICs:
        continue
    avg = (ICs[y] + ICs[years[i - 1]]) / 2
    oi = F(table[y]["operating_income"])
    grid[y] = {t: oi * (1 - F(t)) / avg for t in rates}
    print(y, "avgIC", float(avg), "ROIC", {t: r4(grid[y][t]) for t in rates})
    print(y, "largest rel dev ROIC(t) vs ROIC(0)(1-t):", max(abs(grid[y][t] / (grid[y]["0"] * (1 - F(t))) - 1) for t in rates[1:]))
    implied = 1 - F(table[y]["net_income"]) / oi
    print(y, "implied rate 1-NI/OI:", float(implied), "(exact diff from 1/4:", float(implied - F(1, 4)), ")")

y23, y22 = "2023-12-31", "2022-12-31"
y24 = "2024-12-31"
avg23 = (ICs[y23] + ICs[y22]) / 2
oi23 = F(table[y23]["operating_income"])
roic23_25 = oi23 * F("0.75") / avg23
print("FY2023 ROIC 25% avg:", float(roic23_25), r4(roic23_25))
print("FY2023 year-end ROIC 25%:", float(oi23 * F("0.75") / ICs[y23]), r4(oi23 * F("0.75") / ICs[y23]))
print("gap avg vs year-end (%):", float((roic23_25 / (oi23 * F("0.75") / ICs[y23]) - 1) * 100))
# Cash not netted: IC' = E + D
cash23 = F(table[y23]["cash"])
ic_nc23 = ICs[y23] + cash23
avg_nc = (ic_nc23 + (ICs[y22] + F(table[y22]["cash"]))) / 2
r_nc = oi23 * F("0.75") / avg_nc
print("FY2023 25% cash not netted:", float(r_nc), r4(r_nc))
print("netted over not netted (%):", float((roic23_25 / r_nc - 1) * 100))
# 50m hypothetical short-term debt added to long-term debt in every year
ic23_h = ICs[y23] + F(50_000_000)  # the filer is in USD; 50 USD m
ic22_h = ICs[y22] + F(50_000_000)
r_h = oi23 * F("0.75") / ((ic23_h + ic22_h) / 2)
print("hypothetical +50m FY2023 25%:", float(r_h), r4(r_h))
# Growth
for a, b in ((y22, y23), (y23, y24)):
    pass
growth_years = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]
for a, b in zip(growth_years, growth_years[1:]):
    g = ICs[b] / ICs[a] - 1
    print(f"IC growth {a}->{b}: {float(g) * 100:.4f}%")
# E1: 2024 change
nopat23 = oi23 * F("0.75")
oi24 = F(table[y24]["operating_income"])
nopat24 = oi24 * F("0.75")
avg24 = (ICs[y24] + ICs[y23]) / 2
print("NOPAT 2023", float(nopat23), "NOPAT 2024", float(nopat24), "change %", float((nopat24 / nopat23 - 1) * 100))
print("avg IC 2023", float(avg23), "avg IC 2024", float(avg24), "change %", float((avg24 / avg23 - 1) * 100))
print("ROIC ratio exact", float((nopat24 / avg24) / (nopat23 / avg23)), "printed-form (1-0.222)/(1+0.077)", (1 - 0.222) / (1 + 0.077))
print("ROIC 2024 25% / 2023 25%:", float(grid[y24]["0.25"] / grid[y23]["0.25"]), "ROIC 2024 25%", r4(grid[y24]["0.25"]))
# E2: tax rate giving 10% in 2024
roic24_0 = grid[y24]["0"]
print("2024 ROIC at zero tax exact:", float(roic24_0), r4(roic24_0), "tau exact:", float(1 - F("0.10") / roic24_0))
print("tau with printed 0.1299:", float(1 - F("0.10") / F("0.1299")))
print("tau with 0.12989:", float(1 - F("0.10") / F("0.12989")))
print("2024 ROIC at 15,21 rows", r4(grid[y24]["0.15"]), r4(grid[y24]["0.21"]))
# Prop 2.2: ROIC(t2)/ROIC(t1) = (1-t2)/(1-t1) in the table
print("E2 printed 0.1299 vs exact", float(roic24_0))
