"""Round 3 M2-a: duplicate ids and duplicate normalised fronts over the whole M2 cards.json."""
import collections, json, re
cards = json.load(open("/tmp/verifyB3-M2-a/course/modules/M/M2/cards.json"))
print("cards:", len(cards))
print("duplicate ids:", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("'", ""))
dup = [(k, v) for k, v in collections.Counter(norm(c["front"]) for c in cards).items() if v > 1]
print("normalised duplicate fronts:", len(dup))
for c in cards:
    if norm(c["front"]) in {k for k, _ in dup}:
        print(c["id"], c["lesson"], c["front"])
