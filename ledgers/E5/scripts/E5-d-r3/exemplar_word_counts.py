"""E5 slice d r3: word counts of the exemplar memos against the page's own brief limits (summary <= 80 words; body <= 600 words).
Usage: python3 -I exemplar_word_counts.py <repo-root>"""
import html, re, sys
from pathlib import Path
s = (Path(sys.argv[1]) / "course/modules/E/E5/project.html").read_text(encoding="utf-8")
for ex in ["exemplar-a", "exemplar-b"]:
    blk = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, s, flags=re.S).group(0)
    tot = 0
    for p in re.findall(r'<div class="memo-text">(.*?)</div>', blk, flags=re.S):
        w = len(html.unescape(re.sub(r"<[^>]+>", " ", p)).split())
        tot += w
        h = re.search(r"<h5>(.*?)</h5>", p)
        print(ex, h.group(1) if h else "?", w)
    print(ex, "TOTAL body words incl. headings", tot)
