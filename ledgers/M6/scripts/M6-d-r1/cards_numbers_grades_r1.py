import json, re, pathlib, collections, sys
cards = json.load(open(sys.argv[1]))
txt = {p.stem: p.read_text(encoding="utf-8") for p in pathlib.Path(sys.argv[2]).glob("L*.txt")}
allt = "\n".join(txt.values())
miss = []
for c in cards:
    s = c["front"] + " " + c["back"]
    s = re.sub(r"M6-c\d+|Proposition \d+\.\d+|Lemma \d+\.\d+|Theorem \d+\.\d+|Corollary \d+\.\d+|Definition \d+\.\d+|Example \d+\.\d+|Remark \d+\.\d+|Problem [A-Z]\d+|Result \d+\.\d+|Assumption [A-Z]+|Part [A-Z]|Lab \d|L\d\d|\(\w+\)", " ", s)
    for tok in set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])", s)):
        if tok not in ("0", "1") and tok not in allt:
            miss.append((c["id"], tok))
print("cards", len(cards), "numeric tokens missing from M6 lesson text:", miss)
g = collections.Counter(c.get("grade") for c in cards)
print("grades", dict(g))
print("C without basis", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("invalid grade", [c["id"] for c in cards if c.get("grade") not in ("T", "C", None)])
print("dup ids", len(cards) - len({c["id"] for c in cards}), "dup fronts", len(cards) - len({c["front"] for c in cards}), "dup backs", len(cards) - len({c["back"] for c in cards}))
