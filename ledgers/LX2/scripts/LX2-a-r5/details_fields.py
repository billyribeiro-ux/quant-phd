"""Print the Title, Public Law and Amended Through fields of the two GovInfo details pages.

Usage: python -I details_fields.py <scratch dir with COMPS-1884_details.html and COMPS-1885_details.html>
"""
import html
import re
import sys

src = sys.argv[1]
for name in ("COMPS-1884_details.html", "COMPS-1885_details.html"):
    raw = open(f"{src}/{name}", encoding="utf-8", errors="replace").read()
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    print(f"== {name}")
    for pat in (r"To provide[^.]{0,200}", r"Public Law \d+-\d+[^.]{0,60}", r"Amended Through[^.]{0,60}", r"Enacted [A-Za-z]+ \d+, \d{4}"):
        for m in re.finditer(pat, text):
            print("  ", m.group(0)[:220])
            break
