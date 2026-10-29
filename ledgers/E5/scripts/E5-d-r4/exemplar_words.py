import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, src, re.S)
    art = m.group(0)
    heads = []
    body_all = []
    for mm in re.finditer(r'<div class="memo-text">(.*?)</div>', art, re.S):
        blk = mm.group(1)
        h = re.search(r"<h5>(.*?)</h5>", blk, re.S)
        ptxt = " ".join(re.findall(r"<p>(.*?)</p>", blk, re.S))
        ptxt = html.unescape(re.sub(r"<[^>]+>", "", ptxt))
        words = ptxt.split()
        heads.append((h.group(1), len(words)))
        body_all.append(words)
    tot = sum(n for _, n in heads)
    print(ex, "passages", heads, "body total (paragraphs only)", tot,
          "plus headings", tot + sum(len(html.unescape(h).split()) for h, _ in heads))
