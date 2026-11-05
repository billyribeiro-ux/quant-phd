"""E4 slice a, round 11: structure, banned-phrase, notation-macro and concept-link scan for index, L01-L03.

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r11/structure_slice_a.py
Prints every measured quantity so that the ledger rows can cite the observed output.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E4 = ROOT / "course/modules/E/E4"
PAGES = {"index": E4 / "index.html", "L01": E4 / "L01.html", "L02": E4 / "L02.html", "L03": E4 / "L03.html"}
FAILS: list[str] = []


def ok(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


CODE_BLOCK = re.compile(r"<pre\b.*?</pre>", re.S)


def prose_html(html: str) -> str:
    """The page without its <pre> code and expected-output blocks: prose only."""
    return CODE_BLOCK.sub(" ", html)


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def text_of(html: str) -> str:
    t = Text()
    t.feed(html)
    return " ".join(t.parts)


BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "...", "…",  # matched in prose only (code blocks are stripped)
]
PROCESS = ["builder", "verifier", "round", "REQUESTS", "unit report", "planner", "fixer", "architect"]

macros_registered: set[str] = set()
nj = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
blob = json.dumps(nj)
for m in re.findall(r"\\\\([A-Za-z]+)", blob):
    macros_registered.add(m)

for name, path in PAGES.items():
    raw = path.read_text(encoding="utf-8")
    txt = text_of(prose_html(raw))
    words = len(re.findall(r"\S+", txt))
    print(f"{name}: visible-text words {words}")
    for b in BANNED:
        hits = [m.start() for m in re.finditer(re.escape(b), txt)]
        ok(not hits, f"{name}: banned string {b!r} absent (hits {len(hits)})")
    for w in PROCESS:
        hits = [m.start() for m in re.finditer(r"\b" + re.escape(w) + r"\b", txt, re.I)]
        ok(not hits, f"{name}: process word {w!r} absent (hits {len(hits)})")
    used = set(re.findall(r"\\([A-Za-z]+)", raw))  # all TeX control words on the page
    unregistered = sorted(u for u in used if u not in macros_registered and u not in {
        "begin", "end", "left", "right", "frac", "tfrac", "dfrac", "text", "mathrm", "ldots", "cdot", "ge", "le",
        "ne", "neq", "in", "quad", "qquad", "sum", "prod", "ln", "exp", "sqrt", "varepsilon", "lambda", "mu", "pi",
        "sigma", "rho", "alpha", "beta", "delta", "gamma", "bigl", "bigr", "infty", "iota", "bar", "tilde", "hat",
        "min", "max", "to", "partial", "leq", "geq", "log", "mathbb", "over", "lim", "int", "emptyset", "forall",
        "exists", "subset", "cup", "cap", "times", "pm", "mid", "Prob", "E", "R",
        "mapsto", "nabla", "zeta", "Omega", "approx", "psi", "theta"})
    print(f"{name}: TeX control words used not in notation.json macros nor standard set: {unregistered}")
    ok(len(unregistered) == 0, f"{name}: every TeX control word is a registered macro or a standard command")

# Why-it-matters word limit (BUILDER_RULES 4.2 item 1: at most 120 words)
for name in ("L01", "L02", "L03"):
    raw = PAGES[name].read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    n = len(re.findall(r"\S+", text_of(m.group(1))))
    print(f"{name}: why-it-matters words {n}")
    ok(n <= 120, f"{name}: why-it-matters at most 120 words ({n})")

# Problem solutions have at least 15 words each; tiers present with >=3 problems each
for name in ("L01", "L02", "L03"):
    raw = PAGES[name].read_text(encoding="utf-8")
    sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    short = [i for i, s in enumerate(sols) if len(re.findall(r"\S+", text_of(s))) < 15]
    ok(len(sols) >= 12 and not short, f"{name}: {len(sols)} solution blocks, short ones {short}")
    for tier in ("mechanics", "proof", "empirical", "research"):
        n = len(re.findall(r'data-tier="%s"' % tier, raw))
        block = re.search(r'data-tier="%s">(.*?)(?=<div class="tier"|</section>)' % tier, raw, re.S)
        count = len(re.findall(r'<div class="problem"', block.group(1))) if block else 0
        ok(count >= 3, f"{name}: tier {tier} has {count} problems")
    quiz = re.search(r'<section class="quiz".*?</section>', raw, re.S)
    qn = len(re.findall(r'<li class="item"', quiz.group(0))) if quiz else 0
    ok(8 <= qn <= 15, f"{name}: quiz items {qn}")
    mis = re.search(r'<section class="misconceptions".*?</section>', raw, re.S)
    mn = len(re.findall(r'<li class="misconception"', mis.group(0))) if mis else 0
    ok(mn >= 3, f"{name}: misconceptions {mn}")
    kr = len(re.findall(r"<tr><td>", raw))
    print(f"{name}: key-results rows {kr}")

# Concept links and definitions
concepts_html = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts_html))
dfn_seen: dict[str, str] = {}
for name, path in PAGES.items():
    raw = path.read_text(encoding="utf-8")
    for cid in re.findall(r'<a class="concept" data-concept="([^"]+)" href="\.\./\.\./\.\./concepts\.html#([^"]+)"', raw):
        ok(cid[0] == cid[1] and cid[1] in concept_ids, f"{name}: concept link {cid[0]} resolves in concepts.html")
    for did in re.findall(r'<dfn id="(def-[^"]+)" data-concept="([^"]+)"', raw):
        ok(did[0] == "def-" + did[1], f"{name}: dfn id {did[0]} matches data-concept {did[1]}")
        if did[1] in dfn_seen:
            ok(False, f"dfn {did[1]} defined twice ({dfn_seen[did[1]]} and {name})")
        else:
            dfn_seen[did[1]] = name
    for lid in re.findall(r'<a class="concept" data-concept="([^"]+)" href="(L0\d\.html)#def-([^"]+)"', raw):
        ok(lid[0] == lid[2], f"{name}: lesson link {lid[0]} -> {lid[1]} anchor matches")
print("dfn owners:", dfn_seen)
print("FAILS:", len(FAILS))
sys.exit(1 if FAILS else 0)
