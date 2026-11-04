"""Full duplicate scan of course/modules/M/M2/cards.json and listing of the L22-L24 cards."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("course/modules/M/M2/cards.json")
cards = json.loads(path.read_text(encoding="utf-8"))
print("cards:", len(cards), "keys:", sorted({k for c in cards for k in c}))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [i for i, n in ids.items() if n > 1])
fronts = Counter(re.sub(r"\s+", " ", c["front"].strip().lower()) for c in cards)
print("duplicate normalized fronts:", [(f, n) for f, n in fronts.items() if n > 1])
backs = Counter(re.sub(r"\s+", " ", c["back"].strip().lower()) for c in cards)
print("duplicate normalized backs:", [(b[:60], n) for b, n in backs.items() if n > 1])
by_lesson = Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(by_lesson.items())))
for c in cards:
    if c["lesson"] in ("L22", "L23", "L24"):
        print(json.dumps(c, ensure_ascii=False))
