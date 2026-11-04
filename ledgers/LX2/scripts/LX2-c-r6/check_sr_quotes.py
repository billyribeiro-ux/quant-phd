"""Locate each quoted passage of project.html in the SR 26-2 attachment PDF text (pdftotext -layout output).

Usage: python3 -I check_sr_quotes.py <sr.txt> <sr_html.txt>
Prints the PDF page index (1-based), the printed page number found on that page, and whether the quote occurs
after joining hyphen-free whitespace. Only plain text matching; no network.
"""
import re
import sys

pdf_path, html_path = sys.argv[1], sys.argv[2]
pdf_pages = open(pdf_path, encoding="utf-8").read().split("\f")
html_text = open(html_path, encoding="utf-8").read()


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


quotes = [
    ("conceptual soundness", "Validating conceptual soundness involves assessing and documenting model design (including key modeling choices, assumptions, qualitative judgments, and data selection), construction, and developmental testing."),
    ("outcomes analysis", "Outcomes analysis compares model outputs to corresponding real-world outcomes to assess model performance relative to model objectives and business use."),
    ("limitations 1", "includes an assessment of a model's reliability and its limitations"),
    ("limitations 2", "Sound validation identifies model limitations and errors"),
    ("monitoring", "Ongoing model monitoring involves an evaluation of the extent to which a model is performing as expected given potential changes in products, exposures, activities, clients, data relevance, or market conditions."),
    ("established thresholds", "established performance thresholds"),
    ("enforceable", "This guidance does not set forth enforceable standards or prescriptive requirements"),
]
for name, q in quotes:
    qn = norm(q)
    hits = []
    for i, page in enumerate(pdf_pages, start=1):
        pn = norm(page)
        # allow the apostrophe variants
        if qn.lower() in pn.lower() or qn.replace("'", "’").lower() in pn.lower():
            m = re.findall(r"\n\s*(\d{1,2})\s*\n?\s*$", page.rstrip())
            hits.append((i, m[-1] if m else "?"))
    print(f"{name}: pdf_page_hits={hits}")

for name, q in [
    ("supersedes html", "supersedes and replaces SR letter 11-7"),
    ("applicability html", "expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve"),
    ("April 17 2026", "April 17, 2026"),
]:
    print(f"{name}: html_count={norm(html_text).count(norm(q))}")
