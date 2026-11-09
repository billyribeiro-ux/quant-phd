"""Round-1 closing-delta checks on CF8 cards.json (read-only). Run with python -I."""
import json, re, html, collections
base = "course/modules/CF/CF8/"
cards = json.load(open(base + "cards.json", encoding="utf-8"))
old = {c["id"]: c for c in json.load(open("/tmp/cf8c-r1-old-cards.json", encoding="utf-8"))}
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05"]:
    raw = open(base + L + ".html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt = txt.replace("{,}", ",")  # LaTeX thousands grouping: 1{,}500{,}000 is printed 1,500,000
    lessons[L] = re.sub(r"\s+", " ", txt)
tok = re.compile(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?")
absent = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    nums = sorted(set(m.group(0).rstrip(",") for m in tok.finditer(text)))
    miss = [n for n in nums if n not in lessons[c["lesson"]]]
    if miss:
        absent += 1
        print("ABSENT", c["id"], c["lesson"], miss)
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}), "cards with absent numbers (grouping-normalised)", absent)
pairs = collections.Counter((c["front"], c["back"]) for c in cards)
print("duplicate (front,back) pairs", sum(1 for v in pairs.values() if v > 1))
print("lesson counts", dict(collections.Counter(c["lesson"] for c in cards)))
print("no grade field", sum(1 for c in cards if "grade" not in c), "no basis field", sum(1 for c in cards if "basis" not in c))
print("grade values", dict(collections.Counter(c.get("grade") for c in cards)))
words = re.compile(r"\b(round|builder|verifier|revision|this slice|fanout|ruling|blind)\b", re.I)
for c in cards:
    for f in ("front", "back"):
        if words.search(c[f]):
            print("PROCESS-WORD", c["id"], f, words.search(c[f]).group(0))
print("process-word scan done")
for c in cards:
    if c["id"] not in old:
        continue
    o = old[c["id"]]
    if o != c:
        ks = [k for k in set(o) | set(c) if o.get(k) != c.get(k)]
        print("CHANGED", c["id"], sorted(ks), "grade_old", o.get("grade"), "grade_new", c.get("grade"))
for c in cards:
    if "R0" in c["front"] + c["back"]:
        print("R0 symbol", c["id"])
