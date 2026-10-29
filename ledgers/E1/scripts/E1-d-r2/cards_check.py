import html, json, re, sys
from collections import Counter
ROOT = "/tmp/verifyB2-E1-d/course/modules/E/E1/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("count", len(cards), "unique ids", len(set(ids)), "sequential", ids == [f"E1-c{i:03d}" for i in range(1, len(ids) + 1)])
print("keys", Counter(tuple(sorted(c)) for c in cards))
print("grades", Counter(c.get("grade") for c in cards))
print("cite nonempty", [c["id"] for c in cards if c.get("cite")])
text = {}
for L in [f"L0{i}" for i in range(1, 10)]:
    raw = open(ROOT + L + ".html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text[L] = re.sub(r"\s+", " ", t)
    open(f"/tmp/E1d-r2/{L}.txt", "w").write(text[L])
missing = []
for c in cards:
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
    for n in sorted(nums):
        if n not in text[c["lesson"]]:
            missing.append((c["id"], c["lesson"], n))
print("numbers absent from lesson text:", len(missing))
for m in missing: print("  ", m)
nb = [c["id"] for c in cards if c.get("grade") == "T" and re.search(r"\d", c["back"]) and not c.get("basis") and not c.get("cite")]
print("T cards with digits and no basis/cite:", len(nb), nb)
print("C cards:", [(c["id"], c.get("basis")) for c in cards if c.get("grade") == "C"])
