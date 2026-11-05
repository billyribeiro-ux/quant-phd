"""Round-10 word counts of the exemplar memo texts (project.html), headings included, tags removed two ways."""

import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
for name in ("exemplar-a", "exemplar-b"):
    start = page.index(f'id="{name}"')
    end = page.index("</article>", start)
    block = page[start:end]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, flags=re.S)
    raw = " ".join(memos)
    spaced = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    joined = html.unescape(re.sub(r"<[^>]+>", "", raw))
    print(f"{name}: memo blocks={len(memos)} words(tags->space)={len(spaced.split())} words(tags->'')={len(joined.split())}")
