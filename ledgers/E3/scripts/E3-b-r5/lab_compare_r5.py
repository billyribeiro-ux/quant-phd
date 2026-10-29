import re, html, subprocess, sys
root = sys.argv[1]
for n in ("04", "05", "06"):
    page = open(f"{root}/course/modules/E/E3/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/E3/lab-E3-L{n}-1.py", encoding="utf-8").read()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    if exp is None:
        exp = re.search(r'<pre[^>]*expected[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", exp.group(1))) if exp else None
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E3/lab-E3-L{n}-1.py"],
                         capture_output=True, text=True).stdout
    print(n, "embedded code == twin:", code.strip() == twin.strip(),
          "| expected == twin stdout:", (expected or "").strip() == out.strip(),
          "| expected present:", expected is not None)
