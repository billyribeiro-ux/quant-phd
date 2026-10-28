# Compares the page's embedded code and expected output (L07.html, L08.html) with the twins and with a fresh run.
import html, re, sys, subprocess
root = sys.argv[1]
pages = {"L07": ("course/modules/M/M7/L07.html", "tests/labs/M7/lab-M7-L07-1.py", "/tmp/M7-v/c5/out/L07-1.out"),
         "L08": ("course/modules/M/M7/L08.html", "tests/labs/M7/lab-M7-L08-1.py", "/tmp/M7-v/c5/out/L08-1.out")}
for k, (page, twin, outf) in pages.items():
    src = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    print(k, "code == twin (ignoring final newline):", code.rstrip("\n") == tw.rstrip("\n"))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(e.group(1))
    out = open(outf, encoding="utf-8").read()
    print(k, "expected == fresh twin run output:", exp.strip() == out.strip(), "lines", len(out.splitlines()))
