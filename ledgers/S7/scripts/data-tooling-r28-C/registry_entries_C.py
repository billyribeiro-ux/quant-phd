"""Round-28 part C: entry-level comparison of references/references.json at 5e5da87 (release) and c9beb92 (pin).
For every key: is the entry identical (ignoring used_by), identical including used_by, or added/removed?
Also the keys named in the S7 rows of this part, and whether each key's used_by changed.
Run: python -I registry_entries_C.py <checkout>"""
import json
import subprocess
import sys

CK = sys.argv[1]


def at(rev):
    raw = subprocess.run(["git", "-C", CK, "show", f"{rev}:references/references.json"], capture_output=True, check=True).stdout
    return json.loads(raw)


old, new = at("5e5da87"), at("c9beb92")


def entries(doc):
    items = doc["entries"] if isinstance(doc, dict) and "entries" in doc else doc
    if isinstance(items, dict):
        return items
    return {e["key"]: e for e in items}


o, n = entries(old), entries(new)
print("header old:", {k: v for k, v in old.items() if k != "entries"} if isinstance(old, dict) else "list")
print("header new:", {k: v for k, v in new.items() if k != "entries"} if isinstance(new, dict) else "list")
keys_cited = ["hou2018replicating", "chordia2020anomalies", "jensen2023there", "chen2025t", "chen2019publication",
              "lu2025replication", "gine1997student", "jiang2025endogeneity", "harvey2015cross", "moskowitz2012time",
              "huang2020time", "ahn2026overlapping", "huang2012much", "bailey2016probability", "storey2002direct", "jiang2025endogeneity"]
changed_used_by = []
other = []
for k, e in n.items():
    if k not in o:
        continue
    a = {x: y for x, y in o[k].items() if x != "used_by"}
    b = {x: y for x, y in e.items() if x != "used_by"}
    if a != b:
        other.append(k)
    if o[k].get("used_by") != e.get("used_by"):
        changed_used_by.append(k)
print("entries at 5e5da87:", len(o), "at c9beb92:", len(n))
print("added since 5e5da87:", sorted(set(n) - set(o)), "removed:", sorted(set(o) - set(n)))
print("entries whose content changed beyond used_by:", other)
print("entries whose used_by changed:", len(changed_used_by), sorted(changed_used_by))
for k in keys_cited:
    if k not in n:
        print(f"{k}: NOT IN REGISTRY")
        continue
    print(f"{k}: in 5e5da87={k in o} | identical except used_by={k not in other} | used_by changed={k in changed_used_by}")
