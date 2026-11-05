"""Round 13: every curly-quoted passage in cards.json (front/back) must occur, after normalising
whitespace, quote marks, dashes and bracketed alterations, in an admitted source text read from the
round-11 scratch copies or in the lesson text. Usage: python3 -I quote_cards_r13.py <cards.json> <src_dir> <lesson_dir>"""
import json, re, sys, os, glob
cards = json.load(open(sys.argv[1], encoding="utf-8"))
src_dir, lesson_dir = sys.argv[2], sys.argv[3]
def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-").replace("­", "")
    s = re.sub(r"\[[^\]]*\]", " ", s)  # bracketed alterations
    s = re.sub(r"[\s ]+", " ", s)
    s = re.sub(r"\s*\(\s*", "(", s); s = re.sub(r"\s*\)\s*", ")", s)
    s = s.replace("-", "").replace("'", "").replace('"', "").replace(",", "").replace(".", "").replace(";", "")
    return s.lower().strip()
corpus = {}
for fn in glob.glob(os.path.join(src_dir, "*.txt")) + glob.glob(os.path.join(src_dir, "*.norm.txt")) + glob.glob(os.path.join(lesson_dir, "L0*.txt")):
    try:
        corpus[os.path.basename(fn)] = norm(open(fn, encoding="utf-8", errors="replace").read())
    except OSError:
        pass
allsrc = " || ".join(corpus.values())
bad = []
n = 0
for c in cards:
    for field in ("front", "back"):
        for q in re.findall(r"“([^”]+)”", c[field]):
            n += 1
            qn = norm(q)
            if len(qn) < 12:
                continue
            if qn not in allsrc:
                bad.append((c["id"], field, q[:120]))
print("quoted passages:", n)
for b in bad:
    print("NOT FOUND", b)
print("not found:", len(bad))
