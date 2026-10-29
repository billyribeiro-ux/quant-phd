"""Round-5 card checks: text extraction, label presence, number presence, duplicates."""
import html, json, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyC5-E3-d/course/modules/E/E3/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
texts = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    s = open(ROOT + L + ".html", encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s)
    texts[L] = s
    open(f"/tmp/E3d_r5_{L}.txt", "w").write(s)
# duplicates
seen = {}
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
for c in cards:
    for k in ("front", "back"):
        key = re.sub(r"\W+", " ", c[k].lower()).strip()
        seen.setdefault(key, []).append(c["id"])
print("exact duplicate texts:", [v for v in seen.values() if len(v) > 1])
fronts = {}
for c in cards:
    fronts.setdefault(re.sub(r"\W+", " ", c["front"].lower()).strip(), []).append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
# numbers
num_re = re.compile(r"\d[\d,\.]*\d|\d")
for c in cards:
    txt = c["front"] + " " + c["back"]
    nums = set(num_re.findall(txt))
    lesson = texts[c["lesson"]]
    miss = []
    for n in sorted(nums):
        n2 = n.rstrip(".,")
        if not n2:
            continue
        if n2 not in lesson and n2.replace(",", "") not in lesson.replace(",", ""):
            miss.append(n2)
    if miss:
        print("NUMBER NOT IN LESSON", c["id"], c["lesson"], miss)
