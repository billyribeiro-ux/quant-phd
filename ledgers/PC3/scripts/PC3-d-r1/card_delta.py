import json, subprocess, sys
BASE = "5db69a9b"
HEAD = "HEAD"
P = "course/modules/PC/PC3/cards.json"
def load(rev):
    raw = subprocess.check_output(["git", "show", f"{rev}:{P}"])
    return json.loads(raw)
old = load(BASE)
new = load(HEAD)
print("old count", len(old), "new count", len(new))
oi = {c["id"]: c for c in old}
ni = {c["id"]: c for c in new}
print("ids only old", sorted(set(oi) - set(ni)))
print("ids only new", sorted(set(ni) - set(oi)))
changed = []
for cid in [c["id"] for c in new]:
    if cid in oi and oi[cid] != ni[cid]:
        changed.append(cid)
print("changed cards", len(changed))
print(" ".join(changed))
# which fields changed
from collections import Counter
fc = Counter()
for cid in changed:
    keys = set(oi[cid]) | set(ni[cid])
    for k in sorted(keys):
        if oi[cid].get(k) != ni[cid].get(k):
            fc[k] += 1
print(dict(fc))
# order check
print("new ids order", [c["id"] for c in new] == sorted(c["id"] for c in new))
