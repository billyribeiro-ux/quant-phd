"""Round-15 banned-phrase and process-word scan of the E4 slice-d files (BUILDER_RULES 1.3-1.4, fixer rules).

Usage: python -I banned_scan_r15.py  (prints each hit with file:line; no hit means the phrase is absent)
"""
import re
from pathlib import Path

FILES = [
    Path("course/modules/E/E4/project.html"),
    *sorted(Path("course/modules/E/E4/grader").glob("*.py")),
    *sorted(Path("tests/labs/E4").glob("lab-E4-project-*.py")),
]
PATTERNS = {
    "placeholder": r"\bTODO\b|\bTBD\b|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more",
    "ellipsis_omitted": r"\.\.\.(?!\s*\))",
    "filler": r"it is important to note|studies show|experts agree|it is well known|\bobviously\b|\bclearly\b|can be shown that",
    "process_words": r"\bbuilder\b|\bverifier\b|\bREQUESTS\b|unit report|\bfixer\b|\bround \d+\b|\bbuild\b(?! a )",
    "approx_numbers": r"about 6%|roughly half|\bhistorically\b",
}
total = 0
for f in FILES:
    for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
        for name, pat in PATTERNS.items():
            for m in re.finditer(pat, line, flags=re.I):
                total += 1
                print(f"{f}:{i}: [{name}] {m.group(0)!r}: {line.strip()[:120]}")
print("files", len(FILES), "hits", total)
