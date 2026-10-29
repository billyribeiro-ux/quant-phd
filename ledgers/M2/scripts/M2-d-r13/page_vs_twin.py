import html, re, sys
root = sys.argv[1]
for n in range(19, 25):
    page = open(f"{root}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    out = open(f"{root}/ledgers/M2/scripts/M2-d-r13/twin_L{n}.out", encoding="utf-8").read()
    print(f"L{n} code==twin: {code.rstrip() == twin.rstrip()} (len page {len(code)} twin {len(twin)}); expected==output: {html.unescape(exp.group(1)).strip() == out.strip()}")
