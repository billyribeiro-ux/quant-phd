"""Round-9 check of course/modules/M/M4/cards.json: count, id uniqueness, grade values, lesson links, duplicate fronts and
backs (exact and normalised), and the cards changed since the round-8 pin (2d755599). Usage: python -I <this file>
"""
import collections
import json
import pathlib
import re
import subprocess

root = pathlib.Path.cwd()
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
print("type", type(cards).__name__, "count", len(cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)) == len(ids), "first", ids[0], "last", ids[-1])
print("keys", sorted({tuple(sorted(c)) for c in cards}))
print("grades", collections.Counter(c["grade"] for c in cards))
print("lessons", collections.Counter(c["lesson"] for c in cards))
nums = sorted(int(re.sub(r"\D", "", i)) for i in ids)
print("id numbers contiguous", nums == list(range(nums[0], nums[-1] + 1)), "missing", sorted(set(range(nums[0], nums[-1] + 1)) - set(nums)))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


fronts = collections.Counter(norm(c["front"]) for c in cards)
print("exact-normalised duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(norm(c["back"]) for c in cards)
print("exact-normalised duplicate backs:", [k for k, v in backs.items() if v > 1])
for c in cards:
    if c["front"].strip() == "" or c["back"].strip() == "":
        print("EMPTY", c["id"])
# lesson-level number tokens: every digit token in a card's front/back must appear in the cited lesson's html
lesson_text = {}
for c in cards:
    lid = c["lesson"]
    if lid not in lesson_text:
        p = root / f"course/modules/M/M4/{lid}.html"
        lesson_text[lid] = p.read_text(encoding="utf-8") if p.exists() else ""
missing = []
for c in cards:
    for tok in set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"])):
        if tok not in lesson_text[c["lesson"]]:
            missing.append((c["id"], tok))
print("card number tokens absent from the cited lesson:", missing)
diff = subprocess.run(["git", "diff", "2d755599", "HEAD", "--", "course/modules/M/M4/cards.json"], capture_output=True, text=True).stdout
print("cards.json changed since 2d755599:", len(diff) > 0)
old = subprocess.run(["git", "show", "2d755599:course/modules/M/M4/cards.json"], capture_output=True, text=True).stdout
oldc = json.loads(old)
print("old count", len(oldc), "new count", len(cards))
oi = {c["id"]: c for c in oldc}
ni = {c["id"]: c for c in cards}
print("removed ids", sorted(set(oi) - set(ni)), "added ids", sorted(set(ni) - set(oi)))
for i in sorted(set(oi) & set(ni)):
    if oi[i] != ni[i]:
        print("changed", i, {k: (oi[i][k], ni[i][k]) for k in oi[i] if oi[i][k] != ni[i].get(k)})
