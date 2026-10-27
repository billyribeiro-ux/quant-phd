"""Check the L01 prose claims about a REAL company-facts file (Apple, CIK 320193), read-only, from /tmp/ac2-v/l12/edgar.
Run: python -I l01_real_check.py <path-to-companyfacts.json>"""
import json
import sys
from collections import Counter, defaultdict
from datetime import date

d = json.load(open(sys.argv[1], encoding="utf-8"))
print("cik", d.get("cik"), "entityName", d.get("entityName"))
gaap = d["facts"]["us-gaap"]
print("us-gaap tags:", len(gaap))
forms = Counter()
for tag, block in gaap.items():
    for unit, rows in block.get("units", {}).items():
        for r in rows:
            forms[r.get("form")] += 1
print("forms (all tags):", forms.most_common(12))
print("10-K/A rows:", forms.get("10-K/A", 0))

# Repeated comparatives: same end date in several 10-K accns for Revenues tag
rev_tags = [t for t in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet") if t in gaap]
print("revenue tags present:", rev_tags)
for t in rev_tags:
    rows = gaap[t]["units"].get("USD", [])
    annual = [r for r in rows if r.get("form", "").startswith("10-K") and r.get("fp") == "FY"]
    by_end = defaultdict(set)
    for r in annual:
        by_end[r["end"]].add(r["accn"])
    multi = {e: len(a) for e, a in by_end.items() if len(a) > 1}
    fy_ends = sorted(by_end)[-6:]
    print(f"tag {t}: annual rows {len(annual)}, ends with >1 accn: {len(multi)} e.g. {list(multi.items())[:3]}")
    print("   recent FY ends:", fy_ends)
    # Q4 rows inside 10-K
    q4 = [r for r in rows if r.get("form", "").startswith("10-K") and r.get("fp") == "Q4"]
    print("   Q4 rows inside a 10-K:", len(q4), "example:", [(r.get("start"), r["end"], r["form"], r["fp"]) for r in q4[:2]])
    # durations of annual flows
    durs = Counter()
    for r in annual:
        if "start" in r:
            durs[(date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days] += 1
    print("   annual flow durations (days):", sorted(durs.items())[:12])

# 10-K/A restatement example for revenue
for t in rev_tags:
    amend = [r for r in gaap[t]["units"].get("USD", []) if r.get("form") == "10-K/A"]
    print("10-K/A rows under", t, len(amend), amend[:1])

# Ties: same tag, end, filed and accn but different val among annual rows (all tags)
ties = 0
for tag, block in gaap.items():
    for unit, rows in block.get("units", {}).items():
        groups = defaultdict(set)
        for r in rows:
            if r.get("form", "").startswith("10-K") and r.get("fp") == "FY":
                groups[(r["end"], r["filed"], r.get("accn", ""))].add(r["val"])
        ties += sum(1 for v in groups.values() if len(v) > 1)
print("annual (end, filed, accn) groups with different values, all tags:", ties)

# --- round 2 additions: fp values inside 10-K rows; NetIncomeLoss FY durations; 2023 quarter lengths
fp_counts = Counter(r.get("fp") for block in gaap.values() for rows in block.get("units", {}).values()
                    for r in rows if str(r.get("form", "")).startswith("10-K"))
print("fp values in 10-K rows (all tags):", fp_counts.most_common())
ni = [r for r in gaap["NetIncomeLoss"]["units"]["USD"] if r.get("form") == "10-K" and r.get("fp") == "FY" and "start" in r]
print("NetIncomeLoss 10-K FY durations (end minus start):",
      sorted(Counter((date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days for r in ni).items()))
quarters = {"Q1 2023": ("2023-01-01", "2023-03-31"), "Q2 2023": ("2023-04-01", "2023-06-30"),
            "Q3 2023": ("2023-07-01", "2023-09-30"), "Q4 2023": ("2023-10-01", "2023-12-31")}
print("2023 quarters, end minus period start (days):",
      {k: (date.fromisoformat(b) - date.fromisoformat(a)).days for k, (a, b) in quarters.items()})
print("FY lab rows 2023-01-01..2023-12-31 (end minus start):",
      (date.fromisoformat("2023-12-31") - date.fromisoformat("2023-01-01")).days)
