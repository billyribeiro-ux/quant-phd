"""Blind exemplar extraction (ruling 15): memo prose only, with annotations, verdict lines and data-score(s) dropped.

Writes ledgers/BK4/scripts/BK4-c-r15/out/memo_prose_A.txt and memo_prose_B.txt. The official scores and
annotations are NOT printed by this script.
"""
import html
import re
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
out = ROOT / "ledgers/BK4/scripts/BK4-c-r15/out"
for label in ("A", "B"):
    m = re.search(rf'<article class="exemplar" id="exemplar-{label.lower()}".*?</article>', page, flags=re.S)
    art = m.group(0)
    memo = re.search(r'<div class="memo-text">(.*?)</div>\s*<aside', art, flags=re.S).group(1)
    lines = []
    for tag, body in re.findall(r"<(h5|p)[^>]*>(.*?)</\1>", memo, flags=re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        lines.append(("## " if tag == "h5" else "") + text)
    (out / f"memo_prose_{label}.txt").write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    print(f"exemplar {label}: {len(lines)} prose blocks, {sum(len(x.split()) for x in lines)} words")
