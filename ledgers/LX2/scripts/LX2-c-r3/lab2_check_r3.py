# Round 3: lab 2 instant-check experiments. Fills the page's own Lab 2 template with candidate expressions,
# runs each candidate alone under python -I -W error, and compares the whole stdout with the page expected block.
# Also compares every existing ledgers/LX2/mutants lab-2 fixture (whole block and header line) with that block.
# Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r3/lab2_check_r3.py
import glob
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
page = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[1]).strip()
template = html.unescape(codes[1])
assert template.count("hit_rate = ___") == 1 and template.count("bias = ___") == 1
header = expected.splitlines()[0]
print("page lab 2 header:", header)

CASES = [
    # alternatives that are correct: must PASS
    ("alt-correct-fraction-explicit", "Fraction(hits, horizon)", "Fraction(sum(errors), horizon)", "pass"),
    ("alt-correct-float-division", "hits / horizon", "sum(errors) / horizon", "pass"),
    ("alt-correct-len-window", "Fraction(hits, len(REALISED))", "Fraction(sum(errors), len(errors))", "pass"),
    ("alt-correct-count-from-errors", "Fraction(sum(1 for e in errors if abs(e) <= HIT_BAND), horizon)",
     "Fraction(sum(errors), len(errors))", "pass"),
    ("alt-correct-bias-as-fraction-of-int", "Fraction(hits, horizon)", "Fraction(1 * sum(errors), horizon)", "pass"),
    # existing round-2 student-error mutants: must be KILLED
    ("r2-bias-denominator-horizon-minus-1", "Fraction(hits, horizon)", "Fraction(sum(errors), horizon - 1)", "kill"),
    ("r2-bias-over-hit-count", "Fraction(hits, horizon)", "Fraction(sum(errors), hits)", "kill"),
    ("r2-bias-sum-of-hit-errors-only", "Fraction(hits, horizon)",
     "Fraction(sum(e for e in errors if abs(e) <= HIT_BAND), horizon)", "kill"),
    ("r2-one-sided-band-hit-rate", "Fraction(sum(1 for e in errors if e <= HIT_BAND), horizon)",
     "Fraction(sum(errors), horizon)", "kill"),
    ("r2-strict-band-hit-rate", "Fraction(sum(1 for e in errors if abs(e) < HIT_BAND), horizon)",
     "Fraction(sum(errors), horizon)", "kill"),
    # new round-3 student-error mutants: must be KILLED
    ("r3-hit-rate-as-percent", "Fraction(hits, horizon) * 100", "Fraction(sum(errors), horizon)", "kill"),
    ("r3-bias-sign-reversed", "Fraction(hits, horizon)", "-Fraction(sum(errors), horizon)", "kill"),
    ("r3-hit-rate-over-rung1-length", "Fraction(hits, 8)", "Fraction(sum(errors), horizon)", "kill"),
    ("r3-bias-over-rung1-length", "Fraction(hits, horizon)", "Fraction(sum(errors), 8)", "kill"),
    ("r3-bias-mean-of-hit-count-and-horizon", "Fraction(hits, horizon)",
     "Fraction(sum(errors) + hits, horizon)", "kill"),
]
res = []
d = tempfile.mkdtemp(prefix="lx2c-r3-")
for name, hr, b, verdict in CASES:
    src = template.replace("hit_rate = ___", f"hit_rate = {hr}").replace("bias = ___", f"bias = {b}")
    path = os.path.join(d, name + ".py")
    open(path, "w", encoding="utf-8").write(src)
    p = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True)
    matches = p.stdout.strip() == expected and p.returncode == 0
    got = "pass" if matches else "kill"
    res.append((name, verdict, got))
    print(f"{name}: expected={verdict} observed={got} exit={p.returncode}")

print("--- existing fixtures in ledgers/LX2/mutants (whole block vs page block; header line)")
for path in sorted(glob.glob(os.path.join(ROOT, "ledgers/LX2/mutants/*lab2*.py"))):
    p = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True)
    out = p.stdout.strip()
    ol = out.splitlines()
    el = expected.splitlines()
    body_diff = [i + 1 for i, (a, b) in enumerate(zip(ol, el)) if a != b and i > 0]
    print(f"{os.path.basename(path)}: exit={p.returncode} whole_block_match={out == expected} "
          f"header_match={bool(ol) and ol[0] == header} body_differing_lines={body_diff} "
          f"lines_out={len(ol)} lines_expected={len(el)}")

ok = all((verdict == got) for _, verdict, got in res)
print("ALL CANDIDATES AS EXPECTED" if ok else "MISMATCH")
