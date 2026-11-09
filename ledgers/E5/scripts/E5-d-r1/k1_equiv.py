"""Ruling 41 check: run the two moved percent-of-trend mutants and the log-gap reference against the page's lab-2 expected block."""
import glob, html, os, re, subprocess, sys, math, random
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "tools"))
from coursekit import compare_output
page = open(os.path.join(root, "course/modules/E/E5/project.html"), encoding="utf-8").read()
blocks = re.findall(r'<pre class="expected" data-tolerance="1e-6">(.*?)</pre>', page, re.S)
print("expected blocks found:", len(blocks))
exp = html.unescape(blocks[1])
print("EXPECTED lab2 block:"); print(exp)
for f in sorted(glob.glob(os.path.join(root, "ledgers/E5/equivalent/*.py"))):
    r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", f], capture_output=True, text=True, cwd="/tmp")
    ok, why = compare_output(r.stdout, exp, 1e-6) if r.returncode == 0 else (False, "exit %d %s" % (r.returncode, r.stderr[-300:]))
    print("PASSES_CHECK" if ok else "KILLED", os.path.relpath(f, root), why[:150])
    print("  stdout:", r.stdout.replace("\n", " | "))
# independent recomputation of the two candidate gaps at 2026 Q3
SEED, Q, W = 2026, 24, 20
rng = random.Random(SEED)
gdp = [20000.0]
for _ in range(Q - 1):
    gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
t_end = Q - 1; first = t_end - W + 1
xs = list(range(W)); ys = [math.log(gdp[first + k]) for k in range(W)]
mx = sum(xs) / W; my = sum(ys) / W
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
intercept = my - slope * mx
trend_log = intercept + slope * (W - 1)
print(f"log_gap_unrounded {100*(math.log(gdp[t_end]) - trend_log):.6f}")
print(f"pct_gap_unrounded {100*(gdp[t_end]/math.exp(trend_log) - 1):.6f}")
