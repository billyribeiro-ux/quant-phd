"""SC1 slice a, round 9: run the four round-8 lab mutants (not graded; information only) from an empty directory and compare
each printed output with its page's expected block. Run from the checkout root: .venv/bin/python -I <this file>.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
MUTANTS = ROOT / "ledgers/SC1/scripts/SC1-a-r8/lab_mutants"
for mutant in sorted(MUTANTS.glob("*.py")):
    lab = re.search(r"-(L0[1-3])-", mutant.name)
    assert lab is not None, mutant.name
    with tempfile.TemporaryDirectory(prefix="sc1r9mut-") as scratch:
        result = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(mutant)],
            cwd=scratch, capture_output=True, text=True, timeout=120, check=False,
            env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
        )
    page = (ROOT / f"course/modules/SC/SC1/{lab.group(1)}.html").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).rstrip("\n")  # type: ignore[union-attr]
    got = result.stdout.rstrip("\n")
    diff = sum(1 for a, b in zip(got.split("\n"), expected.split("\n")) if a != b) + abs(
        len(got.split("\n")) - len(expected.split("\n"))
    )
    print(f"{mutant.name}: exit={result.returncode} stderr_bytes={len(result.stderr)} equals_expected={got == expected} "
          f"differing_lines={diff}")
