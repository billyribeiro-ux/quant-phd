"""Round 4, slice e: text and link checks on course/modules/E/E3/project.html.

Prints: (1) banned strings and process words in visible text; (2) every href and its target (anchor ids, files,
fragments, concept dfn ids); (3) LaTeX commands and single-letter symbols in the math spans; (4) out-of-closure terms.
Usage: python3 -I project_checks.py <checkout>
"""
import html
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("pre", "script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("pre", "script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


root = Path(sys.argv[1]) / "course/modules/E/E3"
text = (root / "project.html").read_text(encoding="utf-8")

v = Visible()
v.feed(text)
visible = " ".join(v.parts)
print("== (1) banned strings and process words in visible prose")
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "build", "builder", "verifier", "batch", "planner", "architect", "fixer"]
for w in banned:
    hits = [m.start() for m in re.finditer(re.escape(w), visible, flags=re.I)]
    print(f"{w!r}: {len(hits)}")
print("round (whole word, visible):", len(re.findall(r"\bround\b", visible, flags=re.I)))

print("== (2) hrefs and targets")
ids = set(re.findall(r'\sid="([^"]+)"', text))
bad = 0
hrefs = re.findall(r'href="([^"]+)"', text)
for h in hrefs:
    if h.startswith("#"):
        ok = h[1:] in ids
    elif h.startswith("http"):
        ok = False
    else:
        f, _, frag = h.partition("#")
        p = os.path.normpath(os.path.join(root, f))
        ok = os.path.exists(p)
        if ok and frag:
            ok = ('id="%s"' % frag) in Path(p).read_text(encoding="utf-8")
    bad += not ok
    if not ok:
        print("BAD", h)
print("href count", len(hrefs), "bad", bad)
for m in re.finditer(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)"', text):
    cid, h = m.group(1), m.group(2)
    f, _, frag = h.partition("#")
    target = (root / f).read_text(encoding="utf-8")
    dfn = re.search(r'<dfn id="%s" data-concept="%s"' % (frag, cid), target) is not None
    print("concept", cid, h, "dfn present" if dfn else "DFN MISSING")

print("== (3) math commands and single-letter symbols in math spans")
spans = re.findall(r"\\\((.*?)\\\)", text, flags=re.S) + re.findall(r"\\\[(.*?)\\\]", text, flags=re.S)
cmds: dict[str, int] = {}
letters: dict[str, int] = {}
for s in spans:
    s = html.unescape(s)
    for c in re.findall(r"\\([A-Za-z]+)", s):
        cmds[c] = cmds.get(c, 0) + 1
    t = re.sub(r"\\[A-Za-z]+", "", s)
    for c in re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", t):
        letters[c] = letters.get(c, 0) + 1
print("spans", len(spans))
print("commands", sorted(cmds.items()))
print("letters", sorted(letters.items()))

print("== (4) out-of-closure and scope terms in visible prose")
for term in ["maximum likelihood", "Fisher", "confidence interval", "estimator", "convex", "concave", "Bellman",
             "risk-neutral", "equity premium", "martingale", "stochastic discount", "fixed point", "infinite horizon",
             "welfare", "market structure"]:
    print(f"{term!r}: {len(re.findall(re.escape(term), visible, flags=re.I))}")
