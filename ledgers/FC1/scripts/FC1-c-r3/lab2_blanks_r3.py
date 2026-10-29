"""Checks the Lab 2 completion block: exactly two blanks, and the page code with the blanks filled as Lab 2's prose
says equals the twin.

Usage: python ledgers/FC1/scripts/FC1-c-r3/lab2_blanks_r3.py <checkout-root>
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
m = re.search(r'id="lab-FC1-project-2".*?<pre><code[^>]*>(.*?)</code></pre>', page, re.S)
assert m, "Lab 2 block not found"
code = html.unescape(m.group(1))
twin = (root / "tests/labs/FC1/lab-FC1-project-2.py").read_text(encoding="utf-8")
blanks = code.count("___")
filled = code.replace("(1 + y) ** ___", "(1 + y) ** period").replace("(settlement_day, ___)", "(settlement_day, -side * quantity * price_cents)")
print("blanks on page:", blanks, "| filled page == twin:", filled.strip() == twin.strip())
