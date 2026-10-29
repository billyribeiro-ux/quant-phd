"""Build report/run_report.py as project.html line 207 specifies (Lab 3 with difference -> fd_derivative, the analytic
derivative -> sensitivities(instance)["dprice_dy"], unrounded price kept) and check that it prints the Lab 3 expected block.
Run: python report_from_spec.py <repo_root>"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/M/M2/project.html").read_text(encoding="utf-8")
m = re.search(r'id="lab-M2-project-3".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
lab = html.unescape(m.group(1))
expected = html.unescape(m.group(2)).rstrip()
grader = ROOT / "course/modules/M/M2/grader"
# the spec's replacements, applied to Lab 3's text
src = lab.replace('''def difference(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """A forward or central difference estimate of f'(x) with step h."""
    if scheme == "forward":
        return (f(x + h) - f(x)) / h
    if scheme == "backward":
        return (f(x) - f(x - h)) / h
    return (f(x + h) - f(x - h)) / (2 * h)''', '''from sensitivity_engine import fd_derivative as _fd, sensitivities as _sens


def difference(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """Calls to fd_derivative; the backward quotient is the forward quotient at x - h."""
    if scheme == "backward":
        return _fd(f, x - h, h, "forward")
    return _fd(f, x, h, scheme)''')
src = src.replace('exact = -sum(t * cash * v ** (t + 1) for t, cash in flows)',
                  'exact = _sens({"face_cents": face_cents, "coupon_bps": 600, "maturity_years": years, "yield_bps": 500})["dprice_dy"]')
assert "_sens(" in src and "_fd(" in src, "replacement did not apply"
with tempfile.TemporaryDirectory() as work:
    Path(work, "sensitivity_engine.py").write_text((grader / "reference.py").read_text(encoding="utf-8"), encoding="utf-8")
    Path(work, "run_report.py").write_text(src, encoding="utf-8")
    out = subprocess.run([sys.executable, "-W", "error", "run_report.py"], cwd=work, capture_output=True, text=True)
    print("exit", out.returncode, "stderr", out.stderr.strip()[:200])
    print("prints the Lab 3 expected block:", out.stdout.rstrip() == expected)
    if out.stdout.rstrip() != expected:
        print(out.stdout)
