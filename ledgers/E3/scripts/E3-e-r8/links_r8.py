"""Round-8: every local href on the E3 pages resolves to an existing file, and every fragment resolves to an id on that file.

Also checks every concept link (class="concept" data-concept=X, href=FILE#def-X) against a <dfn id="def-X"> on FILE.
Run: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/links_r8.py
"""

import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e")
E3 = ROOT / "course/modules/E/E3"
pages = sorted(E3.glob("*.html")) + [E3 / "grader/starter.py"]
ids: dict[pathlib.Path, set[str]] = {}
for page in pages:
    if page.suffix == ".html":
        ids[page.resolve()] = set(re.findall(r'\sid="([^"]+)"', page.read_text(encoding="utf-8")))

problems = []
count = 0
for page in sorted(E3.glob("*.html")):
    src = page.read_text(encoding="utf-8")
    for m in re.finditer(r'href="([^"]+)"', src):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            problems.append(f"{page.name}: external href {target}")
            continue
        count += 1
        path_part, _, frag = target.partition("#")
        dest = (page.parent / path_part).resolve() if path_part else page.resolve()
        if not dest.exists():
            problems.append(f"{page.name}: missing file {target}")
            continue
        if frag and dest.suffix == ".html":
            if dest not in ids:
                ids[dest] = set(re.findall(r'\sid="([^"]+)"', dest.read_text(encoding="utf-8")))
            if frag not in ids[dest]:
                problems.append(f"{page.name}: fragment #{frag} not an id in {dest.name}")
    for m in re.finditer(r'<a class="concept"[^>]*data-concept="([^"]+)"[^>]*href="([^"]+)"', src):
        concept, target = m.group(1), m.group(2)
        path_part, _, frag = target.partition("#")
        dest = (page.parent / path_part).resolve() if path_part else page.resolve()
        dest_src = dest.read_text(encoding="utf-8")
        if dest.name == "concepts.html":
            # program glossary: the anchor is the concept id itself
            if f'id="{frag}"' not in dest_src:
                problems.append(f"{page.name}: glossary anchor #{frag} not in concepts.html")
            continue
        if frag != f"def-{concept}":
            problems.append(f"{page.name}: concept {concept} link fragment {frag!r} in {dest.name}")
        if f'<dfn id="def-{concept}"' not in dest_src and f"<dfn id='def-{concept}'" not in dest_src:
            problems.append(f"{page.name}: concept {concept} has no <dfn id=def-{concept}> in {dest.name}")

print("local hrefs checked:", count)
print("problems:", len(problems))
for p in problems:
    print("  ", p)
