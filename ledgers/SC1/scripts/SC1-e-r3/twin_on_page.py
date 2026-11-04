"""Check that each SC1 lab twin's code (whitespace-collapsed) appears verbatim in its lesson page (read-only).

Usage: twin_on_page.py <labs dir> <module dir>
"""
import html
import re
import sys

labs, module = sys.argv[1], sys.argv[2]
for n in range(1, 9):
    twin = open(f"{labs}/lab-SC1-L0{n}-1.py", encoding="utf-8").read()
    page = open(f"{module}/L0{n}.html", encoding="utf-8").read()
    norm_twin = re.sub(r"\s+", " ", twin).strip()
    norm_page = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page))).strip()
    # Compare the twin's code body (skip the first docstring line) against the page text
    probe = norm_twin[:120]
    print(f"L0{n}: twin {len(norm_twin)} chars; first 120 chars on page: {probe in norm_page}; "
          f"full twin on page: {norm_twin in norm_page}")
