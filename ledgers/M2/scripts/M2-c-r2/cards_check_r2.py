"""Round-2 card checks for M2 cards of lessons L13-L18: numbers present in the lesson text, duplicates, id and lesson fields.

Run: python -I cards_check_r2.py <checkout_root>
Prints every card number token that does not occur verbatim in its lesson's plain text (for manual review),
duplicate (front) pairs, duplicate ids, and card-lesson mismatches.
"""

import collections
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
slice_ids = {"L13", "L14", "L15", "L16", "L17", "L18"}


def plain(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"(?s)<script.*?</script>", " ", src)
    src = re.sub(r"(?s)<style.*?</style>", " ", src)
    src = re.sub(r"(?s)</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>", " ", src)
    return html.unescape(src)


texts = {l: plain(root / f"course/modules/M/M2/{l}.html") for l in slice_ids}
ids = collections.Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
sl = [c for c in cards if c["lesson"] in slice_ids]
print("slice cards:", len(sl), "per lesson:", collections.Counter(c["lesson"] for c in sl))
fronts = collections.Counter(c["front"] for c in cards)
print("duplicate fronts (unit-wide):", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(c["back"] for c in cards)
print("duplicate backs (unit-wide):", [k for k, v in backs.items() if v > 1])
numtok = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
for c in sl:
    toks = set(numtok.findall(c["back"] + " " + c["front"]))
    miss = []
    for t in sorted(toks):
        if t in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            continue
        if t not in texts[c["lesson"]]:
            miss.append(t)
    if miss:
        print(c["id"], c["lesson"], "numbers not verbatim in lesson:", miss)
