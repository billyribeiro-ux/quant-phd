"""Prose, exemplar, prize-range and lab-output checks for E3 project.html (E3-e round 1). Run: python -I check_prose.py <page>."""
import html
import re
import sys

PAGE = sys.argv[1]
src = open(PAGE, encoding="utf-8").read()

# 1. visible prose: drop scripts, code, pre and math; scan banned and process words
s = re.sub(r"<script.*?</script>", "", src, flags=re.S)
s = re.sub(r"<(code|pre)\b.*?</\1>", "", s, flags=re.S)
s = re.sub(r"\\\((.*?)\\\)", "", s, flags=re.S)
s = re.sub(r"\\\[(.*?)\\\]", "", s, flags=re.S)
s = html.unescape(re.sub(r"<[^>]+>", " ", s)).lower()
terms = ["todo", "tbd", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
         "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
         "obviously", "clearly", "...", "…", "build", "builder", "verifier", "requests", "unit report",
         "agent", "ledger", "fragment", "plan"]
hits = [(t, s[max(0, m.start() - 40): m.end() + 30]) for t in terms for m in re.finditer(re.escape(t), s)]
print("banned/process hits in visible prose:", len(hits))
for h in hits:
    print("  ", h)
# 'round' as a standalone process word (not 'rounded', 'rounding', 'unrounded')
print("standalone 'round' hits:", len(re.findall(r"\bround\b", s)))

# 2. exemplar memo word counts (headings included; a word is a run of non-space characters)
for ex in ("exemplar-a", "exemplar-b"):
    art = src.split(f'<article class="exemplar" id="{ex}"')[1].split("</article>")[0]
    total = 0
    for memo in re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", memo))).strip()
        total += len(t.split())
    print(ex, "memo words", total)

# 3. prize range and mixed-pair count from the Lab 3 answers
block = src.split("ANSWERS: list")[1].split("]\n\n\ndef value")[0]
rows = re.findall(r"\((\d+), \"([AB])\", (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\])\)", block)
from fractions import Fraction  # noqa: E402

prizes, mixed, lens = [], 0, set()
for r in rows:
    pa, qa, pb, qb = eval(r[2]), eval(r[3]), eval(r[4]), eval(r[5])  # trusted local page text
    prizes += pa + pb
    lens |= {len(pa), len(pb)}

    def is_mixed(pr, pq):
        qs = [Fraction(q) for q in pq]
        return any(x > 0 and q > 0 for x, q in zip(pr, qs)) and any(x < 0 and q > 0 for x, q in zip(pr, qs))

    mixed += int(is_mixed(pa, qa) or is_mixed(pb, qb))
    for pr, pq in ((pa, qa), (pb, qb)):
        assert sum(Fraction(q) for q in pq) == 1
print("answers", len(rows), "prize min", min(prizes), "prize max", max(prizes), "prize-list lengths", sorted(lens),
      "mixed pairs", mixed)
