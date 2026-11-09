"""Structural scan of course/modules/FC/FC1/cards.json: ids, duplicates, lessons, grades, per-lesson counts."""
import json
from collections import Counter
from pathlib import Path

cards = json.loads(Path("/Users/billyribeiro/.fanout/wt/verifyF11-FC1-c/course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
print("cards", len(cards))
print("duplicate ids", sorted(i for i, n in Counter(c["id"] for c in cards).items() if n > 1))
print("duplicate fronts (case-insensitive)", sorted(f for f, n in Counter(c["front"].strip().lower() for c in cards).items() if n > 1))
print("duplicate backs (case-insensitive)", sorted(b[:50] for b, n in Counter(c["back"].strip().lower() for c in cards).items() if n > 1))
print("per lesson", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("grades", dict(Counter(c.get("grade", "(none)") for c in cards)))
print("ids not matching FC1-cNNN", [c["id"] for c in cards if not c["id"].startswith("FC1-c") or len(c["id"]) != 8])
