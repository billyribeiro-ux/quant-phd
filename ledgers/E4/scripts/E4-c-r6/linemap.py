"""E4-c round 6: map line numbers between the previous pin (7376a5e2) and the pin (4bd8cb94) with difflib.

Usage: python -I linemap.py <checkout-root> <old-dir>   (old-dir holds the 7376a5e2 copies, names with '_' for '/').
Prints, per file, the changed old line numbers and the shift of every old line that is unchanged. Stdlib only.
"""
import difflib
import json
import os
import sys

root, old_dir = sys.argv[1], sys.argv[2]
FILES = [
    "course/modules/E/E4/L06.html", "course/modules/E/E4/L07.html", "course/modules/E/E4/L08.html",
    "course/modules/E/E4/L09.html", "course/modules/E/E4/cards.json", "course/modules/E/E4/index.html",
    "tests/labs/E4/lab-E4-L07-1.py", "tests/labs/E4/lab-E4-L08-1.py", "tests/labs/E4/lab-E4-L09-1.py",
]
result = {}
for f in FILES:
    old = open(os.path.join(old_dir, f.replace("/", "_")), encoding="utf-8").read().splitlines()
    new = open(os.path.join(root, f), encoding="utf-8").read().splitlines()
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    mapping = {}
    changed = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k + 1] = j1 + k + 1
        else:
            changed.extend(range(i1 + 1, i2 + 1))
    result[f] = {"map": mapping, "changed_old": changed}
    print(f, "old lines", len(old), "new lines", len(new), "changed old lines:", changed)
    shifts = sorted({mapping[k] - k for k in mapping if mapping[k] != k})
    print("   shifts for unchanged lines:", shifts)
json.dump({k: {"map": {str(a): b for a, b in v["map"].items()}, "changed_old": v["changed_old"]} for k, v in result.items()},
          open(os.path.join(root, "ledgers/E4/scripts/E4-c-r6/out/linemap.json"), "w"), indent=0)
