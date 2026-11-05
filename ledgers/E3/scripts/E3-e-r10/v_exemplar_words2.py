"""Verifier r10: alternative word-count conventions for both exemplars, to test the page's stated 117 and 603."""
import re, html
page = open("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/project.html", encoding="utf-8").read()
def art(aid):
    return re.search(rf'<article class="exemplar" id="{aid}".*?</article>', page, re.S).group(0)
def strip_tags(s, repl):
    return html.unescape(re.sub(r"<[^>]+>", repl, s))
for aid in ("exemplar-a", "exemplar-b"):
    a = art(aid)
    memos = " ".join(re.findall(r'<div class="memo-text">(.*?)</div>', a, re.S))
    variants = {
        "memo tags->space": len(strip_tags(memos, " ").split()),
        "memo tags->empty": len(strip_tags(memos, "").split()),
        "whole article tags->space": len(strip_tags(a, " ").split()),
        "whole article tags->empty": len(strip_tags(a, "").split()),
        "memo plus annotations tags->space": len(strip_tags(" ".join(re.findall(r'<div class="passage">(.*?)</div>\s*</div>', a, re.S)) or a, " ").split()),
    }
    print(aid, variants)
    # per-passage counts including annotation
    for i, p in enumerate(re.findall(r'<div class="passage">(.*?)</aside>\s*</div>', a, re.S)):
        print("   passage", i, len(strip_tags(p, " ").split()))
