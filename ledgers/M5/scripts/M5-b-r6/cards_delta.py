"""Card-level delta of course/modules/M/M5/cards.json between the round-5 and round-6 pins, and slice membership."""
import json
import subprocess

OLD = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
NEW = "e896b7a4"
P = "course/modules/M/M5/cards.json"


def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:{P}"], capture_output=True, text=True, check=True).stdout
    data = json.loads(raw)
    cards = data["cards"] if isinstance(data, dict) and "cards" in data else data
    return cards


old = {c["id"]: c for c in load(OLD)}
new = {c["id"]: c for c in load(NEW)}
print("counts old", len(old), "new", len(new))
print("type", type(load(NEW)))
removed = sorted(set(old) - set(new))
added = sorted(set(new) - set(old))
changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
print("removed", removed)
print("added", [(k, new[k]["lesson"], new[k]["grade"]) for k in added])
print("changed")
for k in changed:
    o, n = old[k], new[k]
    diffs = [f for f in set(o) | set(n) if o.get(f) != n.get(f)]
    print(" ", k, "lesson", o.get("lesson"), "->", n.get("lesson"), "fields", sorted(diffs))
    for f in sorted(diffs):
        print("     ", f, "OLD:", str(o.get(f))[:300])
        print("     ", f, "NEW:", str(n.get(f))[:300])
slice_ids = [k for k, c in new.items() if c.get("lesson") in ("L05", "L06", "L07")]
print("slice cards new count", len(slice_ids), "by lesson", {l: sum(1 for c in new.values() if c.get("lesson") == l) for l in ("L05", "L06", "L07")})
