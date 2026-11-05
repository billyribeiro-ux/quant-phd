"""Round-9 verifier (M3 slice d): every card citation (Definition/Lemma/Proposition/Theorem/Corollary/Example/Remark/
Fact/Problem/Assumption/Section, and 'Lab n' outputs) is checked against the block titles of the card's lesson, or of the
lesson named in the citation ('Lesson k, ...'). Also prints every card's citation list for manual reading.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/cards_citations_r9.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path.cwd() / "course/modules/M/M3"
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
LABEL = r"(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Fact|Problem|Assumption|Assumptions|Section|Lesson|Lab) ?(\d+(?:\.\d+)?[a-z]?(?:\(\w\))?)?"
lessons = {}
for n in range(1, 10):
    text = (ROOT / f"L0{n}.html").read_text(encoding="utf-8")
    titles = set()
    for m in re.finditer(r'<span class="block-title[^"]*"[^>]*>(.*?)<span class="name">', text, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        titles.add(t)
    # also headings such as "Definition 1.1" without block-title class
    for m in re.finditer(r"(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Fact|Problem|Assumption)s? (\d+\.\d+[a-z]?)", text):
        titles.add(f"{m.group(1)} {m.group(2)}")
    lessons[f"L0{n}"] = (titles, text)

problems = []
for card in cards:
    lesson = card["lesson"]
    text = " ".join([card["front"], card["back"]])
    cites = []
    for m in re.finditer(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Fact|Problem)s? (\d+\.\d+[a-z]?)(\(\w\))?", text):
        cites.append((m.group(1), m.group(2), m.group(3) or ""))
    named = re.findall(r"Lesson (\d)", text)
    print(card["id"], lesson, "cites:", [f"{a} {b}{c}" for a, b, c in cites], "| lessons named:", named)
    for kind, num, sub in cites:
        target = lesson
        m = re.search(r"Lesson (\d), " + kind + r" ", text)
        if m:
            target = f"L0{m.group(1)}"
        titles, _ = lessons[target]
        label = f"{kind} {num}"
        if label not in titles:
            problems.append((card["id"], lesson, target, label))
print("UNMATCHED citations (card, card lesson, lesson searched, label):")
for p in problems:
    print("  ", p)
print("count", len(problems))
