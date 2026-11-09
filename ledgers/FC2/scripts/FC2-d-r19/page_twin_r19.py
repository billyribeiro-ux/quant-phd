import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC2/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
print("data-run blocks:", len(blocks))
for i, b in enumerate(blocks, 1):
    code = html.unescape(b)
    first = code.splitlines()[0][:70]
    twins = [root / f"tests/labs/FC2/lab-FC2-project-{i}.py"]
    t = twins[0].read_text(encoding="utf-8")
    print(i, first, "| page==twin:", code.rstrip("\n") == t.rstrip("\n"), "| len", len(code), len(t), "| lines", code.count("\n"), t.count("\n"))
