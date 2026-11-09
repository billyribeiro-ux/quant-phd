"""Round 1 closing delta (pin d9de2fe5): page code vs twin, and expected block vs twin stdout, for E3 L01-L04."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in ("L01", "L02", "L03", "L04"):
    src = (root / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    labs = re.findall(r'<section class="lab" id="(lab-E3-[^"]+)"(.*?)</section>', src, re.S)
    print(page, "lab sections:", [l[0] for l in labs])
    for lab_id, body in labs:
        m_code = re.search(r'<code class="language-python"[^>]*>(.*?)</code>', body, re.S)
        m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        twin = root / "tests/labs/E3" / f"{lab_id}.py"
        twin_text = twin.read_text(encoding="utf-8")
        page_code = html.unescape(m_code.group(1)) if m_code else None
        run = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin)],
                             capture_output=True, text=True, cwd=root)
        exp = html.unescape(m_exp.group(1)) if m_exp else None
        print(f"{page} {lab_id} code_equals_twin={page_code is not None and page_code.rstrip() == twin_text.rstrip()} "
              f"expected_equals_stdout={exp is not None and exp.rstrip() == run.stdout.rstrip()} rc={run.returncode} "
              f"stderr={run.stderr.strip()[:200]!r} stdout_lines={len(run.stdout.splitlines())}")
        if page == "L03" and exp is not None:
            print("L03 expected block:\n" + exp)
