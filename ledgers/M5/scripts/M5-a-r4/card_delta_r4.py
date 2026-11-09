# Compares course/modules/M/M5/cards.json at two pins (object by object) and lists the changed, added and removed ids.
# Usage: python3 card_delta_r4.py <old_pin> <new_pin>   (run from the checkout root; reads git blobs, no network)
import json, subprocess, sys
old_pin, new_pin = sys.argv[1], sys.argv[2]
def load(pin):
    raw = subprocess.run(["git", "show", f"{pin}:course/modules/M/M5/cards.json"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)
old = {c["id"]: c for c in load(old_pin)}
new = {c["id"]: c for c in load(new_pin)}
changed = sorted(k for k in old if k in new and old[k] != new[k])
added = sorted(k for k in new if k not in old)
removed = sorted(k for k in old if k not in new)
print("old count", len(old), "new count", len(new))
print("changed", changed)
print("added", added)
print("removed", removed)
print("ids in L01-L04 changed:", [k for k in changed if new[k]["lesson"] in ("L01", "L02", "L03", "L04")])
print("ids in L01-L04 added/removed:", [k for k in added + removed if (new.get(k) or old.get(k))["lesson"] in ("L01", "L02", "L03", "L04")])
