"""Compare data-run code block and expected block of L03/L04 pages with the twins and their live output (LX1-b r7)."""
import html, re, sys, subprocess, pathlib
root = pathlib.Path(sys.argv[1])
for lid in ("L03", "L04"):
    page = (root / f"course/modules/LX/LX1/{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(e.group(1))
    twin = (root / f"tests/labs/LX1/lab-LX1-{lid}-1.py").read_text(encoding="utf-8")
    print(lid, "page code == twin:", code == twin, "| code len", len(code), len(twin), "| expected lines", expected.count("\n"))
    if code != twin:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]))
    run = subprocess.run([sys.executable, "-I", "-W", "error", "-c", code], capture_output=True, text=True, cwd=f"/tmp/lx1b-r7/{lid}")
    out = run.stdout
    print(lid, "page code exit", run.returncode, "| stderr:", run.stderr.strip()[:200])
    print(lid, "expected == live output:", expected.strip() == out.strip())
    if expected.strip() != out.strip():
        print("\n".join(list(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), "expected", "output", lineterm=""))[:40]))
