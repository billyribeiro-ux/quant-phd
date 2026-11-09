# Round-5: list the slice cards (lesson L04-L06) and the deck totals from cards.json; counts per lesson.
import json
from collections import Counter
cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyS5-FC2-b/course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("deck", len(cards), "unique ids", len({c["id"] for c in cards}))
print(sorted(Counter(c["lesson"] for c in cards).items()))
sl = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice", len(sl), dict(Counter(c["lesson"] for c in sl)))
print("ungraded slice", [c["id"] for c in sl if "grade" not in c])
print("C-graded slice", [c["id"] for c in sl if c.get("grade") == "C"])
print("T-graded slice", len([c for c in sl if c.get("grade") == "T"]))
