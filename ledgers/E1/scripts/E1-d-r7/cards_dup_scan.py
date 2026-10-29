"""Near-duplicate scan: Jaccard similarity of word sets (front + back) for every pair of cards, top pairs printed."""
import json, re, sys
from pathlib import Path
cards = json.loads((Path(sys.argv[1]) / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
stop = set("the a an of is and to in for at on by with that this it its be as or from under not no yes does do what how".split())
def toks(c):
    return {w for w in re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()) if w not in stop}
sets = [toks(c) for c in cards]
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        inter = len(sets[i] & sets[j]); uni = len(sets[i] | sets[j])
        if uni: pairs.append((inter / uni, cards[i]["id"], cards[j]["id"]))
pairs.sort(reverse=True)
for s, a, b in pairs[:25]:
    ca = next(c for c in cards if c["id"] == a); cb = next(c for c in cards if c["id"] == b)
    print(f"{s:.2f} {a} {b} | {ca['front'][:70]} || {cb['front'][:70]}")
