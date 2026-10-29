"""Verifier script (M2 slice c, round 2): banned-phrase, process-word and scope-word scan of L13-L18 visible text.

Run as: <checkout>/.venv/bin/python -I ledgers/M2/scripts/M2-c-r2/banned_scan_r2.py <checkout>
Prints every hit with its sentence so each can be read in context; the banned list is BUILDER_RULES 1.2/1.3 plus the process words.
"""

import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
BANNED = [r"\.\.\.", r"…", r"roughly", r"about \d+ ?%", r"historically", r"studies show", r"well[- ]known",
          r"it is clear", r"obviously", r"clearly", r"builder", r"verifier", r"REQUEST", r"\bround\b",
          r"unit report", r"TODO", r"TBD", r"lorem"]
SCOPE = r"\b(always|drives|same|raises|offsets|never|all|only|every|any)\b"
for n in range(13, 19):
    src = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf8")
    body = re.sub(r"<pre.*?</pre>", "", src, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", body))
    hits = 0
    for pat in BANNED:
        for m in re.finditer(pat, txt, flags=re.I):
            hits += 1
            print(f"L{n} BANNED {pat}: {' '.join(txt[max(0, m.start() - 60):m.end() + 40].split())}")
    scope = len(re.findall(SCOPE, txt, flags=re.I))
    print(f"L{n}: banned/process hits {hits}; scope-word occurrences {scope}")
