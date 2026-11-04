"""Whole-page scans of L07 and L08 for verifier round 1 (slice c).

Usage: python -I ledgers/SC1/scripts/SC1-c-r1/scan_r1.py   (run from the checkout root; reads only)
Prints: banned phrases and process words (BUILDER_RULES 1.3-1.4, plan 2.2), scope-word hits, macros used,
terms outside the prerequisite closure (plan section 4 D1-D10), dfn duplicates across SC1, claim spans,
data-cite markup, why-it-matters word counts, structure counts, cross-reference labels, and the T symbol.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SC1 = ROOT / "course/modules/SC/SC1"
PAGES = ["L07", "L08"]
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly",
]
PROCESS = ["builder", "verifier", "round", "REQUESTS", "unit report", "ledger"]
SCOPE = ["every", "all ", "always", "never", "only", "exactly", "same", "any", "everything", "almost surely"]
OUTSIDE = [
    "Itô", "Ito's", "geometric Brownian", "Ornstein", "SDE", "Euler", "Milstein", "Girsanov", "risk-neutral",
    "Feynman", "Kolmogorov", "Poisson", "Lévy", "barrier", "Donsker", "invariance principle", "iterated logarithm",
    "continuity correction", "estimator", "bridge", "Monte Carlo", "martingale", "filtration", "stopping time",
    "quadratic variation", "sigma-algebra", "Gaussian process", "transition density", "strong Markov",
]


def text_of(html_text: str) -> str:
    no_code = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', "", html_text, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", no_code))


def main() -> None:
    print("== banned phrases and process words (prose, lab code excluded)")
    for page in PAGES:
        raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
        prose = text_of(raw)
        hits = {w: len(re.findall(re.escape(w), prose, re.I)) for w in BANNED + PROCESS}
        hits["ellipsis (…)"] = prose.count("…")
        hits["three dots (...)"] = prose.count("...")
        print(page, {k: v for k, v in hits.items() if v})
    print("== scope words in prose (counts; each hit reviewed in the ledger)")
    for page in PAGES:
        prose = text_of((SC1 / f"{page}.html").read_text(encoding="utf-8"))
        print(page, {w.strip(): len(re.findall(r"\b" + re.escape(w.strip()) + r"\b", prose, re.I)) for w in SCOPE})
    print("== 'every result ... carries' and 'everything after' sentences")
    for page in PAGES:
        prose = text_of((SC1 / f"{page}.html").read_text(encoding="utf-8"))
        for pat in [r"Every result on this page[^.]*\.", r"everything after it[^.]*\.", r"same events[^.]*\."]:
            for m in re.finditer(pat, prose):
                print(page, "|", m.group(0)[:200])
    print("== terms outside the prerequisite closure (plan section 4)")
    for page in PAGES:
        prose = text_of((SC1 / f"{page}.html").read_text(encoding="utf-8"))
        found = {w: len(re.findall(re.escape(w), prose, re.I)) for w in OUTSIDE}
        print(page, {k: v for k, v in found.items() if v})
    print("== macros and symbols in math (registered: \\E \\Prob \\indic \\Phi ...)")
    for page in PAGES:
        raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
        maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
        macros = sorted({c for a, b in maths for c in re.findall(r"\\([A-Za-z]+)", a + b)})
        t_symbol = sorted({s.strip() for a, b in maths for s in re.findall(r"(?<![A-Za-z\\])T(?:_\{?\w+\}?)?", a + b)})
        print(page, "macros:", macros)
        print(page, "T symbol forms in math:", t_symbol)
    print("== dfn across SC1 lessons (same plain term defined twice?)")
    for f in sorted(SC1.glob("L0*.html")):
        for m in re.finditer(r"<dfn[^>]*>([^<]*)</dfn>", f.read_text(encoding="utf-8")):
            print(f.name, "|", m.group(1))
    print("== claim spans and data-cite markup (L07, L08)")
    for page in PAGES:
        raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
        print(page, "claim spans:", len(re.findall(r'class="[^"]*claim[^"]*"', raw)), "data-cite:", raw.count("data-cite"),
              "data-locator:", raw.count("data-locator"))
    print("== why-it-matters words (limit 120)")
    for page in PAGES:
        raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
        wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
        print(page, len(text_of(wim.group(1)).split()) if wim else "missing")
    print("== structure counts")
    for page in PAGES:
        raw = (SC1 / f"{page}.html").read_text(encoding="utf-8")
        items = len(re.findall(r'<li class="item"', raw))
        expl = len(re.findall(r'<div class="explain"', raw))
        misc = len(re.findall(r'<li class="misconception"', raw))
        solutions = len(re.findall(r'<details class="solution"', raw))
        tiers = {t: len(re.findall(rf'<div class="problem" id="{t}-\d"', raw)) for t in ["mech", "proof", "emp", "res"]}
        print(page, {"quiz items": items, "explanations": expl, "misconceptions": misc, "solutions": solutions,
                     "problems per tier": tiers, "data-hours": re.search(r'data-hours="(\d+)"', raw).group(1)})
    print("== cross-reference labels")
    checks = {
        "L06.html": ["Lemma 2.1", "Corollary 1.4", "Theorem 2.5", "Corollary 2.6", "first visit", "Proposition 2.3"],
        "L05.html": ["Assumption A3", "Assumption A4", "Assumption A3 is stated for bounded"],
        "L01.html": ["Definition 1.1", "tilde"],
    }
    for name, needles in checks.items():
        raw = html.unescape((SC1 / name).read_text(encoding="utf-8"))
        print(name, {n: raw.count(n) for n in needles})


if __name__ == "__main__":
    main()
