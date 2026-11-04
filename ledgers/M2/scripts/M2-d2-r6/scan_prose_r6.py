"""Scan the visible prose of the L22-L24 pages and the slice cards for banned strings, process words,
scope words, unregistered macros and external references. Usage: python3 -I scan_prose_r6.py <repo-root>"""
import html
import json
import re
import sys
from html.parser import HTMLParser

root = sys.argv[1]


class Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style", "pre"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "pre") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…", "builder", "verifier", "round ", "fixed in", "corrected",
          "revision", "erratum", "previous draft", "Round ", "prerequisite calculus", "taken from", "roughly",
          "historically", "typically", "in practice", "small", "fast", "smooth", "most", "always", "every", "all ",
          "only", "any ", "same ", "exactly", "drives", "clearly", "obvious", "guarantee", "certainly"]
SCOPE = ["only", "all", "always", "every", "any", "same", "drives", "exactly", "small", "fast", "smooth", "most",
         "typically", "in practice", "guarantee", "guaranteed", "roughly", "about"]
pages = ["L22", "L23", "L24"]
out = []
for p in pages:
    path = f"{root}/course/modules/M/M2/{p}.html"
    raw = open(path, encoding="utf-8").read()
    v = Visible()
    v.feed(raw)
    text = html.unescape(" ".join(v.parts))
    text = re.sub(r"\s+", " ", text)
    out.append(f"== {p}: visible chars {len(text)}")
    for b in BANNED:
        for m in re.finditer(re.escape(b), text):
            out.append(f"  banned-or-process '{b}' at ~{m.start()}: ...{text[max(0,m.start()-70):m.start()+70]}...")
    for w in SCOPE:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", text, flags=re.I))
        out.append(f"  scope '{w}': {n}")
    for tok in ["http", "src=", "//cdn", "\\mathbb{", "\\Phi", "\\gamma", "R^\\ast", "R^{e", "R_f", "\\mathbb{Q}"]:
        if tok in raw:
            out.append(f"  raw token present: {tok} count {raw.count(tok)}")
    ext = re.findall(r'(?:src|href)="(https?:[^"]*)"', raw)
    out.append(f"  external src/href: {ext}")
# macros used in math
macros = set()
for p in pages:
    raw = open(f"{root}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    macros |= set(re.findall(r"\\[A-Za-z]+", raw))
out.append("== macros used across L22-L24 (raw html): " + " ".join(sorted(macros)))
nd = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
reg = set(nd["macros"].keys())
out.append("  unregistered macro names (excluding standard KaTeX/HTML names): " + " ".join(sorted(m for m in macros if m in ("\\mathbb", "\\operatorname") )))
out.append("  registered macros used: " + " ".join(sorted(m for m in macros if m in reg)))
print("\n".join(out))
