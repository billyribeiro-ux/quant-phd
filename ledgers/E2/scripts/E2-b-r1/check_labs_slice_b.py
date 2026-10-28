"""E2 slice b verifier script: compare L04-L06 embedded lab code and expected output with their twins, and re-run twins.

Usage: <checkout>/.venv/bin/python -I <checkout>/ledgers/E2/scripts/E2-b-r1/check_labs_slice_b.py <checkout>
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
py = root / ".venv" / "bin" / "python"
for page in ("L04", "L05", "L06"):
    text = (root / "course/modules/E/E2" / f"{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert code_m and exp_m, page
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    lab_id = f"lab-E2-{page}-1"
    twin = (root / "tests/labs/E2" / f"{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    proc = subprocess.run(
        [str(py), "-I", "-W", "error", str(root / "tests/labs/E2" / f"{lab_id}.py")],
        capture_output=True,
        text=True,
        timeout=10,
    )
    same_out = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{page}: code_matches_twin={same_code} run_rc={proc.returncode} stderr_bytes={len(proc.stderr)} "
          f"stdout_matches_page_expected={same_out} lines={len(proc.stdout.splitlines())}")
    if not same_out:
        for i, (a, b) in enumerate(zip(proc.stdout.splitlines(), expected.splitlines())):
            if a != b:
                print(f"  first diff line {i}: run={a!r} page={b!r}")
                break
        print(f"  run lines {len(proc.stdout.splitlines())} page lines {len(expected.splitlines())}")
