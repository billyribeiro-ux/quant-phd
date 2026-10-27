"""Round 28: every S7 lab twin (tests/labs/S7/lab-S7-*.py) and every solution twin (sol-S7-*.py) equals the code block on its page
(after HTML unescape and stripping surrounding newlines). A lab block is the first python code block after id="<lab id>".
Usage: python -I lab_embed_r28B.py <checkout>"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = {p: p.read_text(encoding="utf-8") for p in sorted((root / "course/modules/S/S7").glob("*.html"))}
ok = bad = 0
for twin in sorted((root / "tests/labs/S7").glob("*-S7-*.py")):
    tid = twin.stem
    src_all = twin.read_text(encoding="utf-8").strip("\n")
    found = None
    for page, text in pages.items():
        if tid.startswith("lab-"):
            m = re.search(r'id="%s"' % re.escape(tid), text)
            if not m:
                continue
            code = re.search(r'<code class="language-python"[^>]*>(.*?)</code>', text[m.end():], re.S)
        else:
            code = re.search(r'<code class="language-python"[^>]*data-check="%s"[^>]*>(.*?)</code>' % re.escape(tid), text, re.S)
        if code:
            found = (page.name, html.unescape(code.group(1)).strip("\n"))
            break
    if found is None:
        bad += 1; print("NO BLOCK", tid); continue
    if found[1] == src_all:
        ok += 1
    else:
        bad += 1; print("MISMATCH", tid, found[0])
print(f"S7 twins compared with their page blocks: {ok + bad}; identical: {ok}; mismatches or missing: {bad}")
