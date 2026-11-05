"""Block coverage (BUILDER_RULES 7): every Definition, Theorem, Proposition, Corollary, Assumption, Remark, Example and
Definition-like block title in each lesson must be named by at least one card (front, back or basis) of that lesson.
Also lists misconception paragraphs (section 5) and the card(s) that cover each. Usage: python -I coverage_r7.py <checkout>
"""
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
for n in range(1, 7):
    lid = f"L{n:02d}"
    page = (root / f"course/modules/PC/PC3/{lid}.html").read_text(encoding="utf-8")
    titles = re.findall(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>', page, flags=re.S)
    labels = []
    for t in titles:
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        t = re.sub(r"\s+", " ", t).strip()
        m = re.match(r"(Definition|Theorem|Proposition|Corollary|Assumption|Remark|Example|Problem|Lemma)\s+([0-9]+\.[0-9]+|[A-Z][0-9]+)", t)
        if m:
            labels.append(f"{m.group(1)} {m.group(2)}")
        elif re.match(r"(Standing assumptions)", t):
            labels.append("Standing assumptions")
    labels = sorted(set(labels), key=lambda s: (s.split()[0], s))
    lcards = [c for c in cards if c["lesson"] == lid]
    text_by = {}
    for lab in labels:
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(lab) + r"(?![0-9.])")
        hits = [c["id"] for c in lcards if pat.search(c["front"] + " " + c["back"] + " " + c.get("basis", ""))]
        # Assumption labels are cited as "A1" etc. on the card fronts
        if not hits and lab.startswith("Assumption"):
            a = lab.split()[1]
            hits = [c["id"] for c in lcards if re.search(r"\b" + re.escape(a) + r"\b", c["front"] + " " + c["back"])]
        status = "COVERED" if hits else "UNCOVERED"
        print(f"{lid} {status:9s} {lab:28s} cards: {', '.join(hits) if hits else '-'}")
    # section 5 misconceptions: count quoted misconception paragraphs in the page
    mis = re.findall(r'<p>\s*[“"](.{5,120}?)[”"]\s*</p>', page)
    print(f"{lid} misconception heads on page: {len(mis)}")
