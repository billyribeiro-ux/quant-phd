"""Verifier scan (M3 slice a, round 2): visible text of the hub and L01-L03 against curriculum concepts owned outside the
prerequisite closure of M3 (closure computed from curriculum/curriculum.json prereqs). Prints every name hit with its context.
Usage: python -I -W error ledgers/M3/scripts/M3-a-r2/concept_scan_r2.py   (from the checkout root)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cur = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))
mods = {m["id"]: m for part in cur["parts"] for m in part["modules"]}
closure, stack = set(), ["M3"]
while stack:
    x = stack.pop()
    if x not in closure:
        closure.add(x)
        stack += mods[x].get("prereqs", [])
own = {k for mid in closure for k in mods[mid].get("introduces", {})}
print("closure", sorted(closure), "introduced in closure", len(own))
text = ""
for f in ["index.html", "L01.html", "L02.html", "L03.html"]:
    s = (ROOT / "course/modules/M/M3" / f).read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    text += "\n" + html.unescape(re.sub(r"<[^>]+>", " ", s))
flat = re.sub(r"\s+", " ", text)
hits = 0
for k, v in cur["concepts"].items():
    if v["module"] in closure or k in own:
        continue
    base = re.sub(r"\s*\(.*?\)", "", v["name"].lower()).strip()
    if len(base) < 5:
        continue
    for needle in {base, k.replace("-", " ")}:
        for m in re.finditer(r"(?<![A-Za-z])" + re.escape(needle) + r"(?![A-Za-z])", flat, re.I):
            hits += 1
            print(f"HIT {k} [{v['module']}] {v['name']!r}: ...{flat[max(0, m.start() - 60):m.end() + 40]}...")
print("out-of-closure concept-name hits:", hits)
