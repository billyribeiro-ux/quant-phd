# Compares the embedded lab code and expected block of L05-L07 with the twins and with a fresh run.
import html, re, subprocess, sys
root = sys.argv[1]
py = sys.argv[2]
for p in ("L05", "L06", "L07"):
    src = open(f"{root}/course/modules/M/M4/{p}.html").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1))
    twin = open(f"{root}/tests/labs/M4/lab-M4-{p}-1.py").read()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)).strip()
    out = subprocess.run([py, "-I", "-W", "error", f"{root}/tests/labs/M4/lab-M4-{p}-1.py"], capture_output=True, text=True).stdout.strip()
    print(p, "code==twin", code.rstrip() == twin.rstrip(), "expected==output", exp == out)
