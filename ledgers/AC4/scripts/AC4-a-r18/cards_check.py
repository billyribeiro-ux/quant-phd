import json, re, html, sys
root = "/tmp/verify18-AC4-a/course/modules/AC/AC4/"
cards = json.load(open(root + "cards.json"))
def text(p):
    s = open(root + p, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s))
T = {"L01": text("L01.html"), "L02": text("L02.html")}
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)))
dups = {i for i in ids if ids.count(i) > 1}
print("duplicate ids", dups)
fronts = [c["front"] for c in cards]
print("duplicate fronts", [f for f in set(fronts) if fronts.count(f) > 1])
for c in cards:
    if c["lesson"] not in T: continue
    nums = re.findall(r"\d[\d,]*\.?\d*", c["back"])
    miss = [n.rstrip(".") for n in nums if n.rstrip(".").replace(",", "") and n.rstrip(".") not in T[c["lesson"]]]
    if miss:
        print(c["id"], c["lesson"], "numbers not in lesson text:", miss)
print("L01/L02 cards:", sum(1 for c in cards if c["lesson"] in ("L01","L02")))
for c in cards:
    if c["id"] in ("AC4-c008","AC4-c018","AC4-c125"):
        print(c["id"], c["grade"], c.get("basis"), "|", c["back"])
