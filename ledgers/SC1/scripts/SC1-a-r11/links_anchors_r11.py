"""Local link and anchor check for index.html, L01.html, L02.html, L03.html (round 11).

Every href that is not external must resolve to an existing file, and every fragment must match an id in the
target file. Also counts the local links checked.
"""

import html.parser
import os
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a/course/modules/SC/SC1/"
pages = ["index.html", "L01.html", "L02.html", "L03.html"]


class Collect(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "a" and "href" in d:
            self.hrefs.append(d["href"])


parsed = {}
for p in pages:
    c = Collect()
    c.feed(open(ROOT + p, encoding="utf-8").read())
    parsed[p] = c

total = 0
bad = []
for p in pages:
    for h in parsed[p].hrefs:
        if re.match(r"^[a-z]+:", h) or h.startswith("#") and h == "#":
            continue
        total += 1
        path, _, frag = h.partition("#")
        target = os.path.normpath(os.path.join(ROOT, path)) if path else os.path.join(ROOT, p)
        if not os.path.exists(target):
            bad.append((p, h, "missing file"))
            continue
        if frag:
            if target.endswith(".html"):
                tgt = Collect()
                tgt.feed(open(target, encoding="utf-8").read())
                if frag not in tgt.ids:
                    bad.append((p, h, "missing anchor"))
print("local links checked:", total)
print("broken:", bad)
