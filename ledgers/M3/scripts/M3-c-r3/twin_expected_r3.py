# Round-3 verifier script (slice c). Runs each L07-L09 twin ALONE under python -I -W error from an empty
# scratch directory, then compares stdout with the page's <pre class="expected"> block, and prints
# the twin's SHA-256 next to the one from the page's code block.
import hashlib, html, re, subprocess, sys, os
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PY = str(ROOT / ".venv/bin/python")
pages = {"07": "L07", "08": "L08", "09": "L09"}
for num, page in pages.items():
    twin = ROOT / f"tests/labs/M3/lab-M3-{page}-1.py"
    scratch = Path(f"/private/tmp/verifyD3-twin-{num}")
    for f in scratch.iterdir():
        f.unlink()
    res = subprocess.run([PY, "-I", "-W", "error", str(twin)], cwd=scratch, capture_output=True, text=True, timeout=120)
    text = (ROOT / f"course/modules/M/M3/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(m.group(1)).strip("\n") if m else None
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    page_code = html.unescape(code_m.group(1)) if code_m else None
    twin_src = twin.read_text(encoding="utf-8")
    print(f"== {page} twin={twin.name} exit={res.returncode} stderr_bytes={len(res.stderr.encode())}")
    print(f"   stdout==expected: {res.stdout.strip() == (expected or '').strip()}")
    print(f"   page code == twin (rstrip newline): {(page_code or '').rstrip() == twin_src.rstrip()}")
    print(f"   twin sha256: {hashlib.sha256(twin_src.encode()).hexdigest()[:16]}")
    print("   stdout:")
    for line in res.stdout.splitlines():
        print("     " + line)
