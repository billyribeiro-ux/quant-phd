import html, re, sys, subprocess
from pathlib import Path
root = Path(sys.argv[1])
for page, twin in [("L01", "lab-CF8-L01-1"), ("L02", "lab-CF8-L02-1")]:
    text = (root / "course/modules/CF/CF8" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    tw = (root / "tests/labs/CF8" / f"{twin}.py").read_text(encoding="utf-8")
    print(page, "code==twin:", code.strip() == tw.strip(), len(code), len(tw))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/CF8" / f"{twin}.py")],
                         capture_output=True, text=True).stdout
    print(page, "expected==output:", expected.strip() == out.strip())
