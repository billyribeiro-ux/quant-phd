"""Print the visible text (HTML parser) around each occurrence of a phrase in a lesson. Round 3 helper.

Usage: .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/ctx.py L06 'Definition 1.3' [width] [max_hits]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cards_scan import lesson_text  # noqa: E402

lesson, phrase = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 350
hits = int(sys.argv[4]) if len(sys.argv) > 4 else 3
t = lesson_text(lesson)
start = 0
n = 0
while n < hits:
    i = t.find(phrase, start)
    if i < 0:
        break
    print(f"--- {lesson} @{i}: ...{t[max(0, i - 40):i + width]}...")
    start = i + len(phrase)
    n += 1
if n == 0:
    print("NOT FOUND:", phrase)
