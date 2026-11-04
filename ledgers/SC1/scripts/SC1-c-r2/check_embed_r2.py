"""Verifier check (SC1-c round 2): page code equals the lab twin, expected block equals twin stdout,
and the twin runs alone under python -I -W error. Usage: check_embed_r2.py <repo-root>."""

from __future__ import annotations

import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
pages = {
    "L07": ("course/modules/SC/SC1/L07.html", "tests/labs/SC1/lab-SC1-L07-1.py"),
    "L08": ("course/modules/SC/SC1/L08.html", "tests/labs/SC1/lab-SC1-L08-1.py"),
}
for name, (page_rel, twin_rel) in pages.items():
    page = (root / page_rel).read_text(encoding="utf-8")
    twin = (root / twin_rel).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    print(f"{name}: page code chars={len(code)} twin chars={len(twin)} "
          f"equal_exact={code == twin} equal_mod_final_newline={code.rstrip(chr(10)) == twin.rstrip(chr(10))}")
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    e = re.search(r'<pre class="expected" data-tolerance="[^"]*">(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(root / twin_rel)],
                          capture_output=True, text=True, timeout=60)
    print(f"{name}: twin exit={proc.returncode} stderr_chars={len(proc.stderr)}")
    print(f"{name}: expected chars={len(expected)} stdout chars={len(proc.stdout)} "
          f"equal_exact={expected == proc.stdout} equal_mod_final_newline={expected.rstrip(chr(10)) == proc.stdout.rstrip(chr(10))}")
    if expected.rstrip("\n") != proc.stdout.rstrip("\n"):
        import difflib
        for line in list(difflib.unified_diff(proc.stdout.splitlines(), expected.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    out = root / "ledgers/SC1/scripts/SC1-c-r2/out" / f"twin_stdout_{name}.txt"
    out.write_text(proc.stdout, encoding="utf-8")
