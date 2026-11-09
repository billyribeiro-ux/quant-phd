"""Round-14 markup scan: raw '<' in text outside tags, pre, script and style blocks, for L04-L06; plus the L04-L06 card extract."""

import collections
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b")
OUT = ROOT / "ledgers/PC3/scripts/PC3-b-r14/out"
for page in ("L04", "L05", "L06"):
    s = (ROOT / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    s2 = re.sub(r"<pre.*?</pre>", "", s, flags=re.S)
    s2 = re.sub(r"<script.*?</script>|<style.*?</style>", "", s2, flags=re.S)
    print(f"{page}: raw '<' outside tags = {len(re.findall(r'<(?![a-zA-Z/!])', s2))}")
    print(f"{page}: data-hours = {re.findall(r'data-hours=\"(\d+)\"', s)[:1]}")
cards = json.loads((ROOT / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "duplicate ids", [i for i, n in collections.Counter(ids).items() if n > 1])
print("by lesson", dict(collections.Counter(c["lesson"] for c in cards)))
lines = []
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06"):
        lines.append(f"{c['id']} | {c['lesson']} | grade={c.get('grade')} | cite={c.get('cite')}")
        lines.append(f"   F: {c['front']}")
        lines.append(f"   B: {c['back']}")
(OUT / "cards_L456_r14.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("L04-L06 cards written:", sum(1 for c in cards if c["lesson"] in ("L04", "L05", "L06")))
