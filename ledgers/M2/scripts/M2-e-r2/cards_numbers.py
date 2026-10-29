"""For every card in cards.json: list each number in its front/back and whether that number's text appears in its lesson page."""
import json, re, html, sys
from pathlib import Path
base = Path(sys.argv[1])
cards = json.load(open(base / "cards.json", encoding="utf-8"))
texts = {}
def lesson_text(l):
    if l not in texts:
        raw = (base / f"{l}.html").read_text(encoding="utf-8")
        raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
        raw = re.sub(r"<[^>]+>", " ", raw)
        texts[l] = re.sub(r"\s+", " ", html.unescape(raw))
    return texts[l]
NUM = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?(?:e[-+]?\d+)?)(?![\w])")
missing = []
for c in cards:
    lt = lesson_text(c["lesson"])
    for field in ("front", "back"):
        for n in set(NUM.findall(c[field])):
            if n not in lt:
                missing.append((c["id"], c["lesson"], field, n))
for m in missing: print(*m)
print("cards", len(cards), "numbers-not-in-lesson", len(missing))
