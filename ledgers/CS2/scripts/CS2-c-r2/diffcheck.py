import html, re, difflib, sys
from pathlib import Path
root = Path("/Users/billyribeiro/.fanout/wt/verifyS2-CS2-c")
for page, html_rel, twin_rel in [("L09","course/modules/CS/CS2/L09.html","tests/labs/CS2/lab-CS2-L09-1.py"),("L10","course/modules/CS/CS2/L10.html","tests/labs/CS2/lab-CS2-L10-1.py"),("L11","course/modules/CS/CS2/L11.html","tests/labs/CS2/lab-CS2-L11-1.py")]:
    t = (root/html_rel).read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S).group(1))
    twin = (root/twin_rel).read_text(encoding="utf-8")
    d = list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))
    print(page, "lines equal:", twin.splitlines()==code.splitlines(), "| ends-with-newline twin:", twin.endswith("\n"), "page:", code.endswith("\n"))
    print("".join(d) if d else "(no line diff)")
