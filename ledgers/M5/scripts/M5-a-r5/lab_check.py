import re, sys, html, subprocess
for lab in ["L01", "L02", "L03", "L04"]:
    page = open(f"course/modules/M/M5/{lab}.html", encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    twin = open(f"tests/labs/M5/lab-M5-{lab}-1.py", encoding="utf-8").read()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"tests/labs/M5/lab-M5-{lab}-1.py"], capture_output=True, text=True).stdout
    print(lab, "page_code==twin:", code.strip() == twin.strip(), "| expected==twin_stdout:", expected.strip() == out.strip(), "| lines:", len(out.strip().splitlines()))
