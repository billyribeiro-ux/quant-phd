# Word counts of the two exemplar memo texts (the memo-text blocks only; tags removed; headings included).
import html, re
page = open("/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/course/modules/E/E3/project.html", encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, page, re.S).group(0)
    memo = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
    text = " ".join(memo)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    space_runs = [w for w in text.split(" ") if w]
    ws_runs = text.split()
    print(ex, "blocks", len(memo), "runs between spaces", len(space_runs), "whitespace-separated", len(ws_runs))
