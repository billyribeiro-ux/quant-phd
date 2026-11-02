"""Check every href/src in project.html resolves to a file, and every #fragment resolves to an id in that file (E3-e r1)."""
import os
import re
import sys
from html.parser import HTMLParser

PAGE = os.path.abspath(sys.argv[1])
BASE = os.path.dirname(PAGE)


class Ids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)
            if k in ("href", "src") and v:
                self.refs.append((tag, k, v))


def parse(path):
    p = Ids()
    p.feed(open(path, encoding="utf-8").read())
    return p


here = parse(PAGE)
bad = 0
cache = {}
for tag, attr, ref in here.refs:
    if ref.startswith(("http://", "https://", "mailto:")):
        print("EXTERNAL", tag, attr, ref)
        bad += 1
        continue
    if ref.startswith("#"):
        target, frag = PAGE, ref[1:]
        tpath = PAGE
    else:
        path, _, frag = ref.partition("#")
        tpath = os.path.normpath(os.path.join(BASE, path))
        if not os.path.exists(tpath):
            print("MISSING FILE", tag, attr, ref, "->", tpath)
            bad += 1
            continue
    if frag:
        if tpath not in cache:
            cache[tpath] = parse(tpath) if tpath.endswith(".html") else None
        ids = cache[tpath].ids if cache[tpath] is not None else None
        if ids is not None and frag not in ids:
            print("MISSING ANCHOR", tag, attr, ref, "in", os.path.relpath(tpath, BASE))
            bad += 1
        else:
            print("ok", tag, attr, ref)
    else:
        print("ok", tag, attr, ref)
print("refs", len(here.refs), "problems", bad)
