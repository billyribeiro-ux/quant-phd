"""Round-3 check: page lab code equals twin; page expected block equals twin stdout (run in -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page_dir = root / "course/modules/E/E1"
for lab in ("L07", "L08", "L09"):
    page = (page_dir / f"{lab}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/E1/lab-E1-{lab}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    code_ok = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp", check=False
    ).stdout
    exp_ok = expected.rstrip("\n") == out.rstrip("\n")
    print(f"{lab}: code_equals_twin={code_ok} expected_equals_output={exp_ok} "
          f"code_lines={len(code.splitlines())} expected_lines={len(expected.splitlines())} "
          f"page_code_offset={m.start()} expected_offset={e.start()}")
    if not exp_ok:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
    if not code_ok:
        import difflib
        print("\n".join(list(difflib.unified_diff(code.splitlines(), twin.splitlines(), lineterm=""))[:60]))
