"""Link, banned-phrase, process-word and lab-twin scan for the FC2 slice (verifier, round 1).

Run: python -I ledgers/FC2/scripts/FC2-a-r1/page_scan.py <checkout-root>
Checks: every relative href resolves (and concepts.html anchors exist); dfn ids; banned phrases of
BUILDER_RULES 1 (TODO, TBD, lorem, for brevity, ..., studies show, ...); 'about <digit>'; each lab's
page code equals its twin.
"""
import html
import os
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page_dir = root / "course/modules/FC/FC2"
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts))
broken = []
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    f = page_dir / name
    t = f.read_text(encoding="utf-8")
    own_ids = set(re.findall(r'id="([^"]+)"', t))
    for href in re.findall(r'href="([^"]+)"', t):
        if href.startswith("#"):
            if href[1:] not in own_ids:
                broken.append((name, href))
            continue
        path, _, frag = href.partition("#")
        full = Path(os.path.normpath(f.parent / path))
        if not full.exists():
            broken.append((name, href, "missing file"))
            continue
        if frag:
            if full.name == "concepts.html":
                if frag not in concept_ids:
                    broken.append((name, href, "no concept anchor"))
            elif frag not in set(re.findall(r'id="([^"]+)"', full.read_text(encoding="utf-8"))):
                broken.append((name, href, "no anchor in target"))
print("broken links:", broken if broken else "none")

pats = ["TODO", "TBD", "lorem", "...", "…", "for brevity", "details omitted", "beyond the scope",
        "left as an exercise", "you can add more", "it is important to note", "studies show",
        "experts agree", "it is well known", "obviously", "clearly", "motivat", "let us", "we will see",
        "interestingly", "importantly", "roughly", "historically", "significant", "robust", "of course",
        "in fact", "it can be shown", "it is easy", "builder", "planner", "architect", "verifier",
        "ledger", "mutant", "fixture", "orchestrat", "placeholder"]
for name in ["index.html", "L01.html", "L02.html", "L03.html", "cards.json"]:
    t = (page_dir / name).read_text(encoding="utf-8")
    for p in pats:
        for m in re.finditer(re.escape(p), t, flags=re.I):
            print("phrase hit:", name, repr(p), "|", t[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
    for m in re.finditer(r"\babout \d", t):
        print("about-digit:", name, "|", t[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
print("dfn ids:", re.findall(r'<dfn id="([^"]+)"', "".join((page_dir / n).read_text(encoding="utf-8") for n in ["L01.html", "L02.html", "L03.html"])))

for n in (1, 2, 3):
    page = (page_dir / f"L0{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-FC2-L0%d-1".*?<code class="language-python" data-run>(.*?)</code></pre>' % n, page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/FC2/lab-FC2-L0{n}-1.py").read_text(encoding="utf-8")
    print(f"L0{n} page code == twin (trailing newline ignored):", code.rstrip("\n") == twin.rstrip("\n"))
