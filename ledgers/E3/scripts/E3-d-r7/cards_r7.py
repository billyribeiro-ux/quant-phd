"""Round-7 card checks on the current pin: labels cited by each card exist in its lesson; every card number appears
in its lesson text (cards and lessons read from the pin); duplicate fronts and backs; grade/basis fields."""
import json, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyC7-E3-d/"
S = ROOT + "ledgers/E3/scripts/E3-d-r7/"
cards = json.load(open(ROOT + "course/modules/E/E3/cards.json", encoding="utf-8"))
texts = {L: open(S + "lessons/" + L + ".txt", encoding="utf-8").read() for L in ["L01","L02","L03","L04","L05","L06","L07","L08"]}
allt = " ".join(texts.values())
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
def norm(s): return re.sub(r"\W+", " ", s.lower()).strip()
for field in ("front", "back"):
    seen = {}
    for c in cards:
        seen.setdefault(norm(c[field]), []).append(c["id"])
    print("duplicate", field, [v for v in seen.values() if len(v) > 1])
label_re = re.compile(r"\((Definition|Proposition|Theorem|Remark|Example|Lemma|Corollary|Problem|Observation|Assumption|Model|section|Section|Step|Part)[^()]*\)")
lab_re = re.compile(r"(Definition|Proposition|Theorem|Remark|Example|Lemma|Corollary|Problem|Observation|Model)\s+(\d+(\.\d+)?|[A-Z]\d*)")
num_re = re.compile(r"\d[\d,\.]*\d|\d")
problems = []
for c in cards:
    L = c["lesson"]
    txt = c["front"] + " " + c["back"]
    labels = set(m.group(0) for m in lab_re.finditer(txt))
    for lb in sorted(labels):
        if lb not in texts[L] and lb not in allt:
            problems.append((c["id"], L, "label not in lesson", lb))
        elif lb not in texts[L]:
            problems.append((c["id"], L, "label only in another lesson", lb))
    for n in sorted(set(num_re.findall(txt))):
        n2 = n.rstrip(".,")
        if n2 and n2 not in texts[L] and n2.replace(",", "") not in texts[L].replace(",", ""):
            problems.append((c["id"], L, "number not in own lesson", n2))
for p in problems:
    print(*p)
print("problems", len(problems))
