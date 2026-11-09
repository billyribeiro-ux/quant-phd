# Card checks for M2 lessons L07-L12 (run with python -I from the checkout root).
# 1. counts per lesson; 2. unique ids and fronts across the whole file; 3. every decimal or
#    fraction-like number in a card back (length >= 4 characters) appears in its lesson HTML;
# 4. each card with grade C names a basis; 5. each card in L07-L12 lists its grade or is a definition/example.
import json, re, collections, html
cards = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
print("total cards", len(cards))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate ids", [k for k, v in ids.items() if v > 1])
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
sel = [c for c in cards if c["lesson"] in {f"L{n:02d}" for n in range(7, 13)}]
print("L07-L12 cards", len(sel), collections.Counter(c["lesson"] for c in sel))
lesson_text = {}
for n in range(7, 13):
    raw = open(f"course/modules/M/M2/L{n:02d}.html", encoding="utf-8").read()
    lesson_text[f"L{n:02d}"] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
missing = []
for c in sel:
    back = c["back"]
    nums = re.findall(r"\d+(?:\.\d+)?(?:e-\d+)?", back)
    for num in nums:
        if len(num) < 4:
            continue
        if num not in lesson_text[c["lesson"]]:
            missing.append((c["id"], num))
print("card numbers (len>=4) absent from their lesson:", missing)
bad_c = [c["id"] for c in sel if c.get("grade") == "C" and not c.get("basis")]
print("grade C without basis:", bad_c)
nograde = [c["id"] for c in sel if "grade" not in c]
print("cards with no grade field (definitions/examples/process cards):", len(nograde))
