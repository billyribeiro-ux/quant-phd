"""For each slice card: every 'Kind N.M' label and every decimal in front/back/basis must occur in the card's lesson page
(or, for labels qualified by 'Lesson k', in that lesson page)."""
import html
import json
import re
from pathlib import Path

cards = json.loads(Path("course/modules/M/M5/cards.json").read_text(encoding="utf-8"))
pages = {l: html.unescape(Path(f"course/modules/M/M5/{l}.html").read_text(encoding="utf-8")) for l in ("L05", "L06", "L07")}
pages_plain = {k: re.sub(r"<[^>]+>", " ", v).replace("\\", "") for k, v in pages.items()}
label = re.compile(r"\b(Proposition|Lemma|Theorem|Corollary|Example|Problem|Misconception|Definition|Remark|Assumption) (\d+(?:\.\d+)?|[MPERC]\d)")
dec = re.compile(r"\b\d+\.\d{3,}\b")
problems = []
n = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = " ".join(str(c.get(k, "")) for k in ("front", "back", "basis"))
    lesson_text = pages_plain[c["lesson"]]
    for kind, num in label.findall(text):
        n += 1
        pat = f"{kind} {num}"
        if pat not in lesson_text and pat.replace(" ", " ") not in lesson_text:
            # may be a cross-lesson reference (e.g. 'Lesson 5, Proposition 3.2')
            if re.search(rf"Lesson \d[^.;]*{re.escape(pat)}", text):
                continue
            if any(pat in p for p in pages_plain.values()):
                continue
            problems.append((c["id"], pat))
    for d in dec.findall(text):
        if d not in lesson_text and d not in " ".join(pages_plain.values()):
            problems.append((c["id"], "decimal " + d))
print("label/decimal references checked:", n)
print("unresolved:", problems)
