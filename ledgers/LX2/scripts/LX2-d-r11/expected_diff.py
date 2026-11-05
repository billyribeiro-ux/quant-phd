"""Compare each LX2 lesson's expected block with its twin's output (run: python3 -I expected_diff.py <checkout>).

The twin output files are written to out/ by the run: python -I -W error tests/labs/LX2/lab-LX2-L0n-1.py > out/twin_lab-LX2-L0n-1.txt.
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "ledgers/LX2/scripts/LX2-d-r11/out"
for lesson in ("L01", "L02", "L03", "L04"):
    page = (root / f"course/modules/LX/LX2/{lesson}.html").read_text(encoding="utf-8")
    block = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S).group(1))
    got = (out / f"twin_lab-LX2-{lesson}-1.txt").read_text(encoding="utf-8")
    print(lesson, "expected block == twin output:", block.strip() == got.strip(), "| lines:", len(block.strip().splitlines()))
