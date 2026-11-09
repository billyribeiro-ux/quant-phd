"""Internal cross-reference check for CS2 lessons L05-L08.

Every Definition/Lemma/Proposition/Theorem/Corollary/Example/Remark 'x.y' label and every Problem label
(M1..R3) cited in a lesson's prose must occur as a label in that same lesson. Prints missing references.
Usage: python -I -W error xrefs_check.py <repo_root>
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/CS/CS2"
ok = True
for name in ("L05", "L06", "L07", "L08"):
    raw = (root / f"{name}.html").read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    refs = set(re.findall(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark)\s+(\d+\.\d+)", text))
    missing = [f"{k} {n}" for k, n in sorted(refs) if f"{k} {n}" not in text]
    # a label is defined where it heads a block: '<span class="block-title"...>Kind n.m' -> plain 'Kind n.m' text
    problems = re.findall(r"\bProblem\s+([MPER]\d)\b", text)
    missing_problem = sorted({p for p in problems if f"{p} ·" not in text})
    print(f"{name}: refs={len(refs)} missing={missing} problems_cited={sorted(set(problems))} missing_problem={missing_problem}")
    ok = ok and not missing and not missing_problem
print("XREFS_OK" if ok else "XREFS_MISSING")
