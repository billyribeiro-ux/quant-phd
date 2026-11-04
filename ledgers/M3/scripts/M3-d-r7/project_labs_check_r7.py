"""Round-7 verifier (slice d): for each M3 project lab, (1) the page code block equals its twin (trailing newlines aside),
(2) the twin runs under python -I -W error with no stderr and exit 0, (3) stdout equals the page's expected block
(numbers within 1e-6, other tokens exact). Usage: .venv/bin/python -I <this file>."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/M/M3/project.html").read_text(encoding="utf-8")
for lab in ("lab-M3-project-1", "lab-M3-project-2", "lab-M3-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="' + lab + r'".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_path = ROOT / "tests/labs/M3" / f"{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/private/tmp")
    got = res.stdout.splitlines()
    exp = expected.rstrip("\n").splitlines()
    ok = len(got) == len(exp)
    bad = []
    if ok:
        for g, e in zip(got, exp, strict=True):
            gt, et = g.split(), e.split()
            if len(gt) != len(et):
                bad.append((g, e))
                continue
            for a, b in zip(gt, et, strict=True):
                try:
                    fa, fb = float(a), float(b)
                    if abs(fa - fb) > 1e-6 * (1 + abs(fb)):
                        bad.append((g, e))
                        break
                except ValueError:
                    if a != b:
                        bad.append((g, e))
                        break
    print(f"{lab}: page code == twin: {same}; twin exit {res.returncode}; stderr bytes {len(res.stderr)}; "
          f"lines got {len(got)} expected {len(exp)}; mismatching lines {len(bad)}")
    for g, e in bad[:5]:
        print("   got:", g, "| expected:", e)
