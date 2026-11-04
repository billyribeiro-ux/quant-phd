"""Word count of each exemplar's memo text: the div.memo-text blocks of the article, tags removed, headings included,
words are runs of non-whitespace characters (the page's own definition, project.html line 621)."""
import html
import re
import sys
from pathlib import Path

page = (Path(sys.argv[1]) / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, page, re.S).group(0)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', art, re.S)
    text = " ".join(re.sub(r"<[^>]+>", " ", m) for m in memos)
    text = html.unescape(text)
    runs = text.split()
    print(ex, "memo blocks:", len(memos), "| words (non-space runs, tags removed, headings included):", len(runs))
    raw = " ".join(memos)
    print(ex, "words if tags are left in (for comparison):", len(raw.split()))
