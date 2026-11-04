"""Round-2 BK4-a: every href on index, L01-L03 resolves to an existing file, and every #fragment to an id in that file."""

import os
from html.parser import HTMLParser

BASE = "course/modules/BK/BK4/"


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        a = dict(attrs)
        if "id" in a and a["id"]:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.hrefs.append(a["href"])


def parse(path: str) -> Links:
    p = Links()
    with open(path, encoding="utf-8") as fh:
        p.feed(fh.read())
    return p


total = 0
problems = 0
for page in ["index.html", "L01.html", "L02.html", "L03.html"]:
    for h in parse(BASE + page).hrefs:
        if h.startswith(("http://", "https://", "mailto:")):
            print(page, "EXTERNAL", h)
            problems += 1
            continue
        total += 1
        target, _, frag = h.partition("#")
        path = os.path.normpath(os.path.join(BASE, target)) if target else BASE + page
        if not os.path.exists(path):
            print(page, "MISSING FILE", h)
            problems += 1
            continue
        if frag and frag not in parse(path).ids:
            print(page, "MISSING ANCHOR", h)
            problems += 1
print("links checked", total, "problems", problems)
