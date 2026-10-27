"""Round 28 check: each L07/L08 lab and solution snippet, run as its twin under python -I -W error (from a directory
holding data/ with the embedded snapshot), must (a) have page code identical to the twin and (b) print the page's
expected block token by token, numeric tokens within the page's data-tolerance. Usage (from the checkout):
  .venv/bin/python -I ledgers/S7/scripts/L07-L08-r28/compare_labs.py <work_dir_with_data> <stdout_dir>
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/tmp/verify-s7-r1-l78")
PAGES = {"L07": ROOT / "course/modules/S/S7/L07.html", "L08": ROOT / "course/modules/S/S7/L08.html"}
NUM = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?$")


def same(actual: str, expected: str, tol: float) -> bool:
    a, e = actual.split(), expected.split()
    if len(a) != len(e):
        return False
    return all(x == y or (NUM.match(x) and NUM.match(y) and abs(float(x) - float(y)) <= tol) for x, y in zip(a, e, strict=True))


def main() -> int:
    work, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    jobs: list[tuple[str, str, str, str, float]] = []  # (name, twin path, page key, expected text, tol)
    for key, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        for m in re.finditer(r'<section class="lab" id="(lab-S7-L0[78]-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', text, re.S):
            lab_id, code, tol, expected = m.group(1), html.unescape(m.group(2)), float(m.group(3)), html.unescape(m.group(4))
            twin = ROOT / "tests/labs/S7" / f"{lab_id}.py"
            jobs.append((lab_id, str(twin), key, expected, tol))
            if twin.read_text(encoding="utf-8").rstrip("\n") != code.rstrip("\n"):
                print(f"CODE DIFFERS from twin: {lab_id}")
                failures += 1
        for m in re.finditer(r'<code class="language-python" data-check="(sol-S7-L0[78]-E\d)">(.*?)</code></pre>\s*<pre class="expected" data-check="[^"]+" data-tolerance="([^"]+)">(.*?)</pre>', text, re.S):
            name, code, tol, expected = m.group(1), html.unescape(m.group(2)), float(m.group(3)), html.unescape(m.group(4))
            twin = ROOT / "tests/labs/S7" / f"{name}.py"
            jobs.append((name, str(twin), key, expected, tol))
            if twin.read_text(encoding="utf-8").rstrip("\n") != code.rstrip("\n"):
                print(f"CODE DIFFERS from twin: {name}")
                failures += 1
    for name, twin, key, expected, tol in jobs:
        t0 = time.perf_counter()
        proc = subprocess.run(
            [str(ROOT / ".venv/bin/python"), "-I", "-W", "error", twin],
            cwd=work, capture_output=True, text=True, timeout=300,
        )
        elapsed = time.perf_counter() - t0
        (out_dir / f"{name}.stdout.txt").write_text(proc.stdout, encoding="utf-8")
        ok = proc.returncode == 0 and proc.stderr == "" and same(proc.stdout, expected, tol)
        failures += 0 if ok else 1
        print(f"{name} page={key} exit={proc.returncode} stderr_bytes={len(proc.stderr)} tol={tol} match={ok} wall={elapsed:.2f}s")
    print(f"labs checked: {len(jobs)}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
