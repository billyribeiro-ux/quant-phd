"""Ruling 15 extraction: the memo prose of each exemplar, with the annotation elements (aside), the verdict lines
(p.exemplar-verdict), and data-score(s) attributes dropped. Output is plain text per passage, headings kept as labels.
Round 15, SC1-d. Usage: blind_extract_r15.py <checkout root>"""
import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1], "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
for eid in ("exemplar-a", "exemplar-b"):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % eid, page, re.S).group(0)
    art = re.sub(r'<p class="exemplar-verdict".*?</p>', "", art, flags=re.S)
    art = re.sub(r'<aside.*?</aside>', "", art, flags=re.S)
    print(f"=== {eid} (memo prose only)")
    for block in re.split(r'<div class="passage">', art)[1:]:
        memo = re.search(r'<div class="memo-text">(.*?)</div>\s*$', block.split('</article>')[0], re.S)
        inner = memo.group(1) if memo else block
        inner = re.sub(r"<h5>(.*?)</h5>", lambda m: "\n## " + html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) + "\n", inner, flags=re.S)
        inner = re.sub(r"</p>|</li>", "\n", inner)
        inner = re.sub(r"<li[^>]*>", "- ", inner)
        text = html.unescape(re.sub(r"<[^>]+>", "", inner))
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text).strip()
        print(text)
        print()
