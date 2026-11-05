"""Round-11: extract the L04-L06 cards of cards.json to outputs/cards_L04_L06_r11.txt (every card printed)."""
import collections
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
cards = json.loads((ROOT / "course/modules/E/E4/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
print("duplicate ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
sel = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards", len(sel))
for c in sel:
    print(json.dumps(c, ensure_ascii=False))
