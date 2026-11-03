"""For every L04-L06 card, list number tokens in front/back that do not occur in the cited lesson's visible text."""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/E/E5/cards.json").read_text(encoding="utf-8"))
texts = {}
for L in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/E/E5/{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    texts[L] = html.unescape(re.sub(r"\s+", " ", raw))
num = re.compile(r"(?<![A-Za-z_])(\d+(?:\.\d+)?(?:/\d+)?)(?![\d])")
missing = 0
for c in cards:
    if c.get("lesson") not in texts:
        continue
    body = c["front"] + " " + c["back"]
    toks = sorted(set(num.findall(body)))
    bad = []
    for t in toks:
        if t in ("1", "0", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            # single digits are checked loosely: they must appear as a standalone token in the lesson
            pass
        if re.search(r"(?<![\d.])" + re.escape(t) + r"(?![\d])", texts[c["lesson"]]) is None:
            bad.append(t)
    if bad:
        missing += 1
        print(c["id"], c["lesson"], "tokens not in lesson text:", bad)
print("cards with unmatched number tokens:", missing, "of", sum(1 for c in cards if c.get("lesson") in texts))
