import json, sys
old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
changed = sorted(k for k in old if k in new and old[k] != new[k])
removed = sorted(k for k in old if k not in new)
added = sorted(k for k in new if k not in old)
print("changed:", changed)
print("removed:", removed)
print("added:", added)
slice_lessons = {"L07", "L08"}
print("changed in L07/L08:", [k for k in changed if new[k]["lesson"] in slice_lessons])
print("added in L07/L08:", [k for k in added if new[k]["lesson"] in slice_lessons])
print("changed lessons:", sorted({new[k]["lesson"] for k in changed}))
print("slice-c cards (L07/L08) unchanged count:", sum(1 for k in new if new[k]["lesson"] in slice_lessons and old.get(k) == new[k]), "of", sum(1 for k in new if new[k]["lesson"] in slice_lessons))
for k in ["M7-c121","M7-c122","M7-c123","M7-c124","M7-c125","M7-c126","M7-c127","M7-c128","M7-c136","M7-c142","M7-c226","M7-c227","M7-c144","M7-c145","M7-c148","M7-c149","M7-c041"]:
    print(k, "identical" if old.get(k)==new.get(k) else "DIFFERENT", new.get(k,{}).get("lesson"))
