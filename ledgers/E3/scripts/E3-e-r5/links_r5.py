"""Check every href/src target on project.html and index.html: fragments resolve to ids on the target page, relative
files exist, and concept links point at an existing anchor in course/concepts.html. Round 5. Standard library only.
usage: python -I links_r5.py <checkout-root>
"""

import html.parser
import os
import re
import sys

root = sys.argv[1]
base = os.path.join(root, "course/modules/E/E3")


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        for key in ("href", "src"):
            if key in d and d[key]:
                self.links.append((key, tag, d[key], d.get("class", "")))


def parse(path):
    p = P()
    p.feed(open(path, encoding="utf-8").read())
    return p


concepts = parse(os.path.join(root, "course/concepts.html"))
for page in ("project.html", "index.html"):
    p = parse(os.path.join(base, page))
    results = []
    for key, tag, target, cls in p.links:
        if target.startswith(("http://", "https://", "mailto:")):
            results.append(("EXTERNAL", target))
            continue
        if target.startswith("#"):
            ok = target[1:] in p.ids
            results.append(("OK" if ok else "MISSING", f"{key} {target} (same page)"))
            continue
        path, _, frag = target.partition("#")
        full = os.path.normpath(os.path.join(base, path)) if path else os.path.join(base, page)
        if not os.path.exists(full):
            results.append(("MISSING-FILE", target))
            continue
        if frag:
            if full.endswith(".html"):
                tgt = parse(full)
                ok = frag in tgt.ids
            else:
                ok = True
            if "concept" in cls and "concepts.html" in path:
                ok = frag in concepts.ids
            results.append(("OK" if ok else "MISSING-FRAGMENT", f"{key} {target} [{tag} class={cls}]"))
        else:
            results.append(("OK", f"{key} {target}"))
    counts = {}
    for status, _ in results:
        counts[status] = counts.get(status, 0) + 1
    print(page, "links:", len(results), counts)
    for status, text in results:
        if status not in ("OK",):
            print("  ", status, text)
    # concept links (class concept) with their anchor targets
    for key, tag, target, cls in p.links:
        if "concept" in cls:
            print("   concept link", target)
