import re, html, sys
src = open(sys.argv[1], encoding="utf-8").read()
for art in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % art, src, re.S)
    body = m.group(0)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', body, re.S)
    text_all = " ".join(memos)
    no_tags = re.sub(r"<[^>]+>", " ", text_all)
    no_tags = html.unescape(no_tags)
    # method 1: runs of non-space characters, headings included (tags replaced by space)
    m1 = len([t for t in no_tags.split(" ") if t.strip()])
    # method 2: tags removed without inserting space; split on whitespace
    t2 = html.unescape(re.sub(r"<[^>]+>", "", text_all))
    m2 = len(t2.split())
    # method 3: TeX math spans removed
    t3 = re.sub(r"\\\((.*?)\\\)", " ", t2, flags=re.S)
    m3 = len(t3.split())
    print(art, "memo blocks", len(memos), "| words (tags->space, split on whitespace):", m1,
          "| words (tags removed, split on whitespace):", m2, "| TeX math spans removed:", m3)
    print("  per block (tags removed):", [len(html.unescape(re.sub(r"<[^>]+>", "", x)).split()) for x in memos])
