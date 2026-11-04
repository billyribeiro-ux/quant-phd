import re, html
src = open("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/project.html", encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, src, re.S).group(0)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', art, re.S)
    for label, txt in (("raw", " ".join(memos)), ("unescaped", html.unescape(" ".join(memos)))):
        stripped = re.sub(r"<[^>]+>", " ", txt)
        if label == "unescaped":
            stripped = html.unescape(stripped)
        print(ex, label, "memo blocks:", len(memos), "words:", len(stripped.split()))
    # also count with tags removed without replacing by space (concatenate)
    txt2 = re.sub(r"<[^>]+>", "", " ".join(memos))
    print(ex, "tags removed without space:", len(html.unescape(txt2).split()))
    # memo text must be "memo text" passages only; show per passage counts
    for m in memos:
        print("   passage words:", len(html.unescape(re.sub(r"<[^>]+>", " ", m)).split()))
