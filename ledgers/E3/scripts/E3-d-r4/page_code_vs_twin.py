"""Compare each project lab's data-run code (project.html) with its twin, and its expected block with the twin's output."""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab = f"lab-E3-project-{n}"
    m = re.search(rf'id="{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/E3/{lab}.py").read_text(encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E3/{lab}.py")], capture_output=True, text=True).stdout
    print(lab, "code==twin:", code.strip() == twin.strip(), "| expected==twin output:", expected.strip() == out.strip())
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
