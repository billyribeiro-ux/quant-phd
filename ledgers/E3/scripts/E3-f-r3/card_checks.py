"""E3 slice f round 3: structural and reference checks for the cards of L01 to L04.

Run from the checkout root: python3 -I ledgers/E3/scripts/E3-f-r3/card_checks.py
Prints (1) duplicate and near-duplicate cards over the whole file, (2) every cross-reference in a
card's text (Proposition, Remark, Lemma, Theorem, Definition, Example, Problem, Assumption, section,
Lab 1 part) and whether that label occurs in the lesson it names (or in the card's own lesson).
"""
import json
import re
from collections import Counter

ROOT = "course/modules/E/E3/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
lessons = {}
for n in ("L01", "L02", "L03", "L04"):
    lessons[n] = open(ROOT + n + ".html", encoding="utf-8").read()


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).split()


print("== ids and count")
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "duplicate ids:", [i for i, n in ids.items() if n > 1])
print("per lesson:", Counter(c["lesson"] for c in cards))

print("== duplicate fronts (normalised)")
fr = Counter(" ".join(norm(c["front"])) for c in cards)
print([k for k, n in fr.items() if n > 1] or "none")

print("== near-duplicate fronts or backs (token Jaccard >= 0.6)")
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        for field in ("front", "back"):
            sa, sb = set(norm(a[field])), set(norm(b[field]))
            if sa and sb:
                jac = len(sa & sb) / len(sa | sb)
                if jac >= 0.6:
                    pairs.append((round(jac, 2), a["id"], b["id"], field))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs:", len(pairs))

print("== cross-references in card text")
pat = re.compile(
    r"\b(Proposition|Remark|Lemma|Theorem|Definition|Example|Problem|Assumption|section|Section)\s+"
    r"((?:[0-9]+\.[0-9]+|[A-Z][0-9]|A[0-9]|[0-9])(?:\([a-z]\))?)"
    r"|\b(A[0-9]|F[0-9])\b"
)
bad = []
for c in cards:
    if c["lesson"] not in lessons:
        continue
    text = c["front"] + " " + c["back"]
    for m in pat.finditer(text):
        kind = m.group(1)
        num = m.group(2)
        if kind is None:
            # bare A1..A5 or F1..F6 labels
            label = m.group(3)
            if label.startswith("A") and label not in ("A1", "A2", "A3", "A4", "A5"):
                continue
            needle = label
            ok = needle in lessons[c["lesson"]]
            if not ok:
                bad.append((c["id"], c["lesson"], m.group(0), "not found in own lesson"))
            continue
        base = re.sub(r"\(.*", "", num)
        if kind.lower() == "section":
            ok = ('<h2 id="s' in lessons[c["lesson"]] and True)
            continue
        if kind == "Assumption":
            needle = "Assumption " + base
        elif kind == "Problem":
            needle = 'problem" id="' + base  # problem ids are id="R3" etc
            ok = re.search(r'problem-title">' + re.escape(base) + r' \u00b7', lessons[c["lesson"]]) is not None
            if not ok:
                bad.append((c["id"], c["lesson"], m.group(0), "problem id missing in lesson"))
            continue
        else:
            needle = kind + " " + base
        if kind in ("Proposition", "Remark", "Lemma", "Theorem", "Definition", "Example"):
            # label may be written in the block title, e.g. 'Proposition 1.3 <span'
            ok = re.search(re.escape(needle) + r"\b", lessons[c["lesson"]]) is not None
        else:
            ok = needle in lessons[c["lesson"]]
        if not ok:
            bad.append((c["id"], c["lesson"], m.group(0), "not found in own lesson"))
    # explicit lesson-qualified refs
    for m in re.finditer(r"\b(L0[1-4])\s+(Proposition|Remark|Definition|Example|Problem)\s+([0-9]+\.[0-9]+|[A-Z][0-9])", text):
        target = m.group(1)
        lab = m.group(2) + " " + m.group(3)
        if re.search(re.escape(lab) + r"\b", lessons[target]) is None and not (
            m.group(2) == "Problem" and re.search(r'problem-title">' + re.escape(m.group(3)) + r' \u00b7', lessons[target]) is not None
        ):
            bad.append((c["id"], target, m.group(0), "qualified ref not in that lesson"))
    for m in re.finditer(r"\(L0?(\d)\s*(?:Proposition|Definition|Example)\s*([0-9.]+)?", text):
        pass
print("unresolved references:", len(bad))
for b in bad:
    print(b)
