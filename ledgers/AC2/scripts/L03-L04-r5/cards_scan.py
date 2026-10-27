"""Round-5 cards scan: count, contiguity, duplicates, and which L03/L04 cards differ from pin 2607c60."""
import json, subprocess, sys
from collections import Counter

root = sys.argv[1]
new = json.load(open(f"{root}/course/modules/AC/AC2/cards.json", encoding="utf-8"))
old = json.loads(subprocess.run(["git", "-C", root, "show", "2607c60:course/modules/AC/AC2/cards.json"],
                                capture_output=True, text=True, check=True).stdout)
ids = [c["id"] for c in new]
print("cards", len(new), "ids contiguous", ids == [f"AC2-c{i:03d}" for i in range(1, len(new) + 1)])
print("dup fronts", sum(v - 1 for v in Counter(c["front"] for c in new).values() if v > 1),
      "dup backs", sum(v - 1 for v in Counter(c["back"] for c in new).values() if v > 1))
oldmap = {c["id"]: c for c in old}
changed = [c["id"] for c in new if oldmap.get(c["id"]) != c]
print("changed vs 2607c60:", changed)
print("L03/L04 cards:", [c["id"] for c in new if c["lesson"] in ("L03", "L04")])
print("L03/L04 changed:", [i for i in changed if any(c["id"] == i and c["lesson"] in ("L03", "L04") for c in new)])
print("L03/L04 byte-identical count:", sum(1 for c in new if c["lesson"] in ("L03", "L04") and oldmap.get(c["id"]) == c),
      "of", sum(1 for c in new if c["lesson"] in ("L03", "L04")))
