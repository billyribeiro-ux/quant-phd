import html, re, sys
from pathlib import Path
page = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-[^"]+)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    (out / f"{lab_id}.py").write_text(html.unescape(code), encoding="utf-8")
    (out / f"{lab_id}.expected").write_text(html.unescape(expected), encoding="utf-8")
    print(lab_id, len(code))
