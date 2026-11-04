"""LX2-d round 4: mechanical card-vs-lesson checks (run with python3 -I).

For every card in course/modules/LX/LX2/cards.json:
  - id format, duplicate ids, lesson existence, grade values, registry keys cited;
  - every numeric token in front/back must occur in the plain text of its lesson
    (or, for lab-derived numbers, in the lesson's printed lab output);
  - every quoted fragment (ASCII or curly quotes) must occur in the plain text of its lesson,
    or is reported as NOT-IN-LESSON for manual reading against the statute or opinion.
Usage: python3 -I cards_vs_lessons.py <checkout-root> <text-dir>
<text-dir> holds L01.txt .. L04.txt written by html_to_text.py.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
text_dir = Path(sys.argv[2])
cards = json.loads((root / "course/modules/LX/LX2/cards.json").read_text(encoding="utf-8"))
refs = json.loads((root / "references/references.json").read_text(encoding="utf-8"))
ref_keys = {entry["key"] for entry in refs["entries"]}


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-").replace(" ", " ")
    s = s.replace("\\(", "").replace("\\)", "")
    return " ".join(s.split())


lessons = {}
for name in ("L01", "L02", "L03", "L04"):
    lessons[name] = norm((text_dir / f"{name}.txt").read_text(encoding="utf-8"))

ids = [c["id"] for c in cards]
dups = sorted({i for i in ids if ids.count(i) > 1})
print("cards:", len(cards), "duplicate ids:", dups)
print("grade counts:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "A", "B", "C", "D", "X", None)})
print("cards without grade:", [c["id"] for c in cards if "grade" not in c])
bad_keys = [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in ref_keys]
print("cite keys not in references.json:", bad_keys)
for c in cards:
    if not re.fullmatch(r"LX2-c\d{3}", c["id"]):
        print("BAD ID", c["id"])
    if c["lesson"] not in lessons:
        print("BAD LESSON", c["id"], c["lesson"])

num_re = re.compile(r"(?<![A-Za-z])\d+(?:[./]\d+)*")
for c in cards:
    body = norm(c["front"] + " " + c["back"])
    text = lessons[c["lesson"]]
    for tok in sorted(set(num_re.findall(body))):
        if tok not in text:
            print(f"NUM-NOT-IN-LESSON {c['id']} [{c['lesson']}] token={tok!r}")
    for q in re.findall(r"\"([^\"]{6,})\"|“([^”]{6,})”|‘([^’]{6,})’", c["front"] + " " + c["back"]):
        frag = norm(next(x for x in q if x))
        if frag and frag not in text:
            print(f"QUOTE-NOT-IN-LESSON {c['id']} [{c['lesson']}] {frag!r}")
