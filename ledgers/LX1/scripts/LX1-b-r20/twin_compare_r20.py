"""Round 20: page lab code equals the lab twin (strict and trailing-newline), and the page expected block equals the
twin's stdout captured by a run under python -I -W error (out/twin_L0n.out, minus the trailing exit line).
Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/twin_compare_r20.py
"""
import difflib
import html
import re
from pathlib import Path

ROOT = Path(".")
OUT = ROOT / "ledgers/LX1/scripts/LX1-b-r20/out"
CODE = re.compile(r'<code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
status = 0
for lesson in ("L01", "L03", "L04"):
    page = (ROOT / f"course/modules/LX/LX1/{lesson}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-{lesson}-1.py").read_text(encoding="utf-8")
    m = CODE.search(page)
    code = html.unescape(m.group(1)) if m else None
    same = code is not None and code.rstrip("\n") == twin.rstrip("\n")
    print(f"{lesson}: page code equals twin (trailing newline stripped): {same}; strict byte equality: {code == twin}")
    if not same:
        status = 1
        for line in list(difflib.unified_diff(twin.splitlines(), (code or "").splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    e = EXPECTED.search(page)
    expected = html.unescape(e.group(1)) if e else None
    lines = (OUT / f"twin_{lesson}.out").read_text(encoding="utf-8").splitlines()
    actual = "\n".join(l for l in lines if not l.startswith("exit=")) + "\n"
    ok = expected is not None and expected.rstrip("\n") == actual.rstrip("\n")
    print(f"{lesson}: expected block equals twin stdout: {ok} (expected lines {len(expected.splitlines())}, actual lines {len(actual.splitlines())})")
    if not ok:
        status = 1
print("STATUS", status)
