import json, re, sys
root = sys.argv[1]
cards = json.load(open(root + "/course/modules/AC/AC4/cards.json", encoding="utf-8"))
texts = {}
for lid in ("L03", "L04"):
    texts[lid] = open(f"{root}/course/modules/AC/AC4/{lid}.html", encoding="utf-8").read()
twin = {"L03": open(f"{root}/tests/labs/AC4/lab-AC4-L03-1.py", encoding="utf-8").read(),
        "L04": open(f"{root}/tests/labs/AC4/lab-AC4-L04-1.py", encoding="utf-8").read()}
for c in cards:
    if c["lesson"] not in ("L03", "L04"):
        continue
    nums = re.findall(r"\d[\d,]*(?:\.\d+)?", c["back"] + " " + c["front"])
    miss = []
    for n in nums:
        n2 = n.rstrip(".,")
        if not (n2 in texts[c["lesson"]] or n2.replace(",", "") in texts[c["lesson"]] or n2 in twin[c["lesson"]]):
            miss.append(n2)
    print(c["id"], c["lesson"], "nums", nums, "missing-from-lesson-or-twin", miss)
