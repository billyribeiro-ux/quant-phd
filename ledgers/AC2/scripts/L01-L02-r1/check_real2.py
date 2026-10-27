import json,sys
from datetime import date
from collections import defaultdict
d=json.load(open(sys.argv[1]))
g=d["facts"]["us-gaap"]
def dur(r): return (date.fromisoformat(r["end"])-date.fromisoformat(r["start"])).days
def annual(r):
    if not r["form"].startswith("10-K") or r.get("fp")!="FY": return False
    if "start" in r: return 350<=dur(r)<=380
    return True
# 1) 10-K/A restatements: same tag+end, 10-K/A value differs from the best earlier 10-K value
tot_ka=0; diff_ka=[]; ties_bad=[]
for t,block in g.items():
    for unit,rows in block["units"].items():
        groups=defaultdict(list)
        for r in rows:
            if annual(r): groups[r["end"]].append(r)
        for e,rs in groups.items():
            ka=[r for r in rs if r["form"]=="10-K/A"]
            for r in ka:
                tot_ka+=1
                prior=[p for p in rs if p["form"]=="10-K" and p["filed"]<r["filed"]]
                if prior:
                    last=max(prior,key=lambda p:(p["filed"],p.get("accn","")))
                    if last["val"]!=r["val"]: diff_ka.append((t,e,last["filed"],last["val"],r["filed"],r["val"],r["accn"]))
            # ties on (filed, accn)
            keys=defaultdict(set)
            for r in rs: keys[(r["filed"],r.get("accn",""))].add(r["val"])
            for k,v in keys.items():
                if len(v)>1: ties_bad.append((t,e,k,v))
print("10-K/A annual observations:",tot_ka,"that differ from prior 10-K for same tag/end:",len(diff_ka))
for x in diff_ka[:12]: print("  ",x)
print("ties on (filed,accn) with different val:",len(ties_bad), ties_bad[:3])
