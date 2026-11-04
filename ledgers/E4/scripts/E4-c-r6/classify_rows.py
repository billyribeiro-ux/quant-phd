"""E4-c round 6: classify each round-5 row as carried (cited lines unchanged) or flagged (cited lines changed).

Usage: python -I classify_rows.py <checkout-root> <round5-fragment.json>. Reads out/linemap.json (linemap.py).
Prints one line per row: id, status, CARRY or FLAG, and the cited file:line tokens that changed (if any).
"""
import json
import re
import sys

root, frag = sys.argv[1], sys.argv[2]
lm = json.load(open(root + "/ledgers/E4/scripts/E4-c-r6/out/linemap.json"))
TOKEN = re.compile(r"(L0[6-9]\.html|lab-E4-L0[6-9]-1\.py|cards\.json|index\.html):(\d+)(?:-(\d+))?")
LIST = re.compile(r"\s*,\s*(\d+)(?:-(\d+))?")


def cited(text):
    out = []
    for m in TOKEN.finditer(text):
        f = m.group(1)
        a = int(m.group(2))
        b = int(m.group(3) or a)
        out.append((f, a, b, m.start(), m.end()))
        pos = m.end()
        while True:
            n = LIST.match(text, pos)
            if not n:
                break
            a2 = int(n.group(1))
            b2 = int(n.group(2) or a2)
            out.append((f, a2, b2, n.start(), n.end()))
            pos = n.end()
    return out


def fname(f):
    return {"lab-E4-L07-1.py": "tests/labs/E4/lab-E4-L07-1.py", "lab-E4-L08-1.py": "tests/labs/E4/lab-E4-L08-1.py",
            "lab-E4-L09-1.py": "tests/labs/E4/lab-E4-L09-1.py"}.get(f, "course/modules/E/E4/" + f)


d = json.load(open(frag))
for r in d["rows"]:
    text = r["location"] + " || " + r["evidence"]
    flagged = []
    for f, a, b, _, _ in cited(text):
        key = fname(f)
        ch = set(lm[key]["changed_old"])
        if any(n in ch for n in range(a, b + 1)):
            flagged.append(f"{f}:{a}-{b}")
    print(r["id"], r["status"], "FLAG " + ",".join(flagged) if flagged else "CARRY")
