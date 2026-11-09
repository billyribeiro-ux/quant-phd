"""Does the Rung 2 instant check (labs.js compareOutput, data-tolerance 1e-6) accept a wrong bound line?

Takes the page's Lab 2 code and expected block, fills the three blanks in several ways (correct and wrong),
runs each filled program under python -I -W error, and applies a Python port of labs.js compareOutput.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
page = (REPO / "course/modules/M/M5/project.html").read_text(encoding="utf-8")
sec = page[page.index('id="lab-M5-project-2"'):]
code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
expected = html.unescape(re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', sec, re.S).group(2))
tol = float(re.search(r'<pre class="expected" data-tolerance="([^"]+)">', sec, re.S).group(1))
NUMBER = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?%?$")

def compare(actual, expected, tolerance):
    a = actual.strip().split()
    e = expected.strip().split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for i, (x_s, y_s) in enumerate(zip(a, e), 1):
        if NUMBER.match(x_s) and NUMBER.match(y_s):
            if not abs(float(x_s.rstrip("%")) - float(y_s.rstrip("%"))) <= tolerance * (1 + abs(float(y_s.rstrip("%")))):
                return False, f"token {i}: {x_s} vs {y_s}"
        elif x_s != y_s:
            return False, f"token {i}: {x_s!r} vs {y_s!r}"
    return True, ""

ratio_expr = "sup_distance(bellman(v), bellman(w)) / sup_distance(v, w)"
variants = {
    "correct certified = BETA/(1-BETA)*change": ("BETA / (1 - BETA) * change",),
    "wrong: certified = last change (factor omitted)": ("change",),
    "wrong: certified = 2 * last change (factor 2 for 9)": ("2 * change",),
    "wrong: certified = 1.0 * change / (1 - BETA) * BETA**0": ("change / (1 - BETA)",),
}
ratio_good = ratio_expr
for name, (cert_expr,) in variants.items():
    src = code.replace("ratio = ___", f"ratio = {ratio_good}", 1).replace("certified = ___", f"certified = {cert_expr}", 1)
    assert "___" not in src, "blank left"
    path = Path("/tmp/m5d_r4/lab2_variant.py")
    path.write_text(src, encoding="utf-8")
    r = subprocess.run([str(REPO / ".venv/bin/python"), "-I", "-W", "error", str(path)], capture_output=True, text=True)
    ok, why = compare(r.stdout, expected, tol)
    print(f"{name}: run rc={r.returncode} | stdout: {' / '.join(r.stdout.strip().splitlines())} | instant check {'ACCEPTS' if ok else 'REJECTS'} {why}")
