"""List every class="claim" span of project.html with its locator and whether its quoted text is found verbatim
(after whitespace and apostrophe normalisation) in the SR 26-2 letter or attachment text.

Usage: python3 -I claim_spans.py <project.html> <sr.txt> <sr_html.txt>
"""
import html as htmlmod
import re
import sys

page_path, pdf_path, html_path = sys.argv[1], sys.argv[2], sys.argv[3]
page = open(page_path, encoding="utf-8").read()
pdf = open(pdf_path, encoding="utf-8").read()
srh = open(html_path, encoding="utf-8").read()


def norm(s: str) -> str:
    s = htmlmod.unescape(s)
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip().strip('"').lower()


pdf_n = norm(pdf)
html_n = norm(srh)
spans = re.findall(r'<span class="claim"([^>]*)>(.*?)</span>', page, flags=re.S)
print(f"claim spans: {len(spans)}")
for attrs, body in spans:
    loc = re.search(r'data-locator="([^"]*)"', attrs)
    cite = re.search(r'data-cite="([^"]*)"', attrs)
    text = norm(body)
    # strip the surrounding quote marks and split on the sentence-level quotes if several quotes are inside
    parts = [p.strip().strip('"').strip() for p in re.split(r'"\s*and\s*"|"\s*"', text) if p.strip()]
    in_pdf = [p.rstrip(".") in pdf_n for p in parts]
    in_html = [p.rstrip(".") in html_n for p in parts]
    print(f"- cite={cite.group(1) if cite else None} locator={loc.group(1) if loc else None}")
    print(f"  text={text[:110]!r}")
    print(f"  in_pdf={in_pdf} in_letter_html={in_html}")
