"""E2 slice b verifier script: scan the visible text of L04-L06 and their twins for banned phrases, scope words,
process words and undefined-looking terms. Prints every hit with its page and a 90-character context.

Usage: <checkout>/.venv/bin/python -I <checkout>/ledgers/E2/scripts/E2-b-r1/scope_scan_slice_b.py <checkout>
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pats = [
    r"TODO", r"TBD", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
    r"left as an exercise", r"you can add", r"important to note", r"studies show", r"experts agree",
    r"well known", r"obviously", r"clearly", r"roughly", r"\babout\b", r"approximately", r"historically",
    r"widely", r"can be shown", r"\bbuild", r"verifier", r"\bround\b", r"REQUEST", r"unit report",
    r"\bdrives?\b", r"offsets", r"\braises?\b", r"as much as", r"\balways\b", r"\bevery\b", r"\bonly\b",
    r"\ball\b", r"\bany\b", r"\bsame\b", r"\bnever\b", r"\bfirst\b", r"\befficien", r"\brent\b",
    r"off-path", r"\bthreshold\b", r"\bseparating\b", r"\bcanon\b", r"\bresult\b", r"\bbids?\b",
]
rx = re.compile("|".join(f"(?:{p})" for p in pats), re.I)
for name in ("L04", "L05", "L06"):
    text = (root / "course/modules/E/E2" / f"{name}.html").read_text(encoding="utf-8")
    text = re.sub(r"<pre class=\"expected\".*?</pre>", "", text, flags=re.S)
    text = re.sub(r"<pre><code.*?</code></pre>", "", text, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text)
    for m in rx.finditer(text):
        a, b = max(0, m.start() - 45), min(len(text), m.end() + 45)
        print(f"{name}: [{m.group(0)}] ...{text[a:b]}...")
