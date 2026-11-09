"""For every card: list each number token (integers, fractions, decimals, percentages) in front/back and
report whether it occurs in the card's own lesson text, in any LX2 lesson text, or in the lab outputs.

Usage: python3 -I card_numbers_r14.py <cards.json> <scratch_dir_with_L0x.txt> <run_dir>
A token found nowhere is printed as MISS for manual reading. Structural checks (duplicate ids, duplicate
fronts, lesson field vs. lesson text) are printed first.
"""
import glob
import json
import re
import sys

cards_path, scratch, run_dir = sys.argv[1], sys.argv[2], sys.argv[3]
cards = json.load(open(cards_path, encoding="utf-8"))

ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
fronts = [c["front"] for c in cards]
dup_fronts = {f for f in fronts if fronts.count(f) > 1}
print("duplicate fronts:", sorted(dup_fronts) if dup_fronts else "none")
backs = [c["back"] for c in cards]
dup_backs = {b for b in backs if backs.count(b) > 1}
print("duplicate backs:", len(dup_backs))
print("lesson values:", sorted({c["lesson"] for c in cards}))
print("cards per lesson:", {l: sum(1 for c in cards if c["lesson"] == l) for l in ("L01", "L02", "L03", "L04")})

lesson_text = {}
for path in sorted(glob.glob(f"{scratch}/*L0[1-4].txt")):
    key = re.search(r"L0[1-4]", path).group(0)
    lesson_text[key] = open(path, encoding="utf-8").read()
lab_text = "".join(open(p, encoding="utf-8").read() for p in sorted(glob.glob(f"{run_dir}/*.out")))
all_lessons = "\n".join(lesson_text.values())

TOKEN = re.compile(r"\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?%|\d+(?:[.,]\d+)*")


def norm_num(tok: str) -> str:
    return tok.replace(",", "")


misses = []
for c in cards:
    own = lesson_text.get(c["lesson"], "")
    for field in ("front", "back"):
        for tok in TOKEN.findall(c[field]):
            t = norm_num(tok.rstrip("%"))
            if t in ("1", "0", "2") and field == "front":
                pass
            in_own = t in own or tok in own
            in_all = t in all_lessons or tok in all_lessons
            in_lab = t in lab_text or tok in lab_text
            if not (in_own or in_all or in_lab):
                misses.append((c["id"], field, tok))
            elif not in_own:
                pass
print("number tokens not found in any LX2 lesson text or lab output:")
for m in misses:
    print("  MISS", *m)
print("total misses", len(misses))
