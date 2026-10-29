"""Every number in each card's front and back must occur in the plain text of the card's lesson page (or a lesson lab output)."""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1]) / "course/modules/AC/AC4"
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
def plain(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)
texts = {}
miss = []
for c in cards:
    lesson = c["lesson"]
    if lesson not in texts:
        texts[lesson] = plain(ROOT / f"{lesson}.html")
    body = texts[lesson].replace("\\", "")
    compact = re.sub(r"[\s{},]", "", body)
    for field in ("front", "back"):
        for tok in re.findall(r"\d[\d,]*(?:\.\d+)?", c[field]):
            t = tok.rstrip(",")
            if not t:
                continue
            if t in body or t.replace(",", "") in compact or ("{" + t) in texts[lesson]:
                continue
            miss.append((c["id"], lesson, field, t))
print("cards", len(cards), "numbers not found verbatim in the lesson text:", len(miss))
for m in miss:
    print("MISS", *m)
