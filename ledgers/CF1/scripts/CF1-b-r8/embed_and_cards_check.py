"""Stdlib-only check: embedded lab code equals the twin; expected blocks equal twin stdout; card set of CF1 L03/L04 and duplicate scan."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
pages = {"L03": "lab-CF1-L03-1", "L04": "lab-CF1-L04-1"}
ok = True
for page, twin in pages.items():
    src = (ROOT / f"course/modules/CF/CF1/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin_src = (ROOT / f"tests/labs/CF1/{twin}.py").read_text(encoding="utf-8")
    same = code.strip() == twin_src.strip()
    print(f"{page}: embedded code equals twin (strip): {same}")
    ok &= same
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(e.group(1)).strip()
    printed = (OUT / f"{twin}.out").read_text(encoding="utf-8").strip()
    eq = expected == printed
    print(f"{page}: expected block equals twin stdout: {eq} ({len(expected.splitlines())} lines)")
    ok &= eq
cards = json.loads((ROOT / "course/modules/CF/CF1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "dup ids", len(ids) - len(set(ids)))
print("dup fronts", len(cards) - len({c["front"] for c in cards}), "dup backs", len(cards) - len({c["back"] for c in cards}))
print("L03/L04 cards", sorted(c["id"] for c in cards if c["lesson"] in ("L03", "L04")).__len__())
print("RESULT", "PASS" if ok else "FAIL")
