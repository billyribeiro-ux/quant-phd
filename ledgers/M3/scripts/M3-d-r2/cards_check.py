"""Round-2 card check for M3 (verifier): every card against its lesson page.

For each card in course/modules/M/M3/cards.json:
  * the lesson page it names must exist;
  * every labelled block cited in front or back (Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example x.y)
    must exist as a block-title in that lesson or, failing that, in another M3 lesson (reported);
  * the card's grade (if any) is compared with the data-grade of the cited claim block when it is a claim;
  * every decimal or integer token in the back must occur in the text of the lesson page (reported when absent);
  * exact duplicate fronts and backs are listed.
Usage: cards_check.py <checkout-root>
"""

import collections
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M3"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
pages = {p.stem: p.read_text(encoding="utf-8") for p in sorted(root.glob("L0*.html"))}
text = {k: html.unescape(re.sub(r"<[^>]+>", " ", v)) for k, v in pages.items()}
text = {k: re.sub(r"\s+", " ", v) for k, v in text.items()}
blocks: dict[str, dict[str, str]] = {}
for name, raw in pages.items():
    found: dict[str, str] = {}
    for m in re.finditer(r'<span class="block-title([^"]*)"[^>]*>\s*((?:Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example)\s+\d+\.\d+)', raw):
        grade = re.search(r'data-grade="([TCH])"', raw[max(0, m.start() - 200) : m.start()] + m.group(0))
        found[m.group(2)] = grade.group(1) if grade else "-"
    blocks[name] = found
ref_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example)\s+(\d+\.\d+)")
num_re = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?:e-?\d+)?(?![\w])")
issues = []
rows = []
fronts = collections.Counter(c["front"] for c in cards)
backs = collections.Counter(c["back"] for c in cards)
for c in cards:
    cid, lesson = c["id"], c["lesson"]
    refs = []
    for field in ("front", "back"):
        for m in ref_re.finditer(c[field]):
            refs.append(f"{m.group(1)} {m.group(2)}")
    own = blocks.get(lesson, {})
    missing = []
    elsewhere = []
    for r in refs:
        if r in own:
            continue
        hits = [k for k, v in blocks.items() if r in v]
        if hits:
            elsewhere.append(f"{r}@{hits[0]}")
        else:
            missing.append(r)
    grade_note = ""
    if c.get("grade") == "T":
        bad = [f"{r}={own.get(r) or next((blocks[k][r] for k in blocks if r in blocks[k]), '?')}"
               for r in refs if r.split()[0] in ("Proposition", "Theorem", "Lemma", "Corollary")]
        grade_note = "T-card cites " + ",".join(bad) if bad else ""
    nums = []
    for tok in num_re.findall(c["back"]):
        if tok not in text.get(lesson, ""):
            nums.append(tok)
    rows.append((cid, lesson, c.get("grade", "-"), len(refs), missing, elsewhere, nums, grade_note))
for cid, lesson, g, nrefs, missing, elsewhere, nums, gn in rows:
    flag = "MISSING" if missing else ""
    print(f"{cid} {lesson} grade={g} refs={nrefs} {flag} missing={missing} elsewhere={elsewhere} absent_numbers={nums} {gn}")
print("DUPLICATE fronts:", [f for f, n in fronts.items() if n > 1])
print("DUPLICATE backs:", [b[:60] for b, n in backs.items() if n > 1])
print("cards:", len(cards), "unique ids:", len({c['id'] for c in cards}))
