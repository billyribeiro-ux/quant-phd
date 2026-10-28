"""Round 17 card checks for CF1 slice c: delta against the round-16 pin, duplicate scan, and L05/L06 card listing."""
import json
import subprocess
import sys

CUR = "course/modules/CF/CF1/cards.json"
PREV_PIN = "c5daab261a60575e3ab884fdded45945b2b84cce"
old = {c["id"]: c for c in json.loads(subprocess.run(["git", "show", f"{PREV_PIN}:{CUR}"], capture_output=True, text=True, check=True).stdout)}
cards = json.load(open(CUR, encoding="utf-8"))
new = {c["id"]: c for c in cards}
print("count", len(cards), "unique_ids", len(new))
print("added", sorted(set(new) - set(old)))
print("removed", sorted(set(old) - set(new)))
print("changed", [(i, new[i]["lesson"]) for i in sorted(old) if i in new and old[i] != new[i]])
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print("duplicate_fronts", len(fronts) - len(set(fronts)), "duplicate_backs", len(backs) - len(set(backs)))
print("bad_grades", [c["id"] for c in cards if c.get("grade") not in ("T", "C", "D", "A", "B", "X")])
for lesson in ("L05", "L06"):
    print(lesson, [c["id"] for c in cards if c["lesson"] == lesson])
for cid in ("CF1-c096", "CF1-c109", "CF1-c062", "CF1-c068", "CF1-c099"):
    c = new[cid]
    print(cid, c["grade"], "|", c["back"], "|", c.get("basis"))
