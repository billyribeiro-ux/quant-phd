"""Locate each quotation of L02 in the printed pages of the opinion text (pdftotext, pages split on form feed).

Usage: python -I page_locate.py <dirks.txt|ohagan.txt> <page.html> <first_page> <last_page>
For every curly-quoted passage (>= 12 chars) it prints the printed page(s) on which the normalised passage occurs.
A printed page is the 3-digit number that the running head carries (the page's first line or last line).
The locator text on the page is printed beside it so the reader can compare.
"""
import html
import re
import sys

src, page_html = sys.argv[1], sys.argv[2]
lo, hi = int(sys.argv[3]), int(sys.argv[4])
raw_text = open(src, encoding="utf-8", errors="replace").read()
pages = raw_text.split("\f")


def norm(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r"\[([a-zA-Z])\]", r"\1", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"-\s", "", s)  # soft hyphen at line end: join
    s = re.sub(r"[^A-Za-z0-9]", "", s)
    return s.lower()


def printed_page(text: str) -> int | None:
    heads = [ln for ln in text.splitlines() if ln.strip()]
    for ln in heads[:3] + heads[-3:]:
        s_ = ln.strip()
        m = re.match(r"^(\d{3})\b", s_) or re.search(r"\b(\d{3})$", s_)
        if m and (lo <= int(m.group(1)) <= hi):
            return int(m.group(1))
    return None


page_nums = [printed_page(p) for p in pages]
# Build a normalised corpus per pdf page, keeping the printed page number for each.
corpus = [(page_nums[i], norm(pages[i])) for i in range(len(pages))]

raw = open(page_html, encoding="utf-8").read()
raw = html.unescape(re.sub(r"<[^>]+>", "", raw))
quotes = re.findall(r"“([^”]{12,})”", raw)
for q in quotes:
    nq = norm(q)
    if len(nq) < 10:
        continue
    hits = sorted({pn for pn, c in corpus if pn is not None and nq in c})
    # try the first 60 normalised characters if the full passage spans a page break
    if not hits:
        head = nq[:60]
        hits = sorted({pn for pn, c in corpus if pn is not None and head in c})
        tag = "HEAD60"
    else:
        tag = "FULL"
    print(f"{tag} pages={hits if hits else 'NONE'} | {q[:110]}")
