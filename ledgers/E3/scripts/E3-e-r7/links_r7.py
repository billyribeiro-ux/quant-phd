"""Check every local href/src in the E3 pages: target file exists and the #fragment id exists in it."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/E/E3"
ids_cache: dict[Path, set[str]] = {}


def ids(p: Path) -> set[str]:
    if p not in ids_cache:
        t = p.read_text(encoding="utf-8")
        ids_cache[p] = set(re.findall(r'\sid="([^"]+)"', t))
    return ids_cache[p]


bad = []
count = 0
for page in sorted(base.glob("*.html")):
    text = page.read_text(encoding="utf-8")
    for href in re.findall(r'\b(?:href|src)="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:", "javascript:")):
            bad.append((page.name, href, "EXTERNAL"))
            continue
        count += 1
        path_part, _, frag = href.partition("#")
        target = page if path_part == "" else (base / path_part).resolve()
        if not target.exists():
            bad.append((page.name, href, "missing file"))
            continue
        if frag and target.suffix == ".html" and frag not in ids(target):
            bad.append((page.name, href, "missing id"))
print("local references checked:", count, "| bad:", len(bad))
for b in bad:
    print(b)
