"""List every start-tag name in SC1 lesson pages that is not a standard HTML/SVG element name.

A raw '<' followed by an ASCII letter inside math is read by an HTML parser as a start tag; this prints any such
unexpected name with its line. Usage: python -I tag_names.py <paths...>.
"""
import sys
from html.parser import HTMLParser

KNOWN = set("""a abbr article aside audio b blockquote body br button canvas caption cite code col colgroup dd del
details dfn dialog div dl dt em fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe
img input ins kbd label legend li link main mark meta nav noscript ol optgroup option p picture pre q s samp script
section select small source span strong style sub summary sup table tbody td template textarea tfoot th thead time
title tr u ul var video wbr svg path g circle line rect polyline polygon text tspan defs title desc use marker
clippath lineargradient stop ellipse foreignobject""".split())


class Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []

    def handle_starttag(self, tag, attrs):
        if tag not in KNOWN:
            self.bad.append((self.getpos()[0], tag))


for path in sys.argv[1:]:
    p = Collect()
    p.feed(open(path, encoding="utf-8").read())
    print(f"{path}: unexpected start-tag names = {len(p.bad)}")
    for line, tag in p.bad:
        print(f"  {path}:{line}: <{tag}")
