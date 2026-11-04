import json, re, sys, glob, os
cards = json.load(open(sys.argv[1], encoding="utf-8"))
tdir = sys.argv[2]
ldir = sys.argv[3]
def lesson_text(n):
    full = os.path.join(ldir, f"L0{n}_full.txt")
    base = os.path.join(ldir, f"L0{n}.txt")
    txt = open(full if os.path.exists(full) else base, encoding="utf-8").read()
    labs = open(os.path.join(tdir, f"lab-SC1-L0{n}-1.stdout"), encoding="utf-8").read()
    return txt + "\n" + labs
pat = re.compile(r"\d+\.\d+|\d+/\d+|\d+e-\d+|10\^\(?-\d+\)?|\b\d{2,}\b")
missing = []
for c in cards:
    n = int(c["lesson"][1:])
    txt = lesson_text(n).replace(" ", "")
    for tok in set(pat.findall(c["back"] + " " + c["front"])):
        t = tok.replace(" ", "")
        if t in ("10", "2", "3", "1") : continue
        if t not in txt:
            missing.append((c["id"], c["lesson"], tok))
for m in missing: print(m)
print("numbers not found verbatim in lesson or lab stdout:", len(missing))
