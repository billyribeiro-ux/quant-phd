"""Check each attachment and cover-letter quote on the project page against the SR 26-2 PDFs fetched by plain curl.
Usage: quote_check_r7.py <dir with SR2602.pdf and SR2602a1.pdf already converted to combined.txt / attach.txt by pdftotext -layout>"""
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
combined = (d / "combined.txt").read_text(encoding="utf-8")
attach = (d / "attach.txt").read_text(encoding="utf-8")
letter = (d / "letter.txt").read_text(encoding="utf-8")


def norm(x: str) -> str:
    x = x.replace("\f", " ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", x)


def pdf_pages(text: str, phrase: str) -> list[int]:
    return [i for i, p in enumerate(text.split("\f"), 1) if norm(phrase) in norm(p)]


quotes = {
    "p346 conceptual soundness": "Validating conceptual soundness involves assessing and documenting model design (including key modeling choices, assumptions, qualitative judgments, and data selection), construction, and developmental testing.",
    "p347 outcomes analysis": "Outcomes analysis compares model outputs to corresponding real-world outcomes to assess model performance relative to model objectives and business use.",
    "p347 thresholds": "established performance thresholds",
    "p348 limitations (a)": "includes an assessment of a model's reliability and its limitations",
    "p348 limitations (b)": "Sound validation identifies model limitations and errors",
    "p349 monitoring": "Ongoing model monitoring involves an evaluation of the extent to which a model is performing as expected given potential changes in products, exposures, activities, clients, data relevance, or market conditions.",
    "p360 section I": "This guidance does not set forth enforceable standards or prescriptive requirements",
    "p359 supersession (condensed)": "supersedes and replaces SR letter 11-7 and SR letter 21-8",
    "p360 applicability": "This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.",
}
for k, q in quotes.items():
    where = pdf_pages(letter if "applicability" in k or "supersession" in k else (attach if False else combined), q)
    exact = norm(q) in norm(combined) or norm(q) in norm(letter)
    print(f"{k}: exact={exact} combined-PDF pages={pdf_pages(combined, q)} attachment-file pages={pdf_pages(attach, q)} letter pages={pdf_pages(letter, q)}")
