import html, json, re
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-M3-b"
cards = json.load(open(f"{ROOT}/course/modules/M/M3/cards.json", encoding="utf-8"))
pages = {}
for lab in ["L04", "L05", "L06"]:
    t = open(f"{ROOT}/course/modules/M/M3/{lab}.html", encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    pages[lab] = html.unescape(re.sub(r"<[^>]+>", " ", t))
slice_cards = [c for c in cards if c["lesson"] in pages]
print("slice cards", len(slice_cards), "total", len(cards), "unique ids", len({c["id"] for c in cards}))
for c in slice_cards:
    nums = set(re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c["back"] + " " + c["front"]))
    text = pages[c["lesson"]]
    missing = sorted(n for n in nums if n not in text and n not in ("1", "2", "3", "0"))
    print(c["id"], c["lesson"], c.get("grade"), "basis" if c.get("basis") else "-", "numbers-not-in-lesson:", missing)
