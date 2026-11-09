"""Closing-round source check (LX2-c round 1): the SR 26-2 sentences and quotes the project page cites.

Inputs are the files fetched by plain curl on 2026-11-09 into /tmp/lx2c-r1-src-closing (SR2602a1.pdf, SR2602.pdf,
sr2602.htm) and their pdftotext -layout extracts (a1.txt, combined.txt), made with the poppler pdftotext on this machine.
Prints the sha256 of each file, the PDF page of each attachment quote, and whether each cover-letter sentence is present.
Run: .venv/bin/python ledgers/LX2/scripts/LX2-c-r1/sources_check_r1.py   (from the checkout root)
"""

from __future__ import annotations

import hashlib
import html
import re

SRC = "/tmp/lx2c-r1-src-closing"


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'"))


def main() -> int:
    for name in ("SR2602a1.pdf", "SR2602.pdf", "sr2602.htm"):
        print(f"sha256 {name} {sha(f'{SRC}/{name}')}")
    raw = open(f"{SRC}/sr2602.htm", encoding="utf-8", errors="replace").read()
    htm = norm(html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    cover = [
        "supersedes and replaces SR letter 11-7, Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8",
        "Applicability: This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.",
        "Supersedes: SR letter 11-7",
    ]
    for s in cover:
        print(f"htm {'FOUND' if s in htm else 'MISSING'}: {s[:70]}")
    combined = norm(open(f"{SRC}/combined.txt", encoding="utf-8").read())
    print(f"combined.pdf {'FOUND' if 'supersedes and replaces SR letter 11-7' in combined else 'MISSING'}: cover letter sentence")
    pages = open(f"{SRC}/a1.txt", encoding="utf-8").read().split("\f")
    print(f"a1.pdf pages {len(pages)}")
    quotes = [
        "Validating conceptual soundness",
        "Outcomes analysis compares",
        "established performance thresholds",
        "Sound validation identifies",
        "Ongoing model monitoring involves",
        "includes an assessment of a model",
        "This guidance does not set forth enforceable standards or prescriptive requirements",
        "Conceptual Soundness",
        "Outcomes Analysis",
        "Ongoing Model Monitoring",
    ]
    for q in quotes:
        found = [i + 1 for i, p in enumerate(pages) if q in norm(p)]
        print(f"a1.pdf pages {found}: {q}")
    print("a1.pdf Limitations heading:", "Limitations" in norm("".join(pages)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
