"""Near-duplicate scan for the M2 deck (verifier round 3, slice d2): pairs with a card of L22-L24."""
import difflib
import json
from pathlib import Path

cards = json.loads(Path("course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
slice_cards = [c for c in cards if c["lesson"] in ("L22", "L23", "L24")]
pairs = 0
for a in slice_cards:
    for b in cards:
        if b["id"] == a["id"]:
            continue
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.75:
            pairs += 1
            print(f"front ratio {r:.2f}: {a['id']} [{a['front'][:70]}] vs {b['id']} [{b['front'][:70]}]")
print("pairs with front similarity >= 0.75:", pairs)
# every card number of a slice card must appear in its lesson text (numbers with 3+ digits or decimals)
import re
for c in slice_cards:
    text = Path(f"course/modules/M/M2/{c['lesson']}.html").read_text(encoding="utf-8")
    nums = set(re.findall(r"\d+\.\d+(?:e[-+]?\d+)?|\d{3,}", c["back"]))
    missing = [n for n in nums if n not in text]
    if missing:
        print("NUMBER NOT IN LESSON", c["id"], missing)
print("number-in-lesson scan done for", len(slice_cards), "cards")
