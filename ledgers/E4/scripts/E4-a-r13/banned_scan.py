"""E4 slice a, round 12: banned phrases (BUILDER_RULES 1.3-1.4) and process words in the four slice pages, outside code.

Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-a-r12/banned_scan.py
Strips <pre>, <code> and HTML tags, then searches the visible text.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly",
]
PROCESS = ["verifier", "builder", "build ", "round ", "REQUESTS", "unit report", "fixer", "ledger"]
hits = 0
for name in PAGES:
    raw = (ROOT / "course/modules/E/E4" / name).read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", " ", raw, flags=re.S)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    for word in BANNED + PROCESS:
        for m in re.finditer(re.escape(word), text, flags=re.I):
            hits += 1
            print(f"HIT {name}: {word!r}: ...{text[max(0, m.start() - 50):m.end() + 40]!r}")
    for m in re.finditer(r"\.\.\.", text):
        hits += 1
        print(f"HIT {name}: ellipsis: ...{text[max(0, m.start() - 40):m.end() + 20]!r}")
print("HITS:", hits)
sys.exit(0)
