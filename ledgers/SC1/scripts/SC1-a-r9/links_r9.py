"""SC1 slice a, round 9: every href and src in index.html, L01-L03 resolves; every fragment id exists in its target.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/links_r9.py
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
PAGES = [ROOT / "course/modules/SC/SC1" / p for p in ("index.html", "L01.html", "L02.html", "L03.html")]


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src"):
                self.refs.append(value)
            if name == "id":
                self.ids.add(value)


def parse(path: Path) -> Collector:
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


cache: dict[Path, Collector] = {}
problems = 0
total = 0
for page in PAGES:
    c = parse(page)
    cache[page.resolve()] = c
    for ref in c.refs:
        if ref.startswith(("http://", "https://", "mailto:")):
            print(f"EXTERNAL {page.name}: {ref}")
            problems += 1
            continue
        total += 1
        target_part, _, frag = ref.partition("#")
        target = page if target_part == "" else (page.parent / target_part).resolve()
        if not target.exists():
            print(f"MISSING FILE {page.name}: {ref}")
            problems += 1
            continue
        if frag:
            if target not in cache:
                cache[target] = parse(target)
            if frag not in cache[target].ids:
                print(f"MISSING ANCHOR {page.name}: {ref} (no id in {target.relative_to(ROOT)})")
                problems += 1
print(f"links checked: {total} problems: {problems}")
