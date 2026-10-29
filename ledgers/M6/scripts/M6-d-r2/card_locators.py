"""For each M6 card, check that every parenthesised locator it cites (e.g. 'Proposition 3.1', 'Lemma 10.6',
'Lab 1, Part B', 'Problem P3') names a numbered item present in the card's own lesson HTML or in the cited lesson."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M6/cards.json").read_text(encoding="utf-8"))
texts = {}
for n in range(1, 13):
    lid = f"L{n:02d}"
    raw = (root / f"course/modules/M/M6/{lid}.html").read_text(encoding="utf-8")
    texts[lid] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
pat = re.compile(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Example|Remark|Assumption|Problem|Result|Section|Part|Lab|Lesson|Step)\s+([0-9A-Za-z.]+)")
bad = []
for c in cards:
    text_all = c["front"] + " " + c["back"]
    for kind, num in ((k, n.rstrip(".")) for k, n in pat.findall(text_all)):
        if kind in ("Lab", "Part", "Section", "Step", "Lesson"):
            continue
        hits = [lid for lid, t in texts.items() if re.search(rf"{kind}\s+{re.escape(num)}\b", t)]
        if not hits:
            bad.append((c["id"], c["lesson"], f"{kind} {num}"))
        elif c["lesson"] not in hits and not any(c["lesson"] == h for h in hits):
            bad.append((c["id"], c["lesson"], f"{kind} {num} only in {hits}"))
for b in bad:
    print("UNRESOLVED", *b)
print("checked", len(cards), "cards; unresolved:", len(bad))
