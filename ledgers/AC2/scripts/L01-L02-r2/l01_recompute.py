"""Independent recomputation of the numbers quoted in L01 (round 2). Run: python -I this.py <checkout>."""
import sys
from datetime import date
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "tests/labs/AC2/lab-AC2-L01-1.py").read_text(encoding="utf-8")
src = src.rsplit("main()", 1)[0]  # keep definitions, drop the printing main()
ns: dict = {}
exec(compile(src, "lab-AC2-L01-1-defs", "exec"), ns)
make_filer, standardize, select = ns["make_filer"], ns["standardize"], ns["select"]
f = make_filer()
gaap = f["facts"]["us-gaap"]

# 1. Quarter durations (Remark 2.2): end minus start, by quarter, 2023 and 2024 (leap)
def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days
print("Q1 2023 (1 Jan-31 Mar) days:", days("2023-01-01", "2023-03-31"))
print("Q2 2023 days:", days("2023-03-31", "2023-06-30"), "| Q3 2023:", days("2023-06-30", "2023-09-30"),
      "| Q4 2023 (1 Oct-31 Dec):", days("2023-09-30", "2023-12-31"))
print("Q1 2024 (leap) days:", days("2023-12-31", "2024-03-31"))
print("2022-12-31 to 2023-12-31:", days("2022-12-31", "2023-12-31"))

# 2. Row durations actually in the file
q_rows = [r for r in gaap["Revenues"]["units"]["USD"] if r["form"] == "10-Q"]
q4 = [r for r in gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]
      if r.get("fp") == "Q4"]
print("10-Q rows:", [(r["start"], r["end"], days(r["start"], r["end"])) for r in q_rows][:1],
      "| Q4 rows:", [(r["start"], r["end"], days(r["start"], r["end"])) for r in q4])

# 3. Restatement percent, exact from integers
rev22_filed = [r for r in gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]
               if r["end"] == "2022-12-31" and r["form"] == "10-K"]
rev22_ka = [r for r in gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]
            if r["form"] == "10-K/A"]
orig = rev22_filed[0]["val"]
amend = rev22_ka[0]["val"]
print("FY2022 original", orig, "amended", amend, "pct", (amend - orig) / orig * 100,
      "diff USD m", (amend - orig) / 1e6)
print("printed diff/value %:", 13.6 / 1131.9 * 100)

# 4. Values at each M2 cut-off (the FY2022 revenue for the 2022 year end)
for cut in ("2023-02-14", "2023-02-15", "2024-02-29", "2023-06-30", None):
    t = standardize(f, cut)
    print("cut-off", cut, "2022 revenue:", t.get("2022-12-31", {}).get("revenue"))

# 5. FY2024 10-K filed date and M3 cut-offs
for cut in ("2025-01-31", "2025-02-15"):
    t = standardize(f, cut)
    print("cut-off", cut, "has 2024 year end:", "2024-12-31" in t)

# 6. Counts by form and items per year end
from collections import Counter
c = Counter(r["form"] for block in gaap.values() for rows in block["units"].values() for r in rows)
print("counts by form:", dict(sorted(c.items())))
t = standardize(f)
print("items per year end:", {k: len(v) for k, v in t.items()})
missing = set(ns["ITEMS"]) - set(t["2020-12-31"])
print("items missing for 2020:", sorted(missing))

# 7. Q4 row duration check and 10-K/A fp
print("10-K/A fp:", [r["fp"] for block in gaap.values() for rows in block["units"].values()
                     for r in rows if r["form"] == "10-K/A"])
# 8. Example 4.2: revenue tag per period end
sel = select(f)["revenue"]
print("revenue tags:", {e.isoformat(): tag for e, (tag, _o) in sel.items()})
# 9. Bool/infinite val raise (malformed-input claim)
for bad in (True, float("inf")):
    x = {"facts": {"us-gaap": {"Assets": {"units": {"USD": [
        {"end": "2023-12-31", "val": bad, "filed": "2024-02-15", "form": "10-K", "fp": "FY"}]}}}}}
    try:
        standardize(x)
        print("no error for", bad)
    except ValueError as e:
        print("ValueError for", bad, ":", e)
