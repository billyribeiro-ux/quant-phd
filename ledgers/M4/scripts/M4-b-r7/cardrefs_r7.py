import json, re, sys
cards = json.load(open(sys.argv[1]))
txt = {}
for L in ["L05", "L06", "L07"]:
    txt[L] = open(f"{sys.argv[2]}/{L}.txt", encoding="utf-8").read()
allt = "\n".join(txt.values())
for c in cards:
    if c["lesson"] not in txt:
        continue
    refs = re.findall(r"\b(Definition|Proposition|Lemma|Remark|Example|Problem|Assumption|Misconception)\s+([PMRE]?\d+(?:\.\d+)?)", c["back"] + " " + c["front"])
    for kind, num in refs:
        pat = re.compile(r"(?m)^(?:\S*\s)?" + kind + r"\s+" + re.escape(num) + r"\b")
        pat2 = re.compile(re.escape(kind + " " + num) + r"\b")
        ok = bool(pat2.search(allt)) 
        if not ok:
            print(c["id"], c["lesson"], "MISSING", kind, num)
print("refs checked")
