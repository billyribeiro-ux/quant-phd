"""Extract the three data-run code blocks and their expected blocks from project.html, and diff each against its twin."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-E3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for lab_id, code, expected in labs:
    n = lab_id[-1]
    code_t = html.unescape(code)
    exp_t = html.unescape(expected)
    (out / f"page_{n}.py").write_text(code_t, encoding="utf-8")
    (out / f"page_{n}.expected").write_text(exp_t, encoding="utf-8")
    twin = root / f"tests/labs/E3/lab-E3-project-{n}.py"
    same = twin.read_text(encoding="utf-8") == code_t
    print(f"{lab_id}: twin-identical={same} (twin {twin.name}, page code {len(code_t)} chars, twin {len(twin.read_text(encoding='utf-8'))} chars)")
print("labs found:", len(labs))
