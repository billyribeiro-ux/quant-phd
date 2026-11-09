import json, re, sys, pathlib
cards = json.load(open(sys.argv[1]))
txt = {p.stem: p.read_text(encoding="utf-8") for p in pathlib.Path(sys.argv[2]).glob("L*.txt")}
allt = "\n".join(txt.values())
kinds = r"(Definition|Proposition|Lemma|Theorem|Corollary|Example|Remark|Problem|Result|Assumption|Misconception)"
pat = re.compile(r"\b" + kinds + r" (\d+\.\d+|[A-Z]\d+)")
missing = []
checked = 0
for c in cards:
    fields = c["front"] + " " + c["back"]
    for kind, num in set(pat.findall(fields)):
        checked += 1
        # labels appear as "Kind N.M (" or "Kind N.M\n" or "Kind N.M " in lesson text, or Problem "E1 ·", "R3 ·", "P3 ·", "M2 ·"
        ok = re.search(re.escape(kind + " " + num) + r"(?![\d.])", allt) is not None
        if not ok and kind in ("Problem",):
            ok = re.search(re.escape(num) + r" ·", allt) is not None
        if not ok:
            missing.append((c["id"], kind, num, c["lesson"]))
print("citations checked", checked)
print("missing", missing)
