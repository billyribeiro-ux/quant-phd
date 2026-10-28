"""Round 17 (AC1-c): which card objects differ between the previous pin (af08ad1) and fefbf8b.

Usage: python -I card_delta_r17.py <old cards.json> <new cards.json>
Prints ids changed, ids added, ids removed, and the ids unchanged among cards of lessons L07 and L08.
"""

import json
import sys
from pathlib import Path

old = {c["id"]: c for c in json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))}
new = {c["id"]: c for c in json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))}
changed = sorted(i for i in old if i in new and old[i] != new[i])
added = sorted(i for i in new if i not in old)
removed = sorted(i for i in old if i not in new)
print("changed:", changed)
print("added:", added)
print("removed:", removed)
unchanged_78 = sorted(i for i in new if i in old and old[i] == new[i] and new[i]["lesson"] in ("L07", "L08"))
print("unchanged L07/L08 cards:", len(unchanged_78), unchanged_78)
