"""Compare each BK4 slice-b lab twin with the page code block and the expected block.

Usage: python -I -W error twin_vs_page.py <checkout_root>
Prints one line per check. Exit 1 on any mismatch.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = {
    "lab-BK4-L04-1": root / "course/modules/BK/BK4/L04.html",
    "lab-BK4-L05-1": root / "course/modules/BK/BK4/L05.html",
}
ok = True
for lab_id, page in pages.items():
    text = page.read_text(encoding="utf-8")
    twin_path = root / "tests/labs" / "BK4" / f"{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_match = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(code_match.group(1))
    same_code = code == twin.rstrip("\n")  # tools/embed_labs.py:117 strips the final newline
    print(f"{lab_id}: page code block equals twin: {same_code} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same_code:
        ok = False
        for i, (a, b) in enumerate(zip(code.splitlines(), twin.splitlines())):
            if a != b:
                print(f"  first differing line {i + 1}: page={a!r} twin={b!r}")
                break
    exp_match = re.search(r'<pre class="expected" data-tolerance="[^"]*">(.*?)</pre>', text, re.S)
    expected = html.unescape(exp_match.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        capture_output=True,
        text=True,
        cwd="/tmp",
        check=False,
    )
    print(f"{lab_id}: twin exit code {run.returncode}, stderr bytes {len(run.stderr)}")
    same_out = run.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: expected block equals twin stdout: {same_out}")
    if not same_out:
        ok = False
        out_lines = run.stdout.rstrip("\n").splitlines()
        exp_lines = expected.rstrip("\n").splitlines()
        for i, (a, b) in enumerate(zip(exp_lines, out_lines)):
            if a != b:
                print(f"  first differing line {i + 1}: expected={a!r} output={b!r}")
                break
        print(f"  line counts: expected {len(exp_lines)} output {len(out_lines)}")
    if run.returncode != 0 or run.stderr:
        ok = False
        print(run.stderr)
print("ALL MATCH" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
