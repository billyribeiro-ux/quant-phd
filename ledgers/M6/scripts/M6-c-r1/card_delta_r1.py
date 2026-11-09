import json, sys
base = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
head = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
added = sorted(set(head) - set(base)); removed = sorted(set(base) - set(head))
changed = sorted(k for k in set(base) & set(head) if base[k] != head[k])
print("added", added)
print("removed", removed)
print("changed", changed)
lesson = lambda i: (head.get(i) or base.get(i))["lesson"]
sl = lambda ids: [i for i in ids if lesson(i) in ("L09", "L10", "L11", "L12")]
print("slice-c changed:", sl(changed), "added:", sl(added), "removed:", sl(removed))
