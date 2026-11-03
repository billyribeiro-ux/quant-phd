"""Link, anchor and resource check for the E3 project page and the lessons it cites (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/link_check.py   (run from the checkout root)
"""

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
PAGE = ROOT / "course/modules/E/E3/project.html"


class Collect(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is None:
                continue
            if key == "id":
                self.ids.add(value)
            if key in ("href", "src"):
                self.refs.append((key, value))
            if key == "name" and tag == "a":
                self.ids.add(value)


def collect(path: Path) -> Collect:
    c = Collect()
    c.feed(path.read_text(encoding="utf-8"))
    return c


page = collect(PAGE)
problems = []
for key, ref in page.refs:
    if re.match(r"^(https?:|mailto:|data:)", ref):
        problems.append(f"external reference {key}={ref}")
        continue
    target, _, frag = ref.partition("#")
    if target == "":
        if frag and frag not in page.ids:
            problems.append(f"missing anchor #{frag}")
        continue
    file = (PAGE.parent / target).resolve()
    if not file.exists():
        problems.append(f"missing file {target}")
        continue
    if frag:
        other = collect(file) if file.suffix == ".html" else None
        if other is not None and frag not in other.ids:
            problems.append(f"missing anchor {target}#{frag}")
print(f"project.html: {len(page.refs)} href/src attributes checked; problems: {len(problems)}")
for p in problems:
    print("  ", p)
figs = re.findall(r"<(svg|figure|img|canvas)\b", PAGE.read_text(encoding="utf-8"))
print("svg/figure/img/canvas elements on project.html:", len(figs))
for lesson in ("L02", "L03", "L06", "L07", "L08"):
    for ident in ("def-certainty-equivalent", "def-crra-utility", "def-prospect-theory", "def-loss-aversion"):
        f = ROOT / f"course/modules/E/E3/{lesson}.html"
        ids = collect(f).ids
        if ident in ids:
            print(f"{lesson}.html#{ident}: present")
