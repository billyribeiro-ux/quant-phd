"""Mechanical card checks: numbers in cards must appear in the card's lesson text; labels cited must exist."""
import json
import re
import sys
from pathlib import Path

TEXT = Path(sys.argv[1])
cards = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
lesson_text: dict[str, str] = {}
for p in sorted(TEXT.glob("L*.txt")):
    lesson_text[p.stem] = p.read_text(encoding="utf-8")


def norm(s: str) -> str:
    s = s.replace("\\(", "").replace("\\)", "").replace("\\[", "").replace("\\]", "")
    s = re.sub(r"\s+", " ", s)
    return s


def lesson_of(ref: str) -> str:
    n = int(ref)
    return f"L{n:02d}"


NUM = re.compile(r"(?<![A-Za-z_\w.])(\d+(?:\.\d+)?(?:e-?\d+)?)(?![\w])")
LABEL = re.compile(r"\b(Theorem|Proposition|Assumption|Example|Definition|Corollary|Remark|Lemma|Problem|Misconception|Lesson|Lesson L|Section|§)\s?(\d+(?:\.\d+)?)")
problems = []
for c in cards:
    cid, lesson = c["id"], c["lesson"]
    text = norm(c["front"] + " " + c["back"] + " " + (c.get("basis") or ""))
    body = lesson_text.get(lesson, "")
    if not body:
        problems.append((cid, "NO LESSON TEXT " + lesson))
        continue
    # labels
    for m in LABEL.finditer(text):
        kind, num = m.group(1), m.group(2)
        if kind in ("Lesson", "Lesson L"):
            target = lesson_of(num)
            if target not in lesson_text:
                problems.append((cid, f"lesson ref {num} missing"))
            continue
        if kind == "Section" or kind == "§":
            continue
        if kind == "Problem":
            continue
        pat = f"{kind} {num}"
        ok = pat in body
        if not ok:
            # referenced to another lesson? look in named lesson
            prev = text[max(0, m.start() - 60):m.start()]
            lm = re.search(r"Lesson (?:L)?(\d+)", text[m.end():m.end() + 60]) or re.search(r"Lesson (?:L)?(\d+)", prev)
            if lm:
                other = lesson_of(lm.group(1))
                if pat in lesson_text.get(other, ""):
                    continue
            problems.append((cid, f"label '{pat}' not in {lesson}"))
    # numbers: normalise and look up in lesson body
    nb = norm(body)
    for m in NUM.finditer(text):
        tok = m.group(1)
        if tok in nb:
            continue
        problems.append((cid, f"number '{tok}' not found in {lesson} text"))

print(f"cards={len(cards)} flagged={len(problems)}")
for p in problems:
    print(p)
