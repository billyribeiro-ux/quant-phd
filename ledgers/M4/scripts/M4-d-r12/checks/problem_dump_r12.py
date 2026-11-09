"""Verifier round 12: dump problem-set items (div.problem) and the hidden 'explain' answers of each M4 lesson."""
import html
import re
import sys
from pathlib import Path

TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*)?/?>")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", s))).strip()


for page in sorted(Path("course/modules/M/M4").glob("L*.html")):
    raw = page.read_text(encoding="utf-8")
    parts = re.split(r'(?=<div class="problem" id=")', raw)
    lines = []
    for p in parts[1:]:
        m = re.match(r'<div class="problem" id="([^"]+)">', p)
        end = p.find("</section>")
        seg = p if end == -1 else p[:end]
        lines.append(f"[problem {m.group(1)}] {plain(seg)}")
    (OUT / f"{page.stem}_problems.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(page.stem, len(lines), "problems", sum(len(x) for x in lines), "chars")
