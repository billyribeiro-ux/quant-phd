import json, subprocess, sys
root = sys.argv[1]
def load(rev):
    raw = subprocess.check_output(["git", "-C", root, "show", f"{rev}:course/modules/E/E1/cards.json"])
    return json.loads(raw)
old = load("dde0486b")
new = load("HEAD")
o = {c["id"]: c for c in old}
n = {c["id"]: c for c in new}
print("old count", len(old), "unique", len(o), "new count", len(new), "unique", len(n))
print("removed:", sorted(set(o) - set(n)))
print("added:", sorted(set(n) - set(o)))
changed = sorted(i for i in set(o) & set(n) if o[i] != n[i])
print("changed:", changed)
for i in changed:
    print(i, "lesson", o[i]["lesson"], "->", n[i]["lesson"], "keys", sorted(set(o[i]) ^ set(n[i])))
unchanged_l = sorted(i for i in set(o) & set(n) if o[i] == n[i])
print("unchanged count", len(unchanged_l))
