import json, re, sys, collections
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M3/cards.json", encoding="utf-8"))
print("n", len(cards), "dup ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("missing grade", [c["id"] for c in cards if "grade" not in c])
lessons = {"L07": "course/modules/M/M3/L07.html", "L08": "course/modules/M/M3/L08.html", "L09": "course/modules/M/M3/L09.html"}
txt = {k: open(f"{root}/{v}", encoding="utf-8").read() for k, v in lessons.items()}
ref = re.compile(r"(Theorem|Proposition|Lemma|Definition|Remark|Example|Problem|Section|Lesson|Fact|Corollary|Assumptions?|F|Lab|Table|L|Step|item)\s*$")
bad = []
for c in cards:
    s = c["back"] + " " + c["front"]
    for m in re.finditer(r"(?<![\w.])(-?\d+\.\d+)(?![\w.])", s):
        pre = s[: m.start()]
        if ref.search(pre[-20:]) or re.search(r"\b(Lesson|L)\s*\d", pre[-12:]):
            continue
        n = m.group(1)
        if n not in txt.get(c["lesson"], ""):
            bad.append((c["id"], n))
print("non-reference decimals not in own lesson:", bad)
for c in cards:
    if c["id"] in ("M3-c126", "M3-c127"):
        print(c["id"], c["lesson"], "grade", c.get("grade"), "| '0.8951' in L07:", "0.8951" in txt["L07"])
