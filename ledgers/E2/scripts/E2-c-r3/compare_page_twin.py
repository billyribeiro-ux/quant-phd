import html, re, subprocess, sys, pathlib
for page in ("L07","L08","L09"):
    src = pathlib.Path(f"course/modules/E/E2/{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1))
    twin = pathlib.Path(f"tests/labs/E2/lab-E2-{page}-1.py").read_text(encoding="utf-8")
    out = subprocess.run([sys.executable,"-I","-W","error",f"tests/labs/E2/lab-E2-{page}-1.py"],capture_output=True,text=True).stdout
    print(page, "code==twin ignoring trailing ws:", code.rstrip()==twin.rstrip(), "| exp==out ignoring trailing ws:", exp.rstrip()==out.rstrip())
    print("  repr tail page:", repr(code[-12:]), " twin:", repr(twin[-12:]))
    print("  repr tail exp:", repr(exp[-12:]), " out:", repr(out[-12:]))
    print("  page ends with newline?", code.endswith("\n"), "exp endswith newline?", exp.endswith("\n"))
