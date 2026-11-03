"""Round-3 verifier script for M4 slice a: lab twins, page code and expected blocks.

Run as: python -I -W error ledgers/M4/scripts/M4-a-r3/m4a_r3_twins.py <repo_root>
For each lab L01..L04: (1) the twin tests/labs/M4/lab-M4-<L>-1.py runs alone under python -I -W error
from an empty scratch directory and exits 0 with empty stderr; (2) the page's data-run code equals the
twin (after html.unescape, trailing newline stripped); (3) the page's expected block equals the twin's stdout.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = ("L01", "L02", "L03", "L04")


def main(root: Path) -> int:
    failures = 0
    for lab in LABS:
        twin = root / "tests" / "labs" / "M4" / f"lab-M4-{lab}-1.py"
        page = (root / "course" / "modules" / "M" / "M4" / f"{lab}.html").read_text(encoding="utf-8")
        code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
        if code_m is None or exp_m is None:
            print(f"{lab}: missing code or expected block")
            failures += 1
            continue
        page_code = html.unescape(code_m.group(1)).rstrip("\n")
        page_exp = html.unescape(exp_m.group(1)).rstrip("\n")
        twin_text = twin.read_text(encoding="utf-8").rstrip("\n")
        with tempfile.TemporaryDirectory(prefix="m4a_r3_") as scratch:
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin.resolve())],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=120,
            )
        stdout = proc.stdout.rstrip("\n")
        code_eq = page_code == twin_text
        exp_eq = page_exp == stdout
        ok = proc.returncode == 0 and proc.stderr == "" and code_eq and exp_eq
        failures += 0 if ok else 1
        print(
            f"{lab}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr)} "
            f"page_code_equals_twin={code_eq} expected_equals_stdout={exp_eq} "
            f"stdout_lines={len(stdout.splitlines())} expected_lines={len(page_exp.splitlines())} "
            f"-> {'OK' if ok else 'MISMATCH'}"
        )
        if not exp_eq:
            for a, b in zip(page_exp.splitlines(), stdout.splitlines()):
                if a != b:
                    print(f"  first diff: page={a!r} stdout={b!r}")
                    break
    print("ALL OK" if failures == 0 else f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]).resolve()))
