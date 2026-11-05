"""Kill check for SC1 lab twins (round 12, slice a). Each mutant is one single-change copy of a twin, written to
ledgers/SC1/mutants/SC1-a-r12/. It is KILLED when its stdout under python -I -W error differs from the page's expected
block (the page text, html-unescaped). Lab twins are demonstrations (ruling), so this checks that the printed claims
change when the code changes. Usage: python -I lab_mutants_r12.py <checkout>"""
import html
import os
import re
import subprocess
import sys
import tempfile

root = sys.argv[1]
exe = sys.executable
mut_dir = os.path.join(root, "ledgers/SC1/mutants/SC1-a-r12")
MUTANTS = [
    ("m1-L01-covariance-max-index", "L01", "return sum(variances[: min(i, j)], Fraction(0))",
     "return sum(variances[: max(i, j)], Fraction(0))",
     "Lab 1 covariance sums increments up to max(i, j) instead of min(i, j)."),
    ("m2-L02-hat-peak-half", "L02", "return max(0.0, 1.0 - 2.0**m * abs(t - centre))",
     "return 0.5 * max(0.0, 1.0 - 2.0**m * abs(t - centre))",
     "Lab 2 hat peak is 1/2 instead of 1, so the grid supremum no longer equals the formula."),
    ("m3-L03-closed-form-h3", "L03", "return horizon**4 * (4 * steps * steps - 1) / (3 * steps**3)",
     "return horizon**3 * (4 * steps * steps - 1) / (3 * steps**3)",
     "Lab 3 closed form uses H cubed instead of H to the fourth; the exact-match column must print False."),
    ("m4-L03-mean-square-uses-n", "L03", "variance = sum((v - mean) ** 2 for v in values) / (n - 1)",
     "variance = sum((v - mean) ** 2 for v in values) / n",
     "Lab 3 sample variance divides by n instead of n - 1, so the printed se and z change."),
    ("m5-L02-bound-constant", "L02", "return math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)",
     "return math.sqrt(2 * m * math.log(2)) * 2 ** (-(m + 1) / 2)",
     "Lab 2 bound uses lambda_m = sqrt(2 m log 2) instead of sqrt(4 m log 2); the bound lines change."),
    ("m6-L01-dyadic-width-half-step", "L01", "    width = t / 2**n\n",
     "    width = t / 2**(n + 1)\n",
     "Lab 1 dyadic piece length t/2**(n+1) instead of t/2**n, so the variance sums print t/2."),
    ("m7-L02-grid-level-scale", "L02", "        scale = 2 ** (-(m + 1) / 2)\n        grid_sup",
     "        scale = 2 ** (-(m + 2) / 2)\n        grid_sup",
     "Lab 2 grid check uses a level scale off by a factor of root 2; the grid-supremum line prints False."),
    ("m8-L03-se-divisor-n-plus-1", "L03", "/ (n - 1)\n    return mean",
     "/ (n + 1)\n    return mean",
     "Lab 3 standard error divides the sample variance by n + 1; z for N = 2 changes."),
    ("m9-L03-exact-sum-drops-first-piece", "L03", "for a, b in pairwise(points)",
     "for a, b in pairwise(points[1:])",
     "Lab 3 exact s-squared sum drops the first interval; the closed-form match prints False."),
]
PAGE = {"L01": "course/modules/SC/SC1/L01.html", "L02": "course/modules/SC/SC1/L02.html",
        "L03": "course/modules/SC/SC1/L03.html"}
TWIN = {"L01": "tests/labs/SC1/lab-SC1-L01-1.py", "L02": "tests/labs/SC1/lab-SC1-L02-1.py",
        "L03": "tests/labs/SC1/lab-SC1-L03-1.py"}
expected = {}
for k, p in PAGE.items():
    page = open(os.path.join(root, p), encoding="utf-8").read()
    expected[k] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).rstrip("\n")
killed = 0
for name, lab, old, new, desc in MUTANTS:
    src = open(os.path.join(root, TWIN[lab]), encoding="utf-8").read()
    assert src.count(old) == 1, (name, src.count(old))
    mut_src = src.replace(old, new)
    path = os.path.join(mut_dir, f"{name}.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# Mutant {name} (SC1 lab {lab}): {desc}\n" + mut_src)
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run([exe, "-I", "-W", "error", path], cwd=scratch, capture_output=True, text=True)
    out = proc.stdout.rstrip("\n")
    is_killed = out != expected[lab] or proc.returncode != 0
    killed += is_killed
    first = next((i for i, (a, b) in enumerate(zip(expected[lab].splitlines(), out.splitlines())) if a != b), None)
    print(f"{name} KILLED={is_killed} rc={proc.returncode} stderr_bytes={len(proc.stderr)} first_diff_line={first}")
    if first is not None:
        print("   expected:", expected[lab].splitlines()[first])
        print("   got     :", out.splitlines()[first] if first < len(out.splitlines()) else "<none>")
print(f"killed {killed}/{len(MUTANTS)}")
