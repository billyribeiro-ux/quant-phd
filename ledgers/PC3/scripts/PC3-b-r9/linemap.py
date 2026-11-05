"""Verifier round 9 (PC3-b): map old (0dee921a) line numbers to current (c93dd526) line numbers for carried rows."""
import difflib
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-b"
OLD = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
for page in ("L04", "L05", "L06"):
    path = f"course/modules/PC/PC3/{page}.html"
    old = subprocess.run(["git", "-C", ROOT, "show", f"{OLD}:{path}"], capture_output=True, text=True, check=True).stdout.splitlines()
    new = open(f"{ROOT}/{path}", encoding="utf-8").read().splitlines()
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    changed = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            changed.append((i1 + 1, i2, j1 + 1, j2))
    print(page, "changed old-line ranges -> new ranges:", changed)
    # print the mapping for 'equal' blocks as offsets
    offs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            offs.append((i1 + 1, i2, j1 - i1))
    print(page, "equal blocks (old start-end, offset):", offs)
