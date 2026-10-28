import json, subprocess, sys
root = sys.argv[1]
new = json.load(open(root + "/course/modules/AC/AC4/cards.json", encoding="utf-8"))
old = json.loads(subprocess.check_output(["git", "-C", root, "show", "fefbf8b:course/modules/AC/AC4/cards.json"]))
o = {x["id"]: json.dumps(x, sort_keys=True) for x in old}
n = {x["id"]: json.dumps(x, sort_keys=True) for x in new}
print("changed", [k for k in n if k in o and o[k] != n[k]])
print("new", [k for k in n if k not in o])
print("removed", [k for k in o if k not in n])
L = [x for x in new if x["lesson"] in ("L03", "L04")]
print("L03/L04 cards", len(L), "unchanged", sum(1 for x in L if o.get(x["id"]) == n[x["id"]]))
print("fronts unique", len({x["front"] for x in new}) == len(new), "ids unique", len(n) == len(new))
