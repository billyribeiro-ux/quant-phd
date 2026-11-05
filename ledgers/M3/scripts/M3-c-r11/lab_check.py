"""Round-11 M3 slice c: page code vs twin, expected block vs twin output, twin run under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD11-M3-c")
PY = str(ROOT / ".venv/bin/python")

for page in ("L07", "L08", "L09"):
    text = (ROOT / f"course/modules/M/M3/{page}.html").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="lab-M3-%s-1".*?</section>' % page, text, re.S)
    assert sec, page
    body = sec.group(0)
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (ROOT / f"tests/labs/M3/lab-M3-{page}-1.py").read_text(encoding="utf-8")
    print(f"{page}: page code == twin: {code.rstrip() == twin.rstrip()} (page {len(code)} chars, twin {len(twin)} chars)")
    if code.rstrip() != twin.rstrip():
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    # run the twin alone, isolated, warnings as errors
    res = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M3/lab-M3-{page}-1.py")],
                         capture_output=True, text=True, cwd="/Users/billyribeiro/.fanout/scratch-M3-c-r11")
    print(f"{page}: twin rc={res.returncode} stderr={res.stderr.strip()[:200]!r}")
    out = res.stdout
    print(f"{page}: expected block == twin output: {expected.strip() == out.strip()}")
    if expected.strip() != out.strip():
        import difflib
        for line in difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), "expected", "actual", lineterm=""):
            print("   ", line)
    print("---- output ----")
    print(out)
