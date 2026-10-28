import subprocess, sys, pathlib
ROOT = pathlib.Path("/tmp/verify17-CF1-b")
PY = str(ROOT / ".venv/bin/python")
MUT = pathlib.Path("/tmp/cf1-v/CF1-b-r17/mut")
cases = [
    ("L04", "tests/labs/CF1/lab-CF1-L04-1.py", "    for i in range(steps + 1):\n", None),
    ("L04", "tests/labs/CF1/lab-CF1-L04-1.py", "PROJECT_P: tuple[int, ...] = (-10_000_000, 23_000_000, -13_200_000)", "PROJECT_P: tuple[int, ...] = (-10_000_000, 23_000_000, -13_100_000)"),
    ("L04", "tests/labs/CF1/lab-CF1-L04-1.py", "            roots.append(candidate)\n    return roots", "            roots.append(candidate)\n            break\n    return roots"),
    ("L04", "tests/labs/CF1/lab-CF1-L04-1.py", "    steps = round((GRID_HIGH - GRID_LOW) / GRID_STEP)", "    steps = round((GRID_HIGH - GRID_LOW) / GRID_STEP) - 1"),
    ("L03", "tests/labs/CF1/lab-CF1-L03-1.py", "    return [cf * (1.0 + inflation) ** t for t, cf in enumerate(real)]", "    return [cf * (1.0 + inflation) ** (t - 1 if t else 0) for t, cf in enumerate(real)]"),
    ("L03", "tests/labs/CF1/lab-CF1-L03-1.py", "if t >= 1)", "if t >= 0)"),
    ("L03", "tests/labs/CF1/lab-CF1-L03-1.py", "INFLATION_GRID = (0.0, 0.01, 0.03, 0.05)", "INFLATION_GRID = (0.0, 0.01, 0.03, 0.04)"),
    ("L03", "tests/labs/CF1/lab-CF1-L03-1.py", "    n = nominal_rate(REAL_RATE, INFLATION)", "    n = REAL_RATE + INFLATION"),
]
import re, html
for i, (lab, rel, old, new) in enumerate(cases):
    src = (ROOT / rel).read_text(encoding="utf-8")
    if new is None:
        new = old  # placeholder
    if old not in src:
        print(i, "PATTERN NOT FOUND", old[:50]); continue
    if i == 0:
        # control: unchanged copy must pass
        mutated = src
    else:
        mutated = src.replace(old, new, 1)
    f = MUT / f"mut{i:02d}_{lab}.py"
    f.write_text(mutated, encoding="utf-8")
    r = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True)
    page = ROOT / ("course/modules/CF/CF1/%s.html" % lab)
    s = page.read_text(encoding="utf-8")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)).strip().splitlines()
    got = r.stdout.strip().splitlines()
    status = "SURVIVES (output identical to expected)" if (r.returncode == 0 and got == exp) else "KILLED"
    print(i, lab, status, "rc", r.returncode, "|", (old.strip()[:45]), "->", (new.strip()[:60]))
