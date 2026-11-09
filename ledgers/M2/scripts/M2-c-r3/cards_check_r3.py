"""cards.json checks for L13-L18 (verifier round 3): ids, fronts, grades, basis, and card numbers present in the lesson text."""
import collections, html, json, re
cards = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
sl = [c for c in cards if c["lesson"] in ("L13", "L14", "L15", "L16", "L17", "L18")]
print("slice cards", len(sl), dict(collections.Counter(c.get("grade", "none") for c in sl)))
for c in sl:
    if c.get("grade") == "C" and not c.get("basis"):
        print("C card without basis", c["id"])
lessons = {n: html.unescape(re.sub(r"<[^>]+>", " ", open(f"course/modules/M/M2/{n}.html", encoding="utf-8").read())) for n in ("L13", "L14", "L15", "L16", "L17", "L18")}
for c in sl:
    text = lessons[c["lesson"]]
    nums = set(re.findall(r"\d+\.\d{3,}", c["back"]))
    missing = sorted(n for n in nums if n not in text)
    if missing:
        print(c["id"], "numbers not in lesson text:", missing)
print("number check done")
