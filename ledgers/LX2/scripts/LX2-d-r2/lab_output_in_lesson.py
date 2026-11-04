"""For each line printed by a lab twin, report whether that exact line (whitespace-normalised) appears in the lesson text.

Usage: python3 -I lab_output_in_lesson.py <twin_output.txt> <lesson.html>
Prints MISSING for each twin line that does not occur in the lesson's tag-stripped text.
"""
import html
import re
import sys

out_path, lesson_path = sys.argv[1], sys.argv[2]
with open(lesson_path, encoding="utf-8") as fh:
    raw = fh.read()
text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
text = re.sub(r"\s+", " ", text)
with open(out_path, encoding="utf-8") as fh:
    lines = [ln.rstrip("\n") for ln in fh if ln.strip()]
missing = 0
for ln in lines:
    norm = re.sub(r"\s+", " ", ln).strip()
    ok = norm in text
    if not ok:
        missing += 1
    print(("OK      " if ok else "MISSING ") + norm[:150])
print(f"lines={len(lines)} missing={missing}")
