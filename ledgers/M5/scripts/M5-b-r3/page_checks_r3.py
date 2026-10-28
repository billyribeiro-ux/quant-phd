"""Round-3 checks for M5-b: tag-name scan, expected-block diff against live lab output, and the duplicated-word grep.

Run from the checkout root with: .venv/bin/python -I ledgers/M5/scripts/M5-b-r3/page_checks_r3.py
"""

import html
import re
import subprocess
import sys
from collections import Counter

ROOT = "."
KNOWN = {
    "a", "body", "button", "code", "details", "dfn", "div", "em", "fieldset", "footer", "h1", "h2", "h3", "head",
    "header", "html", "input", "label", "legend", "li", "link", "main", "meta", "nav", "ol", "p", "pre", "script",
    "section", "span", "strong", "summary", "table", "tbody", "td", "th", "thead", "title", "tr", "ul",
}
LESSONS = {"L05": "lab-M5-L05-1.py", "L06": "lab-M5-L06-1.py", "L07": "lab-M5-L07-1.py"}

for lesson, lab in LESSONS.items():
    page = open(f"{ROOT}/course/modules/M/M5/{lesson.lower()}.html", encoding="utf-8").read()
    tags = Counter(m.group(1).lower() for m in re.finditer(r"<([a-zA-Z][a-zA-Z0-9]*)", page))
    unknown = sorted(t for t in tags if t not in KNOWN)
    print(lesson, "unknown tag names:", unknown)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    expected_lines = [html.unescape(x) for x in expected.split("\n")]
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/M5/{lab}"],
        capture_output=True, text=True, check=False,
    )
    out_lines = run.stdout.rstrip("\n").split("\n")
    print(lesson, "lab rc", run.returncode, "output lines", len(out_lines), "expected lines", len(expected_lines))
    print(lesson, "output == expected block:", out_lines == expected_lines)
    print(lesson, "duplicated word 'is is' (word match):", len(re.findall(r"\bis is\b", page)))
