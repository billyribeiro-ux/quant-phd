# Round-1 delta (M3 slice d): every numbered reference on a card (Definition/Example/Proposition/Theorem/Remark/
# Corollary/Lemma/Fact N.M) must appear as a heading of the lesson the card names, or of the lesson named in
# "Lesson N" just before it. Reads plain-text lesson extracts written to /private/tmp/verifyD1-txt/.
import json, re, sys
cards = json.load(open(sys.argv[1]))
txt = {}
for n in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"]:
    txt[n] = open("/private/tmp/verifyD1-txt/%s.txt" % n, encoding="utf-8").read()
ref = re.compile(r"(Definition|Example|Proposition|Theorem|Remark|Corollary|Lemma|Fact|Assumption|Problem|Misconception) (\d+\.\d+)")
lessref = re.compile(r"Lesson (\d)")
bad = []
for c in cards:
    lesson = c["lesson"]
    text = " ".join([c["front"], c["back"]])
    for m in ref.finditer(text):
        kind, num = m.group(1), m.group(2)
        # find a preceding "Lesson N" within 40 chars before the match
        pre = text[max(0, m.start() - 40): m.start()]
        lm = lessref.findall(pre)
        target = "L0" + lm[-1] if lm else lesson
        if target not in txt:
            continue
        pat = re.compile(r"%s %s[ \(\.:]" % (kind, re.escape(num)))
        if not pat.search(txt[target]):
            bad.append((c["id"], lesson, "%s %s" % (kind, num), target))
print("card reference checks:", len(bad), "unresolved")
for b in bad:
    print(*b)
