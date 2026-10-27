"""Round-34 listing of vague quantity words that qualify a number in S7 L05 and L06 visible text.
Writes one line per occurrence (page:line and context) to stdout; the round-34 run saved it as
/tmp/ap1-r5/L05-L06/r34/vague_contexts.txt. Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/vague_contexts.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
pat = re.compile(r"\b(hundreds?|thousands?|dozens?|handful|a few|few|several|many|roughly|about|around|nearly|almost|million|some)\b", re.I)
for name in ("L05", "L06"):
    lines = (ROOT / "course/modules/S/S7" / f"{name}.html").read_text(encoding="utf-8").splitlines()
    n = 0
    for i, line in enumerate(lines, 1):
        src = re.sub(r"<script.*?</script>|<style.*?</style>", "", line, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", src))
        for m in pat.finditer(t):
            after = t[m.end(): m.end() + 30]
            if re.search(r"\d|\\\(", after) or m.group(0).lower() in ("hundreds", "thousands", "dozens", "handful", "million", "several", "many", "a few", "few"):
                n += 1
                print(f"{name}:{i}: ...{t[max(0, m.start() - 70): m.end() + 45]}...")
    print(f"{name} contexts {n}")
