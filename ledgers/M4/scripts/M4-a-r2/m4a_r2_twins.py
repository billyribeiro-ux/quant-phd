"""Round-2 slice-a check: each lab page's data-run code equals its twin; each expected block equals twin stdout.

Run: .venv/bin/python ledgers/M4/scripts/M4-a-r2/m4a_r2_twins.py  (from the repository root)
The twin is executed as `python -I -W error <abs twin>` from an empty scratch directory.
"""

import html
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
PAGES = ["L01", "L02", "L03", "L04"]
RUN_RE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXP_RE = re.compile(r'<pre class="expected" data-tolerance="[^"]*">(.*?)</pre>', re.S)

ok = True
for lid in PAGES:
    page = (ROOT / "course/modules/M/M4" / f"{lid}.html").read_text(encoding="utf-8")
    runs = RUN_RE.findall(page)
    exps = EXP_RE.findall(page)
    twin_path = ROOT / "tests/labs/M4" / f"lab-M4-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = html.unescape(runs[0])
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{lid}: data-run blocks={len(runs)} expected blocks={len(exps)} page code == twin: {same}")
    if not same:
        ok = False
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin_path)],
            cwd=scratch, capture_output=True, text=True, timeout=120,
        )
    expected = html.unescape(exps[0])
    stdout_ok = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lid}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr)} stdout_lines={len(proc.stdout.splitlines())} "
          f"expected_lines={len(expected.splitlines())} stdout == expected: {stdout_ok}")
    if proc.returncode != 0 or proc.stderr:
        ok = False
        print(proc.stderr[:2000])
    if not stdout_ok:
        ok = False
        import difflib
        for line in list(difflib.unified_diff(expected.splitlines(), proc.stdout.splitlines(), "expected", "stdout", lineterm=""))[:40]:
            print("   ", line)
    print(f"--- {lid} stdout ---")
    print(proc.stdout)
print("ALL OK" if ok else "MISMATCH")
