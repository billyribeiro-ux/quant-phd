"""Round 2 mechanical checks on course/modules/LX/LX2/cards.json against the four lessons (and, for quotes, the sources).

Usage: python3 -I cards_checks_r2.py <checkout_root> <source_dir>
Checks: schema and ids; lesson-range; grade/cite/basis; exact and near duplicates; every digit token of a card
appears in its lesson; every curly-quoted span appears in the lesson or in a fetched source text.
"""
import difflib
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
src_dir = Path(sys.argv[2])
cards = json.loads((root / "course/modules/LX/LX2/cards.json").read_text(encoding="utf-8"))

ALLOWED_GRADES = {"T", "A", "B", "C", "D", "X"}


def norm(s: str) -> str:
    s = html.unescape(s)
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                                   "–": "-", "—": "-", " ": " ", "−": "-"}))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s)


lessons = {}
for L in ("L01", "L02", "L03", "L04"):
    lessons[L] = norm((root / f"course/modules/LX/LX2/{L}.html").read_text(encoding="utf-8"))
sources = {}
for p in src_dir.glob("*.txt"):
    sources[p.name] = norm(p.read_text(encoding="utf-8", errors="replace"))
for p in src_dir.glob("*.html.txt"):
    sources[p.name] = norm(p.read_text(encoding="utf-8", errors="replace"))
all_sources = " ".join(sources.values())

problems = []
ids = [c["id"] for c in cards]
assert len(ids) == len(set(ids)), "duplicate ids"
expected = [f"LX2-c{n:03d}" for n in range(1, len(cards) + 1)]
if ids != expected:
    problems.append(f"ids not contiguous c001..c{len(cards):03d}")
print("cards:", len(cards))
range_of = lambda n: "L01" if n <= 27 else "L02" if n <= 43 else "L03" if n <= 63 else "L04"
for c in cards:
    n = int(c["id"][-3:])
    if c["lesson"] != range_of(n):
        problems.append(f"{c['id']}: lesson {c['lesson']} outside range {range_of(n)}")
    if "grade" in c and c["grade"] not in ALLOWED_GRADES:
        problems.append(f"{c['id']}: grade {c['grade']!r} not in T/A/B/C/D/X")
    if "grade" in c and not (c.get("cite") or c.get("basis")):
        problems.append(f"{c['id']}: graded card has neither cite nor basis")
    for key in ("front", "back"):
        if not c.get(key, "").strip():
            problems.append(f"{c['id']}: empty {key}")
print("schema problems:", problems if problems else "none")

print("--- duplicates (exact fronts or backs)")
seen_f, seen_b = {}, {}
for c in cards:
    seen_f.setdefault(c["front"], []).append(c["id"])
    seen_b.setdefault(c["back"], []).append(c["id"])
dups = [v for v in list(seen_f.values()) + list(seen_b.values()) if len(v) > 1]
print("exact duplicate groups:", dups if dups else "none")
print("--- near duplicates (back similarity >= 0.85 or front >= 0.85)")
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        if rb >= 0.85 or rf >= 0.85:
            near.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("near-duplicate pairs:", near if near else "none")

print("--- digit tokens absent from the card's lesson")
miss_num = []
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson = lessons[c["lesson"]]
    for tok in sorted(set(re.findall(r"(?<![A-Za-z_])\d+(?:[.,]\d+)?", text))):
        if not re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", lesson):
            miss_num.append((c["id"], tok))
print("digit tokens not in lesson:", miss_num if miss_num else "none")

print("--- curly-quoted spans absent from the lesson and from fetched sources")
miss_q = []
for c in cards:
    for span in re.findall(r"“([^”]+)”", c["front"] + " " + c["back"]):
        s = norm(span).strip(" .,;:")
        in_lesson = s in lessons[c["lesson"]] or s in " ".join(lessons.values())
        in_src = s in all_sources
        if not (in_lesson or in_src):
            miss_q.append((c["id"], s[:80], "lesson" if in_lesson else "-", "source" if in_src else "-"))
for c in cards:
    for span in re.findall(r"'([^']{12,})'", c["front"] + " " + c["back"]):
        s = norm(span).strip(" .,;:")
        if not (s in " ".join(lessons.values()) or s in all_sources):
            miss_q.append((c["id"], "single-quoted: " + s[:70], "-", "-"))
print("quoted spans not found:", miss_q if miss_q else "none")
print("problems total:", len(problems))
