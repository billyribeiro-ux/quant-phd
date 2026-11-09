# Round-1: every labelled cross-reference (Theorem/Lemma/Proposition/Corollary/Remark/Example/Definition/Assumption/Problem/Misconception)
# in the changed and added slice cards must name a label that exists in the page it cites (own lesson, or 'of Lesson N').
import json, re, html
S = "ledgers/M2/scripts/M2-b-r1/"
cards = json.load(open(S + "cards_head_95f3f8cb.json", encoding="utf-8"))
ids = ["M2-c087", "M2-c161", "M2-c169", "M2-c176", "M2-c417", "M2-c421", "M2-c422", "M2-c423", "M2-c425", "M2-c428", "M2-c429"]
def page(n):
    return html.unescape(re.sub(r"<[^>]+>", " ", open(f"course/modules/M/M2/L{n:02d}.html", encoding="utf-8").read()))
pages = {n: page(n) for n in range(1, 25) if __import__("os").path.exists(f"course/modules/M/M2/L{n:02d}.html")}
LAB = r"(Theorem|Lemma|Proposition|Corollary|Remark|Example|Definition|Assumption|Problem|Misconception|Section|Lab 1, part|part) ([0-9]+\.[0-9]+|[A-Z][0-9]|[0-9]+|[A-D])"
for c in cards:
    if c["id"] not in ids:
        continue
    own = int(c["lesson"][1:])
    text = c["front"] + " " + c["back"]
    for m in re.finditer(LAB + r"( of Lesson (\d+))?", text):
        kind, num, _, other = m.group(1), m.group(2), m.group(3), m.group(4)
        tgt = int(other) if other else own
        label = f"{kind} {num}"
        pg = pages.get(tgt, "")
        ok = label in pg or (kind in ("Section",) and f"Section {num}" in pg) or (kind.startswith("Lab") and f"Lab 1" in pg)
        if kind == "Section":
            ok = bool(re.search(r"\b%s\b" % re.escape(num), pg))
        print(c["id"], repr(m.group(0)), "-> L%02d" % tgt, "FOUND" if ok else "MISSING")
