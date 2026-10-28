import html, re, sys
root = sys.argv[1]
for t in ("L08", "L09", "L10"):
    page = open(f"{root}/course/modules/M/M4/{t}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/M4/lab-M4-{t}-1.py", encoding="utf-8").read()
    runs = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, flags=re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    code = html.unescape(re.sub(r'<[^>]+>', '', runs[0])) if runs else None
    out = html.unescape(re.sub(r'<[^>]+>', '', exps[0])) if exps else None
    print(t, "twin-equals-page-code", code is not None and code.strip()==twin.strip(), "runs", len(runs), "expected", len(exps),
          "code==twin", code is not None and code.strip() == twin.strip(),
          "twin_len", len(twin), "code_len", len(code) if code else None)
    if out is not None:
        open(f"/tmp/M4-v/c5/{t}-page-expected.txt", "w", encoding="utf-8").write(out)
