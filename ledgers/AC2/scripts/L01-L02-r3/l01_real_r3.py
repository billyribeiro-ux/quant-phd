"""Round-3 check of L01 claims against the real company-facts file (read-only; path given as argv[1])."""
import json
import sys
from collections import Counter, defaultdict
from datetime import date

data = json.load(open(sys.argv[1], encoding="utf-8"))
print("cik", data.get("cik"), "entity", data.get("entityName"))
gaap = data["facts"]["us-gaap"]
print("taxonomies", list(data["facts"].keys()), "gaap tags", len(gaap))
print("units used by tags of interest:")
for tag in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "NetIncomeLoss", "Assets"]:
    b = gaap.get(tag)
    if b:
        print(" ", tag, {u: len(v) for u, v in b["units"].items()})
    else:
        print(" ", tag, "ABSENT")

def annual_rows(tag, unit="USD"):
    rows = gaap.get(tag, {}).get("units", {}).get(unit, [])
    return [r for r in rows if r.get("form", "").startswith("10-K") and r.get("fp") == "FY"]

# shape: keys of observations (all tags)
keys = Counter()
for block in gaap.values():
    for rows in block["units"].values():
        for r in rows:
            keys[tuple(sorted(r.keys()))] += 1
print("observation key sets (count):")
for k, n in keys.most_common(6):
    print(" ", n, k)

# tag switch
for tag in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"]:
    flows = [r for r in annual_rows(tag) if "start" in r]
    if flows:
        ends = sorted(r["end"] for r in flows)
        print(tag, "annual FY rows:", len(flows), "first end", ends[0], "last end", ends[-1])

# repeated comparatives: period ends with >1 distinct accn among annual rows
for tag in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "NetIncomeLoss"]:
    by_end = defaultdict(set)
    for r in annual_rows(tag):
        by_end[r["end"]].add(r.get("accn"))
    multi = {e: len(a) for e, a in by_end.items() if len(a) > 1}
    print(tag, "period ends:", len(by_end), "ends with >1 accn:", len(multi))

# restatements: 10-K/A rows
amend = Counter()
examples = []
for tag, block in gaap.items():
    for unit, rows in block["units"].items():
        for r in rows:
            if r.get("form") == "10-K/A":
                amend[tag] += 1
                if tag == "SalesRevenueNet" or tag == "Revenues" and len(examples) < 3:
                    examples.append((tag, r.get("end"), r.get("filed"), r.get("val"), r.get("start")))
print("10-K/A rows per tag (top):", amend.most_common(4), "total", sum(amend.values()))
print("examples:", examples[:5])

# durations of annual flow rows under NetIncomeLoss
durs = Counter()
for r in annual_rows("NetIncomeLoss"):
    if "start" in r:
        durs[(date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days] += 1
print("NetIncomeLoss FY durations (days: count):", sorted(durs.items()))
fp = Counter(r.get("fp") for rows in gaap["NetIncomeLoss"]["units"]["USD"] for r in [rows] ) if False else None
fp_by_form = Counter((r.get("form"), r.get("fp")) for block in gaap.values() for rows in block["units"].values() for r in rows)
print("form, fp counts (top 8):", fp_by_form.most_common(8))
