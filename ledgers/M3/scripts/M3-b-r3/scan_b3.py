"""Round 3, M3-b: embedded-output and code-block comparison, scope-word and process-word scan for L04-L06."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = str(ROOT / ".venv" / "bin" / "python")
WORDS = r"\b(only|always|every|any|same|drives|offsets|raises|roughly|about|historically|typically|usually|generally|normally|often|most|half|all|build|builder|round|verifier)\b|\.\.\.|…"

for lesson in ["L04", "L05", "L06"]:
    page = (ROOT / f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1)).strip()
    twin = (ROOT / f"tests/labs/M3/lab-M3-{lesson}-1.py").read_text(encoding="utf-8").strip()
    out = subprocess.run(
        [PY, "-I", "-W", "error", f"tests/labs/M3/lab-M3-{lesson}-1.py"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    print(f"{lesson}: embedded output equals fresh run: {expected == out}; embedded code equals twin: {code == twin}")
    visible = re.sub(r"<pre.*?</pre>", "", page, flags=re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
    hits = [re.sub(r"\s+", " ", visible[max(0, m.start() - 40) : m.end() + 25]) for m in re.finditer(WORDS, visible, re.I)]
    print(f"{lesson}: scope, banned and process word hits outside code blocks: {len(hits)}")
    for h in hits:
        print("   ", h)
