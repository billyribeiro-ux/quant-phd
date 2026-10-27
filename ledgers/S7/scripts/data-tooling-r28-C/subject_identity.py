"""Round-28 part C: for every row, list the repository paths it names and whether each is byte-identical
(git diff --quiet) between the carry bases 47bac8d and 5e5da87 and the pin c9beb92.
Usage: python -I subject_identity.py <checkout>  (prints one line per row)."""
import json
import re
import subprocess
import sys

CK = sys.argv[1]
PAT = re.compile(r"(?:course|tools|tests|references|curriculum|\.github|atlas|notation|pyproject\.toml|requirements[-a-z]*\.txt|CLAUDE\.md|BLUEPRINT\.md)[A-Za-z0-9_./\-]*")


def same(base, path):
    r = subprocess.run(["git", "-C", CK, "diff", "--quiet", base, "c9beb92", "--", path])
    return r.returncode == 0


def exists(path):
    import os
    return os.path.exists(os.path.join(CK, path))


rows = json.load(open(f"{CK}/ledgers/S7/data-tooling-C.json"))["rows"]
out = []
for i, r in enumerate(rows):
    text = r["location"] + " " + r["evidence"]
    paths = []
    for m in PAT.findall(text):
        p = m.rstrip(".,;:)'\"")
        if p.endswith("/") or p in paths:
            continue
        paths.append(p)
    res = []
    for p in paths:
        if "*" in p or "{" in p:
            continue
        ex = exists(p)
        if not ex and "/" not in p:
            continue
        res.append(f"{p}[{'=47' if same('47bac8d', p) else '!47'}{'=5e' if same('5e5da87', p) else '!5e'}{'' if ex else ' MISSING'}]")
    out.append(f"[{i}] {r['id']} {r['status']}: " + " ".join(res))
print("\n".join(out))
