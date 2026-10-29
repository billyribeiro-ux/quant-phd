"""E5 slice d r3: every number on a card must appear, as a standalone token, in its own lesson page (or in a lab output the card cites).
Usage: python3 -I card_numbers_tight.py <repo-root>"""
import html, json, re, sys
from pathlib import Path
mod = Path(sys.argv[1]) / "course/modules/E/E5"
def text_of(p):
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
lt = {p.stem: text_of(p) for p in mod.glob("L0*.html")}
cards = json.loads((mod / "cards.json").read_text(encoding="utf-8"))
num_re = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:/\d+)?(?![\w])")
miss = []
for c in cards:
    for tok in sorted(set(num_re.findall(c["front"] + " " + c["back"]))):
        if not re.search(r"(?<![\w.])" + re.escape(tok) + r"(?![\w])", lt[c["lesson"]]):
            miss.append((c["id"], c["lesson"], tok))
print("cards", len(cards), "numbers absent from own lesson:", len(miss), miss)
