"""Round-4 slice a: print every card of lessons L01-L06 with its index, and every card anywhere in M2 that shares a lesson-number-free key fact with them (by id list)."""
import json
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
print("total cards:", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
fronts = [c["front"] for c in cards]
print("duplicate fronts:", sorted({f for f in fronts if fronts.count(f) > 1}))
slice_lessons = {"L01", "L02", "L03", "L04", "L05", "L06"}
n = 0
for idx, c in enumerate(cards):
    if c["lesson"] in slice_lessons:
        n += 1
        print(f"[{idx}] {c['id']} {c['lesson']} grade={c.get('grade')} basis={c.get('basis')!r}")
        print(f"   F: {c['front']}")
        print(f"   B: {c['back']}")
print("slice card count:", n)
print("keys used:", sorted({k for c in cards for k in c}))
