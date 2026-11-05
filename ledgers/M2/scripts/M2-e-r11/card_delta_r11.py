import json, subprocess, sys, collections
old = json.loads(subprocess.run(["git", "show", "47a36d8c:course/modules/M/M2/cards.json"], capture_output=True, text=True, check=True).stdout)
new = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
print("old count", len(old), "new count", len(new))
ob = {c["id"]: c for c in old}; nb = {c["id"]: c for c in new}
print("removed:", sorted(set(ob) - set(nb)))
print("added:", sorted(set(nb) - set(ob)))
changed = sorted(i for i in set(ob) & set(nb) if ob[i] != nb[i])
print("changed:", changed)
for i in changed:
    for k in sorted(set(ob[i]) | set(nb[i])):
        if ob[i].get(k) != nb[i].get(k):
            print(f"  {i} {k}\n    OLD: {ob[i].get(k)}\n    NEW: {nb[i].get(k)}")
print("removed cards:")
for i in sorted(set(ob) - set(nb)):
    print(json.dumps(ob[i], ensure_ascii=False))
print("grades new:", collections.Counter(c["grade"] for c in new))
print("per lesson new:", sorted(collections.Counter(c["lesson"] for c in new).items()))
