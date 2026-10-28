"""Round-5 verifier checks: docstring escapes, exemplar word counts, tail numbers, rounding claim, instance spec.

Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r5/r5_numeric_and_text_checks.py
"""

import ast
import html
import math
import re
import sys
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M4 = ROOT / "course/modules/M/M4"
sys.path.insert(0, str(M4 / "grader"))

# 1. non-raw docstrings whose text contains a backslash escape
for rel in ["grader/reference.py", "grader/instance.py", "../../../../tests/labs/M4/lab-M4-project-1.py"]:
    path = (M4 / rel).resolve()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        doc = ast.get_docstring(node, clean=False) if isinstance(node, (ast.Module, ast.FunctionDef)) else None
        if doc and "\t" in doc:
            i = doc.index("\t")
            print(f"TAB in docstring of {path.name} line-ish near: {doc[max(0, i - 12):i + 6]!r}")

# 2. exemplar A body word count under the page's rule (words are runs between spaces), headings included
t = (M4 / "project.html").read_text(encoding="utf-8")
art = re.search(r'<article class="exemplar" id="exemplar-a".*?</article>', t, re.S).group(0)
blocks = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
body = 0
for b in blocks:
    s = html.unescape(re.sub(r"<[^>]+>", " ", b))
    body += len(s.split())
print("exemplar A memo-text words, headings included:", body)
head = sum(len(html.unescape(re.sub(r"<[^>]+>", " ", h)).split()) for h in re.findall(r"<h5>(.*?)</h5>", art, re.S))
print("exemplar A headings words:", head, "| paragraphs only:", body - head)
sm = re.search(r"<h5>Summary</h5>\s*<p>(.*?)</p>", re.search(r'id="exemplar-b".*?</article>', t, re.S).group(0), re.S)
print("exemplar B summary words:", len(html.unescape(re.sub(r"<[^>]+>", " ", sm.group(1))).split()))

# 3. the t(3) tail at x = 1000 in high precision, against the printed 2.205308 and the limit 4 sqrt(3)/pi
getcontext().prec = 50
x = Decimal(1000)
s3 = Decimal(3).sqrt()
u = s3 / x
atan = sum(((-1) ** k) * u ** (2 * k + 1) / (2 * k + 1) for k in range(20))
pi = Decimal("3.14159265358979323846264338327950288419716939937510")
print("x^3 P(|V|>x) at x=1000, high precision:", round(x**3 * (Decimal(2) / pi) * (atan - s3 * x / (3 + x * x)), 9))
print("4 sqrt(3)/pi:", round(4 * s3 / pi, 7))

# 4. the normal and Cauchy tails at x = 10, and the ratio quoted in L10
pz = math.erfc(10 / math.sqrt(2))
pc = (2 / math.pi) * math.atan(0.1)
print(f"P(|Z|>10) = {pz:.6e}, P(|C|>10) = {pc:.6f}, 1/P(|C|>10) = {1 / pc:.2f}, ratio = {pc / pz:.4e}")

# 5. rounding versus truncation of 100 * 2% * Z, the claim in the grader comment (about 4+1/12 and about 2.7)
import random  # noqa: E402

rng = random.Random(0)
xs = [-2.0 * rng.gauss(0, 1) for _ in range(2_000_000)]
print("variance of round(loss):", round(sum(round(v) ** 2 for v in xs) / len(xs), 4), "vs 4 + 1/12 =", round(4 + 1 / 12, 4))
print("variance of trunc(loss):", round(sum(int(v) ** 2 for v in xs) / len(xs), 4))

# 6. instance spec over seeds 0-1999
from instance import make_instance  # noqa: E402

bad = []
for s in range(2000):
    d = make_instance(s)
    n = len(d["positions_cents"])
    ok = (
        all(100_000 <= w <= 5_000_000 for w in d["positions_cents"])
        and 3 <= d["nu"] <= 8
        and d["n_draws"] <= 19_987
        and d["n_draws"] % 100 != 0
        and all(d["cov"][i][j] == d["cov"][j][i] for i in range(n) for j in range(n))
    )
    if not ok:
        bad.append(s)
print("instance spec violations over seeds 0-1999:", len(bad))
