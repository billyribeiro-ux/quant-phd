"""Builds report/run_report.py from Lab 3 by the spec's replacement rules, then runs it against the reference engine."""
import html, re, subprocess, sys
from pathlib import Path
page = Path(sys.argv[1]).read_text(encoding="utf-8")
ref_dir = Path(sys.argv[2])
out = Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
sec = re.search(r'<section class="lab" id="lab-M2-project-3".*?</section>', page, re.S).group(0)
code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).strip()
# 1. the difference function is replaced by fd_derivative (the backward quotient as forward at x - h)
code = re.sub(r'def difference\(.*?\n\n\n', '', code, flags=re.S)
code = re.sub(r'\bdifference\(', 'fd_derivative(', code)
code = code.replace("fd_derivative(kink, 0.3, 1e-3, 'backward')", 'fd_derivative(kink, 0.3 - 1e-3, 1e-3, "forward")')
code = code.replace('from collections.abc import Callable\n',
  'from collections.abc import Callable\nfrom sensitivity_engine import fd_derivative, sensitivities\n')
code = code.replace('difference(kink, 0.3, 1e-3, \'backward\')', 'fd_derivative(kink, 0.3 - 1e-3, 1e-3, "forward")')
# 2. the analytic exact comes from sensitivities
code = code.replace('exact = -sum(t * cash * v ** (t + 1) for t, cash in flows)',
  'exact = sensitivities({"face_cents": face_cents, "coupon_bps": 600, "maturity_years": years, "yield_bps": 500})["dprice_dy"]')
(out / "run_report.py").write_text(code, encoding="utf-8")
(out / "sensitivity_engine.py").write_text(Path(sys.argv[4]).read_text(encoding="utf-8"), encoding="utf-8")
run = subprocess.run([sys.executable, "-W", "error", str(out / "run_report.py")], capture_output=True, text=True, cwd=str(out))
print("rc", run.returncode, run.stderr[-400:])
print("residual 'difference(' calls:", len(re.findall(r'\bdifference\(', code)), "| 'backward' left:", "'backward'" in code)
print("stdout == Lab 3 expected:", run.stdout.strip() == exp)
if run.stdout.strip() != exp:
    import difflib
    print("\n".join(difflib.unified_diff(exp.splitlines(), run.stdout.strip().splitlines(), "expected", "got", lineterm="")))
