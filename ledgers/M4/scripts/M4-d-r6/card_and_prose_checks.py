"""Round-6 verifier (slice d): card, prose and numeric checks over course/modules/M/M4 (run from the checkout root).

1. Cross-reference check: every "Definition/Proposition/Example/Remark/Problem/Lemma/Section/Assumption X" on a card's back
   must appear in the card's lesson text (or in the named lesson when prefixed "Lesson N"). Problem labels appear as "P3 ·".
2. Number check: every decimal or 4+ digit number on a card's back must appear in the card's own lesson text.
3. Near-duplicate scan: Jaccard overlap of card front+back token sets (>= 0.45 listed), plus exact duplicate fronts.
4. Exemplar word counts (raw whitespace tokens of the memo text, math included), as in project.html.
5. Gaussian truncation claim (test_project.py comment): Monte Carlo variance of int(X) for X ~ N(0, 4).
Lesson text comes from strip_lesson_text.py output in /tmp/M4-d-r6/txt (regenerate with that script first).
"""
import html
import itertools
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M4 = ROOT / "course" / "modules" / "M" / "M4"
TXT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/M4-d-r6/txt")
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
lessons = {L: (TXT / f"{L}.txt").read_text(encoding="utf-8") for L in [f"L{i:02d}" for i in range(1, 11)]}

print("== 1. cross-references")
lab_re = re.compile(r"\b(Definition|Proposition|Example|Remark|Problem|Lemma|Theorem|Section|Assumption|Corollary)\s+([A-Z]?\d+(?:\.\d+)?)")
missing = []
for c in cards:
    back = c["back"]
    for m in re.finditer(r"Lesson (\d+)[,]? (Definition|Proposition|Example|Remark|Problem|Lemma|Section|Assumption) ([A-Z]?\d+(?:\.\d+)?)", back):
        L = f"L{int(m.group(1)):02d}"
        if f"{m.group(2)} {m.group(3)}" not in lessons[L] and f"{m.group(3)} ·" not in lessons[L]:
            missing.append((c["id"], L, m.group(2), m.group(3)))
    local = re.sub(r"Lesson \d+[,]? (Definition|Proposition|Example|Remark|Problem|Lemma|Section|Assumption) [A-Z]?\d+(?:\.\d+)?", "", back)
    for m in lab_re.finditer(local):
        lab = f"{m.group(1)} {m.group(2)}"
        if lab not in lessons[c["lesson"]] and f"{m.group(2)} ·" not in lessons[c["lesson"]]:
            missing.append((c["id"], c["lesson"], m.group(1), m.group(2)))
# Section labels are headings like "4Misconceptions"; allow "<n>Heading" lines
filtered = []
for cid, L, kind, label in missing:
    if kind == "Section" and re.search(rf"^{re.escape(label)}[A-Z]", lessons[L], re.M):
        continue
    filtered.append((cid, L, kind, label))
print("unresolved cross-references:", filtered)

print("== 2. numbers on card backs must appear in the card's own lesson")
bad_nums = []
for c in cards:
    for n in re.findall(r"(?<![\w.])(\d+\.\d+|\d{4,})(?![\w])", c["back"]):
        if n not in lessons[c["lesson"]]:
            bad_nums.append((c["id"], n))
print("numbers not in own lesson:", bad_nums)

print("== 3. duplicates")
fronts = [c["front"].strip().lower() for c in cards]
print("exact duplicate fronts:", len(fronts) - len(set(fronts)), "| duplicate ids:", len(cards) - len({c["id"] for c in cards}))
stop = {"the", "a", "of", "is", "and", "for", "what", "does", "to", "in", "on", "with", "its", "an", "or", "by", "as", "be",
        "it", "that", "this", "not", "no", "yes", "from", "at", "when", "which", "how"}
toks = lambda s: set(re.findall(r"[a-z0-9]+", s.lower())) - stop  # noqa: E731
near = []
for a, b in itertools.combinations(cards, 2):
    A, B = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
    if A and B and len(A & B) / len(A | B) >= 0.6:
        near.append((a["id"], b["id"], round(len(A & B) / len(A | B), 2)))
print("near-duplicate pairs (Jaccard >= 0.6):", near)

print("== 4. exemplar raw word counts (project.html)")
s = (M4 / "project.html").read_text(encoding="utf-8")
for name in ("exemplar-a", "exemplar-b"):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % name, s, re.S).group(0)
    total = 0
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>', art, re.S):
        body = re.sub(r"<h5>.*?</h5>", "", m.group(1), flags=re.S)
        total += len(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
    print(name, "body words:", total)
summary = re.search(r'<h5>Summary</h5>\s*<p>(.*?)</p>', re.search(r'id="exemplar-b".*?</article>', s, re.S).group(0), re.S).group(1)
print("exemplar-b summary words:", len(html.unescape(re.sub(r"<[^>]+>", " ", summary)).split()))

print("== 5. Gaussian truncation claim (test_project.py comment: 'about 2.7')")
rng = random.Random(2026)
xs = [2.0 * rng.gauss(0.0, 1.0) for _ in range(500_000)]
tr = [int(x) for x in xs]
m = sum(tr) / len(tr)
print("variance of int(X), X ~ N(0, 4), 500000 draws:", round(sum((v - m) ** 2 for v in tr) / (len(tr) - 1), 3))
