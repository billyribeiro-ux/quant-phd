import html, re, sys
for n in ("01", "02", "03", "04"):
    page = open(f"course/modules/M/M4/L{n}.html", encoding="utf-8").read()
    twin = open(f"tests/labs/M4/lab-M4-L{n}-1.py", encoding="utf-8").read()
    out = open(f"ledgers/M4/scripts/M4-a-r14/twin-L{n}.out", encoding="utf-8").read()
    codes = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_ok = [html.unescape(c) == twin for c in codes]
    exp_ok = [html.unescape(e).strip("\n") == out.strip("\n") for e in exps]
    print(f"L{n}: code blocks {len(codes)} equal-twin {code_ok}; expected blocks {len(exps)} equal-output {exp_ok}")
