"""Extract the data-run code blocks and expected blocks from M7 project.html; compare with the twins."""
import html, re, sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(blocks), "expected blocks:", len(expected))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for i, b in enumerate(blocks, 1):
    (out / f"page_lab{i}.py").write_text(html.unescape(b), encoding="utf-8")
for i, b in enumerate(expected, 1):
    (out / f"page_expected{i}.txt").write_text(html.unescape(b) + "\n", encoding="utf-8")
for i in range(1, 4):
    twin = (root / f"tests/labs/M7/lab-M7-project-{i}.py").read_text(encoding="utf-8")
    page_code = html.unescape(blocks[i - 1])
    print(f"lab{i}: page_code == twin:", page_code.strip() == twin.strip(), "lengths", len(page_code), len(twin))
