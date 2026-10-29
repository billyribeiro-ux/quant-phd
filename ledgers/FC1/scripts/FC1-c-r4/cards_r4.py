"""Round 4: structural and label checks on cards.json (FC1 slice c). Reads only the checkout."""
import collections, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)), "ids contiguous", sorted(int(i[-3:]) for i in ids) == list(range(1, len(ids) + 1)))
print("duplicate fronts", [f for f, n in collections.Counter(c["front"] for c in cards).items() if n > 1])
print("lessons", dict(collections.Counter(c["lesson"] for c in cards)))
print("grades", dict(collections.Counter(c.get("grade") for c in cards)))
print("C without basis", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("non-T without basis or cite, no grade set, lab-citing:",
      [c["id"] for c in cards if "grade" not in c and re.search(r"Lab \d", c["back"])])
print("process words", [c["id"] for c in cards if re.search(r"builder|verifier|round \d|planner", json.dumps(c), re.I)])
print("fill-effect wording c067:", [c["back"] for c in cards if c["id"] == "FC1-c067"])
