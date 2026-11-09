"""Independent link scan for the PC3 slice-a pages (round 1). Checks every href and src that is a local path.

For a relative href with a fragment, the fragment must be an id or name in the target file. Read-only.
Usage: python3 -I link_scan.py <checkout root>
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1])
pages = [root / "course/modules/PC/PC3" / p for p in ("index.html", "L01.html", "L02.html", "L03.html")]


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for k, v in attrs:
            if v is None:
                continue
            if k == "id" or (k == "name" and tag == "a"):
                self.ids.add(v)
            if tag in ("a", "link") and k == "href":
                self.refs.append(("href", v))
            if tag in ("img", "script") and k == "src":
                self.refs.append(("src", v))


cache: dict[Path, Collector] = {}


def parsed(path: Path) -> Collector:
    if path not in cache:
        c = Collector()
        c.feed(path.read_text(encoding="utf-8"))
        cache[path] = c
    return cache[path]


bad = 0
total = 0
for page in pages:
    c = parsed(page)
    for kind, ref in c.refs:
        if re.match(r"^(https?:|mailto:|data:|javascript:)", ref):
            continue
        total += 1
        target_part, _, frag = ref.partition("#")
        target = page if target_part == "" else (page.parent / target_part).resolve()
        if not target.exists():
            bad += 1
            print(f"MISSING {page.relative_to(root)} {kind}={ref}")
            continue
        if frag and target.suffix == ".html":
            if frag not in parsed(target).ids:
                bad += 1
                print(f"NO-ANCHOR {page.relative_to(root)} {kind}={ref}")
print(f"local references checked: {total}; problems: {bad}")
sys.exit(1 if bad else 0)
