"""Independent recomputation of the numbers quoted in L02 (round 2). Run: python -I this.py <checkout>."""
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "tests/labs/AC2/lab-AC2-L02-1.py").read_text(encoding="utf-8").rsplit("main()", 1)[0]
ns: dict = {}
exec(compile(src, "lab-AC2-L02-1-defs", "exec"), ns)
standardize, dupont, days_sales = ns["standardize"], ns["dupont"], ns["days_sales_outstanding"]
f = ns["make_filer"]()
full = standardize(f)
asof = standardize(f, as_of="2023-06-30")
y = "2022-12-31"
print("2022 ROE, no cut-off:", round(dupont(full, y)["roe"], 6), " as of 2023-06-30:", round(dupont(asof, y)["roe"], 6))
print("2022 net margin, no cut-off:", round(dupont(full, y)["net_margin"], 6), " as of:", round(dupont(asof, y)["net_margin"], 6))
print("2022 NI, equity (no cut-off):", full[y]["net_income"], full[y]["equity"], " as of:", asof[y]["net_income"], asof[y]["equity"])

d = dupont(full, y)
mm = d["net_margin"] * (full[y]["revenue"] / full[y]["total_assets"]) * d["leverage"]
print("mismatch product 2022:", round(mm, 6), "roe:", round(d["roe"], 6))
ye = full[y]["net_income"] / full[y]["equity"]
print("year-end ROE 2022:", round(ye, 6), "avg/ye - 1 =", round(d["roe"] / ye - 1, 6))

printed = {"nm": (0.1179, 0.0874), "at": (0.8701, 0.8511), "lev": (1.6936, 1.6628), "roe": (0.1738, 0.1237)}
for k, (a, b) in printed.items():
    print("printed log change", k, round(math.log(b / a), 6))
e, l = dupont(full, "2023-12-31"), dupont(full, "2024-12-31")
for k in ("net_margin", "asset_turnover", "leverage", "roe"):
    print("unrounded log change", k, round(math.log(l[k] / e[k]), 6))
tot = math.log(l["roe"] / e["roe"])
print("shares", {k: round(100 * math.log(l[k] / e[k]) / tot, 2) for k in ("net_margin", "asset_turnover", "leverage")})
print("Example 3.3 product of printed factors:", round(0.1179 * 0.8701 * 1.6936, 6))
print("E1 changes:", round(0.1925 / 0.2100 - 1, 4), round(0.1738 / 0.1925 - 1, 4), round(0.1237 / 0.1738 - 1, 4))
print("DSO 2022 with restated revenue:", round(days_sales(full, y), 4),
      " by hand 43.80*1131.9/1145.5 =", round(43.80 * 1131.9 / 1145.5, 4))
g = 0.2
print("avg/ye equity", round((1 + 1 / (1 + g)) / 2, 6), "factor", round(2 * (1 + g) / (2 + g), 6))
print("1/0.9167:", round(1 / 0.9167, 6))
print("M1:", 750 / 280, 50 / 280, 0.1 * (500 / 750) * (750 / 280))
print("M2:", 120 / 900 * 365, 120 / 900 * 360, 365 / 360)
print("quiz Q2 leverage 750/280:", round(750 / 280, 4), " quiz Q4 2(1+g)/(2+g):", round(2.4 / 2.2, 4))
print("E3 DSO constant 0.12*365:", round(0.12 * 365, 2))
