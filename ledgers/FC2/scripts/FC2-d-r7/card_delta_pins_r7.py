"""Per-card JSON comparison of course/modules/FC/FC2/cards.json between two git revisions (read-only git show).

Usage: python3 -I card_delta_pins_r7.py <repo_root> <rev_old> <rev_new>
"""
import json
import subprocess
import sys

root, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
path = "course/modules/FC/FC2/cards.json"


def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=root, capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}


a, b = load(old), load(new)
same = [k for k in b if k in a and a[k] == b[k]]
changed = [k for k in b if k in a and a[k] != b[k]]
added = [k for k in b if k not in a]
removed = [k for k in a if k not in b]
print("old", len(a), "new", len(b), "identical", len(same), "changed", len(changed), "added", added, "removed", removed)
print("changed:", " ".join(changed))
