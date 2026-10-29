import html.parser, pathlib, re
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-M5-b/course/modules/M/M5")
known = set("a abbr body br button code dd details div dfn dl dt em fieldset footer h1 h2 h3 h4 head header html i input label legend li link main meta nav ol option p pre s script section small span strong style summary svg table tbody td th thead title tr u ul var sub sup img figure figcaption caption path g circle line rect text desc defs use noscript iframe template select textarea hr".split())
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.bad=[]
    def handle_starttag(s, tag, attrs):
        if tag not in known: s.bad.append((s.getpos(), tag))
for lid in ["L05","L06","L07"]:
    t=(root/f"{lid}.html").read_text()
    p=P(); p.feed(t); print(lid, "unknown start tags:", p.bad[:10])
    # raw < followed by letter or digit inside prose (not a tag)
    for i,l in enumerate(t.splitlines(),1):
        for m in re.finditer(r'<(?=[A-Za-z]{1,2}\b)(?![/!a-zA-Z]+[ >])', l):
            pass
import collections
