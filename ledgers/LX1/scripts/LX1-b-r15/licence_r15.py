"""LX1-b round 15: plain-curl fetch of the Federal Reserve licence and H.10 about pages, and quote extraction.

Run: sh-free; python3 -I ledgers/LX1/scripts/LX1-b-r15/licence_r15.py  (uses curl for the fetch, writes to /tmp only)
"""

import html
import re
import subprocess
from pathlib import Path

DEST = Path("/tmp/lx1b-r15-web")
DEST.mkdir(parents=True, exist_ok=True)
URLS = [
    "https://www.federalreserve.gov/disclaimer.htm",
    "https://www.federalreserve.gov/releases/h10/about.htm",
]
for url in URLS:
    name = url.split("federalreserve.gov/")[1].replace("/", "_")
    code = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", "30", "-o", str(DEST / name), "-w", "%{http_code}", url],
        capture_output=True, text=True, check=True,
    ).stdout
    print("HTTP", code, url)
    text = (DEST / name).read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text)))
    for pat in ("may be copied and distributed without permission", "Please cite to the Board as the source",
                "monthly averages of bilateral exchange rates", "noon buying rates in New York for cable transfers",
                "Last Update"):
        m = re.search(re.escape(pat), text)
        print(" quote" if m else " MISSING", "|", pat, "|", text[max(0, m.start() - 60): m.end() + 90] if m else "")
