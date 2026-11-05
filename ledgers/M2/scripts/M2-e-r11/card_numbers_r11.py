"""Every number in a card's front/back must appear in that card's lesson text (tags stripped, entities decoded)."""
import html, json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
text = {}
for c in cards:
    L = c["lesson"]
    if L not in text:
        raw = (root / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
        raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
        raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
        text[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
bad = 0
for c in cards:
    nums = set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
    missing = sorted(n for n in nums if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", text[c["lesson"]]))
    if missing:
        bad += 1
        print(c["id"], c["lesson"], "numbers not in lesson:", missing)
print("cards checked:", len(cards), "cards with a number absent from their lesson:", bad)
