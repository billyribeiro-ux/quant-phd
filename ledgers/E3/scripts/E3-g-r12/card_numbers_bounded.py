import json, re, sys
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
texts = {L: open(f"{sys.argv[1]}/{L}.txt", encoding="utf-8").read() for L in ("L05", "L06", "L07", "L08")}
num = re.compile(r"(?<![A-Za-z_\d.])(\d+(?:\.\d+)?(?:e-?\d+)?)(?![\d])")
for c in cards:
    if c["lesson"] not in texts:
        continue
    body = c["front"] + " " + c["back"]
    nums = sorted(set(num.findall(body)))
    lesson = texts[c["lesson"]]
    missing = [n for n in nums if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", lesson)]
    print(c["id"], nums, "MISSING:" + str(missing) if missing else "ok")
