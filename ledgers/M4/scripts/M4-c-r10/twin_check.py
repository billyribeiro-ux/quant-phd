import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for lab, page in (("L08", "L08"), ("L09", "L09"), ("L10", "L10")):
    src = (root / f"course/modules/M/M4/{page}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M4/lab-M4-{lab}-1.py").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    exp = html.unescape(exp).rstrip("\n")
    print(lab, "code==twin", code.strip("\n") == twin.strip("\n"), "len", len(code), len(twin))
    pathlib.Path(f"/tmp/m4c_r10_{lab}_exp.txt").write_text(exp + "\n")
