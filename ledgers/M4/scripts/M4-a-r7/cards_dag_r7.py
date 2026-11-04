"""Card full scan (ids, fronts, backs, grades, lesson counts), card numbers present in their lesson,
and DAG/notation greps over slice a pages. Usage: python3 -I cards_dag_r7.py <checkout>"""
import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
print("cards total", len(cards))
print("dup ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()  # noqa: E731
print("dup fronts", [k for k, v in collections.Counter(norm(c["front"]) for c in cards).items() if v > 1])
print("dup backs", [k[:50] for k, v in collections.Counter(norm(c["back"]) for c in cards).items() if v > 1])
print("grades", collections.Counter(c["grade"] for c in cards))
print("missing fields", [c["id"] for c in cards if not all(c.get(k) for k in ("id", "lesson", "front", "back", "grade"))])
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
text = {}
for f in ["index", "L01", "L02", "L03", "L04"]:
    raw = (root / f"course/modules/M/M4/{f}.html").read_text(encoding="utf-8")
    text[f] = re.sub(r"<[^>]+>", " ", raw)
for c in [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]:
    nums = re.findall(r"\b\d+(?:\.\d+)?/\d+\b|\b\d+\.\d+\b|\b\d{3,}\b", c["back"])
    lesson_txt = text[c["lesson"]]
    missing = [n for n in nums if n not in lesson_txt]
    if missing:
        print("card number not in lesson", c["id"], missing)
print("card numbers check done (slice cards)")
for f in ["L01", "L02", "L03", "L04", "index"]:
    for pat in ["standard normal", "Student-t", "Lesson [5-9]", "Lesson 10", "phi|varphi|\\\\phi"]:
        hits = [i + 1 for i, l in enumerate((root / f"course/modules/M/M4/{f}.html").read_text(encoding="utf-8").split("\n"))
                if re.search(pat, re.sub(r"<[^>]+>", " ", l))]
        if hits:
            print(f"{f} /{pat}/ lines {hits[:20]}")
