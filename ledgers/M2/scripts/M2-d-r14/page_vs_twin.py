import html, re, subprocess, sys
root = sys.argv[1]
for L in ["19","20","21","22","23","24"]:
    page = open(f"{root}/course/modules/M/M2/L{L}.html", encoding="utf-8").read()
    twin_path = f"{root}/tests/labs/M2/lab-M2-L{L}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1)) if m else None
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)) if e else None
    out = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True).stdout
    print(f"L{L}: code==twin {code is not None and code.strip()==twin.strip()}  expected==output {expected is not None and expected.strip()==out.strip()}  len(code)={len(code or '')}")
