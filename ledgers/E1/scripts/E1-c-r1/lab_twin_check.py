"""Round-1 slice c check: each L07-L09 lab page code equals its twin, the expected block equals the twin's output,
and the twin runs alone under python -I -W error with no warnings.

Usage: .venv/bin/python -I ledgers/E1/scripts/E1-c-r1/lab_twin_check.py  (run from the checkout root)
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["L07", "L08", "L09"]
PY = sys.executable


def sections(page_text: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for m in re.finditer(r'<section class="lab" id="(lab-E1-[^"]+)".*?</section>', page_text, re.S):
        block = m.group(0)
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', block, re.S)
        exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S)
        out.append((m.group(1), html.unescape(code.group(1)) if code else "", html.unescape(exp.group(1)) if exp else ""))
    return out


def main() -> int:
    ok = True
    for page in PAGES:
        text = (ROOT / f"course/modules/E/E1/{page}.html").read_text(encoding="utf-8")
        for lab_id, code, expected in sections(text):
            n = lab_id.rsplit("-", 1)[1]
            twin = ROOT / f"tests/labs/E1/lab-E1-{page}-{n}.py"
            twin_src = twin.read_text(encoding="utf-8")
            code_eq = code.strip("\n") == twin_src.strip("\n")
            run = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=ROOT)
            out = run.stdout
            exp_eq = expected.strip("\n") == out.strip("\n")
            print(f"{lab_id}: twin={twin.name} page_code_equals_twin={code_eq} exit={run.returncode} "
                  f"stderr_bytes={len(run.stderr)} expected_equals_output={exp_eq} lines={len(out.splitlines())}")
            if not (code_eq and exp_eq and run.returncode == 0 and not run.stderr):
                ok = False
                if not code_eq:
                    print("  code mismatch")
                if not exp_eq:
                    print("  expected mismatch; first differing lines:")
                    for a, b in zip(expected.splitlines(), out.splitlines()):
                        if a != b:
                            print("   page :", a)
                            print("   twin :", b)
                            break
                if run.stderr:
                    print("  stderr:", run.stderr[:500])
    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
