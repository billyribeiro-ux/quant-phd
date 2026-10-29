# For every card: each 'Definition/Proposition/Corollary/Remark/Theorem/Problem/Section/Lab' label cited in front or back
# must appear in the card's own lesson; banned phrases and process words must be absent from every card.
# Usage: python -I cards_labels_banned.py <checkout>
import html, json, re, sys
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/AC/AC1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
banned = re.compile(r"roughly|about \d|historically|typically|usually|generally|\.\.\.|…|\bbuilder\b|\bverifier\b|\bround \d|REQUEST", re.I)
label = re.compile(r"(Definition|Proposition|Corollary|Remark|Theorem|Problem|Problem [A-Z]\d*|Section|Lab) (\d+(\.\d+)?|[A-Z]\d*)")
texts: dict[str, str] = {}
miss = 0
for c in cards:
    lesson = c["lesson"]
    if lesson not in texts:
        raw = (root / f"{lesson}.html").read_text(encoding="utf-8")
        texts[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    s = c["front"] + " " + c["back"]
    if banned.search(s):
        print("BANNED", c["id"], banned.search(s).group(0))
    for m in label.finditer(s):
        if m.group(0) not in texts[lesson]:
            miss += 1
            print("LABEL NOT IN LESSON", c["id"], lesson, m.group(0))
print("cards checked", len(cards), "label misses", miss)
