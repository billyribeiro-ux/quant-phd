"""GovInfo record pages (plain curl, scratch/src/COMPS-188x_details.html): Title and Amended Through checks (run: python3 -I govinfo_check.py <src>)."""

import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
CHECKS = (
    ("COMPS-1884_details.html", "To provide full and fair disclosure of the character of securities", "119-27", "July 18, 2025"),
    ("COMPS-1885_details.html", "To provide for the regulation of securities exchanges and of over-the-counter markets", "119-60", "December 18, 2025"),
)
for fn, title, pl, enacted in CHECKS:
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", (src / fn).read_text(encoding="utf-8", errors="replace"))))
    print(fn, "| title FOUND:", title in text, "| P.L. " + pl + ":", pl in text, "| enacted " + enacted + ":", enacted in text)
