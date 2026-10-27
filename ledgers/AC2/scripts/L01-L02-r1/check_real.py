import json,sys
from datetime import date
d=json.load(open(sys.argv[1]))
g=d["facts"]["us-gaap"]
def dur(r): return (date.fromisoformat(r["end"])-date.fromisoformat(r["start"])).days
def annual(r,flow):
    if not r["form"].startswith("10-K") or r.get("fp")!="FY": return False
    if flow: return "start" in r and 350<=dur(r)<=380
    return "start" not in r
# fp values and forms overall for 10-K rows
from collections import Counter
for t in ["Revenues","SalesRevenueNet","RevenueFromContractWithCustomerExcludingAssessedTax","NetIncomeLoss","Assets"]:
    rows=g[t]["units"]["USD"]
    print(t, "fp:",Counter((r["form"],r.get("fp")) for r in rows if r["form"].startswith("10-K")).most_common(8))
    ann=[r for r in rows if annual(r, "start" in r)]
    by=Counter(r["end"] for r in ann)
    multi={e:c for e,c in by.items() if c>1}
    print("  annual rows:",len(ann),"ends:",len(by),"ends with >1 annual obs:",len(multi), "sample:", sorted(multi)[-3:] if multi else None)
    # durations of 10-K FY flows
    if "start" in rows[0]:
        print("  10-K FY durations:", sorted(Counter(dur(r) for r in rows if r["form"]=="10-K" and r.get("fp")=="FY").items())[:12])
# show revenue annual observations ending in 2019-2023 with forms
for t in ["Revenues","SalesRevenueNet","RevenueFromContractWithCustomerExcludingAssessedTax"]:
    rows=[r for r in g[t]["units"]["USD"] if annual(r,True)]
    print("==",t)
    for r in sorted(rows,key=lambda r:(r["end"],r["filed"])):
        if r["end"]>="2016-01-01": print("  ",r["end"],r["filed"],r["form"],r["fp"],r["accn"],r["val"],dur(r))
