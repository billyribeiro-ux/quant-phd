"""Scan the visible text of lesson HTML pages (argv: page.html ...) for banned phrases, process words and scope words.

Tags are removed with the same rule as strip_view.py (only '<' that opens a real tag). Prints file:line hits."""
import html
import re
import sys

PATTERNS = [r"TODO", r"TBD", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
            r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
            r"obviously", r"clearly", r"roughly", r"historically", r"in practice", r"typically", r"\bmost\b", r"\bsmall\b",
            r"\bfast\b", r"smooth", r"verifier", r"builder", r"ledger", r"fragment", r"orchestrat", r"round \d", r"haiku",
            r"\brung\b", r"\.\.\.", r"…", r"\bonly\b", r"\bevery\b", r"\ball\b", r"\balways\b", r"\bany\b",
            r"\bexactly\b", r"\bdrives\b", r"\bsame\b", r"\bnever\b"]
tag = re.compile(r"<(?=/?[A-Za-z!])[^>]*>")
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as fh:
        for no, raw in enumerate(fh, 1):
            line = html.unescape(tag.sub("", raw)).strip()
            for pat in PATTERNS:
                for m in re.finditer(pat, line, re.I):
                    s = max(0, m.start() - 50)
                    print(f"{path.split('/')[-1]}:{no}: [{pat}] ...{line[s:m.end() + 50]}...")
