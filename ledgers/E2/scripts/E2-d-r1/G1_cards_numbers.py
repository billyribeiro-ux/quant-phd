# Checks, for every E2 card, that each number in its front/back appears in the card's lesson HTML text.
# Also: duplicate fronts, structure, and the byte-identity of unchanged cards against the base pin.
import json, re, subprocess, sys, html
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
base = json.loads(subprocess.run(["git", "-C", str(root), "show", "95f3f8cb:course/modules/E/E2/cards.json"],
                                 capture_output=True, text=True, check=True).stdout)
bmap = {c["id"]: c for c in base}
def lesson_text(lid):
    raw = (root / f"course/modules/E/E2/{lid}.html").read_text(encoding="utf-8")
    raw = re.sub(r"</?[a-zA-Z][^>]*>", " ", raw)
    return html.unescape(raw)
texts = {}
num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
problems = []
fronts = {}
changed = []
for c in cards:
    lid = c["lesson"]
    if lid not in texts:
        texts[lid] = lesson_text(lid)
        texts[lid + "_nc"] = texts[lid].replace(",", "")
    s = c["front"] + " " + c["back"]
    for n in set(num_re.findall(s)):
        n2 = n.rstrip(",")
        if not n2:
            continue
        if n2 in texts[lid] or n2.replace(",", "") in texts[lid + "_nc"]:
            continue
        problems.append(f"{c['id']} ({lid}): number {n2!r} not found in lesson text")
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    if c["id"] in bmap and bmap[c["id"]] != c:
        changed.append(c["id"])
dups = {k: v for k, v in fronts.items() if len(v) > 1}
print("cards:", len(cards), "changed vs 95f3f8cb:", changed)
print("number problems:", len(problems))
for p in problems: print("  ", p)
print("duplicate fronts:", dups)
