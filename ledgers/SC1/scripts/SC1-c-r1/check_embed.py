"""Verify that each lab section in a page embeds its twin exactly and that the expected block equals the twin's output.

Usage: python -I ledgers/SC1/scripts/SC1-c-r1/check_embed.py  (run from the checkout root)
Reads only the repository files; writes nothing.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PYTHON = ROOT / ".venv" / "bin" / "python"
PAGES = {
    "L07": ("course/modules/SC/SC1/L07.html", "lab-SC1-L07-1"),
    "L08": ("course/modules/SC/SC1/L08.html", "lab-SC1-L08-1"),
}


def lab_section(page_text: str, lab_id: str) -> str:
    start = page_text.index(f'id="{lab_id}"')
    end = page_text.index("</section>", start)
    return page_text[start:end]


def main() -> int:
    failures = 0
    for page, (rel, lab_id) in PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        section = lab_section(text, lab_id)
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S)
        assert code and expected, page
        page_code = html.unescape(code.group(1))
        page_expected = html.unescape(expected.group(1))
        twin = (ROOT / "tests/labs/SC1" / f"{lab_id}.py").read_text(encoding="utf-8")
        code_equal = page_code == twin
        run = subprocess.run(
            [str(PYTHON), "-I", "-W", "error", str(ROOT / "tests/labs/SC1" / f"{lab_id}.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        out_equal = run.stdout == page_expected
        print(f"{page}: page code == twin: {code_equal}; expected == twin output: {out_equal}; exit={run.returncode}")
        if not code_equal:
            failures += 1
            print(f"  code lengths page={len(page_code)} twin={len(twin)}")
        if not out_equal:
            failures += 1
            print("  expected block:")
            print(page_expected)
            print("  twin output:")
            print(run.stdout)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
