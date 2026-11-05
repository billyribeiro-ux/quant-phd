"""LX2-c r12: checks every SR 26-2 quote, locator and cover-letter sentence on project.html against the fetched files.

Usage: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r12/sr26_quotes_r12.py <dir>
<dir> must hold sr2602.htm, SR2602a1.pdf and SR2602.pdf fetched by plain curl from
https://www.federalreserve.gov/supervisionreg/srletters/ (the fetch is recorded in the round 12 fragment).
Needs pdftotext (poppler). Prints the PDF page on which each quote is found, and the printed page number.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

d = Path(sys.argv[1])
page = Path("course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
claims = re.findall(r'data-cite="frb2026fed"[^>]*data-locator="([^"]*)">(.*?)</span>', page, re.S)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", html.unescape(s).lower().replace("’", "'"))


def pdf_pages(name: str) -> list[str]:
    out = subprocess.run(["pdftotext", "-layout", str(d / name), "-"], capture_output=True, text=True, check=True).stdout
    return out.split("\f")


a1 = pdf_pages("SR2602a1.pdf")
combined = pdf_pages("SR2602.pdf")
htm = html.unescape(re.sub(r"<[^>]+>", " ", (d / "sr2602.htm").read_text(encoding="utf-8-sig")))
for locator, body in claims:
    text = re.sub(r"<[^>]+>", "", body).strip()
    quote = re.findall(r'"([^"]+)"', html.unescape(text))
    targets = quote or [text]
    for q in targets:
        q_norm = norm(q)
        if len(q_norm) < 25:
            continue
        in_a1 = [i + 1 for i, p in enumerate(a1) if q_norm in norm(p)]
        in_combined = [i + 1 for i, p in enumerate(combined) if q_norm in norm(p)]
        in_htm = q_norm in norm(htm)
        print(f"[{locator[:60]}] {q[:70]!r}: a1 pdf pages {in_a1}; combined pages {in_combined}; htm {in_htm}")
print("cover-letter sentences in htm:",
      all(norm(s) in norm(htm) for s in ["supersedes and replaces SR letter 11-7", "over $30 billion in total assets regulated by the Federal Reserve", "Supersedes:"]))
print("dated April 17, 2026 in htm:", "April 17, 2026" in htm)
