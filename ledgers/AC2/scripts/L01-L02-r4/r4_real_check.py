"""Round-4 check of L01 claims about the real SEC companyfacts file (CIK0000320193), read-only."""
import json, collections
from datetime import date
d = json.load(open("/tmp/ac2-v/l12/r4/edgar4/companyfacts.json", encoding="utf-8"))
print("top keys", sorted(d))
gaap = d["facts"]["us-gaap"]
keyset = collections.Counter()
for tag, block in gaap.items():
    for unit, rows in block["units"].items():
        for row in rows:
            keyset[tuple(sorted(row))] += 1
print("observation key sets:", keyset.most_common(4))
flow_has_start = collections.Counter()
for tag in ("NetIncomeLoss", "Assets"):
    for unit, rows in gaap[tag]["units"].items():
        for row in rows:
            flow_has_start[(tag, "start" in row)] += 1
print("NetIncomeLoss rows with start:", flow_has_start[("NetIncomeLoss", True)], "without:", flow_has_start[("NetIncomeLoss", False)])
print("Assets rows with start:", flow_has_start[("Assets", True)], "without:", flow_has_start[("Assets", False)])
for tag in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"):
    if tag in gaap:
        rows = gaap[tag]["units"].get("USD", [])
        fys = sorted({r["fy"] for r in rows if r.get("form", "").startswith("10-K")})
        print(tag, "rows", len(rows), "10-K fy range", fys[:1], fys[-1:] if fys else None)
# 10-K/A rows and repeated comparatives for NetIncomeLoss
rows = gaap["NetIncomeLoss"]["units"]["USD"]
forms = collections.Counter(r["form"] for r in rows)
print("NetIncomeLoss forms", forms.most_common(6))
rep = collections.Counter((r["end"], r.get("start")) for r in rows if r["form"] == "10-K" and r.get("fp") == "FY")
print("annual (end,start) repeated across filings:", sum(1 for k, v in rep.items() if v > 1), "of", len(rep))
amend = [r for r in rows if r["form"] == "10-K/A"]
print("NetIncomeLoss 10-K/A rows:", len(amend), amend[:1])
