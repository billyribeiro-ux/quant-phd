"""Round-13 card delta for E4 slice b: cards whose lesson is L04, L05 or L06, old pin vs new pin.

Usage: python card_delta_r13.py <old_rev> <new_rev>. Reads course/modules/E/E4/cards.json from git.
"""
import json
import subprocess
import sys

old_rev, new_rev = sys.argv[1], sys.argv[2]
path = "course/modules/E/E4/cards.json"


def load(rev: str) -> list[dict]:
    raw = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


old = {c["id"]: c for c in load(old_rev)}
new = {c["id"]: c for c in load(new_rev)}
slice_lessons = {"L04", "L05", "L06"}
ids = sorted(set(old) | set(new))
print(f"old cards {len(old)} new cards {len(new)}")
for cid in ids:
    o, n = old.get(cid), new.get(cid)
    lesson = (n or o).get("lesson")
    if lesson not in slice_lessons:
        continue
    if o == n:
        continue
    if o is None:
        print(f"ADDED {cid} {lesson}")
    elif n is None:
        print(f"REMOVED {cid} {lesson}")
    else:
        keys = sorted(k for k in set(o) | set(n) if o.get(k) != n.get(k))
        print(f"CHANGED {cid} {lesson} keys={keys}")
        for k in keys:
            print(f"  old {k}: {o.get(k)}")
            print(f"  new {k}: {n.get(k)}")
slice_ids = [c for c in new if new[c]["lesson"] in slice_lessons]
print(f"new slice cards {len(slice_ids)}: {sorted(slice_ids)[0]} .. {sorted(slice_ids)[-1]}")
