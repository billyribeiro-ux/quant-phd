"""Round-10 link check for E3 project.html: every href resolves (file exists; #anchor is an id in the target file)."""

import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).resolve()
text = page.read_text(encoding="utf-8")
ids_cache: dict[Path, set[str]] = {}


def ids_of(path: Path) -> set[str]:
    if path not in ids_cache:
        ids_cache[path] = set(re.findall(r'\bid="([^"]+)"', path.read_text(encoding="utf-8")))
    return ids_cache[path]


problems = 0
count = 0
for href in re.findall(r'href="([^"]+)"', text):
    count += 1
    if href.startswith(("http://", "https://", "mailto:")):
        print("EXTERNAL", href)
        problems += 1
        continue
    target, _, anchor = href.partition("#")
    path = page if target == "" else (page.parent / target).resolve()
    if not path.exists():
        print("MISSING FILE", href)
        problems += 1
        continue
    if anchor and anchor not in ids_of(path):
        print("MISSING ANCHOR", href)
        problems += 1
print(f"hrefs={count} problems={problems}")
