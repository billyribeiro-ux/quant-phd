# Round 3: page code vs twin, expected block vs twin stdout, lab 2 blanks; run from the checkout root.
# Run: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r3/page_vs_twin_r3.py
import difflib
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
page = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(codes), "expected blocks", len(expected))
assert len(codes) == 3 and len(expected) == 3
d = tempfile.mkdtemp(prefix="lx2c-r3-")
for n in (1, 2, 3):
    page_code = html.unescape(codes[n - 1])
    twin_path = os.path.join(ROOT, f"tests/labs/LX2/lab-LX2-project-{n}.py")
    twin = open(twin_path, encoding="utf-8").read()
    same = page_code == twin
    print(f"lab {n}: page code == twin: {same}")
    if not same:
        for line in difflib.unified_diff(twin.splitlines(), page_code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    # run the twin alone
    p = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True)
    exp = html.unescape(expected[n - 1]).strip()
    print(f"lab {n}: twin exit={p.returncode} stderr={p.stderr.strip()!r}")
    print(f"lab {n}: twin stdout == page expected block: {p.stdout.strip() == exp}")
    # run the page code as a file (the page's own code)
    pc = os.path.join(d, f"page_lab{n}.py")
    open(pc, "w", encoding="utf-8").write(page_code)
    q = subprocess.run([sys.executable, "-I", "-W", "error", pc], capture_output=True, text=True)
    print(f"lab {n}: page code run exit={q.returncode} stdout == expected: {q.stdout.strip() == exp}")
    # lab 2: fill the two blanks with the twin expressions and check
    if n == 2:
        fill = page_code.replace("hit_rate = ___", "hit_rate = Fraction(hits, horizon)").replace(
            "bias = ___", "bias = Fraction(sum(errors), horizon)")
        fp = os.path.join(d, "page_lab2_filled.py")
        open(fp, "w", encoding="utf-8").write(fill)
        r = subprocess.run([sys.executable, "-I", "-W", "error", fp], capture_output=True, text=True)
        print(f"lab 2 filled with twin expressions: exit={r.returncode} == expected: {r.stdout.strip() == exp}")
        print("lab 2 blank lines in page:", [ln for ln in page_code.splitlines() if "___" in ln])
