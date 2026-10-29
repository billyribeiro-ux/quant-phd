import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for L in ["L09", "L10", "L11", "L12"]:
    page = (root / f"course/modules/M/M6/{L}.html").read_text()
    twin = (root / f"tests/labs/M6/lab-M6-{L}-1.py").read_text()
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(codes[0]) if codes else None
    exp = html.unescape(exps[0]) if exps else None
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M6/lab-M6-{L}-1.py")], capture_output=True, text=True).stdout
    print(L, "ncode", len(codes), "nexp", len(exps), "code==twin", code == twin, "exp==out", exp is not None and exp.rstrip("\n") == out.rstrip("\n"), "outlines", out.count("\n"))
