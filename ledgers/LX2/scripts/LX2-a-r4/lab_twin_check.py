"""For each LX2 page in the slice: compare the page's runnable code block with the lab twin, and the
expected block with the twin's output run under python -I -W error. Usage: python3 -I lab_twin_check.py <repo_root> <page> <lab_id>..."""

import html
import re
import subprocess
import sys
from pathlib import Path


def blocks(page_text: str) -> tuple[list[str], list[str]]:
    code = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page_text, flags=re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page_text, flags=re.S)
    return [html.unescape(c) for c in code], [html.unescape(e) for e in expected]


def main() -> None:
    root = Path(sys.argv[1])
    page = sys.argv[2]
    lab_ids = sys.argv[3:]
    text = (root / "course/modules/LX/LX2" / f"{page}.html").read_text(encoding="utf-8")
    code_blocks, expected_blocks = blocks(text)
    print(f"page {page}: code blocks {len(code_blocks)}, expected blocks {len(expected_blocks)}")
    for lab_id, code, expected in zip(lab_ids, code_blocks, expected_blocks):
        twin = (root / "tests/labs/LX2" / f"{lab_id}.py").read_text(encoding="utf-8")
        same = code.strip() == twin.strip()
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(root / "tests/labs/LX2" / f"{lab_id}.py")],
            capture_output=True, text=True, timeout=120,
        )
        out_ok = run.stdout.strip() == expected.strip()
        print(f"{lab_id}: page_code_equals_twin={same} exit={run.returncode} expected_equals_output={out_ok}")
        if not out_ok:
            print("--- stdout ---"); print(run.stdout); print("--- stderr ---"); print(run.stderr)


if __name__ == "__main__":
    main()
