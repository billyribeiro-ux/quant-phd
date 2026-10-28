import html, json, re, sys
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/M/M3"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
texts = {}
for p in sorted(root.glob("L0*.html")):
    t = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8"))))
    texts[p.stem] = t
# statement heads: "Theorem 2.2 (name)" etc; capture 160 chars after each label occurrence in each lesson
lab = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Fact)\s+(\d+\.\d+)\b")
heads = {}
for name, t in texts.items():
    for m in lab.finditer(t):
        heads.setdefault((name, f"{m.group(1)} {m.group(2)}"), t[m.end(): m.end() + 120])
ref = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Fact)\s+(\d+\.\d+)")
out = []
for c in cards:
    blob = c["front"] + " " + c["back"]
    lesson = c["lesson"]
    for m in dict.fromkeys(f"{x.group(1)} {x.group(2)}" for x in ref.finditer(blob)):
        h = heads.get((lesson, m))
        if h is None:
            # also check other lessons in case the card cites a numbered item from another lesson without naming it
            cands = [k[0] for k in heads if k[1] == m]
            out.append((c["id"], lesson, m, "NOT IN OWN LESSON", cands))
            continue
        hyp = h.lstrip().startswith("(") and False
        assumed = bool(re.search(r"^[^.]{0,120}?(Assuming|Under F|assuming F|Assumptions? F)", h)) or bool(re.search(r"^[^.]{0,200}", h) and re.search(r"Assuming F|under F|Under F|Assumptions F", h[:200]))
        carries = bool(re.search(r"F1|F2|F3|F4|[Aa]ssum|[Uu]nder F|Under F|under F", blob))
        out.append((c["id"], lesson, m, "ASSUMED" if assumed else "plain", "card-carries" if carries else "card-silent", h[:90]))
for o in out:
    print(*o, sep=" | ")
