"""Round-5 delta and card checks for SC1-b (L04-L06, their twins, and the cards tagged L04-L06).
Compares the pin 7376a5e with the round-4 pin 9a02b1af. Run from the checkout root with python3 -I."""

import json
import subprocess

BASE = "9a02b1af"
PIN = "7376a5e"
SLICE_PATHS = [
    "course/modules/SC/SC1/L04.html",
    "course/modules/SC/SC1/L05.html",
    "course/modules/SC/SC1/L06.html",
    "tests/labs/SC1/lab-SC1-L04-1.py",
    "tests/labs/SC1/lab-SC1-L05-1.py",
    "tests/labs/SC1/lab-SC1-L06-1.py",
    "course/modules/SC/SC1/cards.json",
    "course/modules/SC/SC1/L01.html",
    "course/modules/SC/SC1/L02.html",
    "course/modules/SC/SC1/L03.html",
    "course/modules/SC/SC1/L08.html",
    "course/modules/SC/SC1/index.html",
    "notation/notation.json",
    "references/references.json",
    "plans/SC1-build-plan.md",
    "plans/SC1-open-items.md",
]

print(f"delta {BASE}..{PIN} for slice paths:")
for p in SLICE_PATHS:
    stat = subprocess.run(
        ["git", "diff", "--shortstat", BASE, PIN, "--", p], capture_output=True, text=True
    ).stdout.strip()
    print(f"  {p}: {stat if stat else 'byte-identical'}")

old = json.loads(subprocess.run(["git", "show", f"{BASE}:course/modules/SC/SC1/cards.json"], capture_output=True, text=True).stdout)
new = json.load(open("course/modules/SC/SC1/cards.json", encoding="utf-8"))
oi = {c["id"]: c for c in old}
ni = {c["id"]: c for c in new}
changed = sorted(k for k in ni if k in oi and ni[k] != oi[k])
added = sorted(k for k in ni if k not in oi)
removed = sorted(k for k in oi if k not in ni)
slice_ids = {c["id"] for c in new if c["lesson"] in ("L04", "L05", "L06")}
print("cards changed (all lessons):", changed)
print("cards changed in L04-L06:", sorted(k for k in changed if k in slice_ids))
print("cards added:", added)
print("cards added in L04-L06:", sorted(k for k in added if k in slice_ids))
print("cards removed:", removed, "(removed cards were lesson:", [oi[k]["lesson"] for k in removed], ")")
fronts = [c["front"].strip().lower() for c in new]
backs = [c["back"].strip().lower() for c in new]
print("cards total", len(new), "unique fronts", len(set(fronts)), "unique backs", len(set(backs)))

for k in sorted(slice_ids):
    if k in oi and oi[k] != ni[k]:
        print("CHANGED", k)
        print("  old:", json.dumps(oi[k], ensure_ascii=False)[:400])
        print("  new:", json.dumps(ni[k], ensure_ascii=False)[:400])
