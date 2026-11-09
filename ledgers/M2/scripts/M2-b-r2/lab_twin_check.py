"""For each lab of slice b: the page's data-run code equals the twin byte for byte (after HTML unescape),
and the expected block equals the twin's printed output (run as python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L07": "lab-M2-L07-1", "L08": "lab-M2-L08-1", "L09": "lab-M2-L09-1",
         "L10": "lab-M2-L10-1", "L11": "lab-M2-L11-1", "L12": "lab-M2-L12-1"}
code_re = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
exp_re = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
for lesson, lab in PAGES.items():
    page = (ROOT / "course/modules/M/M2" / f"{lesson}.html").read_text(encoding="utf-8")
    twin = (ROOT / "tests/labs/M2" / f"{lab}.py").read_text(encoding="utf-8")
    codes = code_re.findall(page)
    exps = exp_re.findall(page)
    page_code = html.unescape(codes[0]) if codes else None
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/M2" / f"{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    printed = out.stdout
    exp_text = html.unescape(exps[0]) if exps else None
    same_code = page_code is not None and page_code.strip("\n") == twin.strip("\n")
    same_exp = exp_text is not None and exp_text.strip("\n") == printed.strip("\n")
    print(f"{lesson} {lab}: code_blocks={len(codes)} expected_blocks={len(exps)} "
          f"page_code_equals_twin={same_code} expected_equals_output={same_exp} "
          f"twin_exit={out.returncode} stderr_bytes={len(out.stderr)} twin_lines={twin.count(chr(10))}")
    if not same_code:
        print("  page code first diff at:", next((i for i, (a, b) in enumerate(zip(page_code.splitlines(), twin.splitlines())) if a != b), None))
    if not same_exp:
        print("  expected vs output first diff:", [ (a, b) for a, b in zip((exp_text or '').splitlines(), printed.splitlines()) if a != b][:2])
