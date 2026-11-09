"""Profile every E4 mutant against grader/reference.py (round 16 verifier).

For each mutant prints: the first docstring line, the number of differing lines (unified diff, '+'/'-' lines),
whether MAX_BISECTION_STEPS is 240 in the mutant, and the diff lines (compact) so single-change form can be checked.
Usage: python -I mutant_diff_profile_r16.py <checkout-root>
"""
import difflib
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8").splitlines()
mdir = root / "ledgers/E4/mutants"
rows = []
for f in sorted(mdir.glob("*.py")):
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    doc = ""
    m = re.match(r'\s*"""(.*)', text)
    if m:
        doc = m.group(1).strip()
        if not doc:
            doc = lines[1].strip() if len(lines) > 1 else ""
    d = [l for l in difflib.unified_diff(ref, lines, lineterm="", n=0)
         if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    cap = re.search(r"MAX_BISECTION_STEPS = (\d+)", text)
    rows.append((f.name, len(d), cap.group(1) if cap else "-", doc[:110], d))
for name, n, cap, doc, d in rows:
    print(f"{name} | changed_lines={n} | MAX_BISECTION_STEPS={cap} | {doc}")
print("TOTAL mutants:", len(rows))
print("mutants with MAX_BISECTION_STEPS != 240 (if the mutant has the constant):",
      [r[0] for r in rows if r[2] not in ("-", "240")])
print("changed-line histogram:", {k: sum(1 for r in rows if r[1] == k) for k in sorted({r[1] for r in rows})})
