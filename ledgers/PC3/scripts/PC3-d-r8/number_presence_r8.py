"""For every card, list each numeric token on the card that does not occur in the card's own lesson text dump
(or in the lesson's lab output, which the dump includes). Tokens are compared after removing thousands separators."""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
dumps = {}
for lid in [f"L{n:02d}" for n in range(1, 7)]:
    dumps[lid] = pathlib.Path(sys.argv[2], f"{lid}.txt").read_text(encoding="utf-8").replace(",", "").replace("\\", "")
pat = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:/\d+)?")
missing = 0
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    toks = set(pat.findall(text))
    for t in sorted(toks):
        if t in ("1", "2", "3", "0", "4", "5", "6", "10"):
            continue
        if t not in dumps[c["lesson"]] and t not in dumps["L01"] and not any(t in d for d in dumps.values()):
            missing += 1
            print(f"{c['id']} {c['lesson']} token {t!r} not in any lesson dump")
        elif t not in dumps[c["lesson"]]:
            print(f"{c['id']} {c['lesson']} token {t!r} only in another lesson")
print("tokens not in any lesson:", missing)
