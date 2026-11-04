"""Compare each BK4-a lab twin with its page: the code block must equal the twin file, and the expected block must equal the twin's stdout.

Usage (repo root): python3 -I ledgers/BK4/scripts/BK4-a-r3/twin_vs_page.py
Runs each twin as python3 -I -W error and compares stdout with the page's <pre class="expected"> block (HTML unescaped).
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAIRS = {
    "L01": ("course/modules/BK/BK4/L01.html", "tests/labs/BK4/lab-BK4-L01-1.py", "lab-BK4-L01-1"),
    "L02": ("course/modules/BK/BK4/L02.html", "tests/labs/BK4/lab-BK4-L02-1.py", "lab-BK4-L02-1"),
    "L03": ("course/modules/BK/BK4/L03.html", "tests/labs/BK4/lab-BK4-L03-1.py", "lab-BK4-L03-1"),
}


def pre_blocks(text: str, kind: str) -> list[str]:
    if kind == "code":
        pat = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
    else:
        pat = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
    return [html.unescape(m) for m in pat.findall(text)]


def main() -> int:
    ok = True
    for lab, (page, twin, _lid) in PAIRS.items():
        ptxt = Path(page).read_text(encoding="utf-8")
        ttxt = Path(twin).read_text(encoding="utf-8")
        codes = pre_blocks(ptxt, "code")
        exp = pre_blocks(ptxt, "expected")
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, check=False
        )
        code_eq = any(c.strip() == ttxt.strip() for c in codes)
        exp_eq = any(e.strip() == run.stdout.strip() for e in exp)
        print(
            f"{lab}: twin exit {run.returncode}; stderr bytes {len(run.stderr.encode())}; "
            f"code blocks {len(codes)}, twin-equal {code_eq}; expected blocks {len(exp)}, output-equal {exp_eq}"
        )
        if run.returncode != 0 or not code_eq or not exp_eq:
            ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
