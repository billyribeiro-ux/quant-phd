"""Verifier round 12: dump every labelled block of each M4 lesson in full (nested divs and bare '<' in math kept).
Blocks run from their opening <div class="block ..."> to the next block opening or the end of the <section>."""
import html
import re
import sys
from pathlib import Path

LESSONS = Path("course/modules/M/M4")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*)?/?>")
START = re.compile(r'<div class="block ([a-z]+)">')
TITLE = re.compile(r'<span class="block-title[^"]*"(?: data-grade="([A-Z])")?>(.*?)</span>\s*</span>|<span class="block-title[^"]*"(?: data-grade="([A-Z])")?>(.*?)</span>', re.S)


def plain(s):
    s = TAG.sub("", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


for page in sorted(LESSONS.glob("L*.html")):
    raw = page.read_text(encoding="utf-8")
    starts = [(m.start(), m.group(1)) for m in START.finditer(raw)]
    lines = []
    for idx, (pos, kind) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(raw)
        seg = raw[pos:end]
        cut = seg.find("</section>")
        if cut != -1:
            seg = seg[:cut]
        m = re.search(r'<span class="block-title[^"]*"(?: data-grade="([A-Z])")?>', seg)
        if not m:
            lines.append(f"[{kind}] (no title) :: {plain(seg)}")
            continue
        # title spans nest one level: take until the matching close of the outer span
        t0 = m.end()
        depth = 1
        i = t0
        while depth and i < len(seg):
            if seg.startswith("<span", i):
                depth += 1
            elif seg.startswith("</span>", i):
                depth -= 1
            i += 1
        title = plain(seg[t0:i - len("</span>")])
        grade = m.group(1) or "-"
        content = plain(seg[i:])
        lines.append(f"[{kind}] {title} grade={grade} :: {content}")
    (OUT / f"{page.stem}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(page.stem, len(lines), "blocks", sum(len(x) for x in lines), "chars")
