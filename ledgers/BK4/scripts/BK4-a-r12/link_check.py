"""Round 12 internal-link check for BK4 slice a: every href in index, L01-L03 resolves to a file and, when it has a
fragment, to an id in the target page. Usage: python3 -I link_check.py <checkout_root>"""

import os
import re
import sys

root = sys.argv[1]
base = os.path.join(root, "course/modules/BK/BK4")
pages = ["index.html", "L01.html", "L02.html", "L03.html"]


def ids_of(path: str) -> set[str]:
    return set(re.findall(r'\bid="([^"]+)"', open(path, encoding="utf-8").read()))


count = 0
bad: list[str] = []
for p in pages:
    src = os.path.join(base, p)
    for m in re.finditer(r'href="([^"]+)"', open(src, encoding="utf-8").read()):
        h = m.group(1)
        if h.startswith(("http:", "https:", "mailto:")):
            continue
        count += 1
        file, _, frag = h.partition("#")
        target = src if not file else os.path.normpath(os.path.join(os.path.dirname(src), file))
        if not os.path.exists(target):
            bad.append(f"{p}: {h} missing file")
            continue
        if frag and frag not in ids_of(target):
            bad.append(f"{p}: {h} missing id")
print("internal hrefs checked:", count, "bad:", len(bad))
for b in bad:
    print(b)
