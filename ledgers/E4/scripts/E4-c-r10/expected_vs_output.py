"""Round 10, slice E4-c: compare each page's expected block with the stdout of its twin run standalone (exact line equality)."""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/wt/verifyE10-E4-c")
PY = str(BASE / ".venv/bin/python")
ok = True
for lesson in ("L07", "L08", "L09"):
    src = (BASE / "course/modules/E/E4" / (lesson + ".html")).read_text(encoding="utf-8")
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [PY, "-I", "-W", "error", str(BASE / "tests/labs/E4" / ("lab-E4-" + lesson + "-1.py"))],
            cwd=scratch, capture_output=True, text=True, timeout=120,
        )
    got = proc.stdout.splitlines()
    expected = html.unescape(blocks[0]).strip("\n").splitlines() if blocks else []
    same = expected == got and proc.returncode == 0 and len(blocks) == 1
    ok = ok and same
    print(lesson, "expected blocks", len(blocks), "expected lines", len(expected), "stdout lines", len(got),
          "rc", proc.returncode, "identical", same)
    if not same:
        for i, (a, b) in enumerate(zip(expected, got)):
            if a != b:
                print("  first diff at", i, "expected:", a, "| got:", b)
                break
sys.exit(0 if ok else 1)
