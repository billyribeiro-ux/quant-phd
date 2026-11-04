"""Static checks for the BK4 project slice (verifier BK4-c, round 2). Run from the checkout root.

Usage: .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/static_checks.py
Covers: banned strings (BUILDER_RULES 1.3-1.4), process words in learner text, bare notation symbols vs
notation/notation.json, anchors and relative links, concept markup (DAG), __tracebackhide__ per test, the Context
sentence count (BUILDER_RULES 5.2), and the 2**53 claim in the suite.
"""

from __future__ import annotations

import ast
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "course/modules/BK/BK4"
PAGE = (BASE / "project.html").read_text(encoding="utf-8")
SUITE_PATH = BASE / "grader/test_project.py"
SUITE = SUITE_PATH.read_text(encoding="utf-8")
LEARNER = [BASE / "project.html", *sorted((BASE / "grader").glob("*.py")), *sorted((ROOT / "tests/labs/BK4").glob("lab-BK4-project-*.py"))]

print("== banned strings and filler (BUILDER_RULES 1.3-1.4)")
banned = r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|in conclusion|let us|let's|we will see|\.\.\. "
hits = [f"{p.relative_to(ROOT)}:{i}" for p in LEARNER for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if re.search(banned, ln, re.I)]
print("hits:", hits)

print("== process words in learner text")
process = r"builder|verifier|planner|fixer|architect|ruling|\bround\b|ledger|fragment|\bQ[0-9]+\b|\bB[0-9]\b|FINAL|§|REFERENCE_REQUEST|DATA_REQUEST|honest-pending|atlas"
hits = [f"{p.relative_to(ROOT)}:{i}" for p in LEARNER for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if re.search(process, ln, re.I)]
print("hits:", hits)

print("== bare symbols vs notation/notation.json (registered: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q)")
text = html.unescape(re.sub(r"<[^>]+>", " ", PAGE))
code_syms = sorted(set(re.findall(r"<code>([^<]{1,12})</code>", PAGE)))
registered = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))["symbols"]
reg_syms = [s["symbol"] for s in registered]
print("registered symbols:", reg_syms)
print("page code tokens:", code_syms)
print("bare T in page text:", re.findall(r"\bT\b", text))

print("== anchors and relative links")
ids = set(re.findall(r'\sid="([^"]+)"', PAGE))
hrefs = re.findall(r'href="([^"]+)"', PAGE)
bad = []
for h in hrefs:
    if h.startswith("#"):
        if h[1:] not in ids:
            bad.append(h)
    else:
        path, _, frag = h.partition("#")
        target = (BASE / path).resolve()
        if not target.exists():
            bad.append(h)
print("links:", len(hrefs), "bad:", bad)

print("== concept markup (DAG)")
print("class=concept or dfn count:", len(re.findall(r'class="concept"|<dfn', PAGE)))

print("== __tracebackhide__ in every test")
tree = ast.parse(SUITE)
no_hide = [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_") and "__tracebackhide__" not in (ast.get_source_segment(SUITE, n) or "")]
print("tests without __tracebackhide__:", no_hide)

print("== Context sentence count (BUILDER_RULES 5.2: 2-4 sentences)")
m = re.search(r"<dt>Context</dt>\s*<dd>(.*?)</dd>", PAGE, re.S)
ctx = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
sents = [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", ctx.strip()) if x]
print("sentences:", len(sents))
for x in sents:
    print("  -", x[:100])

print("== the 2**53 claim in the suite")
for i, ln in enumerate(SUITE.splitlines(), 1):
    if "2**53" in ln:
        print(f"  test_project.py:{i}: {ln.strip()[:150]}")
print("  2**53 =", 2**53, "| largest value in the big case:", max(6_585_696_953_829_388, 6_692_931_089_932_558, 7_278_398_114_431_529), "| below 2**53:", max(6_585_696_953_829_388, 6_692_931_089_932_558, 7_278_398_114_431_529) < 2**53)
