"""Round-3 card checks for SC1 L07 and L08: duplicates, A3 dependence in basis, misconception coverage (BUILDER_RULES 7)."""
import html
import json
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/SC/SC1/cards.json", encoding="utf-8"))
mine = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("cards total:", len(cards), "| L07:", sum(c["lesson"] == "L07" for c in cards),
      "| L08:", sum(c["lesson"] == "L08" for c in cards))
print("duplicate ids:", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts:", [k for k, v in Counter(c["front"].strip().lower() for c in cards).items() if v > 1])

# A3 dependence: cards whose front or back says A3/A4/closed form/Theorem 1.3 must say A3 in basis
for c in mine:
    text = c["front"] + " " + c["back"]
    dep = bool(re.search(r"A3|A4|assum|Theorem 1\.3|closed form|Corollary 1\.[345]|Corollary 1\.3", text))
    if dep and "A3" not in c.get("basis", "") and "assum" not in c.get("basis", "").lower():
        print("basis lacks A3/assumption:", c["id"], "| basis:", c.get("basis", "<none>"), "| front:", c["front"][:90])
    if dep and "A3" not in c.get("basis", "") and re.search(r"Corollary 1\.5\(a\)|Corollary 1\.5\(b\)|Corollary 1\.3|Theorem 1\.3", c.get("basis", "")):
        print("  (dependent card, basis cites theorem but not A3):", c["id"])

# misconception coverage: each misconception paragraph on the page needs a card (BUILDER_RULES 7)
KEYS = {
    "L07": {"same law as": ["same law"], "grid maximum can overstate": ["overstate"],
            "normal one-time marginals": ["normal one-time", "marginals"]},
    "L08": {"finite on every path": ["finite on every path"],
            "terminal value": ["terminal value", "P(B_t"], "mean of tau": ["mean of", "finiteness does not bound"]},
}
for lesson, keys in KEYS.items():
    page = open(f"{ROOT}/course/modules/SC/SC1/{lesson}.html", encoding="utf-8").read()
    wrongs = [html.unescape(re.sub(r"<[^>]+>", "", m)).strip() for m in re.findall(r'<p class="wrong">(.*?)</p>', page, re.S)]
    print(lesson, "misconceptions on page:", len(wrongs))
    lesson_cards = [c for c in cards if c["lesson"] == lesson]
    for w in wrongs:
        hit = [c["id"] for c in lesson_cards if any(k.lower() in (c["front"] + c["back"]).lower() for k in
               sum(([v for v in KEYS[lesson].values()] and [s for ks in KEYS[lesson].values() for s in ks] and [], []) , []) or [])]
        # explicit keyword match against each misconception's own keys
        ids = []
        for name, ks in KEYS[lesson].items():
            if name.lower() in w.lower() or any(k.lower() in w.lower() for k in ks):
                ids = [c["id"] for c in lesson_cards if any(k.lower() in (c["front"] + " " + c["back"]).lower() for k in ks)]
                print(f"  {lesson} misconception [{w[:70]}] -> cards: {ids or 'NONE'}")
                break
        else:
            print(f"  {lesson} misconception [{w[:70]}] -> no key set (manual)")
