"""Card checks for L07/L08: unique ids, every number in a card appears in its lesson text, every cited Definition/Theorem/Remark/Lemma/Proposition/Corollary/Problem/Section appears in the lesson."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.load(open(root / "course/modules/M/M7/cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("total cards", len(cards), "duplicate ids", [k for k, v in ids.items() if v > 1])
# duplicate fronts across the unit
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
text = {}
for lid in ("L07", "L08"):
    raw = (root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r'<pre class="expected".*?</pre>', lambda m: m.group(0), raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text[lid] = re.sub(r"\s+", " ", t)
slice_cards = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("slice cards", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
for c in slice_cards:
    body = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", body))
    lt = text[c["lesson"]]
    missing = [n for n in nums if n not in lt and n not in text["L07" if c["lesson"] == "L08" else "L08"]]
    refs = set(re.findall(r"(Definition|Theorem|Remark|Lemma|Proposition|Corollary|Problem|Part|Section|Misconception)\s+([A-Z]?\d+(?:\.\d+)?)", body))
    refs_missing = []
    for kind, num in refs:
        if kind in ("Problem",):
            pat = None
        pats = {
            "Definition": rf"Definition {re.escape(num)}\b",
            "Theorem": rf"Theorem {re.escape(num)}\b",
            "Remark": rf"Remark {re.escape(num)}\b",
            "Lemma": rf"Lemma {re.escape(num)}\b",
            "Proposition": rf"Proposition {re.escape(num)}\b",
            "Corollary": rf"Corollary {re.escape(num)}\b",
            "Problem": rf"Problem {re.escape(num)}\b",
            "Part": rf"Part {re.escape(num)}\b",
            "Section": rf"Section {re.escape(num)}\b",
            "Misconception": rf"Misconception {re.escape(num)}\b",
        }
        p = pats.get(kind)
        if p and not re.search(p, lt):
            refs_missing.append((kind, num))
    print(c["id"], c["lesson"], c["grade"], "numbers-missing:", sorted(missing), "refs-missing:", sorted(refs_missing))
