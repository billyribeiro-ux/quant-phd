"""Run lab 2 candidate modules and compare stdout with the page's expected block under labs.js compareOutput rules.

Usage: python -I -W error harness_lab2_r8.py <file> [<file> ...]   (run from the checkout root)
Prints one line per file: KILLED/PASS-OK and the first differing token.
"""
import html
import re
import subprocess
import sys
import tempfile
import os

NUMBER = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")  # approximates labs.js NUMBER
src = open("course/modules/LX/LX2/project.html", encoding="utf-8").read()
m = re.search(r'<section class="lab completion" id="lab-LX2-project-2".*?<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', src, flags=re.S)
tol = float(m.group(1))
expected = html.unescape(m.group(2))


def compare(actual, exp, tolerance):
    a = actual.strip().split()
    e = exp.strip().split()
    if len(a) != len(e):
        return False, f"expected {len(e)} tokens, got {len(a)}"
    for i, (x, y) in enumerate(zip(a, e)):
        if NUMBER.match(x) and NUMBER.match(y):
            if not abs(float(x) - float(y)) <= tolerance * (1 + abs(float(y))):
                return False, f"token {i+1}: {x} vs {y}"
        elif x != y:
            return False, f"token {i+1}: {x!r} vs {y!r}"
    return True, ""


for path in sys.argv[1:]:
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", os.path.abspath(path)], cwd=d, capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or r.stderr.strip():
        print(f"{path}: KILLED (exit {r.returncode}, stderr {r.stderr.strip()[-120:]!r})")
        continue
    ok, why = compare(r.stdout, expected, tol)
    print(f"{path}: {'PASSES (survives)' if ok else 'KILLED'} {'' if ok else '- ' + why}")
