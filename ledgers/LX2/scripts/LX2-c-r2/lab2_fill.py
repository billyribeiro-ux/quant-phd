import html, re, subprocess, sys, tempfile, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX2-c"
page = open(f"{ROOT}/course/modules/LX/LX2/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[1]).strip()
template = html.unescape(blocks[1])
assert template.count("hit_rate = ___") == 1 and template.count("bias = ___") == 1
# (name, hit_rate expr, bias expr, expected verdict: pass|kill)
CASES = [
 ("alt-correct-fraction-explicit", "Fraction(hits, horizon)", "Fraction(sum(errors), horizon)", "pass"),
 ("alt-correct-float-division", "hits / horizon", "sum(errors) / horizon", "pass"),
 ("alt-correct-len-window", "Fraction(hits, len(REALISED))", "Fraction(sum(errors), len(errors))", "pass"),
 ("r2-bias-denominator-horizon-minus-1", "Fraction(hits, horizon)", "Fraction(sum(errors), horizon - 1)", "kill"),
 ("r2-bias-over-hit-count", "Fraction(hits, horizon)", "Fraction(sum(errors), hits)", "kill"),
 ("r2-bias-sum-of-hit-errors-only", "Fraction(hits, horizon)", "Fraction(sum(e for e in errors if abs(e) <= HIT_BAND), horizon)", "kill"),
 ("r2-one-sided-band-hit-rate", "Fraction(sum(1 for e in errors if e <= HIT_BAND), horizon)", "Fraction(sum(errors), horizon)", "kill"),
 ("r2-strict-band-hit-rate", "Fraction(sum(1 for e in errors if abs(e) < HIT_BAND), horizon)", "Fraction(sum(errors), horizon)", "kill"),
]
res = []
d = tempfile.mkdtemp(prefix="lx2c-r2-")  # scratch outside the checkout, not run from inside it
for name, hr, b, verdict in CASES:
    src = template.replace("hit_rate = ___", f"hit_rate = {hr}").replace("bias = ___", f"bias = {b}")
    path = os.path.join(d, name + ".py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    p = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True)
    out = p.stdout.strip()
    matches = out == expected and p.returncode == 0
    got = "pass" if matches else "kill"
    res.append((name, verdict, got, "OK" if got == verdict else "MISMATCH"))
    print(f"{name}: expected-verdict={verdict} observed={got} exit={p.returncode} "
          f"{'' if matches else '| last line: ' + (out.splitlines()[-1] if out else p.stderr.strip().splitlines()[-1])}")
print("ALL OK" if all(r[3] == "OK" for r in res) else "SOME MISMATCH")
