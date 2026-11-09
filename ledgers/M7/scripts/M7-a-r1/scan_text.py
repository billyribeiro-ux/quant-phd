"""Verifier M7 slice a round 1: banned-string scan of the hub, the L01-L03 pages and the twins.

Scans the raw text (tags stripped for the prose pass) for the BUILDER_RULES 1.3 placeholder strings, the 1.4 filler
phrases, the rule 2 vague quantities and the process words that must not appear in learner text. Prints every hit
with its line number; zero hits per file is the expected output.
"""
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M7-a")
M7 = ROOT / "course/modules/M/M7"
files = [M7 / "index.html", M7 / "L01.html", M7 / "L02.html", M7 / "L03.html",
         ROOT / "tests/labs/M7/lab-M7-L01-1.py", ROOT / "tests/labs/M7/lab-M7-L02-1.py", ROOT / "tests/labs/M7/lab-M7-L03-1.py"]
patterns = [
    r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
    r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
    r"\bobviously\b", r"\bclearly\b", r"it can be shown", r"\babout \d+ ?%", r"roughly half", r"historically",
    r"\.\.\.", r"…", r"\bwe (?:now )?(?:draft|revise|rewrite|fix|edit)\b", r"\bthe (?:builder|verifier|fixer|architect)\b",
    r"\bround \d\b", r"\bfixed\b", r"\bround-trip\b", r"\bagent\b", r"\bwe changed\b",
]
rx = re.compile("|".join(f"(?:{p})" for p in patterns), re.I)
total = 0
for f in files:
    hits = []
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        for m in rx.finditer(line):
            hits.append((i, m.group(0), line[max(0, m.start() - 50): m.end() + 50]))
    total += len(hits)
    print(f"{f.relative_to(ROOT)}: {len(hits)} hits")
    for h in hits[:20]:
        print("   ", h[0], repr(h[1]), "|", h[2][:160])
print("total hits", total)
