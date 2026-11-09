import re, html, subprocess, sys
root = "/Users/billyribeiro/.fanout/wt/verifyS7-FC2-b"
ok = True
for lid in ("L04", "L05", "L06"):
    page = open(f"{root}/course/modules/FC/FC2/{lid}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/FC2/lab-FC2-{lid}-1.py", encoding="utf-8").read()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(e.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/FC2/lab-FC2-{lid}-1.py"],
                         capture_output=True, text=True, cwd=root).stdout
    print(lid, "code==twin:", code.strip("\n") == twin.strip("\n"), "len", len(code), len(twin),
          "| expected==stdout:", exp.strip("\n") == out.strip("\n"), "lines", len(out.splitlines()))
    ok = ok and code.strip("\n") == twin.strip("\n") and exp.strip("\n") == out.strip("\n")
print("ALL", ok)
