import re, sys, collections
# HTML element names (WHATWG list, subset that can appear in these pages). Any '<name' not in this set is a raw '<' in text.
KNOWN = set("""a abbr address article aside audio b bdi bdo blockquote body br button canvas caption cite code col colgroup
data datalist dd del details dfn dialog div dl dt em embed fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header
hgroup hr html i iframe img input ins kbd label legend li link main map mark menu meta meter nav noscript object ol optgroup option
output p picture pre progress q rp rt ruby s samp script search section select slot small source span strong style sub summary sup
table tbody td template textarea tfoot th thead time title tr track u ul var video wbr svg path g circle line polyline polygon rect
text tspan defs use desc marker title foreignobject""".split())
for f in sys.argv[1:]:
    src = open(f, encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    bad = []
    for m in re.finditer(r"<(/?)([A-Za-z][A-Za-z0-9-]*)", body):
        name = m.group(2).lower()
        if name not in KNOWN:
            bad.append((body[:m.start()].count("\n") + 1, body[m.start():m.start()+30].replace("\n", " ")))
    print(f, "unknown_tag_like_lt:", len(bad), "entity_lt(&lt;):", src.count("&lt;"))
    for ln, ctx in bad:
        print("   line", ln, repr(ctx))
