"""For every file in ledgers/E4/mutants and ledgers/E4/equivalent: the first docstring line and the number of changed
lines against grader/reference.py (code only, docstring excluded), so each description can be compared with its edit.

Run: python3 -I mutant_summary_r9.py <repo-root>
"""
import ast
import difflib
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref_text = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")


def code_lines(text):
    tree = ast.parse(text)
    doc = ast.get_docstring(tree, clean=False) or ""
    body = text.split('"""', 2)[2] if text.startswith('"""') else text
    return body.splitlines(), doc


ref_code, _ = code_lines(ref_text)
for folder in ["mutants", "equivalent", "alternatives"]:
    for path in sorted((root / "ledgers/E4" / folder).glob("*.py")):
        if path.name.startswith("alt_") and folder != "alternatives":
            continue
        text = path.read_text(encoding="utf-8")
        try:
            code, doc = code_lines(text)
        except SyntaxError as err:
            print(f"{folder}/{path.name}: SYNTAX {err}")
            continue
        first = doc.strip().splitlines()[0][:95] if doc.strip() else "(no docstring)"
        changed = sum(1 for l in difflib.ndiff(ref_code, code) if l[:1] in "+-" and not l.startswith(("+ ", "- ")) or (l[:1] in "+-" and l[:2] in ("+ ", "- ") and False))
        changed = len([l for l in difflib.unified_diff(ref_code, code, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))])
        print(f"{folder}/{path.name}: changed-lines={changed} | {first}")
