"""Round-5 card checks for M2 slice b (run from the verifier checkout root).

Compares every card object of course/modules/M/M2/cards.json at the previous pin (edbb7aa8) and the current pin (HEAD),
counts cards per lesson, checks id and front uniqueness across the whole deck, and lists the slice cards that changed.
"""
import json
import subprocess
import sys
from collections import Counter

PATH = "course/modules/M/M2/cards.json"


def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:{PATH}"], capture_output=True, text=True, check=True).stdout
    return raw, json.loads(raw)


raw_old, old = load("edbb7aa8")
raw_new, new = load("HEAD")
print("cards old", len(old), "new", len(new))
ids_new = [c["id"] for c in new]
fronts_new = [c["front"].strip().lower() for c in new]
print("dup ids in new:", [k for k, v in Counter(ids_new).items() if v > 1])
print("dup fronts in new:", [k[:60] for k, v in Counter(fronts_new).items() if v > 1])
print("cards per lesson (new):", sorted(Counter(c["lesson"] for c in new).items()))
old_by = {c["id"]: c for c in old}
new_by = {c["id"]: c for c in new}
changed = sorted(i for i in new_by if i in old_by and old_by[i] != new_by[i])
added = sorted(i for i in new_by if i not in old_by)
removed = sorted(i for i in old_by if i not in new_by)
print("changed:", changed)
print("added:", added)
print("removed:", removed)
slice_lessons = {"L07", "L08", "L09", "L10", "L11", "L12"}
for lesson in sorted(slice_lessons):
    cs = [c for c in new if c["lesson"] == lesson]
    ids = [c["id"] for c in cs]
    print(lesson, len(cs), ids[0], ids[-1], "grades:", dict(Counter(c.get("grade") for c in cs)))
