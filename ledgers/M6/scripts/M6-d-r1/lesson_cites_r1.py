import re, pathlib, sys
base = pathlib.Path(sys.argv[1])
allt = "\n".join(p.read_text(encoding="utf-8") for p in base.glob("L*.txt"))
kinds = r"(Definition|Proposition|Lemma|Theorem|Corollary|Example|Remark|Problem|Result|Assumption|Misconception)"
pat = re.compile(r"\b" + kinds + r" (\d+\.\d+|[A-Z]\d+)")
for L in ["L01","L02","L03","L04","L05","L06","L07","L08","L09","L10","L11","L12","project"]:
    t = (base / f"{L}.txt").read_text(encoding="utf-8")
    cites = set(pat.findall(t)); miss = []
    for kind, num in sorted(cites):
        ok = re.search(re.escape(kind + " " + num) + r"(?![\d.])", allt) is not None
        if not ok and kind == "Problem":
            ok = re.search(re.escape(num) + r" ·", allt) is not None
        if not ok: miss.append((kind, num))
    print(L, "cites", len(cites), "missing", miss)
