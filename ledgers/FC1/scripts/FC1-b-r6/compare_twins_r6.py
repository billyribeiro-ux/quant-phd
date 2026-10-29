import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-FC1-b")
for lesson in ("L04", "L05"):
    src = (root / f"course/modules/FC/FC1/{lesson}.html").read_text()
    twin = (root / f"tests/labs/FC1/lab-FC1-{lesson}-1.py").read_text()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC1/lab-FC1-{lesson}-1.py")],
                       capture_output=True, text=True)
    print(lesson, "page_code==twin:", code.rstrip("\n") == twin.rstrip("\n"),
          "| rc:", r.returncode, "| stderr bytes:", len(r.stderr),
          "| expected==stdout (trailing newlines ignored):", exp.rstrip("\n") == r.stdout.rstrip("\n"))
