"""Compare per-card JSON objects of course/modules/FC/FC2/cards.json between two git revisions.

Usage: python3 -I card_delta.py <repo_root> <old_rev> <new_rev>
"""

import json
import subprocess
import sys

root, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
path = "course/modules/FC/FC2/cards.json"


def load(rev: str) -> dict[str, str]:
    raw = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    cards = json.loads(raw)
    return {c["id"]: json.dumps(c, sort_keys=True, ensure_ascii=False) for c in cards}


a, b = load(old), load(new)
print("cards old", len(a), "new", len(b))
print("added", sorted(set(b) - set(a)))
print("removed", sorted(set(a) - set(b)))
print("changed", sorted(k for k in set(a) & set(b) if a[k] != b[k]))
print("identical", len([k for k in set(a) & set(b) if a[k] == b[k]]))
