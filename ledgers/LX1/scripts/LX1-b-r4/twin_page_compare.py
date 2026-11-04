"""Round-4 verifier script for LX1-b: run each twin alone, compare page code block and expected block.

Does not import the twins. Usage: python -I -W error twin_page_compare.py <checkout> <scratch_root>
"""
import difflib
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
scratch = Path(sys.argv[2])
labs = [
    ("L03", "course/modules/LX/LX1/L03.html", "tests/labs/LX1/lab-LX1-L03-1.py"),
    ("L04", "course/modules/LX/LX1/L04.html", "tests/labs/LX1/lab-LX1-L04-1.py"),
]
py = str(checkout / ".venv" / "bin" / "python")
for tag, page, twin in labs:
    text = (checkout / page).read_text(encoding="utf-8")
    m = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    print(tag, "data-run blocks in page:", len(m))
    code = html.unescape(m[0])
    twin_text = (checkout / twin).read_text(encoding="utf-8")
    print(tag, "page code chars", len(code), "twin chars", len(twin_text), "exact identical:", code == twin_text,
          "rstrip identical:", code.rstrip() == twin_text.rstrip())
    if code.rstrip() != twin_text.rstrip():
        for line in difflib.unified_diff(twin_text.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print(line)
    run_dir = scratch / tag
    if run_dir.exists():
        shutil.rmtree(run_dir)
    (run_dir / "data").mkdir(parents=True)
    if tag == "L04":
        shutil.copy(checkout / "course/assets/data/market/fx_monthly.csv", run_dir / "data" / "fx_monthly.csv")
    res = subprocess.run([py, "-I", "-W", "error", str(checkout / twin)], cwd=run_dir, capture_output=True, text=True)
    print(tag, "twin alone exit", res.returncode, "stderr bytes", len(res.stderr.encode()), "stdout lines", len(res.stdout.splitlines()))
    (scratch / f"{tag}.twin.out").write_text(res.stdout, encoding="utf-8")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    exp_lines = expected.splitlines()
    out_lines = res.stdout.splitlines()
    print(tag, "expected lines", len(exp_lines), "output lines", len(out_lines), "line-for-line equal:", exp_lines == out_lines)
    for i, (a, b) in enumerate(zip(exp_lines, out_lines), 1):
        if a != b:
            print("  mismatch line", i, repr(a), repr(b))
