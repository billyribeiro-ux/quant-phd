"""Dump the retrieval cards of lessons L07 to L12 and scan the whole cards.json for duplicate ids, fronts and backs."""
import collections
import json
import sys

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in ("L07", "L08", "L09", "L10", "L11", "L12")]
for c in slice_cards:
    print(c["id"], c["lesson"], "| F:", c["front"], "| B:", c["back"])
print("slice cards:", len(slice_cards), "total cards:", len(cards))
print("duplicate ids:", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts:", [k for k, v in collections.Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("duplicate backs:", [k[:60] for k, v in collections.Counter(c["back"].strip().lower() for c in cards).items() if v > 1])
