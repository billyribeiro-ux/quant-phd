"""Byte-compare each L05-L07 card block (raw text between its '  {' and '  }' lines) across the two pins."""
import json
import re
import subprocess

OLD = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
NEW = "e896b7a4"
P = "course/modules/M/M5/cards.json"


def blocks(rev):
    text = subprocess.run(["git", "show", f"{rev}:{P}"], capture_output=True, text=True, check=True).stdout
    lines = text.split("\n")
    out, cur, start = {}, None, None
    for i, line in enumerate(lines):
        if line == "  {":
            start, cur = i, []
        if cur is not None:
            cur.append(line)
        if line in ("  }", "  },") and cur is not None:
            block = "\n".join(cur)
            cid = re.search(r'"id": "(M5-c\d+)"', block).group(1)
            lesson = re.search(r'"lesson": "(L\d+)"', block).group(1)
            out[cid] = (lesson, block, start + 1)
            cur = None
    return out


o, n = blocks(OLD), blocks(NEW)
slice_ids = sorted(k for k, (l, _, _) in n.items() if l in ("L05", "L06", "L07"))
print("slice card blocks (new):", len(slice_ids), "| old blocks with L05-L07:", sum(1 for k, (l, _, _) in o.items() if l in ("L05", "L06", "L07")))
same = [k for k in slice_ids if k in o and o[k][1] == n[k][1]]
print("byte-identical slice card blocks:", len(same), "of", len(slice_ids))
print("not identical:", [k for k in slice_ids if k not in same])
for k, (l, _, ln) in sorted(o.items()):
    if l in ("L05", "L06", "L07") and (k not in n or n[k][1] != _):
        print("CHANGED OLD slice card", k)
