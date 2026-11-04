import html, re, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3")
page = open("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/project.html", encoding="utf-8").read()
def article(aid):
    start = page.index(f'<article class="exemplar" id="{aid}"')
    end = page.index("</article>", start)
    return page[start:end]
for aid in ("exemplar-a", "exemplar-b"):
    art = article(aid)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', art, re.S)
    total = 0
    for m in memos:
        txt = html.unescape(re.sub(r"<[^>]+>", " ", m))
        total += len(txt.split())
    # also the full article text, for comparison
    full = html.unescape(re.sub(r"<[^>]+>", " ", art)).split()
    print(aid, "memo blocks:", len(memos), "memo words (headings included):", total, "| whole article words:", len(full))
# report whole-page grader words for the 350-800 claim (informational)
