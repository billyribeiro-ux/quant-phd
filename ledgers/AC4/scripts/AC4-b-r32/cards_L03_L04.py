import html, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", cards)
text = {}
for u in ("L03", "L04"):
    raw = (root / f"course/modules/AC/AC4/{u}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text[u] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
ids = []
for c in cards:
    if c.get("lesson") not in ("L03", "L04"):
        continue
    ids.append(c["id"])
    back = c["back"] + " " + c["front"]
    nums = set(re.findall(r"\d[\d,\.]*\d|\d", back))
    missing = [n for n in nums if n.replace(",", "") not in text[c["lesson"]].replace(",", "")]
    print(c["id"], c["lesson"], c.get("grade"), "numbers", len(nums), "missing", missing)
print("count", len(ids), ids)
