import json, subprocess
root = "/Users/billyribeiro/.fanout/wt/verifyS7-FC2-b"
def load(rev):
    s = subprocess.run(["git", "-C", root, "show", f"{rev}:course/modules/FC/FC2/cards.json"], capture_output=True, text=True).stdout
    return {c["id"]: c for c in json.loads(s)}
a, b = load("e896b7a4"), load("aa659725")
print("pin e896b7a4 cards", len(a), "pin aa659725 cards", len(b))
print("removed:", sorted(set(a) - set(b)))
print("added:", sorted(set(b) - set(a)))
print("changed:", sorted(k for k in set(a) & set(b) if a[k] != b[k]))
for k in sorted(set(a) & set(b)):
    if a[k] != b[k] and b[k]["lesson"] in ("L04", "L05", "L06"):
        print("SLICE CHANGED", k)
print("slice lesson counts now:", {l: sum(1 for c in b.values() if c["lesson"] == l) for l in ("L04", "L05", "L06")})
print("c187:", b["FC2-c187"])
