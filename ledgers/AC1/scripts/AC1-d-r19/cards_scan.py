# Scans course/modules/AC/AC1/cards.json: duplicates, grade field, numbers and cited labels against the card's lesson.
import html, json, re, sys
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/AC/AC1/cards.json", encoding="utf-8"))
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
print("dup fronts", [k for k, v in Counter(c["front"] for c in cards).items() if v > 1])
print("dup backs", [k[:60] for k, v in Counter(c["back"] for c in cards).items() if v > 1])
print("grades", Counter(c.get("grade") for c in cards))
texts = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = open(f"{root}/course/modules/AC/AC1/{L}.html", encoding="utf-8").read()
    texts[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    texts[L] = re.sub(r"\s+", " ", texts[L])
bad = []
for c in cards:
    t = texts[c["lesson"]]
    nums = re.findall(r"\d[\d,]*\.?\d*", c["back"])
    for n in nums:
        n2 = n.rstrip(".,")
        if n2 and n2 not in t and n2.replace(",", "") not in t.replace(",", ""):
            bad.append((c["id"], "number", n2))
    for lab in re.findall(r"\((?:Definition|Proposition|Theorem|Corollary|Remark|Example|Problem|Lab) [\d.]+[^)]*\)", c["back"] + " " + c["front"]):
        key = re.match(r"\((\w+ [\d.]+)", lab).group(1).rstrip(".")
        if key not in t:
            bad.append((c["id"], "label", key))
print("flagged (number or label not found in its lesson text, a lead to check by hand):", bad)
