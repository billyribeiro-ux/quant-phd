"""Round-6 BK4 slice a: every href/src of index, L01, L02, L03 resolves to an existing file, and every fragment
resolves to an id in the target file. Usage: python3 -I links_a_r6.py <checkout root>"""
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/BK/BK4"
ids_cache: dict[Path, set[str]] = {}


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):  # type: ignore[override]
        for k, v in attrs:
            if k == "id" and v:
                self.ids.add(v)
            if k in ("href", "src") and v:
                self.refs.append((k, v))


def parse(path: Path) -> P:
    p = P()
    p.feed(path.read_text(encoding="utf-8"))
    return p


problems = 0
total = 0
for page in ("index.html", "L01.html", "L02.html", "L03.html"):
    src = base / page
    p = parse(src)
    for kind, ref in p.refs:
        total += 1
        if re.match(r"^(https?:|mailto:|data:)", ref):
            print(page, kind, ref, "EXTERNAL")
            problems += 1
            continue
        target, _, frag = ref.partition("#")
        tpath = src if target == "" else (src.parent / target).resolve()
        if not tpath.exists():
            print(page, kind, ref, "MISSING FILE")
            problems += 1
            continue
        if frag:
            if tpath not in ids_cache:
                ids_cache[tpath] = parse(tpath).ids if tpath.suffix == ".html" else set()
            if frag not in ids_cache[tpath]:
                print(page, kind, ref, "MISSING FRAGMENT in", tpath.relative_to(root))
                problems += 1
print("links checked:", total, "problems:", problems)
