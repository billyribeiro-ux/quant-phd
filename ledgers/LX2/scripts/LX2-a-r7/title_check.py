"""Check the two quoted Act titles (L01.html:59, :61) and the two amendment lines (L01.html:65) against the GovInfo
details pages and the compilation text.

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/title_check.py <source_dir>
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quote_locate as q  # noqa: E402


def details_text(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    return q.alnum(html.unescape(re.sub(r"<[^>]+>", " ", raw)))


def main() -> int:
    src = sys.argv[1]
    t84 = details_text(os.path.join(src, "COMPS-1884_details.html"))
    t85 = details_text(os.path.join(src, "COMPS-1885_details.html"))
    s84 = ("To provide full and fair disclosure of the character of securities sold in interstate and foreign commerce "
           "and through the mails, and to prevent frauds in the sale thereof, and for other purposes.")
    s85 = ("To provide for the regulation of securities exchanges and of over-the-counter markets operating in interstate "
           "and foreign commerce and through the mails, to prevent inequitable and unfair practices on such exchanges and "
           "markets, and for other purposes.")
    print("1933 title (L01.html:59) in COMPS-1884 details:", q.alnum(s84) in t84)
    print("1934 title (L01.html:61) in COMPS-1885 details:", q.alnum(s85) in t85)
    for label, text, pl in (("COMPS-1884", t84, "119-27"), ("COMPS-1885", t85, "119-60")):
        print(label, "details carries Public Law", pl, ":", ("Public Law " + pl) in text.replace("Public Law", "Public Law ").replace("  ", " ") or ("publiclaw" + pl.replace("-", "")) in text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
