"""Closing-delta card checks (M3 slice a, round 1). Reads repository files only; run with python -I -W error.

1. Full-file duplicate scan of course/modules/M/M3/cards.json (all 210 cards): identical fronts, difflib ratio >= 0.7
   on fronts, token Jaccard >= 0.5 on fronts, and ids.
2. For each card of L01-L03 whose bytes changed since the base pin (read from git), each number token in its back
   must appear in the text of its lesson page (tags stripped), and each cited Definition/Proposition/Theorem/
   Corollary/Example/Remark number must exist in the lesson it cites.
"""
import difflib
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M3-a")
PATH = "course/modules/M/M3/cards.json"
new = json.loads((ROOT / PATH).read_text(encoding="utf-8"))
old = json.loads(subprocess.run(["git", "-C", str(ROOT), "show", f"9294b914:{PATH}"], capture_output=True, text=True, check=True).stdout)
ids = [c["id"] for c in new]
print("cards total", len(new), "duplicate ids", sorted({x for x in ids if ids.count(x) > 1}))

def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()

exact = {}
for c in new:
    exact.setdefault(norm(c["front"]), []).append(c["id"])
print("exact duplicate fronts:", [v for v in exact.values() if len(v) > 1])
print("difflib fronts ratio >= 0.7:")
for i, a in enumerate(new):
    for b in new[i + 1:]:
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.7:
            print("  ", a["id"], b["id"], round(r, 2), "|", a["front"][:90], "||", b["front"][:90])
print("token Jaccard >= 0.5 on fronts:")
tok = {c["id"]: set(norm(c["front"]).split()) - {"in", "the", "of", "a", "is", "are", "and", "to", "what", "how", "many", "lab", "1", "does", "do", "for", "if", "or", "by", "with", "on", "that", "this", "whether", "from", "at", "as"} for c in new}
for i, a in enumerate(new):
    for b in new[i + 1:]:
        A, B = tok[a["id"]], tok[b["id"]]
        if A and B and len(A & B) / len(A | B) >= 0.5:
            print("  ", a["id"], a["lesson"], "/", b["id"], b["lesson"], round(len(A & B) / len(A | B), 2), "|", a["front"][:80], "||", b["front"][:80])

lessons = {}
for n in ("L01", "L02", "L03"):
    t = (ROOT / f"course/modules/M/M3/{n}.html").read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    lessons[n] = html.unescape(re.sub(r"<[^>]+>", " ", t))

oldby = {c["id"]: c for c in old}
print("changed L01-L03 cards (bytes differ from base):")
for c in new:
    if c["lesson"] in ("L01", "L02", "L03") and oldby.get(c["id"]) != c:
        print(" ", c["id"], c["lesson"], c["grade"], c["basis"])
        print("    back:", c["back"])
        nums = set(re.findall(r"(?<![A-Za-z])-?\d+(?:\.\d+)?(?:e-?\d+)?", c["back"]))
        for n in sorted(nums):
            key = n.lstrip("-")
            present = re.search(r"(?<![\d.])" + re.escape(key) + r"(?![\d])", lessons[c["lesson"]]) is not None
            print(f"    number {n!r} in {c['lesson']} text: {present}")
        for kind, num in re.findall(r"(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Assumption) (\d+\.\d+)", c["back"] + " " + c["front"]):
            print(f"    cites {kind} {num}: in {c['lesson']} text: {bool(re.search(kind + ' ' + re.escape(num), lessons[c['lesson']]))}")
