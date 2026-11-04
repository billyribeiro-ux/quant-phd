"""LX2-c round 4: locators for the SR 26-2 statements on project.html, read from letter.txt (pdftotext -layout).

Run: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/sr2602_checks_r4.py <dir containing letter.txt>
"""

import sys
from pathlib import Path

text = (Path(sys.argv[1]) / "letter.txt").read_text(encoding="utf-8")
pages = text.split("\f")
checks = [
    "the attached Revised Guidance on Model Risk Management, which supersedes and replaces SR",
    "letter 11-7, Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8",
    "Applicability: This letter is expected to be most relevant to banking organizations with over $30",
    "Supersedes:",
    "April 17, 2026",
    "Components of Model Validation",
    "Conceptual Soundness",
    "Outcomes Analysis",
    "Ongoing Model Monitoring",
]
flat = " ".join(text.split())
for c in checks:
    needle = " ".join(c.split())
    where = [i for i, p in enumerate(pages, 1) if needle in " ".join(p.split())]
    print(f"{c[:70]!r}: found={needle in flat} pdf_pages={where}")
