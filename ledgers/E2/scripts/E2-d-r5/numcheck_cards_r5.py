import json, re, html, glob, sys
changed = sys.argv[1].split(",")
cards = {x["id"]: x for x in json.load(open("cards.json", encoding="utf-8"))}
def norm_lesson(lesson):
    t = open(f"{lesson}.html", encoding="utf-8").read()
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = t.replace("{,}", "").replace("\\,", "")
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)
    return t
cache = {}
for cid in changed:
    c = cards[cid]
    L = c["lesson"]
    if L not in cache:
        cache[L] = norm_lesson(L)
    text = cache[L]
    back = c["back"] + " " + c["front"]
    back = re.sub(r"(?<=\d),(?=\d{3})", "", back)
    nums = set(re.findall(r"\d+(?:\.\d+)?", back))
    missing = sorted(n for n in nums if n not in text and not (n.endswith(".0")))
    print(cid, L, "numbers:", sorted(nums)[:14], "MISSING in lesson:", missing)
