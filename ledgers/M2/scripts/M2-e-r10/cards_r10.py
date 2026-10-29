"""Round-10 verifier: structural and number-membership scan of M2 cards.json against lesson text (read-only)."""
import html, json, re, collections, pathlib, sys
ROOT = pathlib.Path(sys.argv[1]) / "course/modules/M/M2"
cards = json.load(open(ROOT / "cards.json"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", [k for k, v in collections.Counter(ids).items() if v > 1])
fronts = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("keys:", collections.Counter(tuple(sorted(c)) for c in cards))
print("grades:", collections.Counter(c.get("grade") for c in cards))
print("lessons:", collections.Counter(c["lesson"] for c in cards))
def text(lesson):
    raw = (ROOT / f"{lesson}.html").read_text()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))
texts = {}
miss = []
numtok = re.compile(r"\d+(?:\.\d+)?")
for c in cards:
    L = c["lesson"]
    texts.setdefault(L, text(L))
    for n in set(numtok.findall(c["back"] + " " + c["front"])):
        if n not in texts[L]:
            miss.append((c["id"], L, n))
print("card numbers absent from its lesson text:", len(miss))
for m in miss:
    print("  ", m)
