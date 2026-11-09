import json, sys
prev = json.load(open(sys.argv[1], encoding="utf-8"))
now = json.load(open(sys.argv[2], encoding="utf-8"))
pm = {r["id"]: r for r in prev}
nm = {r["id"]: r for r in now}
print("prev records", len(prev), "now records", len(now))
print("removed", sorted(set(pm) - set(nm)))
print("added", sorted(set(nm) - set(pm)))
changed = sorted(k for k in set(pm) & set(nm) if pm[k] != nm[k])
print("changed", changed)
slice_ids = [k for k in nm if nm[k]["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice L01-L04 records now", len(slice_ids))
print("slice changed", sorted(k for k in changed if nm[k]["lesson"] in ("L01", "L02", "L03", "L04")))
print("slice removed", sorted(k for k in set(pm) - set(nm) if pm[k]["lesson"] in ("L01", "L02", "L03", "L04")))
print("slice added", sorted(k for k in set(nm) - set(pm) if nm[k]["lesson"] in ("L01", "L02", "L03", "L04")))
