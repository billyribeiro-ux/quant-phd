"""Convert the fetched HTML source pages to plain text (tags stripped, entities decoded) for quote checks.

Reads /tmp/lx2b-src/*.htm written by fetch_sources.sh and writes the matching .txt files beside them.
"""

import html
import re
from pathlib import Path

SRC = Path("/tmp/lx2b-src")
for name in ["sr2602", "cfa", "standards-of-practice-iii-a", "standards-of-practice-vi-a", "standards-of-practice-vi-b"]:
    raw = (SRC / f"{name}.htm").read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"[ \t\r\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    (SRC / f"{name}.txt").write_text(text, encoding="utf-8")
    print(name, len(text))
