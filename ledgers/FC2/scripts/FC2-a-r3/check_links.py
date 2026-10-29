"""Internal href targets and fragment ids for the FC2 slice pages (FC2-a r3). Usage: check_links.py <module dir>."""
import pathlib
import re
import sys

base = pathlib.Path(sys.argv[1]).resolve()
bad = []
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    text = (base / name).read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http", "mailto", "#")):
            continue
        path, _, frag = href.partition("#")
        target = (base / path).resolve() if path else (base / name).resolve()
        if not target.exists():
            bad.append((name, href, "missing file"))
            continue
        if frag and target.suffix == ".html" and f'id="{frag}"' not in target.read_text(encoding="utf-8"):
            bad.append((name, href, "missing id"))
print("problems:", bad or "none")
