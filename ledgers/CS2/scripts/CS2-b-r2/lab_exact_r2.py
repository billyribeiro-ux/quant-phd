"""CS2 slice b, round 2: lab twins L05-L08, checked independently of tools/run_labs.py.

For each lesson page: the inline code block (unescaped) must equal the twin tests/labs/CS2/<lab-id>.py
(trailing newlines aside); the twin must run alone, under python -I -W error, in an empty scratch
directory, exit 0, write nothing to stderr; its stdout must equal the page's expected block exactly.
Usage: python -I -W error lab_exact_r2.py <checkout-root>
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGES = ["L05", "L06", "L07", "L08"]
CODE_RE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXP_RE = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)


def main() -> int:
    ok_all = True
    for page in PAGES:
        src = (ROOT / "course/modules/CS/CS2" / f"{page}.html").read_text(encoding="utf-8")
        codes = CODE_RE.findall(src)
        expects = EXP_RE.findall(src)
        if len(codes) != 1 or len(expects) != 1:
            print(f"{page}: expected one code block and one expected block, found {len(codes)} and {len(expects)}")
            ok_all = False
            continue
        page_code = html.unescape(codes[0]).rstrip("\n")
        expected = html.unescape(expects[0]).rstrip("\n")
        twin_path = ROOT / "tests/labs/CS2" / f"lab-CS2-{page}-1.py"
        twin = twin_path.read_text(encoding="utf-8").rstrip("\n")
        same = page_code == twin
        with tempfile.TemporaryDirectory() as scratch:
            started = time.perf_counter()
            result = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin_path)],
                capture_output=True,
                text=True,
                cwd=scratch,
                env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
                timeout=120,
                check=False,
            )
            elapsed = time.perf_counter() - started
            written = os.listdir(scratch)
        stdout_match = result.stdout.rstrip("\n") == expected
        top_level_main = bool(re.search(r"^main\(\)\s*$", twin, re.M))
        line = (
            f"{page}: page==twin {same}; exit {result.returncode}; stderr_empty {result.stderr == ''}; "
            f"stdout==expected {stdout_match}; top_level_main {top_level_main}; files_written {written}; "
            f"stdout_lines {len(result.stdout.splitlines())}; seconds {elapsed:.2f}"
        )
        print(line)
        if not (same and result.returncode == 0 and result.stderr == "" and stdout_match and top_level_main):
            ok_all = False
            if not stdout_match:
                print("---- diff: expected vs got")
                exp_lines = expected.splitlines()
                got_lines = result.stdout.rstrip("\n").splitlines()
                for i in range(max(len(exp_lines), len(got_lines))):
                    e = exp_lines[i] if i < len(exp_lines) else "<missing>"
                    g = got_lines[i] if i < len(got_lines) else "<missing>"
                    if e != g:
                        print(f"  line {i + 1}: expected {e!r} got {g!r}")
    print("ALL_OK" if ok_all else "FAILURES")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
