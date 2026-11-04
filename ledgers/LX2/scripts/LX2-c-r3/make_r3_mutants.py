# Round 3: writes the new student-error mutants of the rung-2 completion problem as complete lab-2 programs
# under ledgers/LX2/mutants/. Each file is the page's own Lab 2 program with the two blanks filled by a student error.
# Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r3/make_r3_mutants.py
import html
import os
import re

ROOT = os.getcwd()
page = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
template = html.unescape(codes[1])
assert template.count("hit_rate = ___") == 1 and template.count("bias = ___") == 1

MUTANTS = [
    ("r3_lab2_hit_rate_as_percent",
     "Student error: hit rate printed as a percentage (hits / H times 100) where the page defines a share between 0 and 1.",
     "Fraction(hits, horizon) * 100", "Fraction(sum(errors), horizon)"),
    ("r3_lab2_bias_sign_reversed",
     "Student error: bias sign reversed (realised minus forecast) against the page's forecast-minus-realised convention.",
     "Fraction(hits, horizon)", "-Fraction(sum(errors), horizon)"),
    ("r3_lab2_hit_rate_rung1_length",
     "Student error: hit rate divided by 8, the length of rung 1's window, instead of H = 6 of this window.",
     "Fraction(hits, 8)", "Fraction(sum(errors), horizon)"),
    ("r3_lab2_bias_rung1_length",
     "Student error: bias divided by 8, the length of rung 1's window, instead of H = 6 of this window.",
     "Fraction(hits, horizon)", "Fraction(sum(errors), 8)"),
    ("r3_lab2_bias_adds_hit_count",
     "Student error: hit count added to the error sum before dividing by H (a sum over two different quantities).",
     "Fraction(hits, horizon)", "Fraction(sum(errors) + hits, horizon)"),
]
for name, first_line, hr, b in MUTANTS:
    src = template.replace("hit_rate = ___", f"hit_rate = {hr}").replace("bias = ___", f"bias = {b}")
    # the first docstring line describes the error (BUILDER / VERIFIER mutant format)
    assert src.startswith('"""LX2 project lab 2')
    src = '"""' + first_line + "\n\n" + src[3:]
    path = os.path.join(ROOT, "ledgers/LX2/mutants", name + ".py")
    open(path, "w", encoding="utf-8").write(src)
    print("wrote", os.path.relpath(path, ROOT))
