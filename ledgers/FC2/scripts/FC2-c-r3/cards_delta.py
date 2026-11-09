"""Verifier check (FC2 slice c, round 3): L07/L08 card delta since the round-2 pin 9294b914.

Run from the checkout root: git show 9294b914:course/modules/FC/FC2/cards.json is read via git; then compares with HEAD's file.
"""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
prev_text = subprocess.run(
    ["git", "show", "9294b914:course/modules/FC/FC2/cards.json"], capture_output=True, text=True, cwd=str(ROOT), check=True
).stdout
prev = json.loads(prev_text)
cur = json.loads((ROOT / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
pm = {c["id"]: c for c in prev}
cm = {c["id"]: c for c in cur}
print("prev", len(prev), "cur", len(cur))
print("removed", sorted(set(pm) - set(cm)))
print("added", sorted(set(cm) - set(pm)))
changed = sorted(i for i in pm if i in cm and pm[i] != cm[i])
print("changed", changed)
for i in changed:
    if cm[i].get("lesson") in ("L07", "L08"):
        print("L07/L08 changed:", i, "| prev:", pm[i]["front"], "| cur:", cm[i]["front"])
l78_prev = {c["id"] for c in prev if c.get("lesson") in ("L07", "L08")}
l78_cur = {c["id"] for c in cur if c.get("lesson") in ("L07", "L08")}
print("L07/L08 ids identical set:", l78_prev == l78_cur, len(l78_cur))
c113 = cm["FC2-c113"]
print("FC2-c113 has basis key:", "basis" in c113, "unchanged since prev pin:", pm["FC2-c113"] == c113)
