"""For each lesson L01-L09: run the lab twin under python -I -W error, then compare its stdout with the <pre class="expected"> block of the lesson page, and compare the code block of the page with the twin source."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for i in range(1, 10):
    lid = f"L{i:02d}"
    twin = root / "tests/labs/E4" / f"lab-E4-{lid}-1.py"
    page = (root / f"course/modules/E/E4/{lid}.html").read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=root
    )
    out = proc.stdout
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    exp = [html.unescape(re.sub(r"<[^>]+>", "", b)).strip() for b in blocks]
    actual = out.strip()
    match = any(e == actual for e in exp)
    code_blocks = re.findall(r"<pre>(.*?)</pre>", page, flags=re.S)
    twin_src = twin.read_text(encoding="utf-8").strip()
    code_match = any(html.unescape(re.sub(r"<[^>]+>", "", c)).strip() == twin_src for c in code_blocks)
    print(f"{lid}: exit={proc.returncode} stderr_bytes={len(proc.stderr)} expected_blocks={len(blocks)} "
          f"expected_matches_output={match} page_code_blocks={len(code_blocks)} page_code_equals_twin={code_match} "
          f"stdout_lines={len(out.splitlines())}")
    if not match:
        print("  first expected:", exp[0][:200].replace("\n", " | ") if exp else None)
        print("  actual:", actual[:200].replace("\n", " | "))
