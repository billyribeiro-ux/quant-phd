"""Word-count variants for the exemplar memo texts: tags removed with no space, with space, and with/without headings."""
import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    start = page.index(f'id="{ex}"')
    end = page.index("</article>", start)
    block = page[start:end]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, re.S)
    for label, body in (("all", memos), ("no-h5", [re.sub(r"<h5>.*?</h5>", "", m, flags=re.S) for m in memos])):
        text = " ".join(body)
        for mode in ("tags->empty", "tags->space"):
            t = re.sub(r"<[^>]+>", "" if mode == "tags->empty" else " ", text)
            t = t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            runs_space = [x for x in t.split(" ") if x]
            runs_ws = t.split()
            print(f"{ex} {label} {mode}: split(' ')={len(runs_space)} split(ws)={len(runs_ws)}")
    # math-free count: strip \( ... \) spans too
    text = " ".join(memos)
    t = re.sub(r"<[^>]+>", "", text)
    print(f"{ex} raw-html-length chars={len(t)}")
