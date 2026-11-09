"""CS2-c-r8: scope and hedge words in the four changed cards, with the card text they come from."""

import json
import re
import sys

ROOT = sys.argv[1]
cards = {c["id"]: c for c in json.load(open(ROOT + "/course/modules/CS/CS2/cards.json", encoding="utf-8"))}
pat = re.compile(r"\b(all|every|only|same|any|always|never|exact|exactly|stable|optimal|each|candidate|hypothes\w*)\b", re.I)
for cid in ("CS2-c200", "CS2-c231", "CS2-c244", "CS2-c245"):
    text = cards[cid]["front"] + " || " + cards[cid]["back"]
    print(cid, [(m.group(0).lower(), text[max(0, m.start() - 30):m.end() + 30]) for m in pat.finditer(text)])
