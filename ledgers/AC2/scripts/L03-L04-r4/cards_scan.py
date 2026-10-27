"""Round-4 card scan: 140 cards, contiguous ids, no duplicate fronts or backs; L03/L04 cards vs pin 4a8690a (byte level)."""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
new_raw = (root / "course/modules/AC/AC2/cards.json").read_bytes()
old_raw = subprocess.run(["git", "-C", str(root), "show", "4a8690a:course/modules/AC/AC2/cards.json"],
                         capture_output=True, check=True).stdout
new = json.loads(new_raw)
old = {c["id"]: c for c in json.loads(old_raw)}
ids = [c["id"] for c in new]
print("count", len(new), "unique ids", len(set(ids)), "contiguous c001-c140", sorted(ids) == [f"AC2-c{i:03d}" for i in range(1, 141)])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
print("dup fronts", [k for k, v in Counter(norm(c["front"]) for c in new).items() if v > 1])
print("dup backs", [k[:60] for k, v in Counter(norm(c["back"]) for c in new).items() if v > 1])
mine = [c for c in new if c["lesson"] in ("L03", "L04")]
same = [c["id"] for c in mine if json.dumps(c, sort_keys=True) == json.dumps(old.get(c["id"]), sort_keys=True)]
print("L03/L04 cards", len(mine), "byte-identical to 4a8690a", len(same))
print("changed", [c["id"] for c in mine if c["id"] not in same])
