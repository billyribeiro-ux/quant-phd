"""Round-14 check: each page's pre.expected block equals its twin's stdout, exactly (SC1 slice b)."""

from __future__ import annotations

import difflib
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/SC1/scripts/SC1-b-r14/out"
for lesson in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/SC/SC1/{lesson}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S)
    twin = (OUT / f"twin_{lesson}.stdout").read_text(encoding="utf-8")
    print(f"{lesson}: expected blocks {len(blocks)}")
    for block in blocks:
        text = html.unescape(re.sub(r"<[^>]+>", "", block))
        same = text.strip("\n") == twin.strip("\n")
        print(f"  exact match with twin stdout: {same} ({len(text.strip().splitlines())} lines)")
        if not same:
            print("\n".join(difflib.unified_diff(text.strip("\n").splitlines(), twin.strip("\n").splitlines(), lineterm="")))
