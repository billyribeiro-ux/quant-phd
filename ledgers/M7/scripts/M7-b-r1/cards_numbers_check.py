"""Verifier script (M7-b round 2): every number in an L04-L06 card back must appear in its lesson page.

A fraction a/b counts as present when the page has the plain text a/b or the LaTeX form {a}{b} (tfrac, frac).
Run from the checkout root with: python3 -I ledgers/M7/scripts/M7-b-r2/cards_numbers_check.py
"""
import html
import json
import re

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
raw_pages = {p: open(f"course/modules/M/M7/{p}.html", encoding="utf-8").read() for p in ("L04", "L05", "L06")}
text_pages = {p: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r))) for p, r in raw_pages.items()}
num_re = re.compile(r"\d+(?:\.\d+)?(?:/\d+)?")


def present(token, page):
    if token in text_pages[page]:
        return True
    if "/" in token:
        a, b = token.split("/")
        return ("{%s}{%s}" % (a, b)) in raw_pages[page]
    return False


checked = 0
missing = []
for c in cards:
    if c["lesson"] not in raw_pages:
        continue
    checked += 1
    for n in sorted(set(num_re.findall(c["back"]))):
        if not present(n, c["lesson"]):
            missing.append((c["id"], n))
print("cards checked", checked)
for m in missing:
    print("NOT IN LESSON", m)
print("missing count", len(missing))
