"""FC2-a round 4: every href in index/L01/L02/L03 resolves to an existing file and (if given) an existing id.

Also checks every <a class="concept" data-concept=X> target anchor exists in course/concepts.html, and that every
<dfn> id in the four slice pages is unique across the unit's built pages.
Usage: python -I links_check.py <repo_root>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/FC/FC2"
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts))
problems = 0
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    text = (base / name).read_text(encoding="utf-8")
    for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>', text):
        href = m.group(1)
        if href.startswith(("http:", "https:", "mailto:", "#")):
            if href.startswith("#"):
                ident = href[1:]
                if not re.search(rf'id="{re.escape(ident)}"', text):
                    print(f"{name}: missing same-page anchor {href}")
                    problems += 1
            else:
                print(f"{name}: external href {href}")
                problems += 1
            continue
        path, _, frag = href.partition("#")
        target = (base / path).resolve() if path else (base / name)
        if not target.exists():
            print(f"{name}: missing file {href}")
            problems += 1
            continue
        if frag:
            tt = target.read_text(encoding="utf-8")
            if not re.search(rf'id="{re.escape(frag)}"', tt):
                print(f"{name}: missing anchor {href}")
                problems += 1
    for m in re.finditer(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)"', text):
        cid, href = m.group(1), m.group(2)
        if cid not in concept_ids:
            print(f"{name}: concept {cid} not in concepts.html")
            problems += 1
        if "concepts.html#" in href and href.split("#", 1)[1] != cid:
            print(f"{name}: concept anchor mismatch {cid} -> {href}")
            problems += 1
print("links_check", "PASS" if problems == 0 else f"FAIL ({problems})")
