"""Round-11 verifier: every href and data-concept link on the LX1 project page resolves (fragment ids exist in the
page or the target file; relative files exist). Argument 1 is the checkout root."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); page_path = root / "course/modules/LX/LX1/project.html"
page = page_path.read_text(encoding="utf-8")
ids_here = set(re.findall(r'\sid="([^"]+)"', page))
bad = []
hrefs = re.findall(r'href="([^"]+)"', page)
for h in hrefs:
    if h.startswith("http"):
        continue
    target, _, frag = h.partition("#")
    if target == "":
        if frag and frag not in ids_here:
            bad.append(("missing local id", h))
        continue
    f = (page_path.parent / target).resolve()
    if not f.exists():
        bad.append(("missing file", h))
        continue
    if frag:
        ids = set(re.findall(r'\sid="([^"]+)"', f.read_text(encoding="utf-8")))
        if frag not in ids:
            bad.append(("missing id in file", h))
print("hrefs:", len(hrefs), "problems:", bad)
