"""Round-8 verifier check for M3 slice c: page lab code and expected block vs the lab twin, and twin output.

Usage: python -I ledgers/M3/scripts/M3-c-r8/twin_vs_page.py <repo_root>
Runs each twin under `python -I -W error` with cwd set to a fresh scratch directory under /tmp.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGES = {"L07": "lab-M3-L07-1", "L08": "lab-M3-L08-1", "L09": "lab-M3-L09-1"}


def section_parts(page_html: str, lab_id: str) -> tuple[str, str]:
    start = page_html.index(f'id="{lab_id}"')
    end = page_html.index("</section>", start)
    body = page_html[start:end]
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    assert code_m and exp_m, lab_id
    return html.unescape(code_m.group(1)), html.unescape(exp_m.group(1))


def main() -> None:
    for page, lab in PAGES.items():
        page_html = (ROOT / f"course/modules/M/M3/{page}.html").read_text(encoding="utf-8")
        page_code, page_expected = section_parts(page_html, lab)
        twin_path = ROOT / f"tests/labs/M3/{lab}.py"
        twin = twin_path.read_text(encoding="utf-8")
        print(f"{page} code == twin: {page_code.rstrip() == twin.rstrip()} (twin bytes {len(twin)}, page code bytes {len(page_code)})")
        with tempfile.TemporaryDirectory(dir="/tmp", prefix="m3c_r8_") as scratch:
            run = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin_path)],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=120,
            )
        out = run.stdout
        print(f"{page} twin exit={run.returncode} stderr_bytes={len(run.stderr)}")
        print(f"{page} expected == output: {page_expected.strip() == out.strip()}")
        if page_expected.strip() != out.strip():
            print("--- expected")
            print(page_expected)
            print("--- output")
            print(out)
        print(f"{page} twin last line: {twin.rstrip().splitlines()[-1]!r}")


if __name__ == "__main__":
    main()
