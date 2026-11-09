"""Round-15 verifier: for each E3 lab on pages L05-L08, compare the page code (HTML-unescaped) with the
twin file byte for byte, and the expected block with the twin's stdout under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in ("L05", "L06", "L07", "L08"):
    src = (root / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    sections = re.findall(
        r'<section class="lab" id="(lab-E3-[^"]+)".*?<code class="language-python" data-run>(.*?)</code></pre>'
        r'.*?<pre class="expected"[^>]*>(.*?)</pre>',
        src,
        re.S,
    )
    print(f"{page} labs found: {[s[0] for s in sections]}")
    for lab_id, code, expected in sections:
        twin = root / "tests/labs/E3" / f"{lab_id}.py"
        twin_text = twin.read_text(encoding="utf-8")
        page_code = html.unescape(code)
        same = page_code.rstrip("\n") == twin_text.rstrip("\n")
        run = subprocess.run(
            [str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin)],
            capture_output=True,
            text=True,
            cwd=root,
        )
        exp = html.unescape(expected)
        out_ok = run.stdout.rstrip("\n") == exp.rstrip("\n")
        print(
            f"{page} {lab_id} page_code_equals_twin={same} expected_equals_stdout={out_ok} "
            f"rc={run.returncode} stderr={run.stderr.strip()[:200]!r}"
        )
        if not out_ok:
            print("--- expected ---")
            print(exp)
            print("--- stdout ---")
            print(run.stdout)
