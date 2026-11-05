"""Verifier r10: word counts of each exemplar memo (memo-text blocks, tags removed, headings included) and whole-article variants."""
import re, html
page = open("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/project.html", encoding="utf-8").read()
def article(aid):
    m = re.search(rf'<article class="exemplar" id="{aid}".*?</article>', page, re.S)
    return m.group(0)
def text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)
for aid in ("exemplar-a", "exemplar-b"):
    art = article(aid)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
    mem = " ".join(memos)
    print(aid, "memo-text blocks:", len(memos), "words (tags removed, headings included):", len(text(mem).split()))
    for i, mm in enumerate(memos):
        print("   block", i, len(text(mm).split()))
    # variant: article text without annotation and verdict
    body = re.sub(r'<aside.*?</aside>', ' ', art, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', ' ', body, flags=re.S)
    body = re.sub(r'<h4.*?</h4>', ' ', body, flags=re.S)
    print("   variant (article minus aside, verdict, h4):", len(text(body).split()))
