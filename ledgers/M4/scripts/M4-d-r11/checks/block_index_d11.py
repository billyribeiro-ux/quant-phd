"""Index every labelled block (Definition, Theorem, Proposition, Example, Remark, Lemma, Problem, Assumption) of each
M4 lesson: label, grade, name, and the block's text (math kept as TeX, tags stripped). Writes one text file per lesson
under the scratch folder given as argv[1]. Standard library only."""

import html
import re
import sys
from pathlib import Path

LESSONS = Path("course/modules/M/M4")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
BLOCK = re.compile(r'<div class="block ([a-z]+)">(.*?)</div>', re.S)
TITLE = re.compile(r'<span class="block-title[^"]*"(?: data-grade="([A-Z])")?>(.*?)</span>', re.S)


def plain(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


for page in sorted(LESSONS.glob("L*.html")):
    raw = page.read_text(encoding="utf-8")
    lines = []
    for kind, body in BLOCK.findall(raw):
        m = TITLE.search(body)
        if not m:
            continue
        title = plain(m.group(2))
        grade = m.group(1) or "-"
        content = plain(body[m.end():])
        lines.append(f"[{kind}] {title} grade={grade} :: {content}")
    (OUT / f"{page.stem}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(page.stem, len(lines), "blocks")
