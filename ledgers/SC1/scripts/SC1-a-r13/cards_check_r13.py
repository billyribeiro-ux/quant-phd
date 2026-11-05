"""Compare SC1 L01-L03 card objects between the previous pin and this pin, and dump them for reading.

Usage: .venv/bin/python -I cards_check_r13.py <checkout root> <previous cards.json path>
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
cur = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
prev_by = {c["id"]: c for c in prev}
cur_by = {c["id"]: c for c in cur}
changed = sorted(i for i in set(prev_by) | set(cur_by) if prev_by.get(i) != cur_by.get(i))
print("cards changed between pins:", changed)
print("changed lessons:", sorted({(cur_by.get(i) or prev_by.get(i))["lesson"] for i in changed}))
l123 = [c for c in cur if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards identical to previous pin:", all(prev_by.get(c["id"]) == c for c in l123), "count", len(l123))
for c in l123:
    print(c["id"], c["lesson"], c.get("grade"), "| F:", c["front"], "| B:", c["back"], "| basis:", c.get("basis"))
