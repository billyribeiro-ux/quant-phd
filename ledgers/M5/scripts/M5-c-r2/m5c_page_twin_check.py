"""Round-2 check for M5 slice c: page code equals twin; expected block equals twin output (stdout)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lid in ("L08", "L09", "L10"):
    page = (ROOT / f"course/modules/M/M5/{lid}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    page_code = html.unescape(code.group(1))
    exp = html.unescape(expected.group(1))
    twin_path = ROOT / f"tests/labs/M5/lab-M5-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(f"{lid}: page code len {len(page_code)} twin len {len(twin)} identical_after_strip={page_code.strip() == twin.strip()}")
    if page_code.strip() != twin.strip():
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), page_code.splitlines(), lineterm="", n=0):
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT)
    print(f"{lid}: twin exit {out.returncode} stderr_len {len(out.stderr)}")
    got = out.stdout.rstrip("\n").splitlines()
    want = exp.rstrip("\n").splitlines()
    print(f"{lid}: expected lines {len(want)} output lines {len(got)} exact_equal={got == want}")
    for g, w in zip(got, want):
        if g != w:
            print("   OUT:", g)
            print("   EXP:", w)
    # the expected block carries the same text, so compare the numeric tokens too
    print(f"{lid}: expected block has data-tolerance {re.search(r'data-tolerance=\"([^\"]+)\"', page).group(1)}")
