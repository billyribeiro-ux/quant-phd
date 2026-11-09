# Full-scan of course/modules/M/M5/cards.json (all lessons): duplicate ids, duplicate fronts, duplicate backs (case-folded),
# per-lesson counts, grades, and cards whose lesson is in slice a. Run from the checkout root.
import json
from collections import Counter
cs = json.load(open("course/modules/M/M5/cards.json", encoding="utf-8"))
print("cards", len(cs))
ids = Counter(c["id"] for c in cs)
print("duplicate ids", [i for i, n in ids.items() if n > 1])
fr = Counter(c["front"].strip().casefold() for c in cs)
print("duplicate fronts", [f[:60] for f, n in fr.items() if n > 1])
bk = Counter(c["back"].strip().casefold() for c in cs)
print("duplicate backs", [b[:60] for b, n in bk.items() if n > 1])
print("keys", sorted(set(k for c in cs for k in c)))
print("per lesson", sorted(Counter(c["lesson"] for c in cs).items()))
print("grades", Counter(c.get("grade") for c in cs))
sl = [c["id"] for c in cs if c["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice-a cards", len(sl), sl[0], sl[-1])
