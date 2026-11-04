"""Rung-2 instant check: run each candidate with python -I -W error, compare with the page's expected block using the labs.js compareOutput rule (whitespace tokens, numeric tolerance 1e-6 relative)."""
import glob, html, os, re, subprocess, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE5-LX2-c"
page = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)[1])
NUMBER = re.compile(r"^[-+]?\d+(\.\d+)?$")
def compare(actual, expected, tol=1e-6):
    a = actual.strip().split(); e = expected.strip().split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for i, (x, y) in enumerate(zip(a, e), 1):
        if NUMBER.match(x) and NUMBER.match(y):
            if not abs(float(x) - float(y)) <= tol * (1 + abs(float(y))):
                return False, f"token {i}: {x} vs {y}"
        elif x != y:
            return False, f"token {i}: {x!r} vs {y!r}"
    return True, ""
files = sys.argv[1:]
for f in files:
    p = subprocess.run([sys.executable, "-I", "-W", "error", f], capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        print(f"{os.path.basename(f)}: ERROR exit {p.returncode} {p.stderr.strip()[-120:]}")
        continue
    ok, why = compare(p.stdout, expected)
    print(f"{os.path.basename(f)}: {'PASSES (alternative)' if ok else 'KILLED'}{'' if ok else ' - ' + why}")
