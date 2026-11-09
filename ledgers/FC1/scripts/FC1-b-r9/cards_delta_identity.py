import json, subprocess, sys
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
PATH = "course/modules/FC/FC1/cards.json"
def at(rev):
    raw = subprocess.run(["git", "-C", W, "show", f"{rev}:{PATH}"], capture_output=True, text=True, check=True).stdout
    return raw, json.loads(raw)
raw_old, old = at("4540351d")
raw_new, new = at("95f3f8cb")
old_ids = [c["id"] for c in old]
new_ids = [c["id"] for c in new]
print("old count", len(old), "new count", len(new))
print("removed ids", sorted(set(old_ids) - set(new_ids)))
print("added ids", sorted(set(new_ids) - set(old_ids)))
om = {c["id"]: c for c in old}
nm = {c["id"]: c for c in new}
changed = [i for i in new_ids if i in om and om[i] != nm[i]]
print("entries changed (object compare):", changed)
print("order of surviving ids preserved:", [i for i in old_ids if i in nm] == new_ids)
print("ids unique:", len(new_ids) == len(set(new_ids)))
print("fronts unique:", len({c['front'] for c in new}) == len(new))
print("new file ends with newline:", raw_new.endswith("\n"), "bytes", len(raw_new))
print("old file ends with newline:", raw_old.endswith("\n"), "bytes", len(raw_old))
print("lines new:", raw_new.count("\n"), "old:", raw_old.count("\n"))
import re
bad = [c["id"] for c in new if not re.fullmatch(r"FC1-c\d{3}", c["id"])]
print("bad id pattern:", bad)
print("grade values:", sorted({str(c.get("grade")) for c in new}))
print("C without basis:", [c["id"] for c in new if c.get("grade") == "C" and not c.get("basis")])
print("basis on non-C:", [c["id"] for c in new if c.get("grade") != "C" and "basis" in c])
print("c173/c174/c125 present:", [i for i in ("FC1-c173","FC1-c174","FC1-c125") if i in nm])
print("L04 count old/new:", sum(1 for c in old if c['lesson']=='L04'), sum(1 for c in new if c['lesson']=='L04'))
print("sorted by numeric id:", [c['id'] for c in new] == sorted([c['id'] for c in new]))
