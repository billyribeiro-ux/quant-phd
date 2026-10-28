# Compares each page's data-run code and expected output block with the lab twin and a fresh run.
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
py = str(root / ".venv/bin/python")
for n in ("L07", "L08", "L09"):
    page = (root / f"course/modules/M/M3/{n}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    twin = (root / f"tests/labs/M3/lab-M3-{n}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{n}-1.py")], capture_output=True, text=True).stdout
    print(n, "page code == twin:", code.strip() == twin.strip(), "| page expected == fresh run:", expected.strip() == run.strip())
    if code.strip() != twin.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]))
