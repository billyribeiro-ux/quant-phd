"""Round-9 structure check of AC4 cards.json: ids, lesson files, field sets, grade values, and the changed card."""
import json
import collections
from pathlib import Path

root = Path("/tmp/verify9-AC4-e/course/modules/AC/AC4")
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
keysets = collections.Counter(tuple(sorted(c)) for c in cards)
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}) == len(cards))
print("key sets:", {k: v for k, v in keysets.items()})
lessons = {c["lesson"] for c in cards}
print("lessons cited:", sorted(lessons), "files exist:", all((root / f"{l}.html").exists() for l in lessons))
print("grades:", collections.Counter(c.get("grade") for c in cards))
print("basis present when grade present:", all(("basis" in c) for c in cards if "grade" in c))
c61 = [c for c in cards if c["id"] == "AC4-c061"][0]
print("c061 lesson", c61["lesson"], "front:", c61["front"])
