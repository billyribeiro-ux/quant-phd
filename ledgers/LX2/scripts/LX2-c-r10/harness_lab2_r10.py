"""Run lab 2 candidate modules; compare stdout with the page's expected block under labs.js compareOutput rules.
Usage (from checkout root): python -I -W error harness_lab2_r9.py <file> ...  Prints KILLED/SURVIVES per file."""
import html, os, re, subprocess, sys, tempfile
NUMBER = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?%?$")  # labs.js line 16
src = open("course/modules/LX/LX2/project.html", encoding="utf-8").read()
m = re.search(r'<section class="lab completion" id="lab-LX2-project-2".*?<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', src, re.S)
tol = float(m.group(1)); expected = html.unescape(m.group(2))
def num(s): return float(s[:-1]) if s.endswith("%") else float(s)
def compare(actual, exp):
    a = actual.strip().split(); e = exp.strip().split()
    if len(a) != len(e): return False, f"tokens {len(e)} vs {len(a)}"
    for i, (x, y) in enumerate(zip(a, e)):
        if NUMBER.match(y) and NUMBER.match(x):
            if not abs(num(x) - num(y)) <= tol * (1 + abs(num(y))): return False, f"token {i+1}: {x} vs {y}"
        elif x != y: return False, f"token {i+1}: {x!r} vs {y!r}"
    return True, ""
for path in sys.argv[1:]:
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", os.path.abspath(path)], cwd=d, capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or r.stderr.strip():
        print(f"KILLED(crash) {os.path.basename(path)}: exit {r.returncode}"); continue
    ok, why = compare(r.stdout, expected)
    print(f"{'SURVIVES' if ok else 'KILLED  '} {os.path.basename(path)}" + ("" if ok else f" - {why}"))
