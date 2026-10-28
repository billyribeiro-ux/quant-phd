"""Card scan for CF1 (round 10): ids, duplicates, grades, cite-or-basis, registry keys, per-lesson counts.

Usage (run with -I): cards_scan.py <checkout>
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/CF/CF1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "sequential ids", ids == [f"CF1-c{i:03d}" for i in range(1, len(ids) + 1)])
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("duplicate fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
print("grades", dict(collections.Counter(c["grade"] for c in cards)))
print("without cite or basis", [c["id"] for c in cards if not (c.get("cite") or c.get("basis"))])
entries = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))["entries"]
keys = {e["key"] for e in entries}
print("cite keys missing from registry", [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys])
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
