"""Count words of the two exemplar memo texts (tags removed, runs of characters between spaces), and the spec length."""
import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    start = page.index(f'id="{ex}"')
    end = page.index("</article>", start)
    block = page[start:end]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, re.S)
    text = " ".join(memos)
    no_tags = re.sub(r"<[^>]+>", " ", text)
    no_tags = no_tags.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    by_space_runs = [t for t in no_tags.split(" ") if t]
    by_ws = no_tags.split()
    print(f"{ex}: memo blocks={len(memos)} words(split ' ' non-empty)={len(by_space_runs)} words(split whitespace)={len(by_ws)}")
