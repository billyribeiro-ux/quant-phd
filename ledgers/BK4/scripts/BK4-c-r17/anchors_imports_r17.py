"""Round 17 (BK4 slice c): (1) every in-page anchor and local file link of project.html resolves; (2) imports of the
project lab twins are standard library only; (3) the project page's ids used by the rubric and exemplar hooks exist.
Usage: python -I anchors_imports_r17.py <checkout-root>"""
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
BK4 = ROOT / "course/modules/BK/BK4"
page = (BK4 / "project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'\sid="([^"]+)"', page))
bad = []
for href in re.findall(r'href="([^"]+)"', page):
    if href.startswith("#"):
        if href[1:] not in ids:
            bad.append(href)
    elif href.startswith(("http://", "https://", "mailto:")):
        bad.append(("external", href))
    else:
        target = (BK4 / href.split("#")[0]).resolve()
        if not target.exists():
            bad.append(href)
        elif "#" in href and href.split("#", 1)[1] not in (target.read_text(encoding="utf-8") if target.suffix == ".html" else ""):
            bad.append(href)
print("project.html anchors/links that do not resolve:", bad)
for crit in ("C1", "C2", "C3", "C4", "C5"):
    print(crit, "row present:", f'data-criterion="{crit}"' in page)
print("exemplar ids present:", "exemplar-a" in ids, "exemplar-b" in ids, "self-assessment" in ids)
for n in (1, 2, 3):
    src = (ROOT / f"tests/labs/BK4/lab-BK4-project-{n}.py").read_text(encoding="utf-8")
    mods = sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z_][\w.]*)", src, re.M)))
    print(f"twin {n} imports:", mods)
print("grader panel:", re.search(r'<section class="grader-panel"[^>]*>', page).group(0))
