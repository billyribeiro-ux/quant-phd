"""Round-4 recomputation of L01/L02 numeric claims. Loads the lab twins without their trailing main() call."""
import math, sys, types
from datetime import date

def load(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    assert src.rstrip().endswith("main()")
    src = src.rstrip()[: -len("main()")]
    mod = types.ModuleType("twin")
    sys.modules["twin"] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod

R = "/tmp/verify-ac2r4-l12/tests/labs/AC2/"
L1 = load(R + "lab-AC2-L01-1.py")
L2 = load(R + "lab-AC2-L02-1.py")

# ---- L01 truth values (original, unrestated) for FY2022 revenue and the E2 percentage
rev_orig = None
f = L1.make_filer()
g = f["facts"]["us-gaap"]
# original FY2022 revenue: the 10-K filed 2023-02-15 for end 2022-12-31 with fp FY
vals = []
for tag, block in g.items():
    if tag in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"):
        for row in block["units"].get("USD", []):
            if row["end"] == "2022-12-31" and row["fp"] == "FY":
                vals.append((row["val"], row["form"], row["filed"], row["accn"], row.get("start")))
print("L01 FY2022 revenue rows:", vals)
orig = [v for v in vals if v[1] == "10-K" and v[2] == "2023-02-15"][0][0]
restated = [v for v in vals if v[1] == "10-K/A"][0][0]
print("orig", orig, "restated", restated, "pct change exact-ratio", (restated / orig - 1) * 100)
print("13.6 / 1131.9 in %:", 13.6 / 1131.9 * 100)
print("generator constant 1.012 -> pct", (1.012 - 1) * 100)
# the 10-Q and Q4 durations
for tag, block in g.items():
    for unit, rows in block["units"].items():
        for row in rows:
            if row["form"] != "10-K" or row["fp"] != "FY":
                if "start" in row:
                    d = (date.fromisoformat(row["end"]) - date.fromisoformat(row["start"])).days
                    print("non-annual flow row", tag, row["form"], row["fp"], row["end"], "duration", d)
# years and the 10-Q row count per year
print("L01 observation counts", L1.observation_counts(L1._us_gaap(f)))

# ---- L02 numbers
S = L2.standardize(L2.make_filer())
end = "2022-12-31"
def dp(st, e):
    return L2.dupont(st, e)
for e in ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]:
    d = dp(S, e)
    print(e, {k: round(v, 6) for k, v in d.items()})
d23, d24 = dp(S, "2023-12-31"), dp(S, "2024-12-31")
print("ROE 2023 unrounded", d23["roe"], "2024", d24["roe"])
lt = math.log(d24["roe"] / d23["roe"])
print("log total", lt)
for k in ("net_margin", "asset_turnover", "leverage"):
    s = math.log(d24[k] / d23[k])
    print(k, "log", s, "share %", 100 * s / lt)
print("Example 3.3 product 2023 (rounded factors):", 0.1179 * 0.8701 * 1.6936)
print("Example 3.3 product 2023 (unrounded):", d23["net_margin"] * d23["asset_turnover"] * d23["leverage"], "roe", d23["roe"])
# 2022 items
y = "2022-12-31"
d22 = dp(S, y)
print("2022 avg equity", L2._average(S, y, "equity") / 1e6, "avg assets", L2._average(S, y, "total_assets") / 1e6)
ye = S[y]["net_income"] / S[y]["equity"]
print("2022 year-end ROE", ye, "ratio", d22["roe"] / ye - 1, "NI", S[y]["net_income"] / 1e6, "rev", S[y]["revenue"] / 1e6, "eq", S[y]["equity"] / 1e6)
mism = d22["net_margin"] * (S[y]["revenue"] / S[y]["total_assets"]) * d22["leverage"]
print("mismatch product", mism, "roe", d22["roe"])
print("2022 net margin as filed", S[y]["net_income"] / (1131.9e6), "restated", d22["net_margin"])
S_asof = L2.standardize(L2.make_filer(), as_of="2023-06-30")
print("as-of 2023-06-30 rev 2022", S_asof[y]["revenue"], "NM", S_asof[y]["net_income"] / S_asof[y]["revenue"])
print("DSO 2022 restated", dp and L2.days_sales_outstanding(S, y), "as filed-rev DSO", L2.days_sales_outstanding(S_asof, y))
print("receivables 2022 truth-based", S[y]["receivables"] / 1e6, "0.12*orig rev", 0.12 * S_asof[y]["revenue"] / 1e6)
print("DSO constant check", [round(L2.days_sales_outstanding(S, e), 4) for e in S])
print("Remark 2.1 factor at g from year-end equity", S[y]["equity"] / S["2021-12-31"]["equity"] - 1)
g_eq = S[y]["equity"] / S["2021-12-31"]["equity"]
print("factor 2(1+g)/(2+g) with g=", g_eq - 1, "=", 2 * g_eq / (1 + g_eq))
