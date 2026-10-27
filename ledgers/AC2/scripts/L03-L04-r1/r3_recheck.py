"""Independent re-derivation of every L03 number (AC2 L03). Run: python -I -W error <this file> <checkout>.

Loads the twin's functions (make_filer, standardize) by exec of the twin source minus its final main() call,
then recomputes ROIC from first principles (no call to the lab's roic) at full precision.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "tests/labs/AC2/lab-AC2-L03-1.py").read_text(encoding="utf-8")
src = src[: src.rindex("main()")]
import types
mod = types.ModuleType("twin")
sys.modules["twin"] = mod
ns = mod.__dict__
exec(compile(src, "twin", "exec"), ns)
filer = ns["make_filer"]()
st = ns["standardize"](filer)
ends = list(st)


def ic(row):  # invested capital = equity + LTD - cash (independent formula)
    return row["equity"] + row["long_term_debt"] - row["cash"]


def roic_indep(table, end, tau, prev):
    nopat = table[end]["operating_income"] * (1 - tau)
    avg = (ic(table[end]) + ic(table[prev])) / 2
    return nopat / avg


M = 1e6
print("year-end IC (USD m):", {e: round(ic(st[e]) / M, 3) for e in ends if "long_term_debt" in st[e]})
for end, prev in [("2022-12-31", "2021-12-31"), ("2023-12-31", "2022-12-31"), ("2024-12-31", "2023-12-31")]:
    print(end, "ROIC at 0,.15,.21,.25,.30:", [round(roic_indep(st, end, t, prev), 6) for t in (0, 0.15, 0.21, 0.25, 0.30)])
e, p = "2023-12-31", "2022-12-31"
avg = (ic(st[e]) + ic(st[p])) / 2
print("FY2023 avg IC (USD m):", avg / M, " NOPAT25:", st[e]["operating_income"] * 0.75 / M)
print("FY2023 ROIC25 avg:", roic_indep(st, e, 0.25, p), " year-end:", st[e]["operating_income"] * 0.75 / ic(st[e]))
nc = {k: dict(v) for k, v in st.items()}
for k in nc:
    nc[k]["cash"] = 0.0
print("FY2023 ROIC25 cash not netted:", roic_indep(nc, e, 0.25, p))
print("cash-netted vs not netted, % higher:", (roic_indep(st, e, 0.25, p) / roic_indep(nc, e, 0.25, p) - 1) * 100)
hyp = {k: dict(v) for k, v in st.items()}
for k in hyp:
    if "long_term_debt" in hyp[k]:
        hyp[k]["long_term_debt"] += 50 * M
print("hypothetical 50m STD, FY2023 ROIC25:", roic_indep(hyp, e, 0.25, p))
print("implied rate 1-NI/OI:", [round(1 - st[k]["net_income"] / st[k]["operating_income"], 6) for k in ends])
print("IC growth 2022,2023,2024 (%):", [round((ic(st[b]) / ic(st[a]) - 1) * 100, 3) for a, b in [("2021-12-31", "2022-12-31"), ("2022-12-31", "2023-12-31"), ("2023-12-31", "2024-12-31")]])
# E1: decomposition 2023 -> 2024 at 25%
n23 = st["2023-12-31"]["operating_income"] * 0.75
n24 = st["2024-12-31"]["operating_income"] * 0.75
a23 = (ic(st["2023-12-31"]) + ic(st["2022-12-31"])) / 2
a24 = (ic(st["2024-12-31"]) + ic(st["2023-12-31"])) / 2
print("E1 NOPAT change %:", (n24 / n23 - 1) * 100, " avgIC 2024 (USD m):", a24 / M, " avgIC change %:", (a24 / a23 - 1) * 100)
print("E1 ROIC ratio:", (n24 / a24) / (n23 / a23), " ROIC fall %:", ((n24 / a24) / (n23 / a23) - 1) * 100)
print("E1 product check (1+dN)/(1+dIC):", (n24 / n23) / (a24 / a23))
# E2: tax rate giving 10% for 2024 at zero tax
r0_24 = roic_indep(st, "2024-12-31", 0, "2023-12-31")
print("2024 ROIC at 0 tax:", r0_24, " tau for 10%:", 1 - 0.10 / round(r0_24, 4), " exact:", 1 - 0.10 / r0_24)
print("ROIC 2024 at .15,.21:", roic_indep(st, "2024-12-31", 0.15, "2023-12-31"), roic_indep(st, "2024-12-31", 0.21, "2023-12-31"))
print("Remark 1.2 printed: 0.1349 -> 0.1287 ; computed:", round(roic_indep(st, e, 0.25, p), 4), round(roic_indep(hyp, e, 0.25, p), 4))
print("Example 3.3 year-end ROIC:", round(st[e]["operating_income"] * 0.75 / ic(st[e]), 4))
print("misc gap %:", (roic_indep(st, e, 0.25, p) / (st[e]["operating_income"] * 0.75 / ic(st[e])) - 1) * 100)
