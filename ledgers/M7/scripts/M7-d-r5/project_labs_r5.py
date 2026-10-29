"""Extract the three project lab codes from project.html, run each with python -I -W error, compare with its expected block.

Lab 2 is run with its three blanks filled by the expressions its hypothesis paragraph describes.
Usage: python3 project_labs_r5.py <checkout-root> <scratch-dir>
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
text = (root / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
for i, (code, expected) in enumerate(blocks, 1):
    code = html.unescape(code)
    expected = html.unescape(expected).strip()
    if i == 2:
        code = code.replace("    residual = ___", "    residual = [GAMMA * sum(SIGMA[i][j] * w[j] for j in range(N)) - MU[i] + nu for i in range(N)]", 1)
        code = code.replace("    signs = ___", "    signs = [x >= 0 for x in lam]", 1)
        code = code.replace("    dual_feasible = ___", "    dual_feasible = all(signs)", 1)
    path = scratch / f"lab{i}.py"
    path.write_text(code, encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=False)
    print(f"lab{i}", "MATCH" if run.stdout.strip() == expected else "DIFF", run.returncode)
