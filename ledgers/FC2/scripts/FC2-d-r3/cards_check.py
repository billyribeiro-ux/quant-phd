"""Round-3 cards check for FC2: duplicates, schema, every number and every quoted label on a card appears in its lesson."""
import collections
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
MOD = ROOT / "course/modules/FC/FC2"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "keys:", collections.Counter(tuple(sorted(c)) for c in cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", [i for i, n in collections.Counter(ids).items() if n > 1])
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
fronts = collections.Counter(norm(c["front"]) for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(norm(c["back"]) for c in cards)
print("duplicate backs:", [f[:80] for f, n in backs.items() if n > 1])
lessons = {}
for lid in sorted({c["lesson"] for c in cards}):
    raw = (MOD / f"{lid}.html").read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    lessons[lid] = re.sub(r"\s+", " ", text)
bad = []
for c in cards:
    text = lessons[c["lesson"]]
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
    missing = sorted(n for n in nums if n not in text)
    if missing:
        bad.append((c["id"], missing))
print("cards with a number absent from their lesson:", bad)
for c in cards:
    if "  " in c["front"] + c["back"] or c["front"] != c["front"].strip() or c["back"] != c["back"].strip():
        print("whitespace issue:", c["id"])
print("per-lesson counts:", dict(collections.Counter(c["lesson"] for c in cards)))
