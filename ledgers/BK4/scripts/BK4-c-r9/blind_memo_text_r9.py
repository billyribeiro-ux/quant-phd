"""Round-9 blind extraction: prints only the memo text of exemplars A and B (no annotations, verdicts or data-scores)."""
import re, sys, html
page = open(sys.argv[1], encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="' + ex + r'".*?<div class="memo-text">(.*?)</div>\s*<aside', page, re.S)
    txt = re.sub(r"<[^>]+>", "", m.group(1))
    print("==", ex)
    print("\n".join(line.strip() for line in html.unescape(txt).splitlines() if line.strip()))
